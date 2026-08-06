"""Discrete two-lognormal mixtures for complete avalanche-size distributions."""

from __future__ import annotations

from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy import optimize, special

from .models import (
    ModelFit,
    _cutoff_log_normalization,
    _ks_from_cdf,
    _log_difference,
    _lognormal_log_probabilities,
    _tail_arrays,
    fit_lognormal,
    fit_cutoff_power_law,
)
from .power_law import Histogram
from .gof import sample_power_law_counts
from .alternative_gof import _sample_cutoff_counts


def _component_cdf(
    sizes: np.ndarray, *, xmin: int, mu: float, sigma: float
) -> tuple[np.ndarray, np.ndarray]:
    boundary = (np.log(xmin - 0.5) - mu) / sigma
    log_survival_boundary = special.log_ndtr(-boundary)
    upper_after = (np.log(sizes + 0.5) - mu) / sigma
    upper_before = (np.log(sizes - 0.5) - mu) / sigma
    normalization = np.full(sizes.shape, log_survival_boundary)
    after = np.exp(
        _log_difference(normalization, special.log_ndtr(-upper_after))
        - log_survival_boundary
    )
    before = np.exp(
        _log_difference(normalization, special.log_ndtr(-upper_before))
        - log_survival_boundary
    )
    return after, before


def mixture_log_probabilities(
    sizes: np.ndarray,
    *,
    xmin: int,
    weight_small: float,
    mu_small: float,
    sigma_small: float,
    mu_large: float,
    sigma_large: float,
) -> np.ndarray:
    """Log PMF of a two-component, integer-binned truncated lognormal mixture."""
    if not 0.0 < weight_small < 1.0:
        raise ValueError("mixture weight must lie strictly between zero and one")
    first = _lognormal_log_probabilities(
        sizes, xmin=xmin, mu=mu_small, sigma=sigma_small
    )
    second = _lognormal_log_probabilities(
        sizes, xmin=xmin, mu=mu_large, sigma=sigma_large
    )
    return np.logaddexp(
        np.log(weight_small) + first,
        np.log1p(-weight_small) + second,
    )


def cutoff_lognormal_log_probabilities(
    sizes: np.ndarray,
    *,
    xmin: int,
    weight_small: float,
    alpha: float,
    rate: float,
    mu_large: float,
    sigma_large: float,
) -> np.ndarray:
    """Log PMF of a decreasing cutoff component plus a discrete lognormal."""
    if not 0.0 < weight_small < 1.0 or alpha < 0.0 or rate < 0.0:
        raise ValueError("invalid cutoff-lognormal mixture parameters")
    cutoff = (
        -alpha * np.log(sizes / float(xmin))
        - rate * (sizes - xmin)
        - _cutoff_log_normalization(alpha, rate, xmin)
    )
    lognormal = _lognormal_log_probabilities(
        sizes, xmin=xmin, mu=mu_large, sigma=sigma_large
    )
    return np.logaddexp(
        np.log(weight_small) + cutoff,
        np.log1p(-weight_small) + lognormal,
    )


def _weighted_log_moments(
    sizes: np.ndarray, frequencies: np.ndarray
) -> tuple[float, float]:
    logs = np.log(sizes.astype(float))
    mean = float(np.average(logs, weights=frequencies))
    sigma = float(np.sqrt(np.average((logs - mean) ** 2, weights=frequencies)))
    return mean, max(sigma, 0.03)


def fit_two_lognormal_mixture(
    histogram: Histogram,
    xmin: int = 2,
    *,
    initial: dict[str, float] | None = None,
) -> ModelFit:
    """Fit a discrete two-lognormal mixture by exact histogram likelihood."""
    sizes, frequencies = _tail_arrays(histogram, xmin)
    n = int(frequencies.sum())
    maximum = int(sizes[-1])

    def unpack(parameters: np.ndarray) -> tuple[float, float, float, float, float]:
        eta, first_mu, first_log_sigma, second_mu, second_log_sigma = parameters
        weight = float(special.expit(eta))
        return (
            weight,
            float(first_mu),
            float(np.exp(first_log_sigma)),
            float(second_mu),
            float(np.exp(second_log_sigma)),
        )

    def objective(parameters: np.ndarray) -> float:
        weight, first_mu, first_sigma, second_mu, second_sigma = unpack(parameters)
        log_probabilities = mixture_log_probabilities(
            sizes,
            xmin=xmin,
            weight_small=weight,
            mu_small=first_mu,
            sigma_small=first_sigma,
            mu_large=second_mu,
            sigma_large=second_sigma,
        )
        if not np.all(np.isfinite(log_probabilities)):
            return float("inf")
        value = -float(np.dot(frequencies, log_probabilities))
        return value if np.isfinite(value) else float("inf")

    if initial is None:
        cumulative = np.cumsum(frequencies, dtype=np.int64)
        starts: list[tuple[float, float, float, float, float]] = []
        for probability in (0.90, 0.95, 0.98, 0.985, 0.99, 0.995):
            split_index = int(np.searchsorted(cumulative, probability * n))
            split_index = min(max(split_index, 1), sizes.size - 2)
            first_mu, first_sigma = _weighted_log_moments(
                sizes[: split_index + 1], frequencies[: split_index + 1]
            )
            second_mu, second_sigma = _weighted_log_moments(
                sizes[split_index + 1 :], frequencies[split_index + 1 :]
            )
            first_weight = float(cumulative[split_index] / n)
            starts.append(
                (
                    special.logit(np.clip(first_weight, 1e-5, 1.0 - 1e-5)),
                    first_mu,
                    np.log(first_sigma),
                    second_mu,
                    np.log(second_sigma),
                )
            )
    else:
        starts = [
            (
                special.logit(initial["weight_small"]),
                initial["mu_small"],
                np.log(initial["sigma_small"]),
                initial["mu_large"],
                np.log(initial["sigma_large"]),
            )
        ]

    mu_lower = np.log(max(0.51, xmin - 0.49)) - 20.0
    mu_upper = np.log(maximum + 0.5) + 5.0
    bounds = (
        (-14.0, 14.0),
        (mu_lower, mu_upper),
        (-5.0, 4.0),
        (mu_lower, mu_upper),
        (-5.0, 4.0),
    )
    results = [
        optimize.minimize(
            objective,
            np.asarray(start),
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 2000, "ftol": 1e-13, "gtol": 1e-7},
        )
        for start in starts
    ]
    valid = [result for result in results if result.success and np.isfinite(result.fun)]
    if not valid:
        if initial is not None:
            return fit_two_lognormal_mixture(histogram, xmin, initial=None)
        raise RuntimeError("all two-lognormal mixture optimizations failed")
    best = min(valid, key=lambda result: result.fun)
    weight, first_mu, first_sigma, second_mu, second_sigma = unpack(best.x)
    if first_mu > second_mu:
        weight = 1.0 - weight
        first_mu, second_mu = second_mu, first_mu
        first_sigma, second_sigma = second_sigma, first_sigma

    first_after, first_before = _component_cdf(
        sizes, xmin=xmin, mu=first_mu, sigma=first_sigma
    )
    second_after, second_before = _component_cdf(
        sizes, xmin=xmin, mu=second_mu, sigma=second_sigma
    )
    cdf_after = weight * first_after + (1.0 - weight) * second_after
    cdf_before = weight * first_before + (1.0 - weight) * second_before
    return ModelFit(
        model="two_lognormal_mixture",
        xmin=xmin,
        parameters={
            "weight_small": weight,
            "mu_small": first_mu,
            "sigma_small": first_sigma,
            "mu_large": second_mu,
            "sigma_large": second_sigma,
        },
        log_likelihood=-float(best.fun),
        ks=_ks_from_cdf(frequencies, cdf_after, cdf_before),
        n_tail=n,
        parameter_count=5,
    )


def fit_cutoff_lognormal_mixture(
    histogram: Histogram,
    xmin: int = 2,
    *,
    initial: dict[str, float] | None = None,
) -> ModelFit:
    """Fit a decreasing cutoff-power-law plus discrete-lognormal mixture."""
    sizes, frequencies = _tail_arrays(histogram, xmin)
    n = int(frequencies.sum())

    def unpack(parameters: np.ndarray) -> tuple[float, float, float, float, float]:
        eta, log_alpha, log_rate, mu_large, log_sigma_large = parameters
        return (
            float(special.expit(eta)),
            float(np.exp(log_alpha)),
            float(np.exp(log_rate)),
            float(mu_large),
            float(np.exp(log_sigma_large)),
        )

    def objective(parameters: np.ndarray) -> float:
        weight, alpha, rate, mu_large, sigma_large = unpack(parameters)
        log_probabilities = cutoff_lognormal_log_probabilities(
            sizes,
            xmin=xmin,
            weight_small=weight,
            alpha=alpha,
            rate=rate,
            mu_large=mu_large,
            sigma_large=sigma_large,
        )
        if not np.all(np.isfinite(log_probabilities)):
            return float("inf")
        return -float(np.dot(frequencies, log_probabilities))

    if initial is None:
        cumulative = np.cumsum(frequencies, dtype=np.int64)
        starts: list[tuple[float, float, float, float, float]] = []
        for probability in (0.95, 0.98, 0.985, 0.99, 0.995):
            split_index = int(np.searchsorted(cumulative, probability * n))
            split_index = min(max(split_index, 1), sizes.size - 2)
            small_histogram = {
                int(size): int(count)
                for size, count in zip(
                    sizes[: split_index + 1],
                    frequencies[: split_index + 1],
                    strict=True,
                )
            }
            small_fit = fit_cutoff_power_law(small_histogram, xmin)
            large_mu, large_sigma = _weighted_log_moments(
                sizes[split_index + 1 :], frequencies[split_index + 1 :]
            )
            weight = float(cumulative[split_index] / n)
            starts.append(
                (
                    special.logit(np.clip(weight, 1e-5, 1.0 - 1e-5)),
                    np.log(max(small_fit.parameters["alpha"], 1e-6)),
                    np.log(max(small_fit.parameters["lambda"], 1e-7)),
                    large_mu,
                    np.log(large_sigma),
                )
            )
    else:
        starts = [
            (
                special.logit(initial["weight_small"]),
                np.log(initial["alpha"]),
                np.log(max(initial["lambda"], np.exp(-16.0))),
                initial["mu_large"],
                np.log(initial["sigma_large"]),
            )
        ]

    bounds = (
        (-14.0, 14.0),
        (-14.0, np.log(100.0)),
        (-16.0, 3.0),
        (np.log(xmin - 0.5) - 5.0, np.log(int(sizes[-1]) + 0.5) + 5.0),
        (-5.0, 4.0),
    )
    results = [
        optimize.minimize(
            objective,
            np.asarray(start),
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 2000, "ftol": 1e-13, "gtol": 1e-7},
        )
        for start in starts
    ]
    valid = [result for result in results if result.success and np.isfinite(result.fun)]
    if not valid:
        if initial is not None:
            return fit_cutoff_lognormal_mixture(histogram, xmin, initial=None)
        raise RuntimeError("all cutoff-lognormal mixture optimizations failed")
    best = min(valid, key=lambda result: result.fun)
    weight, alpha, rate, mu_large, sigma_large = unpack(best.x)
    if best.x[2] <= -16.0 + 1e-6:
        rate = 0.0

    log_normalization = _cutoff_log_normalization(alpha, rate, xmin)
    full_support = np.arange(xmin, int(sizes[-1]) + 1)
    cutoff_pmf = np.exp(
        -alpha * np.log(full_support / float(xmin))
        - rate * (full_support - xmin)
        - log_normalization
    )
    cutoff_cdf = np.cumsum(cutoff_pmf)
    cutoff_after = cutoff_cdf[sizes - xmin]
    cutoff_before = np.where(sizes == xmin, 0.0, cutoff_cdf[sizes - xmin - 1])
    large_after, large_before = _component_cdf(
        sizes, xmin=xmin, mu=mu_large, sigma=sigma_large
    )
    cdf_after = weight * cutoff_after + (1.0 - weight) * large_after
    cdf_before = weight * cutoff_before + (1.0 - weight) * large_before
    return ModelFit(
        model="cutoff_lognormal_mixture",
        xmin=xmin,
        parameters={
            "weight_small": weight,
            "alpha": alpha,
            "lambda": rate,
            "mu_large": mu_large,
            "sigma_large": sigma_large,
        },
        log_likelihood=-float(best.fun),
        ks=_ks_from_cdf(frequencies, cdf_after, cdf_before),
        n_tail=n,
        parameter_count=5,
    )
def sample_two_lognormal_counts(
    n: int, fit: ModelFit, *, rng: np.random.Generator
) -> dict[int, int]:
    """Sample exactly from the fitted integer-binned truncated mixture."""
    if fit.model != "two_lognormal_mixture":
        raise ValueError("fit must be a two-lognormal mixture")
    parameters = fit.parameters
    first_n = int(rng.binomial(n, parameters["weight_small"]))

    def sample_component(count: int, mu: float, sigma: float) -> dict[int, int]:
        if count == 0:
            return {}
        boundary = (np.log(fit.xmin - 0.5) - mu) / sigma
        boundary_cdf = special.ndtr(boundary)
        target_cdf = boundary_cdf + (1.0 - boundary_cdf) * (1.0 - 1e-13)
        target_cdf = min(float(target_cdf), np.nextafter(1.0, 0.0))
        upper = int(np.ceil(np.exp(mu + sigma * special.ndtri(target_cdf)) + 0.5))
        if upper - fit.xmin > 10_000_000:
            raise RuntimeError("mixture sampling table exceeded ten million sizes")
        support = np.arange(fit.xmin, max(fit.xmin + 1, upper + 1))
        probabilities = np.exp(
            _lognormal_log_probabilities(
                support, xmin=fit.xmin, mu=mu, sigma=sigma
            )
        )
        probabilities /= probabilities.sum()
        allocations = rng.multinomial(count, probabilities)
        nonzero = np.flatnonzero(allocations)
        return {
            int(fit.xmin + index): int(allocations[index]) for index in nonzero
        }

    first = sample_component(
        first_n, parameters["mu_small"], parameters["sigma_small"]
    )
    second = sample_component(
        n - first_n, parameters["mu_large"], parameters["sigma_large"]
    )
    combined = dict(first)
    for size, count in second.items():
        combined[size] = combined.get(size, 0) + count
    return combined


def _sample_lognormal_counts(
    n: int,
    *,
    xmin: int,
    mu: float,
    sigma: float,
    rng: np.random.Generator,
) -> dict[int, int]:
    if n == 0:
        return {}
    boundary = (np.log(xmin - 0.5) - mu) / sigma
    boundary_cdf = special.ndtr(boundary)
    target_cdf = boundary_cdf + (1.0 - boundary_cdf) * (1.0 - 1e-13)
    target_cdf = min(float(target_cdf), np.nextafter(1.0, 0.0))
    upper = int(np.ceil(np.exp(mu + sigma * special.ndtri(target_cdf)) + 0.5))
    if upper - xmin > 10_000_000:
        raise RuntimeError("lognormal sampling table exceeded ten million sizes")
    support = np.arange(xmin, max(xmin + 1, upper + 1))
    probabilities = np.exp(
        _lognormal_log_probabilities(support, xmin=xmin, mu=mu, sigma=sigma)
    )
    probabilities /= probabilities.sum()
    allocations = rng.multinomial(n, probabilities)
    return {
        int(xmin + index): int(allocations[index])
        for index in np.flatnonzero(allocations)
    }


def sample_cutoff_lognormal_counts(
    n: int, fit: ModelFit, *, rng: np.random.Generator
) -> dict[int, int]:
    """Sample the decreasing-body plus lognormal-extreme mixture."""
    if fit.model != "cutoff_lognormal_mixture":
        raise ValueError("fit must be a cutoff-lognormal mixture")
    parameters = fit.parameters
    small_n = int(rng.binomial(n, parameters["weight_small"]))
    if parameters["lambda"] == 0.0:
        small = sample_power_law_counts(
            small_n,
            xmin=fit.xmin,
            alpha=parameters["alpha"],
            rng=rng,
        )
    else:
        component_fit = ModelFit(
            model="cutoff_power_law",
            xmin=fit.xmin,
            parameters={
                "alpha": parameters["alpha"],
                "lambda": parameters["lambda"],
            },
            log_likelihood=0.0,
            ks=0.0,
            n_tail=small_n,
            parameter_count=2,
        )
        small = _sample_cutoff_counts(small_n, component_fit, rng=rng)
    large = _sample_lognormal_counts(
        n - small_n,
        xmin=fit.xmin,
        mu=parameters["mu_large"],
        sigma=parameters["sigma_large"],
        rng=rng,
    )
    combined = dict(small)
    for size, count in large.items():
        combined[size] = combined.get(size, 0) + count
    return combined


def _one_cutoff_lognormal_replica(
    arguments: tuple[ModelFit, int]
) -> float:
    observed, seed = arguments
    synthetic = sample_cutoff_lognormal_counts(
        observed.n_tail, observed, rng=np.random.default_rng(seed)
    )
    return fit_cutoff_lognormal_mixture(
        synthetic, observed.xmin, initial=observed.parameters
    ).ks


def cutoff_lognormal_goodness_of_fit(
    histogram: Histogram,
    *,
    xmin: int = 2,
    replicates: int = 2500,
    seed: int = 12738,
    workers: int = 1,
) -> MixtureBootstrapResult:
    """Absolute parametric GOF with full mixture refitting per replica."""
    if replicates < 1 or workers < 1:
        raise ValueError("replicates and workers must be positive")
    observed = fit_cutoff_lognormal_mixture(histogram, xmin)
    seeds = [
        int(child.generate_state(1, dtype=np.uint64)[0])
        for child in np.random.SeedSequence(seed).spawn(replicates)
    ]
    arguments = [(observed, child_seed) for child_seed in seeds]
    if workers == 1:
        synthetic_ks = [_one_cutoff_lognormal_replica(item) for item in arguments]
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            synthetic_ks = list(
                executor.map(
                    _one_cutoff_lognormal_replica,
                    arguments,
                    chunksize=max(1, replicates // (workers * 8)),
                )
            )
    exceedances = sum(value >= observed.ks for value in synthetic_ks)
    p_value = exceedances / replicates
    return MixtureBootstrapResult(
        observed=observed,
        p_value=p_value,
        exceedances=exceedances,
        replicates=replicates,
        monte_carlo_standard_error=float(
            np.sqrt(p_value * (1.0 - p_value) / replicates)
        ),
        synthetic_ks=tuple(synthetic_ks),
    )


@dataclass(frozen=True)
class MixtureBootstrapResult:
    observed: ModelFit
    p_value: float
    exceedances: int
    replicates: int
    monte_carlo_standard_error: float
    synthetic_ks: tuple[float, ...]


def mixture_goodness_of_fit(
    histogram: Histogram,
    *,
    xmin: int = 2,
    replicates: int = 2500,
    seed: int = 12738,
) -> MixtureBootstrapResult:
    """Parametric KS bootstrap with a complete mixture refit per replica."""
    if replicates < 1:
        raise ValueError("replicates must be positive")
    observed = fit_two_lognormal_mixture(histogram, xmin)
    rng = np.random.default_rng(seed)
    synthetic_ks: list[float] = []
    for _ in range(replicates):
        synthetic = sample_two_lognormal_counts(observed.n_tail, observed, rng=rng)
        fitted = fit_two_lognormal_mixture(
            synthetic, xmin, initial=observed.parameters
        )
        synthetic_ks.append(fitted.ks)
    exceedances = sum(value >= observed.ks for value in synthetic_ks)
    p_value = exceedances / replicates
    return MixtureBootstrapResult(
        observed=observed,
        p_value=p_value,
        exceedances=exceedances,
        replicates=replicates,
        monte_carlo_standard_error=float(
            np.sqrt(p_value * (1.0 - p_value) / replicates)
        ),
        synthetic_ks=tuple(synthetic_ks),
    )


def compare_single_to_mixture(
    histogram: Histogram, *, xmin: int = 2
) -> tuple[ModelFit, ModelFit, float, float, float]:
    """Return single fit, mixture fit, LR, delta-AIC and delta-BIC."""
    single = fit_lognormal(histogram, xmin)
    mixture = fit_two_lognormal_mixture(histogram, xmin)
    likelihood_ratio = 2.0 * (mixture.log_likelihood - single.log_likelihood)
    single_aic = 2 * single.parameter_count - 2 * single.log_likelihood
    mixture_aic = 2 * mixture.parameter_count - 2 * mixture.log_likelihood
    single_bic = single.parameter_count * np.log(single.n_tail) - 2 * single.log_likelihood
    mixture_bic = mixture.parameter_count * np.log(mixture.n_tail) - 2 * mixture.log_likelihood
    return (
        single,
        mixture,
        likelihood_ratio,
        float(single_aic - mixture_aic),
        float(single_bic - mixture_bic),
    )

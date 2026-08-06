"""Competing discrete models on a common power-law-selected tail."""

from __future__ import annotations

from dataclasses import dataclass

import mpmath
import numpy as np
from scipy import optimize, special

from .power_law import Histogram, PowerLawFit, fit_alpha, histogram_arrays


@dataclass(frozen=True)
class ModelFit:
    model: str
    xmin: int
    parameters: dict[str, float]
    log_likelihood: float
    ks: float
    n_tail: int
    parameter_count: int


def _tail_arrays(histogram: Histogram, xmin: int) -> tuple[np.ndarray, np.ndarray]:
    sizes, frequencies = histogram_arrays(histogram)
    selected = sizes >= xmin
    if not np.any(selected):
        raise ValueError("empty model-fitting tail")
    return sizes[selected], frequencies[selected]


def _ks_from_cdf(
    frequencies: np.ndarray, model_after: np.ndarray, model_before: np.ndarray
) -> float:
    n = int(frequencies.sum())
    after_empirical = np.cumsum(frequencies, dtype=np.int64) / n
    before_empirical = (np.cumsum(frequencies) - frequencies) / n
    return float(
        max(
            np.max(np.abs(after_empirical - model_after)),
            np.max(np.abs(before_empirical - model_before)),
        )
    )


def fit_power_law_model(histogram: Histogram, xmin: int) -> ModelFit:
    sizes, frequencies = _tail_arrays(histogram, xmin)
    alpha, log_likelihood = fit_alpha(histogram, xmin)
    normalization = special.zeta(alpha, float(xmin))
    cdf_after = 1.0 - special.zeta(alpha, sizes.astype(float) + 1.0) / normalization
    cdf_before = 1.0 - special.zeta(alpha, sizes.astype(float)) / normalization
    return ModelFit(
        model="power_law",
        xmin=xmin,
        parameters={"alpha": alpha},
        log_likelihood=log_likelihood,
        ks=_ks_from_cdf(frequencies, cdf_after, cdf_before),
        n_tail=int(frequencies.sum()),
        parameter_count=1,
    )


def fit_exponential(histogram: Histogram, xmin: int) -> ModelFit:
    sizes, frequencies = _tail_arrays(histogram, xmin)
    n = int(frequencies.sum())
    total_excess = float(np.dot(frequencies, sizes - xmin))
    mean_excess = total_excess / n
    if mean_excess == 0.0:
        rate = float("inf")
        log_likelihood = 0.0
        cdf_after = np.ones(sizes.shape)
        cdf_before = np.where(sizes == xmin, 0.0, 1.0)
    else:
        q = mean_excess / (1.0 + mean_excess)
        rate = -float(np.log(q))
        log_likelihood = n * np.log1p(-q) + total_excess * np.log(q)
        cdf_after = 1.0 - np.exp(-rate * (sizes - xmin + 1))
        cdf_before = 1.0 - np.exp(-rate * (sizes - xmin))
    return ModelFit(
        model="exponential",
        xmin=xmin,
        parameters={"lambda": rate},
        log_likelihood=float(log_likelihood),
        ks=_ks_from_cdf(frequencies, cdf_after, cdf_before),
        n_tail=n,
        parameter_count=1,
    )


def _log_difference(log_larger: np.ndarray, log_smaller: np.ndarray) -> np.ndarray:
    ratio = np.minimum(log_smaller - log_larger, 0.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        return log_larger + np.log(-np.expm1(ratio))


def _lognormal_log_probabilities(
    sizes: np.ndarray, *, xmin: int, mu: float, sigma: float
) -> np.ndarray:
    upper = (np.log(sizes + 0.5) - mu) / sigma
    lower = (np.log(sizes - 0.5) - mu) / sigma
    log_bin_mass = np.empty(upper.shape, dtype=float)
    left_tail = upper <= 0.0
    right_tail = lower >= 0.0
    middle = ~(left_tail | right_tail)
    log_bin_mass[left_tail] = _log_difference(
        special.log_ndtr(upper[left_tail]), special.log_ndtr(lower[left_tail])
    )
    log_bin_mass[right_tail] = _log_difference(
        special.log_ndtr(-lower[right_tail]), special.log_ndtr(-upper[right_tail])
    )
    if np.any(middle):
        mass = special.ndtr(upper[middle]) - special.ndtr(lower[middle])
        log_bin_mass[middle] = np.log(mass)
    boundary = (np.log(xmin - 0.5) - mu) / sigma
    log_normalization = special.log_ndtr(-boundary)
    return log_bin_mass - log_normalization


def fit_lognormal(
    histogram: Histogram,
    xmin: int,
    *,
    initial: dict[str, float] | None = None,
) -> ModelFit:
    sizes, frequencies = _tail_arrays(histogram, xmin)
    logs = np.log(sizes.astype(float))
    weighted_mean = float(np.average(logs, weights=frequencies))
    weighted_sd = float(
        np.sqrt(np.average((logs - weighted_mean) ** 2, weights=frequencies))
    )

    def objective(parameters: np.ndarray) -> float:
        mu, log_sigma = parameters
        sigma = float(np.exp(log_sigma))
        log_probabilities = _lognormal_log_probabilities(
            sizes, xmin=xmin, mu=float(mu), sigma=sigma
        )
        if not np.all(np.isfinite(log_probabilities)):
            return float("inf")
        return -float(np.dot(frequencies, log_probabilities))

    if initial is None:
        starts = (
            (weighted_mean, np.log(max(weighted_sd, 0.05))),
            (np.log(float(xmin)), np.log(0.5)),
            (weighted_mean - 1.0, np.log(1.0)),
            (weighted_mean - 3.0, np.log(2.0)),
        )
    else:
        starts = ((initial["mu"], np.log(initial["sigma"])),)
    results = [
        optimize.minimize(
            objective,
            np.asarray(start),
            method="Nelder-Mead",
            options={"maxiter": 3000, "xatol": 1e-9, "fatol": 1e-6},
        )
        for start in starts
    ]
    valid = [result for result in results if result.success and np.isfinite(result.fun)]
    if not valid:
        if initial is not None:
            return fit_lognormal(histogram, xmin, initial=None)
        raise RuntimeError("all discrete-lognormal optimizations failed")
    best = min(valid, key=lambda result: result.fun)
    mu = float(best.x[0])
    sigma = float(np.exp(best.x[1]))
    log_probabilities = _lognormal_log_probabilities(
        sizes, xmin=xmin, mu=mu, sigma=sigma
    )
    boundary = (np.log(xmin - 0.5) - mu) / sigma
    log_survival_boundary = special.log_ndtr(-boundary)
    upper_after = (np.log(sizes + 0.5) - mu) / sigma
    upper_before = (np.log(sizes - 0.5) - mu) / sigma
    cdf_after = np.exp(
        _log_difference(
            np.full(sizes.shape, log_survival_boundary),
            special.log_ndtr(-upper_after),
        )
        - log_survival_boundary
    )
    cdf_before = np.exp(
        _log_difference(
            np.full(sizes.shape, log_survival_boundary),
            special.log_ndtr(-upper_before),
        )
        - log_survival_boundary
    )
    return ModelFit(
        model="lognormal",
        xmin=xmin,
        parameters={"mu": mu, "sigma": sigma},
        log_likelihood=-float(best.fun),
        ks=_ks_from_cdf(frequencies, cdf_after, cdf_before),
        n_tail=int(frequencies.sum()),
        parameter_count=2,
    )


def _cutoff_log_normalization(alpha: float, rate: float, xmin: int) -> float:
    """Log normalization after scaling the first support weight to one."""
    if rate == 0.0:
        if alpha <= 1.0:
            return float("inf")
        return float(np.log(special.zeta(alpha, float(xmin))) + alpha * np.log(xmin))
    if rate < 1e-4 and alpha < 10.0:
        with mpmath.workdps(35):
            value = (
                mpmath.mpf(xmin) ** alpha
                * mpmath.lerchphi(mpmath.exp(-rate), alpha, xmin)
            )
            return float(mpmath.log(value))

    log_total = float("-inf")
    lower = xmin
    while True:
        upper = lower + 4096
        support = np.arange(lower, upper, dtype=float)
        log_weights = -alpha * np.log(support / xmin) - rate * (support - xmin)
        log_total = float(np.logaddexp(log_total, special.logsumexp(log_weights)))
        log_next_weight = -alpha * np.log(upper / xmin) - rate * (upper - xmin)
        log_exponential_bound = log_next_weight - np.log(rate)
        if alpha > 1.0:
            log_power_bound = (
                alpha * np.log(float(xmin))
                + (1.0 - alpha) * np.log(float(upper))
                - np.log(alpha - 1.0)
            )
            pass
        else:
            log_power_bound = float("inf")
        if min(log_exponential_bound, log_power_bound) <= log_total + np.log(1e-13):
            return log_total
        lower = upper


def fit_cutoff_power_law(
    histogram: Histogram,
    xmin: int,
    *,
    initial: dict[str, float] | None = None,
) -> ModelFit:
    sizes, frequencies = _tail_arrays(histogram, xmin)
    n = int(frequencies.sum())
    log_ratios = np.log(sizes / float(xmin))
    excess = sizes - xmin
    sum_log_ratios = float(np.dot(frequencies, log_ratios))
    sum_excess = float(np.dot(frequencies, excess))
    pure = fit_power_law_model(histogram, xmin)

    def objective(parameters: np.ndarray) -> float:
        alpha = float(parameters[0])
        rate = float(np.exp(parameters[1]))
        log_normalization = _cutoff_log_normalization(alpha, rate, xmin)
        value = n * log_normalization + alpha * sum_log_ratios + rate * sum_excess
        return float(value) if np.isfinite(value) else float("inf")

    if initial is None:
        starts = [
            (pure.parameters["alpha"], log_rate)
            for log_rate in (-12.0, -9.0, -6.0, -3.0)
        ]
        starts.extend((0.0, log_rate) for log_rate in (-9.0, -6.0, -3.0))
    else:
        initial_rate = max(initial["lambda"], np.exp(-16.0))
        starts = [(initial["alpha"], np.log(initial_rate))]
    results = [
        optimize.minimize(
            objective,
            np.asarray(start),
            method="L-BFGS-B",
            bounds=((-10_000.0, 200.0), (-16.0, 3.0)),
            options={"maxiter": 1000, "ftol": 1e-12},
        )
        for start in starts
    ]
    valid = [result for result in results if result.success and np.isfinite(result.fun)]
    if not valid:
        if initial is not None:
            return fit_cutoff_power_law(histogram, xmin, initial=None)
        raise RuntimeError("all cutoff-power-law optimizations failed")
    best = min(valid, key=lambda result: result.fun)
    if -float(best.fun) <= pure.log_likelihood:
        return ModelFit(
            model="cutoff_power_law",
            xmin=xmin,
            parameters={"alpha": pure.parameters["alpha"], "lambda": 0.0},
            log_likelihood=pure.log_likelihood,
            ks=pure.ks,
            n_tail=n,
            parameter_count=2,
        )
    alpha = float(best.x[0])
    rate = float(np.exp(best.x[1]))
    log_normalization = _cutoff_log_normalization(alpha, rate, xmin)
    log_probabilities = -alpha * log_ratios - rate * excess - log_normalization
    full_support = np.arange(xmin, int(sizes[-1]) + 1, dtype=np.int64)
    full_log_probabilities = (
        -alpha * np.log(full_support / float(xmin))
        - rate * (full_support - xmin)
        - log_normalization
    )
    full_cdf = np.cumsum(np.exp(full_log_probabilities))
    cdf_after = full_cdf[sizes - xmin]
    cdf_before = np.where(sizes == xmin, 0.0, full_cdf[sizes - xmin - 1])
    return ModelFit(
        model="cutoff_power_law",
        xmin=xmin,
        parameters={"alpha": alpha, "lambda": rate},
        log_likelihood=-float(best.fun),
        ks=_ks_from_cdf(frequencies, cdf_after, cdf_before),
        n_tail=n,
        parameter_count=2,
    )


def log_probabilities(fit: ModelFit, sizes: np.ndarray) -> np.ndarray:
    values = np.asarray(sizes, dtype=np.int64)
    if fit.model == "power_law":
        alpha = fit.parameters["alpha"]
        return -alpha * np.log(values) - np.log(special.zeta(alpha, fit.xmin))
    if fit.model == "exponential":
        rate = fit.parameters["lambda"]
        return np.log(-np.expm1(-rate)) - rate * (values - fit.xmin)
    if fit.model == "lognormal":
        return _lognormal_log_probabilities(
            values,
            xmin=fit.xmin,
            mu=fit.parameters["mu"],
            sigma=fit.parameters["sigma"],
        )
    if fit.model == "cutoff_power_law":
        alpha = fit.parameters["alpha"]
        rate = fit.parameters["lambda"]
        normalization = _cutoff_log_normalization(alpha, rate, fit.xmin)
        return (
            -alpha * np.log(values / float(fit.xmin))
            - rate * (values - fit.xmin)
            - normalization
        )
    raise ValueError(f"unknown model {fit.model}")


def vuong_test(
    histogram: Histogram, first: ModelFit, second: ModelFit
) -> tuple[float, float, float]:
    """Return log-likelihood ratio, normalized statistic, and two-sided p."""
    if first.xmin != second.xmin:
        raise ValueError("Vuong models must use the same xmin")
    sizes, frequencies = _tail_arrays(histogram, first.xmin)
    differences = log_probabilities(first, sizes) - log_probabilities(second, sizes)
    n = int(frequencies.sum())
    ratio = float(np.dot(frequencies, differences))
    mean = ratio / n
    variance = float(np.dot(frequencies, (differences - mean) ** 2) / (n - 1))
    statistic = float(np.sqrt(n) * mean / np.sqrt(variance))
    p_value = float(special.erfc(abs(statistic) / np.sqrt(2.0)))
    return ratio, statistic, p_value

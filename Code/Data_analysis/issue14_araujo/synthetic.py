"""Independent generators and synthetic-validation experiments for Issue 14."""

from __future__ import annotations

import csv
import json
from collections import Counter
from collections.abc import Mapping
from dataclasses import asdict
from pathlib import Path

import numpy as np
from scipy import stats

from .models import (
    FitResult,
    araujo_logpmf,
    fit_model,
    model_cdf,
    model_pmf,
    observed_arrays,
)


def histogram(sample: np.ndarray) -> np.ndarray | dict[int, int]:
    sample = np.asarray(sample, dtype=np.int64)
    if sample.size == 0 or np.any(sample < 1):
        raise ValueError("sample must contain positive integer sizes")
    if int(sample.max()) > 1_000_000:
        values, frequencies = np.unique(sample, return_counts=True)
        return {
            int(value): int(frequency)
            for value, frequency in zip(values, frequencies, strict=True)
        }
    return np.bincount(sample)


def sample_power_law(
    rng: np.random.Generator, n: int, *, alpha: float, xmin: int
) -> np.ndarray:
    """Exact conditional Zipf sampler by vectorized inverse-CDF search."""
    if alpha <= 1.0 or xmin < 1 or n < 1:
        raise ValueError("invalid power-law generator parameters")
    if xmin <= 5:
        accepted: list[np.ndarray] = []
        remaining = n
        while remaining:
            batch = max(remaining, 2 * remaining)
            draw = rng.zipf(alpha, size=batch)
            keep = draw[draw >= xmin]
            if keep.size:
                selected = keep[:remaining]
                accepted.append(selected)
                remaining -= selected.size
        return np.concatenate(accepted)
    from scipy import special

    survival_target = (1.0 - rng.random(n)) * special.zeta(alpha, float(xmin))
    lower = np.full(n, xmin - 1, dtype=np.int64)
    log_scale = (
        np.log(max(xmin - 0.5, 0.5))
        - np.log(np.maximum(survival_target / special.zeta(alpha, float(xmin)), 1e-300))
        / (alpha - 1.0)
        + np.log(2.0)
    )
    if np.any(log_scale >= np.log(np.iinfo(np.int64).max / 2)):
        raise RuntimeError("power-law draw exceeds int64 support")
    upper = np.maximum(xmin, np.ceil(np.exp(log_scale)).astype(np.int64))
    too_low = special.zeta(alpha, upper.astype(float) + 1.0) > survival_target
    while np.any(too_low):
        if np.any(upper[too_low] > np.iinfo(np.int64).max // 2):
            raise RuntimeError("power-law inverse search exceeded int64 support")
        upper[too_low] *= 2
        too_low = special.zeta(alpha, upper.astype(float) + 1.0) > survival_target
    while np.any(upper - lower > 1):
        middle = lower + (upper - lower) // 2
        cdf_reached = special.zeta(alpha, middle.astype(float) + 1.0) <= survival_target
        upper[cdf_reached] = middle[cdf_reached]
        lower[~cdf_reached] = middle[~cdf_reached]
    return upper


def sample_araujo(
    rng: np.random.Generator,
    n: int,
    *,
    alpha: float,
    eta: float,
    s0: float,
    xmin: int,
) -> np.ndarray:
    """Generate the survival-difference model by inverting continuous survival.

    No fitting probability routine is called: if ``Y`` has the continuous
    survival in Eq. (4), then ``floor(Y)`` has the exact survival-difference
    PMF on the integers.
    """
    target = -np.log(rng.random(n))
    x0_eta = (xmin / s0) ** eta
    lower = np.full(n, float(xmin))
    upper = np.maximum(
        2.0 * xmin,
        2.0 * s0 * np.maximum(target + x0_eta + 1.0, 1.0) ** (1.0 / eta),
    )

    def equation(x: np.ndarray) -> np.ndarray:
        return alpha * np.log(x / xmin) + (x / s0) ** eta - x0_eta

    while np.any(equation(upper) < target):
        upper[equation(upper) < target] *= 2.0
    for _ in range(60):
        middle = 0.5 * (lower + upper)
        below = equation(middle) < target
        lower[below] = middle[below]
        upper[~below] = middle[~below]
    return np.maximum(np.floor(0.5 * (lower + upper)).astype(np.int64), xmin)


def sample_lognormal(
    rng: np.random.Generator, n: int, *, mu: float, sigma: float, xmin: int
) -> np.ndarray:
    lower = (np.log(xmin - 0.5) - mu) / sigma
    latent = stats.truncnorm.rvs(
        lower,
        np.inf,
        loc=mu,
        scale=sigma,
        size=n,
        random_state=rng,
    )
    values = np.exp(np.minimum(latent, np.log(np.iinfo(np.int64).max - 1)))
    return np.maximum(np.floor(values + 0.5).astype(np.int64), xmin)


def sample_cutoff_power_law(
    rng: np.random.Generator,
    n: int,
    *,
    alpha: float,
    rate: float,
    xmin: int,
) -> np.ndarray:
    # Independent inverse table; extend until a rigorous geometric tail bound
    # is below 1e-12 of the accumulated mass.
    values: list[float] = []
    total = 0.0
    size = xmin
    q = np.exp(-rate)
    while True:
        weight = np.exp(-alpha * np.log(size / xmin) - rate * (size - xmin))
        values.append(weight)
        total += weight
        next_weight = np.exp(
            -alpha * np.log((size + 1) / xmin) - rate * (size + 1 - xmin)
        )
        if next_weight / (1.0 - q) <= 1e-12 * total:
            break
        size += 1
    probabilities = np.asarray(values) / total
    return xmin + rng.choice(len(probabilities), size=n, p=probabilities)


def sample_two_population(
    rng: np.random.Generator,
    n: int,
    *,
    weight_body: float,
    alpha: float,
    mu: float,
    sigma: float,
    xmin: int,
) -> np.ndarray:
    body = rng.random(n) < weight_body
    sample = np.empty(n, dtype=np.int64)
    sample[body] = sample_power_law(
        rng, int(body.sum()), alpha=alpha, xmin=xmin
    )
    sample[~body] = sample_lognormal(
        rng, int((~body).sum()), mu=mu, sigma=sigma, xmin=xmin
    )
    return sample


def sample_from_fit(
    rng: np.random.Generator, n: int, fit: FitResult
) -> np.ndarray:
    p = fit.parameters
    if fit.model == "araujo":
        return sample_araujo(
            rng,
            n,
            alpha=p["alpha"],
            eta=p["eta"],
            s0=p["s0"],
            xmin=fit.xmin,
        )
    if fit.model == "power_law":
        return sample_power_law(
            rng, n, alpha=p["alpha"], xmin=fit.xmin
        )
    if fit.model == "cutoff_power_law":
        return sample_cutoff_power_law(
            rng,
            n,
            alpha=p["alpha"],
            rate=p["rate"],
            xmin=fit.xmin,
        )
    if fit.model == "lognormal":
        return sample_lognormal(
            rng, n, mu=p["mu"], sigma=p["sigma"], xmin=fit.xmin
        )
    if fit.model == "two_population":
        return sample_two_population(
            rng,
            n,
            weight_body=p["weight_body"],
            alpha=p["alpha"],
            mu=p["mu"],
            sigma=p["sigma"],
            xmin=fit.xmin,
        )
    raise ValueError(f"sampling is not defined for {fit.model}")


def sample_histogram_from_fit(
    rng: np.random.Generator, n: int, fit: FitResult
) -> np.ndarray | dict[int, int]:
    """Sample a histogram efficiently without truncating heavy power-law tails."""
    if fit.model == "power_law":
        return sample_power_law_histogram(
            rng,
            n,
            alpha=fit.parameters["alpha"],
            xmin=fit.xmin,
        )
    if fit.model == "two_population":
        body_n = int(rng.binomial(n, fit.parameters["weight_body"]))
        body = sample_power_law_histogram(
            rng,
            body_n,
            alpha=fit.parameters["alpha"],
            xmin=fit.xmin,
        )
        large = sample_lognormal_histogram(
            rng,
            n - body_n,
            mu=fit.parameters["mu"],
            sigma=fit.parameters["sigma"],
            xmin=fit.xmin,
        )
        combined = dict(body)
        for size, frequency in large.items():
            combined[size] = combined.get(size, 0) + frequency
        return combined
    if fit.model == "lognormal":
        return sample_lognormal_histogram(
            rng,
            n,
            mu=fit.parameters["mu"],
            sigma=fit.parameters["sigma"],
            xmin=fit.xmin,
        )
    maximum = max(fit.xmin + 64, int(max(fit.parameters.get("s0", 0.0) * 2, np.exp(fit.parameters.get("mu", 0.0)) * 2)))
    while True:
        _, before = model_cdf(np.array([maximum + 1]), fit)
        survival = 1.0 - float(before[0])
        if survival <= min(1e-12, 1e-3 / n):
            break
        maximum *= 2
        if maximum > 5_000_000:
            return histogram(sample_from_fit(rng, n, fit))
    sizes = np.arange(fit.xmin, maximum + 1, dtype=np.int64)
    probabilities = model_pmf(sizes, fit)
    probabilities /= probabilities.sum()
    draws = rng.multinomial(n, probabilities)
    result = np.zeros(maximum + 1, dtype=np.int64)
    result[fit.xmin :] = draws
    return result


def sample_power_law_histogram(
    rng: np.random.Generator,
    n: int,
    *,
    alpha: float,
    xmin: int,
    expected_tail: float = 16.0,
) -> dict[int, int]:
    """Draw an exact conditional-Zipf histogram with a small explicit tail.

    The body and a tail category are sampled jointly with a multinomial draw.
    Only observations assigned to the tail category are generated by exact
    inverse-CDF sampling conditional on ``s >= cutoff + 1``.  This avoids both
    a finite-support approximation and millions of scalar Zipf draws.
    """
    from scipy import special

    if n < 1:
        return {}
    normalization = float(special.zeta(alpha, float(xmin)))
    cutoff = max(xmin + 64, 128)
    while n * float(special.zeta(alpha, float(cutoff + 1))) / normalization > expected_tail:
        cutoff *= 2
        if cutoff > 5_000_000:
            raise RuntimeError("power-law histogram body exceeded safe support")
    sizes = np.arange(xmin, cutoff + 1, dtype=np.int64)
    body_probabilities = sizes.astype(float) ** (-alpha) / normalization
    tail_probability = float(special.zeta(alpha, float(cutoff + 1))) / normalization
    probabilities = np.append(body_probabilities, tail_probability)
    probabilities /= probabilities.sum()
    draws = rng.multinomial(n, probabilities)
    result = {
        int(size): int(frequency)
        for size, frequency in zip(sizes, draws[:-1], strict=True)
        if frequency
    }
    tail_n = int(draws[-1])
    if tail_n:
        tail = sample_power_law(
            rng,
            tail_n,
            alpha=alpha,
            xmin=cutoff + 1,
        )
        tail_sizes, tail_frequencies = np.unique(tail, return_counts=True)
        for size, frequency in zip(tail_sizes, tail_frequencies, strict=True):
            result[int(size)] = result.get(int(size), 0) + int(frequency)
    return result


def sample_lognormal_histogram(
    rng: np.random.Generator,
    n: int,
    *,
    mu: float,
    sigma: float,
    xmin: int,
    expected_tail: float = 16.0,
) -> dict[int, int]:
    """Draw the rounded, lower-truncated lognormal as an exact histogram."""
    if n < 1:
        return {}
    lower_log = np.log(xmin - 0.5)
    lower_z = (lower_log - mu) / sigma
    normalization = float(stats.norm.sf(lower_z))
    cutoff = max(xmin + 64, 128)
    while n * float(stats.norm.sf((np.log(cutoff + 0.5) - mu) / sigma)) / normalization > expected_tail:
        cutoff *= 2
        if cutoff > 5_000_000:
            raise RuntimeError("lognormal histogram body exceeded safe support")
    sizes = np.arange(xmin, cutoff + 1, dtype=np.int64)
    upper_z = (np.log(sizes + 0.5) - mu) / sigma
    lower_bin_z = (np.log(sizes - 0.5) - mu) / sigma
    body_probabilities = (stats.norm.cdf(upper_z) - stats.norm.cdf(lower_bin_z)) / normalization
    tail_probability = float(stats.norm.sf(upper_z[-1])) / normalization
    probabilities = np.append(body_probabilities, tail_probability)
    probabilities /= probabilities.sum()
    draws = rng.multinomial(n, probabilities)
    result = {
        int(size): int(frequency)
        for size, frequency in zip(sizes, draws[:-1], strict=True)
        if frequency
    }
    tail_n = int(draws[-1])
    if tail_n:
        tail_lower = (np.log(cutoff + 0.5) - mu) / sigma
        latent = stats.truncnorm.rvs(
            tail_lower,
            np.inf,
            loc=mu,
            scale=sigma,
            size=tail_n,
            random_state=rng,
        )
        tail = np.floor(np.exp(latent) + 0.5).astype(np.int64)
        tail_sizes, tail_frequencies = np.unique(tail, return_counts=True)
        for size, frequency in zip(tail_sizes, tail_frequencies, strict=True):
            result[int(size)] = result.get(int(size), 0) + int(frequency)
    return result


def alpha_standard_error(counts: np.ndarray | Mapping[int, int], fit: FitResult) -> float:
    if fit.model != "power_law":
        raise ValueError("alpha standard error requires a power-law fit")
    alpha = fit.parameters["alpha"]
    step = 1e-4 * max(alpha, 1.0)

    def nll(value: float) -> float:
        return _power_nll(counts, fit.xmin, value)

    curvature = (nll(alpha + step) - 2.0 * nll(alpha) + nll(alpha - step)) / step**2
    return float(1.0 / np.sqrt(curvature))


def _power_nll(counts: np.ndarray | Mapping[int, int], xmin: int, alpha: float) -> float:
    from scipy import special

    sizes, frequencies = observed_arrays(counts, xmin)
    return float(
        alpha * np.dot(frequencies, np.log(sizes))
        + frequencies.sum() * np.log(special.zeta(alpha, float(xmin)))
    )


def select_power_law_xmin(
    counts: np.ndarray | Mapping[int, int],
    *,
    minimum_xmin: int = 1,
    minimum_tail: int = 100,
    maximum_candidates: int = 80,
) -> FitResult:
    sizes, frequencies = observed_arrays(counts, minimum_xmin)
    tail = np.cumsum(frequencies[::-1], dtype=np.int64)[::-1]
    candidates = sizes[(tail >= minimum_tail) & (sizes < sizes[-1])]
    if candidates.size == 0:
        raise ValueError("no xmin candidate has the required tail size")
    if candidates.size > maximum_candidates:
        indices = np.unique(np.linspace(0, candidates.size - 1, maximum_candidates).astype(int))
        candidates = candidates[indices]
    fits = [fit_model(counts, "power_law", xmin=int(xmin)) for xmin in candidates]
    return min(fits, key=lambda item: (item.ks, item.xmin))


def clopper_pearson(successes: int, trials: int, confidence: float = 0.95) -> tuple[float, float]:
    alpha = 1.0 - confidence
    lower = 0.0 if successes == 0 else float(stats.beta.ppf(alpha / 2.0, successes, trials - successes + 1))
    upper = 1.0 if successes == trials else float(stats.beta.ppf(1.0 - alpha / 2.0, successes + 1, trials - successes))
    return lower, upper


def parametric_gof(
    counts: np.ndarray | Mapping[int, int],
    fit: FitResult,
    *,
    rng: np.random.Generator,
    replicates: int,
) -> tuple[dict[str, float | int], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    exceed = 0
    for replicate in range(replicates):
        sampled_counts = sample_histogram_from_fit(rng, fit.n, fit)
        fitted = fit_model(
            sampled_counts, fit.model, xmin=fit.xmin, initial=fit.parameters
        )
        exceed += fitted.ks >= fit.ks
        rows.append(
            {
                "replicate": replicate,
                "ks": fitted.ks,
                "tail_ad": fitted.tail_ad,
                "converged": fitted.converged,
                **{f"parameter_{key}": value for key, value in fitted.parameters.items()},
            }
        )
    lower, upper = clopper_pearson(exceed, replicates)
    return (
        {
            "replicates": replicates,
            "exceedances": exceed,
            "p_raw": exceed / replicates,
            "p_add_one": (exceed + 1) / (replicates + 1),
            "p_ci_low": lower,
            "p_ci_high": upper,
        },
        rows,
    )


def araujo_wald_diagnostics(
    counts: np.ndarray | Mapping[int, int], fit: FitResult
) -> dict[str, float]:
    """Observed-information intervals and eta/log-s0 correlation diagnostic."""
    if fit.model != "araujo":
        raise ValueError("Araújo diagnostics require an Araújo fit")
    sizes, frequencies = observed_arrays(counts, fit.xmin)
    p = fit.parameters
    point = np.array([p["alpha"], np.log(p["eta"]), np.log(p["s0"])])

    def objective(x: np.ndarray) -> float:
        values = araujo_logpmf(
            sizes,
            xmin=fit.xmin,
            alpha=float(x[0]),
            eta=float(np.exp(x[1])),
            s0=float(np.exp(x[2])),
        )
        return -float(np.dot(frequencies, values))

    steps = 2e-4 * np.maximum(1.0, np.abs(point))
    steps[0] = min(steps[0], max(point[0] * 0.25, 1e-8))
    hessian = np.empty((3, 3), dtype=float)
    base = objective(point)
    for i in range(3):
        ei = np.zeros(3)
        ei[i] = steps[i]
        hessian[i, i] = (objective(point + ei) - 2.0 * base + objective(point - ei)) / steps[i] ** 2
        for j in range(i):
            ej = np.zeros(3)
            ej[j] = steps[j]
            hessian[i, j] = hessian[j, i] = (
                objective(point + ei + ej)
                - objective(point + ei - ej)
                - objective(point - ei + ej)
                + objective(point - ei - ej)
            ) / (4.0 * steps[i] * steps[j])
    if not np.all(np.isfinite(hessian)):
        return {
            "alpha_se": float("inf"),
            "eta_ci_low": 0.0,
            "eta_ci_high": float("inf"),
            "s0_ci_low": 0.0,
            "s0_ci_high": float("inf"),
            "alpha_ci_low": 0.0,
            "alpha_ci_high": float("inf"),
            "eta_log_s0_correlation": float("nan"),
            "information_condition_number": float("inf"),
        }
    covariance = np.linalg.pinv(hessian)
    se = np.sqrt(np.maximum(np.diag(covariance), 0.0))
    return {
        "alpha_se": float(se[0]),
        "eta_ci_low": float(np.exp(point[1] - 1.96 * se[1])),
        "eta_ci_high": float(np.exp(point[1] + 1.96 * se[1])),
        "s0_ci_low": float(np.exp(point[2] - 1.96 * se[2])),
        "s0_ci_high": float(np.exp(point[2] + 1.96 * se[2])),
        "alpha_ci_low": float(point[0] - 1.96 * se[0]),
        "alpha_ci_high": float(point[0] + 1.96 * se[0]),
        "eta_log_s0_correlation": float(
            covariance[1, 2] / np.sqrt(max(covariance[1, 1] * covariance[2, 2], np.finfo(float).tiny))
        ),
        "information_condition_number": float(np.linalg.cond(hessian)),
    }


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def run_synthetic_validation(
    output_dir: Path,
    *,
    seed: int = 20260818,
    grid_replicates: int = 8,
    gof_repetitions: int = 30,
    gof_bootstrap: int = 39,
    negative_replicates: int = 12,
    araujo_replicates: int = 8,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    seeds: list[dict[str, object]] = []

    benchmark_seed = int(rng.integers(0, 2**32 - 1))
    sample = sample_power_law(
        np.random.default_rng(benchmark_seed), 10_000, alpha=2.5, xmin=1
    )
    benchmark_fit = fit_model(histogram(sample), "power_law", xmin=1)
    benchmark_se = alpha_standard_error(histogram(sample), benchmark_fit)
    benchmark = {
        "truth_alpha": 2.5,
        "xmin": 1,
        "n": 10_000,
        "estimate": benchmark_fit.parameters["alpha"],
        "standard_error": benchmark_se,
        "z_score": (benchmark_fit.parameters["alpha"] - 2.5) / benchmark_se,
        "seed": benchmark_seed,
    }
    print("synthetic validation: Clauset benchmark complete", flush=True)

    grid_rows: list[dict[str, object]] = []
    selection_rows: list[dict[str, object]] = []
    for alpha in (1.5, 2.0, 2.5, 3.0):
        for xmin in (1, 2, 5, 10):
            for n in (500, 2_000):
                for replicate in range(grid_replicates):
                    local_seed = int(rng.integers(0, 2**32 - 1))
                    generated = sample_power_law(
                        np.random.default_rng(local_seed), n, alpha=alpha, xmin=xmin
                    )
                    counts = histogram(generated)
                    fitted = fit_model(counts, "power_law", xmin=xmin)
                    se = alpha_standard_error(counts, fitted)
                    selected = select_power_law_xmin(
                        counts,
                        minimum_xmin=1,
                        minimum_tail=max(50, n // 10),
                    )
                    row = {
                        "truth_alpha": alpha,
                        "truth_xmin": xmin,
                        "n": n,
                        "replicate": replicate,
                        "seed": local_seed,
                        "alpha_hat": fitted.parameters["alpha"],
                        "alpha_se": se,
                        "covered_95": abs(fitted.parameters["alpha"] - alpha) <= 1.96 * se,
                        "converged": fitted.converged,
                        "selected_xmin": selected.xmin,
                        "selected_alpha": selected.parameters["alpha"],
                    }
                    grid_rows.append(row)
                    selection_rows.append(
                        {
                            "truth_alpha": alpha,
                            "truth_xmin": xmin,
                            "n": n,
                            "selected_xmin": selected.xmin,
                            "replicate": replicate,
                        }
                    )
                    seeds.append({"experiment": "power_grid", **row})
    print("synthetic validation: discrete power-law grid complete", flush=True)

    calibration_rows: list[dict[str, object]] = []
    false_rejections = 0
    for replicate in range(gof_repetitions):
        local_seed = int(rng.integers(0, 2**32 - 1))
        local_rng = np.random.default_rng(local_seed)
        generated = sample_power_law(local_rng, 1_000, alpha=2.5, xmin=2)
        counts = histogram(generated)
        fitted = fit_model(counts, "power_law", xmin=2)
        summary, _ = parametric_gof(
            counts, fitted, rng=local_rng, replicates=gof_bootstrap
        )
        rejected = float(summary["p_add_one"]) <= 0.1
        false_rejections += rejected
        calibration_rows.append(
            {
                "replicate": replicate,
                "seed": local_seed,
                "alpha_hat": fitted.parameters["alpha"],
                "ks": fitted.ks,
                "p_value": summary["p_add_one"],
                "rejected_at_0_1": rejected,
            }
        )
    calibration_interval = clopper_pearson(false_rejections, gof_repetitions)
    print("synthetic validation: goodness-of-fit calibration complete", flush=True)

    semiparametric_rows: list[dict[str, object]] = []
    for replicate in range(max(12, grid_replicates)):
        local_seed = int(rng.integers(0, 2**32 - 1))
        local_rng = np.random.default_rng(local_seed)
        body = local_rng.choice(np.arange(1, 5), size=1_200, p=[0.5, 0.25, 0.17, 0.08])
        tail = sample_power_law(local_rng, 800, alpha=2.3, xmin=5)
        counts = histogram(np.concatenate((body, tail)))
        selected = select_power_law_xmin(counts, minimum_tail=200)
        semiparametric_rows.append(
            {
                "replicate": replicate,
                "seed": local_seed,
                "truth_xmin": 5,
                "truth_alpha": 2.3,
                "selected_xmin": selected.xmin,
                "alpha_hat": selected.parameters["alpha"],
            }
        )
    print("synthetic validation: semiparametric recovery complete", flush=True)

    negative_rows: list[dict[str, object]] = []
    generators = {
        "discrete_lognormal": lambda r: sample_lognormal(r, 2_000, mu=2.0, sigma=1.0, xmin=1),
        "exponential": lambda r: r.geometric(0.15, size=2_000),
        "cutoff_power_law": lambda r: sample_cutoff_power_law(r, 2_000, alpha=1.3, rate=0.035, xmin=1),
        "stretched_exponential": lambda r: sample_araujo(r, 2_000, alpha=0.05, eta=1.6, s0=35.0, xmin=1),
        "terminal_peak_mixture": lambda r: sample_two_population(r, 2_000, weight_body=0.97, alpha=1.8, mu=np.log(180.0), sigma=0.12, xmin=1),
    }
    for name, generator in generators.items():
        for replicate in range(negative_replicates):
            local_seed = int(rng.integers(0, 2**32 - 1))
            local_rng = np.random.default_rng(local_seed)
            counts = histogram(generator(local_rng))
            selected = select_power_law_xmin(counts, minimum_tail=200)
            summary, _ = parametric_gof(
                counts, selected, rng=local_rng, replicates=gof_bootstrap
            )
            negative_rows.append(
                {
                    "generator": name,
                    "replicate": replicate,
                    "seed": local_seed,
                    "selected_xmin": selected.xmin,
                    "alpha_hat": selected.parameters["alpha"],
                    "p_value": summary["p_add_one"],
                    "rejected_at_0_1": float(summary["p_add_one"]) <= 0.1,
                }
            )
        print(f"synthetic validation: negative control {name} complete", flush=True)

    araujo_rows: list[dict[str, object]] = []
    araujo_grid = (
        (0.255, 1.5, 100.0),
        (0.075, 2.0, 150.0),
        (0.015, 0.22, 30.0),
        (2.0, 8.0, 20.0),
    )
    for alpha, eta, s0 in araujo_grid:
        cell_replicates = (
            max(2, araujo_replicates // 4)
            if (alpha, eta) in {(0.015, 0.22), (2.0, 8.0)}
            else araujo_replicates
        )
        for n in (1_000, 5_000):
            for replicate in range(cell_replicates):
                local_seed = int(rng.integers(0, 2**32 - 1))
                generated = sample_araujo(
                    np.random.default_rng(local_seed),
                    n,
                    alpha=alpha,
                    eta=eta,
                    s0=s0,
                    xmin=2,
                )
                fitted = fit_model(histogram(generated), "araujo", xmin=2)
                diagnostics = araujo_wald_diagnostics(histogram(generated), fitted)
                araujo_rows.append(
                    {
                        "truth_alpha": alpha,
                        "truth_eta": eta,
                        "truth_s0": s0,
                        "n": n,
                        "replicate": replicate,
                        "seed": local_seed,
                        "alpha_hat": fitted.parameters["alpha"],
                        "eta_hat": fitted.parameters["eta"],
                        "s0_hat": fitted.parameters["s0"],
                        **diagnostics,
                        "alpha_covered_95": diagnostics["alpha_ci_low"] <= alpha <= diagnostics["alpha_ci_high"],
                        "eta_covered_95": diagnostics["eta_ci_low"] <= eta <= diagnostics["eta_ci_high"],
                        "s0_covered_95": diagnostics["s0_ci_low"] <= s0 <= diagnostics["s0_ci_high"],
                        "converged": fitted.converged,
                    }
                )
        print(
            f"synthetic validation: Araújo recovery alpha={alpha}, eta={eta} complete",
            flush=True,
        )

    for name, rows in (
        ("power_law_grid_replicates.csv", grid_rows),
        ("xmin_selection_replicates.csv", selection_rows),
        ("power_law_gof_calibration.csv", calibration_rows),
        ("semiparametric_recovery.csv", semiparametric_rows),
        ("negative_controls.csv", negative_rows),
        ("araujo_recovery_replicates.csv", araujo_rows),
    ):
        _write_csv(output_dir / name, rows)

    def summarize(rows: list[dict[str, object]], keys: tuple[str, ...], estimate: str, truth: str) -> list[dict[str, object]]:
        groups: dict[tuple[object, ...], list[dict[str, object]]] = {}
        for row in rows:
            groups.setdefault(tuple(row[key] for key in keys), []).append(row)
        result = []
        for group, items in groups.items():
            errors = np.array([float(item[estimate]) - float(item[truth]) for item in items])
            result.append(
                {
                    **dict(zip(keys, group, strict=True)),
                    "replicates": len(items),
                    "bias": float(errors.mean()),
                    "rmse": float(np.sqrt(np.mean(errors**2))),
                    "coverage_95": float(np.mean([bool(item.get("covered_95", False)) for item in items])),
                    "convergence_failures": int(sum(not bool(item.get("converged", True)) for item in items)),
                }
            )
        return result

    power_summary = summarize(
        grid_rows, ("truth_alpha", "truth_xmin", "n"), "alpha_hat", "truth_alpha"
    )
    _write_csv(output_dir / "power_law_grid_summary.csv", power_summary)

    negative_summary = []
    for name in generators:
        items = [row for row in negative_rows if row["generator"] == name]
        rejected = int(sum(bool(row["rejected_at_0_1"]) for row in items))
        low, high = clopper_pearson(rejected, len(items))
        negative_summary.append(
            {
                "generator": name,
                "replicates": len(items),
                "rejections": rejected,
                "rejection_power": rejected / len(items),
                "ci_low": low,
                "ci_high": high,
            }
        )
    _write_csv(output_dir / "negative_control_summary.csv", negative_summary)

    araujo_summary: list[dict[str, object]] = []
    for alpha, eta, s0 in araujo_grid:
        for n in (1_000, 5_000):
            items = [row for row in araujo_rows if row["truth_alpha"] == alpha and row["truth_eta"] == eta and row["n"] == n]
            for parameter, truth in (("alpha", alpha), ("eta", eta), ("s0", s0)):
                errors = np.array([float(row[f"{parameter}_hat"]) - truth for row in items])
                araujo_summary.append(
                    {
                        "truth_alpha": alpha,
                        "truth_eta": eta,
                        "truth_s0": s0,
                        "n": n,
                        "parameter": parameter,
                        "replicates": len(items),
                        "bias": float(errors.mean()),
                        "relative_bias": float(errors.mean() / truth),
                        "rmse": float(np.sqrt(np.mean(errors**2))),
                        "coverage_95": float(np.mean([bool(row[f"{parameter}_covered_95"]) for row in items])),
                        "median_eta_log_s0_correlation": float(np.median([float(row["eta_log_s0_correlation"]) for row in items])),
                        "median_information_condition_number": float(np.median([float(row["information_condition_number"]) for row in items])),
                        "convergence_failures": int(sum(not bool(row["converged"]) for row in items)),
                    }
                )
    _write_csv(output_dir / "araujo_recovery_summary.csv", araujo_summary)

    result = {
        "master_seed": seed,
        "benchmark": benchmark,
        "power_law_grid": {
            "alphas": [1.5, 2.0, 2.5, 3.0],
            "xmins": [1, 2, 5, 10],
            "sample_sizes": [500, 2_000],
            "replicates_per_cell": grid_replicates,
        },
        "gof_calibration": {
            "threshold": 0.1,
            "repetitions": gof_repetitions,
            "bootstrap_replicates": gof_bootstrap,
            "false_rejections": false_rejections,
            "false_rejection_rate": false_rejections / gof_repetitions,
            "exact_binomial_ci": calibration_interval,
            "compatible_with_0_1": calibration_interval[0] <= 0.1 <= calibration_interval[1],
        },
        "generator_independence": (
            "Synthetic generators invert survival functions or sample standard variates; "
            "they do not call any fitted-model probability implementation."
        ),
    }
    (output_dir / "synthetic_validation_summary.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if gof_repetitions >= 30 and not result["gof_calibration"]["compatible_with_0_1"]:
        raise AssertionError(
            "power-law GOF false-rejection interval is incompatible with 0.1"
        )
    return result

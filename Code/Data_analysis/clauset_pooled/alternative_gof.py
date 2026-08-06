"""Fixed-support parametric goodness-of-fit tests for alternative models."""

from __future__ import annotations

from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

import numpy as np
from scipy import special

from .models import (
    ModelFit,
    _cutoff_log_normalization,
    fit_cutoff_power_law,
    fit_exponential,
    fit_lognormal,
)
from .power_law import Histogram, histogram_arrays


@dataclass(frozen=True)
class AlternativeGoodnessOfFit:
    observed: ModelFit
    p_value: float
    exceedances: int
    replicates: int
    monte_carlo_standard_error: float
    synthetic_ks: tuple[float, ...]


def _log_survival(fit: ModelFit, threshold: int) -> float:
    """Return log P(X >= threshold | X >= xmin)."""
    if threshold <= fit.xmin:
        return 0.0
    if fit.model == "exponential":
        return -fit.parameters["lambda"] * (threshold - fit.xmin)
    if fit.model == "lognormal":
        mu = fit.parameters["mu"]
        sigma = fit.parameters["sigma"]
        boundary = (np.log(fit.xmin - 0.5) - mu) / sigma
        value = (np.log(threshold - 0.5) - mu) / sigma
        return float(special.log_ndtr(-value) - special.log_ndtr(-boundary))
    if fit.model == "cutoff_power_law":
        alpha = fit.parameters["alpha"]
        rate = fit.parameters["lambda"]
        log_tail = (
            _cutoff_log_normalization(alpha, rate, threshold)
            - alpha * np.log(float(threshold))
            - rate * threshold
        )
        log_total = (
            _cutoff_log_normalization(alpha, rate, fit.xmin)
            - alpha * np.log(float(fit.xmin))
            - rate * fit.xmin
        )
        return float(log_tail - log_total)
    raise ValueError(f"unsupported model: {fit.model}")


def sample_model_counts(
    n: int, fit: ModelFit, *, rng: np.random.Generator
) -> dict[int, int]:
    """Sample exact integer counts by recursive CDF partitioning."""
    if n < 0:
        raise ValueError("sample size must be nonnegative")
    if fit.model == "cutoff_power_law":
        return _sample_cutoff_counts(n, fit, rng=rng)
    sampled: Counter[int] = Counter()
    survival_cache: dict[int, float] = {}

    def log_survival(threshold: int) -> float:
        if threshold not in survival_cache:
            survival_cache[threshold] = _log_survival(fit, threshold)
        return survival_cache[threshold]

    def split_interval(lower: int, upper: int, count: int) -> None:
        if count == 0:
            return
        if lower == upper:
            sampled[lower] += count
            return
        midpoint = (lower + upper) // 2
        log_lower = log_survival(lower)
        log_middle = log_survival(midpoint + 1)
        log_upper = log_survival(upper + 1)
        total_mass = -np.expm1(min(0.0, log_upper - log_lower))
        left_mass = -np.expm1(min(0.0, log_middle - log_lower))
        probability_left = float(np.clip(left_mass / total_mass, 0.0, 1.0))
        left_count = int(rng.binomial(count, probability_left))
        split_interval(lower, midpoint, left_count)
        split_interval(midpoint + 1, upper, count - left_count)

    remaining = n
    lower = fit.xmin
    while remaining:
        upper = 2 * lower - 1
        log_lower = log_survival(lower)
        log_upper = log_survival(upper + 1)
        tail_ratio = float(np.clip(np.exp(log_upper - log_lower), 0.0, 1.0))
        block_count = int(rng.binomial(remaining, 1.0 - tail_ratio))
        split_interval(lower, upper, block_count)
        remaining -= block_count
        lower = upper + 1
        if lower.bit_length() > 1024:
            raise RuntimeError("model sampler did not terminate")
    return dict(sampled)


def _sample_cutoff_counts(
    n: int, fit: ModelFit, *, rng: np.random.Generator
) -> dict[int, int]:
    """Sample cutoff counts from a finite table accurate to floating precision."""
    alpha = fit.parameters["alpha"]
    rate = fit.parameters["lambda"]
    xmin = fit.xmin
    log_normalization = _cutoff_log_normalization(alpha, rate, xmin)
    chunks: list[np.ndarray] = []
    total_probability = 0.0
    lower = xmin
    while True:
        upper = lower + 4096
        support = np.arange(lower, upper, dtype=float)
        probabilities = np.exp(
            -alpha * np.log(support / xmin)
            - rate * (support - xmin)
            - log_normalization
        )
        chunks.append(probabilities)
        total_probability += float(probabilities.sum())
        if 1.0 - total_probability <= 1e-13:
            break
        lower = upper
        if lower - xmin > 10_000_000:
            raise RuntimeError("cutoff sampling table exceeded ten million sizes")
    probabilities = np.concatenate(chunks)
    probabilities /= probabilities.sum()
    allocations = rng.multinomial(n, probabilities)
    nonzero = np.flatnonzero(allocations)
    return {int(xmin + index): int(allocations[index]) for index in nonzero}


def _fit_model(
    histogram: Histogram,
    model: str,
    xmin: int,
    *,
    initial: ModelFit | None = None,
) -> ModelFit:
    if model == "cutoff_power_law":
        return fit_cutoff_power_law(
            histogram,
            xmin,
            initial=initial.parameters if initial is not None else None,
        )
    if model == "lognormal":
        return fit_lognormal(
            histogram,
            xmin,
            initial=initial.parameters if initial is not None else None,
        )
    if model == "exponential":
        return fit_exponential(histogram, xmin)
    raise ValueError(f"unsupported model: {model}")


def _one_replica(arguments: tuple[ModelFit, int, int]) -> ModelFit:
    observed, n, seed = arguments
    synthetic = sample_model_counts(n, observed, rng=np.random.default_rng(seed))
    return _fit_model(
        synthetic, observed.model, observed.xmin, initial=observed
    )


def parametric_gof(
    histogram: Histogram,
    *,
    model: str,
    xmin: int,
    replicates: int = 2500,
    seed: int = 12738,
    workers: int = 1,
) -> AlternativeGoodnessOfFit:
    """Generate, refit and compare KS under one fitted alternative family."""
    if replicates < 1 or workers < 1:
        raise ValueError("replicates and workers must be positive")
    observed = _fit_model(histogram, model, xmin)
    sizes, frequencies = histogram_arrays(histogram)
    n = int(frequencies[sizes >= xmin].sum())
    seeds = [
        int(child.generate_state(1, dtype=np.uint64)[0])
        for child in np.random.SeedSequence(seed).spawn(replicates)
    ]
    arguments = [(observed, n, child_seed) for child_seed in seeds]
    if workers == 1:
        fits = [_one_replica(argument) for argument in arguments]
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            fits = list(
                executor.map(
                    _one_replica,
                    arguments,
                    chunksize=max(1, replicates // (workers * 8)),
                )
            )
    exceedances = sum(fit.ks >= observed.ks for fit in fits)
    p_value = exceedances / replicates
    standard_error = float(np.sqrt(p_value * (1.0 - p_value) / replicates))
    return AlternativeGoodnessOfFit(
        observed=observed,
        p_value=p_value,
        exceedances=exceedances,
        replicates=replicates,
        monte_carlo_standard_error=standard_error,
        synthetic_ks=tuple(fit.ks for fit in fits),
    )

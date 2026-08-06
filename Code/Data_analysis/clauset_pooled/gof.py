"""Semiparametric goodness-of-fit test for a pooled discrete power law."""

from __future__ import annotations

from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

import numpy as np

from .power_law import (
    Histogram,
    PowerLawFit,
    _log_zeta,
    histogram_arrays,
    select_xmin,
)


@dataclass(frozen=True)
class GoodnessOfFit:
    observed: PowerLawFit
    p_value: float
    exceedances: int
    replicates: int
    monte_carlo_standard_error: float
    synthetic_ks: tuple[float, ...]
    synthetic_xmin: tuple[int, ...]


def _conditional_survival(alpha: float, threshold: int, lower: int) -> float:
    log_probability = _log_zeta(alpha, threshold) - _log_zeta(alpha, lower)
    return float(np.clip(np.exp(log_probability), 0.0, 1.0))


def sample_power_law_counts(
    n: int, *, xmin: int, alpha: float, rng: np.random.Generator
) -> dict[int, int]:
    """Sample an exact infinite-support power law as sparse integer counts."""
    if n < 0 or xmin < 1 or alpha <= 1.0:
        raise ValueError("invalid power-law sampling parameters")
    sampled: Counter[int] = Counter()

    def split_interval(lower: int, upper: int, count: int) -> None:
        if count == 0:
            return
        if lower == upper:
            sampled[lower] += count
            return
        midpoint = (lower + upper) // 2
        log_total_tail = _log_zeta(alpha, upper + 1) - _log_zeta(alpha, lower)
        log_left_tail = _log_zeta(alpha, midpoint + 1) - _log_zeta(alpha, lower)
        total_mass = -np.expm1(log_total_tail)
        left_mass = -np.expm1(log_left_tail)
        probability_left = float(np.clip(left_mass / total_mass, 0.0, 1.0))
        left_count = int(rng.binomial(count, probability_left))
        split_interval(lower, midpoint, left_count)
        split_interval(midpoint + 1, upper, count - left_count)

    remaining = n
    lower = xmin
    while remaining:
        upper = 2 * lower - 1
        tail_probability = _conditional_survival(alpha, upper + 1, lower)
        block_count = int(rng.binomial(remaining, 1.0 - tail_probability))
        split_interval(lower, upper, block_count)
        remaining -= block_count
        lower = upper + 1
        if lower.bit_length() > 1024:
            raise RuntimeError("power-law sampler did not terminate")
    return dict(sampled)


def semiparametric_sample(
    histogram: Histogram, fit: PowerLawFit, *, rng: np.random.Generator
) -> dict[int, int]:
    """Resample the empirical body and generate the fitted power-law tail."""
    sizes, frequencies = histogram_arrays(histogram)
    total = int(frequencies.sum())
    tail_mask = sizes >= fit.xmin
    observed_tail = int(frequencies[tail_mask].sum())
    synthetic_tail = int(rng.binomial(total, observed_tail / total))
    synthetic_body = total - synthetic_tail

    result: Counter[int] = Counter()
    body_sizes = sizes[~tail_mask]
    body_frequencies = frequencies[~tail_mask]
    if synthetic_body:
        if body_frequencies.size == 0:
            raise RuntimeError("a synthetic body was requested from an empty body")
        allocations = rng.multinomial(
            synthetic_body, body_frequencies / body_frequencies.sum()
        )
        result.update(
            {
                int(size): int(count)
                for size, count in zip(body_sizes, allocations, strict=True)
                if count
            }
        )
    result.update(
        sample_power_law_counts(
            synthetic_tail,
            xmin=fit.xmin,
            alpha=fit.alpha,
            rng=rng,
        )
    )
    return dict(result)


def _one_replica(arguments: tuple[dict[int, int], PowerLawFit, int, int, int]) -> PowerLawFit:
    histogram, observed, minimum_xmin, minimum_tail, seed = arguments
    synthetic = semiparametric_sample(
        histogram, observed, rng=np.random.default_rng(seed)
    )
    return select_xmin(
        synthetic, minimum_xmin=minimum_xmin, minimum_tail=minimum_tail
    )


def clauset_gof(
    histogram: Histogram,
    *,
    minimum_xmin: int = 2,
    minimum_tail: int = 1000,
    replicates: int = 2500,
    seed: int = 12738,
    workers: int = 1,
) -> GoodnessOfFit:
    """Run the full-refit semiparametric Monte Carlo test of Clauset et al."""
    if replicates < 1 or workers < 1:
        raise ValueError("replicates and workers must be positive")
    observed = select_xmin(
        histogram, minimum_xmin=minimum_xmin, minimum_tail=minimum_tail
    )
    sizes, frequencies = histogram_arrays(histogram)
    compact = {
        int(size): int(frequency)
        for size, frequency in zip(sizes, frequencies, strict=True)
    }
    seeds = [
        int(child.generate_state(1, dtype=np.uint64)[0])
        for child in np.random.SeedSequence(seed).spawn(replicates)
    ]
    arguments = [
        (compact, observed, minimum_xmin, minimum_tail, child_seed)
        for child_seed in seeds
    ]
    if workers == 1:
        fits = [_one_replica(argument) for argument in arguments]
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            fits = list(executor.map(_one_replica, arguments, chunksize=1))
    exceedances = sum(fit.ks >= observed.ks for fit in fits)
    p_value = exceedances / replicates
    standard_error = float(np.sqrt(p_value * (1.0 - p_value) / replicates))
    return GoodnessOfFit(
        observed=observed,
        p_value=p_value,
        exceedances=exceedances,
        replicates=replicates,
        monte_carlo_standard_error=standard_error,
        synthetic_ks=tuple(fit.ks for fit in fits),
        synthetic_xmin=tuple(fit.xmin for fit in fits),
    )

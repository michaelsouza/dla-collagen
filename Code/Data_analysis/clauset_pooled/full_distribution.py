"""Exact empirical summaries and distances for complete avalanche distributions."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import spatial, stats


@dataclass(frozen=True)
class DistributionSummary:
    population: str
    minimum_size: int
    n_events: int
    mode: int
    maximum: int
    mean: float
    standard_deviation: float
    coefficient_of_variation: float
    gini: float
    q50: int
    q75: int
    q90: int
    q95: int
    q99: int
    q999: int


@dataclass(frozen=True)
class DistributionDistance:
    total_variation: float
    jensen_shannon: float
    kolmogorov_smirnov: float
    wasserstein: float


def _validate_histogram(histogram: np.ndarray) -> np.ndarray:
    counts = np.asarray(histogram)
    if counts.ndim != 1:
        raise ValueError("histogram must be one-dimensional")
    if np.any(counts < 0):
        raise ValueError("histogram counts must be nonnegative")
    if not np.issubdtype(counts.dtype, np.integer):
        if not np.all(counts == np.rint(counts)):
            raise ValueError("histogram counts must be integers")
        counts = np.rint(counts).astype(np.int64)
    return counts.astype(np.int64, copy=False)


def condition_histogram(histogram: np.ndarray, minimum_size: int) -> np.ndarray:
    """Return a copy containing only sizes at or above ``minimum_size``."""
    if minimum_size < 1:
        raise ValueError("minimum_size must be positive")
    counts = _validate_histogram(histogram).copy()
    counts[: min(minimum_size, counts.size)] = 0
    if counts.sum() == 0:
        raise ValueError(f"histogram has no events with size >= {minimum_size}")
    return counts


def histogram_quantiles(
    histogram: np.ndarray, probabilities: tuple[float, ...]
) -> tuple[int, ...]:
    """Return exact inverse-empirical-CDF quantiles from integer counts."""
    counts = _validate_histogram(histogram)
    n = int(counts.sum())
    if n == 0:
        raise ValueError("empty histogram")
    requested = np.asarray(probabilities, dtype=float)
    if np.any((requested < 0.0) | (requested > 1.0)):
        raise ValueError("quantile probabilities must lie in [0, 1]")
    cumulative = np.cumsum(counts, dtype=np.int64)
    ranks = np.maximum(1, np.ceil(requested * n).astype(np.int64))
    return tuple(int(value) for value in np.searchsorted(cumulative, ranks, side="left"))


def summarize_histogram(
    histogram: np.ndarray, *, population: str, minimum_size: int
) -> DistributionSummary:
    """Calculate exact count-weighted descriptive statistics."""
    counts = condition_histogram(histogram, minimum_size)
    sizes = np.flatnonzero(counts)
    frequencies = counts[sizes]
    n = int(frequencies.sum())
    total_size = float(np.dot(sizes.astype(float), frequencies.astype(float)))
    mean = total_size / n
    centered = sizes.astype(float) - mean
    variance = float(np.dot(centered * centered, frequencies) / n)

    cumulative_before = np.cumsum(frequencies, dtype=np.int64) - frequencies
    gini_numerator = float(
        np.dot(
            (2 * cumulative_before + frequencies - n).astype(float),
            sizes.astype(float) * frequencies,
        )
    )
    gini = gini_numerator / (n * total_size) if total_size else 0.0
    quantiles = histogram_quantiles(
        counts, (0.50, 0.75, 0.90, 0.95, 0.99, 0.999)
    )
    standard_deviation = float(np.sqrt(variance))
    return DistributionSummary(
        population=population,
        minimum_size=minimum_size,
        n_events=n,
        mode=int(sizes[np.argmax(frequencies)]),
        maximum=int(sizes[-1]),
        mean=mean,
        standard_deviation=standard_deviation,
        coefficient_of_variation=standard_deviation / mean,
        gini=gini,
        q50=quantiles[0],
        q75=quantiles[1],
        q90=quantiles[2],
        q95=quantiles[3],
        q99=quantiles[4],
        q999=quantiles[5],
    )


def tail_probability(histogram: np.ndarray, threshold: int) -> float:
    """Return the empirical probability P(S >= threshold)."""
    if threshold < 1:
        raise ValueError("threshold must be positive")
    counts = _validate_histogram(histogram)
    n = int(counts.sum())
    if n == 0:
        raise ValueError("empty histogram")
    return float(counts[threshold:].sum() / n) if threshold < counts.size else 0.0


def distribution_distance(
    first: np.ndarray, second: np.ndarray, *, minimum_size: int = 1
) -> DistributionDistance:
    """Compare two empirical PMFs using four sample-size-independent distances."""
    first_counts = condition_histogram(first, minimum_size)
    second_counts = condition_histogram(second, minimum_size)
    support_size = max(first_counts.size, second_counts.size)
    first_counts = np.pad(first_counts, (0, support_size - first_counts.size))
    second_counts = np.pad(second_counts, (0, support_size - second_counts.size))
    first_pmf = first_counts / first_counts.sum()
    second_pmf = second_counts / second_counts.sum()
    first_cdf = np.cumsum(first_pmf)
    second_cdf = np.cumsum(second_pmf)
    support = np.arange(support_size, dtype=float)
    return DistributionDistance(
        total_variation=float(0.5 * np.abs(first_pmf - second_pmf).sum()),
        jensen_shannon=float(
            spatial.distance.jensenshannon(first_pmf, second_pmf, base=2.0)
        ),
        kolmogorov_smirnov=float(np.max(np.abs(first_cdf - second_cdf))),
        wasserstein=float(
            stats.wasserstein_distance(
                support,
                support,
                u_weights=first_pmf,
                v_weights=second_pmf,
            )
        ),
    )

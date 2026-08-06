"""Nonparametric behavior metrics for exact discrete avalanche histograms."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .full_distribution import condition_histogram, histogram_quantiles


@dataclass(frozen=True)
class TwoScaleSplit:
    small_maximum: int
    large_minimum: int
    small_fraction: float
    large_fraction: float
    explained_log_variance: float
    small_geometric_mean: float
    large_geometric_mean: float
    small_median: int
    large_q25: int
    large_median: int
    large_q75: int
    large_q90: int
    large_q99: int


def _positive_arrays(histogram: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    counts = np.asarray(histogram, dtype=np.int64)
    sizes = np.flatnonzero(counts)
    frequencies = counts[sizes]
    if sizes.size < 2 or np.any(sizes < 1) or np.any(frequencies <= 0):
        raise ValueError("histogram needs at least two positive size categories")
    return sizes, frequencies


def characteristic_size(histogram: np.ndarray, *, minimum_size: int = 2) -> float:
    """Return <S^2>/<S>, a nonparametric size-weighted scale."""
    counts = condition_histogram(histogram, minimum_size)
    sizes, frequencies = _positive_arrays(counts)
    first = float(np.dot(sizes.astype(float), frequencies))
    second = float(np.dot(sizes.astype(float) ** 2, frequencies))
    return second / first


def top_event_damage_share(
    histogram: np.ndarray, fraction: float, *, minimum_size: int = 2
) -> tuple[float, float]:
    """Return actual event fraction and size share carried by the largest events."""
    if not 0.0 < fraction <= 1.0:
        raise ValueError("fraction must lie in (0, 1]")
    counts = condition_histogram(histogram, minimum_size)
    sizes, frequencies = _positive_arrays(counts)
    target = max(1, int(np.ceil(fraction * frequencies.sum())))
    remaining = target
    selected_size = 0.0
    for size, count in zip(sizes[::-1], frequencies[::-1], strict=True):
        take = min(remaining, int(count))
        selected_size += take * int(size)
        remaining -= take
        if remaining == 0:
            break
    total_size = float(np.dot(sizes.astype(float), frequencies))
    return target / int(frequencies.sum()), selected_size / total_size


def lorenz_curve(
    histogram: np.ndarray,
    *,
    minimum_size: int = 2,
    points: int = 1001,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the exact piecewise-linear Lorenz curve on a regular event grid."""
    if points < 2:
        raise ValueError("points must be at least two")
    counts = condition_histogram(histogram, minimum_size)
    sizes, frequencies = _positive_arrays(counts)
    cumulative_events = np.concatenate(([0.0], np.cumsum(frequencies, dtype=float)))
    cumulative_size = np.concatenate(
        ([0.0], np.cumsum(sizes.astype(float) * frequencies))
    )
    cumulative_events /= cumulative_events[-1]
    cumulative_size /= cumulative_size[-1]
    event_grid = np.linspace(0.0, 1.0, points)
    return event_grid, np.interp(event_grid, cumulative_events, cumulative_size)


def _subset_quantiles(
    sizes: np.ndarray, frequencies: np.ndarray, probabilities: tuple[float, ...]
) -> tuple[int, ...]:
    histogram = np.zeros(int(sizes[-1]) + 1, dtype=np.int64)
    histogram[sizes] = frequencies
    return histogram_quantiles(histogram, probabilities)


def split_two_scales(
    histogram: np.ndarray, *, minimum_size: int = 2
) -> TwoScaleSplit:
    """Find the exact two-means partition minimizing weighted variance in log S."""
    counts = condition_histogram(histogram, minimum_size)
    sizes, frequencies = _positive_arrays(counts)
    logs = np.log(sizes.astype(float))
    weights = frequencies.astype(float)
    cumulative_w = np.cumsum(weights)
    cumulative_wx = np.cumsum(weights * logs)
    cumulative_wx2 = np.cumsum(weights * logs * logs)
    total_w = cumulative_w[-1]
    total_wx = cumulative_wx[-1]
    total_wx2 = cumulative_wx2[-1]
    first_w = cumulative_w[:-1]
    second_w = total_w - first_w
    first_sse = cumulative_wx2[:-1] - cumulative_wx[:-1] ** 2 / first_w
    second_sse = (
        total_wx2
        - cumulative_wx2[:-1]
        - (total_wx - cumulative_wx[:-1]) ** 2 / second_w
    )
    split_index = int(np.argmin(first_sse + second_sse))
    total_sse = total_wx2 - total_wx**2 / total_w
    best_sse = float(first_sse[split_index] + second_sse[split_index])
    small_sizes = sizes[: split_index + 1]
    small_frequencies = frequencies[: split_index + 1]
    large_sizes = sizes[split_index + 1 :]
    large_frequencies = frequencies[split_index + 1 :]
    small_weight = float(small_frequencies.sum())
    large_weight = float(large_frequencies.sum())
    large_quantiles = _subset_quantiles(
        large_sizes, large_frequencies, (0.25, 0.50, 0.75, 0.90, 0.99)
    )
    return TwoScaleSplit(
        small_maximum=int(small_sizes[-1]),
        large_minimum=int(large_sizes[0]),
        small_fraction=small_weight / total_w,
        large_fraction=large_weight / total_w,
        explained_log_variance=1.0 - best_sse / total_sse,
        small_geometric_mean=float(
            np.exp(np.dot(np.log(small_sizes), small_frequencies) / small_weight)
        ),
        large_geometric_mean=float(
            np.exp(np.dot(np.log(large_sizes), large_frequencies) / large_weight)
        ),
        small_median=_subset_quantiles(small_sizes, small_frequencies, (0.50,))[0],
        large_q25=large_quantiles[0],
        large_median=large_quantiles[1],
        large_q75=large_quantiles[2],
        large_q90=large_quantiles[3],
        large_q99=large_quantiles[4],
    )


def ccdf_crossings(
    first: np.ndarray,
    second: np.ndarray,
    *,
    minimum_size: int = 2,
    minimum_survival: float = 1e-5,
    minimum_difference: float = 1e-8,
) -> tuple[tuple[int, float, float], ...]:
    """Locate sign changes in adjacent empirical CCDF differences."""
    first = condition_histogram(first, minimum_size)
    second = condition_histogram(second, minimum_size)
    support_size = max(first.size, second.size)
    first = np.pad(first, (0, support_size - first.size))
    second = np.pad(second, (0, support_size - second.size))
    first_survival = np.cumsum(first[::-1], dtype=float)[::-1] / first.sum()
    second_survival = np.cumsum(second[::-1], dtype=float)[::-1] / second.sum()
    difference = second_survival - first_survival
    crossings: list[tuple[int, float, float]] = []
    for size in range(minimum_size, support_size - 1):
        if max(first_survival[size], second_survival[size]) < minimum_survival:
            continue
        before = difference[size]
        after = difference[size + 1]
        if (
            np.signbit(before) != np.signbit(after)
            and abs(before) >= minimum_difference
            and abs(after) >= minimum_difference
        ):
            crossings.append((size, float(before), float(after)))
    return tuple(crossings)


def normalized_quantile_distance(
    first: np.ndarray,
    second: np.ndarray,
    *,
    first_minimum: int,
    second_minimum: int,
    points: int = 999,
) -> float:
    """Mean absolute log-quantile distance after median normalization."""
    probabilities = tuple(np.linspace(0.001, 0.999, points))
    first_counts = condition_histogram(first, first_minimum)
    second_counts = condition_histogram(second, second_minimum)
    first_quantiles = np.asarray(histogram_quantiles(first_counts, probabilities))
    second_quantiles = np.asarray(histogram_quantiles(second_counts, probabilities))
    first_median = histogram_quantiles(first_counts, (0.5,))[0]
    second_median = histogram_quantiles(second_counts, (0.5,))[0]
    return float(
        np.mean(
            np.abs(
                np.log(first_quantiles / first_median)
                - np.log(second_quantiles / second_median)
            )
        )
    )


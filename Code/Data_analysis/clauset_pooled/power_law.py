"""Exact discrete power-law fitting for pooled local-avalanche sizes."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import optimize, special


Histogram = np.ndarray | Mapping[int, int]


@dataclass(frozen=True)
class PowerLawFit:
    xmin: int
    alpha: float
    ks: float
    log_likelihood: float
    n_tail: int


def read_size_histogram(
    path: Path, *, minimum_size: int = 2, chunk_bytes: int = 8 * 1024 * 1024
) -> np.ndarray:
    """Read a headerless size file into an exact size-indexed histogram."""
    if minimum_size < 1:
        raise ValueError("minimum_size must be positive")
    if chunk_bytes < 1:
        raise ValueError("chunk_bytes must be positive")

    histogram = np.zeros(minimum_size + 1, dtype=np.int64)
    remainder = b""
    with path.open("rb") as stream:
        while block := stream.read(chunk_bytes):
            data = remainder + block
            complete, separator, remainder = data.rpartition(b"\n")
            if not separator:
                remainder = data
                continue
            values = np.fromstring(complete, dtype=np.int64, sep="\n")
            if values.size:
                if np.any(values < 1):
                    raise ValueError(f"{path} contains a non-positive avalanche size")
                selected = values[values >= minimum_size]
                if selected.size:
                    counts = np.bincount(selected)
                    if counts.size > histogram.size:
                        histogram = np.pad(histogram, (0, counts.size - histogram.size))
                    histogram[: counts.size] += counts
    if remainder.strip():
        try:
            final_value = int(remainder)
        except ValueError as error:
            raise ValueError(f"{path} ends with an invalid avalanche size") from error
        if final_value < 1:
            raise ValueError(f"{path} contains a non-positive avalanche size")
        if final_value >= minimum_size:
            if final_value >= histogram.size:
                histogram = np.pad(histogram, (0, final_value + 1 - histogram.size))
            histogram[final_value] += 1
    if histogram.sum() == 0:
        raise ValueError(f"{path} contains no sizes >= {minimum_size}")
    return histogram


def _log_scaled_zeta(alpha: float, xmin: int) -> float:
    """Return log[xmin**alpha * zeta(alpha, xmin)] without underflow."""
    if alpha <= 1.0:
        return float("inf")
    log_scale = alpha * np.log(float(xmin))
    zeta_value = special.zeta(alpha, float(xmin))
    if np.isfinite(zeta_value) and zeta_value > 0.0:
        return float(np.log(zeta_value) + log_scale)

    total = 0.0
    lower = xmin
    while True:
        upper = lower + 4096
        support = np.arange(lower, upper, dtype=float)
        total += float(np.exp(-alpha * np.log(support / xmin)).sum())
        tail_bound = (
            upper
            * np.exp(-alpha * np.log(upper / xmin))
            / (alpha - 1.0)
        )
        if tail_bound <= 1e-14 * total:
            return float(np.log(total))
        lower = upper


def _log_zeta(alpha: float, xmin: int) -> float:
    return _log_scaled_zeta(alpha, xmin) - alpha * np.log(float(xmin))


def histogram_arrays(histogram: Histogram) -> tuple[np.ndarray, np.ndarray]:
    """Return sorted observed sizes and positive integer frequencies."""
    if isinstance(histogram, Mapping):
        items = sorted((int(size), int(count)) for size, count in histogram.items() if count)
        if not items:
            raise ValueError("empty histogram")
        sizes = np.array([size for size, _ in items], dtype=np.int64)
        frequencies = np.array([count for _, count in items], dtype=np.int64)
    else:
        counts = np.asarray(histogram)
        if counts.ndim != 1:
            raise ValueError("histogram must be one-dimensional")
        sizes = np.flatnonzero(counts)
        frequencies = counts[sizes]
        if not np.issubdtype(frequencies.dtype, np.integer):
            if not np.all(frequencies == np.rint(frequencies)):
                raise ValueError("histogram frequencies must be integers")
            frequencies = np.rint(frequencies).astype(np.int64)
        else:
            frequencies = frequencies.astype(np.int64, copy=False)
    if np.any(sizes < 1) or np.any(frequencies <= 0):
        raise ValueError("sizes and frequencies must be positive integers")
    return sizes, frequencies


def fit_alpha(histogram: Histogram, xmin: int) -> tuple[float, float]:
    """Fit alpha by exact maximum likelihood on integer sizes >= xmin."""
    if xmin < 1:
        raise ValueError("xmin must be positive")
    all_sizes, all_frequencies = histogram_arrays(histogram)
    selected = all_sizes >= xmin
    sizes = all_sizes[selected]
    frequencies = all_frequencies[selected]
    n = int(frequencies.sum())
    if n == 0:
        raise ValueError("empty tail")
    sum_log_ratio = float(np.dot(frequencies, np.log(sizes / float(xmin))))
    if sum_log_ratio <= 0.0:
        raise ValueError("alpha is unbounded because every tail value equals xmin")

    def negative_log_likelihood(alpha: float) -> float:
        normalization = _log_scaled_zeta(alpha, xmin)
        return n * normalization + alpha * sum_log_ratio

    upper = 4.0
    previous = negative_log_likelihood(2.0)
    current = negative_log_likelihood(upper)
    while current < previous:
        previous = current
        upper *= 2.0
        current = negative_log_likelihood(upper)
        if upper > 1e8:
            raise RuntimeError("failed to bracket a finite alpha estimate")

    result = optimize.minimize_scalar(
        negative_log_likelihood,
        bounds=(1.0 + 1e-10, upper),
        method="bounded",
        options={"xatol": 1e-11, "maxiter": 1000},
    )
    if not result.success or not np.isfinite(result.fun):
        raise RuntimeError(f"alpha optimization failed: {result.message}")
    alpha = float(result.x)
    log_likelihood = -float(result.fun)
    return alpha, log_likelihood


def power_law_cdf(values: np.ndarray, *, xmin: int, alpha: float) -> np.ndarray:
    """Evaluate P(X <= value | X >= xmin) for the discrete power law."""
    values = np.asarray(values, dtype=np.int64)
    result = np.zeros(values.shape, dtype=float)
    selected = values >= xmin
    if np.any(selected):
        thresholds = values[selected] + 1
        denominator = special.zeta(alpha, float(xmin))
        numerators = special.zeta(alpha, thresholds.astype(float))
        if (
            np.isfinite(denominator)
            and denominator > 0.0
            and np.all(np.isfinite(numerators))
            and np.all(numerators > 0.0)
        ):
            log_survival = np.log(numerators) - np.log(denominator)
        else:
            denominator_log = _log_zeta(alpha, xmin)
            log_survival = np.array(
                [_log_zeta(alpha, int(value)) - denominator_log for value in thresholds]
            )
        result[selected] = -np.expm1(log_survival)
    return np.clip(result, 0.0, 1.0)


def discrete_ks(histogram: Histogram, *, xmin: int, alpha: float) -> float:
    """Compute the two-sided KS distance for an integer-valued tail."""
    all_sizes, all_frequencies = histogram_arrays(histogram)
    selected = all_sizes >= xmin
    sizes = all_sizes[selected]
    frequencies = all_frequencies[selected]
    return _discrete_ks_arrays(sizes, frequencies, xmin=xmin, alpha=alpha)


def _discrete_ks_arrays(
    sizes: np.ndarray, frequencies: np.ndarray, *, xmin: int, alpha: float
) -> float:
    n = int(frequencies.sum())
    cumulative = np.cumsum(frequencies, dtype=np.int64) / n
    empirical_before = (np.cumsum(frequencies) - frequencies) / n
    after = np.abs(cumulative - power_law_cdf(sizes, xmin=xmin, alpha=alpha))
    before = np.abs(
        empirical_before - power_law_cdf(sizes - 1, xmin=xmin, alpha=alpha)
    )
    return float(max(after.max(), before.max()))


def _batch_alpha_estimates(
    xmins: np.ndarray, tail_counts: np.ndarray, tail_log_sums: np.ndarray
) -> np.ndarray:
    """Solve all discrete likelihood equations together by Newton iteration."""
    xmins_float = xmins.astype(float)
    n = tail_counts.astype(float)
    mean_log = tail_log_sums / n
    denominator = tail_log_sums - n * np.log(xmins_float - 0.5)
    alpha = 1.0 + n / denominator
    alpha = np.maximum(alpha, 1.0 + 1e-8)

    for _ in range(30):
        step = 1e-4 * np.maximum(1.0, alpha)
        log_zeta = np.log(special.zeta(alpha, xmins_float))
        log_zeta_plus = np.log(special.zeta(alpha + step, xmins_float))
        log_zeta_minus = np.log(special.zeta(alpha - step, xmins_float))
        gradient = (log_zeta_plus - log_zeta_minus) / (2.0 * step) + mean_log
        curvature = (
            log_zeta_plus - 2.0 * log_zeta + log_zeta_minus
        ) / step**2
        update = gradient / curvature
        next_alpha = np.maximum(1.0 + 1e-9, alpha - update)
        if float(np.max(np.abs(next_alpha - alpha))) < 1e-9:
            alpha = next_alpha
            break
        alpha = next_alpha
    if not np.all(np.isfinite(alpha)):
        raise RuntimeError("batched alpha estimation produced a non-finite value")
    return alpha


def _screen_candidate_ks(
    sizes: np.ndarray,
    frequencies: np.ndarray,
    candidate_indices: np.ndarray,
    tail_counts: np.ndarray,
    candidate_alphas: np.ndarray,
) -> np.ndarray:
    """Compute a lower-dimensional KS screen at early and quantile points."""
    cumulative = np.cumsum(frequencies, dtype=np.int64)
    previous = np.where(
        candidate_indices > 0, cumulative[candidate_indices - 1], 0
    )
    n = tail_counts[candidate_indices]
    quantiles = np.linspace(0.0, 1.0, 65)
    targets = previous[:, None] + n[:, None] * quantiles[None, :]
    quantile_indices = np.searchsorted(cumulative, targets.ravel()).reshape(
        targets.shape
    )
    quantile_indices = np.maximum(quantile_indices, candidate_indices[:, None])
    quantile_indices = np.minimum(quantile_indices, sizes.size - 1)
    early_indices = np.minimum(
        candidate_indices[:, None] + np.arange(32)[None, :], sizes.size - 1
    )
    evaluation_indices = np.concatenate((early_indices, quantile_indices), axis=1)
    evaluation_sizes = sizes[evaluation_indices]
    empirical_after = (
        cumulative[evaluation_indices] - previous[:, None]
    ) / n[:, None]
    empirical_before = (
        cumulative[evaluation_indices]
        - frequencies[evaluation_indices]
        - previous[:, None]
    ) / n[:, None]

    normalization = special.zeta(candidate_alphas, sizes[candidate_indices])
    model_after = 1.0 - special.zeta(
        candidate_alphas[:, None], evaluation_sizes + 1.0
    ) / normalization[:, None]
    model_before = 1.0 - special.zeta(
        candidate_alphas[:, None], evaluation_sizes
    ) / normalization[:, None]
    if not np.all(np.isfinite(model_after)) or not np.all(np.isfinite(model_before)):
        raise RuntimeError("candidate KS screen encountered numerical underflow")
    return np.maximum(
        np.max(np.abs(empirical_after - model_after), axis=1),
        np.max(np.abs(empirical_before - model_before), axis=1),
    )


def select_xmin(
    histogram: Histogram, *, minimum_xmin: int = 2, minimum_tail: int = 1000
) -> PowerLawFit:
    """Select xmin by exhaustive minimization of the exact discrete KS."""
    all_sizes, all_frequencies = histogram_arrays(histogram)
    selected = all_sizes >= minimum_xmin
    sizes = all_sizes[selected]
    frequencies = all_frequencies[selected]
    if sizes.size < 2:
        raise ValueError("at least two distinct sizes are required")
    tail_counts = np.cumsum(frequencies[::-1], dtype=np.int64)[::-1]
    tail_log_sums = np.cumsum(
        (frequencies * np.log(sizes))[::-1], dtype=float
    )[::-1]
    candidate_indices = np.flatnonzero(tail_counts >= minimum_tail)
    candidate_indices = candidate_indices[candidate_indices < sizes.size - 1]
    if candidate_indices.size == 0:
        raise ValueError("no xmin candidate satisfies the minimum tail size")

    candidate_alphas = _batch_alpha_estimates(
        sizes[candidate_indices],
        tail_counts[candidate_indices],
        tail_log_sums[candidate_indices],
    )
    screened_ks = _screen_candidate_ks(
        sizes, frequencies, candidate_indices, tail_counts, candidate_alphas
    )
    ranked_positions = np.argsort(screened_ks)[: min(128, candidate_indices.size)]
    evaluation_positions = set(range(min(64, candidate_indices.size)))
    for position in ranked_positions:
        for neighbor in (int(position) - 1, int(position), int(position) + 1):
            if 0 <= neighbor < candidate_indices.size:
                evaluation_positions.add(neighbor)

    complete_ks: dict[int, float] = {}
    for position in evaluation_positions:
        index = int(candidate_indices[position])
        complete_ks[position] = _discrete_ks_arrays(
            sizes[index:],
            frequencies[index:],
            xmin=int(sizes[index]),
            alpha=float(candidate_alphas[position]),
        )

    incumbent = min(complete_ks.values())
    for position in np.flatnonzero(screened_ks <= incumbent + 1e-6):
        integer_position = int(position)
        if integer_position in complete_ks:
            continue
        index = int(candidate_indices[integer_position])
        complete_ks[integer_position] = _discrete_ks_arrays(
            sizes[index:],
            frequencies[index:],
            xmin=int(sizes[index]),
            alpha=float(candidate_alphas[integer_position]),
        )

    # Recompute every numerical finalist with the scalar optimizer.  The batch
    # solve only accelerates screening; the reported fit is the exact MLE.
    threshold = min(complete_ks.values()) + 1e-7
    finalist_positions = [
        position for position, ks in complete_ks.items() if ks <= threshold
    ]
    finalists: list[PowerLawFit] = []
    for position in finalist_positions:
        index = int(candidate_indices[position])
        xmin = int(sizes[index])
        alpha, log_likelihood = fit_alpha(histogram, xmin)
        ks = _discrete_ks_arrays(
            sizes[index:], frequencies[index:], xmin=xmin, alpha=alpha
        )
        finalists.append(
            PowerLawFit(
                xmin=xmin,
                alpha=alpha,
                ks=ks,
                log_likelihood=log_likelihood,
                n_tail=int(tail_counts[index]),
            )
        )
    return min(finalists, key=lambda fit: (fit.ks, fit.xmin))

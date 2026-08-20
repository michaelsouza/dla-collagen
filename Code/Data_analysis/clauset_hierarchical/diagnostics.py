"""Diagnostics for representation, ensemble size, and finite fibril size."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import duckdb
import numpy as np
from scipy import stats

from clauset_pooled.power_law import PowerLawFit, select_xmin

from .analysis import FibrilHistograms


@dataclass(frozen=True)
class SubsetFit:
    subset_size: int
    replicate: int
    alpha: float
    xmin: int
    ks: float
    n_tail: int
    tail_fraction: float
    contributing_fibrils: int


def weighted_quantile(histogram: np.ndarray, probability: float) -> int:
    """Return the left-continuous quantile of an integer histogram."""
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between zero and one")
    counts = np.asarray(histogram, dtype=np.int64)
    total = int(counts.sum())
    if total < 1:
        raise ValueError("empty histogram")
    target = max(1, int(np.ceil(probability * total)))
    return int(np.searchsorted(np.cumsum(counts, dtype=np.int64), target))


def subset_stability(
    data: FibrilHistograms,
    *,
    subset_sizes: tuple[int, ...] = (10, 20, 30, 40, 50),
    repetitions: int = 100,
    minimum_xmin: int = 1,
    minimum_tail: int = 1000,
    seed: int = 12738,
) -> tuple[SubsetFit, ...]:
    """Refit random fibril subsets without replacing events within a fibril."""
    if repetitions < 1:
        raise ValueError("repetitions must be positive")
    if any(size < 2 or size > data.fibrils for size in subset_sizes):
        raise ValueError("subset sizes must be between two and the fibril count")
    rng = np.random.default_rng(seed)
    results: list[SubsetFit] = []
    for size in subset_sizes:
        local_repetitions = 1 if size == data.fibrils else repetitions
        for replicate in range(local_repetitions):
            indices = (
                np.arange(data.fibrils)
                if size == data.fibrils
                else rng.choice(data.fibrils, size=size, replace=False)
            )
            counts = data.counts[indices]
            pooled = counts.sum(axis=0, dtype=np.int64)
            fitted = select_xmin(
                pooled,
                minimum_xmin=minimum_xmin,
                minimum_tail=minimum_tail,
            )
            results.append(
                SubsetFit(
                    subset_size=size,
                    replicate=replicate,
                    alpha=fitted.alpha,
                    xmin=fitted.xmin,
                    ks=fitted.ks,
                    n_tail=fitted.n_tail,
                    tail_fraction=fitted.n_tail / int(pooled.sum()),
                    contributing_fibrils=int(
                        np.count_nonzero(counts[:, fitted.xmin :].sum(axis=1))
                    ),
                )
            )
    return tuple(results)


def leave_one_fibril_out(
    data: FibrilHistograms,
    *,
    minimum_xmin: int = 1,
    minimum_tail: int = 1000,
) -> tuple[tuple[int, PowerLawFit], ...]:
    """Refit after deleting each entire fibril geometry once."""
    results = []
    for index, omitted_seed in enumerate(data.seeds):
        pooled = data.pooled - data.counts[index]
        results.append(
            (
                int(omitted_seed),
                select_xmin(
                    pooled,
                    minimum_xmin=minimum_xmin,
                    minimum_tail=minimum_tail,
                ),
            )
        )
    return tuple(results)


def initial_fibril_sizes(database: str | Path, ts: int) -> dict[int, int]:
    """Read and validate the initial active backbone size for every geometry."""
    connection = duckdb.connect(str(database), read_only=True)
    try:
        rows = connection.execute(
            """
            SELECT seed, min(num_active_particles), max(num_active_particles),
                   count(DISTINCT realization)
            FROM force_steps
            WHERE ts = ? AND step_index = 0
            GROUP BY seed ORDER BY seed
            """,
            [ts],
        ).fetchall()
    finally:
        connection.close()
    if not rows:
        raise ValueError(f"Ts={ts}: missing initial backbone sizes")
    result: dict[int, int] = {}
    for seed, minimum, maximum, realizations in rows:
        if int(minimum) != int(maximum):
            raise ValueError(f"Ts={ts}, seed={seed}: initial size varies by run")
        if int(realizations) != 1000:
            raise ValueError(f"Ts={ts}, seed={seed}: expected 1000 realizations")
        result[int(seed)] = int(minimum)
    return result


def tail_realization_counts(
    database: str | Path, ts: int, xmin: int
) -> tuple[int, dict[int, int]]:
    """Count runs and per-fibril runs represented above the selected cutoff."""
    connection = duckdb.connect(str(database), read_only=True)
    try:
        rows = connection.execute(
            """
            SELECT seed, count(DISTINCT realization)
            FROM run_histograms
            WHERE ts = ? AND NOT is_terminal_step AND avalanche_size >= ?
            GROUP BY seed ORDER BY seed
            """,
            [ts, xmin],
        ).fetchall()
    finally:
        connection.close()
    per_fibril = {int(seed): int(count) for seed, count in rows}
    return int(sum(per_fibril.values())), per_fibril


def spearman_with_p(first: np.ndarray, second: np.ndarray) -> tuple[float, float]:
    """Return a finite Spearman coefficient and two-sided p-value."""
    result = stats.spearmanr(first, second)
    return float(result.statistic), float(result.pvalue)

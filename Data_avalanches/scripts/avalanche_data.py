#!/usr/bin/env python3
"""Loading and validation helpers for the local-avalanche PMF files."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np


FILE_PATTERN = re.compile(
    r"^local_avalanches_Ts_(?P<ts>\d+)_(?P<terminal>com|sem)_terminal\.dat$"
)


@dataclass(frozen=True)
class AvalancheDistribution:
    """One empirical local-avalanche probability mass function."""

    path: Path
    ts: int
    includes_terminal: bool
    sizes: np.ndarray
    probabilities: np.ndarray

    @property
    def terminal_label(self) -> str:
        return "com_terminal" if self.includes_terminal else "sem_terminal"

    def infer_counts(self, *, tolerance: float = 1e-7) -> np.ndarray:
        """Reconstruct exact integer frequencies from the probability quantum.

        Every supplied PMF contains at least one size observed exactly once, so
        its smallest positive probability is 1/N. The returned array is indexed
        directly by avalanche size and contains zeros for unobserved sizes.
        """
        total_events = int(round(1.0 / float(self.probabilities.min())))
        observed_counts = np.rint(self.probabilities * total_events).astype(np.int64)
        reconstructed = observed_counts / total_events
        if not np.allclose(
            reconstructed, self.probabilities, rtol=tolerance, atol=1e-15
        ):
            raise ValueError(
                f"{self.path}: probabilities are not integer multiples of 1/N"
            )
        if int(observed_counts.sum()) != total_events:
            raise ValueError(
                f"{self.path}: reconstructed counts sum to {observed_counts.sum()}, "
                f"expected {total_events}"
            )
        counts = np.zeros(int(self.sizes[-1]) + 1, dtype=np.int64)
        counts[self.sizes] = observed_counts
        return counts


def load_distribution(path: Path) -> AvalancheDistribution:
    """Load one two-column ``size probability`` file and validate its PMF."""
    match = FILE_PATTERN.match(path.name)
    if match is None:
        raise ValueError(f"unexpected avalanche filename: {path.name}")

    values = np.loadtxt(path, dtype=float)
    if values.ndim != 2 or values.shape[1] != 2:
        raise ValueError(f"{path}: expected exactly two numeric columns")

    raw_sizes = values[:, 0]
    sizes = np.rint(raw_sizes).astype(np.int64)
    probabilities = values[:, 1]
    if not np.array_equal(raw_sizes, sizes):
        raise ValueError(f"{path}: avalanche sizes must be integers")
    if np.any(sizes < 1) or np.any(np.diff(sizes) <= 0):
        raise ValueError(f"{path}: sizes must be positive and strictly increasing")
    if np.any(~np.isfinite(probabilities)) or np.any(probabilities <= 0.0):
        raise ValueError(f"{path}: probabilities must be finite and positive")
    if not np.isclose(probabilities.sum(), 1.0, rtol=0.0, atol=5e-13):
        raise ValueError(
            f"{path}: probabilities sum to {probabilities.sum():.16g}, not one"
        )

    distribution = AvalancheDistribution(
        path=path,
        ts=int(match.group("ts")),
        includes_terminal=match.group("terminal") == "com",
        sizes=sizes,
        probabilities=probabilities,
    )
    distribution.infer_counts()
    return distribution


def discover_distributions(data_dir: Path) -> list[AvalancheDistribution]:
    """Discover and load the complete set of supplied avalanche PMFs."""
    paths = sorted(data_dir.glob("local_avalanches_Ts_*_*_terminal.dat"))
    distributions = [load_distribution(path) for path in paths]
    if not distributions:
        raise ValueError(f"no avalanche PMF files found in {data_dir}")

    seen = {(item.ts, item.includes_terminal) for item in distributions}
    if len(seen) != len(distributions):
        raise ValueError("duplicate Ts/terminal population in the input files")

    ts_values = {item.ts for item in distributions}
    for ts in ts_values:
        if (ts, True) not in seen or (ts, False) not in seen:
            raise ValueError(f"Ts={ts}: both terminal populations are required")
    return sorted(distributions, key=lambda item: (item.ts, item.includes_terminal))


def padded_counts(
    first: AvalancheDistribution, second: AvalancheDistribution
) -> tuple[np.ndarray, np.ndarray]:
    """Return two reconstructed histograms on a common integer support."""
    first_counts = first.infer_counts()
    second_counts = second.infer_counts()
    support = max(first_counts.size, second_counts.size)
    return (
        np.pad(first_counts, (0, support - first_counts.size)),
        np.pad(second_counts, (0, support - second_counts.size)),
    )

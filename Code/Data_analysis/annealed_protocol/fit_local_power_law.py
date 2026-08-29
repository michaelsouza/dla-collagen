#!/usr/bin/env python3
"""Fit exact discrete power laws to non-singleton local avalanche sizes.

The primary population is every local connected cluster with s >= 2,
including clusters recorded at the terminal force step.  Fits use the raw
integer frequencies, never binned densities.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize, special


@dataclass(frozen=True)
class PowerLawFit:
    ts: int
    xmin: int
    gamma: float
    ks: float
    n_total: int
    n_tail: int
    tail_fraction: float
    distinct_tail_sizes: int
    max_size: int
    tail_decades: float
    log_likelihood: float


def read_primary_counts(path: Path) -> dict[int, Counter[int]]:
    """Read all local clusters with s >= 2, including terminal clusters."""
    result: dict[int, Counter[int]] = defaultdict(Counter)
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["population"] != "all":
                continue
            size = int(row["local_size"])
            if size >= 2:
                result[int(row["ts"])][size] = int(row["frequency"])
    if not result:
        raise ValueError("frequency table contains no primary-population events")
    return result


def fit_gamma(sizes: np.ndarray, frequencies: np.ndarray, xmin: int) -> tuple[float, float]:
    """Exact MLE using the Hurwitz-zeta normalization."""
    n = int(frequencies.sum())
    sum_log_ratio = float(np.dot(frequencies, np.log(sizes / float(xmin))))

    def log_scaled_normalization(gamma: float) -> float:
        """Return log[xmin**gamma * zeta(gamma, xmin)] stably."""
        if gamma <= 1.0:
            return np.inf
        exponent = gamma * np.log(float(xmin))
        normalization = special.zeta(gamma, float(xmin))
        if np.isfinite(normalization) and normalization > 0.0 and exponent < 650.0:
            return float(np.log(normalization) + exponent)

        relative_sum = 0.0
        lower = xmin
        while True:
            upper = lower + 4096
            support = np.arange(lower, upper, dtype=float)
            relative_sum += float(
                np.exp(-gamma * np.log(support / float(xmin))).sum()
            )
            tail_bound = (
                upper
                * np.exp(-gamma * np.log(upper / float(xmin)))
                / (gamma - 1.0)
            )
            if tail_bound <= 1e-14 * relative_sum:
                return float(np.log(relative_sum))
            lower = upper

    def negative_log_likelihood(gamma: float) -> float:
        log_normalization = log_scaled_normalization(gamma)
        if not np.isfinite(log_normalization):
            return np.inf
        return n * log_normalization + gamma * sum_log_ratio

    if sum_log_ratio <= 0.0:
        raise ValueError("power-law exponent is unbounded when every size equals xmin")
    upper = 4.0
    previous = negative_log_likelihood(1.0 + 1e-8)
    current = negative_log_likelihood(upper)
    while current < previous:
        previous = current
        upper *= 2.0
        current = negative_log_likelihood(upper)
        if upper > 1e8:
            raise RuntimeError("could not bracket the finite power-law MLE")

    result = optimize.minimize_scalar(
        negative_log_likelihood,
        bounds=(1.0 + 1e-8, upper),
        method="bounded",
        options={"xatol": 1e-10, "maxiter": 1000},
    )
    if not result.success:
        raise RuntimeError(f"power-law optimization failed at xmin={xmin}: {result.message}")
    gamma = float(result.x)
    return gamma, -float(result.fun)


def discrete_ks(
    sizes: np.ndarray, frequencies: np.ndarray, xmin: int, gamma: float
) -> float:
    """KS distance accounting for both sides of jumps in a discrete CDF."""
    n = frequencies.sum()
    cumulative = np.cumsum(frequencies) / n
    empirical_before = (np.cumsum(frequencies) - frequencies) / n
    model_after = 1.0 - model_ccdf(sizes + 1, xmin, gamma)
    model_before = 1.0 - model_ccdf(sizes, xmin, gamma)
    return float(
        max(
            np.max(np.abs(cumulative - model_after)),
            np.max(np.abs(empirical_before - model_before)),
        )
    )


def select_xmin(
    ts: int,
    counts: Counter[int],
    *,
    min_tail: int = 1_000,
    min_distinct: int = 10,
) -> PowerLawFit:
    """Select observed xmin by minimum exact discrete KS distance."""
    all_sizes = np.array(sorted(counts), dtype=np.int64)
    all_frequencies = np.array([counts[int(size)] for size in all_sizes], dtype=np.int64)
    tail_counts = np.cumsum(all_frequencies[::-1], dtype=np.int64)[::-1]
    candidates = [
        index
        for index in range(len(all_sizes))
        if tail_counts[index] >= min_tail and len(all_sizes) - index >= min_distinct
    ]
    if not candidates:
        raise ValueError(f"Ts={ts} has no xmin satisfying the tail requirements")

    best: tuple[float, int, float, float] | None = None
    for index in candidates:
        sizes = all_sizes[index:]
        frequencies = all_frequencies[index:]
        xmin = int(sizes[0])
        gamma, log_likelihood = fit_gamma(sizes, frequencies, xmin)
        ks = discrete_ks(sizes, frequencies, xmin, gamma)
        candidate = (ks, xmin, gamma, log_likelihood)
        if best is None or candidate[:2] < best[:2]:
            best = candidate

    assert best is not None
    ks, xmin, gamma, log_likelihood = best
    start = int(np.searchsorted(all_sizes, xmin))
    n_total = int(all_frequencies.sum())
    n_tail = int(tail_counts[start])
    max_size = int(all_sizes[-1])
    return PowerLawFit(
        ts=ts,
        xmin=xmin,
        gamma=gamma,
        ks=ks,
        n_total=n_total,
        n_tail=n_tail,
        tail_fraction=n_tail / n_total,
        distinct_tail_sizes=len(all_sizes) - start,
        max_size=max_size,
        tail_decades=float(np.log10(max_size / xmin)),
        log_likelihood=log_likelihood,
    )


def empirical_ccdf(counts: Counter[int]) -> tuple[np.ndarray, np.ndarray]:
    sizes = np.array(sorted(counts), dtype=np.int64)
    frequencies = np.array([counts[int(size)] for size in sizes], dtype=np.int64)
    survival = np.cumsum(frequencies[::-1], dtype=np.int64)[::-1] / frequencies.sum()
    return sizes, survival


def model_ccdf(sizes: np.ndarray, xmin: int, gamma: float) -> np.ndarray:
    values = np.asarray(sizes, dtype=np.int64)
    normalization = special.zeta(gamma, float(xmin))
    numerator = special.zeta(gamma, values.astype(float))
    if np.isfinite(normalization) and normalization > 0.0 and np.all(np.isfinite(numerator)):
        return numerator / normalization

    largest = int(values.max())
    lower = xmin
    weights: list[np.ndarray] = []
    total = 0.0
    while True:
        upper = max(lower + 4096, largest + 1)
        support = np.arange(lower, upper, dtype=float)
        chunk = np.exp(-gamma * np.log(support / float(xmin)))
        weights.append(chunk)
        total += float(chunk.sum())
        tail_bound = (
            upper
            * np.exp(-gamma * np.log(upper / float(xmin)))
            / (gamma - 1.0)
        )
        if lower > largest and tail_bound <= 1e-14 * total:
            break
        lower = upper
    mass = np.concatenate(weights)
    survival = np.cumsum(mass[::-1])[::-1]
    indices = values - xmin
    return survival[indices] / survival[0]


def write_results(path: Path, fits: list[PowerLawFit]) -> None:
    fields = list(PowerLawFit.__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: getattr(fit, field) for field in fields} for fit in fits)


def plot_diagnostics(
    counts_by_ts: dict[int, Counter[int]], fits: list[PowerLawFit], output_dir: Path
) -> None:
    fig, axes = plt.subplots(5, 2, figsize=(10, 17), constrained_layout=True)
    for axis, fit in zip(axes.flat, fits):
        sizes, survival = empirical_ccdf(counts_by_ts[fit.ts])
        axis.step(sizes, survival, where="post", color="#555555", linewidth=1.1, label="Empirical")
        tail_sizes = sizes[sizes >= fit.xmin]
        tail_fraction = fit.tail_fraction
        fitted_survival = tail_fraction * model_ccdf(tail_sizes, fit.xmin, fit.gamma)
        axis.plot(tail_sizes, fitted_survival, color="#d7301f", linewidth=1.7, label="Power law fit")
        axis.axvline(fit.xmin, color="#255f85", linestyle="--", linewidth=1.0)
        axis.set(xscale="log", yscale="log")
        axis.set_title(
            rf"$T_s={fit.ts}$: $s_{{min}}={fit.xmin}$, $\hat{{\gamma}}={fit.gamma:.3f}$, "
            rf"$KS={fit.ks:.3f}$"
        )
        axis.set_xlabel(r"Local avalanche size, $s$")
        axis.set_ylabel(r"$P(S\geq s\mid S\geq2)$")
        axis.grid(which="both", alpha=0.2)
        axis.legend(frameon=False, fontsize=8)
    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"discrete_power_law_diagnostics.{suffix}", dpi=300)
    plt.close(fig)


def plot_parameter_summary(fits: list[PowerLawFit], output_dir: Path) -> None:
    ts = np.array([fit.ts for fit in fits])
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), constrained_layout=True)
    values = (
        ([fit.gamma for fit in fits], r"$\hat{\gamma}$"),
        ([fit.xmin for fit in fits], r"$\hat{s}_{min}$"),
        ([100 * fit.tail_fraction for fit in fits], "Events in fitted tail (%)"),
    )
    for axis, (y, ylabel) in zip(axes, values):
        axis.plot(ts, y, marker="o", color="#255f85")
        axis.set_xscale("log", base=2)
        axis.set_xticks(ts)
        axis.set_xticklabels([str(value) for value in ts], rotation=45)
        axis.set_xlabel(r"$T_s$")
        axis.set_ylabel(ylabel)
        axis.grid(alpha=0.25)
    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"discrete_power_law_parameter_summary.{suffix}", dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frequency_csv", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--min-tail", type=int, default=1_000)
    parser.add_argument("--min-distinct", type=int, default=10)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    counts_by_ts = read_primary_counts(args.frequency_csv)
    fits = [
        select_xmin(
            ts,
            counts_by_ts[ts],
            min_tail=args.min_tail,
            min_distinct=args.min_distinct,
        )
        for ts in sorted(counts_by_ts)
    ]
    write_results(args.output_dir / "discrete_power_law_fits.csv", fits)
    plot_diagnostics(counts_by_ts, fits, args.output_dir)
    plot_parameter_summary(fits, args.output_dir)
    for fit in fits:
        print(
            f"Ts={fit.ts:>4}: xmin={fit.xmin}, gamma={fit.gamma:.6f}, KS={fit.ks:.6f}, "
            f"tail={fit.n_tail}/{fit.n_total} ({100 * fit.tail_fraction:.3f}%), "
            f"range={fit.tail_decades:.3f} decades"
        )


if __name__ == "__main__":
    main()

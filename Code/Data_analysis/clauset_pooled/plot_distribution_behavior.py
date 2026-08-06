#!/usr/bin/env python3
"""Plot nonparametric avalanche-distribution behavior diagnostics."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster import hierarchy


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_dir", type=Path)
    args = parser.parse_args()
    summary = _read(args.results_dir / "avalanche_behavior_summary.csv")
    lorenz = _read(args.results_dir / "avalanche_lorenz.csv")
    pmf = _read(args.results_dir / "full_distribution_pmf.csv")
    ts_values = [int(row["ts"]) for row in summary]
    rows = {int(row["ts"]): row for row in summary}
    x = np.arange(len(ts_values))

    figure, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    for field, label, marker in (
        ("top_0p1_size_share", "largest 10%", "o"),
        ("top_0p01_size_share", "largest 1%", "s"),
        ("top_0p001_size_share", "largest 0.1%", "^"),
        ("top_0p0001_size_share", "largest 0.01%", "D"),
    ):
        axes[0, 0].plot(
            x, [float(rows[ts][field]) for ts in ts_values], marker=marker, label=label
        )
    axes[0, 0].set(title="Concentration of cumulative size", ylabel="Fraction of summed $s$")
    axes[0, 0].legend()

    axes[0, 1].plot(
        x,
        [float(rows[ts]["characteristic_size_s2_over_s1"]) for ts in ts_values],
        marker="o",
        label="$\\langle s^2\\rangle/\\langle s\\rangle$",
    )
    axes[0, 1].plot(
        x,
        [float(rows[ts]["large_median"]) for ts in ts_values],
        marker="s",
        label="upper-scale median",
    )
    axes[0, 1].set(title="Nonparametric characteristic scales", ylabel="Size")
    axes[0, 1].legend()

    axes[1, 0].plot(
        x,
        [float(rows[ts]["large_fraction"]) for ts in ts_values],
        marker="o",
        color="#d62728",
        label="upper-scale event fraction",
    )
    second_axis = axes[1, 0].twinx()
    second_axis.plot(
        x,
        [int(rows[ts]["large_minimum"]) for ts in ts_values],
        marker="s",
        color="#1f77b4",
        label="empirical threshold",
    )
    axes[1, 0].set(title="Empirical two-scale partition", ylabel="Fraction of events")
    second_axis.set_ylabel("First upper-scale size")
    handles, labels = axes[1, 0].get_legend_handles_labels()
    handles2, labels2 = second_axis.get_legend_handles_labels()
    axes[1, 0].legend(handles + handles2, labels + labels2, loc="center right")

    colors = plt.cm.viridis(np.linspace(0.03, 0.97, len(ts_values)))
    for ts, color in zip(ts_values, colors, strict=True):
        selected = [row for row in lorenz if int(row["ts"]) == ts]
        axes[1, 1].plot(
            [float(row["event_fraction"]) for row in selected],
            [float(row["cumulative_size_fraction"]) for row in selected],
            color=color,
            linewidth=1.2,
            label=str(ts),
        )
    axes[1, 1].plot([0, 1], [0, 1], color="gray", linestyle="--", linewidth=0.8)
    axes[1, 1].set(
        title="Lorenz curves of avalanche sizes",
        xlabel="Cumulative fraction of events",
        ylabel="Cumulative fraction of summed $s$",
    )
    axes[1, 1].legend(title="$T_s$", ncol=2, fontsize=7)

    for axis in axes.flat:
        axis.grid(alpha=0.25)
        if axis is not axes[1, 1]:
            axis.set(xlabel="$T_s$", xticks=x, xticklabels=ts_values)
            axis.tick_params(axis="x", rotation=45)
    for suffix in ("png", "pdf"):
        figure.savefig(args.results_dir / f"avalanche_behavior_metrics.{suffix}", dpi=220)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(9, 6), constrained_layout=True)
    for ts, color in zip(ts_values, colors, strict=True):
        selected = [row for row in pmf if int(row["ts"]) == ts]
        sizes = np.array([int(row["size"]) for row in selected])
        counts = np.array([int(row["count"]) for row in selected])
        keep = sizes >= int(rows[ts]["large_minimum"])
        sizes = sizes[keep]
        counts = counts[keep]
        survival = np.cumsum(counts[::-1], dtype=float)[::-1] / counts.sum()
        normalized = sizes / float(rows[ts]["large_median"])
        axis.loglog(normalized, survival, color=color, linewidth=1.2, label=str(ts))
    axis.set(
        title="Upper-scale shape after median normalization",
        xlabel="$s/$ upper-scale median",
        ylabel="Conditional survival probability",
    )
    axis.grid(alpha=0.25, which="both")
    axis.legend(title="$T_s$", ncol=2)
    for suffix in ("png", "pdf"):
        figure.savefig(args.results_dir / f"avalanche_large_scale_collapse.{suffix}", dpi=220)
    plt.close(figure)

    linkage = np.loadtxt(
        args.results_dir / "avalanche_regime_linkage.csv", delimiter=",", skiprows=1
    )
    figure, axis = plt.subplots(figsize=(10, 5), constrained_layout=True)
    hierarchy.dendrogram(linkage, labels=[str(ts) for ts in ts_values], ax=axis)
    axis.set(
        title="Clustering of distributions by Jensen–Shannon distance",
        xlabel="$T_s$",
        ylabel="Average distance between clusters",
    )
    axis.grid(alpha=0.2, axis="y")
    for suffix in ("png", "pdf"):
        figure.savefig(args.results_dir / f"avalanche_regime_dendrogram.{suffix}", dpi=220)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(10, 6), constrained_layout=True)
    histogram_by_ts = {}
    for ts in ts_values:
        selected = [row for row in pmf if int(row["ts"]) == ts and int(row["size"]) >= 2]
        maximum = max(int(row["size"]) for row in selected)
        histogram = np.zeros(maximum + 1, dtype=np.int64)
        for row in selected:
            histogram[int(row["size"])] = int(row["count"])
        histogram_by_ts[ts] = histogram
    for first, second, color in zip(ts_values, ts_values[1:], colors[:-1]):
        maximum = max(histogram_by_ts[first].size, histogram_by_ts[second].size)
        first_hist = np.pad(histogram_by_ts[first], (0, maximum - histogram_by_ts[first].size))
        second_hist = np.pad(histogram_by_ts[second], (0, maximum - histogram_by_ts[second].size))
        first_survival = np.cumsum(first_hist[::-1], dtype=float)[::-1] / first_hist.sum()
        second_survival = np.cumsum(second_hist[::-1], dtype=float)[::-1] / second_hist.sum()
        sizes = np.arange(2, maximum)
        axis.semilogx(
            sizes,
            second_survival[2:] - first_survival[2:],
            color=color,
            linewidth=1.0,
            label=f"{first}→{second}",
        )
    axis.axhline(0.0, color="black", linewidth=0.8)
    axis.set(
        title="CCDF change between consecutive conditions",
        xlabel="Size $s$",
        ylabel="$P_{next}(S\\geq s)-P_{previous}(S\\geq s)$",
    )
    axis.grid(alpha=0.25, which="both")
    axis.legend(ncol=2, fontsize=8)
    for suffix in ("png", "pdf"):
        figure.savefig(args.results_dir / f"avalanche_ccdf_crossings.{suffix}", dpi=220)
    plt.close(figure)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

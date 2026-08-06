#!/usr/bin/env python3
"""Plot non-singleton local-avalanche CCDFs and log-binned densities."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from local_avalanche_ccdf import empirical_ccdf


def read_frequency_table(path: Path) -> dict[str, dict[int, Counter[int]]]:
    counts: dict[str, dict[int, Counter[int]]] = {
        "all": defaultdict(Counter),
        "preterminal": defaultdict(Counter),
    }
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            size = int(row["local_size"])
            if size > 1:
                counts[row["population"]][int(row["ts"])][size] = int(row["frequency"])
    return counts


def shared_log_edges(counts: dict[str, dict[int, Counter[int]]], bins: int = 24) -> np.ndarray:
    maximum = max(max(counter) for population in counts.values() for counter in population.values())
    edges = np.unique(np.floor(np.geomspace(2, maximum + 1, bins + 1)).astype(int))
    if edges[-1] <= maximum:
        edges = np.append(edges, maximum + 1)
    return edges


def binned_density(size_counts: Counter[int], edges: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return geometric bin centers, probability density, and integer counts."""
    sizes = np.fromiter(size_counts.keys(), dtype=np.int64)
    frequencies = np.fromiter(size_counts.values(), dtype=np.int64)
    bin_counts, _ = np.histogram(sizes, bins=edges, weights=frequencies)
    widths = np.diff(edges)
    density = bin_counts / (bin_counts.sum() * widths)
    centers = np.sqrt(edges[:-1] * edges[1:])
    return centers, density, bin_counts.astype(np.int64)


def plot_ccdf(population: str, counts: dict[int, Counter[int]], output_dir: Path) -> None:
    fig, axis = plt.subplots(figsize=(7.2, 5.4), constrained_layout=True)
    ts_values = sorted(counts)
    colors = plt.colormaps["viridis"](np.linspace(0.05, 0.95, len(ts_values)))
    for ts, color in zip(ts_values, colors):
        sizes, survival = empirical_ccdf(counts[ts])
        axis.step(sizes, survival, where="post", linewidth=1.35, color=color, label=str(ts))
    scope = "including terminal step" if population == "all" else "preterminal only"
    axis.set(xscale="log", yscale="log")
    axis.set_xlabel(r"Local avalanche size, $s$ ($s\geq2$)")
    axis.set_ylabel(r"Conditional empirical CCDF, $P(S\geq s\mid S\geq2)$")
    axis.set_title(f"Non-singleton local events — {scope}")
    axis.grid(which="both", alpha=0.2)
    axis.legend(title=r"$T_s$", ncol=2, frameon=False)
    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"local_event_ccdf_non_singleton_{population}.{suffix}", dpi=300)
    plt.close(fig)


def plot_binned(
    population: str,
    counts: dict[int, Counter[int]],
    edges: np.ndarray,
    output_dir: Path,
    writer: csv.writer,
) -> None:
    fig, axis = plt.subplots(figsize=(7.2, 5.4), constrained_layout=True)
    ts_values = sorted(counts)
    colors = plt.colormaps["viridis"](np.linspace(0.05, 0.95, len(ts_values)))
    for ts, color in zip(ts_values, colors):
        centers, density, bin_counts = binned_density(counts[ts], edges)
        present = bin_counts > 0
        axis.plot(centers[present], density[present], marker="o", markersize=3, linewidth=1.1,
                  color=color, label=str(ts))
        for lower, upper, center, value, count in zip(
            edges[:-1], edges[1:], centers, density, bin_counts
        ):
            writer.writerow((population, ts, lower, upper, center, count, value))
    scope = "including terminal step" if population == "all" else "preterminal only"
    axis.set(xscale="log", yscale="log")
    axis.set_xlabel(r"Local avalanche size, $s$ ($s\geq2$)")
    axis.set_ylabel("Probability density")
    axis.set_title(f"Log-binned non-singleton local events — {scope}")
    axis.grid(which="both", alpha=0.2)
    axis.legend(title=r"$T_s$", ncol=2, frameon=False)
    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"local_event_binned_non_singleton_{population}.{suffix}", dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frequency_csv", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--bins", type=int, default=24)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    counts = read_frequency_table(args.frequency_csv)
    edges = shared_log_edges(counts, args.bins)
    for population in ("all", "preterminal"):
        plot_ccdf(population, counts[population], args.output_dir)

    with (args.output_dir / "local_event_binned_non_singleton.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(("population", "ts", "lower", "upper", "center", "count", "density"))
        for population in ("all", "preterminal"):
            plot_binned(population, counts[population], edges, args.output_dir, writer)


if __name__ == "__main__":
    main()

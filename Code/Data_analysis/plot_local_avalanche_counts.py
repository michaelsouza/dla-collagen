#!/usr/bin/env python3
"""Plot descriptive summaries of local connected avalanche counts."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def read_numeric_csv(path: Path) -> list[dict[str, float]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: float(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def percent(numerator: float, denominator: float) -> float:
    return 100.0 * numerator / denominator if denominator else float("nan")


def plot_aggregate(rows: list[dict[str, float]], output_dir: Path) -> None:
    rows = sorted(rows, key=lambda row: row["ts"])
    ts = np.array([row["ts"] for row in rows])
    events = np.array([row["local_events"] for row in rows])
    singleton_fraction = np.array(
        [percent(row["singleton_events"], row["local_events"]) for row in rows]
    )
    terminal_event_fraction = np.array(
        [percent(row["terminal_events"], row["local_events"]) for row in rows]
    )
    terminal_rod_fraction = np.array(
        [percent(row["terminal_rods"], row["rods_in_local_events"]) for row in rows]
    )

    fig, axes = plt.subplots(2, 2, figsize=(10, 7.5), constrained_layout=True)
    panels = (
        (events / 1e6, "Local events (millions)", "A"),
        (singleton_fraction, "Singleton events (%)", "B"),
        (terminal_event_fraction, "Terminal local events (%)", "C"),
        (terminal_rod_fraction, "Rods removed at terminal step (%)", "D"),
    )
    for axis, (values, ylabel, label) in zip(axes.flat, panels):
        axis.plot(ts, values, marker="o", linewidth=1.6, color="#255f85")
        axis.set_xscale("log", base=2)
        axis.set_xticks(ts)
        axis.set_xticklabels([str(int(value)) for value in ts], rotation=45)
        axis.set_xlabel(r"Surface relaxation, $T_s$")
        axis.set_ylabel(ylabel)
        axis.grid(alpha=0.25)
        axis.text(-0.14, 1.04, label, transform=axis.transAxes, fontweight="bold")

    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"local_event_descriptive_summary.{suffix}", dpi=300)
    plt.close(fig)


def plot_fibril_variability(rows: list[dict[str, float]], output_dir: Path) -> None:
    grouped: dict[int, list[dict[str, float]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["ts"])].append(row)
    ts_values = sorted(grouped)

    metrics = (
        (
            [[row["local_events"] / row["runs"] for row in grouped[ts]] for ts in ts_values],
            "Local events per rupture realization",
            "A",
        ),
        (
            [
                [percent(row["singleton_events"], row["local_events"]) for row in grouped[ts]]
                for ts in ts_values
            ],
            "Singleton events per fibril (%)",
            "B",
        ),
        (
            [
                [percent(row["terminal_rods"], row["rods_in_local_events"]) for row in grouped[ts]]
                for ts in ts_values
            ],
            "Rods removed at terminal step per fibril (%)",
            "C",
        ),
    )

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3), constrained_layout=True)
    positions = np.arange(1, len(ts_values) + 1)
    for axis, (values, ylabel, label) in zip(axes, metrics):
        plot = axis.boxplot(
            values,
            positions=positions,
            widths=0.65,
            patch_artist=True,
            showfliers=False,
            medianprops={"color": "#8c2d04", "linewidth": 1.5},
        )
        for box in plot["boxes"]:
            box.set_facecolor("#9ecae1")
            box.set_edgecolor("#255f85")
        axis.set_xticks(positions)
        axis.set_xticklabels([str(ts) for ts in ts_values], rotation=45)
        axis.set_xlabel(r"Surface relaxation, $T_s$")
        axis.set_ylabel(ylabel)
        axis.grid(axis="y", alpha=0.25)
        axis.text(-0.14, 1.04, label, transform=axis.transAxes, fontweight="bold")

    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"local_event_fibril_variability.{suffix}", dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("counts_dir", type=Path)
    args = parser.parse_args()

    aggregate = read_numeric_csv(args.counts_dir / "local_event_counts_by_ts.csv")
    fibrils = read_numeric_csv(args.counts_dir / "local_event_counts_by_fibril.csv")
    plot_aggregate(aggregate, args.counts_dir)
    plot_fibril_variability(fibrils, args.counts_dir)


if __name__ == "__main__":
    main()

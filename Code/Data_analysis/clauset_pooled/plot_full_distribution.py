#!/usr/bin/env python3
"""Plot complete empirical local-avalanche distributions across Ts."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_dir", type=Path)
    args = parser.parse_args()

    summaries = _read(args.results_dir / "full_distribution_summary.csv")
    pmf_rows = _read(args.results_dir / "full_distribution_pmf.csv")
    distances = _read(args.results_dir / "full_distribution_pairwise_distances.csv")
    ts_values = sorted({int(row["ts"]) for row in summaries})
    colors = plt.cm.viridis(np.linspace(0.03, 0.97, len(ts_values)))

    figure, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    for ts, color in zip(ts_values, colors):
        selected = [row for row in pmf_rows if int(row["ts"]) == ts]
        sizes = np.array([int(row["size"]) for row in selected])
        ccdf = np.array([float(row["ccdf"]) for row in selected])
        axes[0, 0].loglog(sizes, ccdf, color=color, linewidth=1.2, label=str(ts))

        nontrivial = sizes >= 2
        conditional_ccdf = ccdf[nontrivial] / ccdf[nontrivial][0]
        axes[0, 1].loglog(
            sizes[nontrivial], conditional_ccdf, color=color, linewidth=1.2
        )

    axes[0, 0].set(title="Distribuição completa", xlabel="Tamanho s", ylabel="P(S ≥ s)")
    axes[0, 0].legend(title="$T_s$", ncol=2, fontsize=8)
    axes[0, 1].set(
        title="Eventos não triviais (condicional a s ≥ 2)",
        xlabel="Tamanho s",
        ylabel="P(S ≥ s | S ≥ 2)",
    )

    all_rows = {
        int(row["ts"]): row for row in summaries if row["population"] == "all"
    }
    nontrivial_rows = {
        int(row["ts"]): row
        for row in summaries
        if row["population"] == "nontrivial"
    }
    x = np.arange(len(ts_values))
    for field, label, marker in (
        ("q90", "q90", "o"),
        ("q99", "q99", "s"),
        ("q999", "q99.9", "^"),
        ("mean", "média", "D"),
    ):
        axes[1, 0].plot(
            x,
            [float(nontrivial_rows[ts][field]) for ts in ts_values],
            marker=marker,
            linewidth=1.2,
            label=label,
        )
    axes[1, 0].set_yscale("log")
    axes[1, 0].set(
        title="Escalas dos eventos não triviais",
        xlabel="$T_s$",
        ylabel="Tamanho de avalanche",
        xticks=x,
        xticklabels=ts_values,
    )
    axes[1, 0].tick_params(axis="x", rotation=45)
    axes[1, 0].legend()

    axes[1, 1].plot(
        x,
        [float(all_rows[ts]["singleton_fraction"]) for ts in ts_values],
        marker="o",
        label="P(S=1)",
    )
    for threshold, marker in ((10, "s"), (100, "^"), (1000, "D")):
        axes[1, 1].plot(
            x,
            [
                float(all_rows[ts][f"probability_s_ge_{threshold}"])
                for ts in ts_values
            ],
            marker=marker,
            label=f"P(S≥{threshold})",
        )
    axes[1, 1].set_yscale("log")
    axes[1, 1].set(
        title="Composição da população completa",
        xlabel="$T_s$",
        ylabel="Fração dos eventos",
        xticks=x,
        xticklabels=ts_values,
    )
    axes[1, 1].tick_params(axis="x", rotation=45)
    axes[1, 1].legend()

    for axis in axes.flat:
        axis.grid(alpha=0.25, which="both")
    for suffix in ("png", "pdf"):
        figure.savefig(
            args.results_dir / f"full_distribution_overview.{suffix}", dpi=220
        )
    plt.close(figure)

    matrix = np.zeros((len(ts_values), len(ts_values)), dtype=float)
    index_by_ts = {ts: index for index, ts in enumerate(ts_values)}
    for row in distances:
        if row["population"] != "nontrivial":
            continue
        i = index_by_ts[int(row["ts_first"])]
        j = index_by_ts[int(row["ts_second"])]
        matrix[i, j] = matrix[j, i] = float(row["jensen_shannon"])
    figure, axis = plt.subplots(figsize=(8, 7), constrained_layout=True)
    image = axis.imshow(matrix, cmap="magma", vmin=0.0)
    axis.set(
        title="Distância de Jensen–Shannon: P(S | S≥2)",
        xlabel="$T_s$",
        ylabel="$T_s$",
        xticks=np.arange(len(ts_values)),
        yticks=np.arange(len(ts_values)),
        xticklabels=ts_values,
        yticklabels=ts_values,
    )
    axis.tick_params(axis="x", rotation=45)
    figure.colorbar(image, ax=axis, label="Distância (base 2)")
    for suffix in ("png", "pdf"):
        figure.savefig(
            args.results_dir / f"full_distribution_js_heatmap.{suffix}", dpi=220
        )
    plt.close(figure)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


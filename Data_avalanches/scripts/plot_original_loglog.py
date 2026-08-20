#!/usr/bin/env python3
"""Generate log-log figures directly from the supplied avalanche PMFs.

The plotted points are the original, unbinned probabilities. No interpolation,
regression, smoothing, or parametric fit is applied.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

from avalanche_data import AvalancheDistribution, discover_distributions


WITH_TERMINAL_COLOR = "#d95f02"
WITHOUT_TERMINAL_COLOR = "#1b78a6"


def ts_colors(ts_values: list[int]) -> dict[int, tuple[float, float, float, float]]:
    normalization = LogNorm(vmin=min(ts_values), vmax=max(ts_values))
    colormap = plt.get_cmap("viridis")
    return {ts: colormap(normalization(ts)) for ts in ts_values}


def style_axis(axis: plt.Axes) -> None:
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlabel(r"Local avalanche size, $s$")
    axis.set_ylabel(r"Empirical probability, $P(s)$")
    axis.grid(which="major", color="#b8b8b8", linewidth=0.55, alpha=0.45)
    axis.grid(which="minor", color="#d8d8d8", linewidth=0.35, alpha=0.25)


def plot_population(
    distributions: list[AvalancheDistribution],
    *,
    includes_terminal: bool,
) -> plt.Figure:
    selected = sorted(
        (item for item in distributions if item.includes_terminal == includes_terminal),
        key=lambda item: item.ts,
    )
    colors = ts_colors([item.ts for item in selected])
    figure, axis = plt.subplots(figsize=(8.2, 5.8), constrained_layout=True)
    for item in selected:
        axis.scatter(
            item.sizes,
            item.probabilities,
            s=7.5,
            marker="o",
            linewidths=0.0,
            alpha=0.82,
            color=colors[item.ts],
            label=rf"$T_s={item.ts}$",
            rasterized=True,
        )
    style_axis(axis)
    population = "including terminal rupture" if includes_terminal else "preterminal only"
    axis.set_title(f"Original local-avalanche PMFs — {population}")
    axis.legend(
        frameon=False,
        fontsize=8,
        ncol=2,
        columnspacing=1.1,
        handletextpad=0.35,
        markerscale=1.5,
    )
    return figure


def plot_terminal_comparison(
    distributions: list[AvalancheDistribution],
) -> plt.Figure:
    by_condition = {(item.ts, item.includes_terminal): item for item in distributions}
    ts_values = sorted({item.ts for item in distributions})
    figure, axes = plt.subplots(
        5, 2, figsize=(10.8, 16.5), sharex=False, sharey=False, constrained_layout=True
    )
    for axis, ts in zip(axes.flat, ts_values, strict=True):
        with_terminal = by_condition[(ts, True)]
        without_terminal = by_condition[(ts, False)]
        axis.scatter(
            with_terminal.sizes,
            with_terminal.probabilities,
            s=8,
            color=WITH_TERMINAL_COLOR,
            alpha=0.62,
            linewidths=0.0,
            label="With terminal rupture",
            rasterized=True,
        )
        axis.scatter(
            without_terminal.sizes,
            without_terminal.probabilities,
            s=10,
            facecolors="none",
            edgecolors=WITHOUT_TERMINAL_COLOR,
            linewidths=0.55,
            alpha=0.85,
            label="Preterminal only",
            rasterized=True,
        )
        style_axis(axis)
        axis.set_title(rf"$T_s={ts}$")
    axes.flat[0].legend(frameon=False, fontsize=8, loc="lower left")
    figure.suptitle(
        "Original local-avalanche PMFs: sensitivity to the terminal rupture",
        fontsize=14,
    )
    return figure


def save_figure(
    figure: plt.Figure, output_base: Path, *, formats: list[str], dpi: int
) -> None:
    output_base.parent.mkdir(parents=True, exist_ok=True)
    for extension in formats:
        path = output_base.with_suffix(f".{extension}")
        figure.savefig(
            path,
            dpi=dpi,
            metadata={
                "Title": output_base.name,
                "Subject": "Unbinned empirical local-avalanche PMFs",
            },
        )
        print(f"Wrote {path}")
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", type=Path, default=Path(__file__).resolve().parent.parent
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument(
        "--formats", nargs="+", choices=("png", "pdf", "svg"), default=("png", "pdf")
    )
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()
    output_dir = args.output_dir or args.data_dir / "figures"

    distributions = discover_distributions(args.data_dir)
    save_figure(
        plot_population(distributions, includes_terminal=True),
        output_dir / "original_pmf_com_terminal_loglog",
        formats=list(args.formats),
        dpi=args.dpi,
    )
    save_figure(
        plot_population(distributions, includes_terminal=False),
        output_dir / "original_pmf_sem_terminal_loglog",
        formats=list(args.formats),
        dpi=args.dpi,
    )
    save_figure(
        plot_terminal_comparison(distributions),
        output_dir / "original_pmf_terminal_comparison_loglog",
        formats=list(args.formats),
        dpi=args.dpi,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

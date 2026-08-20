#!/usr/bin/env python3
"""Generate logarithmically binned local-avalanche PMF figures.

Bin probabilities are divided by their integer widths. This width correction
makes the plotted quantity comparable to the original PMF and avoids shifting
a power-law slope by one, as would happen when plotting raw bin masses.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

from avalanche_data import AvalancheDistribution, discover_distributions


WITH_TERMINAL_COLOR = "#d95f02"
WITHOUT_TERMINAL_COLOR = "#1b78a6"


def integer_log_edges(minimum: int, maximum: int, requested_bins: int) -> np.ndarray:
    """Return unique integer edges approximating equal log-width bins."""
    if minimum < 1 or maximum < minimum or requested_bins < 2:
        raise ValueError("invalid logarithmic-bin specification")
    raw = np.geomspace(float(minimum), float(maximum + 1), requested_bins + 1)
    edges = np.unique(np.rint(raw).astype(np.int64))
    edges = edges[(edges >= minimum) & (edges <= maximum + 1)]
    if edges.size == 0 or edges[0] != minimum:
        edges = np.insert(edges, 0, minimum)
    if edges[-1] != maximum + 1:
        edges = np.append(edges, maximum + 1)
    if edges.size < 3:
        raise ValueError("too few represented logarithmic bins")
    return edges


def logarithmic_pmf(
    distribution: AvalancheDistribution,
    edges: np.ndarray,
    *,
    minimum_size: int,
) -> list[dict[str, object]]:
    """Group exact counts and return width-corrected PMF estimates."""
    counts = distribution.infer_counts()
    sizes = np.arange(minimum_size, counts.size, dtype=np.int64)
    frequencies = counts[minimum_size:].astype(float)
    binned_counts, _ = np.histogram(sizes, bins=edges, weights=frequencies)
    widths = np.diff(edges).astype(float)
    left = edges[:-1]
    right = edges[1:]
    centers = np.sqrt(left.astype(float) * (right - 1).astype(float))
    centers = np.where(right - left == 1, left.astype(float), centers)
    total_events = float(counts.sum())
    bin_probability = binned_counts / total_events
    probability_density = bin_probability / widths

    rows: list[dict[str, object]] = []
    for left_edge, right_edge, center, width, count, mass, density in zip(
        left,
        right,
        centers,
        widths,
        binned_counts,
        bin_probability,
        probability_density,
        strict=True,
    ):
        if count <= 0:
            continue
        rows.append(
            {
                "ts": distribution.ts,
                "terminal_population": distribution.terminal_label,
                "minimum_size": minimum_size,
                "bin_left_inclusive": int(left_edge),
                "bin_right_exclusive": int(right_edge),
                "bin_center": float(center),
                "bin_width": int(width),
                "count": int(round(count)),
                "bin_probability": float(mass),
                "probability_density": float(density),
                "poisson_standard_error_density": float(np.sqrt(count) / total_events / width),
                "total_events": int(total_events),
            }
        )
    return rows


def _colors(ts_values: list[int]) -> dict[int, tuple[float, float, float, float]]:
    normalization = LogNorm(vmin=min(ts_values), vmax=max(ts_values))
    colormap = plt.get_cmap("viridis")
    return {ts: colormap(normalization(ts)) for ts in ts_values}


def _style(axis: plt.Axes) -> None:
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlabel(r"Local avalanche size, $s$")
    axis.set_ylabel(r"Log-binned PMF, $P_{\rm bin}(s)/\Delta s$")
    axis.grid(which="major", color="#b8b8b8", linewidth=0.55, alpha=0.45)
    axis.grid(which="minor", color="#d8d8d8", linewidth=0.35, alpha=0.25)


def plot_population(
    rows: list[dict[str, object]], *, includes_terminal: bool
) -> plt.Figure:
    label = "com_terminal" if includes_terminal else "sem_terminal"
    selected = [row for row in rows if row["terminal_population"] == label]
    ts_values = sorted({int(row["ts"]) for row in selected})
    colors = _colors(ts_values)
    figure, axis = plt.subplots(figsize=(8.2, 5.8), constrained_layout=True)
    for ts in ts_values:
        condition = [row for row in selected if int(row["ts"]) == ts]
        axis.plot(
            [float(row["bin_center"]) for row in condition],
            [float(row["probability_density"]) for row in condition],
            marker="o",
            markersize=3.8,
            linewidth=0.9,
            color=colors[ts],
            label=rf"$T_s={ts}$",
        )
    _style(axis)
    population = "including terminal rupture" if includes_terminal else "preterminal only"
    axis.set_title(f"Logarithmically binned local-avalanche PMFs — {population}")
    axis.legend(frameon=False, fontsize=8, ncol=2, columnspacing=1.1)
    return figure


def plot_terminal_comparison(rows: list[dict[str, object]]) -> plt.Figure:
    ts_values = sorted({int(row["ts"]) for row in rows})
    figure, axes = plt.subplots(5, 2, figsize=(10.8, 16.5), constrained_layout=True)
    for axis, ts in zip(axes.flat, ts_values, strict=True):
        for terminal_label, color, marker, display in (
            ("com_terminal", WITH_TERMINAL_COLOR, "o", "With terminal rupture"),
            ("sem_terminal", WITHOUT_TERMINAL_COLOR, "s", "Preterminal only"),
        ):
            condition = [
                row
                for row in rows
                if int(row["ts"]) == ts
                and row["terminal_population"] == terminal_label
            ]
            axis.plot(
                [float(row["bin_center"]) for row in condition],
                [float(row["probability_density"]) for row in condition],
                marker=marker,
                markersize=3.5,
                linewidth=0.9,
                color=color,
                markerfacecolor="none" if terminal_label == "sem_terminal" else color,
                label=display,
            )
        _style(axis)
        axis.set_title(rf"$T_s={ts}$")
    axes.flat[0].legend(frameon=False, fontsize=8)
    figure.suptitle(
        "Log-binned local-avalanche PMFs: terminal-rupture sensitivity",
        fontsize=14,
    )
    return figure


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save_figure(
    figure: plt.Figure, output_base: Path, *, formats: list[str], dpi: int
) -> None:
    output_base.parent.mkdir(parents=True, exist_ok=True)
    for extension in formats:
        path = output_base.with_suffix(f".{extension}")
        figure.savefig(path, dpi=dpi)
        print(f"Wrote {path}")
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", type=Path, default=Path(__file__).resolve().parent.parent
    )
    parser.add_argument("--results-dir", type=Path)
    parser.add_argument("--figures-dir", type=Path)
    parser.add_argument("--minimum-size", type=int, default=2)
    parser.add_argument("--bins", type=int, default=50)
    parser.add_argument(
        "--formats", nargs="+", choices=("png", "pdf", "svg"), default=("png", "pdf")
    )
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()
    if args.minimum_size < 1:
        parser.error("--minimum-size must be positive")
    if args.bins < 2:
        parser.error("--bins must be at least two")

    results_dir = args.results_dir or args.data_dir / "results"
    figures_dir = args.figures_dir or args.data_dir / "figures"
    distributions = discover_distributions(args.data_dir)
    global_maximum = max(int(item.sizes[-1]) for item in distributions)
    edges = integer_log_edges(args.minimum_size, global_maximum, args.bins)
    rows = [
        row
        for distribution in distributions
        for row in logarithmic_pmf(
            distribution, edges, minimum_size=args.minimum_size
        )
    ]
    table_path = results_dir / "log_binned_pmf.csv"
    write_csv(table_path, rows)
    print(
        f"Wrote {table_path} ({len(edges) - 1} represented integer bins "
        f"from {args.bins} requested bins)"
    )

    save_figure(
        plot_population(rows, includes_terminal=True),
        figures_dir / "log_binned_pmf_com_terminal",
        formats=list(args.formats),
        dpi=args.dpi,
    )
    save_figure(
        plot_population(rows, includes_terminal=False),
        figures_dir / "log_binned_pmf_sem_terminal",
        formats=list(args.formats),
        dpi=args.dpi,
    )
    save_figure(
        plot_terminal_comparison(rows),
        figures_dir / "log_binned_pmf_terminal_comparison",
        formats=list(args.formats),
        dpi=args.dpi,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

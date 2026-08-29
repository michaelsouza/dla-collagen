#!/usr/bin/env python3
"""Compare binned avalanche PDFs with and without the terminal rupture row."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from Code.Data_analysis.run_avalanche_statistics import load_or_build_cache


TS_VALUES = (2, 8, 32)
BIN_COUNT = 100
FIT_LOG10_MIN = 1.08
FIT_LOG10_MAX = 2.75


def logarithmic_pdf(counts: np.ndarray) -> list[dict[str, float]]:
    """Return a density histogram using equal-width bins in log10(size)."""

    sizes = np.arange(counts.size, dtype=np.int64)
    selected = (sizes >= 2) & (counts > 0)
    sizes = sizes[selected]
    frequencies = counts[selected].astype(float)
    maximum = int(sizes[-1])
    log_edges = np.linspace(0.0, np.log10(maximum + 1.0), BIN_COUNT + 1)
    edges = 10.0**log_edges
    binned_counts, _ = np.histogram(sizes, bins=edges, weights=frequencies)
    widths = np.diff(edges)
    centers = np.sqrt(edges[:-1] * edges[1:])
    total = float(frequencies.sum())
    density = binned_counts / (total * widths)
    rows = []
    for left, right, center, count, probability_density in zip(
        edges[:-1],
        edges[1:],
        centers,
        binned_counts,
        density,
        strict=True,
    ):
        if count <= 0:
            continue
        rows.append(
            {
                "bin_left": float(left),
                "bin_right": float(right),
                "size": float(center),
                "count": float(count),
                "bin_probability": float(count / total),
                "probability_density": float(probability_density),
                "log10_bin_probability": float(np.log10(count / total)),
                "log10_size": float(np.log10(center)),
                "log10_probability_density": float(np.log10(probability_density)),
            }
        )
    return rows


def fit_binned_regime(
    rows: list[dict[str, float]], *, y_key: str
) -> dict[str, float]:
    selected = [
        row
        for row in rows
        if FIT_LOG10_MIN <= row["log10_size"] <= FIT_LOG10_MAX
    ]
    x = np.asarray([row["log10_size"] for row in selected])
    y = np.asarray([row[y_key] for row in selected])
    fit = stats.linregress(x, y)
    return {
        "bins_in_fit": len(selected),
        "slope": float(fit.slope),
        "gamma": float(-fit.slope),
        "intercept": float(fit.intercept),
        "slope_standard_error": float(fit.stderr),
        "r_squared": float(fit.rvalue**2),
        "fit_log10_min": FIT_LOG10_MIN,
        "fit_log10_max": FIT_LOG10_MAX,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    temporary = path.with_name(f".{path.name}.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    data_root = repo / "Data_fibrils" / "Avalanche_force_grouped" / "runs"
    cache_root = repo / "Data_fibrils" / "Avalanche_force_grouped" / "analysis_cache"
    output = repo / "Reviews" / "Issue5_avalanche_statistics"
    output.mkdir(parents=True, exist_ok=True)

    all_bins: list[dict] = []
    all_fits: list[dict] = []
    figure, axes = plt.subplots(3, 1, figsize=(6.4, 9.0), sharex=True)
    colors = {"excluded": "#1f77b4", "included": "#d62728"}
    markers = {"excluded": "o", "included": "s"}

    for axis, ts in zip(axes, TS_VALUES, strict=True):
        condition = load_or_build_cache(data_root, cache_root, ts)
        for include_terminal in (False, True):
            label = "included" if include_terminal else "excluded"
            counts = condition.fibril_counts(
                include_terminal=include_terminal
            ).sum(axis=0)
            rows = logarithmic_pdf(counts)
            mass_fit = fit_binned_regime(rows, y_key="log10_bin_probability")
            density_fit = fit_binned_regime(
                rows, y_key="log10_probability_density"
            )
            fit = {
                "bins_in_fit": mass_fit["bins_in_fit"],
                "fit_log10_min": mass_fit["fit_log10_min"],
                "fit_log10_max": mass_fit["fit_log10_max"],
                "gamma_bin_probability": mass_fit["gamma"],
                "slope_bin_probability": mass_fit["slope"],
                "intercept_bin_probability": mass_fit["intercept"],
                "slope_standard_error_bin_probability": mass_fit[
                    "slope_standard_error"
                ],
                "r_squared_bin_probability": mass_fit["r_squared"],
                "gamma_density_corrected": density_fit["gamma"],
                "slope_density_corrected": density_fit["slope"],
                "intercept_density_corrected": density_fit["intercept"],
                "slope_standard_error_density_corrected": density_fit[
                    "slope_standard_error"
                ],
                "r_squared_density_corrected": density_fit["r_squared"],
            }
            all_bins.extend(
                {"ts": ts, "terminal": label, **row} for row in rows
            )
            all_fits.append({"ts": ts, "terminal": label, **fit})

            x = np.asarray([row["size"] for row in rows])
            y = np.asarray([row["bin_probability"] for row in rows])
            axis.plot(
                x,
                y,
                linestyle="none",
                marker=markers[label],
                markersize=3.6,
                markerfacecolor="none",
                markeredgewidth=0.8,
                color=colors[label],
                label=(
                    f"{'with terminal rupture' if include_terminal else 'precursors'}; "
                    f"binned slope={fit['gamma_bin_probability']:.2f}"
                ),
            )
            fit_x = np.geomspace(10**FIT_LOG10_MIN, min(10**FIT_LOG10_MAX, x.max()), 100)
            fit_y = 10 ** (
                fit["intercept_bin_probability"]
                + fit["slope_bin_probability"] * np.log10(fit_x)
            )
            axis.plot(fit_x, fit_y, color=colors[label], linewidth=1.0)

        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.set_ylabel(r"binned probability")
        axis.text(0.03, 0.08, rf"$T_s={ts}$", transform=axis.transAxes)
        axis.legend(frameon=False, fontsize=8)
        axis.tick_params(direction="in", top=True, right=True)

    axes[-1].set_xlabel(r"avalanche-cluster size, $s$")
    figure.tight_layout()
    figure.savefig(output / "binned_terminal_comparison.pdf")
    figure.savefig(output / "binned_terminal_comparison.png", dpi=300)
    plt.close(figure)
    write_csv(output / "binned_distributions.csv", all_bins)
    write_csv(output / "binned_linear_fits.csv", all_fits)

    for row in all_fits:
        print(
            f"Ts={row['ts']}, terminal={row['terminal']}: "
            f"gamma_bin_probability={row['gamma_bin_probability']:.6g} +/- "
            f"{row['slope_standard_error_bin_probability']:.3g}, "
            f"gamma_density_corrected={row['gamma_density_corrected']:.6g}, "
            f"R2={row['r_squared_bin_probability']:.6g}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Plot pooled empirical CCDFs and the fitted discrete tail models."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import special

from .models import _cutoff_log_normalization
from .power_law import histogram_arrays, read_size_histogram


def _load_fits(path: Path) -> dict[int, dict[str, dict[str, float]]]:
    fits: dict[int, dict[str, dict[str, float]]] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            ts = int(row["ts"])
            numeric = {
                key: float(value)
                for key, value in row.items()
                if value not in (None, "") and key not in {"model", "ts"}
            }
            fits.setdefault(ts, {})[row["model"]] = numeric
    return fits


def _empirical_ccdf(histogram: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    sizes, frequencies = histogram_arrays(histogram)
    survival = np.cumsum(frequencies[::-1], dtype=np.int64)[::-1] / frequencies.sum()
    return sizes, survival


def _model_survivals(
    support: np.ndarray, fits: dict[str, dict[str, float]]
) -> dict[str, np.ndarray]:
    power = fits["power_law"]
    xmin = int(power["xmin"])
    alpha = power["alpha"]
    survivals: dict[str, np.ndarray] = {
        "Pure power law": special.zeta(alpha, support.astype(float))
        / special.zeta(alpha, float(xmin))
    }

    cutoff = fits["cutoff_power_law"]
    cutoff_alpha = cutoff["alpha"]
    cutoff_rate = cutoff["lambda"]
    cutoff_log_normalization = _cutoff_log_normalization(
        cutoff_alpha, cutoff_rate, xmin
    )
    full_support = np.arange(xmin, int(support[-1]) + 1, dtype=np.int64)
    cutoff_probabilities = np.exp(
        -cutoff_alpha * np.log(full_support / float(xmin))
        - cutoff_rate * (full_support - xmin)
        - cutoff_log_normalization
    )
    cutoff_cdf_before = np.concatenate(
        ([0.0], np.cumsum(cutoff_probabilities)[:-1])
    )
    survivals["Power law + cutoff"] = 1.0 - cutoff_cdf_before[support - xmin]

    lognormal = fits["lognormal"]
    mu = lognormal["mu"]
    sigma = lognormal["sigma"]
    boundary = (np.log(xmin - 0.5) - mu) / sigma
    thresholds = (np.log(support - 0.5) - mu) / sigma
    survivals["Discrete lognormal"] = np.exp(
        special.log_ndtr(-thresholds) - special.log_ndtr(-boundary)
    )
    return survivals


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("model_fits_csv", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    fits_by_ts = _load_fits(args.model_fits_csv)
    paths = sorted(
        args.input_dir.glob("ts_*.txt"),
        key=lambda path: int(path.stem.removeprefix("ts_")),
    )
    if not paths:
        raise SystemExit("no ts_*.txt inputs found")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    figure, axes = plt.subplots(5, 2, figsize=(12, 18), constrained_layout=True)
    colors = {
        "Pure power law": "#d73027",
        "Power law + cutoff": "#2166ac",
        "Discrete lognormal": "#1a9850",
    }
    styles = {
        "Pure power law": "--",
        "Power law + cutoff": "-",
        "Discrete lognormal": "-.",
    }

    for axis, path in zip(axes.flat, paths, strict=True):
        ts = int(path.stem.removeprefix("ts_"))
        histogram = read_size_histogram(path, minimum_size=2)
        sizes, empirical = _empirical_ccdf(histogram)
        condition_fits = fits_by_ts[ts]
        xmin = int(condition_fits["power_law"]["xmin"])
        n_tail = int(condition_fits["power_law"]["n_tail"])
        tail_fraction = n_tail / int(histogram.sum())
        support = np.arange(xmin, int(sizes[-1]) + 1, dtype=np.int64)
        survivals = _model_survivals(support, condition_fits)

        axis.step(
            sizes,
            empirical,
            where="post",
            color="#333333",
            linewidth=1.2,
            label="Empirical",
        )
        for label, survival in survivals.items():
            positive = survival > 0.0
            axis.plot(
                support[positive],
                tail_fraction * survival[positive],
                color=colors[label],
                linestyle=styles[label],
                linewidth=1.6,
                label=label,
            )
        axis.axvline(xmin, color="#777777", linestyle=":", linewidth=1.0)
        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.set_title(
            rf"$T_s={ts}$, $s_{{min}}={xmin}$, tail={100 * tail_fraction:.3g}%"
        )
        axis.set_xlabel(r"Local avalanche size $s$")
        axis.set_ylabel(r"$P(S\geq s\mid S\geq2)$")
        axis.grid(which="both", alpha=0.2)

    handles, labels = axes.flat[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="outside upper center", ncol=4, frameon=False)
    for suffix in ("png", "pdf"):
        figure.savefig(
            args.output_dir / f"pooled_model_ccdf_comparison.{suffix}", dpi=300
        )
    plt.close(figure)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

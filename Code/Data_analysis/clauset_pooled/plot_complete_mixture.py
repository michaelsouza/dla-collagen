#!/usr/bin/env python3
"""Plot complete empirical distributions and their rejected mixture fits."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import special

from .models import _cutoff_log_normalization


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def _model_survivals(
    sizes: np.ndarray, row: dict[str, str]
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xmin = 2
    alpha = float(row["alpha"])
    rate = float(row["lambda"])
    weight = float(row["weight_small"])
    normalization = _cutoff_log_normalization(alpha, rate, xmin)
    full_support = np.arange(xmin, int(sizes[-1]) + 1)
    cutoff_pmf = np.exp(
        -alpha * np.log(full_support / xmin)
        - rate * (full_support - xmin)
        - normalization
    )
    cutoff_survival = 1.0 - np.concatenate(([0.0], np.cumsum(cutoff_pmf)[:-1]))
    cutoff_survival = cutoff_survival[sizes - xmin]

    mu = float(row["mu_large"])
    sigma = float(row["sigma_large"])
    boundary = (np.log(xmin - 0.5) - mu) / sigma
    lower = (np.log(sizes - 0.5) - mu) / sigma
    large_survival = np.exp(
        special.log_ndtr(-lower) - special.log_ndtr(-boundary)
    )
    mixture = weight * cutoff_survival + (1.0 - weight) * large_survival
    return mixture, weight * cutoff_survival, (1.0 - weight) * large_survival


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_dir", type=Path)
    parser.add_argument("--tag", default="complete_mixture_gof_B100")
    args = parser.parse_args()
    fits = {int(row["ts"]): row for row in _read(args.results_dir / f"{args.tag}.csv")}
    pmf = _read(args.results_dir / "full_distribution_pmf.csv")
    ts_values = sorted(fits)

    figure, axes = plt.subplots(5, 2, figsize=(12, 18), constrained_layout=True)
    for axis, ts in zip(axes.flat, ts_values, strict=True):
        selected = [row for row in pmf if int(row["ts"]) == ts and int(row["size"]) >= 2]
        sizes = np.array([int(row["size"]) for row in selected])
        probabilities = np.array([float(row["probability"]) for row in selected])
        empirical = np.cumsum(probabilities[::-1])[::-1] / probabilities.sum()
        mixture, small, large = _model_survivals(sizes, fits[ts])
        axis.loglog(sizes, empirical, color="black", linewidth=1.4, label="empírica")
        axis.loglog(sizes, mixture, color="#d62728", linewidth=1.3, label="mistura")
        axis.loglog(sizes, small, color="#1f77b4", linestyle="--", linewidth=1.0, label="componente pequeno")
        axis.loglog(sizes, large, color="#2ca02c", linestyle=":", linewidth=1.2, label="componente grande")
        axis.set(
            title=f"$T_s={ts}$; KS={float(fits[ts]['observed_ks']):.3f}; $p<0.030$",
            xlabel="Tamanho s",
            ylabel="P(S≥s | S≥2)",
        )
        axis.grid(alpha=0.25, which="both")
    axes[0, 0].legend(fontsize=8)
    for suffix in ("png", "pdf"):
        figure.savefig(args.results_dir / f"complete_mixture_comparison.{suffix}", dpi=220)
    plt.close(figure)

    x = np.arange(len(ts_values))
    figure, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
    axes[0, 0].plot(x, [float(fits[ts]["alpha"]) for ts in ts_values], marker="o")
    axes[0, 0].set(ylabel="$\\alpha$ do componente pequeno")
    axes[0, 1].plot(x, [1.0 - float(fits[ts]["weight_small"]) for ts in ts_values], marker="o")
    axes[0, 1].set(ylabel="Peso do componente grande")
    axes[1, 0].plot(x, [np.exp(float(fits[ts]["mu_large"])) for ts in ts_values], marker="o")
    axes[1, 0].set(ylabel="Mediana do componente grande")
    axes[1, 1].plot(x, [float(fits[ts]["sigma_large"]) for ts in ts_values], marker="o")
    axes[1, 1].set(ylabel="$\\sigma$ lognormal do componente grande")
    for axis in axes.flat:
        axis.set(xlabel="$T_s$", xticks=x, xticklabels=ts_values)
        axis.tick_params(axis="x", rotation=45)
        axis.grid(alpha=0.25)
    for suffix in ("png", "pdf"):
        figure.savefig(args.results_dir / f"complete_mixture_parameters.{suffix}", dpi=220)
    plt.close(figure)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


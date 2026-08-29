#!/usr/bin/env python3
"""Build representation, ensemble-stability, and finite-size diagnostics."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import special

from clauset_hierarchical.analysis import load_fibril_histograms
from clauset_hierarchical.diagnostics import (
    initial_fibril_sizes,
    leave_one_fibril_out,
    spearman_with_p,
    subset_stability,
    tail_realization_counts,
    weighted_quantile,
)


REPOSITORY = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE = (
    REPOSITORY / "Data_avalanches_all_fibrils" / "derived"
    / "avalanche_analysis_v1.duckdb"
)
DEFAULT_FITS = REPOSITORY / "Reviews" / "Issue5_clauset_hierarchical" / "power_law_fits.csv"
DEFAULT_OUTPUT = REPOSITORY / "Reviews" / "Issue5_clauset_hierarchical" / "diagnostics"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ccdf_figure(datasets, fits, path: Path) -> None:
    figure, axes = plt.subplots(2, 5, figsize=(15, 7), constrained_layout=True)
    for axis, data, fit in zip(axes.flat, datasets, fits, strict=True):
        histogram = data.pooled
        support = np.flatnonzero(histogram)
        reverse = np.cumsum(histogram[::-1], dtype=np.int64)[::-1]
        ccdf = reverse[support] / int(histogram.sum())
        axis.loglog(support, ccdf, ".", ms=2.2, alpha=0.65, label="empirical")
        xmin = int(fit["xmin"])
        alpha = float(fit["alpha"])
        model_support = np.arange(xmin, int(support[-1]) + 1)
        tail_fraction = float(fit["tail_fraction"])
        model_ccdf = special.zeta(alpha, model_support.astype(float)) / special.zeta(alpha, xmin)
        axis.loglog(model_support, tail_fraction * model_ccdf, lw=1.5, label="power law")
        axis.axvline(xmin, color="0.35", ls="--", lw=0.8)
        axis.set_title(f"$T_s={data.ts}$")
        axis.set_xlabel("s")
        axis.set_ylabel("P(S >= s)")
    axes.flat[0].legend(fontsize=8)
    figure.savefig(path, dpi=180)
    plt.close(figure)


def stability_figure(rows: list[dict[str, object]], path: Path) -> None:
    figure, axes = plt.subplots(2, 5, figsize=(15, 7), constrained_layout=True)
    for axis, ts in zip(axes.flat, sorted({int(row["ts"]) for row in rows}), strict=True):
        selected = [row for row in rows if int(row["ts"]) == ts]
        for size in (10, 20, 30, 40, 50):
            values = np.array([float(row["alpha"]) for row in selected if int(row["subset_size"]) == size])
            axis.scatter(np.full(values.size, size), values, s=5, alpha=0.12, color="tab:blue")
            axis.plot(size, np.median(values), "o", ms=4, color="black")
        axis.set_title(f"$T_s={ts}$")
        axis.set_xlabel("fibrils")
        axis.set_ylabel("alpha")
    figure.savefig(path, dpi=180)
    plt.close(figure)


def finite_size_figure(rows: list[dict[str, object]], path: Path) -> None:
    figure, axes = plt.subplots(2, 5, figsize=(15, 7), constrained_layout=True)
    for axis, ts in zip(axes.flat, sorted({int(row["ts"]) for row in rows}), strict=True):
        selected = [row for row in rows if int(row["ts"]) == ts]
        axis.scatter(
            [int(row["initial_backbone_size"]) for row in selected],
            [int(row["preterminal_q999_size"]) for row in selected],
            s=13,
            alpha=0.7,
        )
        axis.set_title(f"$T_s={ts}$")
        axis.set_xlabel("initial backbone N0")
        axis.set_ylabel("per-fibril q99.9(s)")
    figure.savefig(path, dpi=180)
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--fits", type=Path, default=DEFAULT_FITS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--repetitions", type=int, default=100)
    parser.add_argument("--seed", type=int, default=27182)
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        raise SystemExit(f"output directory is not empty: {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)

    fits = sorted(read_csv(args.fits), key=lambda row: int(row["ts"]))
    datasets = []
    condition_rows = []
    fibril_rows = []
    stability_rows = []
    loo_rows = []
    for condition_index, fit in enumerate(fits):
        ts = int(fit["ts"])
        xmin = int(fit["xmin"])
        data = load_fibril_histograms(args.database, ts)
        datasets.append(data)
        initial_sizes = initial_fibril_sizes(args.database, ts)
        total_tail_runs, tail_runs = tail_realization_counts(args.database, ts, xmin)
        tail_by_fibril = data.counts[:, xmin:].sum(axis=1, dtype=np.int64)
        maximums = []
        quantiles = []
        n0_values = []
        for index, seed in enumerate(data.seeds):
            histogram = data.counts[index]
            maximum = int(np.flatnonzero(histogram)[-1])
            quantile = weighted_quantile(histogram, 0.999)
            n0 = initial_sizes[int(seed)]
            maximums.append(maximum)
            quantiles.append(quantile)
            n0_values.append(n0)
            fibril_rows.append(
                {
                    "ts": ts,
                    "seed": int(seed),
                    "initial_backbone_size": n0,
                    "preterminal_maximum_size": maximum,
                    "preterminal_q999_size": quantile,
                    "tail_events": int(tail_by_fibril[index]),
                    "tail_realizations": tail_runs.get(int(seed), 0),
                }
            )
        n0_array = np.asarray(n0_values)
        maximum_array = np.asarray(maximums)
        quantile_array = np.asarray(quantiles)
        max_rho, max_p = spearman_with_p(n0_array, maximum_array)
        quantile_rho, quantile_p = spearman_with_p(n0_array, quantile_array)
        pooled = data.pooled
        singleton_count = int(pooled[1])
        condition_rows.append(
            {
                "ts": ts,
                "fibrils": data.fibrils,
                "realizations": data.fibrils * 1000,
                "events": int(pooled.sum()),
                "singleton_events": singleton_count,
                "singleton_fraction": singleton_count / int(pooled.sum()),
                "xmin": xmin,
                "tail_events": int(pooled[xmin:].sum()),
                "tail_fraction": float(fit["tail_fraction"]),
                "tail_distinct_sizes": int(np.count_nonzero(pooled[xmin:])),
                "tail_fibrils": int(np.count_nonzero(tail_by_fibril)),
                "tail_realizations": total_tail_runs,
                "initial_size_min": int(n0_array.min()),
                "initial_size_median": float(np.median(n0_array)),
                "initial_size_max": int(n0_array.max()),
                "n0_vs_max_spearman_rho": max_rho,
                "n0_vs_max_p": max_p,
                "n0_vs_q999_spearman_rho": quantile_rho,
                "n0_vs_q999_p": quantile_p,
            }
        )
        stability_rows.extend(
            {"ts": ts, **asdict(result)}
            for result in subset_stability(
                data,
                repetitions=args.repetitions,
                seed=args.seed + condition_index,
            )
        )
        loo_rows.extend(
            {
                "ts": ts,
                "omitted_seed": omitted_seed,
                "xmin": result.xmin,
                "alpha": result.alpha,
                "ks": result.ks,
                "n_tail": result.n_tail,
            }
            for omitted_seed, result in leave_one_fibril_out(data)
        )
        print(f"Ts={ts}: diagnostics complete", flush=True)

    write_csv(args.output / "condition_diagnostics.csv", condition_rows)
    write_csv(args.output / "fibril_diagnostics.csv", fibril_rows)
    write_csv(args.output / "ensemble_stability.csv", stability_rows)
    write_csv(args.output / "leave_one_fibril_out.csv", loo_rows)
    ccdf_figure(datasets, fits, args.output / "ccdf_power_law.png")
    stability_figure(stability_rows, args.output / "ensemble_stability_alpha.png")
    finite_size_figure(fibril_rows, args.output / "finite_size_q999.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

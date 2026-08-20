#!/usr/bin/env python3
"""Evaluate a discrete stretched-cutoff power law for high-Ts avalanches."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from clauset_hierarchical.analysis import fit_block_model_gof, load_fibril_histograms
from clauset_hierarchical.stretched_cutoff import (
    fit_joint_block_gof,
    fit_joint_selected_block_gof,
    fit_joint_stretched_cutoff,
    select_joint_stretched_cutoff_xmin,
)
from clauset_pooled.models import (
    fit_cutoff_power_law,
    fit_lognormal,
    fit_power_law_model,
    fit_stretched_cutoff_power_law,
    log_probabilities,
)


REPOSITORY = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE = (
    REPOSITORY / "Data_avalanches_all_fibrils" / "derived"
    / "avalanche_analysis_v1.duckdb"
)
DEFAULT_OUTPUT = (
    REPOSITORY / "Reviews" / "Issue5_clauset_hierarchical"
    / "stretched_cutoff_high_ts"
)
DEFAULT_TS = (512, 1024, 4096, 8192)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def plot_ccdfs(datasets, fits, path: Path) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)
    for axis, data, fit in zip(axes.flat, datasets, fits, strict=True):
        histogram = data.pooled
        xmin = fit.xmin
        maximum = int(np.flatnonzero(histogram)[-1])
        support = np.arange(xmin, maximum + 1)
        tail = histogram[xmin : maximum + 1]
        empirical = np.cumsum(tail[::-1], dtype=np.int64)[::-1] / int(tail.sum())
        probabilities = np.exp(log_probabilities(fit, support))
        model = 1.0 - np.concatenate(([0.0], np.cumsum(probabilities[:-1])))
        axis.loglog(support, empirical, ".", ms=2.5, label="empirical")
        axis.loglog(support, model, lw=1.5, label="stretched cutoff")
        axis.set_title(
            f"$T_s={data.ts}$; $s_c={fit.parameters['scale']:.1f}$, "
            f"$\\beta={fit.parameters['beta']:.2f}$"
        )
        axis.set_xlabel("s")
        axis.set_ylabel(rf"$P(S\geq s\mid S\geq{xmin})$")
    axes.flat[0].legend(fontsize=8)
    figure.savefig(path, dpi=180)
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--ts", dest="ts_values", action="append", type=int)
    parser.add_argument(
        "--xmin", type=int,
        help="fix the common lower cutoff; otherwise select it by joint KS",
    )
    parser.add_argument("--minimum-xmin", type=int, default=1)
    parser.add_argument("--maximum-xmin", type=int)
    parser.add_argument("--minimum-tail", type=int, default=1000)
    parser.add_argument("--individual-replicates", type=int, default=199)
    parser.add_argument("--joint-replicates", type=int, default=199)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--reselect-xmin-bootstrap",
        action="store_true",
        help="repeat the full xmin scan in every centered block replicate",
    )
    parser.add_argument("--seed", type=int, default=161803)
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        raise SystemExit(f"output directory is not empty: {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)
    ts_values = tuple(args.ts_values or DEFAULT_TS)
    datasets = tuple(load_fibril_histograms(args.database, ts) for ts in ts_values)

    if args.xmin is None:
        selection = select_joint_stretched_cutoff_xmin(
            datasets,
            minimum_xmin=args.minimum_xmin,
            maximum_xmin=args.maximum_xmin,
            minimum_tail=args.minimum_tail,
        )
        joint = selection.selected
        xmin = joint.xmin
    else:
        joint = fit_joint_stretched_cutoff(datasets, xmin=args.xmin)
        selection = None
        xmin = args.xmin
    print(
        f"selected common xmin={xmin}; maximum KS={max(joint.ks):.6f}",
        flush=True,
    )

    rows = []
    fitted_stretched = []
    for index, data in enumerate(datasets):
        histogram = data.pooled
        candidates = (
            fit_power_law_model(histogram, xmin),
            fit_cutoff_power_law(histogram, xmin),
            fit_lognormal(histogram, xmin),
            fit_stretched_cutoff_power_law(histogram, xmin),
        )
        stretched = candidates[-1]
        fitted_stretched.append(stretched)
        goodness = fit_block_model_gof(
            data,
            model="stretched_cutoff_power_law",
            xmin=xmin,
            replicates=args.individual_replicates,
            seed=args.seed + index,
        )
        for fit in candidates:
            rows.append({
                "ts": data.ts,
                "model": fit.model,
                "xmin": fit.xmin,
                "n_tail": fit.n_tail,
                "log_likelihood": fit.log_likelihood,
                "ks": fit.ks,
                "aic": 2 * fit.parameter_count - 2 * fit.log_likelihood,
                "bic": fit.parameter_count * math.log(fit.n_tail) - 2 * fit.log_likelihood,
                "block_gof_p": goodness.p_value if fit is stretched else "",
                "block_gof_exceedances": goodness.exceedances if fit is stretched else "",
                "block_gof_replicates": goodness.replicates if fit is stretched else "",
                **fit.parameters,
            })
        print(
            f"Ts={data.ts}: stretched KS={stretched.ks:.6f}, "
            f"block p={goodness.p_value:.4f}",
            flush=True,
        )

    if selection is None or not args.reselect_xmin_bootstrap:
        joint_gof = fit_joint_block_gof(
            datasets,
            xmin=xmin,
            replicates=args.joint_replicates,
            seed=args.seed + 10_000,
        )
    else:
        joint_gof, gof_selection = fit_joint_selected_block_gof(
            datasets,
            minimum_xmin=args.minimum_xmin,
            maximum_xmin=args.maximum_xmin,
            minimum_tail=args.minimum_tail,
            replicates=args.joint_replicates,
            seed=args.seed + 10_000,
            workers=args.workers,
        )
        if gof_selection.selected.xmin != xmin:
            raise RuntimeError("repeated xmin selection was not deterministic")
    joint_rows = []
    for index, ts in enumerate(ts_values):
        joint_rows.append({
            "ts": ts,
            "xmin": xmin,
            "common_alpha": joint.alpha,
            "common_beta": joint.beta,
            "scale": joint.scales[index],
            "n_tail": joint.n_tail[index],
            "ks": joint.ks[index],
            "condition_block_gof_p": joint_gof.condition_p_values[index],
            "condition_exceedances": joint_gof.condition_exceedances[index],
            "replicates": joint_gof.replicates,
            "joint_log_likelihood": joint.log_likelihood,
            "joint_block_gof_p": joint_gof.joint_p_value,
            "joint_exceedances": joint_gof.joint_exceedances,
        })
    bootstrap_rows = []
    for result in joint_gof.bootstrap:
        row = {
            "replicate": result.replicate,
            "xmin": result.xmin,
            "gof_xmin": result.gof_xmin,
            "alpha": result.alpha,
            "beta": result.beta,
            "maximum_centered_ks": result.maximum_centered_ks,
        }
        for index, ts in enumerate(ts_values):
            row[f"scale_ts_{ts}"] = result.scales[index]
            row[f"centered_ks_ts_{ts}"] = result.centered_ks[index]
        bootstrap_rows.append(row)
    write_csv(args.output / "individual_model_fits.csv", rows)
    write_csv(args.output / "joint_fit.csv", joint_rows)
    write_csv(args.output / "joint_block_bootstrap.csv", bootstrap_rows)
    if selection is not None:
        write_csv(args.output / "xmin_scan.csv", [
            {
                "xmin": fit.xmin,
                "maximum_ks": max(fit.ks),
                "alpha": fit.alpha,
                "beta": fit.beta,
                "joint_log_likelihood": fit.log_likelihood,
                **{
                    f"scale_ts_{ts}": fit.scales[index]
                    for index, ts in enumerate(ts_values)
                },
                **{
                    f"ks_ts_{ts}": fit.ks[index]
                    for index, ts in enumerate(ts_values)
                },
                **{
                    f"n_tail_ts_{ts}": fit.n_tail[index]
                    for index, ts in enumerate(ts_values)
                },
            }
            for fit in selection.candidates
        ])
    plot_ccdfs(datasets, fitted_stretched, args.output / "individual_ccdf.png")
    plot_ccdfs(
        datasets,
        [joint.model_for(index) for index in range(len(datasets))],
        args.output / "joint_ccdf.png",
    )
    metadata = {
        "model": "p(s) proportional to s^-alpha exp[-(s/scale)^beta]",
        "normalization": "exact discrete infinite support with bounded remainder",
        "population": "local preterminal connected avalanches; singletons retained in body",
        "support": f"common xmin={xmin}",
        "xmin_selection": (
            "fixed by command line" if selection is None else
            "minimum maximum condition-wise KS after joint MLE"
        ),
        "xmin_candidate_range": (
            None if selection is None else
            [selection.candidates[0].xmin, selection.candidates[-1].xmin]
        ),
        "minimum_tail_per_condition": args.minimum_tail,
        "conditions": ts_values,
        "individual_replicates": args.individual_replicates,
        "joint_replicates": args.joint_replicates,
        "joint_workers": args.workers,
        "gof_xmin_treatment": (
            "reselected in every block replicate"
            if args.reselect_xmin_bootstrap else
            "conditional on the selected common xmin"
        ),
        "seed": args.seed,
        "selection_status": "exploratory; family selected after inspecting high-Ts curvature",
        "database": str(args.database.resolve()),
    }
    (args.output / "analysis.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    plausible_individual = {
        int(row["ts"]): float(row["block_gof_p"]) > 0.10
        for row in rows if row["model"] == "stretched_cutoff_power_law"
    }
    lines = [
        "# High-Ts stretched-cutoff analysis",
        "",
        "The exploratory candidate is the exact discrete model "
        r"$p(s)\propto s^{-\alpha}\exp[-(s/s_c)^\beta]$ on the fixed common "
        rf"support $s\geq{xmin}$.",
        "",
        "| Ts | alpha | beta | scale | KS | individual block p | decision |",
        "|---:|---:|---:|---:|---:|---:|:---|",
    ]
    for fit, row in zip(fitted_stretched, [
        row for row in rows if row["model"] == "stretched_cutoff_power_law"
    ], strict=True):
        lines.append(
            f"| {row['ts']} | {fit.parameters['alpha']:.4f} | "
            f"{fit.parameters['beta']:.4f} | {fit.parameters['scale']:.2f} | "
            f"{fit.ks:.5f} | {float(row['block_gof_p']):.3f} | "
            f"{'not rejected' if plausible_individual[int(row['ts'])] else 'rejected'} |"
        )
    lines.extend([
        "",
        f"The joint common-shape fit gives alpha={joint.alpha:.4f}, "
        f"beta={joint.beta:.4f}, and joint block p={joint_gof.joint_p_value:.3f}. ",
        "The family is considered a common high-Ts description only if the joint "
        "test and every condition-specific absolute-fit test exceed 0.10.",
        "",
        "Because this family was proposed after inspecting the observed curvature, "
        "the analysis is exploratory even if a goodness-of-fit test does not reject it.",
        "",
    ])
    (args.output / "RUN_SUMMARY.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

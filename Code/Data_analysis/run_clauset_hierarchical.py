#!/usr/bin/env python3
"""Run block-aware Clauset analysis on local preterminal avalanches."""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict
from pathlib import Path

from clauset_hierarchical.analysis import (
    available_ts,
    fit_block_model_gof,
    fit_block_power_law,
    fit_competing_models,
    load_fibril_histograms,
)


REPOSITORY = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE = (
    REPOSITORY
    / "Data_avalanches_all_fibrils"
    / "derived"
    / "avalanche_analysis_v1.duckdb"
)
DEFAULT_OUTPUT = REPOSITORY / "Reviews" / "Issue5_clauset_hierarchical"


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _decision(
    p_value: float,
    comparisons: list[dict[str, object]],
    alternative_gof: dict[str, float],
) -> str:
    if p_value <= 0.10:
        plausible = sorted(
            model for model, model_p in alternative_gof.items()
            if model_p >= 0.10
        )
        if plausible:
            return "pure_power_law_rejected;plausible=" + "+".join(plausible)
        return "pure_power_law_rejected;no_tested_model_plausible"
    favored_alternative = any(
        row["second"] in {"lognormal", "exponential"}
        and float(row["p_value"]) < 0.05
        and row["favored"] == row["second"]
        and alternative_gof[str(row["second"])] > 0.10
        for row in comparisons
        if row["p_value"] not in (None, "")
    )
    if favored_alternative:
        return "pure_power_law_plausible_but_alternative_favored"
    return "pure_power_law_plausible"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--ts", dest="ts_values", action="append", type=int)
    parser.add_argument("--replicates", type=int, default=999)
    parser.add_argument("--alternative-replicates", type=int, default=499)
    parser.add_argument("--minimum-xmin", type=int, default=1)
    parser.add_argument("--minimum-tail", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=12738)
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        raise SystemExit(f"output directory is not empty: {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)
    selected_ts = args.ts_values or available_ts(args.database)

    power_rows: list[dict[str, object]] = []
    bootstrap_rows: list[dict[str, object]] = []
    model_rows: list[dict[str, object]] = []
    comparison_rows: list[dict[str, object]] = []
    model_gof_rows: list[dict[str, object]] = []
    for condition_index, ts in enumerate(selected_ts):
        data = load_fibril_histograms(args.database, ts)
        result = fit_block_power_law(
            data,
            minimum_xmin=args.minimum_xmin,
            minimum_tail=args.minimum_tail,
            replicates=args.replicates,
            seed=args.seed + condition_index,
        )
        models, comparisons = fit_competing_models(data, result.observed.xmin)
        alternative_gof = {}
        for model_index, model in enumerate(
            ("cutoff_power_law", "lognormal", "exponential")
        ):
            goodness = fit_block_model_gof(
                data,
                model=model,
                xmin=result.observed.xmin,
                replicates=args.alternative_replicates,
                seed=args.seed + 10_000 + condition_index * 10 + model_index,
            )
            alternative_gof[model] = goodness.p_value
            model_gof_rows.append(
                {
                    "ts": ts,
                    "model": model,
                    "xmin": goodness.xmin,
                    "ks": goodness.ks,
                    "block_gof_p": goodness.p_value,
                    "exceedances": goodness.exceedances,
                    "replicates": goodness.replicates,
                }
            )
        local_comparisons = []
        for comparison in comparisons:
            row = {"ts": ts, **asdict(comparison)}
            comparison_rows.append(row)
            local_comparisons.append(row)
        power_rows.append(
            {
                "ts": ts,
                "fibrils": data.fibrils,
                "events": int(data.pooled.sum()),
                "xmin": result.observed.xmin,
                "alpha": result.observed.alpha,
                "ks": result.observed.ks,
                "n_tail": result.observed.n_tail,
                "tail_fraction": result.tail_fraction,
                "maximum_size": result.maximum_size,
                "scaling_decades": result.scaling_decades,
                "block_gof_p": result.p_value,
                "block_gof_exceedances": result.exceedances,
                "block_gof_replicates": result.replicates,
                "alpha_ci_low": result.alpha_ci[0],
                "alpha_ci_high": result.alpha_ci[1],
                "xmin_ci_low": result.xmin_ci[0],
                "xmin_ci_high": result.xmin_ci[1],
                "cutoff_block_gof_p": alternative_gof["cutoff_power_law"],
                "lognormal_block_gof_p": alternative_gof["lognormal"],
                "exponential_block_gof_p": alternative_gof["exponential"],
                "decision": _decision(
                    result.p_value, local_comparisons, alternative_gof
                ),
            }
        )
        for bootstrap in result.bootstrap:
            bootstrap_rows.append({"ts": ts, **asdict(bootstrap)})
        for fit in models.values():
            model_rows.append(
                {
                    "ts": ts,
                    "model": fit.model,
                    "xmin": fit.xmin,
                    "n_tail": fit.n_tail,
                    "log_likelihood": fit.log_likelihood,
                    "ks": fit.ks,
                    "aic_descriptive": 2 * fit.parameter_count - 2 * fit.log_likelihood,
                    "bic_descriptive": (
                        fit.parameter_count * math.log(fit.n_tail)
                        - 2 * fit.log_likelihood
                    ),
                    **fit.parameters,
                }
            )
        print(
            f"Ts={ts}: xmin={result.observed.xmin}, "
            f"alpha={result.observed.alpha:.4f}, "
            f"block p={result.p_value:.4f}",
            flush=True,
        )

    _write_csv(args.output / "power_law_fits.csv", power_rows)
    _write_csv(args.output / "block_bootstrap_replicates.csv", bootstrap_rows)
    _write_csv(args.output / "model_fits.csv", model_rows)
    _write_csv(args.output / "model_comparisons.csv", comparison_rows)
    _write_csv(args.output / "model_gof.csv", model_gof_rows)
    metadata = {
        "method": "Clauset discrete MLE/xmin/KS with centered fibril-block bootstrap",
        "population": "local preterminal connected avalanches; singletons retained",
        "independent_block": "fibril geometry (seed); 50 per Ts",
        "gof_support": "conditional on observed power-law-selected xmin",
        "models": ["power_law", "cutoff_power_law", "lognormal", "exponential"],
        "acceptance": "pure power law rejected when block GOF p <= 0.10",
        "nested_cutoff_warning": (
            "Wilks is reported only as a descriptive reference because the models "
            "are nested at a boundary; cutoff plausibility uses block goodness of fit"
        ),
        "parameters": {
            "replicates": args.replicates,
            "alternative_replicates": args.alternative_replicates,
            "minimum_xmin": args.minimum_xmin,
            "minimum_tail": args.minimum_tail,
            "seed": args.seed,
            "ts": selected_ts,
        },
        "database": str(args.database.resolve()),
    }
    (args.output / "analysis.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Hierarchical Clauset analysis",
        "",
        "Local connected avalanches are analyzed before the terminal rupture step. "
        "The exact discrete power-law MLE and KS-selected lower cutoff follow "
        "Clauset et al.; goodness of fit is calibrated by a centered bootstrap "
        "that resamples the 50 fibril geometries as independent blocks.",
        "",
        "| Ts | xmin | alpha (95% block CI) | pure p | cutoff p | lognormal p | exponential p | decades | decision |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|:---|",
    ]
    for row in power_rows:
        lines.append(
            f"| {row['ts']} | {row['xmin']} | {float(row['alpha']):.4f} "
            f"[{float(row['alpha_ci_low']):.4f}, {float(row['alpha_ci_high']):.4f}] | "
            f"{float(row['block_gof_p']):.3f} | "
            f"{float(row['cutoff_block_gof_p']):.3f} | "
            f"{float(row['lognormal_block_gof_p']):.3f} | "
            f"{float(row['exponential_block_gof_p']):.3f} | "
            f"{float(row['scaling_decades']):.2f} | {row['decision']} |"
        )
    lines.extend(
        [
            "",
            "A p-value above 0.10 makes the pure power law plausible; it does "
            "not prove it. Model comparisons use the same selected support. The "
            "pure-versus-cutoff Wilks value remains a descriptive reference because "
            "the models are nested at a boundary; cutoff plausibility is determined "
            "by its block-aware absolute-fit test.",
            "",
        ]
    )
    (args.output / "README.md").write_text("\n".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

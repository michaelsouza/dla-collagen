#!/usr/bin/env python3
"""Run fixed-support parametric GOF tests for pooled alternative models."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .alternative_gof import parametric_gof
from .models import fit_lognormal
from .power_law import read_size_histogram, select_xmin


def _write(path: Path, rows: list[dict[str, object]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=sorted({key for row in rows for key in row}))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--replicates", type=int, default=2500)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=12738)
    parser.add_argument("--minimum-tail", type=int, default=1000)
    parser.add_argument("--ts", type=int, action="append")
    parser.add_argument(
        "--models",
        nargs="+",
        default=["cutoff_power_law", "lognormal", "exponential"],
        choices=["cutoff_power_law", "lognormal", "exponential"],
    )
    parser.add_argument("--tag", default="alternative_model_gof_B2500")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    selected_ts = set(args.ts or [])
    paths = sorted(
        args.input_dir.glob("ts_*.txt"),
        key=lambda path: int(path.stem.removeprefix("ts_")),
    )
    if selected_ts:
        paths = [path for path in paths if int(path.stem.removeprefix("ts_")) in selected_ts]
    if not paths:
        raise SystemExit("no selected input files")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / f"{args.tag}.csv"
    replica_path = args.output_dir / f"{args.tag}_replicates.csv"
    summaries: list[dict[str, object]] = []
    replicas: list[dict[str, object]] = []
    if args.resume and summary_path.exists() and replica_path.exists():
        with summary_path.open(newline="", encoding="utf-8") as stream:
            summaries.extend(csv.DictReader(stream))
        with replica_path.open(newline="", encoding="utf-8") as stream:
            replicas.extend(csv.DictReader(stream))
    completed = {
        (int(row["ts"]), str(row["model"]))
        for row in summaries
        if int(row["replicates"]) == args.replicates
        or str(row.get("status", "")).startswith("not_testable")
    }

    for path in paths:
        ts = int(path.stem.removeprefix("ts_"))
        histogram = read_size_histogram(path, minimum_size=2)
        xmin = select_xmin(histogram, minimum_tail=args.minimum_tail).xmin
        for model_index, model in enumerate(args.models, start=1):
            if (ts, model) in completed:
                print(f"Ts={ts}, model={model}: checkpoint already complete", flush=True)
                continue
            condition_seed = args.seed + 100_000 * ts + 1_000 * model_index
            if model == "lognormal":
                observed_lognormal = fit_lognormal(histogram, xmin)
                if (
                    abs(observed_lognormal.parameters["mu"]) > 10_000.0
                    and observed_lognormal.parameters["sigma"] > 100.0
                ):
                    summaries.append(
                        {
                            "ts": ts,
                            "model": model,
                            "xmin": xmin,
                            "n_tail": observed_lognormal.n_tail,
                            "observed_ks": observed_lognormal.ks,
                            "replicates": 0,
                            "exceedances": "",
                            "p_value": "",
                            "monte_carlo_standard_error": "",
                            "seed": condition_seed,
                            "status": "not_testable_nonfinite_mle_limit",
                            **observed_lognormal.parameters,
                        }
                    )
                    _write(summary_path, summaries)
                    print(
                        f"Ts={ts}, model={model}: non-finite MLE limit; bootstrap skipped",
                        flush=True,
                    )
                    completed.add((ts, model))
                    continue
            print(
                f"Ts={ts}, model={model}: starting B={args.replicates}", flush=True
            )
            result = parametric_gof(
                histogram,
                model=model,
                xmin=xmin,
                replicates=args.replicates,
                seed=condition_seed,
                workers=args.workers,
            )
            summaries.append(
                {
                    "ts": ts,
                    "model": model,
                    "xmin": xmin,
                    "n_tail": result.observed.n_tail,
                    "observed_ks": result.observed.ks,
                    "replicates": result.replicates,
                    "exceedances": result.exceedances,
                    "p_value": result.p_value,
                    "monte_carlo_standard_error": result.monte_carlo_standard_error,
                    "seed": condition_seed,
                    "status": "completed",
                    **result.observed.parameters,
                }
            )
            replicas.extend(
                {
                    "ts": ts,
                    "model": model,
                    "replicate": index,
                    "synthetic_ks": ks,
                }
                for index, ks in enumerate(result.synthetic_ks, start=1)
            )
            _write(summary_path, summaries)
            _write(replica_path, replicas)
            print(
                f"Ts={ts}, model={model}: p={result.p_value:.6f} "
                f"({result.exceedances}/{result.replicates})",
                flush=True,
            )

    (args.output_dir / f"{args.tag}_run.json").write_text(
        json.dumps(
            {
                "method": "fixed-support parametric bootstrap with full parameter refit",
                "population": "pooled local events on s>=power-law-selected xmin",
                "hierarchical_or_per_fibril_analysis": "not performed",
                "replicates": args.replicates,
                "models": args.models,
                "master_seed": args.seed,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

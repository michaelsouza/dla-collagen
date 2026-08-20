#!/usr/bin/env python3
"""Run the iid parametric-bootstrap sensitivity for the joint high-Ts model."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from clauset_hierarchical.analysis import load_fibril_histograms
from clauset_hierarchical.stretched_cutoff import fit_joint_parametric_gof


REPOSITORY = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE = (
    REPOSITORY / "Data_avalanches_all_fibrils" / "derived"
    / "avalanche_analysis_v1.duckdb"
)
DEFAULT_OUTPUT = (
    REPOSITORY / "Reviews" / "Issue5_clauset_hierarchical"
    / "stretched_cutoff_high_ts" / "iid_joint_B999"
)
DEFAULT_TS = (512, 1024, 4096, 8192)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--ts", dest="ts_values", action="append", type=int)
    parser.add_argument("--xmin", type=int, default=8)
    parser.add_argument("--replicates", type=int, default=999)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=271828)
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        raise SystemExit(f"output directory is not empty: {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)
    ts_values = tuple(args.ts_values or DEFAULT_TS)
    datasets = tuple(
        load_fibril_histograms(args.database, ts) for ts in ts_values
    )
    result = fit_joint_parametric_gof(
        datasets,
        xmin=args.xmin,
        replicates=args.replicates,
        seed=args.seed,
        workers=args.workers,
    )
    summary = []
    for index, ts in enumerate(ts_values):
        summary.append({
            "ts": ts,
            "xmin": args.xmin,
            "alpha": result.observed.alpha,
            "beta": result.observed.beta,
            "scale": result.observed.scales[index],
            "observed_ks": result.observed.ks[index],
            "condition_iid_p": result.condition_p_values[index],
            "condition_exceedances": result.condition_exceedances[index],
            "replicates": result.replicates,
            "joint_iid_p": result.joint_p_value,
            "joint_exceedances": result.joint_exceedances,
        })
    replicas = []
    for replicate, values in enumerate(result.synthetic_ks):
        row = {"replicate": replicate, "maximum_synthetic_ks": max(values)}
        for ts, value in zip(ts_values, values, strict=True):
            row[f"synthetic_ks_ts_{ts}"] = value
        replicas.append(row)
    write_csv(args.output / "iid_joint_gof.csv", summary)
    write_csv(args.output / "iid_joint_replicates.csv", replicas)
    metadata = {
        "method": "iid parametric bootstrap with joint six-parameter refit",
        "role": "secondary sensitivity; avalanche events are not iid",
        "model": "discrete stretched-cutoff power law",
        "xmin": args.xmin,
        "ts": ts_values,
        "replicates": args.replicates,
        "workers": args.workers,
        "seed": args.seed,
        "database": str(args.database.resolve()),
    }
    (args.output / "analysis.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"joint iid p={result.joint_p_value:.4f} "
        f"({result.joint_exceedances}/{result.replicates})",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

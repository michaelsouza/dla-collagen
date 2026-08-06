#!/usr/bin/env python3
"""Run pooled semiparametric Clauset goodness-of-fit tests by Ts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .gof import clauset_gof
from .power_law import read_size_histogram


def _ts_from_path(path: Path) -> int:
    return int(path.stem.removeprefix("ts_"))


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--replicates", type=int, default=2500)
    parser.add_argument("--minimum-tail", type=int, default=1000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=12738)
    parser.add_argument("--ts", type=int, action="append")
    parser.add_argument("--tag", default="power_law_gof")
    args = parser.parse_args()

    selected_ts = set(args.ts or [])
    paths = sorted(args.input_dir.glob("ts_*.txt"), key=_ts_from_path)
    if selected_ts:
        paths = [path for path in paths if _ts_from_path(path) in selected_ts]
    if not paths:
        raise SystemExit("no selected ts_*.txt inputs found")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    summaries: list[dict[str, object]] = []
    replicas: list[dict[str, object]] = []
    summary_path = args.output_dir / f"{args.tag}.csv"
    replica_path = args.output_dir / f"{args.tag}_replicates.csv"
    for path in paths:
        ts = _ts_from_path(path)
        histogram = read_size_histogram(path, minimum_size=2)
        condition_seed = args.seed + 100_000 * ts
        print(
            f"Ts={ts}: starting B={args.replicates}, workers={args.workers}",
            flush=True,
        )
        result = clauset_gof(
            histogram,
            minimum_xmin=2,
            minimum_tail=args.minimum_tail,
            replicates=args.replicates,
            seed=condition_seed,
            workers=args.workers,
        )
        summaries.append(
            {
                "ts": ts,
                "xmin": result.observed.xmin,
                "alpha": result.observed.alpha,
                "observed_ks": result.observed.ks,
                "n_tail": result.observed.n_tail,
                "replicates": result.replicates,
                "exceedances": result.exceedances,
                "p_value": result.p_value,
                "monte_carlo_standard_error": result.monte_carlo_standard_error,
                "seed": condition_seed,
            }
        )
        replicas.extend(
            {
                "ts": ts,
                "replicate": index,
                "synthetic_ks": ks,
                "synthetic_xmin": xmin,
            }
            for index, (ks, xmin) in enumerate(
                zip(result.synthetic_ks, result.synthetic_xmin, strict=True), start=1
            )
        )
        _write_csv(summary_path, summaries)
        _write_csv(replica_path, replicas)
        print(
            f"Ts={ts}: p={result.p_value:.6f} "
            f"({result.exceedances}/{result.replicates})",
            flush=True,
        )

    metadata = {
        "method": "Clauset semiparametric Monte Carlo with full xmin and alpha refit",
        "population": "pooled local events with s>=2, including terminal force steps",
        "hierarchical_or_per_fibril_analysis": "not performed",
        "replicates": args.replicates,
        "minimum_tail": args.minimum_tail,
        "workers": args.workers,
        "master_seed": args.seed,
        "inputs": [str(path.resolve()) for path in paths],
        "outputs": [str(summary_path.resolve()), str(replica_path.resolve())],
    }
    (args.output_dir / f"{args.tag}_run.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

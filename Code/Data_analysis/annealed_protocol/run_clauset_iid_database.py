#!/usr/bin/env python3
"""Run the original iid Clauset bootstrap on preterminal database histograms."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from clauset_hierarchical.analysis import available_ts, load_fibril_histograms
from clauset_pooled.gof import clauset_gof


REPOSITORY = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE = (
    REPOSITORY / "Data_avalanches_all_fibrils" / "derived"
    / "avalanche_analysis_v1.duckdb"
)
DEFAULT_OUTPUT = REPOSITORY / "Reviews" / "Issue5_clauset_hierarchical" / "iid_clauset"


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
    parser.add_argument("--replicates", type=int, default=2500)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--minimum-tail", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=314159)
    parser.add_argument("--ts", dest="ts_values", action="append", type=int)
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        raise SystemExit(f"output directory is not empty: {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)
    ts_values = args.ts_values or available_ts(args.database)
    summaries = []
    replicas = []
    for index, ts in enumerate(ts_values):
        data = load_fibril_histograms(args.database, ts)
        condition_seed = args.seed + index
        result = clauset_gof(
            data.pooled,
            minimum_xmin=1,
            minimum_tail=args.minimum_tail,
            replicates=args.replicates,
            seed=condition_seed,
            workers=args.workers,
        )
        summaries.append(
            {
                "ts": ts,
                "population": "local_preterminal_s_ge_1",
                "events": int(data.pooled.sum()),
                "xmin": result.observed.xmin,
                "alpha": result.observed.alpha,
                "ks": result.observed.ks,
                "n_tail": result.observed.n_tail,
                "replicates": result.replicates,
                "exceedances": result.exceedances,
                "iid_clauset_p": result.p_value,
                "monte_carlo_standard_error": result.monte_carlo_standard_error,
                "seed": condition_seed,
            }
        )
        replicas.extend(
            {
                "ts": ts,
                "replicate": replicate,
                "synthetic_ks": ks,
                "synthetic_xmin": xmin,
            }
            for replicate, (ks, xmin) in enumerate(
                zip(result.synthetic_ks, result.synthetic_xmin, strict=True), start=1
            )
        )
        write_csv(args.output / "iid_clauset_gof.csv", summaries)
        write_csv(args.output / "iid_clauset_replicates.csv", replicas)
        print(
            f"Ts={ts}: iid Clauset p={result.p_value:.4f} "
            f"({result.exceedances}/{result.replicates})",
            flush=True,
        )
    metadata = {
        "method": "original iid semiparametric Clauset bootstrap with full refit",
        "population": "local preterminal connected avalanches; s>=1 retained",
        "warning": (
            "Events are not iid: runs share fibril geometry and events within a run "
            "share damage history. This is a secondary sensitivity diagnostic."
        ),
        "replicates": args.replicates,
        "workers": args.workers,
        "minimum_tail": args.minimum_tail,
        "master_seed": args.seed,
        "ts": ts_values,
        "database": str(args.database.resolve()),
    }
    (args.output / "analysis.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Fit and test a two-component model on every complete s>=2 distribution."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from .mixture_models import cutoff_lognormal_goodness_of_fit
from .models import fit_lognormal
from .power_law import read_size_histogram


def _write(path: Path, rows: list[dict[str, object]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=sorted({key for row in rows for key in row})
        )
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--replicates", type=int, default=100)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=12738)
    parser.add_argument("--ts", type=int, action="append")
    parser.add_argument("--tag", default="complete_mixture_gof_B100")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    selected_ts = set(args.ts or [])
    paths = sorted(
        args.input_dir.glob("ts_*.txt"),
        key=lambda path: int(path.stem.removeprefix("ts_")),
    )
    if selected_ts:
        paths = [
            path
            for path in paths
            if int(path.stem.removeprefix("ts_")) in selected_ts
        ]
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
        int(row["ts"])
        for row in summaries
        if int(row["replicates"]) == args.replicates
    }

    for path in paths:
        ts = int(path.stem.removeprefix("ts_"))
        if ts in completed:
            print(f"Ts={ts}: checkpoint already complete", flush=True)
            continue
        histogram = read_size_histogram(path, minimum_size=2)
        condition_seed = args.seed + 100_000 * ts
        print(f"Ts={ts}: starting B={args.replicates}", flush=True)
        result = cutoff_lognormal_goodness_of_fit(
            histogram,
            xmin=2,
            replicates=args.replicates,
            seed=condition_seed,
            workers=args.workers,
        )
        single = fit_lognormal(histogram, xmin=2)
        mixture = result.observed
        single_bic = single.parameter_count * np.log(single.n_tail) - 2 * single.log_likelihood
        mixture_bic = mixture.parameter_count * np.log(mixture.n_tail) - 2 * mixture.log_likelihood
        zero_exceedance_upper_95 = (
            1.0 - 0.05 ** (1.0 / result.replicates)
            if result.exceedances == 0
            else ""
        )
        summaries.append(
            {
                "ts": ts,
                "model": mixture.model,
                "xmin": 2,
                "n_events": mixture.n_tail,
                "observed_ks": mixture.ks,
                "single_lognormal_ks": single.ks,
                "log_likelihood": mixture.log_likelihood,
                "single_lognormal_log_likelihood": single.log_likelihood,
                "delta_bic_single_minus_mixture": float(single_bic - mixture_bic),
                "replicates": result.replicates,
                "exceedances": result.exceedances,
                "p_value": result.p_value,
                "monte_carlo_standard_error": result.monte_carlo_standard_error,
                "zero_exceedance_p_upper_95": zero_exceedance_upper_95,
                "seed": condition_seed,
                **mixture.parameters,
            }
        )
        replicas.extend(
            {
                "ts": ts,
                "replicate": index,
                "synthetic_ks": value,
            }
            for index, value in enumerate(result.synthetic_ks, start=1)
        )
        _write(summary_path, summaries)
        _write(replica_path, replicas)
        print(
            f"Ts={ts}: KS={mixture.ks:.6f}, p={result.p_value:.6f} "
            f"({result.exceedances}/{result.replicates})",
            flush=True,
        )

    (args.output_dir / f"{args.tag}_run.json").write_text(
        json.dumps(
            {
                "model": "decreasing discrete cutoff power law plus discrete lognormal mixture",
                "support": "all pooled local-avalanche sizes s>=2",
                "replicates": args.replicates,
                "master_seed": args.seed,
                "decision_note": "For zero exceedances, the CSV reports the exact one-sided 95% binomial upper bound.",
                "force_conditioning": "not performed",
                "hierarchical_or_per_fibril_analysis": "not performed",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
"""Run the independent Issue 14 audit, validation, and observed analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

from issue14_araujo.data import audit_pmf_data
from issue14_araujo.observed import run_observed_analysis
from issue14_araujo.report import build_report, plot_synthetic_validation
from issue14_araujo.synthetic import run_synthetic_validation


REPOSITORY = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = REPOSITORY / "Reviews" / "Issue14_araujo_validation"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage",
        choices=("all", "audit", "synthetic", "observed", "report"),
        default="all",
    )
    parser.add_argument(
        "--pmf-data", type=Path, default=REPOSITORY / "Data_avalanches"
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=20260818)
    parser.add_argument("--observed-bootstrap", type=int, default=39)
    parser.add_argument("--quick", action="store_true", help="Smoke-test settings; not publication evidence")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    stages = {args.stage} if args.stage != "all" else {"audit", "synthetic", "observed", "report"}
    if "audit" in stages:
        counts, pmf_rows, terminal_rows = audit_pmf_data(
            args.pmf_data,
            provenance_manifest=(
                REPOSITORY
                / "Data_fibrils"
                / "Avalanche_force_grouped"
                / "local_avalanche_sizes"
                / "manifest.json"
            ),
        )
        npz_values = {
            f"ts_{ts}_{population}": values
            for (ts, population), values in counts.items()
        }
        import csv
        import json
        import numpy as np

        np.savez_compressed(args.output / "audited_counts.npz", **npz_values)
        for name, rows in (("pmf_audit.csv", pmf_rows), ("terminal_partition_audit.csv", terminal_rows)):
            with (args.output / name).open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
        (args.output / "input_manifest.json").write_text(
            json.dumps(
                {
                    "pmf_directory": str(args.pmf_data.resolve()),
                    "audit_basis": "Data_avalanches PMFs plus authoritative com_terminal provenance manifest",
                    "count_reconstruction": "denominator consensus across every PMF entry; never min(P)",
                    "terminal_rule": "com_terminal minus sem_terminal; nonnegative for every integer size",
                    "analysis_support": "s >= 2",
                    "hierarchy_warning": "Data_avalanches does not retain fibril/realization identity and cannot support hierarchical uncertainty.",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    if "synthetic" in stages:
        settings = (
            {
                "grid_replicates": 1,
                "gof_repetitions": 3,
                "gof_bootstrap": 5,
                "negative_replicates": 1,
                "araujo_replicates": 1,
            }
            if args.quick
            else {}
        )
        run_synthetic_validation(args.output, seed=args.seed, **settings)
        plot_synthetic_validation(args.output)
    if "observed" in stages:
        counts_path = args.output / "audited_counts.npz"
        if not counts_path.exists():
            parser.error(f"missing {counts_path}; run --stage audit first")
        run_observed_analysis(
            counts_path,
            args.output,
            seed=args.seed + 1,
            bootstrap_replicates=(3 if args.quick else args.observed_bootstrap),
        )
    if "report" in stages:
        build_report(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

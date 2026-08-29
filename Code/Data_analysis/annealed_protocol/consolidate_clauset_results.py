#!/usr/bin/env python3
"""Consolidate primary fits with preregistered, higher-resolution refinements."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from scipy import stats


REPOSITORY = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = REPOSITORY / "Reviews" / "Issue5_clauset_hierarchical"
REFINED_FIELDS = (
    "block_gof_p",
    "block_gof_exceedances",
    "block_gof_replicates",
    "alpha_ci_low",
    "alpha_ci_high",
    "xmin_ci_low",
    "xmin_ci_high",
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def monte_carlo_interval(exceedances: int, replicates: int) -> tuple[float, float]:
    """Exact 95% binomial interval for the uncorrected exceedance probability."""
    low = 0.0 if exceedances == 0 else float(
        stats.beta.ppf(0.025, exceedances, replicates - exceedances + 1)
    )
    high = 1.0 if exceedances == replicates else float(
        stats.beta.ppf(0.975, exceedances + 1, replicates - exceedances)
    )
    return low, high


def decision(row: dict[str, str]) -> str:
    p_value = float(row["block_gof_p"])
    low = float(row["block_gof_mc_ci_low"])
    iid_rejected = float(row.get("iid_clauset_p", "nan")) <= 0.10
    if p_value <= 0.10:
        result = (
            "pure_power_law_rejected_by_block_and_iid"
            if iid_rejected else "pure_power_law_rejected_by_block"
        )
    elif low <= 0.10:
        result = "block_not_rejected_borderline"
    else:
        result = "block_not_rejected"
    if p_value > 0.10 and iid_rejected:
        result += ";iid_rejected;sensitive_to_dependence"
    if float(row["scaling_decades"]) < 1.0:
        result += ";tail_shorter_than_one_decade"
    alternatives = ("cutoff", "lognormal", "exponential")
    if all(float(row[f"{name}_block_gof_p"]) <= 0.10 for name in alternatives):
        result += ";all_tested_alternatives_rejected"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--refinement", action="append", type=Path, default=[])
    args = parser.parse_args()
    primary_path = args.output / "power_law_fits.csv"
    rows = {int(row["ts"]): row for row in read_rows(primary_path)}
    iid_path = args.output / "iid_clauset" / "iid_clauset_gof.csv"
    if iid_path.exists():
        for iid in read_rows(iid_path):
            ts = int(iid["ts"])
            if ts not in rows:
                raise SystemExit(f"iid result Ts={ts} is absent from primary table")
            for invariant in ("xmin", "alpha", "ks", "n_tail", "events"):
                if iid[invariant] != rows[ts][invariant]:
                    raise SystemExit(f"iid result changed Ts={ts} invariant {invariant}")
            rows[ts]["iid_clauset_p"] = iid["iid_clauset_p"]
            rows[ts]["iid_clauset_exceedances"] = iid["exceedances"]
            rows[ts]["iid_clauset_replicates"] = iid["replicates"]
    refinement_records = []
    for directory in args.refinement:
        candidates = read_rows(directory / "power_law_fits.csv")
        if len(candidates) != 1:
            raise SystemExit(f"expected one fit in refinement: {directory}")
        refined = candidates[0]
        ts = int(refined["ts"])
        if ts not in rows:
            raise SystemExit(f"refinement Ts={ts} is absent from primary table")
        if int(refined["block_gof_replicates"]) <= int(rows[ts]["block_gof_replicates"]):
            raise SystemExit(f"refinement Ts={ts} has no additional resolution")
        for invariant in ("xmin", "alpha", "ks", "n_tail", "events"):
            if refined[invariant] != rows[ts][invariant]:
                raise SystemExit(f"refinement changed Ts={ts} invariant {invariant}")
        for field in REFINED_FIELDS:
            rows[ts][field] = refined[field]
        refinement_records.append(
            f"Ts={ts}: {refined['block_gof_replicates']} block replicates "
            f"from {directory.as_posix()}"
        )

    final_rows = []
    for ts in sorted(rows):
        row = rows[ts]
        row["primary_decision"] = row.pop("decision")
        low, high = monte_carlo_interval(
            int(row["block_gof_exceedances"]), int(row["block_gof_replicates"])
        )
        row["block_gof_mc_ci_low"] = low
        row["block_gof_mc_ci_high"] = high
        row["final_decision"] = decision(row)
        final_rows.append(row)
    fields = list(dict.fromkeys(key for row in final_rows for key in row))
    with (args.output / "final_power_law_fits.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(final_rows)
    (args.output / "refinement_manifest.txt").write_text(
        "\n".join(refinement_records) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

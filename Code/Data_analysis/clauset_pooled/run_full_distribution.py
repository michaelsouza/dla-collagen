#!/usr/bin/env python3
"""Analyze complete pooled distributions of local-avalanche sizes."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from .full_distribution import (
    condition_histogram,
    distribution_distance,
    summarize_histogram,
    tail_probability,
)
from .power_law import read_size_histogram


TAIL_THRESHOLDS = (2, 5, 10, 50, 100, 500, 1000)


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    paths = sorted(
        args.input_dir.glob("ts_*.txt"),
        key=lambda path: int(path.stem.removeprefix("ts_")),
    )
    if not paths:
        raise SystemExit("no ts_*.txt input files")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    histograms: dict[int, np.ndarray] = {}
    summary_rows: list[dict[str, object]] = []
    pmf_rows: list[dict[str, object]] = []
    for path in paths:
        ts = int(path.stem.removeprefix("ts_"))
        histogram = read_size_histogram(path, minimum_size=1)
        histograms[ts] = histogram
        total = int(histogram.sum())
        nontrivial = int(histogram[2:].sum())
        common = {
            "ts": ts,
            "n_total": total,
            "n_singleton": int(histogram[1]) if histogram.size > 1 else 0,
            "singleton_fraction": float(histogram[1] / total),
            "nontrivial_fraction": float(nontrivial / total),
        }
        for population, minimum_size in (("all", 1), ("nontrivial", 2)):
            conditioned = condition_histogram(histogram, minimum_size)
            summary = summarize_histogram(
                conditioned, population=population, minimum_size=minimum_size
            )
            row = {"ts": ts, **asdict(summary), **common}
            row.update(
                {
                    f"probability_s_ge_{threshold}": tail_probability(
                        conditioned, threshold
                    )
                    for threshold in TAIL_THRESHOLDS
                }
            )
            summary_rows.append(row)

        sizes = np.flatnonzero(histogram)
        cumulative_from_right = np.cumsum(histogram[::-1], dtype=np.int64)[::-1]
        for size in sizes:
            pmf_rows.append(
                {
                    "ts": ts,
                    "size": int(size),
                    "count": int(histogram[size]),
                    "probability": float(histogram[size] / total),
                    "ccdf": float(cumulative_from_right[size] / total),
                }
            )
        print(f"Ts={ts}: {total:,} events; {nontrivial:,} with s>=2", flush=True)

    distance_rows: list[dict[str, object]] = []
    ordered_ts = sorted(histograms)
    for index, first_ts in enumerate(ordered_ts):
        for second_ts in ordered_ts[index + 1 :]:
            for population, minimum_size in (("all", 1), ("nontrivial", 2)):
                distance_rows.append(
                    {
                        "ts_first": first_ts,
                        "ts_second": second_ts,
                        "adjacent": second_ts == ordered_ts[index + 1],
                        "population": population,
                        **asdict(
                            distribution_distance(
                                histograms[first_ts],
                                histograms[second_ts],
                                minimum_size=minimum_size,
                            )
                        ),
                    }
                )

    _write_csv(args.output_dir / "full_distribution_summary.csv", summary_rows)
    _write_csv(args.output_dir / "full_distribution_pmf.csv", pmf_rows)
    _write_csv(
        args.output_dir / "full_distribution_pairwise_distances.csv", distance_rows
    )
    (args.output_dir / "full_distribution_run.json").write_text(
        json.dumps(
            {
                "method": "exact pooled empirical histograms",
                "populations": {"all": "s>=1", "nontrivial": "s>=2"},
                "input_files": [str(path) for path in paths],
                "tail_thresholds": TAIL_THRESHOLDS,
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


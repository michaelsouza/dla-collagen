#!/usr/bin/env python3
"""Run pooled exact-discrete power-law fits for every prepared Ts file."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from .power_law import read_size_histogram, select_xmin


def _ts_from_path(path: Path) -> int:
    try:
        return int(path.stem.removeprefix("ts_"))
    except ValueError as error:
        raise ValueError(f"unexpected input filename: {path.name}") from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--minimum-tail", type=int, default=1000)
    args = parser.parse_args()

    paths = sorted(args.input_dir.glob("ts_*.txt"), key=_ts_from_path)
    if not paths:
        raise SystemExit("no ts_*.txt inputs found")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, int | float]] = []
    for path in paths:
        ts = _ts_from_path(path)
        histogram = read_size_histogram(path, minimum_size=2)
        fit = select_xmin(histogram, minimum_xmin=2, minimum_tail=args.minimum_tail)
        n_total = int(histogram.sum())
        observed_sizes = np.flatnonzero(histogram)
        row = {
            "ts": ts,
            **asdict(fit),
            "n_total_s_ge_2": n_total,
            "tail_fraction": fit.n_tail / n_total,
            "distinct_tail_sizes": int(np.count_nonzero(histogram[fit.xmin :])),
            "maximum_size": int(observed_sizes[-1]),
            "tail_span_decades": float(np.log10(observed_sizes[-1] / fit.xmin)),
        }
        rows.append(row)
        print(
            f"Ts={ts}: xmin={fit.xmin}, alpha={fit.alpha:.8f}, "
            f"KS={fit.ks:.8f}, tail={fit.n_tail}/{n_total}",
            flush=True,
        )

    output_csv = args.output_dir / "observed_power_law_fits.csv"
    temporary = output_csv.with_suffix(".csv.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(output_csv)

    metadata = {
        "method": "Clauset pooled-event exact discrete MLE and exhaustive KS xmin selection",
        "minimum_event_size": 2,
        "minimum_tail": args.minimum_tail,
        "terminal_force_steps": "included because they are present in the prepared inputs",
        "hierarchical_or_per_fibril_analysis": "not performed",
        "inputs": [str(path.resolve()) for path in paths],
        "output": str(output_csv.resolve()),
    }
    (args.output_dir / "observed_run.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Fit and compare pooled discrete tail models on a common support."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from scipy import special

from .models import (
    fit_cutoff_power_law,
    fit_exponential,
    fit_lognormal,
    fit_power_law_model,
    vuong_test,
)
from .power_law import read_size_histogram, select_xmin


def _write(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=sorted({key for row in rows for key in row}))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--minimum-tail", type=int, default=1000)
    args = parser.parse_args()
    paths = sorted(
        args.input_dir.glob("ts_*.txt"),
        key=lambda path: int(path.stem.removeprefix("ts_")),
    )
    if not paths:
        raise SystemExit("no ts_*.txt inputs found")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    fit_rows: list[dict[str, object]] = []
    comparison_rows: list[dict[str, object]] = []
    for path in paths:
        ts = int(path.stem.removeprefix("ts_"))
        histogram = read_size_histogram(path, minimum_size=2)
        selected = select_xmin(histogram, minimum_tail=args.minimum_tail)
        fits = {
            "power_law": fit_power_law_model(histogram, selected.xmin),
            "cutoff_power_law": fit_cutoff_power_law(histogram, selected.xmin),
            "lognormal": fit_lognormal(histogram, selected.xmin),
            "exponential": fit_exponential(histogram, selected.xmin),
        }
        for fit in fits.values():
            fit_rows.append(
                {
                    "ts": ts,
                    "model": fit.model,
                    "xmin": fit.xmin,
                    "n_tail": fit.n_tail,
                    "log_likelihood": fit.log_likelihood,
                    "ks": fit.ks,
                    "aic": 2 * fit.parameter_count - 2 * fit.log_likelihood,
                    "bic": fit.parameter_count * __import__("math").log(fit.n_tail)
                    - 2 * fit.log_likelihood,
                    **fit.parameters,
                }
            )
        power = fits["power_law"]
        for alternative_name in ("lognormal", "exponential"):
            alternative = fits[alternative_name]
            ratio, statistic, p_value = vuong_test(histogram, power, alternative)
            comparison_rows.append(
                {
                    "ts": ts,
                    "model_1": "power_law",
                    "model_2": alternative_name,
                    "log_likelihood_ratio": ratio,
                    "test": "Vuong two-sided normal",
                    "test_statistic": statistic,
                    "p_value": p_value,
                    "interpretation": "model_1" if ratio > 0 else "model_2",
                }
            )
        cutoff = fits["cutoff_power_law"]
        cutoff_lr = 2.0 * (cutoff.log_likelihood - power.log_likelihood)
        comparison_rows.append(
            {
                "ts": ts,
                "model_1": "power_law",
                "model_2": "cutoff_power_law",
                "log_likelihood_ratio": power.log_likelihood - cutoff.log_likelihood,
                "test": "Wilks chi-square df=1",
                "test_statistic": cutoff_lr,
                "p_value": float(special.gammaincc(0.5, cutoff_lr / 2.0)),
                "interpretation": "model_2" if cutoff_lr > 0 else "model_1",
            }
        )
        print(
            f"Ts={ts}: best BIC={min(fits.values(), key=lambda fit: fit.parameter_count * __import__('math').log(fit.n_tail) - 2 * fit.log_likelihood).model}",
            flush=True,
        )

    _write(args.output_dir / "model_fits.csv", fit_rows)
    _write(args.output_dir / "model_comparisons.csv", comparison_rows)
    (args.output_dir / "model_run.json").write_text(
        json.dumps(
            {
                "support": "same s>=power-law-selected xmin for every model",
                "population": "pooled local events s>=2, terminal force steps included",
                "hierarchical_or_per_fibril_analysis": "not performed",
                "nested_test_note": "pure versus cutoff power law uses the chi-square df=1 Wilks limit specified in the analysis protocol",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

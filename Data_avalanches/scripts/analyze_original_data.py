#!/usr/bin/env python3
"""Create exact descriptive tables from the original avalanche PMFs.

No binning or distributional fitting is performed. The script reconstructs
integer frequencies, summarizes the full and non-singleton populations, and
quantifies the effect of including the terminal rupture step.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
from scipy.spatial.distance import jensenshannon

from avalanche_data import AvalancheDistribution, discover_distributions, padded_counts


QUANTILES = (0.50, 0.90, 0.99, 0.999)


def empirical_quantiles(counts: np.ndarray) -> tuple[int, ...]:
    total = int(counts.sum())
    cumulative = np.cumsum(counts, dtype=np.int64)
    ranks = np.maximum(1, np.ceil(np.asarray(QUANTILES) * total).astype(np.int64))
    return tuple(int(value) for value in np.searchsorted(cumulative, ranks, side="left"))


def summarize(distribution: AvalancheDistribution) -> dict[str, object]:
    counts = distribution.infer_counts()
    sizes = np.arange(counts.size, dtype=float)
    total = int(counts.sum())
    nontrivial = counts.copy()
    nontrivial[:2] = 0
    nontrivial_total = int(nontrivial.sum())
    q50, q90, q99, q999 = empirical_quantiles(nontrivial)
    return {
        "file": distribution.path.name,
        "ts": distribution.ts,
        "terminal_population": distribution.terminal_label,
        "observed_size_classes": len(distribution.sizes),
        "n_events": total,
        "n_nontrivial_s_ge_2": nontrivial_total,
        "singleton_probability": counts[1] / total,
        "nontrivial_probability": nontrivial_total / total,
        "mean_all": float(np.dot(sizes, counts) / total),
        "mean_s_ge_2": float(np.dot(sizes, nontrivial) / nontrivial_total),
        "q50_s_ge_2": q50,
        "q90_s_ge_2": q90,
        "q99_s_ge_2": q99,
        "q999_s_ge_2": q999,
        "maximum": int(np.flatnonzero(counts)[-1]),
        "probability_sum": float(distribution.probabilities.sum()),
    }


def terminal_effect(
    with_terminal: AvalancheDistribution, without_terminal: AvalancheDistribution
) -> dict[str, object]:
    all_counts, preterminal_counts = padded_counts(with_terminal, without_terminal)
    terminal_counts = all_counts - preterminal_counts
    if np.any(terminal_counts < 0):
        raise ValueError(f"Ts={with_terminal.ts}: negative inferred terminal counts")

    sizes = np.arange(all_counts.size, dtype=float)
    n_all = int(all_counts.sum())
    n_preterminal = int(preterminal_counts.sum())
    n_terminal = int(terminal_counts.sum())
    n_all_nontrivial = int(all_counts[2:].sum())
    n_terminal_nontrivial = int(terminal_counts[2:].sum())
    rods_all = float(np.dot(sizes, all_counts))
    rods_terminal = float(np.dot(sizes, terminal_counts))

    all_pmf = all_counts[2:] / n_all_nontrivial
    preterminal_pmf = preterminal_counts[2:] / preterminal_counts[2:].sum()
    all_cdf = np.cumsum(all_pmf)
    preterminal_cdf = np.cumsum(preterminal_pmf)

    return {
        "ts": with_terminal.ts,
        "n_all_events": n_all,
        "n_preterminal_events": n_preterminal,
        "n_terminal_events": n_terminal,
        "terminal_fraction_all_events": n_terminal / n_all,
        "terminal_fraction_events_s_ge_2": n_terminal_nontrivial / n_all_nontrivial,
        "terminal_singleton_fraction": terminal_counts[1] / n_terminal,
        "mean_terminal_size": rods_terminal / n_terminal,
        "maximum_terminal_size": int(np.flatnonzero(terminal_counts)[-1]),
        "terminal_fraction_removed_rods": rods_terminal / rods_all,
        "jensen_shannon_s_ge_2": float(
            jensenshannon(all_pmf, preterminal_pmf, base=2.0)
        ),
        "kolmogorov_smirnov_s_ge_2": float(
            np.max(np.abs(all_cdf - preterminal_cdf))
        ),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", type=Path, default=Path(__file__).resolve().parent.parent
    )
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output_dir = args.output_dir or args.data_dir / "results"

    distributions = discover_distributions(args.data_dir)
    summaries = [summarize(item) for item in distributions]
    write_csv(output_dir / "original_data_summary.csv", summaries)

    by_condition = {(item.ts, item.includes_terminal): item for item in distributions}
    effects = [
        terminal_effect(by_condition[(ts, True)], by_condition[(ts, False)])
        for ts in sorted({item.ts for item in distributions})
    ]
    write_csv(output_dir / "terminal_effect_summary.csv", effects)

    print(f"Wrote {output_dir / 'original_data_summary.csv'}")
    print(f"Wrote {output_dir / 'terminal_effect_summary.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

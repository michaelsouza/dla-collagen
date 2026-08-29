#!/usr/bin/env python3
"""Build and plot exact empirical CCDFs of local avalanche sizes."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from local_avalanche_counts import FILE_RE, iter_force_steps


def collect_size_counts(paths: list[Path]) -> dict[str, dict[int, Counter[int]]]:
    """Count exact local sizes by Ts for all and preterminal events."""
    counts: dict[str, dict[int, Counter[int]]] = {
        "all": defaultdict(Counter),
        "preterminal": defaultdict(Counter),
    }
    for path in paths:
        match = FILE_RE.match(path.name)
        if not match:
            raise ValueError(f"unexpected rupture filename: {path.name}")
        ts = int(match.group("ts"))
        for step in iter_force_steps(path):
            counts["all"][ts].update(step.local_sizes)
            if not step.terminal:
                counts["preterminal"][ts].update(step.local_sizes)
    return counts


def empirical_ccdf(size_counts: Counter[int]) -> tuple[np.ndarray, np.ndarray]:
    """Return observed sizes and exact P(S >= s) at each observed size."""
    sizes = np.array(sorted(size_counts), dtype=np.int64)
    frequencies = np.array([size_counts[int(size)] for size in sizes], dtype=np.int64)
    survival = np.cumsum(frequencies[::-1], dtype=np.int64)[::-1] / frequencies.sum()
    return sizes, survival


def write_counts(path: Path, counts: dict[str, dict[int, Counter[int]]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("population", "ts", "local_size", "frequency"))
        for population in ("all", "preterminal"):
            for ts in sorted(counts[population]):
                for size, frequency in sorted(counts[population][ts].items()):
                    writer.writerow((population, ts, size, frequency))


def plot_population(
    population: str,
    counts: dict[int, Counter[int]],
    output_dir: Path,
) -> None:
    fig, axis = plt.subplots(figsize=(7.2, 5.4), constrained_layout=True)
    ts_values = sorted(counts)
    colors = plt.colormaps["viridis"](np.linspace(0.05, 0.95, len(ts_values)))
    for ts, color in zip(ts_values, colors):
        sizes, survival = empirical_ccdf(counts[ts])
        axis.step(sizes, survival, where="post", linewidth=1.35, color=color, label=str(ts))

    title = "All local events" if population == "all" else "Preterminal local events"
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlabel(r"Local avalanche size, $s$")
    axis.set_ylabel(r"Empirical CCDF, $P(S \geq s)$")
    axis.set_title(title)
    axis.grid(which="both", alpha=0.2)
    axis.legend(title=r"$T_s$", ncol=2, frameon=False)

    stem = f"local_event_ccdf_{population}"
    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"{stem}.{suffix}", dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_root", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    paths = sorted(args.data_root.glob("runs/ts_*/*_m_*.txt"))
    if not paths:
        raise SystemExit("no rupture files found")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    counts = collect_size_counts(paths)
    write_counts(args.output_dir / "local_event_size_frequencies.csv", counts)
    plot_population("all", counts["all"], args.output_dir)
    plot_population("preterminal", counts["preterminal"], args.output_dir)

    for population in ("all", "preterminal"):
        totals = ", ".join(
            f"Ts={ts}: n={sum(counts[population][ts].values())}"
            for ts in sorted(counts[population])
        )
        print(f"{population}: {totals}")


if __name__ == "__main__":
    main()

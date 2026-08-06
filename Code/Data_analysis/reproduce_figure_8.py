#!/usr/bin/env python3
"""Reproduce Figure 8 from the grouped fracture-output files.

By default, every force is normalized by the rupture force of its own
realization, ``F_n = F/F_rup``, as defined in the manuscript. Within each
realization and normalized-force bin, ``Psi`` is the fraction of removed
molecules belonging to connected clusters with size ``s >= 2``. The plotted
value is the mean of Psi over active realization-bin pairs (pairs containing
at least one removed molecule). The old file-level normalization remains
available as an explicit command-line option.

The raw files contain one fibril per file and several rupture realizations,
separated by dashed marker lines.  Reading them directly avoids depending on
the exploratory notebook state and makes all exported data reproducible.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DEFAULT_TS = (2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192)
DEFAULT_SELECTED_TS = (8, 32, 128, 8192)
EXPECTED_HEADER = (
    "f,num_active_particles,num_deleted_particles,total_deleted_rods,"
    "avalanche_sizes"
)


@dataclass(frozen=True)
class FileEvents:
    """The event-bearing rows needed from one raw fibril file."""

    force: np.ndarray
    run_id: np.ndarray
    singleton_mass: np.ndarray
    collective_mass: np.ndarray
    run_count: int
    terminal_forces: np.ndarray


@dataclass(frozen=True)
class CurveStatistics:
    """Mean cluster contribution for one value of Ts."""

    ts: int
    normalization: str
    force_midpoint: np.ndarray
    mean_singleton_fraction: np.ndarray
    std_singleton_fraction: np.ndarray
    mean_collective_fraction: np.ndarray
    std_collective_fraction: np.ndarray
    active_pairs: np.ndarray
    file_count: int
    run_count: int


def _parse_cluster_masses(value: str, *, source: Path, line_number: int) -> tuple[int, int]:
    """Return molecule mass in singleton and non-singleton clusters."""

    value = value.strip().strip('"')
    if value in {"", "0"}:
        return 0, 0
    try:
        sizes = tuple(int(item) for item in value.split("-"))
    except ValueError as error:
        raise ValueError(
            f"{source}:{line_number}: malformed avalanche_sizes value {value!r}"
        ) from error
    if any(size <= 0 for size in sizes):
        raise ValueError(
            f"{source}:{line_number}: avalanche sizes must be positive: {value!r}"
        )
    singleton_mass = sum(size for size in sizes if size == 1)
    collective_mass = sum(size for size in sizes if size >= 2)
    return singleton_mass, collective_mass


def parse_fibril_file(source: Path) -> FileEvents:
    """Parse one fibril file, retaining only rows with removed molecules."""

    forces: list[float] = []
    run_ids: list[int] = []
    singleton_masses: list[int] = []
    collective_masses: list[int] = []
    terminal_forces: list[float] = []
    current_run = 0
    current_run_max_force = -np.inf
    current_run_terminal_force: float | None = None
    saw_header = False
    saw_data = False

    with source.open("r", encoding="utf-8", newline="") as stream:
        for line_number, raw_line in enumerate(stream, start=1):
            line = raw_line.strip()
            if not line:
                continue
            if line == EXPECTED_HEADER:
                if saw_header:
                    raise ValueError(f"{source}:{line_number}: repeated header")
                saw_header = True
                continue
            if line.startswith("---"):
                if not saw_data or current_run_terminal_force is None:
                    raise ValueError(
                        f"{source}:{line_number}: run {current_run} has no terminal row"
                    )
                terminal_forces.append(current_run_max_force)
                current_run += 1
                current_run_max_force = -np.inf
                current_run_terminal_force = None
                saw_data = False
                continue
            if not saw_header:
                raise ValueError(f"{source}:{line_number}: data precede the header")

            fields = next(csv.reader([line]))
            if len(fields) != 5:
                raise ValueError(
                    f"{source}:{line_number}: expected 5 fields, found {len(fields)}"
                )
            try:
                force = float(fields[0])
                active_particles = int(fields[1])
                total_deleted_rods = int(fields[3])
            except ValueError as error:
                raise ValueError(
                    f"{source}:{line_number}: malformed numeric field"
                ) from error
            if not np.isfinite(force) or force < 0:
                raise ValueError(f"{source}:{line_number}: invalid force {force}")
            if current_run_terminal_force is not None:
                raise ValueError(
                    f"{source}:{line_number}: data found after terminal row in run {current_run}"
                )

            current_run_max_force = max(current_run_max_force, force)
            saw_data = True
            singleton_mass, collective_mass = _parse_cluster_masses(
                fields[4], source=source, line_number=line_number
            )
            if singleton_mass + collective_mass != total_deleted_rods:
                raise ValueError(
                    f"{source}:{line_number}: cluster mass "
                    f"{singleton_mass + collective_mass} does not equal "
                    f"total_deleted_rods {total_deleted_rods}"
                )
            if total_deleted_rods > 0:
                forces.append(force)
                run_ids.append(current_run)
                singleton_masses.append(singleton_mass)
                collective_masses.append(collective_mass)
            if active_particles == 0:
                current_run_terminal_force = force

    if not saw_header:
        raise ValueError(f"{source}: expected header was not found")
    if not saw_data or current_run_terminal_force is None:
        raise ValueError(f"{source}: final run {current_run} has no terminal row")
    terminal_forces.append(current_run_max_force)

    terminal_array = np.asarray(terminal_forces, dtype=float)
    if not np.all(np.isfinite(terminal_array)) or np.any(terminal_array <= 0):
        raise ValueError(f"{source}: every realization must have a positive rupture force")

    return FileEvents(
        force=np.asarray(forces, dtype=float),
        run_id=np.asarray(run_ids, dtype=np.int64),
        singleton_mass=np.asarray(singleton_masses, dtype=np.int64),
        collective_mass=np.asarray(collective_masses, dtype=np.int64),
        run_count=current_run + 1,
        terminal_forces=terminal_array,
    )


def _file_bin_statistics(
    events: FileEvents, *, bins: int, normalization: str
) -> tuple[np.ndarray, ...]:
    """Return sufficient statistics using the requested force normalization."""

    if normalization == "realization":
        normalized_force = events.force / events.terminal_forces[events.run_id]
        bin_edges = np.linspace(0.0, 1.0, bins + 1)
    elif normalization == "file":
        file_maximum_force = float(events.terminal_forces.max())
        normalized_force = events.force / file_maximum_force
        # pd.cut with an integer bin count extends the observed range slightly.
        # Deriving the edges from [0, 1] reproduces the exploratory notebook,
        # which included the zero-force rows before binning each fibril file.
        _, bin_edges = pd.cut(
            np.asarray([0.0, 1.0]),
            bins=bins,
            labels=False,
            include_lowest=True,
            retbins=True,
        )
    else:
        raise ValueError(f"unsupported normalization: {normalization}")
    if np.any(normalized_force < 0.0) or np.any(normalized_force > 1.0):
        raise ValueError("normalized force lies outside [0, 1]")
    bin_id = np.asarray(
        pd.cut(
            normalized_force,
            bins=bin_edges,
            labels=False,
            include_lowest=True,
        ),
        dtype=np.int64,
    )

    singleton = np.zeros((events.run_count, bins), dtype=np.int64)
    collective = np.zeros((events.run_count, bins), dtype=np.int64)
    np.add.at(singleton, (events.run_id, bin_id), events.singleton_mass)
    np.add.at(collective, (events.run_id, bin_id), events.collective_mass)

    total = singleton + collective
    active = total > 0
    collective_fraction = np.zeros_like(total, dtype=float)
    collective_fraction[active] = collective[active] / total[active]
    singleton_fraction = np.zeros_like(total, dtype=float)
    singleton_fraction[active] = singleton[active] / total[active]

    return (
        active.sum(axis=0, dtype=np.int64),
        singleton_fraction.sum(axis=0),
        np.square(singleton_fraction).sum(axis=0),
        collective_fraction.sum(axis=0),
        np.square(collective_fraction).sum(axis=0),
    )


def _sample_mean_std(
    count: np.ndarray, value_sum: np.ndarray, square_sum: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Calculate a mean and pandas-compatible sample standard deviation."""

    mean = np.divide(
        value_sum,
        count,
        out=np.zeros_like(value_sum, dtype=float),
        where=count > 0,
    )
    variance = np.divide(
        square_sum - np.divide(
            np.square(value_sum),
            count,
            out=np.zeros_like(value_sum, dtype=float),
            where=count > 0,
        ),
        count - 1,
        out=np.zeros_like(value_sum, dtype=float),
        where=count > 1,
    )
    return mean, np.sqrt(np.maximum(variance, 0.0))


def analyze_ts(
    input_root: Path,
    *,
    ts: int,
    bins: int = 30,
    normalization: str = "realization",
) -> CurveStatistics:
    """Analyze every available fibril file for one Ts value."""

    condition_root = input_root / f"ts_{ts}"
    if condition_root.is_dir():
        sources = sorted(condition_root.glob(f"ts_{ts}_seed_*_m_2.txt"))
    else:
        # Retain support for a flat directory so small fixtures and archived
        # data sets can be checked with the same analysis code.
        sources = sorted(input_root.glob(f"ts_{ts}_seed_*_m_2.txt"))
    if not sources:
        raise FileNotFoundError(
            f"no raw files match ts_{ts}_seed_*_m_2.txt in {input_root}"
        )

    count = np.zeros(bins, dtype=np.int64)
    singleton_sum = np.zeros(bins, dtype=float)
    singleton_square_sum = np.zeros(bins, dtype=float)
    collective_sum = np.zeros(bins, dtype=float)
    collective_square_sum = np.zeros(bins, dtype=float)
    run_count = 0

    for source in sources:
        events = parse_fibril_file(source)
        file_stats = _file_bin_statistics(
            events, bins=bins, normalization=normalization
        )
        count += file_stats[0]
        singleton_sum += file_stats[1]
        singleton_square_sum += file_stats[2]
        collective_sum += file_stats[3]
        collective_square_sum += file_stats[4]
        run_count += events.run_count

    mean_singleton, std_singleton = _sample_mean_std(
        count, singleton_sum, singleton_square_sum
    )
    mean_collective, std_collective = _sample_mean_std(
        count, collective_sum, collective_square_sum
    )
    edges = np.linspace(0.0, 1.0, bins + 1)
    midpoints = (edges[:-1] + edges[1:]) / 2.0
    return CurveStatistics(
        ts=ts,
        normalization=normalization,
        force_midpoint=midpoints,
        mean_singleton_fraction=mean_singleton,
        std_singleton_fraction=std_singleton,
        mean_collective_fraction=mean_collective,
        std_collective_fraction=std_collective,
        active_pairs=count,
        file_count=len(sources),
        run_count=run_count,
    )


def write_all_curves_csv(path: Path, curves: list[CurveStatistics]) -> None:
    """Write all means, standard deviations, and sample sizes in long form."""

    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            (
                "ts",
                "f_midpoint",
                "mean_singleton_fraction",
                "std_singleton_fraction",
                "mean_collective_fraction",
                "std_collective_fraction",
                "psi_percent",
                "psi_std_percent",
                "active_realization_bins",
                "fibril_files",
                "rupture_realizations",
            )
        )
        for curve in curves:
            for index, force in enumerate(curve.force_midpoint):
                writer.writerow(
                    (
                        curve.ts,
                        f"{force:.8f}",
                        f"{curve.mean_singleton_fraction[index]:.8f}",
                        f"{curve.std_singleton_fraction[index]:.8f}",
                        f"{curve.mean_collective_fraction[index]:.8f}",
                        f"{curve.std_collective_fraction[index]:.8f}",
                        f"{100.0 * curve.mean_collective_fraction[index]:.8f}",
                        f"{100.0 * curve.std_collective_fraction[index]:.8f}",
                        int(curve.active_pairs[index]),
                        curve.file_count,
                        curve.run_count,
                    )
                )


def write_xmgrace(path: Path, curves: list[CurveStatistics]) -> None:
    """Write multiple xmgrace XY sets separated by ampersands."""

    with path.open("w", encoding="utf-8") as stream:
        stream.write(f"# Figure 8: normalization = {curves[0].normalization}\n")
        stream.write("# Columns: F_n_midpoint  Psi_percent\n")
        stream.write("# Each data set is separated by '&'.\n")
        for curve_index, curve in enumerate(curves):
            stream.write(f"# Ts = {curve.ts}\n")
            for force, mean in zip(
                curve.force_midpoint,
                curve.mean_collective_fraction,
                strict=True,
            ):
                stream.write(f"{force:.8f} {100.0 * mean:.8f}\n")
            if curve_index != len(curves) - 1:
                stream.write("&\n")


def write_individual_dat(path: Path, curve: CurveStatistics) -> None:
    """Write one Ts curve as an xmgrace-friendly XY data set."""

    with path.open("w", encoding="utf-8") as stream:
        stream.write(f"# Ts = {curve.ts}\n")
        stream.write("# normalized_force_midpoint  Psi_percent\n")
        for force, mean in zip(
            curve.force_midpoint,
            curve.mean_collective_fraction,
            strict=True,
        ):
            stream.write(f"{force:.8f} {100.0 * mean:.8f}\n")


def plot_curves(path_stem: Path, curves: list[CurveStatistics]) -> None:
    """Plot Psi for every requested Ts value."""

    style = Path(__file__).with_name("xmgrace_paper.mplstyle")
    with plt.style.context(style):
        figure, axis = plt.subplots(figsize=(8.0, 6.0))
        colors = plt.cm.viridis(np.linspace(0.05, 0.95, len(curves)))
        for color, curve in zip(colors, curves, strict=True):
            axis.plot(
                curve.force_midpoint,
                100.0 * curve.mean_collective_fraction,
                marker="o",
                markersize=3.2,
                linewidth=1.2,
                color=color,
                label=rf"$T_s={curve.ts}$",
            )
        axis.set_xlim(0.0, 1.0)
        axis.set_ylim(0.0, 100.0)
        axis.set_xlabel(r"normalized force, $F_n$")
        axis.set_ylabel(r"clustered removed molecules, $\Psi$ (%)")
        axis.legend(ncol=2, fontsize=9, loc="upper left")
        figure.tight_layout()
        figure.savefig(path_stem.with_suffix(".pdf"))
        figure.savefig(path_stem.with_suffix(".png"), dpi=300)
        plt.close(figure)


def _parse_integer_list(value: str) -> tuple[int, ...]:
    try:
        values = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    except ValueError as error:
        raise argparse.ArgumentTypeError("expected comma-separated integers") from error
    if not values:
        raise argparse.ArgumentTypeError("at least one integer is required")
    return values


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-root",
        type=Path,
        default=Path("Data_fibrils/Avalanche_force_grouped/runs"),
        help="directory containing ts_<Ts>/ts_<Ts>_seed_*_m_2.txt files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("Reviews/Issue5_local_avalanche_reanalysis/figure_8"),
        help="directory for figures and tabular outputs",
    )
    parser.add_argument(
        "--ts",
        type=_parse_integer_list,
        default=DEFAULT_TS,
        help="comma-separated Ts values included in the all-curves figure",
    )
    parser.add_argument(
        "--selected-ts",
        type=_parse_integer_list,
        default=DEFAULT_SELECTED_TS,
        help="comma-separated Ts values exported to the xmgrace .dat file",
    )
    parser.add_argument("--bins", type=int, default=30)
    parser.add_argument(
        "--normalization",
        choices=("file", "realization"),
        default="realization",
        help="force normalization; 'realization' matches the manuscript",
    )
    return parser


def main() -> int:
    arguments = build_parser().parse_args()
    if arguments.bins <= 0:
        raise ValueError("--bins must be positive")
    missing_selected = set(arguments.selected_ts) - set(arguments.ts)
    if missing_selected:
        raise ValueError(
            "every --selected-ts value must also appear in --ts: "
            + ", ".join(str(value) for value in sorted(missing_selected))
        )

    arguments.output_dir.mkdir(parents=True, exist_ok=True)
    curves: list[CurveStatistics] = []
    for ts in arguments.ts:
        print(f"[Figure 8] processing Ts={ts}", flush=True)
        curve = analyze_ts(
            arguments.input_root,
            ts=ts,
            bins=arguments.bins,
            normalization=arguments.normalization,
        )
        curves.append(curve)
        print(
            f"[Figure 8] Ts={ts}: {curve.file_count} fibrils, "
            f"{curve.run_count} rupture realizations",
            flush=True,
        )

    write_all_curves_csv(arguments.output_dir / "figure_8_all_curves.csv", curves)
    plot_curves(arguments.output_dir / "figure_8_all_curves", curves)
    selected = [curve for curve in curves if curve.ts in arguments.selected_ts]
    selected.sort(key=lambda curve: arguments.selected_ts.index(curve.ts))
    write_xmgrace(arguments.output_dir / "figure_8_selected_xmgrace.dat", selected)
    for curve in curves:
        write_individual_dat(
            arguments.output_dir / f"figure_8_ts_{curve.ts}.dat", curve
        )
    print(f"[Figure 8] outputs written to {arguments.output_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

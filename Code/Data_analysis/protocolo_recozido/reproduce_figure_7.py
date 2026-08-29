#!/usr/bin/env python3
"""Reproduce the damage curves and phenomenological fits in Figure 7.

The analysis reads the new grouped fracture outputs.  For every rupture
realization and force, it retains the last state with at least one active
molecule and calculates the removed fraction relative to that realization's
initial molecule count.  Curves are conditional means over realizations that
have a preterminal state at the force.  Following the useful part of the
exploratory notebook, fits retain forces supported by at least 25% of all
rupture realizations.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


DEFAULT_TS = (2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192)
DEFAULT_SELECTED_TS = (8, 32, 128, 8192)
EXPECTED_HEADER = (
    "f,num_active_particles,num_deleted_particles,total_deleted_rods,"
    "avalanche_sizes"
)


@dataclass(frozen=True)
class DamageCurve:
    ts: int
    force: np.ndarray
    mean_percent: np.ndarray
    std_percent: np.ndarray
    realization_count: np.ndarray
    support_fraction: np.ndarray
    file_count: int
    total_realizations: int


@dataclass(frozen=True)
class DamageFit:
    ts: int
    alpha: float
    alpha_standard_error: float
    beta: float
    beta_standard_error: float
    r_squared: float
    force_max: float
    points: int


def damage_model(force: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    """Phenomenological interpolation used in the manuscript."""

    force = np.asarray(force, dtype=float)
    return 1.0e-3 * (np.expm1(beta * force) + np.power(force, alpha))


def _find_sources(input_root: Path, ts: int) -> list[Path]:
    condition_root = input_root / f"ts_{ts}"
    if condition_root.is_dir():
        sources = sorted(condition_root.glob(f"ts_{ts}_seed_*_m_2.txt"))
    else:
        sources = sorted(input_root.glob(f"ts_{ts}_seed_*_m_2.txt"))
    if not sources:
        raise FileNotFoundError(
            f"no raw files match ts_{ts}_seed_*_m_2.txt below {input_root}"
        )
    return sources


def _finish_run(
    *,
    source: Path,
    run_id: int,
    initial_particles: int | None,
    terminal_seen: bool,
    active_by_force: dict[float, int],
    damage_by_force: dict[float, list[float]],
) -> None:
    if initial_particles is None:
        raise ValueError(f"{source}: run {run_id} is empty")
    if not terminal_seen:
        raise ValueError(f"{source}: run {run_id} has no terminal row")
    for force, active_particles in active_by_force.items():
        damage_by_force[force].append(
            100.0 * (initial_particles - active_particles) / initial_particles
        )


def parse_damage_file(source: Path) -> tuple[dict[float, list[float]], int]:
    """Return one preterminal damage value per run and force."""

    damage_by_force: dict[float, list[float]] = defaultdict(list)
    active_by_force: dict[float, int] = {}
    run_id = 0
    initial_particles: int | None = None
    terminal_seen = False
    saw_header = False

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
                _finish_run(
                    source=source,
                    run_id=run_id,
                    initial_particles=initial_particles,
                    terminal_seen=terminal_seen,
                    active_by_force=active_by_force,
                    damage_by_force=damage_by_force,
                )
                run_id += 1
                initial_particles = None
                terminal_seen = False
                active_by_force = {}
                continue
            if not saw_header:
                raise ValueError(f"{source}:{line_number}: data precede header")
            if terminal_seen:
                raise ValueError(
                    f"{source}:{line_number}: data found after terminal row in run {run_id}"
                )

            fields = next(csv.reader([line]))
            if len(fields) != 5:
                raise ValueError(
                    f"{source}:{line_number}: expected 5 fields, found {len(fields)}"
                )
            try:
                force = float(fields[0])
                active_particles = int(fields[1])
                deleted_particles = int(fields[2])
            except ValueError as error:
                raise ValueError(
                    f"{source}:{line_number}: malformed numeric field"
                ) from error
            if not np.isfinite(force) or force < 0:
                raise ValueError(f"{source}:{line_number}: invalid force {force}")
            if active_particles < 0 or deleted_particles < 0:
                raise ValueError(f"{source}:{line_number}: negative particle count")

            if initial_particles is None:
                initial_particles = active_particles + deleted_particles
                if force != 0.0 or deleted_particles != 0 or initial_particles <= 0:
                    raise ValueError(
                        f"{source}:{line_number}: run {run_id} has invalid initial row"
                    )
            if active_particles + deleted_particles != initial_particles:
                raise ValueError(
                    f"{source}:{line_number}: active plus deleted particles changed "
                    f"within run {run_id}"
                )

            if active_particles == 0:
                terminal_seen = True
            else:
                # Repeated rows at a force are successive damage-relaxation
                # substeps. The last active row is the state immediately before
                # advancing the force or losing the load path.
                active_by_force[force] = active_particles

    if not saw_header:
        raise ValueError(f"{source}: expected header was not found")
    _finish_run(
        source=source,
        run_id=run_id,
        initial_particles=initial_particles,
        terminal_seen=terminal_seen,
        active_by_force=active_by_force,
        damage_by_force=damage_by_force,
    )
    return damage_by_force, run_id + 1


def analyze_ts(
    input_root: Path, *, ts: int, minimum_support: float = 0.25
) -> DamageCurve:
    """Build a support-filtered mean damage curve for one Ts."""

    if not 0.0 < minimum_support <= 1.0:
        raise ValueError("minimum_support must lie in (0, 1]")
    sources = _find_sources(input_root, ts)
    combined: dict[float, list[float]] = defaultdict(list)
    total_realizations = 0
    for source in sources:
        file_damage, run_count = parse_damage_file(source)
        total_realizations += run_count
        for force, damage in file_damage.items():
            combined[force].extend(damage)

    forces: list[float] = []
    means: list[float] = []
    standard_deviations: list[float] = []
    counts: list[int] = []
    support: list[float] = []
    for force in sorted(combined):
        values = np.asarray(combined[force], dtype=float)
        force_support = values.size / total_realizations
        if force_support < minimum_support:
            continue
        forces.append(force)
        means.append(float(values.mean()))
        standard_deviations.append(
            float(values.std(ddof=1)) if values.size > 1 else 0.0
        )
        counts.append(int(values.size))
        support.append(float(force_support))

    return DamageCurve(
        ts=ts,
        force=np.asarray(forces, dtype=float),
        mean_percent=np.asarray(means, dtype=float),
        std_percent=np.asarray(standard_deviations, dtype=float),
        realization_count=np.asarray(counts, dtype=np.int64),
        support_fraction=np.asarray(support, dtype=float),
        file_count=len(sources),
        total_realizations=total_realizations,
    )


def fit_damage_curve(curve: DamageCurve) -> DamageFit:
    """Fit alpha and beta by unweighted nonlinear least squares."""

    parameters, covariance = curve_fit(
        damage_model,
        curve.force,
        curve.mean_percent,
        p0=(2.0, 0.06),
        bounds=((0.5, 0.0), (4.0, 0.5)),
        maxfev=100_000,
    )
    alpha, beta = (float(value) for value in parameters)
    standard_errors = np.sqrt(np.diag(covariance))
    fitted = damage_model(curve.force, alpha, beta)
    residual_sum = float(np.square(curve.mean_percent - fitted).sum())
    total_sum = float(
        np.square(curve.mean_percent - curve.mean_percent.mean()).sum()
    )
    r_squared = 1.0 - residual_sum / total_sum if total_sum > 0.0 else np.nan
    return DamageFit(
        ts=curve.ts,
        alpha=alpha,
        alpha_standard_error=float(standard_errors[0]),
        beta=beta,
        beta_standard_error=float(standard_errors[1]),
        r_squared=r_squared,
        force_max=float(curve.force.max()),
        points=curve.force.size,
    )


def write_curves(path: Path, curves: list[DamageCurve]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            (
                "ts",
                "force",
                "mean_removed_percent",
                "std_removed_percent",
                "realization_count",
                "support_fraction",
                "fibril_files",
                "total_realizations",
            )
        )
        for curve in curves:
            for values in zip(
                curve.force,
                curve.mean_percent,
                curve.std_percent,
                curve.realization_count,
                curve.support_fraction,
                strict=True,
            ):
                force, mean, std, count, support = values
                writer.writerow(
                    (
                        curve.ts,
                        f"{force:.8f}",
                        f"{mean:.8f}",
                        f"{std:.8f}",
                        int(count),
                        f"{support:.8f}",
                        curve.file_count,
                        curve.total_realizations,
                    )
                )


def write_fits(path: Path, fits: list[DamageFit]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            (
                "ts",
                "ln_ts",
                "log10_ts",
                "alpha",
                "alpha_standard_error",
                "beta",
                "beta_standard_error",
                "r_squared",
                "force_max",
                "curve_points",
            )
        )
        for fit in fits:
            writer.writerow(
                (
                    fit.ts,
                    f"{np.log(fit.ts):.8f}",
                    f"{np.log10(fit.ts):.8f}",
                    f"{fit.alpha:.8f}",
                    f"{fit.alpha_standard_error:.8f}",
                    f"{fit.beta:.8f}",
                    f"{fit.beta_standard_error:.8f}",
                    f"{fit.r_squared:.8f}",
                    f"{fit.force_max:.8f}",
                    fit.points,
                )
            )


def write_xmgrace(
    path: Path, curves: list[DamageCurve], fits_by_ts: dict[int, DamageFit]
) -> None:
    """Write data and fitted curves as alternating xmgrace XY sets."""

    with path.open("w", encoding="utf-8") as stream:
        stream.write("# Figure 7a; alternating data and fit XY sets\n")
        stream.write("# Data columns: F  mean_removed_percent\n")
        for set_index, curve in enumerate(curves):
            fit = fits_by_ts[curve.ts]
            stream.write(f"# Ts = {curve.ts}; data\n")
            for force, damage in zip(curve.force, curve.mean_percent, strict=True):
                stream.write(f"{force:.8f} {damage:.8f}\n")
            stream.write("&\n")
            stream.write(f"# Ts = {curve.ts}; fit\n")
            fit_force = np.linspace(0.0, curve.force.max(), 500)
            fit_damage = damage_model(fit_force, fit.alpha, fit.beta)
            for force, damage in zip(fit_force, fit_damage, strict=True):
                stream.write(f"{force:.8f} {damage:.8f}\n")
            if set_index != len(curves) - 1:
                stream.write("&\n")


def plot_figure(
    path_stem: Path,
    curves: list[DamageCurve],
    fits: list[DamageFit],
    selected_ts: tuple[int, ...],
) -> None:
    style = Path(__file__).with_name("xmgrace_paper.mplstyle")
    curves_by_ts = {curve.ts: curve for curve in curves}
    fits_by_ts = {fit.ts: fit for fit in fits}
    colors = {8: "#6f2dbd", 32: "#008000", 128: "#0000ff", 8192: "#ff1f0f"}
    markers = {8: "o", 32: "s", 128: "D", 8192: "v"}

    with plt.style.context(style):
        figure = plt.figure(figsize=(12.0, 5.2), layout="constrained")
        grid = figure.add_gridspec(2, 2, width_ratios=(1.15, 1.0), hspace=0.14)
        damage_axis = figure.add_subplot(grid[:, 0])
        beta_axis = figure.add_subplot(grid[0, 1])
        alpha_axis = figure.add_subplot(grid[1, 1], sharex=beta_axis)

        for ts in selected_ts:
            curve = curves_by_ts[ts]
            fit = fits_by_ts[ts]
            color = colors.get(ts)
            damage_axis.plot(
                curve.force,
                curve.mean_percent,
                linestyle="none",
                marker=markers.get(ts, "o"),
                markersize=3.2,
                color=color,
                label=rf"$T_s={ts}$",
            )
            fit_force = np.linspace(0.0, curve.force.max(), 500)
            damage_axis.plot(
                fit_force,
                damage_model(fit_force, fit.alpha, fit.beta),
                color="black",
                linewidth=1.4,
            )
        damage_axis.set_xlabel(r"applied force, $F$")
        damage_axis.set_ylabel(r"removed molecules, $\varphi$ (%)")
        damage_axis.set_ylim(bottom=0.0)
        damage_axis.legend(fontsize=9, loc="upper left")
        damage_axis.text(0.96, 0.95, "(a)", transform=damage_axis.transAxes, ha="right", va="top")

        parameter_fits = [fit for fit in fits if fit.ts >= min(selected_ts)]
        log_ts = np.asarray([np.log(fit.ts) for fit in parameter_fits])
        beta = np.asarray([fit.beta for fit in parameter_fits])
        alpha = np.asarray([fit.alpha for fit in parameter_fits])
        beta_axis.plot(log_ts, beta, "o-", color="red")
        alpha_axis.plot(log_ts, alpha, "s-", color="blue")
        beta_axis.set_ylabel(r"$\beta$", rotation=0, labelpad=14)
        alpha_axis.set_ylabel(r"$\alpha$", rotation=0, labelpad=14)
        alpha_axis.set_xlabel(r"$\ln T_s$")
        beta_axis.tick_params(labelbottom=False)
        beta_axis.text(0.04, 0.88, "(b)", transform=beta_axis.transAxes)
        alpha_axis.text(0.04, 0.88, "(c)", transform=alpha_axis.transAxes)
        figure.savefig(path_stem.with_suffix(".pdf"))
        figure.savefig(path_stem.with_suffix(".png"), dpi=300)
        plt.close(figure)


def _parse_integer_list(value: str) -> tuple[int, ...]:
    try:
        parsed = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    except ValueError as error:
        raise argparse.ArgumentTypeError("expected comma-separated integers") from error
    if not parsed:
        raise argparse.ArgumentTypeError("at least one integer is required")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-root",
        type=Path,
        default=Path("Data_fibrils/Avalanche_force_grouped/runs"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("Reviews/Issue5_local_avalanche_reanalysis/figure_7"),
    )
    parser.add_argument("--ts", type=_parse_integer_list, default=DEFAULT_TS)
    parser.add_argument(
        "--selected-ts", type=_parse_integer_list, default=DEFAULT_SELECTED_TS
    )
    parser.add_argument("--minimum-support", type=float, default=0.25)
    return parser


def write_readme(path: Path) -> None:
    path.write_text(
        """# Figure 7 reproduction

This directory contains the damage curves and phenomenological fits generated
from `Data_fibrils/Avalanche_force_grouped/runs`.

For each rupture realization and force, the analysis retains the last state
with `num_active_particles > 0` and calculates the removed percentage relative
to that realization's initial particle count. The terminal zero-particle row
is excluded. Means are calculated with one value per realization and force;
forces represented by fewer than 25% of the realizations are omitted.

The curves are fitted by unweighted nonlinear least squares to

`f(F) = 1e-3 [exp(beta F) - 1 + F^alpha]`.

The right-hand panels use `ln(Ts)`. The published Figure 7 labels this axis as
`log10(Ts)`, although its numerical range corresponds to the natural logarithm.

Regenerate from the repository root with:

```bash
python3 Code/Data_analysis/reproduce_figure_7.py
```
""",
        encoding="utf-8",
    )


def main() -> int:
    arguments = build_parser().parse_args()
    if set(arguments.selected_ts) - set(arguments.ts):
        raise ValueError("every selected Ts must also be included in --ts")
    arguments.output_dir.mkdir(parents=True, exist_ok=True)

    curves: list[DamageCurve] = []
    fits: list[DamageFit] = []
    for ts in arguments.ts:
        print(f"[Figure 7] processing Ts={ts}", flush=True)
        curve = analyze_ts(
            arguments.input_root,
            ts=ts,
            minimum_support=arguments.minimum_support,
        )
        fit = fit_damage_curve(curve)
        curves.append(curve)
        fits.append(fit)
        print(
            f"[Figure 7] Ts={ts}: {curve.file_count} fibrils, "
            f"{curve.total_realizations} realizations, alpha={fit.alpha:.5g}, "
            f"beta={fit.beta:.5g}, R2={fit.r_squared:.5f}",
            flush=True,
        )

    write_curves(arguments.output_dir / "figure_7_damage_curves.csv", curves)
    write_fits(arguments.output_dir / "figure_7_fit_parameters.csv", fits)
    selected_curves = [
        next(curve for curve in curves if curve.ts == ts)
        for ts in arguments.selected_ts
    ]
    fits_by_ts = {fit.ts: fit for fit in fits}
    write_xmgrace(
        arguments.output_dir / "figure_7a_selected_xmgrace.dat",
        selected_curves,
        fits_by_ts,
    )
    plot_figure(
        arguments.output_dir / "figure_7_reproduced",
        curves,
        fits,
        arguments.selected_ts,
    )
    write_readme(arguments.output_dir / "README.md")
    print(f"[Figure 7] outputs written to {arguments.output_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

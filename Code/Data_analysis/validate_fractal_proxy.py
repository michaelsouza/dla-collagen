#!/usr/bin/env python3
"""Validate cross-sectional mass-radius D_f against 3D backbone descriptors.

The published D_f values were obtained from ensemble-averaged mass-radius
curves using 11 cross-sections per fibril.  The xmgrace project records the
condition-specific radial window used for each linear fit.  This script:

1. reconstructs and validates those published fits;
2. applies the same radial window to each fibril in a condition;
3. extracts the trunk and backbone using the rupture-model implementation;
4. writes one row of structural descriptors per independent fibril.

The compact input files are read directly.  Rods are expanded in memory over
18 lattice layers, which is equivalent to the project's extend_molecules
notebook but avoids reading the much larger expanded files.
"""

from __future__ import annotations

import argparse
import importlib.util
import io
import math
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, TextIO
from zipfile import ZipFile

import numpy as np
import pandas as pd
from scipy.stats import linregress


TS_ORDER = (2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192)
SECTION_Y = np.arange(-90, 91, 18, dtype=int)
TRUNK_Y_MIN = -100
TRUNK_Y_MAX = 100
TRUNK_HALF_WIDTH = 8
ROD_LENGTH = 18
FILENAME_RE = re.compile(r"_ts_(\d+).*?_seed_(\d+)")


@dataclass(frozen=True)
class FitSpec:
    ts: int
    log_r: np.ndarray
    log_m: np.ndarray
    fit_count: int
    published_df: float
    published_fit_error: float

    @property
    def radii(self) -> np.ndarray:
        return np.power(10.0, self.log_r)

    @property
    def fit_r_max(self) -> float:
        return float(self.radii[self.fit_count - 1])


def load_fracture_module(repo_root: Path):
    module_path = repo_root / "Code" / "Fracture_fibril" / "stress_strain_ava.py"
    spec = importlib.util.spec_from_file_location("stress_strain_ava", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load rupture implementation: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_grace_xy_datasets(path: Path) -> dict[int, np.ndarray]:
    """Return x-y datasets keyed by the S index in an xmgrace project."""
    datasets: dict[int, list[tuple[float, float]]] = {}
    current: int | None = None

    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if line.startswith("@target"):
                match = re.search(r"\.S(\d+)$", line)
                current = int(match.group(1)) if match else None
                if current is not None:
                    datasets.setdefault(current, [])
                continue
            if line == "&":
                current = None
                continue
            if current is None or not line or line.startswith("@"):
                continue
            fields = line.split()
            if len(fields) < 2:
                continue
            try:
                datasets[current].append((float(fields[0]), float(fields[1])))
            except ValueError:
                continue

    return {
        index: np.asarray(values, dtype=float)
        for index, values in datasets.items()
        if values
    }


def load_published_df(path: Path) -> dict[int, tuple[float, float]]:
    table = np.loadtxt(path, dtype=float)
    if table.ndim == 1:
        table = table.reshape(1, -1)
    return {
        int(row[0]): (float(row[1]), float(row[2]))
        for row in table
    }


def build_fit_specs(grace_path: Path, published_path: Path) -> dict[int, FitSpec]:
    datasets = parse_grace_xy_datasets(grace_path)
    published = load_published_df(published_path)
    specs: dict[int, FitSpec] = {}

    for position, ts in enumerate(TS_ORDER):
        data_index = 2 * position
        fit_index = data_index + 1
        if data_index not in datasets or fit_index not in datasets:
            raise ValueError(
                f"Missing xmgrace datasets S{data_index}/S{fit_index} for Ts={ts}"
            )
        curve = datasets[data_index]
        fitted_line = datasets[fit_index]
        fit_count = len(fitted_line)
        if fit_count < 3 or fit_count > len(curve):
            raise ValueError(f"Invalid fit window for Ts={ts}: {fit_count}")
        if not np.allclose(
            curve[:fit_count, 0],
            fitted_line[:, 0],
            rtol=0.0,
            atol=1e-6,
        ):
            raise ValueError(f"xmgrace fit x values do not match curve for Ts={ts}")
        if ts not in published:
            raise ValueError(f"Ts={ts} is absent from {published_path}")

        published_df, published_error = published[ts]
        specs[ts] = FitSpec(
            ts=ts,
            log_r=curve[:, 0].copy(),
            log_m=curve[:, 1].copy(),
            fit_count=fit_count,
            published_df=published_df,
            published_fit_error=published_error,
        )

    return specs


def validate_published_fits(specs: dict[int, FitSpec]) -> pd.DataFrame:
    rows = []
    for ts in TS_ORDER:
        spec = specs[ts]
        fit = linregress(
            spec.log_r[: spec.fit_count],
            spec.log_m[: spec.fit_count],
        )
        rows.append(
            {
                "ts": ts,
                "fit_count": spec.fit_count,
                "fit_r_min": float(spec.radii[0]),
                "fit_r_max": spec.fit_r_max,
                "reconstructed_df": float(fit.slope),
                "published_df": spec.published_df,
                "df_difference": float(fit.slope - spec.published_df),
                "reconstructed_fit_error": float(fit.stderr),
                "published_fit_error": spec.published_fit_error,
                "r_squared": float(fit.rvalue**2),
            }
        )
    return pd.DataFrame(rows)


def efficient_create_neighs(ssd) -> None:
    """Populate the rupture-model neighbor sets without all-pairs searches."""
    offsets = ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))

    for layer in ssd.layers.values():
        by_position: dict[tuple[int, int], list[int]] = {}
        for pid in layer.pids:
            particle = ssd.particles[pid]
            key = (int(particle.xz[0]), int(particle.xz[1]))
            by_position.setdefault(key, []).append(pid)

        for pid_a in layer.pids:
            particle_a = ssd.particles[pid_a]
            x, z = int(particle_a.xz[0]), int(particle_a.xz[1])
            for dx, dz in offsets:
                for pid_b in by_position.get((x + dx, z + dz), ()):
                    if pid_b <= pid_a:
                        continue
                    particle_b = ssd.particles[pid_b]
                    particle_a.add_neigh_rid(particle_b.rid)
                    particle_b.add_neigh_rid(particle_a.rid)


def section_index_for_rod(y0: int) -> int | None:
    """Return the one sampled section intersected by a length-18 rod."""
    index = math.ceil((y0 - int(SECTION_Y[0])) / 18)
    if index < 0 or index >= len(SECTION_Y):
        return None
    y_section = int(SECTION_Y[index])
    if y0 <= y_section <= y0 + ROD_LENGTH - 1:
        return index
    return None


def iter_compact_rows(handle: TextIO, source: str):
    for line_number, line in enumerate(handle, start=1):
        fields = line.split()
        if len(fields) != 5 or fields[0] != "uid:":
            continue
        try:
            yield (
                int(fields[1]),
                int(fields[2]),
                int(fields[3]),
                int(fields[4]),
            )
        except ValueError as exc:
            raise ValueError(f"Malformed row {source}:{line_number}") from exc


def parse_grown_sections(path: Path) -> list[np.ndarray]:
    """Read the 11 sampled sections of one laterally grown fibril."""
    sections: list[list[tuple[int, int]]] = [[] for _ in SECTION_Y]

    with path.open("r", encoding="utf-8") as handle:
        for _rid, x, y0, z in iter_compact_rows(handle, str(path)):
            section_index = section_index_for_rod(y0)
            if section_index is not None:
                sections[section_index].append((x, z))

    missing_sections = [
        int(y) for y, section in zip(SECTION_Y, sections) if not section
    ]
    if missing_sections:
        raise ValueError(f"Empty sampled sections in {path}: {missing_sections}")
    return [np.asarray(section, dtype=float) for section in sections]


def build_original_trunk(
    handle: TextIO,
    source: str,
    fracture_module,
):
    """Construct the rupture-model trunk from one original compact fibril."""
    ssd = fracture_module.StressStrainData()
    pid = 0

    for rid, x, y0, z in iter_compact_rows(handle, source):
        if abs(x) > TRUNK_HALF_WIDTH or abs(z) > TRUNK_HALF_WIDTH:
            continue
        y_start = max(y0, TRUNK_Y_MIN)
        y_stop = min(y0 + ROD_LENGTH - 1, TRUNK_Y_MAX)
        if y_start > y_stop:
            continue

        if rid not in ssd.rods:
            ssd.rods[rid] = fracture_module.Rod(ssd, rid)

        for y in range(y_start, y_stop + 1):
            particle = fracture_module.Particle(
                ssd=ssd,
                pid=pid,
                rid=rid,
                lid=y,
                xz=np.asarray([x, z], dtype=float),
            )
            ssd.particles[pid] = particle
            ssd.rods[rid].add_pid(pid)
            if y not in ssd.layers:
                ssd.layers[y] = fracture_module.Layer(y)
            ssd.layers[y].add_pid(pid)
            pid += 1

    if not ssd.layers:
        raise ValueError(f"No trunk particles in {source}")

    ssd.lid_min = min(ssd.layers)
    ssd.lid_max = max(ssd.layers)
    if ssd.lid_min != TRUNK_Y_MIN or ssd.lid_max != TRUNK_Y_MAX:
        raise ValueError(
            f"Trunk in {source} spans [{ssd.lid_min}, {ssd.lid_max}], "
            f"expected [{TRUNK_Y_MIN}, {TRUNK_Y_MAX}]"
        )

    efficient_create_neighs(ssd)
    return ssd


def mass_radius_for_sections(
    sections: Iterable[np.ndarray],
    radii: np.ndarray,
) -> tuple[np.ndarray, dict[str, float]]:
    masses = []
    occupancies = []
    max_radii = []
    packing_fractions = []

    for coordinates in sections:
        center = np.mean(coordinates, axis=0)
        distances = np.sqrt(np.sum((coordinates - center) ** 2, axis=1))
        distances.sort()
        mass = np.searchsorted(distances, radii, side="right").astype(float)
        masses.append(mass)
        occupancies.append(float(len(coordinates)))
        max_radius = float(distances[-1])
        max_radii.append(max_radius)
        packing_fractions.append(
            float(len(coordinates) / (math.pi * max_radius**2))
            if max_radius > 0
            else float("nan")
        )

    occupancies_array = np.asarray(occupancies, dtype=float)
    descriptors = {
        "full_mean_n_11": float(np.mean(occupancies_array)),
        "full_min_n_11": float(np.min(occupancies_array)),
        "full_cv_n_11": float(
            np.std(occupancies_array, ddof=1) / np.mean(occupancies_array)
        ),
        "full_mean_radius_11": float(np.mean(max_radii)),
        "full_mean_packing_fraction_11": float(np.nanmean(packing_fractions)),
    }
    return np.mean(np.vstack(masses), axis=0), descriptors


def fit_individual_df(mean_mass: np.ndarray, spec: FitSpec) -> dict[str, float]:
    if np.any(mean_mass[: spec.fit_count] <= 0):
        raise ValueError(f"Non-positive mass in fit window for Ts={spec.ts}")
    log_mass = np.log10(mean_mass)
    fit = linregress(
        spec.log_r[: spec.fit_count],
        log_mass[: spec.fit_count],
    )
    return {
        "df": float(fit.slope),
        "df_fit_error": float(fit.stderr),
        "df_fit_r_squared": float(fit.rvalue**2),
    }


def backbone_descriptors(ssd) -> dict[str, float]:
    initial_rods = len(ssd.rods)
    initial_particles = ssd.num_active_particles()

    ssd.filter_rids(reverse=False)
    ssd.filter_rids(reverse=True)

    layer_counts = np.asarray(
        [ssd.layers[y].len() for y in range(TRUNK_Y_MIN, TRUNK_Y_MAX + 1)],
        dtype=float,
    )
    if np.any(layer_counts <= 0):
        raise ValueError("Backbone has an empty layer after extraction")

    coordination = np.asarray(
        [len(rod.neigh_pids) for rod in ssd.rods.values()],
        dtype=float,
    )
    unit_stresses = []
    for rod in ssd.rods.values():
        rod_layer_counts = np.asarray(
            [
                ssd.layers[ssd.particles[pid].lid].len()
                for pid in rod.pids
                if pid in ssd.particles
            ],
            dtype=float,
        )
        if len(rod_layer_counts):
            unit_stresses.append(float(np.mean(1.0 / rod_layer_counts)))

    return {
        "trunk_initial_rods": float(initial_rods),
        "trunk_initial_particles": float(initial_particles),
        "backbone_rods": float(len(ssd.rods)),
        "backbone_particles": float(ssd.num_active_particles()),
        "backbone_rod_fraction": float(len(ssd.rods) / initial_rods),
        "backbone_particle_fraction": float(
            ssd.num_active_particles() / initial_particles
        ),
        "backbone_mean_n_201": float(np.mean(layer_counts)),
        "backbone_min_n_201": float(np.min(layer_counts)),
        "backbone_cv_n_201": float(
            np.std(layer_counts, ddof=1) / np.mean(layer_counts)
        ),
        "backbone_mean_coordination": float(np.mean(coordination)),
        "backbone_min_coordination": float(np.min(coordination)),
        "backbone_mean_unit_stress": float(np.mean(unit_stresses)),
        "backbone_max_unit_stress": float(np.max(unit_stresses)),
    }


def list_grown_files(input_dir: Path, limit_per_ts: int | None):
    grouped: dict[int, list[tuple[int, Path]]] = {ts: [] for ts in TS_ORDER}
    for path in sorted(input_dir.glob("*.dat")):
        match = FILENAME_RE.search(path.name)
        if not match:
            continue
        ts, seed = int(match.group(1)), int(match.group(2))
        if ts in grouped:
            grouped[ts].append((seed, path))

    if limit_per_ts is not None:
        grouped = {
            ts: values[:limit_per_ts]
            for ts, values in grouped.items()
        }

    missing = [ts for ts, values in grouped.items() if not values]
    if missing:
        raise ValueError(f"No compact fibrils found for Ts={missing}")
    return grouped


def index_original_zip(zip_path: Path) -> dict[tuple[int, int], str]:
    entries: dict[tuple[int, int], str] = {}
    with ZipFile(zip_path) as archive:
        for name in archive.namelist():
            if not name.endswith(".dat"):
                continue
            match = FILENAME_RE.search(name)
            if not match:
                continue
            key = (int(match.group(1)), int(match.group(2)))
            if key in entries:
                raise ValueError(f"Duplicate original fibril for {key} in {zip_path}")
            entries[key] = name
    return entries


def analyze_fibrils(
    grouped_files,
    original_zip_path: Path,
    original_entries: dict[tuple[int, int], str],
    specs: dict[int, FitSpec],
    fracture_module,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    ensemble_rows = []

    with ZipFile(original_zip_path) as original_archive:
        for ts in TS_ORDER:
            files = grouped_files[ts]
            spec = specs[ts]
            ensemble_mass_sum = np.zeros_like(spec.log_r, dtype=float)
            section_count = 0
            started = time.monotonic()

            for index, (seed, grown_path) in enumerate(files, start=1):
                original_key = (ts, seed)
                if original_key not in original_entries:
                    raise ValueError(
                        f"No original mechanical fibril paired with {grown_path}"
                    )
                original_entry = original_entries[original_key]

                sections = parse_grown_sections(grown_path)
                with original_archive.open(original_entry, "r") as binary_handle:
                    with io.TextIOWrapper(
                        binary_handle,
                        encoding="utf-8",
                    ) as text_handle:
                        ssd = build_original_trunk(
                            text_handle,
                            f"{original_zip_path}:{original_entry}",
                            fracture_module,
                        )

                mean_mass, full_descriptors = mass_radius_for_sections(
                    sections,
                    spec.radii,
                )
                df_result = fit_individual_df(mean_mass, spec)
                mechanical_descriptors = backbone_descriptors(ssd)

                row = {
                    "ts": ts,
                    "seed": seed,
                    "grown_source_file": str(grown_path),
                    "original_source_archive": str(original_zip_path),
                    "original_source_entry": original_entry,
                    **df_result,
                    **full_descriptors,
                    **mechanical_descriptors,
                }
                rows.append(row)

                ensemble_mass_sum += mean_mass * len(sections)
                section_count += len(sections)

                if index == len(files) or index % 10 == 0:
                    elapsed = time.monotonic() - started
                    print(
                        f"Ts={ts:<5} {index:>2}/{len(files)} paired fibrils "
                        f"({elapsed:.1f} s)",
                        flush=True,
                    )

            ensemble_mean_mass = ensemble_mass_sum / section_count
            ensemble_fit = fit_individual_df(ensemble_mean_mass, spec)
            recomputed_log_mass = np.log10(ensemble_mean_mass)
            ensemble_rows.append(
                {
                    "ts": ts,
                    "fibrils": len(files),
                    "sections": section_count,
                    "recomputed_df": ensemble_fit["df"],
                    "recomputed_fit_error": ensemble_fit["df_fit_error"],
                    "recomputed_r_squared": ensemble_fit["df_fit_r_squared"],
                    "published_df": spec.published_df,
                    "published_fit_error": spec.published_fit_error,
                    "df_difference": ensemble_fit["df"] - spec.published_df,
                    "max_abs_log_mass_difference": float(
                        np.max(np.abs(recomputed_log_mass - spec.log_m))
                    ),
                }
            )

    return pd.DataFrame(rows), pd.DataFrame(ensemble_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--grown-input-dir",
        type=Path,
        required=True,
        help="Compact laterally grown fibrils used for the mass-radius analysis.",
    )
    parser.add_argument(
        "--original-zip",
        type=Path,
        required=True,
        help="Archive of original fibrils used by the rupture model.",
    )
    parser.add_argument("--grace-file", type=Path, required=True)
    parser.add_argument("--published-df", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--limit-per-ts",
        type=int,
        default=None,
        help="Process only the first N fibrils per Ts (pilot/debugging).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    fracture_module = load_fracture_module(repo_root)

    specs = build_fit_specs(args.grace_file, args.published_df)
    fit_validation = validate_published_fits(specs)
    max_slope_difference = fit_validation["df_difference"].abs().max()
    # df_ts.dat mixes two- and three-decimal reporting, so values recorded
    # with two decimals can differ from the reconstructed slope by up to 0.005.
    if max_slope_difference > 6e-3:
        raise RuntimeError(
            "Reconstructed xmgrace slopes do not match published values: "
            f"max difference={max_slope_difference:.6g}"
        )

    grouped_files = list_grown_files(args.grown_input_dir, args.limit_per_ts)
    original_entries = index_original_zip(args.original_zip)
    grown_keys = {
        (ts, seed)
        for ts, files in grouped_files.items()
        for seed, _path in files
    }
    missing_originals = sorted(grown_keys - original_entries.keys())
    if missing_originals:
        raise RuntimeError(
            "Laterally grown fibrils without paired originals: "
            f"{missing_originals[:10]}"
        )
    per_fibril, ensemble_validation = analyze_fibrils(
        grouped_files,
        args.original_zip,
        original_entries,
        specs,
        fracture_module,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    fit_validation.to_csv(
        args.output_dir / "published_fit_validation.csv",
        index=False,
    )
    per_fibril.to_csv(
        args.output_dir / "fractal_proxy_per_fibril.csv",
        index=False,
    )
    ensemble_validation.to_csv(
        args.output_dir / "ensemble_curve_validation.csv",
        index=False,
    )

    print(f"Wrote results to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

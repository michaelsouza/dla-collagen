"""Independent input-data audit for Issue 14.

The raw rupture files are streamed directly.  The resulting histograms retain
the accepted definition: each positive hyphen-separated connected component is
one event; rows with ``num_active_particles == 0`` are terminal rows.
"""

from __future__ import annotations

import csv
import json
import re
from fractions import Fraction
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path

import numpy as np


RAW_FILE_RE = re.compile(r"^ts_(?P<ts>\d+)_seed_(?P<seed>\d+)_m_(?P<m>\d+)\.txt$")
PMF_FILE_RE = re.compile(
    r"^local_avalanches_Ts_(?P<ts>\d+)_(?P<population>com|sem)_terminal\.dat$"
)


@dataclass(frozen=True)
class RawFileAudit:
    path: str
    ts: int
    fibril_seed: int
    weibull_m: int
    runs: int
    terminal_rows: int
    all_counts: dict[int, int]
    preterminal_counts: dict[int, int]


def _parse_sizes(raw: bytes) -> tuple[int, ...]:
    value = raw.strip().strip(b'"')
    if not value or value == b"0":
        return ()
    sizes = tuple(int(part) for part in value.split(b"-"))
    if any(size <= 0 for size in sizes):
        raise ValueError(f"invalid nonpositive local size in {raw!r}")
    return sizes


def audit_raw_file(path: Path) -> RawFileAudit:
    match = RAW_FILE_RE.match(path.name)
    if match is None:
        raise ValueError(f"unexpected raw filename: {path.name}")
    all_counts: Counter[int] = Counter()
    preterminal_counts: Counter[int] = Counter()
    separators = 0
    data_rows = 0
    terminal_rows = 0
    with path.open("rb") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line or line.startswith(b"f,num_active_particles"):
                continue
            if line.startswith(b"-"):
                separators += 1
                continue
            parts = line.rstrip(b"\r\n").split(b",", 4)
            if len(parts) != 5:
                raise ValueError(f"{path}:{line_number}: expected five CSV fields")
            try:
                active = int(parts[1])
                total_deleted = int(parts[3])
                sizes = _parse_sizes(parts[4])
            except ValueError as error:
                raise ValueError(f"{path}:{line_number}: invalid rupture row") from error
            if sum(sizes) != total_deleted:
                raise ValueError(
                    f"{path}:{line_number}: component sum {sum(sizes)} != {total_deleted}"
                )
            data_rows += 1
            all_counts.update(sizes)
            if active == 0:
                terminal_rows += 1
            else:
                preterminal_counts.update(sizes)
    runs = separators + 1 if data_rows else 0
    if terminal_rows != runs:
        raise ValueError(
            f"{path}: found {terminal_rows} terminal rows for {runs} rupture runs"
        )
    return RawFileAudit(
        str(path),
        int(match.group("ts")),
        int(match.group("seed")),
        int(match.group("m")),
        runs,
        terminal_rows,
        dict(all_counts),
        dict(preterminal_counts),
    )


def _counter_to_array(counter: Counter[int]) -> np.ndarray:
    result = np.zeros(max(counter, default=0) + 1, dtype=np.int64)
    for size, frequency in counter.items():
        result[size] = frequency
    return result


def audit_raw_data(data_root: Path, *, workers: int = 8) -> tuple[dict[tuple[int, str], np.ndarray], list[dict[str, object]]]:
    paths = sorted(data_root.glob("runs/ts_*/*_m_*.txt"))
    if not paths:
        raise ValueError(f"no raw rupture files found below {data_root}")
    grouped_all: dict[int, Counter[int]] = {}
    grouped_pre: dict[int, Counter[int]] = {}
    metadata: dict[int, dict[str, object]] = {}
    with ProcessPoolExecutor(max_workers=workers) as executor:
        for index, item in enumerate(executor.map(audit_raw_file, paths), start=1):
            grouped_all.setdefault(item.ts, Counter()).update(item.all_counts)
            grouped_pre.setdefault(item.ts, Counter()).update(item.preterminal_counts)
            row = metadata.setdefault(
                item.ts,
                {
                    "ts": item.ts,
                    "raw_files": 0,
                    "fibril_seeds": set(),
                    "weibull_moduli": set(),
                    "runs": 0,
                    "terminal_rows": 0,
                },
            )
            row["raw_files"] = int(row["raw_files"]) + 1
            row["fibril_seeds"].add(item.fibril_seed)  # type: ignore[union-attr]
            row["weibull_moduli"].add(item.weibull_m)  # type: ignore[union-attr]
            row["runs"] = int(row["runs"]) + item.runs
            row["terminal_rows"] = int(row["terminal_rows"]) + item.terminal_rows
            if index % 25 == 0:
                print(f"audited {index}/{len(paths)} raw fibril files", flush=True)
    counts: dict[tuple[int, str], np.ndarray] = {}
    rows: list[dict[str, object]] = []
    for ts in sorted(grouped_all):
        counts[(ts, "com_terminal")] = _counter_to_array(grouped_all[ts])
        counts[(ts, "sem_terminal")] = _counter_to_array(grouped_pre[ts])
        row = metadata[ts]
        row["fibrils"] = len(row.pop("fibril_seeds"))  # type: ignore[arg-type]
        row["weibull_moduli"] = ";".join(
            str(value) for value in sorted(row["weibull_moduli"])  # type: ignore[arg-type]
        )
        rows.append(row)
    return counts, rows


def load_pmf(path: Path) -> tuple[np.ndarray, np.ndarray]:
    values = np.loadtxt(path, dtype=float)
    if values.ndim != 2 or values.shape[1] != 2:
        raise ValueError(f"{path}: expected two columns")
    sizes = np.rint(values[:, 0]).astype(np.int64)
    probabilities = values[:, 1]
    if not np.array_equal(sizes.astype(float), values[:, 0]):
        raise ValueError(f"{path}: noninteger size")
    if np.any(sizes < 1) or np.any(np.diff(sizes) <= 0):
        raise ValueError(f"{path}: support is not strictly increasing")
    if np.any(probabilities <= 0.0) or not np.isclose(
        probabilities.sum(), 1.0, atol=5e-13, rtol=0.0
    ):
        raise ValueError(f"{path}: invalid PMF")
    return sizes, probabilities


def reconstruct_counts_from_pmf(
    sizes: np.ndarray,
    probabilities: np.ndarray,
    *,
    maximum_denominator: int = 100_000_000,
) -> tuple[np.ndarray, dict[str, object]]:
    """Recover the common PMF denominator from all rationalized entries.

    This deliberately does not use the smallest positive probability. Each
    printed probability is rationalized independently; the largest reduced
    denominator is accepted only if every probability maps back to an integer
    frequency and those frequencies sum to that denominator.
    """
    denominators = np.asarray(
        [
            Fraction(str(value)).limit_denominator(maximum_denominator).denominator
            for value in probabilities
        ],
        dtype=np.int64,
    )
    total = int(denominators.max())
    observed_counts = np.rint(probabilities * total).astype(np.int64)
    residual = np.abs(probabilities * total - observed_counts)
    if int(observed_counts.sum()) != total or float(residual.max()) > 1e-6:
        raise ValueError(
            "PMF denominator consensus failed integer-frequency validation"
        )
    counts = np.zeros(int(sizes[-1]) + 1, dtype=np.int64)
    counts[sizes] = observed_counts
    return counts, {
        "denominator_method": "maximum reduced denominator across all PMF entries",
        "distinct_reduced_denominators": int(np.unique(denominators).size),
        "maximum_integer_residual": float(residual.max()),
    }


def audit_pmf_data(
    pmf_dir: Path,
    *,
    provenance_manifest: Path | None = None,
) -> tuple[dict[tuple[int, str], np.ndarray], list[dict[str, object]], list[dict[str, object]]]:
    """Audit and reconstruct all Data_avalanches PMFs without raw-file parsing."""
    manifest_totals: dict[int, dict[str, int]] = {}
    if provenance_manifest and provenance_manifest.exists():
        manifest = json.loads(provenance_manifest.read_text(encoding="utf-8"))
        manifest_totals = {int(row["ts"]): row for row in manifest["conditions"]}
    counts: dict[tuple[int, str], np.ndarray] = {}
    rows: list[dict[str, object]] = []
    for path in sorted(pmf_dir.glob("local_avalanches_Ts_*_*_terminal.dat")):
        match = PMF_FILE_RE.match(path.name)
        if match is None:
            continue
        ts = int(match.group("ts"))
        population = (
            "com_terminal" if match.group("population") == "com" else "sem_terminal"
        )
        sizes, probabilities = load_pmf(path)
        reconstructed, denominator_evidence = reconstruct_counts_from_pmf(
            sizes, probabilities
        )
        counts[(ts, population)] = reconstructed
        observed = np.flatnonzero(reconstructed)
        manifest_total = (
            int(manifest_totals[ts]["local_events_s_ge_1"])
            if population == "com_terminal" and ts in manifest_totals
            else None
        )
        rows.append(
            {
                "file": path.name,
                "ts": ts,
                "population": population,
                "reconstructed_total_s_ge_1": int(reconstructed.sum()),
                "reconstructed_singletons_s_eq_1": int(reconstructed[1]),
                "reconstructed_collective_s_ge_2": int(reconstructed[2:].sum()),
                "maximum": int(observed[-1]),
                "observed_support_classes": int(observed.size),
                "integer_support_gaps": int(observed[-1] - observed[0] + 1 - observed.size),
                "pmf_sum": float(probabilities.sum()),
                "manifest_total_com_terminal": manifest_total,
                "matches_provenance_manifest": (
                    None if manifest_total is None else int(reconstructed.sum()) == manifest_total
                ),
                "probability_quantum": 1.0 / int(reconstructed.sum()),
                "smallest_positive_probability": float(probabilities.min()),
                "smallest_equals_quantum": bool(
                    np.isclose(
                        probabilities.min(),
                        1.0 / int(reconstructed.sum()),
                        rtol=1e-10,
                        atol=1e-18,
                    )
                ),
                **denominator_evidence,
            }
        )
    if len(counts) != 20:
        raise ValueError(f"expected 20 PMFs, found {len(counts)}")

    terminal_rows: list[dict[str, object]] = []
    for ts in sorted({key[0] for key in counts}):
        with_terminal = counts[(ts, "com_terminal")]
        preterminal = counts[(ts, "sem_terminal")]
        preterminal = np.pad(
            preterminal, (0, with_terminal.size - preterminal.size)
        )
        terminal = with_terminal - preterminal
        if np.any(terminal < 0):
            raise ValueError(f"Ts={ts}: terminal difference contains negative counts")
        terminal_rows.append(
            {
                "ts": ts,
                "terminal_events": int(terminal.sum()),
                "terminal_singletons": int(terminal[1]),
                "terminal_collective_events_s_ge_2": int(terminal[2:].sum()),
                "terminal_removed_rods": int(np.dot(np.arange(terminal.size), terminal)),
                "terminal_maximum": int(np.flatnonzero(terminal)[-1]),
                "expected_runs_from_manifest": (
                    int(manifest_totals[ts]["runs"]) if ts in manifest_totals else None
                ),
            }
        )
    return counts, rows, terminal_rows


def compare_pmf_to_raw(
    pmf_dir: Path,
    raw_counts: dict[tuple[int, str], np.ndarray],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    paths = sorted(pmf_dir.glob("local_avalanches_Ts_*_*_terminal.dat"))
    for path in paths:
        match = PMF_FILE_RE.match(path.name)
        if match is None:
            raise ValueError(f"unexpected PMF filename: {path.name}")
        ts = int(match.group("ts"))
        population = (
            "com_terminal" if match.group("population") == "com" else "sem_terminal"
        )
        counts = raw_counts[(ts, population)]
        sizes, probabilities = load_pmf(path)
        total = int(counts.sum())
        observed = np.flatnonzero(counts)
        raw_probabilities = counts[observed] / total
        exact_support = np.array_equal(sizes, observed)
        max_error = (
            float(np.max(np.abs(probabilities - raw_probabilities)))
            if exact_support
            else float("nan")
        )
        rounded = np.rint(probabilities * total).astype(np.int64)
        exact_frequencies = bool(
            exact_support and np.array_equal(rounded, counts[observed])
        )
        rows.append(
            {
                "file": path.name,
                "ts": ts,
                "population": population,
                "raw_total_s_ge_1": total,
                "raw_singletons_s_eq_1": int(counts[1]) if counts.size > 1 else 0,
                "raw_collective_s_ge_2": int(counts[2:].sum()),
                "raw_maximum": int(observed[-1]),
                "observed_support_classes": int(observed.size),
                "integer_support_gaps": int(observed[-1] - observed[0] + 1 - observed.size),
                "pmf_sum": float(probabilities.sum()),
                "support_matches_raw": exact_support,
                "frequencies_match_raw": exact_frequencies,
                "maximum_probability_error": max_error,
                "probability_quantum": 1.0 / total,
                "smallest_positive_probability": float(probabilities.min()),
                "smallest_equals_quantum": bool(
                    np.isclose(probabilities.min(), 1.0 / total, rtol=1e-10, atol=1e-18)
                ),
            }
        )
    expected = len(raw_counts)
    if len(rows) != expected:
        raise ValueError(f"found {len(rows)} PMFs for {expected} audited populations")
    return rows


def save_audit(
    output_dir: Path,
    counts: dict[tuple[int, str], np.ndarray],
    raw_rows: list[dict[str, object]],
    pmf_rows: list[dict[str, object]],
    *,
    data_root: Path,
    pmf_dir: Path,
    audit_basis: str = "raw rupture files",
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output_dir / "audited_counts.npz",
        **{f"ts_{ts}_{population}": values for (ts, population), values in counts.items()},
    )
    for name, rows in (("raw_data_audit.csv", raw_rows), ("pmf_audit.csv", pmf_rows)):
        with (output_dir / name).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    manifest = {
        "raw_data_root": str(data_root.resolve()),
        "pmf_directory": str(pmf_dir.resolve()),
        "audit_basis": audit_basis,
        "terminal_rule": "num_active_particles == 0",
        "event_rule": "each positive hyphen-separated connected component is one event",
        "analysis_support": "s >= 2",
        "hierarchy_warning": (
            "The Data_avalanches PMFs contain no fibril or realization identity. "
            "They cannot support hierarchical uncertainty; a hierarchy-preserving "
            "raw source is required for any final block-uncertainty claim."
        ),
    }
    (output_dir / "input_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def load_audited_counts(path: Path) -> dict[tuple[int, str], np.ndarray]:
    result: dict[tuple[int, str], np.ndarray] = {}
    with np.load(path) as archive:
        for key in archive.files:
            match = re.match(r"^ts_(\d+)_(com_terminal|sem_terminal)$", key)
            if match is None:
                raise ValueError(f"unexpected audited-count key: {key}")
            result[(int(match.group(1)), match.group(2))] = archive[key]
    return result

#!/usr/bin/env python3
"""Stream and validate raw collagen-fibril rupture runs.

The rupture simulator writes one file per fibril geometry.  A file contains
many stochastic rupture realizations separated by a line such as
``----------------------------------------------1``.  Each force-step row
stores the sizes of the spatially connected deletion clusters as a
dash-separated field.

This module deliberately keeps file parsing separate from statistical
selection.  In particular, singleton clusters and the terminal force step
are represented in the parsed data even though a downstream analysis may
choose to exclude them.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import multiprocessing
import os
import re
import shutil
import sys
import tempfile
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from contextlib import nullcontext
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence, TextIO


SCHEMA_VERSION = "1.1.0"
DEFAULT_RUN_ROOT = Path("Data_avalanches_all_fibrils/runs")
DEFAULT_DERIVED_ROOT = Path("Data_avalanches_all_fibrils/derived")
DEFAULT_PARQUET_CACHE = DEFAULT_DERIVED_ROOT / "avalanche_runs_v1"
DEFAULT_ANALYSIS_DATABASE = DEFAULT_DERIVED_ROOT / "avalanche_analysis_v1.duckdb"


EXPECTED_HEADER = (
    "f",
    "num_active_particles",
    "num_deleted_particles",
    "total_deleted_rods",
    "avalanche_sizes",
)
RUN_FILE_PATTERN = re.compile(
    r"^ts_(?P<ts>\d+)_seed_(?P<seed>\d+)_m_(?P<modulus>\d+)\.txt$"
)
TS_DIRECTORY_PATTERN = re.compile(r"^ts_(?P<ts>\d+)$")
REALIZATION_SEPARATOR_PATTERN = re.compile(r"^-+(?P<realization>\d+)$")


class RunDataError(ValueError):
    """Raised when a run path or row violates the documented data format."""


@dataclass(frozen=True, slots=True)
class RunFile:
    """Metadata identifying one fibril geometry and its rupture output."""

    path: Path
    ts: int
    seed: int
    weibull_modulus: int

    @property
    def fibril_id(self) -> str:
        """Stable identifier for the independent fibril geometry."""

        return f"ts_{self.ts}_seed_{self.seed}"


@dataclass(frozen=True, slots=True)
class ForceStep:
    """One force level in one stochastic rupture realization."""

    run_file: RunFile
    realization: int
    force: float
    num_active_particles: int
    num_deleted_particles: int
    total_deleted_rods: int
    avalanche_sizes: tuple[int, ...]
    source_line: int
    step_index: int

    @property
    def is_terminal(self) -> bool:
        return self.num_active_particles == 0


@dataclass(frozen=True, slots=True)
class AvalancheEvent:
    """One connected deletion cluster recorded at a force level."""

    run_file: RunFile
    realization: int
    step_index: int
    force: float
    event_index: int
    size: int
    is_terminal_step: bool
    source_line: int


@dataclass(slots=True)
class ConditionSummary:
    """Streaming inventory for one ``(Ts, Weibull modulus)`` condition."""

    ts: int
    weibull_modulus: int
    files: int = 0
    realizations: int = 0
    force_steps: int = 0
    events_all_sizes: int = 0
    singleton_events: int = 0
    terminal_step_events: int = 0
    selected_events: int = 0
    maximum_event_size: int = 0


def _error(path: Path, message: str, line_number: int | None = None) -> RunDataError:
    location = str(path) if line_number is None else f"{path}:{line_number}"
    return RunDataError(f"{location}: {message}")


def parse_run_file(path: str | Path) -> RunFile:
    """Parse ``Ts``, fibril seed, and Weibull modulus from a run filename."""

    path = Path(path)
    match = RUN_FILE_PATTERN.fullmatch(path.name)
    if match is None:
        raise _error(
            path,
            "expected filename ts_<TS>_seed_<SEED>_m_<M>.txt",
        )

    ts = int(match.group("ts"))
    directory_match = TS_DIRECTORY_PATTERN.fullmatch(path.parent.name)
    if directory_match is not None and int(directory_match.group("ts")) != ts:
        raise _error(
            path,
            f"directory Ts={directory_match.group('ts')} disagrees with filename Ts={ts}",
        )

    return RunFile(
        path=path,
        ts=ts,
        seed=int(match.group("seed")),
        weibull_modulus=int(match.group("modulus")),
    )


def discover_run_files(
    root: str | Path,
    *,
    ts_values: set[int] | None = None,
    weibull_moduli: set[int] | None = None,
) -> list[RunFile]:
    """Discover run files recursively and return them in numeric order.

    Every ``.txt`` file below a run directory is expected to follow the run
    naming convention.  Unexpected text files are reported rather than
    silently omitted from a supposedly complete analysis.
    """

    root = Path(root)
    if not root.exists():
        raise RunDataError(f"{root}: run path does not exist")

    paths = [root] if root.is_file() else list(root.rglob("*.txt"))
    run_files = [parse_run_file(path) for path in paths]
    if ts_values is not None:
        run_files = [run for run in run_files if run.ts in ts_values]
    if weibull_moduli is not None:
        run_files = [
            run for run in run_files if run.weibull_modulus in weibull_moduli
        ]
    run_files.sort(
        key=lambda run: (
            run.ts,
            run.seed,
            run.weibull_modulus,
            run.path.as_posix(),
        )
    )
    return run_files


def _parse_nonnegative_int(value: str, field: str, path: Path, line: int) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise _error(path, f"{field} is not an integer: {value!r}", line) from exc
    if parsed < 0:
        raise _error(path, f"{field} must be nonnegative, got {parsed}", line)
    return parsed


def _parse_avalanche_sizes(value: str, path: Path, line: int) -> tuple[int, ...]:
    value = value.strip()
    if value == "0":
        return ()
    if not value:
        raise _error(path, "avalanche_sizes is empty; use 0 for no events", line)

    sizes = tuple(
        _parse_nonnegative_int(token, "avalanche size", path, line)
        for token in value.split("-")
    )
    if any(size == 0 for size in sizes):
        raise _error(path, "nonempty avalanche sizes must all be positive", line)
    return sizes


def iter_force_steps(run_file: RunFile | str | Path) -> Iterator[ForceStep]:
    """Yield validated force steps from one run file without loading it all.

    Validation covers the file header, consecutive realization markers,
    monotonic force, particle accounting, cluster-size totals, and a terminal
    row for every realization.  Errors include the input path and line.
    """

    if not isinstance(run_file, RunFile):
        run_file = parse_run_file(run_file)

    header_seen = False
    realization = 0
    rows_in_realization = 0
    previous_force: float | None = None
    initial_particles: int | None = None
    previous_active_particles: int | None = None
    previous_deleted_particles: int | None = None
    terminal_seen = False

    try:
        handle = run_file.path.open("r", encoding="utf-8", newline="")
    except OSError as exc:
        raise _error(run_file.path, str(exc)) from exc

    with handle:
        reader = csv.reader(handle)
        try:
            for row in reader:
                line = reader.line_num
                if not row or all(not field.strip() for field in row):
                    continue

                if tuple(row) == EXPECTED_HEADER:
                    if header_seen:
                        raise _error(run_file.path, "duplicate CSV header", line)
                    if realization != 0 or rows_in_realization:
                        raise _error(run_file.path, "CSV header occurs after data", line)
                    header_seen = True
                    continue

                if len(row) == 1:
                    separator_match = REALIZATION_SEPARATOR_PATTERN.fullmatch(
                        row[0].strip()
                    )
                    if separator_match is not None:
                        if not header_seen:
                            raise _error(
                                run_file.path,
                                "realization separator occurs before CSV header",
                                line,
                            )
                        if rows_in_realization == 0:
                            raise _error(
                                run_file.path,
                                f"realization {realization} has no force-step rows",
                                line,
                            )
                        if not terminal_seen:
                            raise _error(
                                run_file.path,
                                f"realization {realization} has no terminal row",
                                line,
                            )

                        next_realization = int(separator_match.group("realization"))
                        if next_realization != realization + 1:
                            raise _error(
                                run_file.path,
                                "expected realization marker "
                                f"{realization + 1}, got {next_realization}",
                                line,
                            )
                        realization = next_realization
                        rows_in_realization = 0
                        previous_force = None
                        initial_particles = None
                        previous_active_particles = None
                        previous_deleted_particles = None
                        terminal_seen = False
                        continue

                if not header_seen:
                    raise _error(run_file.path, "missing CSV header before data", line)
                if terminal_seen:
                    raise _error(
                        run_file.path,
                        f"data found after terminal row of realization {realization}",
                        line,
                    )
                if len(row) != len(EXPECTED_HEADER):
                    raise _error(
                        run_file.path,
                        f"expected {len(EXPECTED_HEADER)} CSV fields, got {len(row)}",
                        line,
                    )

                try:
                    force = float(row[0])
                except ValueError as exc:
                    raise _error(
                        run_file.path,
                        f"f is not numeric: {row[0]!r}",
                        line,
                    ) from exc
                if not math.isfinite(force) or force < 0:
                    raise _error(
                        run_file.path,
                        f"f must be finite and nonnegative, got {force}",
                        line,
                    )
                if previous_force is None:
                    if not math.isclose(force, 0.0, abs_tol=1e-12):
                        raise _error(
                            run_file.path,
                            f"realization {realization} must start at f=0, got {force}",
                            line,
                        )
                elif force <= previous_force:
                    raise _error(
                        run_file.path,
                        f"force must increase strictly within realization {realization}",
                        line,
                    )

                active_particles = _parse_nonnegative_int(
                    row[1], "num_active_particles", run_file.path, line
                )
                deleted_particles = _parse_nonnegative_int(
                    row[2], "num_deleted_particles", run_file.path, line
                )
                total_deleted_rods = _parse_nonnegative_int(
                    row[3], "total_deleted_rods", run_file.path, line
                )
                avalanche_sizes = _parse_avalanche_sizes(
                    row[4], run_file.path, line
                )

                if sum(avalanche_sizes) != total_deleted_rods:
                    raise _error(
                        run_file.path,
                        "sum(avalanche_sizes) does not equal total_deleted_rods: "
                        f"{sum(avalanche_sizes)} != {total_deleted_rods}",
                        line,
                    )

                if initial_particles is None:
                    initial_particles = active_particles + deleted_particles
                if active_particles + deleted_particles != initial_particles:
                    raise _error(
                        run_file.path,
                        "num_active_particles + num_deleted_particles changed within "
                        f"realization {realization}",
                        line,
                    )
                if (
                    previous_active_particles is not None
                    and active_particles > previous_active_particles
                ):
                    raise _error(
                        run_file.path,
                        "num_active_particles increased within "
                        f"realization {realization}",
                        line,
                    )
                if (
                    previous_deleted_particles is not None
                    and deleted_particles < previous_deleted_particles
                ):
                    raise _error(
                        run_file.path,
                        "num_deleted_particles decreased within "
                        f"realization {realization}",
                        line,
                    )

                step = ForceStep(
                    run_file=run_file,
                    realization=realization,
                    force=force,
                    num_active_particles=active_particles,
                    num_deleted_particles=deleted_particles,
                    total_deleted_rods=total_deleted_rods,
                    avalanche_sizes=avalanche_sizes,
                    source_line=line,
                    step_index=rows_in_realization,
                )
                yield step

                rows_in_realization += 1
                previous_force = force
                previous_active_particles = active_particles
                previous_deleted_particles = deleted_particles
                terminal_seen = step.is_terminal
        except csv.Error as exc:
            raise _error(run_file.path, f"invalid CSV: {exc}", reader.line_num) from exc

    if not header_seen:
        raise _error(run_file.path, "missing CSV header")
    if rows_in_realization == 0:
        raise _error(run_file.path, f"realization {realization} has no force-step rows")
    if not terminal_seen:
        raise _error(run_file.path, f"realization {realization} has no terminal row")


def iter_avalanche_events(
    force_steps: Iterable[ForceStep],
    *,
    minimum_size: int = 1,
    include_terminal_step: bool = True,
) -> Iterator[AvalancheEvent]:
    """Expand force-step cluster lists into one record per selected event."""

    if minimum_size < 1:
        raise ValueError("minimum_size must be at least 1")

    for step in force_steps:
        if step.is_terminal and not include_terminal_step:
            continue
        for event_index, size in enumerate(step.avalanche_sizes):
            if size < minimum_size:
                continue
            yield AvalancheEvent(
                run_file=step.run_file,
                realization=step.realization,
                step_index=step.step_index,
                force=step.force,
                event_index=event_index,
                size=size,
                is_terminal_step=step.is_terminal,
                source_line=step.source_line,
            )


def summarize_dataset(
    run_files: Sequence[RunFile],
    *,
    minimum_size: int = 2,
    include_terminal_step: bool = True,
) -> dict[str, object]:
    """Validate and summarize a collection while keeping memory bounded."""

    if minimum_size < 1:
        raise ValueError("minimum_size must be at least 1")

    conditions: dict[tuple[int, int], ConditionSummary] = {}
    for run_file in run_files:
        key = (run_file.ts, run_file.weibull_modulus)
        summary = conditions.setdefault(
            key,
            ConditionSummary(
                ts=run_file.ts,
                weibull_modulus=run_file.weibull_modulus,
            ),
        )
        summary.files += 1

        seen_realizations: set[int] = set()
        for step in iter_force_steps(run_file):
            seen_realizations.add(step.realization)
            summary.force_steps += 1
            for size in step.avalanche_sizes:
                summary.events_all_sizes += 1
                summary.maximum_event_size = max(summary.maximum_event_size, size)
                if size == 1:
                    summary.singleton_events += 1
                if step.is_terminal:
                    summary.terminal_step_events += 1
                if (
                    size >= minimum_size
                    and (include_terminal_step or not step.is_terminal)
                ):
                    summary.selected_events += 1
        summary.realizations += len(seen_realizations)

    condition_rows = [
        asdict(conditions[key])
        for key in sorted(conditions, key=lambda item: (item[0], item[1]))
    ]
    total_keys = (
        "files",
        "realizations",
        "force_steps",
        "events_all_sizes",
        "singleton_events",
        "terminal_step_events",
        "selected_events",
    )
    totals = {
        key: sum(int(condition[key]) for condition in condition_rows)
        for key in total_keys
    }
    totals["maximum_event_size"] = max(
        (int(condition["maximum_event_size"]) for condition in condition_rows),
        default=0,
    )
    return {
        "selection": {
            "minimum_size": minimum_size,
            "include_terminal_step": include_terminal_step,
        },
        "conditions": condition_rows,
        "totals": totals,
    }


EVENT_COLUMNS = (
    "ts",
    "seed",
    "weibull_modulus",
    "fibril_id",
    "realization",
    "step_index",
    "force",
    "event_index",
    "avalanche_size",
    "is_terminal_step",
    "source_file",
    "source_line",
)


def write_events_csv(
    run_files: Sequence[RunFile],
    output: TextIO,
    *,
    minimum_size: int = 2,
    include_terminal_step: bool = True,
) -> int:
    """Write selected raw events in long form and return the row count."""

    writer = csv.DictWriter(output, fieldnames=EVENT_COLUMNS, lineterminator="\n")
    writer.writeheader()
    count = 0
    for run_file in run_files:
        events = iter_avalanche_events(
            iter_force_steps(run_file),
            minimum_size=minimum_size,
            include_terminal_step=include_terminal_step,
        )
        for event in events:
            writer.writerow(
                {
                    "ts": event.run_file.ts,
                    "seed": event.run_file.seed,
                    "weibull_modulus": event.run_file.weibull_modulus,
                    "fibril_id": event.run_file.fibril_id,
                    "realization": event.realization,
                    "step_index": event.step_index,
                    "force": event.force,
                    "event_index": event.event_index,
                    "avalanche_size": event.size,
                    "is_terminal_step": int(event.is_terminal_step),
                    "source_file": event.run_file.path.as_posix(),
                    "source_line": event.source_line,
                }
            )
            count += 1
    return count


def _sha256(path: Path, *, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def _provenance(run_file: RunFile, root: Path) -> dict[str, Any]:
    stat = run_file.path.stat()
    try:
        source_file = run_file.path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        source_file = run_file.path.resolve().as_posix()
    return {
        "schema_version": SCHEMA_VERSION,
        "ts": run_file.ts,
        "seed": run_file.seed,
        "weibull_modulus": run_file.weibull_modulus,
        "fibril_id": run_file.fibril_id,
        "source_file": source_file,
        "source_size_bytes": stat.st_size,
        "source_mtime_ns": stat.st_mtime_ns,
        "source_sha256": _sha256(run_file.path),
    }


def _quoted_path(path: Path) -> str:
    return "'" + path.as_posix().replace("'", "''") + "'"


def _insert_batch(connection: Any, table: str, rows: list[tuple[Any, ...]]) -> None:
    """Move one bounded Python batch into DuckDB without row-wise inserts."""
    if not rows:
        return
    import pandas as pd

    frame = pd.DataFrame.from_records(rows)
    connection.register("incoming_batch", frame)
    try:
        connection.execute(f"INSERT INTO {table} SELECT * FROM incoming_batch")
    finally:
        connection.unregister("incoming_batch")
    rows.clear()


def _create_cache_buffers(connection: Any) -> None:
    """Create fresh per-source-file buffers without retained deleted rows."""
    connection.execute("""
        CREATE TABLE force_buffer (
          schema_version VARCHAR, ts INTEGER, seed BIGINT,
          weibull_modulus INTEGER, fibril_id VARCHAR, realization INTEGER,
          step_index INTEGER, force DOUBLE, num_active_particles BIGINT,
          num_deleted_particles BIGINT, total_deleted_rods BIGINT,
          avalanche_count INTEGER, is_terminal_step BOOLEAN,
          source_file VARCHAR, source_line BIGINT
        );
        CREATE TABLE event_buffer (
          schema_version VARCHAR, ts INTEGER, seed BIGINT,
          weibull_modulus INTEGER, fibril_id VARCHAR, realization INTEGER,
          step_index INTEGER, force DOUBLE, event_index INTEGER,
          avalanche_size BIGINT, is_terminal_step BOOLEAN,
          source_file VARCHAR, source_line BIGINT
        );
        CREATE TABLE run_summary_buffer (
          schema_version VARCHAR, ts INTEGER, seed BIGINT,
          weibull_modulus INTEGER, fibril_id VARCHAR,
          realization INTEGER, force_steps BIGINT,
          avalanche_events BIGINT, singleton_events BIGINT,
          terminal_step_events BIGINT, maximum_avalanche_size BIGINT,
          terminal_force DOUBLE, source_file VARCHAR
        );
        CREATE TABLE run_histogram_buffer (
          schema_version VARCHAR, ts INTEGER, seed BIGINT,
          weibull_modulus INTEGER, fibril_id VARCHAR,
          realization INTEGER, is_terminal_step BOOLEAN,
          avalanche_size BIGINT, event_count BIGINT,
          source_file VARCHAR
        );
    """)


def _drop_cache_buffers(connection: Any) -> None:
    connection.execute("""
        DROP TABLE force_buffer;
        DROP TABLE event_buffer;
        DROP TABLE run_summary_buffer;
        DROP TABLE run_histogram_buffer;
    """)


def _build_cache_fragment(
    run_file: RunFile,
    file_index: int,
    temporary: Path,
    root: Path,
) -> tuple[int, dict[str, Any], int, int, int, int]:
    """Parse one source file and write its independent Parquet fragments."""
    import duckdb

    connection = duckdb.connect()
    connection.execute("SET threads = 1")
    _create_cache_buffers(connection)
    try:
        provenance = _provenance(run_file, root)
        source = provenance["source_file"]
        force_rows: list[tuple[Any, ...]] = []
        event_rows: list[tuple[Any, ...]] = []
        realizations: set[int] = set()
        run_histogram: Counter[tuple[int, bool, int]] = Counter()
        run_summaries: dict[int, dict[str, int | float]] = {}
        for step in iter_force_steps(run_file):
            realizations.add(step.realization)
            run_summary = run_summaries.setdefault(
                step.realization,
                {
                    "force_steps": 0,
                    "avalanche_events": 0,
                    "singleton_events": 0,
                    "terminal_step_events": 0,
                    "maximum_avalanche_size": 0,
                    "terminal_force": math.nan,
                },
            )
            run_summary["force_steps"] += 1
            run_summary["avalanche_events"] += len(step.avalanche_sizes)
            run_summary["singleton_events"] += step.avalanche_sizes.count(1)
            if step.is_terminal:
                run_summary["terminal_step_events"] += len(step.avalanche_sizes)
                run_summary["terminal_force"] = step.force
            common = (
                SCHEMA_VERSION, run_file.ts, run_file.seed,
                run_file.weibull_modulus, run_file.fibril_id,
                step.realization, step.step_index, step.force,
            )
            force_rows.append(common + (
                step.num_active_particles, step.num_deleted_particles,
                step.total_deleted_rods, len(step.avalanche_sizes),
                step.is_terminal, source, step.source_line,
            ))
            for event_index, size in enumerate(step.avalanche_sizes):
                run_histogram[(step.realization, step.is_terminal, size)] += 1
                run_summary["maximum_avalanche_size"] = max(
                    int(run_summary["maximum_avalanche_size"]), size
                )
                event_rows.append(common + (
                    event_index, size, step.is_terminal, source,
                    step.source_line,
                ))
            if len(force_rows) >= 10_000:
                _insert_batch(connection, "force_buffer", force_rows)
            if len(event_rows) >= 50_000:
                _insert_batch(connection, "event_buffer", event_rows)
        _insert_batch(connection, "force_buffer", force_rows)
        _insert_batch(connection, "event_buffer", event_rows)

        summary_rows = [
            (
                SCHEMA_VERSION, run_file.ts, run_file.seed,
                run_file.weibull_modulus, run_file.fibril_id, realization,
                int(summary["force_steps"]),
                int(summary["avalanche_events"]),
                int(summary["singleton_events"]),
                int(summary["terminal_step_events"]),
                int(summary["maximum_avalanche_size"]),
                float(summary["terminal_force"]), source,
            )
            for realization, summary in sorted(run_summaries.items())
        ]
        histogram_rows = [
            (
                SCHEMA_VERSION, run_file.ts, run_file.seed,
                run_file.weibull_modulus, run_file.fibril_id, realization,
                terminal, size, count, source,
            )
            for (realization, terminal, size), count
            in sorted(run_histogram.items())
        ]
        _insert_batch(connection, "run_summary_buffer", summary_rows)
        _insert_batch(connection, "run_histogram_buffer", histogram_rows)

        partition = (
            Path(f"ts={run_file.ts}")
            / f"weibull_modulus={run_file.weibull_modulus}"
        )
        directories = {
            "force_buffer": temporary / "force_steps" / partition,
            "event_buffer": temporary / "avalanche_events" / partition,
            "run_summary_buffer": temporary / "run_summary" / partition,
            "run_histogram_buffer": temporary / "run_histograms" / partition,
        }
        for directory in directories.values():
            directory.mkdir(parents=True, exist_ok=True)
        fragment = f"part-{file_index:05d}-seed-{run_file.seed}.parquet"
        for table, directory in directories.items():
            connection.execute(
                f"COPY {table} TO {_quoted_path(directory / fragment)} "
                "(FORMAT PARQUET, COMPRESSION ZSTD)"
            )
        force_count = int(
            connection.execute("SELECT count(*) FROM force_buffer").fetchone()[0]
        )
        event_count = int(
            connection.execute("SELECT count(*) FROM event_buffer").fetchone()[0]
        )
        histogram_count = int(
            connection.execute(
                "SELECT count(*) FROM run_histogram_buffer"
            ).fetchone()[0]
        )
        return (
            file_index, provenance, len(realizations), force_count,
            event_count, histogram_count,
        )
    finally:
        connection.close()


def _build_parquet_cache_sequential(
    run_files: Sequence[RunFile],
    output: str | Path,
    *,
    root: str | Path = DEFAULT_RUN_ROOT,
) -> dict[str, int]:
    """Build a versioned, reconstructible Parquet cache and publish atomically.

    Raw events are never filtered: singleton and terminal-step events are both
    present.  One fragment per source run keeps peak memory bounded.  The only
    Hive partition keys are ``ts`` and ``weibull_modulus``.
    """
    try:
        import duckdb
    except ImportError as exc:  # pragma: no cover - environment diagnostic
        raise RuntimeError("duckdb is required to build the Parquet cache") from exc

    output = Path(output)
    root = Path(root)
    if output.exists():
        raise RunDataError(f"{output}: output already exists; choose a new path")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{output.name}.building-", dir=output.parent)
    )
    counts = {
        "files": 0,
        "realizations": 0,
        "force_steps": 0,
        "avalanche_events": 0,
        "run_histogram_rows": 0,
    }
    connection = duckdb.connect()
    try:
        connection.execute("""
            CREATE TABLE manifest (
              schema_version VARCHAR, ts INTEGER, seed BIGINT,
              weibull_modulus INTEGER, fibril_id VARCHAR, source_file VARCHAR,
              source_size_bytes BIGINT, source_mtime_ns BIGINT,
              source_sha256 VARCHAR, realizations INTEGER,
              force_steps BIGINT, avalanche_events BIGINT
            );
        """)
        _create_cache_buffers(connection)
        for file_index, run_file in enumerate(run_files):
            provenance = _provenance(run_file, root)
            source = provenance["source_file"]
            force_rows: list[tuple[Any, ...]] = []
            event_rows: list[tuple[Any, ...]] = []
            realizations: set[int] = set()
            run_histogram: Counter[tuple[int, bool, int]] = Counter()
            run_summaries: dict[int, dict[str, int | float]] = {}
            for step in iter_force_steps(run_file):
                realizations.add(step.realization)
                run_summary = run_summaries.setdefault(
                    step.realization,
                    {
                        "force_steps": 0,
                        "avalanche_events": 0,
                        "singleton_events": 0,
                        "terminal_step_events": 0,
                        "maximum_avalanche_size": 0,
                        "terminal_force": math.nan,
                    },
                )
                run_summary["force_steps"] += 1
                run_summary["avalanche_events"] += len(step.avalanche_sizes)
                run_summary["singleton_events"] += step.avalanche_sizes.count(1)
                if step.is_terminal:
                    run_summary["terminal_step_events"] += len(step.avalanche_sizes)
                    run_summary["terminal_force"] = step.force
                common = (
                    SCHEMA_VERSION, run_file.ts, run_file.seed,
                    run_file.weibull_modulus, run_file.fibril_id,
                    step.realization, step.step_index, step.force,
                )
                force_rows.append(common + (
                    step.num_active_particles, step.num_deleted_particles,
                    step.total_deleted_rods, len(step.avalanche_sizes),
                    step.is_terminal, source, step.source_line,
                ))
                for event_index, size in enumerate(step.avalanche_sizes):
                    run_histogram[(step.realization, step.is_terminal, size)] += 1
                    run_summary["maximum_avalanche_size"] = max(
                        int(run_summary["maximum_avalanche_size"]), size
                    )
                    event_rows.append(common + (
                        event_index, size, step.is_terminal, source,
                        step.source_line,
                    ))
                if len(force_rows) >= 10_000:
                    _insert_batch(connection, "force_buffer", force_rows)
                if len(event_rows) >= 50_000:
                    _insert_batch(connection, "event_buffer", event_rows)
            _insert_batch(connection, "force_buffer", force_rows)
            _insert_batch(connection, "event_buffer", event_rows)

            summary_rows = [
                (
                    SCHEMA_VERSION, run_file.ts, run_file.seed,
                    run_file.weibull_modulus, run_file.fibril_id, realization,
                    int(summary["force_steps"]),
                    int(summary["avalanche_events"]),
                    int(summary["singleton_events"]),
                    int(summary["terminal_step_events"]),
                    int(summary["maximum_avalanche_size"]),
                    float(summary["terminal_force"]), source,
                )
                for realization, summary in sorted(run_summaries.items())
            ]
            histogram_rows = [
                (
                    SCHEMA_VERSION, run_file.ts, run_file.seed,
                    run_file.weibull_modulus, run_file.fibril_id, realization,
                    terminal, size, count, source,
                )
                for (realization, terminal, size), count
                in sorted(run_histogram.items())
            ]
            _insert_batch(connection, "run_summary_buffer", summary_rows)
            _insert_batch(connection, "run_histogram_buffer", histogram_rows)

            partition = Path(f"ts={run_file.ts}") / f"weibull_modulus={run_file.weibull_modulus}"
            force_dir = temporary / "force_steps" / partition
            event_dir = temporary / "avalanche_events" / partition
            summary_dir = temporary / "run_summary" / partition
            histogram_dir = temporary / "run_histograms" / partition
            force_dir.mkdir(parents=True, exist_ok=True)
            event_dir.mkdir(parents=True, exist_ok=True)
            summary_dir.mkdir(parents=True, exist_ok=True)
            histogram_dir.mkdir(parents=True, exist_ok=True)
            fragment = f"part-{file_index:05d}-seed-{run_file.seed}.parquet"
            connection.execute(f"COPY force_buffer TO {_quoted_path(force_dir / fragment)} (FORMAT PARQUET, COMPRESSION ZSTD)")
            connection.execute(f"COPY event_buffer TO {_quoted_path(event_dir / fragment)} (FORMAT PARQUET, COMPRESSION ZSTD)")
            connection.execute(f"COPY run_summary_buffer TO {_quoted_path(summary_dir / fragment)} (FORMAT PARQUET, COMPRESSION ZSTD)")
            connection.execute(f"COPY run_histogram_buffer TO {_quoted_path(histogram_dir / fragment)} (FORMAT PARQUET, COMPRESSION ZSTD)")
            force_count = connection.execute("SELECT count(*) FROM force_buffer").fetchone()[0]
            event_count = connection.execute("SELECT count(*) FROM event_buffer").fetchone()[0]
            histogram_count = connection.execute(
                "SELECT count(*) FROM run_histogram_buffer"
            ).fetchone()[0]
            connection.execute(
                "INSERT INTO manifest VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                tuple(provenance.values()) + (len(realizations), force_count, event_count),
            )
            _drop_cache_buffers(connection)
            _create_cache_buffers(connection)
            counts["files"] += 1
            counts["realizations"] += len(realizations)
            counts["force_steps"] += force_count
            counts["avalanche_events"] += event_count
            counts["run_histogram_rows"] += histogram_count

        manifest_dir = temporary / "manifest"
        manifest_dir.mkdir()
        connection.execute(f"COPY manifest TO {_quoted_path(manifest_dir / 'manifest.parquet')} (FORMAT PARQUET, COMPRESSION ZSTD)")
        metadata = {
            "schema_version": SCHEMA_VERSION,
            "raw_root": root.resolve().as_posix(),
            "partition_keys": ["ts", "weibull_modulus"],
            "datasets": [
                "manifest",
                "force_steps",
                "avalanche_events",
                "run_summary",
                "run_histograms",
            ],
            "counts": counts,
        }
        (temporary / "dataset.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        os.replace(temporary, output)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    finally:
        connection.close()
    return counts


def build_parquet_cache(
    run_files: Sequence[RunFile],
    output: str | Path,
    *,
    root: str | Path = DEFAULT_RUN_ROOT,
    workers: int = 1,
) -> dict[str, int]:
    """Build the canonical cache, optionally processing fibrils in parallel."""
    if workers < 1:
        raise ValueError("workers must be at least 1")
    if workers == 1:
        return _build_parquet_cache_sequential(run_files, output, root=root)

    output = Path(output)
    root = Path(root)
    if output.exists():
        raise RunDataError(f"{output}: output already exists; choose a new path")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{output.name}.building-", dir=output.parent)
    )
    counts = {
        "files": 0,
        "realizations": 0,
        "force_steps": 0,
        "avalanche_events": 0,
        "run_histogram_rows": 0,
    }
    results: list[tuple[int, dict[str, Any], int, int, int, int]] = []
    try:
        with ProcessPoolExecutor(
            max_workers=workers,
            mp_context=multiprocessing.get_context("spawn"),
        ) as executor:
            futures = [
                executor.submit(
                    _build_cache_fragment,
                    run_file,
                    file_index,
                    temporary,
                    root,
                )
                for file_index, run_file in enumerate(run_files)
            ]
            for completed, future in enumerate(as_completed(futures), start=1):
                results.append(future.result())
                if completed % 10 == 0 or completed == len(futures):
                    print(
                        f"cache progress: {completed}/{len(futures)} files",
                        file=sys.stderr,
                        flush=True,
                    )

        results.sort(key=lambda result: result[0])
        import duckdb

        connection = duckdb.connect()
        try:
            connection.execute("""
                CREATE TABLE manifest (
                  schema_version VARCHAR, ts INTEGER, seed BIGINT,
                  weibull_modulus INTEGER, fibril_id VARCHAR,
                  source_file VARCHAR, source_size_bytes BIGINT,
                  source_mtime_ns BIGINT, source_sha256 VARCHAR,
                  realizations INTEGER, force_steps BIGINT,
                  avalanche_events BIGINT
                )
            """)
            manifest_rows = []
            for _, provenance, realizations, force_steps, events, histograms in results:
                manifest_rows.append(
                    tuple(provenance.values())
                    + (realizations, force_steps, events)
                )
                counts["files"] += 1
                counts["realizations"] += realizations
                counts["force_steps"] += force_steps
                counts["avalanche_events"] += events
                counts["run_histogram_rows"] += histograms
            _insert_batch(connection, "manifest", manifest_rows)
            manifest_dir = temporary / "manifest"
            manifest_dir.mkdir()
            connection.execute(
                f"COPY manifest TO "
                f"{_quoted_path(manifest_dir / 'manifest.parquet')} "
                "(FORMAT PARQUET, COMPRESSION ZSTD)"
            )
        finally:
            connection.close()

        metadata = {
            "schema_version": SCHEMA_VERSION,
            "raw_root": root.resolve().as_posix(),
            "partition_keys": ["ts", "weibull_modulus"],
            "datasets": [
                "manifest", "force_steps", "avalanche_events",
                "run_summary", "run_histograms",
            ],
            "counts": counts,
            "workers": workers,
        }
        (temporary / "dataset.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        os.replace(temporary, output)
        return counts
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def build_analysis_database(
    parquet_cache: str | Path,
    output: str | Path,
) -> dict[str, int]:
    """Build an atomic DuckDB database from a normalized Parquet cache."""
    try:
        import duckdb
    except ImportError as exc:  # pragma: no cover - environment diagnostic
        raise RuntimeError("duckdb is required to build the analysis database") from exc

    parquet_cache = Path(parquet_cache)
    output = Path(output)
    descriptor_path = parquet_cache / "dataset.json"
    if not descriptor_path.is_file():
        raise RunDataError(f"{parquet_cache}: missing dataset.json")
    descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
    if descriptor.get("schema_version") != SCHEMA_VERSION:
        raise RunDataError(
            f"{parquet_cache}: schema version {descriptor.get('schema_version')!r} "
            f"does not match reader version {SCHEMA_VERSION!r}"
        )
    required = {"manifest", "force_steps", "avalanche_events",
                "run_summary", "run_histograms"}
    missing = required.difference(descriptor.get("datasets", []))
    if missing:
        raise RunDataError(
            f"{parquet_cache}: missing datasets {sorted(missing)}"
        )
    if output.exists():
        raise RunDataError(f"{output}: output already exists; choose a new path")

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.building-{os.getpid()}")
    if temporary.exists():
        raise RunDataError(f"{temporary}: temporary output already exists")
    globs = {
        name: (parquet_cache.resolve() / name / "**" / "*.parquet").as_posix()
        for name in required.difference({"manifest"})
    }
    manifest_path = (parquet_cache.resolve() / "manifest" / "manifest.parquet").as_posix()
    connection = duckdb.connect(temporary.as_posix())
    try:
        connection.execute("SET preserve_insertion_order = false")
        connection.execute(
            "CREATE TABLE cache_metadata (key VARCHAR PRIMARY KEY, value VARCHAR)"
        )
        metadata_rows = [
            ("schema_version", SCHEMA_VERSION),
            ("parquet_cache", parquet_cache.resolve().as_posix()),
            ("raw_root", str(descriptor.get("raw_root", ""))),
            ("source_counts", json.dumps(descriptor.get("counts", {}), sort_keys=True)),
        ]
        connection.executemany("INSERT INTO cache_metadata VALUES (?, ?)", metadata_rows)
        connection.execute(
            f"CREATE TABLE source_manifest AS SELECT * FROM read_parquet({_quoted_path(Path(manifest_path))})"
        )
        connection.execute(
            "CREATE TABLE run_summary AS SELECT * FROM "
            f"read_parquet({_quoted_path(Path(globs['run_summary']))}, hive_partitioning=true) "
            "ORDER BY ts, seed, realization"
        )
        connection.execute(
            "CREATE TABLE run_histograms AS SELECT * FROM "
            f"read_parquet({_quoted_path(Path(globs['run_histograms']))}, hive_partitioning=true) "
            "ORDER BY ts, seed, realization, is_terminal_step, avalanche_size"
        )
        connection.execute("""
            CREATE TABLE fibril_histograms AS
            SELECT schema_version, ts, seed, weibull_modulus, fibril_id,
                   is_terminal_step, avalanche_size,
                   sum(event_count)::BIGINT AS event_count
            FROM run_histograms
            GROUP BY ALL
            ORDER BY ts, seed, is_terminal_step, avalanche_size
        """)
        connection.execute("""
            CREATE TABLE pooled_histograms AS
            SELECT schema_version, ts, weibull_modulus, is_terminal_step,
                   avalanche_size, sum(event_count)::BIGINT AS event_count
            FROM run_histograms
            GROUP BY ALL
            ORDER BY ts, is_terminal_step, avalanche_size
        """)
        connection.execute(
            "CREATE VIEW force_steps AS SELECT * FROM "
            f"read_parquet({_quoted_path(Path(globs['force_steps']))}, hive_partitioning=true)"
        )
        connection.execute(
            "CREATE VIEW avalanche_events AS SELECT * FROM "
            f"read_parquet({_quoted_path(Path(globs['avalanche_events']))}, hive_partitioning=true)"
        )
        counts = {
            table: int(connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0])
            for table in (
                "source_manifest", "run_summary", "run_histograms",
                "fibril_histograms", "pooled_histograms",
            )
        }
        event_total = int(
            connection.execute("SELECT coalesce(sum(event_count), 0) FROM run_histograms").fetchone()[0]
        )
        expected_events = int(descriptor.get("counts", {}).get("avalanche_events", -1))
        if event_total != expected_events:
            raise RunDataError(
                f"analysis database event total {event_total} != cache total {expected_events}"
            )
        counts["avalanche_events_represented"] = event_total
        connection.execute("CHECKPOINT")
        connection.close()
        os.replace(temporary, output)
        return counts
    except BaseException:
        connection.close()
        temporary.unlink(missing_ok=True)
        Path(f"{temporary}.wal").unlink(missing_ok=True)
        raise


def _add_selection_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=DEFAULT_RUN_ROOT,
        help=(
            "run directory or one run file "
            f"(default: {DEFAULT_RUN_ROOT.as_posix()})"
        ),
    )
    parser.add_argument(
        "--ts",
        dest="ts_values",
        action="append",
        type=int,
        help="include this Ts value; may be repeated",
    )
    parser.add_argument(
        "--weibull-modulus",
        dest="weibull_moduli",
        action="append",
        type=int,
        help="include this Weibull modulus; may be repeated",
    )
    parser.add_argument(
        "--minimum-size",
        type=int,
        default=2,
        help="minimum event size selected downstream (default: 2)",
    )
    parser.add_argument(
        "--exclude-terminal-step",
        action="store_true",
        help="exclude clusters recorded on the terminal force step",
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    summary_parser = subparsers.add_parser(
        "summary",
        help="validate all selected files and print a JSON inventory",
    )
    _add_selection_arguments(summary_parser)

    events_parser = subparsers.add_parser(
        "events",
        help="write selected avalanche events as a provenance-rich CSV",
    )
    _add_selection_arguments(events_parser)
    events_parser.add_argument(
        "--output",
        type=Path,
        help="output CSV path; omit to write to standard output",
    )
    cache_parser = subparsers.add_parser(
        "build-cache",
        help="validate raw files and atomically build the full Parquet cache",
    )
    cache_parser.add_argument(
        "root", nargs="?", type=Path, default=DEFAULT_RUN_ROOT,
        help=(
            "run directory or one run file "
            f"(default: {DEFAULT_RUN_ROOT.as_posix()})"
        ),
    )
    cache_parser.add_argument("--ts", dest="ts_values", action="append", type=int)
    cache_parser.add_argument(
        "--weibull-modulus", dest="weibull_moduli", action="append", type=int
    )
    cache_parser.add_argument(
        "--output", type=Path, required=True,
        help="new output directory (must be outside runs/ and not already exist)",
    )
    cache_parser.add_argument(
        "--workers",
        type=int,
        default=min(4, os.cpu_count() or 1),
        help="fibrils converted concurrently (default: up to 4)",
    )
    database_parser = subparsers.add_parser(
        "build-analysis-db",
        help="build compact DuckDB tables and Parquet-backed detail views",
    )
    database_parser.add_argument(
        "cache", nargs="?", type=Path, default=DEFAULT_PARQUET_CACHE,
        help=(
            "normalized Parquet cache "
            f"(default: {DEFAULT_PARQUET_CACHE.as_posix()})"
        ),
    )
    database_parser.add_argument(
        "--output", type=Path, default=DEFAULT_ANALYSIS_DATABASE,
        help=(
            "new DuckDB file "
            f"(default: {DEFAULT_ANALYSIS_DATABASE.as_posix()})"
        ),
    )
    return parser


def _selected_files(args: argparse.Namespace) -> list[RunFile]:
    run_files = discover_run_files(
        args.root,
        ts_values=set(args.ts_values) if args.ts_values else None,
        weibull_moduli=(
            set(args.weibull_moduli) if args.weibull_moduli else None
        ),
    )
    if not run_files:
        raise RunDataError(f"{args.root}: no run files match the selection")
    return run_files


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "minimum_size") and args.minimum_size < 1:
        parser.error("--minimum-size must be at least 1")

    try:
        if args.command == "build-analysis-db":
            counts = build_analysis_database(args.cache, args.output)
            print(json.dumps(counts, indent=2))
            return 0
        run_files = _selected_files(args)
        if args.command == "build-cache":
            raw = args.root.resolve()
            destination = args.output.resolve()
            if destination == raw or raw in destination.parents:
                raise RunDataError(
                    f"{args.output}: derived cache must be outside the raw-data root"
                )
            counts = build_parquet_cache(
                run_files,
                args.output,
                root=args.root if args.root.is_dir() else args.root.parent,
                workers=args.workers,
            )
            print(json.dumps(counts, indent=2))
            return 0
        include_terminal_step = not args.exclude_terminal_step
        if args.command == "summary":
            summary = summarize_dataset(
                run_files,
                minimum_size=args.minimum_size,
                include_terminal_step=include_terminal_step,
            )
            summary["root"] = args.root.as_posix()
            print(json.dumps(summary, indent=2, sort_keys=False))
            return 0

        output_context = (
            args.output.open("w", encoding="utf-8", newline="")
            if args.output is not None
            else nullcontext(sys.stdout)
        )
        with output_context as output:
            write_events_csv(
                run_files,
                output,
                minimum_size=args.minimum_size,
                include_terminal_step=include_terminal_step,
            )
        return 0
    except (OSError, RunDataError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

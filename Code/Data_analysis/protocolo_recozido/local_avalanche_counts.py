#!/usr/bin/env python3
"""Count local connected avalanche events in the raw rupture outputs.

This module deliberately performs no distribution fitting.  It streams the
raw text files, treats every positive integer in ``avalanche_sizes`` as one
local connected event, and preserves the fibril/run hierarchy in the counts.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


FILE_RE = re.compile(r"^ts_(?P<ts>\d+)_seed_(?P<seed>\d+)_m_(?P<m>\d+)\.txt$")
RUN_SEPARATOR_RE = re.compile(r"^-+(?P<run_id>\d+)\s*$")


@dataclass(frozen=True)
class ForceStep:
    run_id: int
    force: float
    num_active_particles: int
    total_deleted_rods: int
    local_sizes: tuple[int, ...]

    @property
    def terminal(self) -> bool:
        return self.num_active_particles == 0


def parse_local_sizes(raw: str) -> tuple[int, ...]:
    """Parse the hyphen-separated connected-component sizes in one row."""
    value = raw.strip().strip('"')
    if not value or value == "0":
        return ()
    sizes = tuple(int(part) for part in value.split("-"))
    if any(size <= 0 for size in sizes):
        raise ValueError(f"local avalanche sizes must be positive: {raw!r}")
    return sizes


def iter_force_steps(path: Path) -> Iterator[ForceStep]:
    """Stream force steps from one fibril file, retaining the rupture run ID."""
    run_id = 0
    with path.open(newline="", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("f,num_active_particles"):
                continue
            separator = RUN_SEPARATOR_RE.match(stripped)
            if separator:
                run_id = int(separator.group("run_id"))
                continue

            try:
                row = next(csv.reader([line]))
                force = float(row[0])
                num_active = int(row[1])
                total_deleted = int(row[3])
                local_sizes = parse_local_sizes(row[4])
            except (IndexError, ValueError) as exc:
                raise ValueError(f"invalid row in {path}:{line_number}: {stripped}") from exc

            if sum(local_sizes) != total_deleted:
                raise ValueError(
                    f"inconsistent local sizes in {path}:{line_number}: "
                    f"sum={sum(local_sizes)}, total_deleted_rods={total_deleted}"
                )
            yield ForceStep(run_id, force, num_active, total_deleted, local_sizes)


def summarize_file(path: Path) -> dict[str, int]:
    """Return counts for one fibril geometry."""
    match = FILE_RE.match(path.name)
    if not match:
        raise ValueError(f"unexpected rupture filename: {path.name}")

    runs: set[int] = set()
    terminal_runs: set[int] = set()
    force_steps = 0
    nonzero_steps = 0
    preterminal_events = 0
    terminal_events = 0
    preterminal_rods = 0
    terminal_rods = 0
    size_counts: Counter[int] = Counter()

    for step in iter_force_steps(path):
        runs.add(step.run_id)
        force_steps += 1
        if step.local_sizes:
            nonzero_steps += 1
        if step.terminal:
            terminal_runs.add(step.run_id)
            terminal_events += len(step.local_sizes)
            terminal_rods += sum(step.local_sizes)
        else:
            preterminal_events += len(step.local_sizes)
            preterminal_rods += sum(step.local_sizes)
        size_counts.update(step.local_sizes)

    return {
        "ts": int(match.group("ts")),
        "fibril_seed": int(match.group("seed")),
        "weibull_m": int(match.group("m")),
        "runs": len(runs),
        "terminal_runs": len(terminal_runs),
        "force_steps": force_steps,
        "nonzero_force_steps": nonzero_steps,
        "local_events": sum(size_counts.values()),
        "preterminal_events": preterminal_events,
        "terminal_events": terminal_events,
        "rods_in_local_events": preterminal_rods + terminal_rods,
        "preterminal_rods": preterminal_rods,
        "terminal_rods": terminal_rods,
        "singleton_events": size_counts[1],
        "max_local_size": max(size_counts, default=0),
    }


def aggregate_by_ts(rows: list[dict[str, int]]) -> list[dict[str, int]]:
    """Aggregate fibril-level counts without discarding the fibril table."""
    additive = (
        "runs",
        "terminal_runs",
        "force_steps",
        "nonzero_force_steps",
        "local_events",
        "preterminal_events",
        "terminal_events",
        "rods_in_local_events",
        "preterminal_rods",
        "terminal_rods",
        "singleton_events",
    )
    grouped: dict[int, dict[str, int]] = {}
    for row in rows:
        ts = row["ts"]
        summary = grouped.setdefault(
            ts,
            {"ts": ts, "fibrils": 0, **{field: 0 for field in additive}, "max_local_size": 0},
        )
        summary["fibrils"] += 1
        for field in additive:
            summary[field] += row[field]
        summary["max_local_size"] = max(summary["max_local_size"], row["max_local_size"])
    return [grouped[ts] for ts in sorted(grouped)]


def write_csv(path: Path, rows: list[dict[str, int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_root", type=Path, help="Directory containing runs/ts_*/ files")
    parser.add_argument("output_dir", type=Path, help="Directory for count tables")
    parser.add_argument("--ts", type=int, action="append", help="Restrict to one or more Ts values")
    args = parser.parse_args()

    selected_ts = set(args.ts or [])
    paths = sorted(args.data_root.glob("runs/ts_*/*_m_*.txt"))
    if selected_ts:
        paths = [path for path in paths if int(path.parent.name.removeprefix("ts_")) in selected_ts]
    if not paths:
        raise SystemExit("no rupture files matched the requested conditions")

    fibril_rows = [summarize_file(path) for path in paths]
    ts_rows = aggregate_by_ts(fibril_rows)
    write_csv(args.output_dir / "local_event_counts_by_fibril.csv", fibril_rows)
    write_csv(args.output_dir / "local_event_counts_by_ts.csv", ts_rows)

    for row in ts_rows:
        print(
            f"Ts={row['ts']:>4}: fibrils={row['fibrils']}, runs={row['runs']}, "
            f"local_events={row['local_events']}, preterminal={row['preterminal_events']}, "
            f"terminal={row['terminal_events']}, max_size={row['max_local_size']}"
        )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Write one positive local avalanche size per line for each Ts value.

The raw ``avalanche_sizes`` field may contain several hyphen-separated
connected-cluster sizes at one force step.  This script expands that field
without pooling disconnected clusters into a global event.  Zero denotes a
force step with no avalanche and is not written.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from local_avalanche_counts import FILE_RE, iter_force_steps


def _numeric_ts(path: Path) -> int:
    return int(path.name.removeprefix("ts_"))


def extract_ts(ts_dir: Path, output_dir: Path) -> dict[str, object]:
    """Extract all positive local sizes for one Ts directory."""
    ts = _numeric_ts(ts_dir)
    paths = sorted(ts_dir.glob("*_m_*.txt"))
    if not paths:
        raise ValueError(f"no rupture files found in {ts_dir}")

    output_path = output_dir / f"ts_{ts}.txt"
    temporary = output_path.with_suffix(".txt.tmp")
    digest = hashlib.sha256()
    fibril_seeds: set[int] = set()
    weibull_moduli: set[int] = set()
    run_count = 0
    event_count = 0
    singleton_count = 0
    max_size = 0

    with temporary.open("wb") as handle:
        for path in paths:
            match = FILE_RE.match(path.name)
            if match is None:
                raise ValueError(f"unexpected rupture filename: {path.name}")
            if int(match.group("ts")) != ts:
                raise ValueError(f"Ts mismatch between directory and file: {path}")
            fibril_seeds.add(int(match.group("seed")))
            weibull_moduli.add(int(match.group("m")))
            runs: set[int] = set()
            for step in iter_force_steps(path):
                runs.add(step.run_id)
                for size in step.local_sizes:
                    encoded = f"{size}\n".encode("ascii")
                    handle.write(encoded)
                    digest.update(encoded)
                    event_count += 1
                    singleton_count += size == 1
                    max_size = max(max_size, size)
            run_count += len(runs)

    temporary.replace(output_path)
    return {
        "ts": ts,
        "output_file": output_path.name,
        "sha256": digest.hexdigest(),
        "input_files": len(paths),
        "fibrils": len(fibril_seeds),
        "runs": run_count,
        "weibull_moduli": sorted(weibull_moduli),
        "local_events_s_ge_1": event_count,
        "singleton_events_s_eq_1": singleton_count,
        "analysis_events_s_ge_2": event_count - singleton_count,
        "max_local_size": max_size,
        "bytes": output_path.stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_root", type=Path, help="Directory containing runs/ts_*/")
    parser.add_argument("output_dir", type=Path, help="Directory for headerless Ts files")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    ts_dirs = sorted(
        (path for path in (args.data_root / "runs").glob("ts_*") if path.is_dir()),
        key=_numeric_ts,
    )
    if not ts_dirs:
        raise SystemExit("no runs/ts_* directories found")
    if args.workers < 1:
        raise SystemExit("--workers must be at least 1")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []
    with ProcessPoolExecutor(max_workers=min(args.workers, len(ts_dirs))) as executor:
        futures = {
            executor.submit(extract_ts, ts_dir, args.output_dir): ts_dir
            for ts_dir in ts_dirs
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"Ts={result['ts']}: {result['local_events_s_ge_1']} local events "
                f"({result['analysis_events_s_ge_2']} with s>=2)",
                flush=True,
            )

    results.sort(key=lambda result: int(result["ts"]))
    manifest = {
        "format": "headerless UTF-8 text; one positive local connected-cluster size per line",
        "population": "all force steps, including terminal steps; s=1 retained; zero rows omitted",
        "analysis_note": "The accepted manuscript distribution excludes singletons by applying s>=2 later.",
        "input_root": str((args.data_root / "runs").resolve()),
        "conditions": results,
    }
    manifest_path = args.output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote manifest: {manifest_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Extract sparse local-event size frequencies for each fibril geometry."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from local_avalanche_counts import FILE_RE, iter_force_steps


def extract_file(path: Path) -> list[dict[str, int]]:
    match = FILE_RE.match(path.name)
    if match is None:
        raise ValueError(f"unexpected rupture filename: {path.name}")
    counts: Counter[int] = Counter()
    runs: set[int] = set()
    for step in iter_force_steps(path):
        runs.add(step.run_id)
        counts.update(size for size in step.local_sizes if size >= 2)
    return [
        {
            "ts": int(match.group("ts")),
            "fibril_seed": int(match.group("seed")),
            "weibull_m": int(match.group("m")),
            "runs": len(runs),
            "local_size": size,
            "frequency": frequency,
        }
        for size, frequency in sorted(counts.items())
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_root", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    paths = sorted(args.data_root.glob("runs/ts_*/*_m_*.txt"))
    if not paths:
        raise SystemExit("no raw rupture files found")
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output_csv.with_suffix(args.output_csv.suffix + ".tmp")
    fields = ("ts", "fibril_seed", "weibull_m", "runs", "local_size", "frequency")
    fibrils_by_ts: Counter[int] = Counter()
    rows = 0
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
          for index, extracted in enumerate(executor.map(extract_file, paths), start=1):
            writer.writerows(extracted)
            rows += len(extracted)
            fibrils_by_ts[int(extracted[0]["ts"])] += 1
            if index % 25 == 0:
                print(f"parsed {index}/{len(paths)} fibrils", flush=True)
    temporary.replace(args.output_csv)
    manifest = {
        "input_root": str(args.data_root.resolve()),
        "files": len(paths),
        "rows": rows,
        "population": "all local clusters s>=2 including terminal force step",
        "fibrils_by_ts": dict(sorted(fibrils_by_ts.items())),
    }
    manifest_path = args.manifest or args.output_csv.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

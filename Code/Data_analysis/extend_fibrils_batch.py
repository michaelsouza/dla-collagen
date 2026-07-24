#!/usr/bin/env python3
"""Expand compact collagen fibrils into their 18-site rod representation."""

from __future__ import annotations

import argparse
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path


FIBRIL_NAME = re.compile(
    r"dla_mode_s_ts_(?P<ts>\d+)_.*seed_(?P<seed>\d+)_.*\.dat"
)


@dataclass(frozen=True)
class ExtensionResult:
    source: Path
    destination: Path
    molecules: int
    occupied_sites: int
    status: str


def extended_filename(source_name: str) -> str:
    match = FIBRIL_NAME.fullmatch(source_name)
    if match is None:
        raise ValueError(f"Unrecognized fibril filename: {source_name}")
    return f"ts_{match.group('ts')}_seed_{match.group('seed')}.dat"


def read_compact_molecules(source: Path):
    with source.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            fields = line.split()
            if not fields or fields[0] != "uid:":
                continue
            if len(fields) != 5:
                raise ValueError(
                    f"{source}:{line_number}: expected 5 fields, found {len(fields)}"
                )
            try:
                rid, x, y, z = map(int, fields[1:])
            except ValueError as error:
                raise ValueError(
                    f"{source}:{line_number}: coordinates must be integers"
                ) from error
            yield rid, x, y, z


def extend_fibril(
    source: Path,
    destination: Path,
    *,
    rod_length: int = 18,
    overwrite: bool = False,
) -> ExtensionResult:
    if rod_length <= 0:
        raise ValueError("rod_length must be positive")

    if destination.exists() and not overwrite:
        return ExtensionResult(source, destination, 0, 0, "skipped")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    molecules = 0

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as output:
            temporary_path = Path(output.name)
            output.write("id uid x y z\n")
            for rid, x, y, z in read_compact_molecules(source):
                molecules += 1
                for offset in range(rod_length):
                    output.write(f"uid {rid} {x} {y + offset} {z}\n")

        if molecules == 0:
            raise ValueError(f"No compact molecule records found in {source}")

        os.replace(temporary_path, destination)
    except Exception:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise

    return ExtensionResult(
        source,
        destination,
        molecules,
        molecules * rod_length,
        "written",
    )


def discover_inputs(input_directory: Path, pattern: str, limit: int | None):
    sources = sorted(input_directory.glob(pattern))
    if limit is not None:
        if limit <= 0:
            raise ValueError("limit must be positive")
        sources = sources[:limit]
    if not sources:
        raise ValueError(
            f"No input files matching {pattern!r} in {input_directory}"
        )
    return sources


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Expand each compact collagen molecule into consecutive lattice "
            "sites along y."
        )
    )
    parser.add_argument("input_directory", type=Path)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--pattern", default="*.dat")
    parser.add_argument("--rod-length", type=int, default=18)
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing extended file. The default is to skip it.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate filenames and show destinations without writing files.",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    sources = discover_inputs(args.input_directory, args.pattern, args.limit)

    destinations = {}
    for source in sources:
        destination = args.output_directory / extended_filename(source.name)
        if destination in destinations:
            raise ValueError(
                f"Output collision: {source} and {destinations[destination]}"
            )
        destinations[destination] = source

    written = 0
    skipped = 0
    total_molecules = 0
    total_sites = 0

    for destination, source in destinations.items():
        if args.dry_run:
            print(f"would write {source} -> {destination}")
            continue

        result = extend_fibril(
            source,
            destination,
            rod_length=args.rod_length,
            overwrite=args.overwrite,
        )
        if result.status == "written":
            written += 1
            total_molecules += result.molecules
            total_sites += result.occupied_sites
            print(
                f"written {destination.name}: "
                f"{result.molecules} molecules, "
                f"{result.occupied_sites} occupied sites"
            )
        else:
            skipped += 1
            print(f"skipped existing {destination}")

    if args.dry_run:
        print(f"validated {len(destinations)} input files")
    else:
        print(
            f"summary: written={written}, skipped={skipped}, "
            f"molecules={total_molecules}, occupied_sites={total_sites}"
        )


if __name__ == "__main__":
    main()

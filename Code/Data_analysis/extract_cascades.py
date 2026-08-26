#!/usr/bin/env python3
"""Reduce the campaign runs to per-realization histograms of CASCADE size.

The cascade -- every rod that goes in one quasi-static load step, including the
consequential structural removals -- is the primary observable of the quenched
protocol.  It is `total_deleted_rods` in the legacy schema, column 3.  The
per-cascade decomposition into connected clusters (column 4) is a separate
observable and is not touched here.

For each condition (Ts, m) this writes a CSR matrix with one ROW PER
REALIZATION and one column per cascade size, plus the fibril each row belongs
to, which is what the block bootstrap resamples.  The terminal cascade of every
realization -- the one that takes the last rod out -- is stored separately, as
the existing pipeline does for clusters: it is not a critical-point event and
including it contaminates the tail.

    extract_cascades.py --runs-dir DIR --out DIR [--workers N]
"""
from __future__ import annotations

import argparse
import os
import re
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy import sparse

NAME = re.compile(r"ts_(\d+)_seed_(\d+)_m_(\d+)\.txt")
SEP = re.compile(r"^-+\d+$")


def read_file(path):
    """Return (preterminal, terminal) lists of Counter, one entry per run."""
    pre, term = [], []
    current = Counter()
    last = 0
    with open(path) as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line or line.startswith("f,"):
                continue
            if SEP.match(line):
                if last:
                    current[last] -= 1
                    if current[last] == 0:
                        del current[last]
                pre.append(current)
                term.append(Counter({last: 1}) if last else Counter())
                current, last = Counter(), 0
                continue
            size = int(line.split(",", 4)[3])
            if size > 0:
                current[size] += 1
                last = size
    if last:
        current[last] -= 1
        if current[last] == 0:
            del current[last]
    pre.append(current)
    term.append(Counter({last: 1}) if last else Counter())
    return pre, term


def to_csr(rows, width):
    data, indices, indptr = [], [], [0]
    for row in rows:
        for size, count in sorted(row.items()):
            indices.append(size)
            data.append(count)
        indptr.append(len(indices))
    return sparse.csr_matrix(
        (np.array(data, dtype=np.int64), np.array(indices, dtype=np.int64),
         np.array(indptr, dtype=np.int64)),
        shape=(len(rows), width))


def job(path):
    pre, term = read_file(path)
    peak = max((max(r) if r else 0) for r in pre + term)
    return path, pre, term, peak


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    by_cond = {}
    for root, _dirs, files in os.walk(args.runs_dir):
        for name in files:
            m = NAME.fullmatch(name)
            if m:
                key = (int(m.group(1)), int(m.group(3)))
                by_cond.setdefault(key, []).append(
                    (int(m.group(2)), os.path.join(root, name)))

    for (ts, mod) in sorted(by_cond):
        items = sorted(by_cond[(ts, mod)])
        paths = [p for _s, p in items]
        with ProcessPoolExecutor(args.workers) as pool:
            out = list(pool.map(job, paths, chunksize=4))
        width = max(o[3] for o in out) + 1
        pre_rows, term_rows, fibril = [], [], []
        for index, (_path, pre, term, _peak) in enumerate(out):
            pre_rows.extend(pre)
            term_rows.extend(term)
            fibril.extend([index] * len(pre))
        stem = f"{args.out}/casc_ts{ts}_m{mod}"
        sparse.save_npz(f"{stem}_pre.npz", to_csr(pre_rows, width))
        sparse.save_npz(f"{stem}_term.npz", to_csr(term_rows, width))
        np.save(f"{stem}_fibril.npy", np.asarray(fibril, dtype=np.int32))
        total = sum(sum(r.values()) for r in pre_rows)
        print(f"ts={ts:<5} m={mod:<3} fibrilas={len(paths):>4} "
              f"runs={len(pre_rows):>6} cascatas={total:>9} smax={width - 1}",
              flush=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Cross-sectional diameter of a fibril as a function of position along its axis.

The fibril is grown from a seed rod spanning y in [-9, 8] and is far longer
than it is wide: the bounding box of a 30000-molecule fibril measures ~3400-3800
lattice sites in y against ~35-85 in x and z.  So y is the axis, and a
cross-section is the set of particles sharing one y.

Two diameters are reported per section, because they answer different questions
and disagree in a way that is itself informative for a fractal aggregate:

  d_gyr = 2 * sqrt(<|r - r_c|^2>)   the gyration diameter, a second moment; it
                                    weighs the bulk and is insensitive to a
                                    single far particle
  d_max = 2 * max|r - r_c|          the enclosing diameter, set by the single
                                    most distant particle -- the quantity the
                                    published mass-radius fits use

Input is the COMPACT generator output, one line per molecule, and the 18
lattice layers of each molecule are expanded in memory.  This follows
validate_fractal_proxy.py: the expanded files carry the same information at 18x
the size, so there is no reason to read them.

    fibril_diameter_profile.py --compact-dir DIR --out-csv FILE [--ts 2 ...]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict

import numpy as np

ROD_HEIGHT = 18
COMPACT_RE = re.compile(r'dla_mode_s_ts_(\d+)_nb_(\d+)_seed_(\d+)_\.dat')


def read_compact(path):
    """Return (x, y_base, z) int arrays, one entry per molecule.

    The generator writes 'uid: <id> <x> <y> <z>', where y is the BASE of the
    rod; the molecule occupies y .. y + ROD_HEIGHT - 1.
    """
    with open(path) as fh:
        text = fh.read()
    # np.loadtxt is far too slow for 30001 lines x hundreds of fibrils.  Every
    # line is 'uid: <id> <x> <y> <z>', so the whole file parses as one flat
    # array of five integers per line.
    flat = np.fromstring(text.replace('uid:', ''), dtype=np.int64, sep=' ')
    if flat.size % 4:
        raise ValueError(f'{path}: expected 4 integers per line, got {flat.size}')
    rows = flat.reshape(-1, 4)
    return rows[:, 1], rows[:, 2], rows[:, 3]


def diameter_profile(x, y_base, z):
    """Per-layer (y, count, d_gyr, d_max) for one fibril.

    Each molecule contributes one particle to each of its ROD_HEIGHT layers at
    the same (x, z).  Rather than materialising every particle, the layer sums
    are accumulated directly: for a fixed offset every molecule shifts by the
    same amount in y, so the whole fibril is folded in ROD_HEIGHT passes.
    """
    y_min = int(y_base.min())
    y_max = int(y_base.max()) + ROD_HEIGHT - 1
    n_layers = y_max - y_min + 1

    count = np.zeros(n_layers, dtype=np.int64)
    sx = np.zeros(n_layers); sz = np.zeros(n_layers)
    sxx = np.zeros(n_layers); szz = np.zeros(n_layers)

    xf = x.astype(np.float64); zf = z.astype(np.float64)
    for offset in range(ROD_HEIGHT):
        idx = (y_base - y_min) + offset
        np.add.at(count, idx, 1)
        np.add.at(sx, idx, xf)
        np.add.at(sz, idx, zf)
        np.add.at(sxx, idx, xf * xf)
        np.add.at(szz, idx, zf * zf)

    ys = np.arange(y_min, y_max + 1)
    occupied = count > 0
    n = np.maximum(count, 1)
    cx = sx / n
    cz = sz / n
    # <|r - r_c|^2> = <x^2> - <x>^2 + <z^2> - <z>^2
    var = (sxx / n - cx * cx) + (szz / n - cz * cz)
    d_gyr = 2.0 * np.sqrt(np.maximum(var, 0.0))

    # d_max needs the actual extremes, so make one more pass per offset.
    max_r2 = np.zeros(n_layers)
    for offset in range(ROD_HEIGHT):
        idx = (y_base - y_min) + offset
        dx = xf - cx[idx]
        dz = zf - cz[idx]
        np.maximum.at(max_r2, idx, dx * dx + dz * dz)
    d_max = 2.0 * np.sqrt(max_r2)

    return ys[occupied], count[occupied], d_gyr[occupied], d_max[occupied]


def accumulate(paths, limit=None):
    """Mean profiles over fibrils, keyed by y.  Returns dict y -> stats."""
    acc = defaultdict(lambda: {'n': 0, 'g': 0.0, 'gg': 0.0, 'm': 0.0, 'c': 0.0})
    used = 0
    for path in paths[:limit] if limit else paths:
        try:
            x, yb, z = read_compact(path)
        except Exception as exc:                      # noqa: BLE001
            print(f'skip {os.path.basename(path)}: {exc}', file=sys.stderr)
            continue
        ys, count, d_gyr, d_max = diameter_profile(x, yb, z)
        for y, c, g, m in zip(ys, count, d_gyr, d_max):
            a = acc[int(y)]
            a['n'] += 1
            a['g'] += g
            a['gg'] += g * g
            a['m'] += m
            a['c'] += c
        used += 1
    return acc, used


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--compact-dir', required=True)
    ap.add_argument('--out-csv', required=True)
    ap.add_argument('--ts', type=int, action='append',
                    help='condition to include; repeatable (default: all found)')
    ap.add_argument('--fibrils', type=int, default=25,
                    help='fibrils per condition (default 25)')
    args = ap.parse_args(argv)

    by_ts = defaultdict(list)
    for name in sorted(os.listdir(args.compact_dir)):
        match = COMPACT_RE.fullmatch(name)
        if match:
            by_ts[int(match.group(1))].append(os.path.join(args.compact_dir, name))

    wanted = args.ts if args.ts else sorted(by_ts)
    with open(args.out_csv, 'w') as fh:
        fh.write('ts,y,n_fibrils,mean_count,mean_d_gyr,se_d_gyr,mean_d_max\n')
        for ts in wanted:
            paths = by_ts.get(ts)
            if not paths:
                print(f'no fibrils for ts={ts}', file=sys.stderr)
                continue
            acc, used = accumulate(paths, args.fibrils)
            print(f'ts={ts}: {used} fibrils, {len(acc)} layers', file=sys.stderr)
            for y in sorted(acc):
                a = acc[y]
                n = a['n']
                mean_g = a['g'] / n
                # SE across fibrils; undefined for a single contributor.
                if n > 1:
                    var = max(a['gg'] / n - mean_g * mean_g, 0.0)
                    se = (var / (n - 1)) ** 0.5
                else:
                    se = float('nan')
                fh.write(f'{ts},{y},{n},{a["c"] / n:.4f},{mean_g:.6f},'
                         f'{se:.6f},{a["m"] / n:.6f}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

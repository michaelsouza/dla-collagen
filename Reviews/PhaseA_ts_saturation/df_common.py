"""D_f on a common radius window, comparable across T_s.

The published pipeline takes its radius grid and fit window from a per-T_s
xmgrace project, so it cannot score T_s values that were never published. Here
every condition is fitted on the SAME window, which is what makes the
comparison across T_s internally consistent. Absolute values are therefore not
expected to match the published ones -- only the trend matters.

Reuses parse_grown_sections and mass_radius_for_sections from the repository
so the section sampling and mass counting stay identical.
"""
import sys, glob, re, os
from pathlib import Path
import numpy as np
from scipy.stats import linregress

sys.path.insert(0, '/home/michael/gitrepos/dla-collagen/Code/Data_analysis')
from validate_fractal_proxy import parse_grown_sections, mass_radius_for_sections

LOG_R = np.linspace(np.log10(1.5), np.log10(12.0), 14)   # common window
RADII = np.power(10.0, LOG_R)


def df_of_file(path):
    sections = parse_grown_sections(Path(path))
    mean_mass, desc = mass_radius_for_sections(sections, RADII)
    if np.any(mean_mass <= 0):
        return None
    fit = linregress(LOG_R, np.log10(mean_mass))
    return {'df': float(fit.slope), 'se': float(fit.stderr),
            'r2': float(fit.rvalue ** 2), 'n': desc['full_mean_n_11'],
            'radius': desc['full_mean_radius_11']}


def main():
    rows = {}
    for pattern in sys.argv[1:]:
        for path in glob.glob(pattern):
            m = re.search(r'_ts_(\d+)_.*seed_(\d+)_', os.path.basename(path))
            if not m:
                continue
            ts, seed = int(m.group(1)), int(m.group(2))
            r = df_of_file(path)
            if r:
                rows.setdefault(ts, []).append(r)
    print(f'{"Ts":>7} {"n_fib":>6} {"Df":>8} {"sd":>7} {"R2":>7} '
          f'{"<N>":>8} {"raio":>7}')
    for ts in sorted(rows):
        v = rows[ts]
        d = np.array([x['df'] for x in v])
        print(f'{ts:>7} {len(v):>6} {d.mean():>8.4f} '
              f'{(d.std(ddof=1) if len(d) > 1 else float("nan")):>7.4f} '
              f'{np.mean([x["r2"] for x in v]):>7.4f} '
              f'{np.mean([x["n"] for x in v]):>8.1f} '
              f'{np.mean([x["radius"] for x in v]):>7.2f}')


if __name__ == '__main__':
    main()

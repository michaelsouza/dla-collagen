#!/usr/bin/env python3
"""Compaction of the fibril cross-section with T_s, without any fitted exponent.

Two observables, both free of a fit window:

  coordination   fraction of a particle's 4 lattice neighbours that are
                 occupied.  No centroid, no radius, no window -- a purely local
                 count.  0 for an isolated particle, 1 deep inside a solid.

  rho(r)         local density N(r) / (pi r^2) of a cross-section.  A compact
                 object has rho flat in r; a fractal of dimension D has
                 rho ~ r^(D-2), so the DECAY of rho is the fractal signature.
                 The ratio rho(3)/rho(R/2) turns that decay into one number,
                 and implies D = 2 + ln(ratio)/ln(6/R) with nothing fitted.

Writes compaction.json for the plotting script.
"""
import os, sys, json
import numpy as np
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_fractal_proxy import parse_grown_sections, mass_radius_for_sections

ROOT = "/petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign"
D_IN = f"{ROOT}/fibrils/compact"
OUT = f"{ROOT}/analysis/compaction"
TS = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]
RAD = np.power(10.0, np.linspace(np.log10(1.0), np.log10(64.0), 96))
R_INNER = 3.0                       # lattice cutoff: below this we count pixels
NEIGH = ((1, 0), (-1, 0), (0, 1), (0, -1))


def coordination(sections):
    vals = []
    for sec in sections:
        occ = set(map(tuple, sec.astype(int)))
        total = sum(sum(((x + dx, z + dz) in occ) for dx, dz in NEIGH)
                    for x, z in occ)
        vals.append(total / (4 * len(occ)))
    return float(np.mean(vals))


def main():
    nfib = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    os.makedirs(OUT, exist_ok=True)
    res = {"radii": RAD.tolist()}
    print(f"{'Ts':>5} {'R':>6} {'coord':>14} {'rho(3)/rho(R/2)':>18} {'D implicito':>13}")
    for ts in TS:
        files = [f for f in sorted(os.listdir(D_IN))
                 if f.startswith(f"dla_mode_s_ts_{ts}_nb_")][:nfib]
        coord, ratio, radius, profiles = [], [], [], []
        for f in files:
            sec = parse_grown_sections(Path(os.path.join(D_IN, f)))
            mass, desc = mass_radius_for_sections(sec, RAD)
            R = desc["full_mean_radius_11"]
            rho = mass / (np.pi * RAD ** 2)
            coord.append(coordination(sec))
            radius.append(R)
            ratio.append(np.interp(R_INNER, RAD, rho) / np.interp(R / 2, RAD, rho))
            # profile on r/R so conditions of different size are comparable
            profiles.append(np.interp(np.linspace(0.05, 1.15, 80), RAD / R, rho))
        n = len(files)

        def stat(v):
            v = np.asarray(v, dtype=float)
            return [float(v.mean()), float(v.std(ddof=1) / np.sqrt(n))]

        Rm = float(np.mean(radius))
        rm = float(np.mean(ratio))
        implied = 2.0 + np.log(rm) / np.log(2 * R_INNER / Rm)
        res[str(ts)] = {"n": n, "R": stat(radius), "coord": stat(coord),
                        "ratio": stat(ratio), "implied_D": float(implied),
                        "profile": np.mean(profiles, axis=0).tolist(),
                        "profile_x": np.linspace(0.05, 1.15, 80).tolist()}
        print(f"{ts:>5} {Rm:>6.1f} {res[str(ts)]['coord'][0]:>8.3f}±{res[str(ts)]['coord'][1]:<5.3f}"
              f" {rm:>12.3f}±{res[str(ts)]['ratio'][1]:<5.3f} {implied:>13.3f}")
    json.dump(res, open(f"{OUT}/compaction.json", "w"))
    print("wrote", f"{OUT}/compaction.json")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fit the Araujo et al. (2003) ansatz to the cascade sizes of every condition.

    F(s) ~ s^-alpha exp[-(s/s_c)^eta]

written as a probability mass function, p(s) proportional to
s^-gamma exp[-(s/s_c)^eta].  eta = 1 is the ordinary exponential cutoff, so the
extra parameter is testable by a likelihood ratio on one degree of freedom.

For every condition this records the three parameters with a block bootstrap
over fibrils, the likelihood ratio against eta = 1, and the KS distance of the
four competing families on the identical tail.

    run_araujo.py --cascades DIR --stats CSV --out CSV [--replicates N]
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys

import numpy as np
from scipy import sparse, stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avalanche_statistics import (          # noqa: E402
    fit_cutoff_power_law,
    fit_discrete_lognormal,
    fit_generalized_cutoff,
    fit_stretched_exponential,
    hierarchical_resample_fibril_counts,
)


def blocks(matrix, fibril):
    return [matrix[np.flatnonzero(fibril == i)] for i in np.unique(fibril)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cascades", required=True)
    ap.add_argument("--stats", required=True,
                    help="cascade_stats_clauset.csv, for the floor-constrained xmin")
    ap.add_argument("--out", required=True)
    ap.add_argument("--replicates", type=int, default=120)
    ap.add_argument("--seed", type=int, default=12738)
    args = ap.parse_args()

    xmins = {(int(r["ts"]), int(r["m"])): int(r["xmin_floor"])
             for r in csv.DictReader(open(args.stats))}

    fields = ["ts", "m", "xmin", "n_tail",
              "gamma", "se_gamma", "s_c", "se_s_c", "eta", "se_eta",
              "lr_vs_exponential", "p_lr", "d_B_implied",
              "ks_araujo", "ks_exponential", "ks_lognormal", "ks_stretched",
              "best_model"]
    with open(args.out, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for (ts, mod) in sorted(xmins):
            stem = f"{args.cascades}/casc_ts{ts}_m{mod}"
            pre = sparse.csr_matrix(sparse.load_npz(f"{stem}_pre.npz"))
            fibril = np.load(f"{stem}_fibril.npy")
            counts = np.asarray(pre.sum(axis=0)).ravel()
            xmin = xmins[(ts, mod)]

            araujo = fit_generalized_cutoff(counts, xmin=xmin)
            exponential = fit_cutoff_power_law(counts, xmin=xmin)
            lognormal = fit_discrete_lognormal(counts, xmin=xmin)
            stretched = fit_stretched_exponential(counts, xmin=xmin)

            statistic = 2.0 * (araujo.log_likelihood - exponential.log_likelihood)
            p_lr = float(stats.chi2.sf(max(statistic, 0.0), df=1))

            rng = np.random.default_rng(args.seed + 1000 * ts + mod)
            block = blocks(pre, fibril)
            draws = []
            for _ in range(args.replicates):
                rows = hierarchical_resample_fibril_counts(block, rng=rng)
                fit = fit_generalized_cutoff(rows.sum(axis=0), xmin=xmin)
                draws.append((fit.parameters["gamma"], fit.parameters["s_c"],
                              fit.parameters["eta"]))
            draws = np.asarray(draws, dtype=float)

            ks = {"araujo": araujo.ks, "exponential": exponential.ks,
                  "lognormal": lognormal.ks, "stretched": stretched.ks}
            best = min(ks, key=ks.get)

            # Araujo's own reading: alpha = d/d_B - 1 with alpha = gamma - 1,
            # so d_B = d/gamma.  Recorded to be CHECKED, not assumed: the
            # relation comes from percolation blob statistics and there is no
            # reason for a fiber-bundle cascade to obey it.
            d_B = 2.0 / araujo.parameters["gamma"]

            writer.writerow(dict(
                ts=ts, m=mod, xmin=xmin, n_tail=int(araujo.n),
                gamma=round(araujo.parameters["gamma"], 4),
                se_gamma=round(float(draws[:, 0].std(ddof=1)), 4),
                s_c=round(araujo.parameters["s_c"], 2),
                se_s_c=round(float(draws[:, 1].std(ddof=1)), 2),
                eta=round(araujo.parameters["eta"], 4),
                se_eta=round(float(draws[:, 2].std(ddof=1)), 4),
                lr_vs_exponential=round(statistic, 1),
                p_lr=f"{p_lr:.3e}",
                d_B_implied=round(d_B, 3),
                ks_araujo=round(araujo.ks, 6),
                ks_exponential=round(exponential.ks, 6),
                ks_lognormal=round(lognormal.ks, 6),
                ks_stretched=round(stretched.ks, 6),
                best_model=best))
            handle.flush()
            print(f"ts={ts:<5} m={mod:<3} gamma={araujo.parameters['gamma']:.3f}"
                  f"±{draws[:,0].std(ddof=1):.3f} eta={araujo.parameters['eta']:.2f}"
                  f"±{draws[:,2].std(ddof=1):.2f} s_c={araujo.parameters['s_c']:.1f}"
                  f" | LR={statistic:.0f} | melhor={best}", flush=True)
    print("wrote", args.out)


if __name__ == "__main__":
    main()

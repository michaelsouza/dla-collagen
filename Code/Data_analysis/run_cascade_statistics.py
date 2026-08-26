#!/usr/bin/env python3
"""Clauset analysis of CASCADE sizes, per (T_s, m), on the full campaign.

The primary estimand is the preterminal cascade-size distribution: for every
condition, x_min is selected by minimising the discrete KS distance, gamma is
the exact discrete MLE, the fit is tested against a semiparametric
goodness-of-fit, and the uncertainty comes from a block bootstrap whose block
is the FIBRIL -- runs within a fibril share a topology and are not independent.

Everything but the cascade extraction reuses avalanche_statistics.py, which the
existing test suite covers.

    run_cascade_stats.py --cascades DIR --out FILE [--replicates N]
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys

import numpy as np
from scipy import sparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avalanche_statistics import (          # noqa: E402
    clauset_power_law_gof,
    fit_competing_models,
    fit_cutoff_power_law,
    cutoff_power_law_likelihood_ratio_test,
    fit_discrete_power_law,
    hierarchical_resample_fibril_counts,
    select_power_law_xmin,
    vuong_likelihood_ratio,
)

STEM = re.compile(r"casc_ts(\d+)_m(\d+)_pre\.npz")


def blocks(matrix, fibril):
    """Split the run-by-size matrix into one CSR per fibril block."""
    out = []
    for index in np.unique(fibril):
        out.append(matrix[np.flatnonzero(fibril == index)])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cascades", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--replicates", type=int, default=400,
                    help="block-bootstrap replicates (default 400)")
    ap.add_argument("--gof-replicates", type=int, default=2500,
                    help="Clauset's rule: >= 1/(4 eps^2); 2500 gives eps=0.01")
    ap.add_argument("--lr-replicates", type=int, default=500)
    ap.add_argument("--min-tail", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed", type=int, default=12738)
    args = ap.parse_args()

    conditions = []
    for name in sorted(os.listdir(args.cascades)):
        m = STEM.fullmatch(name)
        if m:
            conditions.append((int(m.group(1)), int(m.group(2))))
    conditions.sort()

    fields = ["ts", "m", "n_fibrils", "n_runs", "n_cascades", "s_max",
              "xmin", "gamma", "se_gamma", "ci_lo", "ci_hi", "n_tail",
              "ks", "gof_p", "lr_stat", "lr_p", "mean_size", "p99_size",
              # The pure power law is rejected almost everywhere, so the
              # cutoff model's parameters are the ones worth quoting.
              "cut_gamma", "cut_se_gamma", "cut_lambda", "cut_sc", "cut_ks",
              # xmin selection is unstable at m=10, where the KS minimum can
              # land on a far tail holding 0.2% of the events.  A floor on the
              # tail size shows whether a fit is that kind of artifact.
              "xmin_floor", "gamma_floor", "n_tail_floor",
              # Same fits repeated on the floor-constrained xmin.  The
              # unconstrained KS minimum lands on a 0.2%-of-the-data far tail
              # in four m=10 conditions, and the cutoff model inherits that
              # instability because it shares xmin.  These columns are the ones
              # that are comparable across the grid.
              "cutf_gamma", "cutf_se_gamma", "cutf_sc",
              # Table 1 of Clauset et al.: the three NON-nested alternatives,
              # each by the normalized ratio of eq. (C.6).  A positive R
              # favours the power law; the p-value is two-sided.
              "R_lognorm", "p_lognorm", "R_exp", "p_exp",
              "R_stretch", "p_stretch", "beta_stretch",
              "verdict"]
    with open(args.out, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()

        for ts, mod in conditions:
            stem = f"{args.cascades}/casc_ts{ts}_m{mod}"
            pre = sparse.csr_matrix(sparse.load_npz(f"{stem}_pre.npz"))
            fibril = np.load(f"{stem}_fibril.npy")
            counts = np.asarray(pre.sum(axis=0)).ravel()
            per_fibril = np.asarray(
                [np.asarray(pre[np.flatnonzero(fibril == i)].sum(axis=0)).ravel()
                 for i in np.unique(fibril)], dtype=np.int64)

            gof = clauset_power_law_gof(
                counts, min_tail=args.min_tail, replicates=args.gof_replicates,
                fibril_counts=per_fibril, min_fibrils=2,
                workers=args.workers, seed=args.seed)
            fit = gof.observed_fit
            xmin = int(fit.xmin)

            # Block bootstrap: resample fibrils, then runs within each fibril.
            rng = np.random.default_rng(args.seed + 1000 * ts + mod)
            block = blocks(pre, fibril)
            draws = []
            for _ in range(args.replicates):
                rows = hierarchical_resample_fibril_counts(block, rng=rng)
                draws.append(fit_discrete_power_law(
                    rows.sum(axis=0), xmin=xmin, compute_ks=False).parameters["gamma"])
            draws = np.asarray(draws, dtype=float)

            lr = cutoff_power_law_likelihood_ratio_test(
                counts, xmin=xmin, replicates=args.lr_replicates,
                seed=args.seed, workers=args.workers)

            cut = fit_cutoff_power_law(counts, xmin=xmin)
            cut_draws = []
            rng2 = np.random.default_rng(args.seed + 7 + 1000 * ts + mod)
            for _ in range(max(args.replicates // 4, 40)):
                rows = hierarchical_resample_fibril_counts(block, rng=rng2)
                cut_draws.append(fit_cutoff_power_law(
                    rows.sum(axis=0), xmin=xmin).parameters["gamma"])
            cut_draws = np.asarray(cut_draws, dtype=float)

            floor = select_power_law_xmin(
                counts, min_tail=max(int(0.05 * counts.sum()), 1000),
                fibril_counts=per_fibril, min_fibrils=2)

            models = fit_competing_models(counts, xmin=xmin)
            power = models["power_law"]
            alt = {}
            for name in ("lognormal", "exponential", "stretched_exponential"):
                ratio, normalized, p_alt = vuong_likelihood_ratio(
                    power, models[name], counts)
                alt[name] = (normalized, p_alt)

            # Clauset's Box 1: p > 0.1 keeps the power law alive, otherwise it
            # is rejected.  An alternative counts as favoured when its ratio is
            # negative AND the two-sided p-value is significant.
            if gof.p_value > 0.1:
                favoured = [n for n, (r, pv) in alt.items() if r < 0 and pv < 0.05]
                if lr.p_value < 0.05:
                    favoured.append("cutoff")
                verdict = "power law plausible" if not favoured else (
                    "power law plausible; also " + "/".join(favoured))
            else:
                better = [n for n, (r, pv) in alt.items() if r < 0 and pv < 0.05]
                if lr.p_value < 0.05:
                    better.insert(0, "cutoff")
                verdict = "rejected" + (" -> " + "/".join(better) if better else "")

            xmin_f = int(floor.xmin)
            cutf = fit_cutoff_power_law(counts, xmin=xmin_f)
            cutf_draws = []
            rng3 = np.random.default_rng(args.seed + 13 + 1000 * ts + mod)
            for _ in range(max(args.replicates // 4, 40)):
                rowsf = hierarchical_resample_fibril_counts(block, rng=rng3)
                cutf_draws.append(fit_cutoff_power_law(
                    rowsf.sum(axis=0), xmin=xmin_f).parameters["gamma"])
            cutf_draws = np.asarray(cutf_draws, dtype=float)

            sizes = np.arange(len(counts))
            total = counts.sum()
            mean = float((sizes * counts).sum() / total)
            cdf = np.cumsum(counts) / total
            p99 = int(sizes[np.searchsorted(cdf, 0.99)])

            row = dict(
                ts=ts, m=mod, n_fibrils=len(np.unique(fibril)),
                n_runs=pre.shape[0], n_cascades=int(total),
                s_max=int(sizes[counts > 0].max()),
                xmin=xmin, gamma=round(float(fit.parameters["gamma"]), 4),
                se_gamma=round(float(draws.std(ddof=1)), 4),
                ci_lo=round(float(np.percentile(draws, 2.5)), 4),
                ci_hi=round(float(np.percentile(draws, 97.5)), 4),
                n_tail=int(fit.n), ks=round(float(fit.ks), 5),
                gof_p=round(float(gof.p_value), 4),
                lr_stat=round(float(lr.observed_likelihood_ratio), 3),
                lr_p=round(float(lr.p_value), 4),
                mean_size=round(mean, 3), p99_size=p99,
                cut_gamma=round(float(cut.parameters["gamma"]), 4),
                cut_se_gamma=round(float(cut_draws.std(ddof=1)), 4),
                cut_lambda=round(float(cut.parameters["lambda"]), 6),
                cut_sc=round(1.0 / float(cut.parameters["lambda"]), 2)
                if cut.parameters["lambda"] > 0 else float("inf"),
                cut_ks=round(float(cut.ks), 5),
                xmin_floor=int(floor.xmin),
                gamma_floor=round(float(floor.parameters["gamma"]), 4),
                n_tail_floor=int(floor.n),
                cutf_gamma=round(float(cutf.parameters["gamma"]), 4),
                cutf_se_gamma=round(float(cutf_draws.std(ddof=1)), 4),
                cutf_sc=round(1.0 / float(cutf.parameters["lambda"]), 2)
                if cutf.parameters["lambda"] > 0 else float("inf"),
                R_lognorm=round(alt["lognormal"][0], 2),
                p_lognorm=round(alt["lognormal"][1], 4),
                R_exp=round(alt["exponential"][0], 2),
                p_exp=round(alt["exponential"][1], 4),
                R_stretch=round(alt["stretched_exponential"][0], 2),
                p_stretch=round(alt["stretched_exponential"][1], 4),
                beta_stretch=round(
                    float(models["stretched_exponential"].parameters["beta"]), 4),
                verdict=verdict)
            writer.writerow(row)
            handle.flush()
            print(f"ts={ts:<5} m={mod:<3} xmin={xmin:<3} "
                  f"gamma={row['gamma']:.3f}±{row['se_gamma']:.3f} "
                  f"n_tail={row['n_tail']:>8} gof_p={row['gof_p']:.3f} | "
                  f"corte: g={row['cut_gamma']:.3f}±{row['cut_se_gamma']:.3f} "
                  f"s_c={row['cut_sc']:>8.1f} | piso: xmin={row['xmin_floor']:<3} "
                  f"g={row['gamma_floor']:.3f} | {row['verdict']}", flush=True)
    print("wrote", args.out)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Phase B: how many realizations per fibril, and how many fibrils, are needed.

The two axes obey different rules and are decided separately.

Realizations.  The variance of an ensemble estimator decomposes as

    Var = sigma2_between / n_fib  +  sigma2_within / (n_fib * n_real)

so realizations only attack the second term.  From the intraclass correlation
rho = sigma2_b / (sigma2_b + sigma2_w), the point beyond which realizations
contribute less than 10% of the total variance is

    n_real >= 10 * (1 - rho) / rho

Under a fixed compute budget C = n_fib * n_real the variance becomes
(n_real * sigma2_b + sigma2_w) / C, which is INCREASING in n_real: for the same
cost, more fibrils always beat more realizations per fibril.

Fibrils.  Reported as a sequential curve: the block-bootstrap standard error of
each target metric as fibrils accumulate, so a campaign can stop per condition
when the precision target is met instead of at a fixed size.

Reads the same layout read_avalanche_runs.py expects, and reuses its parser so
the invariants are checked on the way in.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from read_avalanche_runs import (  # noqa: E402
    discover_run_files,
    iter_force_steps,
)

# Metrics whose precision drives the campaign.  gamma is the slowest to
# converge and therefore governs the stopping rule.
METRICS = ("f_rupture", "mean_size", "p99_size", "gamma")


def gamma_mle(sizes: np.ndarray, s_min: int) -> float:
    """Discrete power-law exponent above s_min, by maximum likelihood.

    Hill-type estimator for the discrete tail; adequate for a convergence
    study, where what matters is how the estimate's dispersion shrinks rather
    than the absolute value.
    """
    tail = sizes[sizes >= s_min]
    if tail.size < 50:
        return math.nan
    return 1.0 + tail.size / np.log(tail / (s_min - 0.5)).sum()


def realization_metrics(steps) -> dict[str, float] | None:
    """Collapse one realization into its target metrics."""
    sizes, forces, terminal = [], [], None
    for step in steps:
        if step.is_terminal:
            terminal = step.force
            continue
        if step.total_deleted_rods > 0:
            sizes.append(step.total_deleted_rods)
            forces.append(step.force)
    if not sizes or terminal is None:
        return None
    arr = np.asarray(sizes, dtype=float)
    return {
        "f_rupture": float(terminal),
        "mean_size": float(arr.mean()),
        "p99_size": float(np.percentile(arr, 99)),
        "_sizes": arr,
    }


def load(root: Path, ts_values=None, moduli=None):
    """-> {(ts, m): {seed: [per-realization metrics]}}"""
    data: dict[tuple[int, int], dict[int, list]] = defaultdict(
        lambda: defaultdict(list))
    for run_file in discover_run_files(root, ts_values=ts_values,
                                       weibull_moduli=moduli):
        by_realization: dict[int, list] = defaultdict(list)
        for step in iter_force_steps(run_file):
            by_realization[step.realization].append(step)
        for steps in by_realization.values():
            metrics = realization_metrics(steps)
            if metrics is not None:
                data[(run_file.ts, run_file.weibull_modulus)][
                    run_file.seed].append(metrics)
    return data


def icc(per_fibril: list[list[float]]) -> tuple[float, float, float]:
    """Intraclass correlation from a ragged list of per-fibril values."""
    usable = [np.asarray(v, float) for v in per_fibril if len(v) >= 2]
    if len(usable) < 2:
        return math.nan, math.nan, math.nan
    means = np.array([v.mean() for v in usable])
    s2_between = float(means.var(ddof=1))
    s2_within = float(np.mean([v.var(ddof=1) for v in usable]))
    total = s2_between + s2_within
    rho = s2_between / total if total > 0 else math.nan
    return s2_between, s2_within, rho


def recommended_realizations(rho: float, ceiling: int) -> int:
    """n_real >= 10 (1 - rho) / rho, clipped to [1, ceiling]."""
    if not math.isfinite(rho) or rho <= 0:
        return ceiling
    return int(max(1, min(ceiling, math.ceil(10.0 * (1.0 - rho) / rho))))


def bootstrap_se(values: np.ndarray, draws: int, rng) -> float:
    """Block bootstrap over fibrils: the fibril is the resampling unit."""
    if values.size < 2:
        return math.nan
    idx = rng.integers(0, values.size, size=(draws, values.size))
    return float(values[idx].mean(axis=1).std())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path, help="directory holding ts_<TS>/")
    ap.add_argument("--s-min", type=int, default=5,
                    help="lower threshold for the tail exponent")
    ap.add_argument("--ceiling", type=int, default=100,
                    help="maximum realizations per fibril the campaign allows")
    ap.add_argument("--se-target-gamma", type=float, default=0.02)
    ap.add_argument("--se-target-relative", type=float, default=0.05)
    ap.add_argument("--draws", type=int, default=2000)
    ap.add_argument("--json", type=Path, help="write the full report here")
    args = ap.parse_args()

    rng = np.random.default_rng(0)
    data = load(args.root)
    if not data:
        print(f"no run files under {args.root}", file=sys.stderr)
        return 1

    report = {"root": str(args.root), "conditions": []}

    print(f'{"Ts":>7} {"m":>3} {"fib":>4} {"real":>5} '
          f'{"rho(mean)":>10} {"n_real*":>8} '
          f'{"SE(gamma)":>10} {"SE(mean)%":>10} {"gamma":>7}')

    for (ts, m), by_seed in sorted(data.items()):
        seeds = sorted(by_seed)
        n_real = min(len(v) for v in by_seed.values())

        # ICC on the per-realization mean avalanche size: the metric with the
        # cleanest per-realization definition.
        rho_values = [[r["mean_size"] for r in by_seed[s]] for s in seeds]
        s2_b, s2_w, rho = icc(rho_values)
        n_star = recommended_realizations(rho, args.ceiling)

        # Fibril-level aggregates for the precision targets.
        fib_mean = np.array([np.mean([r["mean_size"] for r in by_seed[s]])
                             for s in seeds])
        fib_gamma = []
        for s in seeds:
            pooled = np.concatenate([r["_sizes"] for r in by_seed[s]])
            fib_gamma.append(gamma_mle(pooled, args.s_min))
        fib_gamma = np.array(fib_gamma, dtype=float)
        finite = fib_gamma[np.isfinite(fib_gamma)]

        se_gamma = bootstrap_se(finite, args.draws, rng)
        se_mean = bootstrap_se(fib_mean, args.draws, rng)
        rel_mean = se_mean / fib_mean.mean() if fib_mean.mean() else math.nan

        print(f'{ts:>7} {m:>3} {len(seeds):>4} {n_real:>5} '
              f'{rho:>10.3f} {n_star:>8} '
              f'{se_gamma:>10.4f} {100 * rel_mean:>9.2f}% '
              f'{(finite.mean() if finite.size else math.nan):>7.3f}')

        # Sequential curve: SE as fibrils accumulate, for the stopping rule.
        curve = []
        for k in range(2, len(seeds) + 1):
            curve.append({
                "n_fibrils": k,
                "se_gamma": bootstrap_se(
                    fib_gamma[:k][np.isfinite(fib_gamma[:k])],
                    args.draws, rng),
                "se_mean_relative": (
                    bootstrap_se(fib_mean[:k], args.draws, rng)
                    / fib_mean[:k].mean() if fib_mean[:k].mean() else math.nan),
            })

        report["conditions"].append({
            "ts": ts, "weibull_modulus": m,
            "fibrils": len(seeds), "realizations_per_fibril": n_real,
            "sigma2_between": s2_b, "sigma2_within": s2_w, "icc": rho,
            "recommended_realizations": n_star,
            "se_gamma": se_gamma, "se_mean_relative": rel_mean,
            "gamma": float(finite.mean()) if finite.size else None,
            "meets_gamma_target": bool(
                math.isfinite(se_gamma) and se_gamma <= args.se_target_gamma),
            "meets_relative_target": bool(
                math.isfinite(rel_mean) and rel_mean <= args.se_target_relative),
            "sequential": curve,
        })

    finite_icc = [c["icc"] for c in report["conditions"]
                  if math.isfinite(c["icc"])]
    if finite_icc:
        worst = max(c["recommended_realizations"] for c in report["conditions"])
        print()
        print(f"ICC across conditions: {min(finite_icc):.3f}-{max(finite_icc):.3f}")
        print(f"realizations needed (worst condition): {worst}")
        print("under a fixed budget, more fibrils beat more realizations: "
              "Var = (n_real*s2_b + s2_w)/C rises with n_real")
        report["recommended_realizations_overall"] = worst

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2))
        print(f"report: {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

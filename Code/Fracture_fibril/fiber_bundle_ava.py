"""Quenched-disorder (fiber-bundle) rupture protocol for DLA fibrils.

Replaces the annealed removal rule of ``stress_strain_ava`` by the standard
quasi-static fiber-bundle protocol:

* each rod i draws once, at t=0, a quenched variable X_i with CDF
  P(X <= x) = x**m on [0, 1], and carries the failure threshold
  sigma_th_i(t) = K_i(t) * sigma_c * X_i,
  where K_i(t) is the CURRENT coordination.  This is exactly Eq. (4) of the
  manuscript reinterpreted as a quenched strength distribution: the failure
  probability under stress sigma is (sigma/(K sigma_c))**m, capped at 1.
* the external force is raised continuously to the smallest failure force
  F*_i = sigma_th_i / a_i,  with  sigma_M_i(F) = F * a_i,
  a_i = mean over the rod's cross-sections of 1/N(section);
* at that fixed force the failure cascade proceeds deterministically:
  every rod with F*_i <= F fails, loads and coordinations are recomputed,
  and the cascade repeats until no rod is above threshold;
* the avalanche is the total number of rods removed in the cascade
  (threshold failures plus rods that lost the load path), exactly the
  force-step definition suggested by Referee 2;
* rupture happens when the cascade destroys the continuous load path.

There is no force increment ``dF``, no sweep, and no stopping criterion:
cascade termination is deterministic, which removes the protocol dependence
of the annealed rule (cf. R2-1).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stress_strain_ava as S  # noqa: E402


# --------------------------------------------------------------------- engine
def quasistatic_rupture(system):
    """Generic quasi-static extremal loading with deterministic cascades.

    ``system`` must provide:
      next_failure_force() -> float or None   (min F*_i over active elements)
      fail_at(F) -> int      (remove every element with F*_i <= F, including
                              consequential structural removals; return the
                              number removed; 0 when the cascade is over)
      num_active() -> int

    Returns (events, F_rupture) where events is a list of (F, size) with the
    terminal event last.
    """
    events = []
    F = 0.0
    while system.num_active() > 0:
        Fnext = system.next_failure_force()
        if Fnext is None:
            break
        F = max(F, Fnext)
        size = 0
        while True:
            removed = system.fail_at(F)
            if removed == 0:
                break
            size += removed
        if size > 0:
            events.append((F, size))
    return events, F


# ---------------------------------------------------------------- ELS system
class ELSBundle:
    """Equal-load-sharing bundle, for validating the engine.

    N fibers, load F/N_active per fiber, quenched thresholds ``x``.  With
    uniform thresholds the avalanche-size distribution follows the classical
    mean-field power law D(s) ~ s**(-5/2) (Hemmer & Hansen 1992).
    """

    def __init__(self, thresholds):
        self.x = np.asarray(thresholds, float)
        self.active = np.ones(len(self.x), bool)

    def num_active(self):
        return int(self.active.sum())

    def _fstar(self):
        n = self.active.sum()
        return self.x[self.active] * n   # F*_i = x_i * N_active

    def next_failure_force(self):
        if not self.active.any():
            return None
        return float(self._fstar().min())

    def fail_at(self, F):
        n = self.active.sum()
        if n == 0:
            return 0
        idx = np.where(self.active)[0]
        failing = idx[self.x[idx] * n <= F * (1 + 1e-12)]
        self.active[failing] = False
        return len(failing)


# -------------------------------------------------------------- fibril system
class FibrilSystem:
    """DLA fibril with quenched thresholds, backed by the ssd machinery.

    The ssd object (from the corrected ``stress_strain_ava``) remains the
    source of truth for removals and for the structural load-path filter;
    numpy arrays handle the F* recomputation.
    """

    def __init__(self, ssd, m=2, sigma_c=1.0, rng=None):
        self.ssd = ssd
        self.sigma_c = sigma_c
        rng = rng or np.random.default_rng()

        ssd.filter_rids(reverse=False)
        ssd.filter_rids(reverse=True)

        rids = sorted(ssd.rods.keys())
        self.rid_index = {rid: k for k, rid in enumerate(rids)}
        self.rids = np.asarray(rids)
        R = len(rids)

        # static layer membership (particles never move; a rod's layer list is
        # fixed while it is active)
        flat_lids, flat_rod = [], []
        for k, rid in enumerate(rids):
            for lid in ssd.rods[rid].layer_ids():
                flat_lids.append(lid)
                flat_rod.append(k)
        self.flat_lids = np.asarray(flat_lids)
        self.flat_rod = np.asarray(flat_rod)
        self.n_parts = np.bincount(self.flat_rod, minlength=R).astype(float)
        self.lid_off = -int(self.flat_lids.min())
        self.flat_lids = self.flat_lids + self.lid_off
        self.L = int(self.flat_lids.max()) + 1

        # static coordination weights: c[j, i] = number of particles of rod i
        # adjacent to rod j; K_j = sum over ACTIVE i of c[j, i]
        from scipy.sparse import coo_matrix
        rows, cols, vals = [], [], []
        for rid in rids:
            j = self.rid_index[rid]
            counts = {}
            for pid in ssd.rods[rid].neigh_pids:
                i_rid = ssd.particles[pid].rid
                if i_rid in self.rid_index:
                    counts[self.rid_index[i_rid]] = counts.get(self.rid_index[i_rid], 0) + 1
            for i, c in counts.items():
                rows.append(j); cols.append(i); vals.append(c)
        self.C = coo_matrix((vals, (rows, cols)), shape=(R, R)).tocsr()

        # quenched disorder: P(X <= x) = x**m  on [0, 1]
        self.X = rng.random(R) ** (1.0 / m)

        self.active = np.ones(R, bool)
        self._refresh()

    # -- state -----------------------------------------------------------
    def _refresh(self):
        """Recompute a_i, K_i, F*_i from the current active set."""
        act_flat = self.active[self.flat_rod]
        counts = np.bincount(self.flat_lids[act_flat], minlength=self.L).astype(float)
        inv = np.zeros_like(counts)
        np.divide(1.0, counts, out=inv, where=counts > 0)
        a = np.bincount(self.flat_rod, weights=inv[self.flat_lids] * act_flat,
                        minlength=len(self.n_parts)) / self.n_parts
        K = self.C.dot(self.active.astype(float))
        with np.errstate(divide='ignore', invalid='ignore'):
            fstar = np.where(a > 0, K * self.sigma_c * self.X / a, 0.0)
        fstar[~self.active] = np.inf
        self.fstar = fstar

    def _sync_from_ssd(self):
        alive = set(self.ssd.rods.keys())
        for k, rid in enumerate(self.rids):
            if self.active[k] and rid not in alive:
                self.active[k] = False

    # -- engine interface -------------------------------------------------
    def num_active(self):
        return int(self.active.sum())

    def next_failure_force(self):
        if not self.active.any():
            return None
        m = self.fstar[self.active].min()
        return None if not np.isfinite(m) else float(m)

    def fail_at(self, F):
        failing = np.where(self.active & (self.fstar <= F * (1 + 1e-12)))[0]
        if len(failing) == 0:
            return 0
        before = self.num_active()
        self.ssd.drop_rids({int(self.rids[k]) for k in failing})
        act1, _ = self.ssd.filter_rids(reverse=False)
        if act1:
            self.ssd.filter_rids(reverse=True)
        self._sync_from_ssd()
        self._refresh()
        return before - self.num_active()


# ---------------------------------------------------------------------- main
def run_realizations(fn_dat, n, m=2, seed=1):
    ssd0 = S.read_or_create_ssd(fn_dat)
    ssd0.set_rods_exponent(m)
    out = []
    for k in range(n):
        rng = np.random.default_rng(seed + k)
        sys_k = FibrilSystem(ssd0.copy(), m=m, rng=rng)
        t0 = time.time()
        events, F_rup = quasistatic_rupture(sys_k)
        out.append({
            'F_rupture': F_rup,
            'events': [(float(f), int(s)) for f, s in events],
            'secs': round(time.time() - t0, 2),
        })
        pre = [s for _, s in events[:-1]]
        print(f'  run {k + 1}/{n}: F_rup={F_rup:.2f}  events={len(events)}  '
              f'max_preterminal={max(pre) if pre else 0}  '
              f'({out[-1]["secs"]}s)', flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-file', required=True)
    ap.add_argument('-n', type=int, default=5)
    ap.add_argument('-m', type=int, default=2)
    ap.add_argument('-seed', type=int, default=1)
    ap.add_argument('-out', required=True)
    a = ap.parse_args()
    runs = run_realizations(a.file, a.n, m=a.m, seed=a.seed)
    with open(a.out, 'w') as fh:
        json.dump({'file': os.path.basename(a.file), 'm': a.m,
                   'seed': a.seed, 'runs': runs}, fh)
    print('wrote', a.out)


if __name__ == '__main__':
    main()

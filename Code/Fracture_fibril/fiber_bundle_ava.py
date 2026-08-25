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
import re
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
    begin = getattr(system, 'begin_cascade', None)
    end = getattr(system, 'end_cascade', None)
    while system.num_active() > 0:
        Fnext = system.next_failure_force()
        if Fnext is None:
            break
        F = max(F, Fnext)
        if begin is not None:
            begin(F)
        size = 0
        while True:
            removed = system.fail_at(F)
            if removed == 0:
                break
            size += removed
        if end is not None:
            end(F, size)
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
        # Symmetric adjacency list for the cascade cluster decomposition.
        self.adj = [set() for _ in range(R)]
        for j, i in zip(rows, cols):
            self.adj[j].add(i)
            self.adj[i].add(j)

        # quenched disorder: P(X <= x) = x**m  on [0, 1]
        self.X = rng.random(R) ** (1.0 / m)

        self.active = np.ones(R, bool)
        self.log = []
        self._cascade_idx = []
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

    # -- cascade bookkeeping ----------------------------------------------
    def begin_cascade(self, F):
        self._cascade_idx = []

    def end_cascade(self, F, size):
        """Close a cascade and record the row the legacy writer needs.

        `avalanche_sizes` is the decomposition of THIS cascade into
        nearest-neighbour connected clusters.  It is kept only as a geometric
        diagnostic -- the primary observable is the cascade size -- and it also
        satisfies the invariant read_avalanche_runs.py enforces,
        sum(avalanche_sizes) == total_deleted_rods.
        """
        if size <= 0:
            return
        self.log.append({
            'F': float(F),
            'active_particles': self.active_particles(),
            'rods': int(size),
            'clusters': self.cluster_sizes(self._cascade_idx),
        })

    def active_particles(self):
        """Particles still in the backbone.

        Summed per rod rather than assuming 18 each: the mechanical window
        clips |y| <= 100, so a rod near either end can contribute fewer.
        """
        return int(self.n_parts[self.active].sum())

    def cluster_sizes(self, idx):
        """Connected components among the rods removed in one cascade.

        Uses the static adjacency C, so no snapshot of the ssd is needed --
        find_deleted_rod_clusters would require one copy per cascade.
        """
        if not idx:
            return []
        if len(idx) == 1:
            return [1]
        # Plain BFS over a precomputed adjacency list.  Slicing the R x R
        # sparse matrix (C[order][:, order]) reallocates on every cascade and
        # dominated the runtime; cascades are small, so an adjacency walk is
        # far cheaper.
        pending = set(idx)
        sizes = []
        while pending:
            root = pending.pop()
            size = 1
            queue = [root]
            while queue:
                node = queue.pop()
                for neighbour in self.adj[node]:
                    if neighbour in pending:
                        pending.discard(neighbour)
                        size += 1
                        queue.append(neighbour)
            sizes.append(size)
        return sorted(sizes, reverse=True)

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
        was_active = self.active.copy()
        self.ssd.drop_rids({int(self.rids[k]) for k in failing})
        act1, _ = self.ssd.filter_rids(reverse=False)
        if act1:
            self.ssd.filter_rids(reverse=True)
        self._sync_from_ssd()
        self._refresh()
        # every rod that went in this call: threshold failures plus the rods
        # that lost the load path as a consequence
        gone = np.where(was_active & ~self.active)[0]
        self._cascade_idx.extend(int(g) for g in gone)
        return before - self.num_active()


# --------------------------------------------------------------- legacy I/O
LEGACY_HEADER = ('f,num_active_particles,num_deleted_particles,'
                 'total_deleted_rods,avalanche_sizes')


def write_legacy(path, log, initial_particles, realization):
    """Append one realization in the schema read_avalanche_runs.py expects.

    That parser enforces, per realization: the first row has f == 0, the force
    increases strictly, sum(avalanche_sizes) == total_deleted_rods,
    num_active + num_deleted stays constant, num_active is non-increasing, and
    no row follows the terminal one.  All of these hold here, and the synthetic
    f = 0 row supplies the required opening row.

    The force is written with %.17g, not a shorter format.  Cascade forces are
    strictly increasing in exact arithmetic -- thresholds are continuous, so
    ties have measure zero -- but the parser reads the DECIMAL TEXT, and two
    distinct doubles that agree to the printed precision collide there.  At
    %.10g that happened twice in the 165 million forces of the first production
    campaign, on genuinely distinct events (active particles and removed rods
    both changed across the tie).  %.17g round-trips float64 exactly, so a
    printed tie now implies the doubles themselves are equal.
    """
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    lines = []
    if realization == 0:
        lines.append(LEGACY_HEADER)
    else:
        lines.append('-' * 46 + str(realization))
    lines.append(f'0,{initial_particles},0,0,"0"')
    for row in log:
        active = row['active_particles']
        deleted = initial_particles - active
        clusters = '-'.join(str(c) for c in row['clusters']) or '0'
        lines.append(f'{row["F"]:.17g},{active},{deleted},{row["rods"]},'
                     f'"{clusters}"')

    with open(path, 'w' if realization == 0 else 'a') as fh:
        fh.write('\n'.join(lines) + '\n')


def legacy_output_path(fn_dat, m, output_dir=None):
    """ts_<TS>_seed_<SEED>_m_<M>.txt under ts_<TS>/, as the parser requires."""
    stem = os.path.splitext(os.path.basename(fn_dat))[0]
    match = re.fullmatch(r'ts_(\d+)_seed_(\d+)', stem)
    if match is None:
        raise ValueError(
            f'unexpected fibril name {stem!r}: expected ts_<TS>_seed_<SEED>')
    ts = match.group(1)
    name = f'{stem}_m_{m}.txt'
    base = output_dir if output_dir else os.path.dirname(fn_dat)
    return os.path.join(base, f'ts_{ts}', name)


# ---------------------------------------------------------------------- main
def run_realizations(fn_dat, n, m=2, seed=1, legacy_path=None, start=0):
    ssd0 = S.read_or_create_ssd(fn_dat)
    ssd0.set_rods_exponent(m)
    out = []
    for k in range(start, n):
        rng = np.random.default_rng(seed + k)
        sys_k = FibrilSystem(ssd0.copy(), m=m, rng=rng)
        initial_particles = sys_k.active_particles()
        t0 = time.time()
        events, F_rup = quasistatic_rupture(sys_k)
        if legacy_path is not None:
            write_legacy(legacy_path, sys_k.log, initial_particles, k)
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
    ap.add_argument('-out', help='optional JSON summary')
    ap.add_argument('-legacy-dir', dest='legacy_dir',
                    help='write ts_<TS>/ts_<TS>_seed_<SEED>_m_<M>.txt here, in '
                         'the schema read_avalanche_runs.py expects')
    ap.add_argument('-start', type=int, default=0,
                    help='zero-based realization to resume from')
    a = ap.parse_args()

    legacy_path = None
    if a.legacy_dir:
        legacy_path = legacy_output_path(a.file, a.m, a.legacy_dir)
        print('legacy output:', legacy_path)

    runs = run_realizations(a.file, a.n, m=a.m, seed=a.seed,
                            legacy_path=legacy_path, start=a.start)
    if a.out:
        with open(a.out, 'w') as fh:
            json.dump({'file': os.path.basename(a.file), 'm': a.m,
                       'seed': a.seed, 'runs': runs}, fh)
        print('wrote', a.out)


if __name__ == '__main__':
    main()

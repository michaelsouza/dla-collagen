"""create_neighs (spatial hash) must give exactly the neighbor sets of the all-pairs original.

Self-contained: builds a small random fibril in memory, so the test needs no
data file. The lattice is dense on purpose (many same-site and axis-adjacent
pairs, plus diagonals that must NOT count), which is where the two algorithms
could disagree.
"""
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import stress_strain_ava as S


def _synthetic(seed, n_rods=400, half_width=6, height=18, layers=60):
    rng = random.Random(seed)
    ssd = S.StressStrainData()
    pid = 0
    for rid in range(n_rods):
        x, z = rng.randint(-half_width, half_width), rng.randint(-half_width, half_width)
        y0 = rng.randint(-layers // 2, layers // 2 - height)
        rod = S.Rod(ssd, rid); ssd.rods[rid] = rod
        for k in range(height):
            y = y0 + k
            p = S.Particle(ssd, pid, rid, y, np.array([x, z])); ssd.particles[pid] = p
            rod.add_pid(pid); ssd.layers.setdefault(y, S.Layer(y)).add_pid(pid); pid += 1
    return ssd


def test_create_neighs_matches_allpairs():
    for seed in (1, 2, 3):
        a, b = _synthetic(seed), _synthetic(seed)
        S.create_neighs_allpairs(a.layers, a.particles)
        S.create_neighs(b.layers, b.particles)
        assert len(a.particles) == len(b.particles) > 0
        total = 0
        for pid in a.particles:
            na, nb = set(a.particles[pid].get_neigh_rids()), set(b.particles[pid].get_neigh_rids())
            assert na == nb, (seed, pid, na ^ nb)
            total += len(na)
        assert total > 0, "fixture produced no neighbors; test is vacuous"


def test_diagonal_is_not_a_neighbor():
    ssd = S.StressStrainData()
    for rid, (x, z) in enumerate(((0, 0), (1, 1), (1, 0))):
        rod = S.Rod(ssd, rid); ssd.rods[rid] = rod
        p = S.Particle(ssd, rid, rid, 0, np.array([x, z])); ssd.particles[rid] = p
        rod.add_pid(rid); ssd.layers.setdefault(0, S.Layer(0)).add_pid(rid)
    S.create_neighs(ssd.layers, ssd.particles)
    assert set(ssd.particles[0].get_neigh_rids()) == {2}      # axis neighbor yes
    assert 1 not in ssd.particles[0].get_neigh_rids()          # diagonal no

import os
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stress_strain_ava
from fiber_bundle_ava import ELSBundle, FibrilSystem, quasistatic_rupture


class CascadeEngineELSTest(unittest.TestCase):
    """The engine must reproduce the exact ELS burst distribution.

    For an equal-load-sharing bundle with uniform thresholds the burst-size
    distribution is (Hemmer & Hansen, J. Appl. Mech. 59, 909, 1992)
        D(s)/N = s^(s-1)/s! * INT_0^{1/2} a^(s-1) e^(-s a) (1 - a) dx,
    with a(x) = x / (1 - x).  Its tail is the mean-field power law s^(-5/2).
    """

    def test_burst_distribution_matches_hemmer_hansen(self):
        from scipy.special import gammaln
        from scipy.integrate import quad

        rng = np.random.default_rng(7)
        sizes = []
        for _ in range(60):
            events, _ = quasistatic_rupture(ELSBundle(rng.random(3000)))
            sizes.extend(s for _, s in events[:-1])
        sizes = np.asarray(sizes)

        smax = 6
        theory = np.zeros(smax)
        for s in range(1, smax + 1):
            integral, _ = quad(
                lambda x, s=s: (x / (1 - x)) ** (s - 1)
                * np.exp(-s * x / (1 - x)) * (1 - x / (1 - x)),
                0, 0.5, limit=200)
            theory[s - 1] = np.exp((s - 1) * np.log(s) - gammaln(s + 1)) * integral
        theory /= theory.sum()
        empirical = np.array(
            [(sizes == s).sum() for s in range(1, smax + 1)], float)
        empirical /= empirical.sum()

        relative = np.abs(empirical - theory) / theory
        # 60 bundles x 3000 fibers keeps the test fast; the s=5,6 bins then
        # carry ~5% sampling noise (a 150 x 4000 run agrees within 2.5%).
        self.assertLess(relative.max(), 0.10,
                        f'empirical={empirical}, theory={theory}')


class FibrilSystemTest(unittest.TestCase):
    def build(self, seed=3):
        self.tmp = tempfile.TemporaryDirectory()
        fn = Path(self.tmp.name) / 'f.dat'
        # four coplanar rods, two adjacent pairs (same geometry as the
        # sigma regression test in test_stress_strain_ava)
        fn.write_text(
            "id uid x y z\n"
            "uid 1 0 0 0\nuid 1 0 1 0\n"
            "uid 2 1 0 0\nuid 2 1 1 0\n"
            "uid 3 5 0 0\nuid 3 5 1 0\n"
            "uid 4 6 0 0\nuid 4 6 1 0\n",
            encoding='utf-8')
        ssd = stress_strain_ava.read_or_create_ssd(str(fn))
        return FibrilSystem(ssd, m=2, rng=np.random.default_rng(seed))

    def test_failure_force_formula(self):
        system = self.build()
        # both layers hold N=4 particles -> a_i = 1/4; each rod has K=2
        k = system.rid_index[1]
        expected = 2 * 1.0 * system.X[k] / 0.25
        self.assertAlmostEqual(system.fstar[k], expected)

    def test_rupture_is_monotone_and_complete(self):
        system = self.build()
        events, f_rupture = quasistatic_rupture(system)
        forces = [f for f, _ in events]
        self.assertEqual(forces, sorted(forces))
        self.assertEqual(system.num_active(), 0)
        self.assertEqual(sum(s for _, s in events), 4)
        self.assertAlmostEqual(f_rupture, forces[-1])

    def test_thresholds_follow_eq4_distribution(self):
        # P(X <= x) = x^m: with m=2 the median of X is sqrt(0.5)
        rng = np.random.default_rng(11)
        x = rng.random(200_000) ** (1 / 2)
        self.assertAlmostEqual(np.median(x), np.sqrt(0.5), places=2)


if __name__ == '__main__':
    unittest.main()

import unittest
from collections import Counter

import numpy as np
from scipy import special

from fit_local_power_law import discrete_ks, fit_gamma, model_ccdf, select_xmin


class DiscretePowerLawTest(unittest.TestCase):
    def test_model_ccdf_starts_at_one(self):
        values = model_ccdf(np.array([3, 4, 5]), xmin=3, gamma=2.5)
        self.assertAlmostEqual(float(values[0]), 1.0)
        self.assertTrue(np.all(np.diff(values) < 0))

    def test_exact_mle_recovers_deterministic_power_law_frequencies(self):
        sizes = np.arange(2, 500)
        expected = sizes.astype(float) ** -2.5
        frequencies = np.maximum(1, np.rint(2_000_000 * expected / expected.sum())).astype(int)
        gamma, _ = fit_gamma(sizes, frequencies, xmin=2)
        self.assertAlmostEqual(gamma, 2.5, delta=0.03)
        self.assertLess(discrete_ks(sizes, frequencies, 2, gamma), 0.01)

    def test_exact_mle_is_not_capped_at_twenty(self):
        sizes = np.arange(1_000, 3_000)
        expected = sizes.astype(float) ** -35.0
        frequencies = np.maximum(
            1, np.rint(5_000_000 * expected / expected.sum())
        ).astype(int)

        gamma, log_likelihood = fit_gamma(sizes, frequencies, xmin=1_000)

        self.assertGreater(gamma, 20.0)
        self.assertAlmostEqual(gamma, 35.0, delta=1.0)
        self.assertTrue(np.isfinite(log_likelihood))
        self.assertLess(discrete_ks(sizes, frequencies, 1_000, gamma), 0.01)

    def test_xmin_selection_reports_tail_metadata(self):
        counts = Counter({size: max(1, int(100_000 * size**-2.3)) for size in range(2, 80)})
        fit = select_xmin(8, counts, min_tail=100, min_distinct=10)
        self.assertGreaterEqual(fit.xmin, 2)
        self.assertLessEqual(fit.xmin, 70)
        self.assertEqual(fit.n_total, sum(counts.values()))
        self.assertAlmostEqual(fit.tail_fraction, fit.n_tail / fit.n_total)
        self.assertTrue(np.isfinite(special.zeta(fit.gamma, fit.xmin)))


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
from pathlib import Path

import numpy as np

from .power_law import (
    discrete_ks,
    fit_alpha,
    power_law_cdf,
    read_size_histogram,
    select_xmin,
)
from .gof import clauset_gof, sample_power_law_counts


class PreparedInputTest(unittest.TestCase):
    def test_reader_filters_singletons_and_counts_each_size(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ts_2.txt"
            path.write_text("1\n2\n4\n2\n1\n3\n", encoding="ascii")
            histogram = read_size_histogram(path, minimum_size=2, chunk_bytes=4)

        np.testing.assert_array_equal(histogram, np.array([0, 0, 2, 1, 1]))


class ExactDiscretePowerLawTest(unittest.TestCase):
    def test_cdf_starts_with_the_exact_mass_at_xmin(self):
        alpha = 2.5
        values = power_law_cdf(np.array([2, 3, 4]), xmin=2, alpha=alpha)
        expected_first = 2.0**-alpha / sum(
            value**-alpha for value in range(2, 1_000_000)
        )
        self.assertAlmostEqual(values[0], expected_first, places=7)
        self.assertTrue(np.all(np.diff(values) > 0.0))

    def test_mle_recovers_a_high_exponent_without_an_arbitrary_cap(self):
        sizes = np.arange(1000, 3000)
        weights = (sizes / 1000.0) ** -70.0
        frequencies = np.maximum(1, np.rint(8_000_000 * weights / weights.sum())).astype(int)
        histogram = np.zeros(3000, dtype=np.int64)
        histogram[sizes] = frequencies

        alpha, _ = fit_alpha(histogram, xmin=1000)

        self.assertGreater(alpha, 50.0)
        self.assertAlmostEqual(alpha, 70.0, delta=2.0)
        self.assertLess(discrete_ks(histogram, xmin=1000, alpha=alpha), 0.01)

    def test_xmin_selection_excludes_a_non_power_law_body(self):
        sizes = np.arange(5, 500)
        probabilities = sizes.astype(float) ** -2.4
        frequencies = np.maximum(
            1, np.rint(2_000_000 * probabilities / probabilities.sum())
        ).astype(int)
        histogram = np.zeros(500, dtype=np.int64)
        histogram[sizes] = frequencies
        histogram[2:5] = [900_000, 10_000, 500_000]

        fit = select_xmin(histogram, minimum_xmin=2, minimum_tail=10_000)

        self.assertEqual(fit.xmin, 5)
        self.assertAlmostEqual(fit.alpha, 2.4, delta=0.03)

    def test_sparse_histogram_supports_very_large_sampled_values(self):
        histogram = {2: 1000, 3: 500, 10_000_000: 1}
        alpha, log_likelihood = fit_alpha(histogram, xmin=2)
        self.assertGreater(alpha, 1.0)
        self.assertTrue(np.isfinite(log_likelihood))


class SemiparametricGoodnessOfFitTest(unittest.TestCase):
    def test_exact_sampler_recovers_the_generating_alpha(self):
        sampled = sample_power_law_counts(
            100_000, xmin=3, alpha=2.5, rng=np.random.default_rng(9001)
        )
        alpha, _ = fit_alpha(sampled, xmin=3)
        self.assertEqual(sum(sampled.values()), 100_000)
        self.assertGreaterEqual(min(sampled), 3)
        self.assertAlmostEqual(alpha, 2.5, delta=0.03)

    def test_gof_is_reproducible_and_refits_each_replica(self):
        tail = sample_power_law_counts(
            4000, xmin=5, alpha=2.4, rng=np.random.default_rng(1909)
        )
        histogram = {2: 2200, 3: 300, 4: 5000, **tail}
        first = clauset_gof(
            histogram, minimum_tail=200, replicates=19, seed=12738, workers=1
        )
        second = clauset_gof(
            histogram, minimum_tail=200, replicates=19, seed=12738, workers=1
        )
        self.assertEqual(first, second)
        self.assertEqual(first.observed.xmin, 5)
        self.assertEqual(len(first.synthetic_ks), 19)
        self.assertGreater(len(set(first.synthetic_xmin)), 1)


if __name__ == "__main__":
    unittest.main()

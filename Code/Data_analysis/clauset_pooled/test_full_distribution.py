import unittest

import numpy as np

from .full_distribution import (
    distribution_distance,
    histogram_quantiles,
    summarize_histogram,
    tail_probability,
)


class CompleteDistributionTest(unittest.TestCase):
    def setUp(self):
        self.histogram = np.array([0, 2, 1, 0, 1], dtype=np.int64)

    def test_exact_summary_uses_frequency_weights(self):
        summary = summarize_histogram(
            self.histogram, population="all", minimum_size=1
        )
        self.assertEqual(summary.n_events, 4)
        self.assertEqual(summary.mode, 1)
        self.assertEqual(summary.maximum, 4)
        self.assertAlmostEqual(summary.mean, 2.0)
        self.assertEqual(summary.q50, 1)
        self.assertEqual(summary.q75, 2)
        self.assertEqual(summary.q90, 4)

    def test_conditioning_and_tail_probability(self):
        summary = summarize_histogram(
            self.histogram, population="nontrivial", minimum_size=2
        )
        self.assertEqual(summary.n_events, 2)
        self.assertAlmostEqual(summary.mean, 3.0)
        self.assertAlmostEqual(tail_probability(self.histogram, 2), 0.5)

    def test_quantiles_reject_invalid_probabilities(self):
        with self.assertRaises(ValueError):
            histogram_quantiles(self.histogram, (1.1,))

    def test_distances_are_zero_for_identical_distributions(self):
        distance = distribution_distance(self.histogram, self.histogram)
        self.assertEqual(distance.total_variation, 0.0)
        self.assertEqual(distance.jensen_shannon, 0.0)
        self.assertEqual(distance.kolmogorov_smirnov, 0.0)
        self.assertEqual(distance.wasserstein, 0.0)

    def test_distances_are_symmetric(self):
        other = np.array([0, 0, 0, 4], dtype=np.int64)
        forward = distribution_distance(self.histogram, other)
        backward = distribution_distance(other, self.histogram)
        self.assertAlmostEqual(forward.total_variation, backward.total_variation)
        self.assertAlmostEqual(forward.jensen_shannon, backward.jensen_shannon)
        self.assertAlmostEqual(forward.kolmogorov_smirnov, backward.kolmogorov_smirnov)
        self.assertAlmostEqual(forward.wasserstein, backward.wasserstein)


if __name__ == "__main__":
    unittest.main()


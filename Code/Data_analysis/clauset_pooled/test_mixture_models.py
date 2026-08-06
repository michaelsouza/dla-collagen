import unittest

import numpy as np

from .mixture_models import (
    cutoff_lognormal_goodness_of_fit,
    cutoff_lognormal_log_probabilities,
    fit_cutoff_lognormal_mixture,
    fit_two_lognormal_mixture,
    mixture_goodness_of_fit,
    mixture_log_probabilities,
    sample_two_lognormal_counts,
    sample_cutoff_lognormal_counts,
)
from .models import ModelFit


class TwoLognormalMixtureTest(unittest.TestCase):
    def test_probabilities_are_normalized(self):
        sizes = np.arange(2, 100_000)
        probabilities = np.exp(
            mixture_log_probabilities(
                sizes,
                xmin=2,
                weight_small=0.93,
                mu_small=1.0,
                sigma_small=0.8,
                mu_large=6.0,
                sigma_large=0.15,
            )
        )
        self.assertAlmostEqual(float(probabilities.sum()), 1.0, places=10)

    def test_fit_recovers_a_separated_synthetic_mixture(self):
        generating = ModelFit(
            model="two_lognormal_mixture",
            xmin=2,
            parameters={
                "weight_small": 0.96,
                "mu_small": 1.0,
                "sigma_small": 0.7,
                "mu_large": 6.0,
                "sigma_large": 0.12,
            },
            log_likelihood=0.0,
            ks=0.0,
            n_tail=200_000,
            parameter_count=5,
        )
        counts = sample_two_lognormal_counts(
            generating.n_tail, generating, rng=np.random.default_rng(2026)
        )
        fitted = fit_two_lognormal_mixture(counts, xmin=2)
        self.assertAlmostEqual(fitted.parameters["weight_small"], 0.96, delta=0.01)
        self.assertAlmostEqual(fitted.parameters["mu_small"], 1.0, delta=0.05)
        self.assertAlmostEqual(fitted.parameters["sigma_small"], 0.7, delta=0.03)
        self.assertAlmostEqual(fitted.parameters["mu_large"], 6.0, delta=0.02)
        self.assertAlmostEqual(fitted.parameters["sigma_large"], 0.12, delta=0.01)
        self.assertLess(fitted.ks, 0.005)

    def test_bootstrap_is_reproducible(self):
        generating = ModelFit(
            model="two_lognormal_mixture",
            xmin=2,
            parameters={
                "weight_small": 0.95,
                "mu_small": 1.0,
                "sigma_small": 0.6,
                "mu_large": 5.0,
                "sigma_large": 0.15,
            },
            log_likelihood=0.0,
            ks=0.0,
            n_tail=10_000,
            parameter_count=5,
        )
        counts = sample_two_lognormal_counts(
            generating.n_tail, generating, rng=np.random.default_rng(77)
        )
        first = mixture_goodness_of_fit(counts, replicates=5, seed=88)
        second = mixture_goodness_of_fit(counts, replicates=5, seed=88)
        self.assertEqual(first, second)

    def test_cutoff_lognormal_probabilities_are_normalized(self):
        sizes = np.arange(2, 100_000)
        probabilities = np.exp(
            cutoff_lognormal_log_probabilities(
                sizes,
                xmin=2,
                weight_small=0.97,
                alpha=1.4,
                rate=0.04,
                mu_large=6.0,
                sigma_large=0.15,
            )
        )
        self.assertAlmostEqual(float(probabilities.sum()), 1.0, places=10)

    def test_cutoff_lognormal_fit_recovers_synthetic_parameters(self):
        sizes = np.arange(2, 3000)
        probabilities = np.exp(
            cutoff_lognormal_log_probabilities(
                sizes,
                xmin=2,
                weight_small=0.97,
                alpha=1.4,
                rate=0.04,
                mu_large=6.0,
                sigma_large=0.15,
            )
        )
        frequencies = np.rint(1_000_000 * probabilities).astype(np.int64)
        histogram = {
            int(size): int(count)
            for size, count in zip(sizes, frequencies, strict=True)
            if count
        }
        fitted = fit_cutoff_lognormal_mixture(histogram, xmin=2)
        self.assertAlmostEqual(fitted.parameters["weight_small"], 0.97, delta=0.005)
        self.assertAlmostEqual(fitted.parameters["alpha"], 1.4, delta=0.03)
        self.assertAlmostEqual(fitted.parameters["lambda"], 0.04, delta=0.005)
        self.assertAlmostEqual(fitted.parameters["mu_large"], 6.0, delta=0.02)
        self.assertAlmostEqual(fitted.parameters["sigma_large"], 0.15, delta=0.01)
        self.assertLess(fitted.ks, 0.003)

        sampled = sample_cutoff_lognormal_counts(
            100_000, fitted, rng=np.random.default_rng(91)
        )
        self.assertEqual(sum(sampled.values()), 100_000)
        bootstrap = cutoff_lognormal_goodness_of_fit(
            histogram, replicates=3, seed=92
        )
        self.assertEqual(bootstrap.replicates, 3)


if __name__ == "__main__":
    unittest.main()

import unittest

import numpy as np

from .alternative_gof import parametric_gof, sample_model_counts
from .models import (
    _cutoff_log_normalization,
    _lognormal_log_probabilities,
    fit_cutoff_power_law,
    fit_exponential,
    fit_lognormal,
    fit_power_law_model,
    fit_stretched_cutoff_power_law,
    vuong_test,
)


class CompetingModelTest(unittest.TestCase):
    def test_exact_discrete_exponential_recovers_rate(self):
        rate = 0.35
        sizes = np.arange(3, 100)
        probabilities = (1.0 - np.exp(-rate)) * np.exp(-rate * (sizes - 3))
        counts = {
            int(size): int(count)
            for size, count in zip(
                sizes, np.rint(500_000 * probabilities).astype(int), strict=True
            )
            if count
        }
        fit = fit_exponential(counts, xmin=3)
        self.assertAlmostEqual(fit.parameters["lambda"], rate, delta=0.002)
        self.assertLess(fit.ks, 0.002)

    def test_vuong_favors_exponential_for_geometric_data(self):
        rate = 0.4
        sizes = np.arange(2, 80)
        probabilities = (1.0 - np.exp(-rate)) * np.exp(-rate * (sizes - 2))
        counts = {
            int(size): int(count)
            for size, count in zip(
                sizes, np.rint(100_000 * probabilities).astype(int), strict=True
            )
            if count
        }
        power = fit_power_law_model(counts, xmin=2)
        exponential = fit_exponential(counts, xmin=2)
        ratio, _, p_value = vuong_test(counts, power, exponential)
        self.assertLess(ratio, 0.0)
        self.assertLess(p_value, 0.01)

    def test_discrete_lognormal_recovers_synthetic_parameters(self):
        mu = 2.0
        sigma = 0.65
        sizes = np.arange(2, 300)
        probabilities = np.exp(
            _lognormal_log_probabilities(sizes, xmin=2, mu=mu, sigma=sigma)
        )
        counts = {
            int(size): int(count)
            for size, count in zip(
                sizes, np.rint(500_000 * probabilities).astype(int), strict=True
            )
            if count
        }
        fit = fit_lognormal(counts, xmin=2)
        self.assertAlmostEqual(fit.parameters["mu"], mu, delta=0.03)
        self.assertAlmostEqual(fit.parameters["sigma"], sigma, delta=0.02)

    def test_cutoff_power_law_recovers_synthetic_parameters(self):
        alpha = 1.4
        rate = 0.03
        xmin = 2
        sizes = np.arange(xmin, 1000)
        log_normalization = _cutoff_log_normalization(alpha, rate, xmin)
        probabilities = np.exp(
            -alpha * np.log(sizes / xmin)
            - rate * (sizes - xmin)
            - log_normalization
        )
        counts = {
            int(size): int(count)
            for size, count in zip(
                sizes, np.rint(500_000 * probabilities).astype(int), strict=True
            )
            if count
        }
        fit = fit_cutoff_power_law(counts, xmin=xmin)
        self.assertAlmostEqual(fit.parameters["alpha"], alpha, delta=0.03)
        self.assertAlmostEqual(fit.parameters["lambda"], rate, delta=0.003)

    def test_stretched_cutoff_recovers_synthetic_parameters(self):
        alpha = 2.1
        scale = 70.0
        beta = 1.7
        xmin = 8
        sizes = np.arange(xmin, 1000)
        log_weights = -alpha * np.log(sizes / xmin) - (sizes / scale) ** beta
        probabilities = np.exp(log_weights - np.logaddexp.reduce(log_weights))
        counts = {
            int(size): int(count)
            for size, count in zip(
                sizes, np.rint(2_000_000 * probabilities).astype(int), strict=True
            )
            if count
        }
        fit = fit_stretched_cutoff_power_law(counts, xmin=xmin)
        self.assertAlmostEqual(fit.parameters["alpha"], alpha, delta=0.04)
        self.assertAlmostEqual(fit.parameters["scale"], scale, delta=3.0)
        self.assertAlmostEqual(fit.parameters["beta"], beta, delta=0.12)
        self.assertLess(fit.ks, 0.002)
        sampled = sample_model_counts(
            25_000, fit, rng=np.random.default_rng(9191)
        )
        self.assertEqual(sum(sampled.values()), 25_000)
        self.assertGreaterEqual(min(sampled), xmin)

    def test_histogram_sampler_and_parametric_gof_are_reproducible(self):
        rate = 0.3
        sizes = np.arange(2, 80)
        probabilities = (1.0 - np.exp(-rate)) * np.exp(-rate * (sizes - 2))
        counts = {
            int(size): int(count)
            for size, count in zip(
                sizes, np.rint(20_000 * probabilities).astype(int), strict=True
            )
            if count
        }
        fitted = fit_exponential(counts, xmin=2)
        sampled = sample_model_counts(
            20_000, fitted, rng=np.random.default_rng(1234)
        )
        self.assertEqual(sum(sampled.values()), 20_000)
        first = parametric_gof(
            counts, model="exponential", xmin=2, replicates=9, seed=5678
        )
        second = parametric_gof(
            counts, model="exponential", xmin=2, replicates=9, seed=5678
        )
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()

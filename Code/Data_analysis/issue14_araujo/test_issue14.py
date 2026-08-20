from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from issue14_araujo.data import audit_raw_file, reconstruct_counts_from_pmf
from issue14_araujo.models import (
    araujo_logpmf,
    araujo_score,
    cutoff_cdf,
    finite_difference_gradient,
    fit_model,
)
from issue14_araujo.synthetic import (
    histogram,
    sample_araujo,
    sample_lognormal_histogram,
    sample_power_law,
    sample_power_law_histogram,
    select_power_law_xmin,
)


class AraujoFormulaTest(unittest.TestCase):
    def test_survival_difference_matches_hand_calculation(self) -> None:
        sizes = np.array([2.0, 3.0, 4.0])
        alpha, eta, s0, xmin = 0.5, 1.5, 7.0, 2

        def survival(x: np.ndarray) -> np.ndarray:
            return x ** (-alpha) * np.exp(-((x / s0) ** eta))

        expected = (survival(sizes) - survival(sizes + 1.0)) / survival(np.array([xmin]))
        actual = np.exp(
            araujo_logpmf(
                sizes, xmin=xmin, alpha=alpha, eta=eta, s0=s0
            )
        )
        np.testing.assert_allclose(actual, expected, rtol=2e-14, atol=0.0)

    def test_infinite_support_normalizes_without_truncation(self) -> None:
        sizes = np.arange(2, 200_000)
        probabilities = np.exp(
            araujo_logpmf(
                sizes, xmin=2, alpha=0.075, eta=2.0, s0=150.0
            )
        )
        self.assertAlmostEqual(float(probabilities.sum()), 1.0, places=12)

    def test_tau_is_alpha_plus_one_in_the_continuous_density(self) -> None:
        alpha = 0.255
        tau = alpha + 1.0
        x, eta, s0 = 10.0, 1.5, 100.0
        alpha_form = x ** (-(alpha + 1.0)) * (
            alpha + eta * (x / s0) ** eta
        ) * np.exp(-((x / s0) ** eta))
        tau_form = x ** (-tau) * (
            (tau - 1.0) + eta * (x / s0) ** eta
        ) * np.exp(-((x / s0) ** eta))
        self.assertAlmostEqual(alpha_form, tau_form, places=15)

    def test_analytic_score_agrees_with_finite_differences(self) -> None:
        sizes = np.arange(2, 15)
        frequencies = np.arange(1, sizes.size + 1)
        point = np.array([0.255, np.log(1.5), np.log(80.0)])

        def objective(x: np.ndarray) -> float:
            return -float(
                np.dot(
                    frequencies,
                    araujo_logpmf(
                        sizes,
                        xmin=2,
                        alpha=float(x[0]),
                        eta=float(np.exp(x[1])),
                        s0=float(np.exp(x[2])),
                    ),
                )
            )

        analytical = -np.dot(
            frequencies,
            araujo_score(
                sizes, xmin=2, alpha=point[0], eta=np.exp(point[1]), s0=np.exp(point[2])
            ),
        )
        numerical = finite_difference_gradient(objective, point)
        np.testing.assert_allclose(analytical, numerical, rtol=2e-6, atol=2e-6)

    def test_large_s0_limit_is_discrete_power_survival(self) -> None:
        sizes = np.arange(2, 20)
        alpha, s0 = 0.7, 1e12
        actual = np.exp(
            araujo_logpmf(sizes, xmin=2, alpha=alpha, eta=1.3, s0=s0)
        )
        expected = (sizes / 2.0) ** (-alpha) - ((sizes + 1.0) / 2.0) ** (-alpha)
        np.testing.assert_allclose(actual, expected, rtol=2e-10, atol=1e-13)


class EstimationTest(unittest.TestCase):
    def test_recovers_published_araujo_example(self) -> None:
        rng = np.random.default_rng(1401)
        sample = sample_araujo(
            rng, 20_000, alpha=0.255, eta=1.5, s0=100.0, xmin=2
        )
        fit = fit_model(histogram(sample), "araujo", xmin=2)
        self.assertTrue(fit.converged)
        self.assertLess(abs(fit.parameters["alpha"] - 0.255), 0.08)
        self.assertLess(abs(fit.parameters["eta"] - 1.5), 0.25)
        self.assertLess(abs(fit.parameters["s0"] - 100.0) / 100.0, 0.2)

    def test_power_law_benchmark_and_cutoff_selection(self) -> None:
        rng = np.random.default_rng(1402)
        body = rng.choice([1, 2, 3, 4], size=2_000)
        tail = sample_power_law(rng, 4_000, alpha=2.5, xmin=5)
        counts = histogram(np.concatenate((body, tail)))
        fit = select_power_law_xmin(counts, minimum_tail=500)
        self.assertIn(fit.xmin, range(4, 8))
        self.assertLess(abs(fit.parameters["alpha"] - 2.5), 0.2)

    def test_boundary_adjacent_araujo_parameters_remain_finite(self) -> None:
        rng = np.random.default_rng(1403)
        sample = sample_araujo(
            rng, 5_000, alpha=0.015, eta=0.22, s0=30.0, xmin=2
        )
        fit = fit_model(histogram(sample), "araujo", xmin=2)
        self.assertTrue(np.all(np.isfinite(list(fit.parameters.values()))))
        self.assertGreater(fit.parameters["alpha"], 0.0)
        self.assertGreater(fit.parameters["eta"], 0.0)
        self.assertGreater(fit.parameters["s0"], 0.0)

    def test_cutoff_normalization_cdf_reaches_one(self) -> None:
        after, _ = cutoff_cdf(
            np.array([100_000]), xmin=2, alpha=1.2, rate=0.01
        )
        self.assertGreater(float(after[0]), 1.0 - 1e-10)

    def test_exact_histogram_samplers_preserve_requested_counts(self) -> None:
        rng = np.random.default_rng(1404)
        power = sample_power_law_histogram(
            rng, 200_000, alpha=2.3, xmin=2
        )
        lognormal = sample_lognormal_histogram(
            rng, 200_000, mu=2.0, sigma=1.1, xmin=2
        )
        self.assertEqual(sum(power.values()), 200_000)
        self.assertEqual(sum(lognormal.values()), 200_000)
        expected_p2 = 2.0 ** -2.3 / sum(
            value ** -2.3 for value in range(2, 200_000)
        )
        self.assertLess(abs(power.get(2, 0) / 200_000 - expected_p2), 0.004)
        self.assertGreater(max(power), 128)


class RawAuditTest(unittest.TestCase):
    def test_pmf_denominator_consensus_does_not_assume_minimum_is_one_count(self) -> None:
        counts, evidence = reconstruct_counts_from_pmf(
            np.array([1, 2, 3]),
            np.array([0.2, 0.3, 0.5])
        )
        np.testing.assert_array_equal(counts, np.array([0, 2, 3, 5]))
        self.assertEqual(int(counts.sum()), 10)
        self.assertEqual(evidence["distinct_reduced_denominators"], 3)

    def test_preserves_terminal_partition_and_disconnected_clusters(self) -> None:
        fixture = (
            b'f,num_active_particles,num_deleted_particles,total_deleted_rods,avalanche_sizes\n'
            b'0,10,0,0,"0"\n0.5,7,3,3,"2-1"\n1,0,10,4,"4"\n'
            b'----------------------------------------------1\n'
            b'0,8,0,0,"0"\n0.5,5,3,3,"3"\n1,0,8,5,"4-1"\n'
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ts_8_seed_130_m_2.txt"
            path.write_bytes(fixture)
            audit = audit_raw_file(path)
        self.assertEqual(audit.runs, 2)
        self.assertEqual(audit.terminal_rows, 2)
        self.assertEqual(audit.all_counts, {1: 2, 2: 1, 3: 1, 4: 2})
        self.assertEqual(audit.preterminal_counts, {1: 1, 2: 1, 3: 1})


if __name__ == "__main__":
    unittest.main()

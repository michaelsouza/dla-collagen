import tempfile
import unittest
from unittest import mock
from pathlib import Path

import numpy as np
from scipy import sparse, special
from scipy.optimize import OptimizeResult

from Code.Data_analysis.avalanche_statistics import (
    DistributionFit,
    clauset_power_law_gof,
    cutoff_power_law_likelihood_ratio_test,
    distribution_log_probabilities,
    distribution_cdf,
    equal_fibril_weight_counts,
    fit_cutoff_power_law,
    fit_competing_models,
    fit_discrete_power_law,
    fit_discrete_exponential,
    fit_discrete_lognormal,
    hierarchical_resample_counts,
    hierarchical_resample_fibril_counts,
    load_avalanche_condition,
    parametric_distribution_gof,
    parse_avalanche_file,
    sample_fitted_distribution_counts,
    sample_discrete_power_law_counts,
    select_power_law_xmin,
)


class AvalancheFileParserTest(unittest.TestCase):
    def test_parser_preserves_runs_and_separates_terminal_clusters(self):
        fixture = (
            "f,num_active_particles,num_deleted_particles,total_deleted_rods,avalanche_sizes\n"
            '0,100,0,0,"0"\n'
            '0.5,90,10,3,"2-1"\n'
            '1.0,0,100,4,"4"\n'
            "----------------------------------------------1\n"
            '0,100,0,0,"0"\n'
            '0.5,80,20,4,"3-1"\n'
            '1.0,0,100,5,"5"\n'
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "ts_8_seed_130_m_2.txt"
            source.write_text(fixture, encoding="utf-8")

            parsed = parse_avalanche_file(source, expected_runs=2)

        self.assertEqual(parsed.ts, 8)
        self.assertEqual(parsed.fibril_seed, 130)
        self.assertEqual(parsed.run_ids, (0, 1))
        self.assertEqual(parsed.initial_particles, 100)
        self.assertEqual(len(parsed.source_sha256), 64)
        np.testing.assert_array_equal(
            parsed.aggregate_counts(include_terminal=False),
            np.array([0, 2, 1, 1, 0, 0]),
        )
        np.testing.assert_array_equal(
            parsed.aggregate_counts(include_terminal=True),
            np.array([0, 2, 1, 1, 1, 1]),
        )

    def test_parser_rejects_cluster_mass_that_disagrees_with_row_total(self):
        fixture = (
            "f,num_active_particles,num_deleted_particles,total_deleted_rods,avalanche_sizes\n"
            '0,10,0,0,"0"\n'
            '0.5,8,2,3,"2"\n'
            '1.0,0,10,4,"4"\n'
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "ts_8_seed_130_m_2.txt"
            source.write_text(fixture, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "cluster-size sum"):
                parse_avalanche_file(source, expected_runs=1)

    def test_parser_rejects_corrupt_run_structure(self):
        header = (
            "f,num_active_particles,num_deleted_particles,total_deleted_rods,"
            "avalanche_sizes\n"
        )
        corrupt_fixtures = {
            "noncontiguous separator": (
                header
                + '0,10,0,0,"0"\n1,0,10,3,"3"\n'
                + "----------------------------------------------2\n"
                + '0,10,0,0,"0"\n1,0,10,3,"3"\n'
            ),
            "separator before terminal": (
                header
                + '0,10,0,0,"0"\n'
                + "----------------------------------------------1\n"
                + '0,10,0,0,"0"\n1,0,10,3,"3"\n'
            ),
            "missing final terminal row": header + '0,10,0,0,"0"\n0.5,8,2,2,"2"\n',
            "row after terminal": (
                header + '0,10,0,0,"0"\n0.5,0,10,3,"3"\n1,0,10,4,"4"\n'
            ),
            "invalid initial state": header + '0,9,1,0,"0"\n0.5,0,10,3,"3"\n',
            "particle conservation": header + '0,10,0,0,"0"\n0.5,7,2,2,"2"\n1,0,10,3,"3"\n',
            "force step": header + '0,10,0,0,"0"\n0.75,8,2,2,"2"\n1.25,0,10,3,"3"\n',
            "malformed sizes": header + '0,10,0,0,"0"\n0.5,8,2,2,"1--1"\n1,0,10,3,"3"\n',
            "repeated header": (
                header + '0,10,0,0,"0"\n' + header + '0.5,0,10,3,"3"\n'
            ),
        }

        for name, fixture in corrupt_fixtures.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / "ts_8_seed_130_m_2.txt"
                source.write_text(fixture, encoding="utf-8")
                with self.assertRaises(ValueError):
                    parse_avalanche_file(source)

    def test_condition_loader_preserves_fibril_and_run_blocks(self):
        header = (
            "f,num_active_particles,num_deleted_particles,total_deleted_rods,"
            "avalanche_sizes\n"
        )
        first = (
            header
            + '0,10,0,0,"0"\n0.5,8,2,3,"2-1"\n1,0,10,4,"4"\n'
            + "----------------------------------------------1\n"
            + '0,10,0,0,"0"\n0.5,7,3,3,"3"\n1,0,10,5,"5"\n'
        )
        second = (
            header
            + '0,10,0,0,"0"\n0.5,8,2,2,"1-1"\n1,0,10,6,"6"\n'
            + "----------------------------------------------1\n"
            + '0,10,0,0,"0"\n0.5,8,2,2,"2"\n1,0,10,7,"7"\n'
        )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "ts_8_seed_20_m_2.txt").write_text(first, encoding="utf-8")
            (root / "ts_8_seed_10_m_2.txt").write_text(second, encoding="utf-8")

            condition = load_avalanche_condition(
                root, ts=8, expected_fibrils=2, expected_runs=2
            )

        self.assertEqual(condition.fibril_seeds, (10, 20))
        self.assertEqual(condition.run_counts(include_terminal=False).shape, (4, 8))
        self.assertEqual(condition.fibril_counts(include_terminal=False).shape, (2, 8))
        np.testing.assert_array_equal(
            condition.aggregate_counts(include_terminal=False),
            np.array([0, 3, 2, 1, 0, 0, 0, 0]),
        )


class DiscretePowerLawTest(unittest.TestCase):
    def test_sparse_gap_fixture_matches_high_precision_oracle(self):
        fit = fit_discrete_power_law({2: 40, 3: 25, 4: 20, 8: 15}, xmin=2)

        self.assertAlmostEqual(fit.parameters["gamma"], 2.4838842719154615, places=6)
        self.assertAlmostEqual(fit.log_likelihood, -177.82176408713539, places=6)
        self.assertAlmostEqual(fit.ks, 0.11397181497801836, places=7)

    def test_exact_mle_uses_the_discrete_hurwitz_zeta_likelihood(self):
        counts = np.zeros(11, dtype=np.int64)
        counts[2:] = [80, 35, 20, 10, 7, 5, 3, 2, 1]

        fit = fit_discrete_power_law(counts, xmin=2)

        self.assertEqual(fit.model, "power_law")
        self.assertEqual(fit.xmin, 2)
        self.assertEqual(fit.n, 163)
        self.assertAlmostEqual(fit.parameters["gamma"], 2.7006561256776925, places=7)
        self.assertGreaterEqual(fit.ks, 0.0)
        self.assertLessEqual(fit.ks, 1.0)

    def test_xmin_selection_excludes_a_deliberately_non_power_law_body(self):
        sizes = np.arange(5, 2001, dtype=float)
        probabilities = sizes ** -2.5
        probabilities /= probabilities.sum()
        counts = np.zeros(2001, dtype=np.int64)
        counts[5:] = np.rint(2_000_000 * probabilities).astype(np.int64)
        counts[2:5] = [900_000, 10_000, 500_000]

        fit = select_power_law_xmin(counts, xmin_min=2, min_tail=10_000)

        self.assertEqual(fit.xmin, 5)
        self.assertAlmostEqual(fit.parameters["gamma"], 2.5, delta=0.01)

    def test_exact_hurwitz_sampler_returns_a_sparse_recoverable_histogram(self):
        rng = np.random.default_rng(918273)

        sampled = sample_discrete_power_law_counts(
            200_000, gamma=2.5, xmin=3, rng=rng
        )
        fit = fit_discrete_power_law(sampled, xmin=3)

        self.assertEqual(sum(sampled.values()), 200_000)
        self.assertGreaterEqual(min(sampled), 3)
        self.assertAlmostEqual(fit.parameters["gamma"], 2.5, delta=0.02)

    def test_semiparametric_gof_is_reproducible_and_refits_each_replica(self):
        tail = sample_discrete_power_law_counts(
            3_000,
            gamma=2.4,
            xmin=5,
            rng=np.random.default_rng(1909),
        )
        counts = {2: 2_250, 3: 300, 4: 1_800, **tail}

        first = clauset_power_law_gof(
            counts,
            xmin_min=2,
            min_tail=200,
            replicates=49,
            seed=57_721,
        )
        second = clauset_power_law_gof(
            counts,
            xmin_min=2,
            min_tail=200,
            replicates=49,
            seed=57_721,
        )

        self.assertEqual(first, second)
        self.assertEqual(first.observed_fit.xmin, 5)
        self.assertGreater(first.p_value, 0.1)
        self.assertEqual(len(first.synthetic_xmins), 49)
        self.assertGreater(len(set(first.synthetic_xmins)), 1)
        self.assertGreater(len(set(first.synthetic_tail_counts)), 1)

        serial = clauset_power_law_gof(
            counts,
            xmin_min=2,
            min_tail=200,
            replicates=7,
            seed=12_738,
            workers=1,
        )
        parallel = clauset_power_law_gof(
            counts,
            xmin_min=2,
            min_tail=200,
            replicates=7,
            seed=12_738,
            workers=2,
        )
        self.assertEqual(serial, parallel)


class AlternativeDistributionTest(unittest.TestCase):
    def test_lognormal_ignores_a_lower_failed_optimizer_candidate(self):
        transformed_results = [
            OptimizeResult(success=True, fun=10.0, x=np.array([2.0, np.log(0.1)])),
            OptimizeResult(
                success=False,
                fun=9.0,
                x=np.array([2.0, np.log(1e-6)]),
                message="ABNORMAL",
            ),
            OptimizeResult(success=True, fun=11.0, x=np.array([2.0, np.log(0.2)])),
            OptimizeResult(success=True, fun=12.0, x=np.array([2.0, np.log(0.3)])),
        ]
        direct_results = [
            OptimizeResult(success=True, fun=20.0, x=np.array([1.0, 0.0]))
            for _ in range(4)
        ]

        with mock.patch(
            "Code.Data_analysis.avalanche_statistics.optimize.minimize",
            side_effect=transformed_results + direct_results,
        ):
            fit = fit_discrete_lognormal({4: 10, 5: 5}, xmin=4)

        self.assertEqual(fit.diagnostics["lognormal_parameterization"], "gamma_curvature")
        self.assertAlmostEqual(fit.log_likelihood, -150.0)

    def test_fitted_distribution_samplers_recover_their_parameters(self):
        fixtures = (
            DistributionFit(
                model="exponential",
                xmin=2,
                parameters={"lambda": 0.4},
                log_likelihood=0.0,
                ks=0.0,
                n=50_000,
            ),
            DistributionFit(
                model="lognormal",
                xmin=2,
                parameters={"mu": 2.0, "sigma": 0.6},
                log_likelihood=0.0,
                ks=0.0,
                n=50_000,
            ),
            DistributionFit(
                model="cutoff_power_law",
                xmin=2,
                parameters={"gamma": 1.4, "lambda": 0.08},
                log_likelihood=0.0,
                ks=0.0,
                n=50_000,
            ),
        )
        fitters = {
            "exponential": fit_discrete_exponential,
            "lognormal": fit_discrete_lognormal,
            "cutoff_power_law": fit_cutoff_power_law,
        }

        for index, expected in enumerate(fixtures):
            with self.subTest(model=expected.model):
                sampled = sample_fitted_distribution_counts(
                    50_000,
                    expected,
                    rng=np.random.default_rng(73_001 + index),
                )
                recovered = fitters[expected.model](sampled, xmin=expected.xmin)
                self.assertEqual(sum(sampled.values()), 50_000)
                self.assertGreaterEqual(min(sampled), expected.xmin)
                for parameter, value in expected.parameters.items():
                    tolerance = 0.03 if parameter != "lambda" else 0.01
                    self.assertAlmostEqual(
                        recovered.parameters[parameter], value, delta=tolerance
                    )

    def test_low_rate_cutoff_sampler_does_not_truncate_large_acceptances(self):
        expected = DistributionFit(
            model="cutoff_power_law",
            xmin=2,
            parameters={"gamma": 1.5, "lambda": 1e-5},
            log_likelihood=0.0,
            ks=0.0,
            n=20_000,
        )

        sampled = sample_fitted_distribution_counts(
            20_000,
            expected,
            rng=np.random.default_rng(8_675_309),
        )
        sampled_mean = sum(size * count for size, count in sampled.items()) / 20_000

        self.assertAlmostEqual(sampled_mean, 348.52, delta=60.0)

    def test_lognormal_sampler_handles_an_extreme_conditioned_tail(self):
        expected = DistributionFit(
            model="lognormal",
            xmin=4,
            parameters={"mu": -2.85e6, "sigma": 1_801.0},
            log_likelihood=0.0,
            ks=0.0,
            n=2_000,
        )

        sampled = sample_fitted_distribution_counts(
            2_000,
            expected,
            rng=np.random.default_rng(99_001),
        )

        self.assertEqual(sum(sampled.values()), 2_000)
        self.assertGreaterEqual(min(sampled), expected.xmin)
        self.assertLess(max(sampled), 1_000_000)

    def test_parametric_gof_refits_and_is_reproducible_across_workers(self):
        sizes = np.arange(2, 80)
        q = 0.68
        probabilities = (1.0 - q) * q ** (sizes - 2)
        counts = {
            int(size): int(count)
            for size, count in zip(
                sizes,
                np.rint(20_000 * probabilities).astype(int),
                strict=True,
            )
            if count
        }

        serial = parametric_distribution_gof(
            counts,
            model="exponential",
            xmin=2,
            replicates=11,
            seed=12_738,
            workers=1,
        )
        parallel = parametric_distribution_gof(
            counts,
            model="exponential",
            xmin=2,
            replicates=11,
            seed=12_738,
            workers=2,
        )

        self.assertEqual(serial, parallel)
        self.assertEqual(serial.replicates, 11)
        self.assertEqual(len(serial.synthetic_ks), 11)
        self.assertGreater(serial.p_value, 0.0)
        self.assertLessEqual(serial.p_value, 1.0)

        with self.assertRaisesRegex(ValueError, "integer event frequencies"):
            parametric_distribution_gof(
                {2: 0.5, 3: 0.5},
                model="exponential",
                xmin=2,
                replicates=3,
            )

    def test_power_law_gof_rejects_a_clear_cutoff_fixture(self):
        generating_fit = DistributionFit(
            model="cutoff_power_law",
            xmin=2,
            parameters={"gamma": 1.3, "lambda": 0.08},
            log_likelihood=0.0,
            ks=0.0,
            n=5_000,
        )
        counts = sample_fitted_distribution_counts(
            5_000,
            generating_fit,
            rng=np.random.default_rng(12_738),
        )

        result = clauset_power_law_gof(
            counts,
            xmin_min=2,
            min_tail=500,
            replicates=49,
            seed=57_721,
            workers=2,
        )

        self.assertLessEqual(result.p_value, 0.1)

    def test_cutoff_normalization_matches_analytic_and_high_rate_oracles(self):
        analytic = DistributionFit(
            model="cutoff_power_law",
            xmin=2,
            parameters={"gamma": 1.0, "lambda": np.log(2.0)},
            log_likelihood=0.0,
            ks=0.0,
            n=1.0,
        )
        high_rate = DistributionFit(
            model="cutoff_power_law",
            xmin=4,
            parameters={"gamma": 1.0, "lambda": 10.0},
            log_likelihood=0.0,
            ks=0.0,
            n=1.0,
        )

        self.assertAlmostEqual(
            distribution_log_probabilities(analytic, np.array([2]))[0],
            -0.4351387545506944,
            places=12,
        )
        self.assertAlmostEqual(
            distribution_log_probabilities(high_rate, np.array([4]))[0],
            -0.00003632065836277943,
            places=12,
        )

    def test_discrete_exponential_mle_recovers_a_geometric_tail(self):
        sizes = np.arange(2, 101)
        q = 0.7
        probabilities = (1.0 - q) * q ** (sizes - 2)
        counts = np.zeros(101, dtype=np.int64)
        counts[2:] = np.rint(1_000_000 * probabilities).astype(np.int64)

        fit = fit_discrete_exponential(counts, xmin=2)

        self.assertAlmostEqual(fit.parameters["lambda"], -np.log(q), delta=1e-4)

    def test_discrete_lognormal_mle_recovers_rounded_bin_probabilities(self):
        xmin = 2
        mu = 2.0
        sigma = 0.6
        sizes = np.arange(xmin, 101, dtype=float)
        upper = (np.log(sizes + 0.5) - mu) / sigma
        lower = (np.log(sizes - 0.5) - mu) / sigma
        normalizer = special.ndtr(-(np.log(xmin - 0.5) - mu) / sigma)
        probabilities = (special.ndtr(upper) - special.ndtr(lower)) / normalizer
        counts = np.zeros(101, dtype=np.int64)
        counts[xmin:] = np.rint(2_000_000 * probabilities).astype(np.int64)

        fit = fit_discrete_lognormal(counts, xmin=xmin)

        self.assertAlmostEqual(fit.parameters["mu"], mu, delta=0.01)
        self.assertAlmostEqual(fit.parameters["sigma"], sigma, delta=0.01)

    def test_cutoff_power_law_mle_recovers_a_discrete_cutoff_tail(self):
        xmin = 2
        gamma = 1.4
        rate = 0.08
        sizes = np.arange(xmin, 401, dtype=float)
        weights = sizes ** -gamma * np.exp(-rate * sizes)
        probabilities = weights / weights.sum()
        counts = np.zeros(401, dtype=np.int64)
        counts[xmin:] = np.rint(2_000_000 * probabilities).astype(np.int64)

        fit = fit_cutoff_power_law(counts, xmin=xmin)

        self.assertAlmostEqual(fit.parameters["gamma"], gamma, delta=0.02)
        self.assertAlmostEqual(fit.parameters["lambda"], rate, delta=0.005)

    def test_all_model_comparisons_use_the_same_tail_support(self):
        sizes = np.arange(4, 301, dtype=float)
        weights = sizes ** -1.4 * np.exp(-0.08 * sizes)
        tail = {
            int(size): int(count)
            for size, count in zip(
                sizes, np.rint(200_000 * weights / weights.sum()).astype(int), strict=True
            )
            if count
        }
        contaminated = {2: 70_000, 3: 90_000, **tail}

        tail_fits = fit_competing_models(tail, xmin=4)
        contaminated_fits = fit_competing_models(contaminated, xmin=4)

        self.assertEqual(set(tail_fits), set(contaminated_fits))
        for model in tail_fits:
            self.assertEqual(tail_fits[model].xmin, 4)
            self.assertEqual(tail_fits[model].n, contaminated_fits[model].n)
            self.assertAlmostEqual(
                tail_fits[model].log_likelihood,
                contaminated_fits[model].log_likelihood,
                places=7,
            )
            support = np.asarray(sorted(tail), dtype=int)
            frequencies = np.asarray([tail[int(size)] for size in support])
            evaluated = np.dot(
                frequencies,
                distribution_log_probabilities(tail_fits[model], support),
            )
            self.assertAlmostEqual(
                evaluated, tail_fits[model].log_likelihood, places=6
            )
            cdf = distribution_cdf(tail_fits[model], support)
            self.assertTrue(np.all(np.diff(cdf) >= -1e-12))
            self.assertTrue(np.all((cdf >= 0.0) & (cdf <= 1.0)))
        self.assertGreater(
            tail_fits["cutoff_power_law"].log_likelihood
            - tail_fits["power_law"].log_likelihood,
            100.0,
        )

    def test_nested_cutoff_likelihood_ratio_uses_parametric_bootstrap(self):
        counts = sample_discrete_power_law_counts(
            5_000,
            gamma=2.3,
            xmin=3,
            rng=np.random.default_rng(91),
        )

        first = cutoff_power_law_likelihood_ratio_test(
            counts, xmin=3, replicates=19, seed=8128, workers=1
        )
        second = cutoff_power_law_likelihood_ratio_test(
            counts, xmin=3, replicates=19, seed=8128, workers=1
        )

        self.assertEqual(first, second)
        self.assertEqual(first.replicates, 19)
        self.assertGreaterEqual(first.observed_likelihood_ratio, 0.0)
        self.assertGreater(first.p_value, 0.0)
        self.assertLessEqual(first.p_value, 1.0)


class HierarchicalBootstrapTest(unittest.TestCase):
    @staticmethod
    def _single_event_runs(values):
        width = max(values) + 1
        rows = np.arange(len(values))
        return sparse.csr_matrix(
            (np.ones(len(values), dtype=np.int64), (rows, values)),
            shape=(len(values), width),
        )

    def test_resampling_contains_both_fibril_and_run_levels(self):
        fixture_a = [self._single_event_runs([2, 2]), self._single_event_runs([12, 12])]
        fixture_b = [self._single_event_runs([2, 12]), self._single_event_runs([2, 12])]

        def sampled_means(fixture, seed):
            rng = np.random.default_rng(seed)
            means = []
            for _ in range(10_000):
                counts = hierarchical_resample_counts(fixture, rng=rng)
                means.append(np.dot(np.arange(counts.size), counts) / counts.sum())
            return np.asarray(means)

        means_a = sampled_means(fixture_a, 424_242)
        means_b = sampled_means(fixture_b, 424_243)

        self.assertAlmostEqual(means_a.mean(), 7.0, delta=0.10)
        self.assertAlmostEqual(means_a.var(), 12.5, delta=0.40)
        self.assertAlmostEqual(means_b.mean(), 7.0, delta=0.10)
        self.assertAlmostEqual(means_b.var(), 6.25, delta=0.40)

    def test_block_resampler_preserves_the_bootstrap_fibril_rows(self):
        fixture = [self._single_event_runs([2, 3]), self._single_event_runs([7, 8])]

        sampled = hierarchical_resample_fibril_counts(
            fixture, rng=np.random.default_rng(12738)
        )

        self.assertEqual(sampled.shape, (2, 9))
        self.assertTrue(np.all(sampled.sum(axis=1) == 2))

    def test_equal_fibril_weighting_does_not_favor_event_rich_fibrils(self):
        by_fibril = np.zeros((2, 5), dtype=np.int64)
        by_fibril[0, 2] = 100
        by_fibril[1, 4] = 10

        weighted = equal_fibril_weight_counts(by_fibril, min_size=2)
        probabilities = weighted / weighted.sum()

        self.assertAlmostEqual(probabilities[2], 0.5)
        self.assertAlmostEqual(probabilities[4], 0.5)


if __name__ == "__main__":
    unittest.main()

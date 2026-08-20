import tempfile
import unittest
from pathlib import Path

import duckdb
import numpy as np

from clauset_pooled.gof import sample_power_law_counts
from clauset_pooled.alternative_gof import sample_model_counts
from clauset_pooled.models import fit_exponential

from .analysis import (
    FibrilHistograms,
    fit_block_power_law,
    fit_block_model_gof,
    load_fibril_histograms,
    select_model_xmin,
)
from .diagnostics import leave_one_fibril_out, subset_stability, weighted_quantile
from .stretched_cutoff import (
    JointStretchedCutoffFit,
    fit_joint_stretched_cutoff,
    select_joint_stretched_cutoff_xmin,
)


class HierarchicalDataTest(unittest.TestCase):
    def test_loader_retains_fibrils_and_excludes_terminal_events(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "analysis.duckdb"
            connection = duckdb.connect(str(database))
            connection.execute("""
                CREATE TABLE fibril_histograms (
                    ts INTEGER, seed INTEGER, avalanche_size INTEGER,
                    event_count INTEGER, is_terminal_step BOOLEAN
                );
                INSERT INTO fibril_histograms VALUES
                    (2, 10, 1, 5, false), (2, 10, 3, 2, false),
                    (2, 10, 8, 1, true), (2, 20, 2, 4, false);
            """)
            connection.close()

            loaded = load_fibril_histograms(database, 2)

            np.testing.assert_array_equal(loaded.seeds, [10, 20])
            self.assertEqual(loaded.counts[0, 1], 5)
            self.assertEqual(loaded.counts[0, 3], 2)
            self.assertEqual(loaded.counts.shape[1], 4)


class BlockPowerLawTest(unittest.TestCase):
    def make_power_law_blocks(self) -> FibrilHistograms:
        histograms = [
            sample_power_law_counts(
                1500, xmin=3, alpha=2.4,
                rng=np.random.default_rng(1000 + index),
            )
            for index in range(30)
        ]
        maximum = max(max(histogram) for histogram in histograms)
        counts = np.zeros((len(histograms), maximum + 1), dtype=np.int64)
        for row, histogram in enumerate(histograms):
            for size, count in histogram.items():
                counts[row, size] = count
        return FibrilHistograms(
            ts=8, seeds=np.arange(len(histograms)), counts=counts
        )

    def test_block_fit_is_reproducible_and_recovers_power_law(self):
        data = self.make_power_law_blocks()
        first = fit_block_power_law(
            data, minimum_tail=500, replicates=39, seed=2026
        )
        second = fit_block_power_law(
            data, minimum_tail=500, replicates=39, seed=2026
        )

        self.assertEqual(first, second)
        self.assertGreaterEqual(first.observed.xmin, 3)
        self.assertAlmostEqual(first.observed.alpha, 2.4, delta=0.06)
        self.assertGreaterEqual(first.p_value, 0.10)

        subsets = subset_stability(
            data,
            subset_sizes=(10, 30),
            repetitions=2,
            minimum_tail=200,
            seed=55,
        )
        self.assertEqual(subsets, subset_stability(
            data,
            subset_sizes=(10, 30),
            repetitions=2,
            minimum_tail=200,
            seed=55,
        ))
        self.assertEqual(len(subsets), 3)
        self.assertEqual(len(leave_one_fibril_out(data, minimum_tail=200)), 30)
        self.assertEqual(len(first.bootstrap), 39)

    def test_block_exponential_gof_is_reproducible(self):
        rate = 0.3
        template = fit_exponential({2: 700, 3: 200, 4: 100}, xmin=2)
        template = type(template)(
            model=template.model,
            xmin=template.xmin,
            parameters={"lambda": rate},
            log_likelihood=template.log_likelihood,
            ks=template.ks,
            n_tail=template.n_tail,
            parameter_count=template.parameter_count,
        )
        histograms = [
            sample_model_counts(
                1000, template, rng=np.random.default_rng(3000 + index)
            )
            for index in range(25)
        ]
        maximum = max(max(histogram) for histogram in histograms)
        counts = np.zeros((25, maximum + 1), dtype=np.int64)
        for row, histogram in enumerate(histograms):
            for size, count in histogram.items():
                counts[row, size] = count
        data = FibrilHistograms(ts=2, seeds=np.arange(25), counts=counts)

        first = fit_block_model_gof(
            data, model="exponential", xmin=2, replicates=19, seed=44
        )
        second = fit_block_model_gof(
            data, model="exponential", xmin=2, replicates=19, seed=44
        )

        self.assertEqual(first, second)
        self.assertGreaterEqual(first.p_value, 0.10)
        self.assertEqual(len(first.bootstrap), 19)
        self.assertIn("lambda", first.bootstrap[0].parameters)

        selection = select_model_xmin(
            data,
            model="exponential",
            minimum_xmin=2,
            maximum_xmin=5,
            minimum_tail=100,
        )
        self.assertEqual(
            selection.selected.ks,
            min(fit.ks for fit in selection.candidates),
        )
        self.assertEqual(
            tuple(fit.xmin for fit in selection.candidates), (2, 3, 4, 5)
        )


class DiagnosticUtilityTest(unittest.TestCase):
    def test_weighted_integer_quantile(self):
        histogram = np.array([0, 2, 3, 0, 5])
        self.assertEqual(weighted_quantile(histogram, 0.0), 1)
        self.assertEqual(weighted_quantile(histogram, 0.5), 2)
        self.assertEqual(weighted_quantile(histogram, 0.51), 4)

    def test_joint_stretched_cutoff_recovers_common_shape(self):
        alpha = 2.2
        beta = 1.6
        xmin = 8
        datasets = []
        for ts, scale in ((512, 55.0), (1024, 105.0)):
            support = np.arange(xmin, 1200)
            weights = (support / xmin) ** (-alpha) * np.exp(
                -(support / scale) ** beta
            )
            frequencies = np.rint(800_000 * weights / weights.sum()).astype(np.int64)
            counts = np.zeros((10, support[-1] + 1), dtype=np.int64)
            for block in range(10):
                counts[block, support] = (
                    frequencies // 10 + (frequencies % 10 > block)
                )
            datasets.append(FibrilHistograms(
                ts=ts, seeds=np.arange(10), counts=counts
            ))
        initial = JointStretchedCutoffFit(
            xmin=xmin,
            ts_values=(512, 1024),
            alpha=alpha,
            beta=beta,
            scales=(55.0, 105.0),
            log_likelihood=float("nan"),
            n_tail=(0, 0),
            ks=(0.0, 0.0),
        )
        fitted = fit_joint_stretched_cutoff(
            tuple(datasets), xmin=xmin, initial=initial
        )
        self.assertAlmostEqual(fitted.alpha, alpha, delta=0.04)
        self.assertAlmostEqual(fitted.beta, beta, delta=0.10)
        self.assertAlmostEqual(fitted.scales[0], 55.0, delta=3.0)
        self.assertAlmostEqual(fitted.scales[1], 105.0, delta=5.0)

        selection = select_joint_stretched_cutoff_xmin(
            tuple(datasets),
            candidates=(6, 8, 10),
            minimum_tail=1000,
        )
        self.assertEqual(selection.selected.xmin, 8)
        self.assertEqual(
            tuple(fit.xmin for fit in selection.candidates), (6, 8, 10)
        )


if __name__ == "__main__":
    unittest.main()

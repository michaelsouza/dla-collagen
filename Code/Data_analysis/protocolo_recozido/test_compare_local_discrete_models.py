import unittest
from collections import Counter

import numpy as np

from compare_local_discrete_models import (
    MODEL_ORDER,
    comparison_rows,
    fit_models,
    model_ccdf,
)
from fit_local_power_law import PowerLawFit


def selected_fit(counts: Counter[int], xmin: int) -> PowerLawFit:
    n = sum(counts.values())
    xmax = max(counts)
    return PowerLawFit(
        ts=2,
        xmin=xmin,
        gamma=2.0,
        ks=0.1,
        n_total=n,
        n_tail=n,
        tail_fraction=1.0,
        distinct_tail_sizes=len(counts),
        max_size=xmax,
        tail_decades=float(np.log10(xmax / xmin)),
        log_likelihood=-1.0,
    )


class LocalDiscreteModelComparisonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sizes = np.arange(2, 180, dtype=float)
        weights = sizes ** -1.25 * np.exp(-0.055 * sizes)
        frequencies = np.maximum(
            1, np.rint(300_000 * weights / weights.sum())
        ).astype(int)
        cls.counts = Counter(
            {int(size): int(frequency) for size, frequency in zip(sizes, frequencies)}
        )
        cls.fits = fit_models(2, cls.counts, selected_fit(cls.counts, 2))

    def test_every_model_uses_the_identical_observed_tail(self):
        self.assertEqual([fit.model for fit in self.fits], list(MODEL_ORDER))
        self.assertEqual(
            len({(fit.xmin, fit.xmax_observed, fit.n_tail) for fit in self.fits}),
            1,
        )
        self.assertTrue(all(np.isfinite(fit.log_likelihood) for fit in self.fits))
        self.assertTrue(all(np.isfinite(fit.aic) and np.isfinite(fit.bic) for fit in self.fits))

    def test_nested_families_do_not_fit_worse_than_their_nulls(self):
        fitted = {fit.model: fit for fit in self.fits}
        self.assertGreaterEqual(
            fitted["cutoff_power_law"].log_likelihood + 1e-5,
            fitted["power_law"].log_likelihood,
        )
        self.assertGreaterEqual(
            fitted["stretched_exponential"].log_likelihood + 1e-5,
            fitted["exponential"].log_likelihood,
        )
        self.assertEqual(
            fitted["hard_truncated_power_law"].parameters["xmax"],
            max(self.counts),
        )
        self.assertTrue(fitted["hard_truncated_power_law"].nonregular)

    def test_all_ccdfs_begin_at_one_and_are_monotone(self):
        values = np.arange(2, max(self.counts) + 1)
        for fit in self.fits:
            with self.subTest(model=fit.model):
                survival = model_ccdf(fit, values)
                self.assertAlmostEqual(float(survival[0]), 1.0, places=8)
                self.assertTrue(np.all(np.diff(survival) <= 1e-10))
                self.assertTrue(np.all((survival >= -1e-10) & (survival <= 1.0 + 1e-10)))

    def test_boundary_likelihood_ratios_explicitly_defer_bootstrap(self):
        rows = comparison_rows(self.fits, {2: self.counts})
        nested = [row for row in rows if row["comparison"] == "nested_boundary_likelihood_ratio"]
        self.assertEqual(len(nested), 3)
        self.assertTrue(all(row["p_value"] == "" for row in nested))
        self.assertTrue(all(row["calibration"] == "not_run" for row in nested))


if __name__ == "__main__":
    unittest.main()

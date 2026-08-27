"""Checks for the Araujo-style power law with stretched-exponential cutoff."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avalanche_statistics import (  # noqa: E402
    fit_cutoff_power_law,
    fit_generalized_cutoff,
)


def _sample(gamma, s_c, eta, xmin, n, seed, cap=20000):
    grid = np.arange(xmin, cap, dtype=float)
    weight = np.exp(-gamma * np.log(grid) - (grid / s_c) ** eta)
    weight /= weight.sum()
    rng = np.random.default_rng(seed)
    draw = rng.choice(grid.astype(int), size=n, p=weight)
    counts = np.zeros(cap, dtype=np.int64)
    for value in draw:
        counts[value] += 1
    return counts


def test_recovers_its_own_parameters():
    counts = _sample(1.6, 120.0, 1.8, 2, 300000, 5)
    fit = fit_generalized_cutoff(counts, xmin=2)
    assert abs(fit.parameters["gamma"] - 1.6) < 0.06, fit.parameters
    assert abs(fit.parameters["eta"] - 1.8) < 0.25, fit.parameters
    assert abs(fit.parameters["s_c"] / 120.0 - 1.0) < 0.2, fit.parameters


def test_eta_one_matches_the_exponential_cutoff():
    """eta = 1 is fit_cutoff_power_law, so the likelihoods must agree."""
    counts = _sample(1.9, 60.0, 1.0, 2, 200000, 11)
    general = fit_generalized_cutoff(counts, xmin=2)
    exponential = fit_cutoff_power_law(counts, xmin=2)
    assert abs(general.parameters["eta"] - 1.0) < 0.12, general.parameters
    # the larger family cannot fit worse
    assert general.log_likelihood >= exponential.log_likelihood - 1e-3
    assert abs(general.log_likelihood - exponential.log_likelihood) < 5.0


def test_detects_a_sharper_than_exponential_cutoff():
    """Data with eta = 2 must beat the exponential-cutoff fit decisively."""
    counts = _sample(1.5, 80.0, 2.0, 2, 200000, 3)
    general = fit_generalized_cutoff(counts, xmin=2)
    exponential = fit_cutoff_power_law(counts, xmin=2)
    assert general.parameters["eta"] > 1.5, general.parameters
    # one degree of freedom: 2*Delta(loglik) is chi-squared, so >> 10 is decisive
    assert 2 * (general.log_likelihood - exponential.log_likelihood) > 100


def test_ks_is_small_on_its_own_family():
    counts = _sample(1.7, 100.0, 1.5, 3, 150000, 7)
    fit = fit_generalized_cutoff(counts, xmin=3)
    assert fit.ks < 0.01, fit.ks


def test_registered_in_both_dispatchers():
    """A family added only to the fitter is silent until a probability is asked."""
    from avalanche_statistics import distribution_cdf, distribution_log_probabilities
    counts = _sample(1.7, 90.0, 1.9, 2, 80000, 21)
    fit = fit_generalized_cutoff(counts, xmin=2)
    sizes = np.arange(2, 4000)
    total = np.exp(distribution_log_probabilities(fit, sizes)).sum()
    assert abs(total - 1.0) < 1e-6, total
    cdf = distribution_cdf(fit, sizes)
    assert np.all(np.diff(cdf) >= -1e-12)          # non-decreasing
    assert abs(cdf[-1] - 1.0) < 1e-6, cdf[-1]
    # the CDF must be the running sum of the PMF
    assert np.allclose(cdf, np.cumsum(np.exp(distribution_log_probabilities(fit, sizes))),
                       atol=1e-9)

"""Checks for the stretched-exponential fit and the Vuong ratio."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avalanche_statistics import (  # noqa: E402
    distribution_log_probabilities,
    fit_discrete_exponential,
    fit_discrete_power_law,
    fit_stretched_exponential,
    vuong_likelihood_ratio,
)


def _counts_from(sample, width):
    counts = np.zeros(width, dtype=np.int64)
    for value in sample:
        counts[value] += 1
    return counts


def _draw_stretched(beta, rate, xmin, n, seed, width=4000):
    """Inverse-transform sample of the rounded stretched exponential."""
    rng = np.random.default_rng(seed)
    grid = np.arange(xmin, width, dtype=float)
    survival = np.exp(-rate * np.power(grid - 0.5, beta))
    mass = survival - np.exp(-rate * np.power(grid + 0.5, beta))
    mass = mass / mass.sum()
    return rng.choice(grid.astype(int), size=n, p=mass)


def test_pmf_normalises_on_the_tail():
    counts = _counts_from(_draw_stretched(0.6, 0.4, 2, 20000, 1), 4000)
    fit = fit_stretched_exponential(counts, xmin=2)
    sizes = np.arange(2, 3000)
    total = np.exp(distribution_log_probabilities(fit, sizes)).sum()
    assert abs(total - 1.0) < 1e-6, total


def test_recovers_its_own_parameters():
    beta, rate = 0.6, 0.4
    counts = _counts_from(_draw_stretched(beta, rate, 2, 200000, 7), 4000)
    fit = fit_stretched_exponential(counts, xmin=2)
    assert abs(fit.parameters["beta"] - beta) < 0.05, fit.parameters
    assert abs(fit.parameters["lambda"] - rate) < 0.08, fit.parameters


def test_beta_one_matches_the_exponential():
    """beta = 1 is the exponential, so the two fits must agree in likelihood."""
    counts = _counts_from(_draw_stretched(1.0, 0.35, 3, 60000, 11), 4000)
    stretched = fit_stretched_exponential(counts, xmin=3)
    exponential = fit_discrete_exponential(counts, xmin=3)
    assert abs(stretched.parameters["beta"] - 1.0) < 0.06, stretched.parameters
    # the stretched family contains the exponential, so it cannot fit worse
    assert stretched.log_likelihood >= exponential.log_likelihood - 1e-3


def test_vuong_prefers_the_true_family():
    """Data drawn stretched must not favour the power law."""
    counts = _counts_from(_draw_stretched(0.5, 0.5, 2, 100000, 3), 4000)
    power = fit_discrete_power_law(counts, xmin=2)
    stretched = fit_stretched_exponential(counts, xmin=2)
    ratio, normalized, p_value = vuong_likelihood_ratio(power, stretched, counts)
    assert ratio < 0, ratio                    # negative favours the second fit
    assert p_value < 0.01, (normalized, p_value)


def test_vuong_is_antisymmetric():
    counts = _counts_from(_draw_stretched(0.7, 0.3, 2, 40000, 5), 4000)
    power = fit_discrete_power_law(counts, xmin=2)
    stretched = fit_stretched_exponential(counts, xmin=2)
    a = vuong_likelihood_ratio(power, stretched, counts)
    b = vuong_likelihood_ratio(stretched, power, counts)
    assert np.isclose(a[0], -b[0])
    assert np.isclose(a[1], -b[1])
    assert np.isclose(a[2], b[2])

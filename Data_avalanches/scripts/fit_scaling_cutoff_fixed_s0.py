#!/usr/bin/env python3
r"""Fit the finite-scale model with s0 fixed to the largest observed cluster.

For each ``com_terminal`` condition, this script fixes ``s0 = s_max`` and fits
only tau and eta in

    p(s) = C s^(-tau) [tau + eta (s/s0)^eta] exp[-(s/s0)^eta].

The fit is conditioned by default on collective events s >= 2.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp

from avalanche_data import AvalancheDistribution, discover_distributions
from fit_scaling_cutoff import (
    ScalingFit,
    _log_weights,
    plot_fits,
    plot_parameters,
    save_figure,
    write_fits,
)


def fit_distribution_fixed_s0(
    distribution: AvalancheDistribution, *, minimum_size: int = 2
) -> tuple[ScalingFit, np.ndarray, np.ndarray]:
    """Fit tau and eta while setting s0 to the observed maximum size."""
    counts = distribution.infer_counts()
    maximum = int(np.flatnonzero(counts)[-1])
    s0 = float(maximum)
    observed_counts = counts[minimum_size : maximum + 1]
    n_events = int(observed_counts.sum())
    if n_events == 0:
        raise ValueError(f"Ts={distribution.ts}: no events at s >= {minimum_size}")

    normalization_maximum = 4 * maximum
    support = np.arange(minimum_size, normalization_maximum + 1, dtype=float)
    observed_length = maximum - minimum_size + 1

    def objective(parameters: np.ndarray) -> float:
        tau = float(parameters[0])
        eta = float(np.exp(parameters[1]))
        log_weights = _log_weights(support, tau=tau, eta=eta, s0=s0)
        return float(
            logsumexp(log_weights)
            - np.dot(observed_counts, log_weights[:observed_length]) / n_events
        )

    bounds = ((0.01, 10.0), (np.log(0.25), np.log(30.0)))
    starts = [
        np.asarray([tau, np.log(eta)])
        for tau in (0.5, 1.0, 2.0, 3.0, 4.0)
        for eta in (1.0, 2.0, 4.0, 8.0, 12.0, 20.0)
    ]
    attempts = [
        minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 3000, "ftol": 1e-14, "gtol": 1e-9},
        )
        for start in starts
    ]
    successful = [
        attempt for attempt in attempts if attempt.success and np.isfinite(attempt.fun)
    ]
    valid = successful or [attempt for attempt in attempts if np.isfinite(attempt.fun)]
    if not valid:
        raise RuntimeError(f"Ts={distribution.ts}: every optimization failed")
    result = min(valid, key=lambda attempt: attempt.fun)
    tau = float(result.x[0])
    eta = float(np.exp(result.x[1]))

    log_weights = _log_weights(support, tau=tau, eta=eta, s0=s0)
    log_normalization = float(logsumexp(log_weights))
    model_probabilities = np.exp(log_weights - log_normalization)
    empirical_probabilities = observed_counts / n_events
    empirical_cdf = np.cumsum(empirical_probabilities)
    model_cdf = np.cumsum(model_probabilities[:observed_length])
    ks = float(np.max(np.abs(empirical_cdf - model_cdf)))
    tail_probability = float(model_probabilities[observed_length:].sum())
    log_likelihood = float(
        np.dot(
            observed_counts,
            log_weights[:observed_length] - log_normalization,
        )
    )

    fit = ScalingFit(
        ts=distribution.ts,
        minimum_size=minimum_size,
        maximum_observed=maximum,
        normalization_maximum=normalization_maximum,
        n_events=n_events,
        fitted_mass_in_original_pmf=float(
            distribution.probabilities[distribution.sizes >= minimum_size].sum()
        ),
        tau=tau,
        eta=eta,
        s0=s0,
        normalization_c=float(np.exp(-log_normalization)),
        log_likelihood=log_likelihood,
        ks=ks,
        probability_above_observed_maximum=tail_probability,
        converged=bool(result.success),
        optimizer_message=str(result.message),
    )
    return fit, support, model_probabilities


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", type=Path, default=Path(__file__).resolve().parent.parent
    )
    parser.add_argument("--results-dir", type=Path)
    parser.add_argument("--figures-dir", type=Path)
    parser.add_argument("--minimum-size", type=int, default=2)
    parser.add_argument(
        "--formats", nargs="+", choices=("png", "pdf", "svg"), default=("png", "pdf")
    )
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()
    if args.minimum_size < 1:
        parser.error("--minimum-size must be positive")

    results_dir = args.results_dir or args.data_dir / "results"
    figures_dir = args.figures_dir or args.data_dir / "figures"
    distributions = [
        item for item in discover_distributions(args.data_dir) if item.includes_terminal
    ]
    distributions.sort(key=lambda item: item.ts)

    fits: list[ScalingFit] = []
    models: dict[int, tuple[np.ndarray, np.ndarray]] = {}
    for distribution in distributions:
        fit, support, probabilities = fit_distribution_fixed_s0(
            distribution, minimum_size=args.minimum_size
        )
        fits.append(fit)
        models[fit.ts] = (support, probabilities)
        print(
            f"Ts={fit.ts:>4}: s0=s_max={fit.s0:.0f}, tau={fit.tau:.6f}, "
            f"eta={fit.eta:.6f}, KS={fit.ks:.6f}"
        )

    table_path = results_dir / "scaling_cutoff_fixed_s0_parameters.csv"
    write_fits(table_path, fits)
    print(f"Wrote {table_path}")

    fit_figure = plot_fits(distributions, fits, models)
    fit_figure.suptitle(
        r"Finite-scale fits with $s_0=s_{\max}$ and terminal rupture ($s\geq2$)",
        fontsize=14,
    )
    save_figure(
        fit_figure,
        figures_dir / "scaling_cutoff_fixed_s0_fits_loglog",
        formats=list(args.formats),
        dpi=args.dpi,
    )

    parameter_figure = plot_parameters(fits)
    parameter_figure.suptitle(
        r"Constrained finite-scale parameters with $s_0=s_{\max}$", fontsize=14
    )
    save_figure(
        parameter_figure,
        figures_dir / "scaling_cutoff_fixed_s0_parameters_vs_ts",
        formats=list(args.formats),
        dpi=args.dpi,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

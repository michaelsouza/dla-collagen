#!/usr/bin/env python3
r"""Fit the requested finite-scale model to PMFs with terminal rupture.

The discrete model is

    p(s) = C s^(-tau) [tau + eta (s/s0)^eta] exp[-(s/s0)^eta],

conditioned by default on collective events s >= 2. All positive integer sizes,
including unobserved sizes with zero frequency, enter the normalization. Only
input files from the ``com_terminal`` population are fitted.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp

from avalanche_data import AvalancheDistribution, discover_distributions


@dataclass(frozen=True)
class ScalingFit:
    ts: int
    minimum_size: int
    maximum_observed: int
    normalization_maximum: int
    n_events: int
    fitted_mass_in_original_pmf: float
    tau: float
    eta: float
    s0: float
    normalization_c: float
    log_likelihood: float
    ks: float
    probability_above_observed_maximum: float
    converged: bool
    optimizer_message: str


def _log_weights(
    sizes: np.ndarray, *, tau: float, eta: float, s0: float
) -> np.ndarray:
    log_sizes = np.log(sizes)
    log_eta = np.log(eta)
    log_x_eta = eta * (log_sizes - np.log(s0))
    x_eta = np.exp(np.clip(log_x_eta, -745.0, 700.0))
    return (
        -tau * log_sizes
        + np.logaddexp(np.log(tau), log_eta + log_x_eta)
        - x_eta
    )


def fit_distribution(
    distribution: AvalancheDistribution, *, minimum_size: int = 2
) -> tuple[ScalingFit, np.ndarray, np.ndarray]:
    """Fit one condition by discrete multinomial maximum likelihood."""
    counts = distribution.infer_counts()
    maximum = int(np.flatnonzero(counts)[-1])
    observed_counts = counts[minimum_size : maximum + 1]
    n_events = int(observed_counts.sum())
    if n_events == 0:
        raise ValueError(f"Ts={distribution.ts}: no events at s >= {minimum_size}")

    # Four observed maxima are sufficient for the fitted stretched-exponential
    # tails. The residual probability is reported in the output table.
    normalization_maximum = 4 * maximum
    support = np.arange(minimum_size, normalization_maximum + 1, dtype=float)
    observed_length = maximum - minimum_size + 1

    def unpack(parameters: np.ndarray) -> tuple[float, float, float]:
        tau, log_eta, log_s0 = parameters
        return float(tau), float(np.exp(log_eta)), float(np.exp(log_s0))

    def objective(parameters: np.ndarray) -> float:
        tau, eta, s0 = unpack(parameters)
        log_weights = _log_weights(support, tau=tau, eta=eta, s0=s0)
        # Division by N improves numerical scaling without changing the MLE.
        return float(
            logsumexp(log_weights)
            - np.dot(observed_counts, log_weights[:observed_length]) / n_events
        )

    bounds = (
        (0.01, 10.0),
        (np.log(0.25), np.log(30.0)),
        (np.log(float(minimum_size)), np.log(3.0 * maximum)),
    )
    starts = [
        np.asarray(
            [
                tau,
                np.log(eta),
                np.log(max(minimum_size, s0_fraction * maximum)),
            ]
        )
        for tau in (0.5, 1.0, 2.0, 3.0, 4.0)
        for eta in (1.0, 2.0, 4.0, 8.0, 12.0)
        for s0_fraction in (0.3, 0.6, 0.9)
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
    valid = [attempt for attempt in attempts if np.isfinite(attempt.fun)]
    if not valid:
        raise RuntimeError(f"Ts={distribution.ts}: every optimization failed")
    result = min(valid, key=lambda attempt: attempt.fun)
    tau, eta, s0 = unpack(result.x)

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


def write_fits(path: Path, fits: list[ScalingFit]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(ScalingFit.__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(
            {field: getattr(fit, field) for field in fields} for fit in fits
        )


def _style_loglog(axis: plt.Axes) -> None:
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlabel(r"Local avalanche size, $s$")
    axis.set_ylabel(r"Empirical probability, $P(s)$")
    axis.grid(which="major", color="#b8b8b8", linewidth=0.5, alpha=0.45)
    axis.grid(which="minor", color="#d8d8d8", linewidth=0.3, alpha=0.25)


def plot_fits(
    distributions: list[AvalancheDistribution],
    fits: list[ScalingFit],
    models: dict[int, tuple[np.ndarray, np.ndarray]],
) -> plt.Figure:
    by_ts = {item.ts: item for item in distributions}
    figure, axes = plt.subplots(5, 2, figsize=(11, 16.5), constrained_layout=True)
    for axis, fit in zip(axes.flat, fits, strict=True):
        distribution = by_ts[fit.ts]
        selected = distribution.sizes >= fit.minimum_size
        axis.scatter(
            distribution.sizes[selected],
            distribution.probabilities[selected],
            s=9,
            color="#2878a6",
            alpha=0.72,
            linewidths=0.0,
            rasterized=True,
            label="Empirical PMF",
        )
        support, conditional_model = models[fit.ts]
        observed = support <= fit.maximum_observed
        scaled_model = fit.fitted_mass_in_original_pmf * conditional_model
        axis.plot(
            support[observed],
            scaled_model[observed],
            color="#d7301f",
            linewidth=1.45,
            label="Finite-scale fit",
        )
        _style_loglog(axis)
        axis.set_title(
            rf"$T_s={fit.ts}$: $\tau={fit.tau:.3f}$, $s_0={fit.s0:.1f}$, "
            rf"$\eta={fit.eta:.2f}$"
        )
        axis.text(
            0.98,
            0.05,
            rf"$KS={fit.ks:.3f}$",
            transform=axis.transAxes,
            ha="right",
            va="bottom",
            fontsize=8,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.72},
        )
    axes.flat[0].legend(frameon=False, fontsize=8)
    figure.suptitle(
        r"$s^{-\tau}[\tau+\eta(s/s_0)^\eta]e^{-(s/s_0)^\eta}$ "
        r"fitted with terminal rupture ($s\geq2$)",
        fontsize=14,
    )
    return figure


def plot_parameters(fits: list[ScalingFit]) -> plt.Figure:
    ts = np.asarray([fit.ts for fit in fits], dtype=float)
    figure, axes = plt.subplots(1, 3, figsize=(12.0, 3.9), constrained_layout=True)
    panels = (
        (np.asarray([fit.tau for fit in fits]), r"$\tau$"),
        (np.asarray([fit.s0 for fit in fits]), r"$s_0$"),
        (np.asarray([fit.eta for fit in fits]), r"$\eta$"),
    )
    for axis, (values, ylabel) in zip(axes, panels, strict=True):
        axis.plot(ts, values, marker="o", color="#2878a6", linewidth=1.5)
        axis.set_xscale("log", base=2)
        axis.set_xticks(ts)
        axis.set_xticklabels([str(int(value)) for value in ts], rotation=45)
        axis.set_xlabel(r"Surface relaxation, $T_s$")
        axis.set_ylabel(ylabel)
        axis.grid(alpha=0.3)
    figure.suptitle("Parameters of the constrained finite-scale model", fontsize=14)
    return figure


def save_figure(
    figure: plt.Figure, output_base: Path, *, formats: list[str], dpi: int
) -> None:
    output_base.parent.mkdir(parents=True, exist_ok=True)
    for extension in formats:
        path = output_base.with_suffix(f".{extension}")
        figure.savefig(path, dpi=dpi)
        print(f"Wrote {path}")
    plt.close(figure)


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
        fit, support, probabilities = fit_distribution(
            distribution, minimum_size=args.minimum_size
        )
        fits.append(fit)
        models[fit.ts] = (support, probabilities)
        print(
            f"Ts={fit.ts:>4}: tau={fit.tau:.6f}, eta={fit.eta:.6f}, "
            f"s0={fit.s0:.6f}, KS={fit.ks:.6f}"
        )

    table_path = results_dir / "scaling_cutoff_fit_parameters.csv"
    write_fits(table_path, fits)
    print(f"Wrote {table_path}")
    save_figure(
        plot_fits(distributions, fits, models),
        figures_dir / "scaling_cutoff_fits_loglog",
        formats=list(args.formats),
        dpi=args.dpi,
    )
    save_figure(
        plot_parameters(fits),
        figures_dir / "scaling_cutoff_parameters_vs_ts",
        formats=list(args.formats),
        dpi=args.dpi,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

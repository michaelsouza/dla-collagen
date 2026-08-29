#!/usr/bin/env python3
"""Compare discrete models for local avalanche clusters with s >= 2.

The input is the exact frequency table produced by ``local_avalanche_counts``.
Only the ``population=all`` rows are used, so terminal-force clusters remain in
the primary population.  For each Ts, the pure-power-law KS rule chooses xmin;
every candidate is then fitted by maximum likelihood to that identical tail.

This is a relative model-comparison stage.  It deliberately does not perform
the bootstrap absolute goodness-of-fit test or calibrate boundary likelihood-
ratio tests; those computationally heavier steps remain necessary before a
distributional claim can be accepted.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import mpmath
import numpy as np
from scipy import optimize, special, stats

from fit_local_power_law import (
    PowerLawFit,
    fit_gamma,
    model_ccdf as power_law_ccdf,
    read_primary_counts,
    select_xmin,
)


MODEL_ORDER = (
    "power_law",
    "cutoff_power_law",
    "hard_truncated_power_law",
    "lognormal",
    "exponential",
    "stretched_exponential",
)
MODEL_LABELS = {
    "power_law": "Power law",
    "cutoff_power_law": "Power law + exp. cutoff",
    "hard_truncated_power_law": "Power law, hard cutoff",
    "lognormal": "Discrete lognormal",
    "exponential": "Discrete exponential",
    "stretched_exponential": "Stretched exponential",
}
MODEL_COLORS = {
    "power_law": "#d7301f",
    "cutoff_power_law": "#1b9e77",
    "hard_truncated_power_law": "#7570b3",
    "lognormal": "#e6ab02",
    "exponential": "#1f78b4",
    "stretched_exponential": "#e7298a",
}


@dataclass(frozen=True)
class ModelFit:
    ts: int
    model: str
    xmin: int
    xmax_observed: int
    model_support: str
    n_total: int
    n_tail: int
    tail_fraction: float
    parameter_count: int
    parameters: dict[str, float]
    log_likelihood: float
    ks: float
    aic: float
    bic: float
    boundary_solution: bool = False
    nonregular: bool = False
    note: str = ""


def _tail_arrays(counts: Counter[int], xmin: int) -> tuple[np.ndarray, np.ndarray]:
    sizes = np.asarray(sorted(size for size in counts if size >= xmin), dtype=np.int64)
    frequencies = np.asarray([counts[int(size)] for size in sizes], dtype=np.int64)
    if not sizes.size or frequencies.sum() <= 0:
        raise ValueError(f"no observations at or above xmin={xmin}")
    return sizes, frequencies


def _information_criteria(log_likelihood: float, k: int, n: int) -> tuple[float, float]:
    return 2.0 * k - 2.0 * log_likelihood, np.log(float(n)) * k - 2.0 * log_likelihood


def _log_difference(log_larger: np.ndarray, log_smaller: np.ndarray) -> np.ndarray:
    ratio = np.exp(np.minimum(0.0, log_smaller - log_larger))
    return log_larger + np.log1p(-ratio)


def _lognormal_log_mass(sizes: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    values = np.asarray(sizes, dtype=float)
    lower = (np.log(values - 0.5) - mu) / sigma
    upper = (np.log(values + 0.5) - mu) / sigma
    result = np.empty_like(values)
    left = upper <= 0.0
    right = lower >= 0.0
    middle = ~(left | right)
    if np.any(left):
        result[left] = _log_difference(
            special.log_ndtr(upper[left]), special.log_ndtr(lower[left])
        )
    if np.any(right):
        result[right] = _log_difference(
            special.log_ndtr(-lower[right]), special.log_ndtr(-upper[right])
        )
    if np.any(middle):
        result[middle] = np.log(
            special.ndtr(upper[middle]) - special.ndtr(lower[middle])
        )
    return result


def _cutoff_log_normalizer(gamma: float, rate: float, xmin: int) -> float:
    """Exact infinite-support normalization for s^-gamma exp(-rate*s)."""
    if not np.isfinite(gamma) or not np.isfinite(rate) or gamma < 0.0 or rate < 0.0:
        return np.inf
    if rate <= 1e-12:
        if gamma <= 1.0:
            return np.inf
        normalization = special.zeta(gamma, float(xmin))
        if np.isfinite(normalization) and normalization > 0.0:
            return float(np.log(normalization))
        with mpmath.workdps(40):
            return float(mpmath.log(mpmath.zeta(gamma, xmin)))
    span = int(np.ceil(40.0 / rate))
    if span <= 200_000:
        support = np.arange(xmin, xmin + max(64, span) + 1, dtype=float)
        relative = -gamma * np.log(support / xmin) - rate * (support - xmin)
        return float(
            -gamma * np.log(float(xmin))
            - rate * xmin
            + special.logsumexp(relative)
        )
    with mpmath.workdps(40):
        z = mpmath.exp(-rate)
        normalization = z**xmin * mpmath.lerchphi(z, gamma, xmin)
        return float(mpmath.log(normalization))


def model_log_probabilities(fit: ModelFit, sizes: np.ndarray) -> np.ndarray:
    values = np.asarray(sizes, dtype=float)
    result = np.full(values.shape, -np.inf, dtype=float)
    selected = values >= fit.xmin
    if fit.model == "hard_truncated_power_law":
        selected &= values <= fit.parameters["xmax"]
    support = values[selected]
    if fit.model == "power_law":
        gamma = fit.parameters["gamma"]
        result[selected] = (
            -gamma * np.log(support)
            - _cutoff_log_normalizer(gamma, 0.0, fit.xmin)
        )
    elif fit.model == "cutoff_power_law":
        gamma = fit.parameters["gamma"]
        rate = fit.parameters["lambda"]
        result[selected] = (
            -gamma * np.log(support)
            - rate * support
            - _cutoff_log_normalizer(gamma, rate, fit.xmin)
        )
    elif fit.model == "hard_truncated_power_law":
        gamma = fit.parameters["gamma"]
        finite = np.arange(fit.xmin, int(fit.parameters["xmax"]) + 1, dtype=float)
        log_normalizer = special.logsumexp(-gamma * np.log(finite))
        result[selected] = -gamma * np.log(support) - log_normalizer
    elif fit.model == "lognormal":
        mu = fit.parameters["mu"]
        sigma = fit.parameters["sigma"]
        boundary = (np.log(fit.xmin - 0.5) - mu) / sigma
        result[selected] = _lognormal_log_mass(support, mu, sigma) - special.log_ndtr(
            -boundary
        )
    elif fit.model == "exponential":
        rate = fit.parameters["lambda"]
        result[selected] = np.log(-np.expm1(-rate)) - rate * (support - fit.xmin)
    elif fit.model == "stretched_exponential":
        rate = fit.parameters["lambda"]
        beta = fit.parameters["beta"]
        first = -rate * (support**beta - fit.xmin**beta)
        second = -rate * ((support + 1.0) ** beta - fit.xmin**beta)
        result[selected] = _log_difference(first, second)
    else:
        raise ValueError(f"unsupported model {fit.model}")
    return result


def model_ccdf(fit: ModelFit, sizes: np.ndarray) -> np.ndarray:
    values = np.asarray(sizes, dtype=np.int64)
    result = np.ones(values.shape, dtype=float)
    selected = values > fit.xmin
    if fit.model == "power_law":
        return power_law_ccdf(values, fit.xmin, fit.parameters["gamma"])
    if fit.model == "exponential":
        return np.exp(-fit.parameters["lambda"] * (values - fit.xmin))
    if fit.model == "stretched_exponential":
        return np.exp(
            -fit.parameters["lambda"]
            * (values.astype(float) ** fit.parameters["beta"] - fit.xmin ** fit.parameters["beta"])
        )
    if fit.model == "lognormal":
        mu = fit.parameters["mu"]
        sigma = fit.parameters["sigma"]
        boundary = (np.log(fit.xmin - 0.5) - mu) / sigma
        upper = (np.log(values.astype(float) - 0.5) - mu) / sigma
        return np.exp(special.log_ndtr(-upper) - special.log_ndtr(-boundary))
    if fit.model == "hard_truncated_power_law":
        xmax = int(fit.parameters["xmax"])
        support = np.arange(fit.xmin, xmax + 1, dtype=float)
        weights = np.exp(
            -fit.parameters["gamma"] * np.log(support / float(fit.xmin))
        )
        survival = np.cumsum(weights[::-1])[::-1] / weights.sum()
        clipped = np.clip(values, fit.xmin, xmax + 1)
        result = np.zeros(values.shape, dtype=float)
        inside = clipped <= xmax
        result[inside] = survival[clipped[inside] - fit.xmin]
        return result
    if fit.model == "cutoff_power_law":
        maximum = int(values.max())
        support = np.arange(fit.xmin, maximum + 1, dtype=float)
        log_mass = model_log_probabilities(fit, support)
        cumulative = np.cumsum(np.exp(log_mass))
        result[selected] = 1.0 - cumulative[values[selected] - fit.xmin - 1]
        return np.clip(result, 0.0, 1.0)
    raise ValueError(f"unsupported model {fit.model}")


def _ks_distance(fit: ModelFit, sizes: np.ndarray, frequencies: np.ndarray) -> float:
    cumulative = np.cumsum(frequencies) / frequencies.sum()
    before = (np.cumsum(frequencies) - frequencies) / frequencies.sum()
    model_after = 1.0 - model_ccdf(fit, sizes + 1)
    model_before = 1.0 - model_ccdf(fit, sizes)
    return float(max(np.max(np.abs(cumulative - model_after)), np.max(np.abs(before - model_before))))


def _make_fit(
    *,
    ts: int,
    model: str,
    xmin: int,
    counts: Counter[int],
    parameters: dict[str, float],
    log_likelihood: float,
    parameter_count: int,
    model_support: str = "infinite integers [xmin, infinity)",
    boundary_solution: bool = False,
    nonregular: bool = False,
    note: str = "",
) -> ModelFit:
    sizes, frequencies = _tail_arrays(counts, xmin)
    n_total = int(sum(counts.values()))
    n_tail = int(frequencies.sum())
    aic, bic = _information_criteria(log_likelihood, parameter_count, n_tail)
    provisional = ModelFit(
        ts=ts,
        model=model,
        xmin=xmin,
        xmax_observed=int(sizes[-1]),
        model_support=model_support,
        n_total=n_total,
        n_tail=n_tail,
        tail_fraction=n_tail / n_total,
        parameter_count=parameter_count,
        parameters=parameters,
        log_likelihood=log_likelihood,
        ks=float("nan"),
        aic=aic,
        bic=bic,
        boundary_solution=boundary_solution,
        nonregular=nonregular,
        note=note,
    )
    return ModelFit(**{**provisional.__dict__, "ks": _ks_distance(provisional, sizes, frequencies)})


def fit_models(ts: int, counts: Counter[int], selected: PowerLawFit) -> list[ModelFit]:
    xmin = selected.xmin
    sizes, frequencies = _tail_arrays(counts, xmin)
    n = int(frequencies.sum())
    sum_log = float(np.dot(frequencies, np.log(sizes.astype(float))))
    sum_size = float(np.dot(frequencies, sizes.astype(float)))
    fits: list[ModelFit] = []

    gamma, power_ll = fit_gamma(sizes, frequencies, xmin)
    fits.append(
        _make_fit(
            ts=ts,
            model="power_law",
            xmin=xmin,
            counts=counts,
            parameters={"gamma": gamma},
            log_likelihood=power_ll,
            parameter_count=1,
        )
    )

    def cutoff_nll(parameters: np.ndarray) -> float:
        cutoff_gamma = float(np.exp(parameters[0]))
        rate = float(np.exp(parameters[1]))
        log_z = _cutoff_log_normalizer(cutoff_gamma, rate, xmin)
        value = n * log_z + cutoff_gamma * sum_log + rate * sum_size
        return value if np.isfinite(value) else 1e300

    cutoff_results = [
        optimize.minimize(
            cutoff_nll,
            np.asarray(start),
            method="L-BFGS-B",
            bounds=((np.log(1e-8), np.log(1e6)), (np.log(1e-12), np.log(10.0))),
            options={"ftol": 1e-12, "gtol": 1e-8, "maxiter": 1000},
        )
        for start in (
            (np.log(max(0.05, gamma - 0.5)), np.log(1e-3)),
            (np.log(max(0.05, gamma - 1.0)), np.log(1e-2)),
            (np.log(gamma), np.log(1e-5)),
        )
    ]
    cutoff_valid = [item for item in cutoff_results if item.success and np.isfinite(item.fun)]
    cutoff_result = min(cutoff_valid, key=lambda item: item.fun) if cutoff_valid else None
    if cutoff_result is None or -float(cutoff_result.fun) <= power_ll + 1e-7:
        cutoff_gamma, cutoff_rate, cutoff_ll, cutoff_boundary = gamma, 0.0, power_ll, True
    else:
        cutoff_gamma = float(np.exp(cutoff_result.x[0]))
        cutoff_rate = float(np.exp(cutoff_result.x[1]))
        cutoff_ll = -float(cutoff_result.fun)
        cutoff_boundary = cutoff_rate <= 1.01e-12 or cutoff_gamma <= 1.01e-8
    fits.append(
        _make_fit(
            ts=ts,
            model="cutoff_power_law",
            xmin=xmin,
            counts=counts,
            parameters={"gamma": cutoff_gamma, "lambda": cutoff_rate},
            log_likelihood=cutoff_ll,
            parameter_count=2,
            boundary_solution=cutoff_boundary,
            nonregular=cutoff_boundary,
            note=(
                "lambda=0 is the pure-power-law boundary and gamma=0 reduces to "
                "the exponential family; boundary LR p-values require bootstrap"
            ),
        )
    )

    xmax = int(sizes[-1])
    finite_support = np.arange(xmin, xmax + 1, dtype=float)

    def hard_nll(hard_gamma: float) -> float:
        return n * special.logsumexp(-hard_gamma * np.log(finite_support)) + hard_gamma * sum_log

    hard_upper = max(4.0, gamma)
    while hard_nll(hard_upper * 2.0) < hard_nll(hard_upper):
        hard_upper *= 2.0
    hard_result = optimize.minimize_scalar(
        hard_nll, bounds=(0.0, hard_upper * 2.0), method="bounded"
    )
    hard_gamma = float(hard_result.x)
    fits.append(
        _make_fit(
            ts=ts,
            model="hard_truncated_power_law",
            xmin=xmin,
            counts=counts,
            parameters={"gamma": hard_gamma, "xmax": float(xmax)},
            log_likelihood=-float(hard_result.fun),
            parameter_count=2,
            model_support=f"finite integers [xmin, {xmax}]",
            nonregular=True,
            note=(
                "xmax is the observed maximum because no physical upper support is in the "
                "aggregate table; AIC/BIC and LR are sensitivity diagnostics, not regular inference"
            ),
        )
    )

    log_sizes = np.log(sizes.astype(float))
    initial_mu = float(np.dot(frequencies, log_sizes) / n)
    initial_sigma = max(
        float(np.sqrt(np.dot(frequencies, (log_sizes - initial_mu) ** 2) / n)), 0.1
    )

    def lognormal_nll(parameters: np.ndarray) -> float:
        mu = float(parameters[0])
        sigma = float(np.exp(parameters[1]))
        boundary = (np.log(xmin - 0.5) - mu) / sigma
        log_mass = _lognormal_log_mass(sizes, mu, sigma)
        value = -float(np.dot(frequencies, log_mass - special.log_ndtr(-boundary)))
        return value if np.isfinite(value) else np.inf

    lognormal_results = [
        optimize.minimize(
            lognormal_nll,
            np.asarray(start),
            method="L-BFGS-B",
            bounds=((-100.0, 50.0), (np.log(0.005), np.log(100.0))),
            options={"ftol": 1e-12, "gtol": 1e-8, "maxiter": 1000},
        )
        for start in (
            (initial_mu, np.log(initial_sigma)),
            (np.log(xmin), np.log(0.25)),
            (np.log(xmin), 0.0),
            (-20.0, np.log(5.0)),
        )
    ]
    lognormal_valid = [item for item in lognormal_results if item.success and np.isfinite(item.fun)]
    if not lognormal_valid:
        raise RuntimeError(f"Ts={ts}: all lognormal optimizations failed")
    lognormal_result = min(lognormal_valid, key=lambda item: item.fun)
    mu = float(lognormal_result.x[0])
    sigma = float(np.exp(lognormal_result.x[1]))
    lognormal_boundary = abs(mu + 100.0) < 1e-5 or sigma > 99.9
    fits.append(
        _make_fit(
            ts=ts,
            model="lognormal",
            xmin=xmin,
            counts=counts,
            parameters={"mu": mu, "sigma": sigma},
            log_likelihood=-float(lognormal_result.fun),
            parameter_count=2,
            boundary_solution=lognormal_boundary,
            note="rounded continuous lognormal, conditioned on integer s >= xmin",
        )
    )

    excess = float(np.dot(frequencies, sizes - xmin))
    q = excess / (n + excess)
    exponential_rate = -float(np.log(q))
    exponential_ll = float(n * np.log1p(-q) + excess * np.log(q))
    fits.append(
        _make_fit(
            ts=ts,
            model="exponential",
            xmin=xmin,
            counts=counts,
            parameters={"lambda": exponential_rate},
            log_likelihood=exponential_ll,
            parameter_count=1,
            note="exact shifted geometric distribution",
        )
    )

    def stretched_nll(parameters: np.ndarray) -> float:
        rate = float(np.exp(parameters[0]))
        beta = float(parameters[1])
        first = -rate * (sizes.astype(float) ** beta - xmin**beta)
        second = -rate * ((sizes.astype(float) + 1.0) ** beta - xmin**beta)
        log_mass = _log_difference(first, second)
        value = -float(np.dot(frequencies, log_mass))
        return value if np.isfinite(value) else np.inf

    stretched_results = [
        optimize.minimize(
            stretched_nll,
            np.asarray(start),
            method="L-BFGS-B",
            bounds=((np.log(1e-12), np.log(1e6)), (1e-4, 1.0)),
            options={"ftol": 1e-12, "gtol": 1e-8, "maxiter": 1000},
        )
        for start in (
            (np.log(exponential_rate), 1.0),
            (np.log(exponential_rate), 0.7),
            (0.0, 0.3),
        )
    ]
    stretched_valid = [item for item in stretched_results if item.success and np.isfinite(item.fun)]
    if not stretched_valid:
        raise RuntimeError(f"Ts={ts}: all stretched-exponential optimizations failed")
    stretched_result = min(stretched_valid, key=lambda item: item.fun)
    stretched_rate = float(np.exp(stretched_result.x[0]))
    beta = float(stretched_result.x[1])
    stretched_boundary = beta >= 1.0 - 1e-7 or beta <= 1.01e-4
    fits.append(
        _make_fit(
            ts=ts,
            model="stretched_exponential",
            xmin=xmin,
            counts=counts,
            parameters={"lambda": stretched_rate, "beta": beta},
            log_likelihood=-float(stretched_result.fun),
            parameter_count=2,
            boundary_solution=stretched_boundary,
            nonregular=stretched_boundary,
            note=(
                "survival-discretized Weibull with 0 < beta <= 1; beta=1 is "
                "exponential and beta near 0 is a numerical-boundary solution"
            ),
        )
    )
    if [fit.model for fit in fits] != list(MODEL_ORDER):
        raise RuntimeError("internal model ordering error")
    if len({(fit.xmin, fit.n_tail, fit.xmax_observed) for fit in fits}) != 1:
        raise RuntimeError("models were not fitted to a common observed tail")
    return fits


def comparison_rows(fits: list[ModelFit], counts_by_ts: dict[int, Counter[int]]) -> list[dict]:
    rows: list[dict] = []
    for ts in sorted(counts_by_ts):
        selected = {fit.model: fit for fit in fits if fit.ts == ts}
        nested = (
            ("power_law", "cutoff_power_law", "lambda=0 boundary; parametric-bootstrap LR p-value not run"),
            ("power_law", "hard_truncated_power_law", "xmax=infinity boundary and data-selected xmax; nonregular, bootstrap not run"),
            ("exponential", "stretched_exponential", "beta=1 boundary; parametric-bootstrap LR p-value not run"),
        )
        for null, alternative, note in nested:
            lr = 2.0 * max(0.0, selected[alternative].log_likelihood - selected[null].log_likelihood)
            rows.append(
                {
                    "ts": ts,
                    "model_1": null,
                    "model_2": alternative,
                    "comparison": "nested_boundary_likelihood_ratio",
                    "log_likelihood_ratio_model1_minus_model2": selected[null].log_likelihood - selected[alternative].log_likelihood,
                    "statistic": lr,
                    "p_value": "",
                    "calibration": "not_run",
                    "preferred_by_sign": alternative if lr > 0.0 else "tie",
                    "note": note,
                }
            )
        sizes, frequencies = _tail_arrays(counts_by_ts[ts], selected["power_law"].xmin)
        power_logp = model_log_probabilities(selected["power_law"], sizes)
        for alternative in ("lognormal", "exponential", "stretched_exponential"):
            differences = power_logp - model_log_probabilities(selected[alternative], sizes)
            n = float(frequencies.sum())
            mean = float(np.dot(frequencies, differences) / n)
            variance = float(np.dot(frequencies, (differences - mean) ** 2) / n)
            z = float(np.sqrt(n) * mean / np.sqrt(variance)) if variance > 0.0 else float("nan")
            p_value = float(2.0 * stats.norm.sf(abs(z))) if np.isfinite(z) else float("nan")
            rows.append(
                {
                    "ts": ts,
                    "model_1": "power_law",
                    "model_2": alternative,
                    "comparison": "vuong_iid_event_level_exploratory",
                    "log_likelihood_ratio_model1_minus_model2": float(np.dot(frequencies, differences)),
                    "statistic": z,
                    "p_value": p_value,
                    "calibration": "asymptotic_normal_iid_events",
                    "preferred_by_sign": "power_law" if z > 0.0 else alternative,
                    "note": "nominal only: aggregate frequency table cannot preserve fibril/run dependence",
                }
            )
    return rows


def write_fit_csv(path: Path, fits: list[ModelFit]) -> None:
    parameter_names = ("gamma", "lambda", "beta", "mu", "sigma", "xmax")
    rows = []
    for fit in fits:
        row = {field: getattr(fit, field) for field in ModelFit.__dataclass_fields__ if field != "parameters"}
        row["parameters_json"] = json.dumps(fit.parameters, sort_keys=True)
        row.update({name: fit.parameters.get(name, "") for name in parameter_names})
        rows.append(row)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_ccdf_diagnostics(
    counts_by_ts: dict[int, Counter[int]], fits: list[ModelFit], output_dir: Path
) -> None:
    fig, axes = plt.subplots(5, 2, figsize=(11, 18), constrained_layout=True)
    for axis, ts in zip(axes.flat, sorted(counts_by_ts)):
        condition_fits = [fit for fit in fits if fit.ts == ts]
        xmin = condition_fits[0].xmin
        sizes, frequencies = _tail_arrays(counts_by_ts[ts], xmin)
        empirical = np.cumsum(frequencies[::-1])[::-1] / frequencies.sum()
        axis.step(sizes, empirical, where="post", color="#333333", linewidth=1.4, label="Empirical tail")
        for fit in condition_fits:
            axis.plot(
                sizes,
                model_ccdf(fit, sizes),
                color=MODEL_COLORS[fit.model],
                linewidth=1.1,
                label=MODEL_LABELS[fit.model],
            )
        best = min(
            (fit for fit in condition_fits if fit.model != "hard_truncated_power_law"),
            key=lambda fit: fit.bic,
        )
        axis.set(xscale="log", yscale="log")
        axis.set_title(
            rf"$T_s={ts}$, $s_{{min}}={xmin}$; best regular BIC: {MODEL_LABELS[best.model]}"
        )
        axis.set_xlabel(r"Local avalanche size, $s$")
        axis.set_ylabel(r"$P(S\geq s\mid S\geq s_{min})$")
        axis.grid(which="both", alpha=0.2)
        axis.legend(frameon=False, fontsize=6.8, ncol=2)
    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"local_discrete_model_ccdf_diagnostics.{suffix}", dpi=300)
    plt.close(fig)


def plot_information_criteria(fits: list[ModelFit], output_dir: Path) -> None:
    ts_values = sorted({fit.ts for fit in fits})
    matrix = np.zeros((len(MODEL_ORDER), len(ts_values)))
    for column, ts in enumerate(ts_values):
        condition = {fit.model: fit for fit in fits if fit.ts == ts}
        minimum = min(fit.bic for fit in condition.values())
        matrix[:, column] = [condition[model].bic - minimum for model in MODEL_ORDER]
    display = np.log10(1.0 + matrix)
    fig, axis = plt.subplots(figsize=(10, 4.8), constrained_layout=True)
    image = axis.imshow(display, aspect="auto", cmap="viridis", interpolation="nearest")
    axis.set_xticks(range(len(ts_values)), [str(ts) for ts in ts_values])
    axis.set_yticks(range(len(MODEL_ORDER)), [MODEL_LABELS[model] for model in MODEL_ORDER])
    axis.set_xlabel(r"$T_s$")
    axis.set_title(
        r"Relative BIC on the common fitted tail: $\log_{10}(1+\Delta BIC)$ "
        "(hard cutoff is nonregular)"
    )
    fig.colorbar(image, ax=axis, label=r"$\log_{10}(1+\Delta BIC)$")
    for row in range(len(MODEL_ORDER)):
        for column in range(len(ts_values)):
            label = "0" if matrix[row, column] < 0.05 else f"{matrix[row, column]:.0f}"
            axis.text(column, row, label, ha="center", va="center", color="white" if display[row, column] > display.max() / 2 else "black", fontsize=7)
    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"local_discrete_model_bic_summary.{suffix}", dpi=300)
    plt.close(fig)


def write_notes(path: Path, fits: list[ModelFit]) -> None:
    lines = [
        "# Local-avalanche discrete model comparison (pre-bootstrap)",
        "",
        "Primary population: all connected local clusters with $s\\ge2$, including the terminal force step.",
        "For each $T_s$, $s_{min}$ is selected once by the exact discrete pure-power-law KS rule; all candidate models use exactly the same observations $s\\ge s_{min}$.",
        "AIC/BIC are relative criteria, not absolute goodness-of-fit tests. Bootstrap GOF and boundary-LR calibration were intentionally not run at this stage.",
        "",
        "The hard-truncated power law is only a sensitivity model: its upper endpoint is the observed maximum because the aggregate frequency table contains no fibril-specific physical support. Its AIC/BIC and LR are nonregular diagnostics.",
        "",
        "## Preliminary relative result",
        "",
        "- Among the regular infinite-support candidates, the exponential-cutoff power law has the lowest BIC for $T_s=2$ and 8.",
        "- The discrete lognormal has the lowest BIC for every $T_s\\ge16$; at $T_s=64$ its BIC advantage over the exponential is only 0.522 and is not a meaningful separation by the usual criterion.",
        "- The pure power law is not the lowest-BIC regular model in any condition.",
        "- For $T_s\\ge16$, the power-law-selected tail contains only 0.031--0.245% of the primary events and spans at most 0.160 decades. Model rankings there concern a narrow terminal-scale tail, not the complete $s\\ge2$ distribution.",
        "- The stretched exponential reaches the exponential boundary ($\\beta=1$) for every $T_s\\ge16$; the boundary LR still requires bootstrap calibration.",
        "",
        "## BIC ranking by condition",
        "",
        "| Ts | xmin | tail n | tail (%) | decades | best regular BIC | second regular BIC | delta BIC | hard-cutoff delta BIC* |",
        "|---:|---:|---:|---:|---:|:---|:---|---:|---:|",
    ]
    for ts in sorted({fit.ts for fit in fits}):
        condition = [fit for fit in fits if fit.ts == ts]
        ranked = sorted(
            (fit for fit in condition if fit.model != "hard_truncated_power_law"),
            key=lambda fit: fit.bic,
        )
        hard = next(fit for fit in condition if fit.model == "hard_truncated_power_law")
        lines.append(
            f"| {ts} | {ranked[0].xmin} | {ranked[0].n_tail} | "
            f"{100.0 * ranked[0].tail_fraction:.3f} | "
            f"{np.log10(ranked[0].xmax_observed / ranked[0].xmin):.3f} | "
            f"{MODEL_LABELS[ranked[0].model]} | "
            f"{MODEL_LABELS[ranked[1].model]} | {ranked[1].bic - ranked[0].bic:.3f} | "
            f"{hard.bic - ranked[0].bic:.3f} |"
        )
    lines.extend(
        [
            "",
            "*The hard-cutoff delta is shown only as a nonregular sensitivity diagnostic.",
            "",
            "## Interpretation guardrails",
            "",
            "- A model winning AIC/BIC can still be rejected by absolute goodness-of-fit.",
            "- The pure-law versus exponential-cutoff LR has a boundary at $\\lambda=0$; its p-value must be calibrated by parametric bootstrap.",
            "- Event-level Vuong p-values in the comparison CSV are exploratory because aggregation removes fibril/run blocks.",
            "- No SOC, scale-free, universality, or load-sharing conclusion follows from this relative comparison.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frequency_csv", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--min-tail", type=int, default=1_000)
    parser.add_argument("--min-distinct", type=int, default=10)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    counts_by_ts = read_primary_counts(args.frequency_csv)
    fits: list[ModelFit] = []
    for ts in sorted(counts_by_ts):
        selected = select_xmin(
            ts,
            counts_by_ts[ts],
            min_tail=args.min_tail,
            min_distinct=args.min_distinct,
        )
        condition_fits = fit_models(ts, counts_by_ts[ts], selected)
        fits.extend(condition_fits)
        winner = min(
            (fit for fit in condition_fits if fit.model != "hard_truncated_power_law"),
            key=lambda fit: fit.bic,
        )
        print(
            f"Ts={ts:>4}: xmin={selected.xmin}, n_tail={selected.n_tail}, "
            f"best_regular_BIC={winner.model}, KS={winner.ks:.5f}"
        )

    write_fit_csv(args.output_dir / "local_discrete_model_fits.csv", fits)
    write_csv(
        args.output_dir / "local_discrete_model_comparisons.csv",
        comparison_rows(fits, counts_by_ts),
    )
    plot_ccdf_diagnostics(counts_by_ts, fits, args.output_dir)
    plot_information_criteria(fits, args.output_dir)
    write_notes(args.output_dir / "local_discrete_model_comparison_notes.md", fits)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

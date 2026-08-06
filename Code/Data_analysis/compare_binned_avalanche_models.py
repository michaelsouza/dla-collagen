#!/usr/bin/env python3
"""Test candidate models against logarithmically binned avalanche densities.

The candidates follow the focused suggestion in the referee discussion:

* a pure discrete power law;
* a discrete power law with an exponential cutoff;
* a discrete lognormal.

All models are integrated over the same logarithmic bins and conditioned on
the complete observed support s >= 2.  Parameters are estimated internally as
nuisance quantities, but this script reports only goodness-of-fit and model
comparison statistics.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import optimize, stats

from Code.Data_analysis.run_avalanche_statistics import load_or_build_cache
from Code.Data_analysis.test_binned_avalanche_density import (
    BIN_COUNT,
    MINIMUM_SIZE,
    GroupedSupport,
    logarithmic_grouping,
    multinomial_deviance,
)


TS_VALUES = (2, 8, 32)
MODELS = ("power_law", "power_law_cutoff", "lognormal")
BOOTSTRAP_REPLICATES = 2_500
REJECTION_THRESHOLD = 0.1
RANDOM_SEED = 20260801


@dataclass(frozen=True)
class GroupedFit:
    model: str
    parameters: tuple[float, ...]
    probabilities: np.ndarray
    log_likelihood: float


def _group_probabilities(
    grouping: GroupedSupport, log_size_weights: np.ndarray
) -> np.ndarray:
    shifted = log_size_weights - float(np.max(log_size_weights))
    size_weights = np.exp(shifted)
    bin_weights = np.bincount(
        grouping.size_to_bin,
        weights=size_weights,
        minlength=grouping.observed.size,
    )
    probabilities = bin_weights / bin_weights.sum()
    probabilities = np.maximum(probabilities, np.finfo(np.float64).tiny)
    return probabilities / probabilities.sum()


def _negative_grouped_log_likelihood(
    observed: np.ndarray, probabilities: np.ndarray
) -> float:
    nonzero = observed > 0
    return -float(
        np.dot(observed[nonzero], np.log(probabilities[nonzero]))
    )


def _fit_from_objective(
    model: str,
    observed: np.ndarray,
    objective,
    starts: tuple[np.ndarray, ...],
    bounds: tuple[tuple[float, float], ...],
) -> GroupedFit:
    best = None
    for start in starts:
        result = optimize.minimize(
            lambda parameters: objective(parameters)[0],
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"ftol": 1e-12, "gtol": 1e-8, "maxiter": 500},
        )
        if np.isfinite(result.fun) and (best is None or result.fun < best.fun):
            best = result
    if best is None:
        raise RuntimeError(f"{model} grouped fit failed for every starting point")
    negative_log_likelihood, probabilities = objective(best.x)
    return GroupedFit(
        model=model,
        parameters=tuple(float(value) for value in best.x),
        probabilities=probabilities,
        log_likelihood=-float(negative_log_likelihood),
    )


def fit_model(
    grouping: GroupedSupport, observed: np.ndarray, model: str
) -> GroupedFit:
    """Fit one candidate distribution to grouped counts."""

    log_sizes = grouping.log_sizes
    sizes = np.exp(log_sizes)

    if model == "power_law":
        def objective(parameters: np.ndarray) -> tuple[float, np.ndarray]:
            probabilities = _group_probabilities(
                grouping, -float(parameters[0]) * log_sizes
            )
            return _negative_grouped_log_likelihood(observed, probabilities), probabilities

        return _fit_from_objective(
            model,
            observed,
            objective,
            starts=(np.asarray([2.0]),),
            bounds=((0.01, 10.0),),
        )

    if model == "power_law_cutoff":
        pure_fit = fit_model(grouping, observed, "power_law")
        pure_exponent = pure_fit.parameters[0]

        def objective(parameters: np.ndarray) -> tuple[float, np.ndarray]:
            exponent, cutoff = (float(value) for value in parameters)
            probabilities = _group_probabilities(
                grouping, -exponent * log_sizes - cutoff * sizes
            )
            return _negative_grouped_log_likelihood(observed, probabilities), probabilities

        maximum = float(sizes[-1])
        return _fit_from_objective(
            model,
            observed,
            objective,
            starts=(
                np.asarray([pure_exponent, 0.0]),
                np.asarray([pure_exponent, 1.0 / maximum]),
                np.asarray([max(0.1, pure_exponent - 0.5), 5.0 / maximum]),
            ),
            bounds=((0.01, 10.0), (0.0, 5.0)),
        )

    if model == "lognormal":
        centers = np.sqrt(grouping.left_edges * grouping.right_edges)
        total = float(observed.sum())
        initial_mu = float(np.dot(observed, np.log(centers)) / total)
        initial_variance = float(
            np.dot(observed, (np.log(centers) - initial_mu) ** 2) / total
        )
        initial_log_sigma = float(np.log(max(np.sqrt(initial_variance), 0.1)))

        def objective(parameters: np.ndarray) -> tuple[float, np.ndarray]:
            mu, log_sigma = (float(value) for value in parameters)
            sigma = np.exp(log_sigma)
            log_weights = -log_sizes - 0.5 * ((log_sizes - mu) / sigma) ** 2
            probabilities = _group_probabilities(grouping, log_weights)
            return _negative_grouped_log_likelihood(observed, probabilities), probabilities

        minimum_log = float(log_sizes[0])
        maximum_log = float(log_sizes[-1])
        return _fit_from_objective(
            model,
            observed,
            objective,
            starts=(
                np.asarray([initial_mu, initial_log_sigma]),
                np.asarray([(minimum_log + maximum_log) / 2.0, 0.0]),
                np.asarray([minimum_log, 0.5]),
            ),
            bounds=(
                (minimum_log - 5.0, maximum_log + 5.0),
                (np.log(0.03), np.log(20.0)),
            ),
        )

    raise ValueError(f"unknown model: {model}")


def model_goodness_of_fit(
    grouping: GroupedSupport,
    observed_fit: GroupedFit,
    *,
    replicates: int,
    rng: np.random.Generator,
) -> dict[str, float | int | str]:
    """Parametric-bootstrap deviance test for one grouped model."""

    observed = grouping.observed.astype(np.int64)
    observed_deviance = multinomial_deviance(
        observed, observed_fit.probabilities
    )
    event_count = int(observed.sum())
    exceedances = 0
    for _ in range(replicates):
        synthetic = rng.multinomial(event_count, observed_fit.probabilities)
        synthetic_fit = fit_model(grouping, synthetic, observed_fit.model)
        synthetic_deviance = multinomial_deviance(
            synthetic, synthetic_fit.probabilities
        )
        exceedances += synthetic_deviance >= observed_deviance
    p_value = (exceedances + 1.0) / (replicates + 1.0)
    return {
        "deviance": observed_deviance,
        "bootstrap_replicates": replicates,
        "exceedances": exceedances,
        "p_value": p_value,
        "decision_at_0.1": (
            "rejected" if p_value <= REJECTION_THRESHOLD else "not_rejected"
        ),
    }


def nested_cutoff_test(
    grouping: GroupedSupport,
    pure_fit: GroupedFit,
    cutoff_fit: GroupedFit,
    *,
    replicates: int,
    rng: np.random.Generator,
) -> dict[str, float | int | str]:
    """Bootstrap the nested pure-power-law versus cutoff likelihood ratio."""

    observed_lr = 2.0 * max(
        0.0, cutoff_fit.log_likelihood - pure_fit.log_likelihood
    )
    event_count = int(grouping.observed.sum())
    exceedances = 0
    for _ in range(replicates):
        synthetic = rng.multinomial(event_count, pure_fit.probabilities)
        synthetic_pure = fit_model(grouping, synthetic, "power_law")
        synthetic_cutoff = fit_model(grouping, synthetic, "power_law_cutoff")
        synthetic_lr = 2.0 * max(
            0.0,
            synthetic_cutoff.log_likelihood - synthetic_pure.log_likelihood,
        )
        exceedances += synthetic_lr >= observed_lr
    p_value = (exceedances + 1.0) / (replicates + 1.0)
    return {
        "comparison": "power_law_vs_power_law_cutoff",
        "test": "parametric_bootstrap_likelihood_ratio",
        "statistic": observed_lr,
        "p_value": p_value,
        "bootstrap_replicates": replicates,
        "exceedances": exceedances,
        "result": (
            "power_law_cutoff_favored"
            if p_value <= REJECTION_THRESHOLD
            else "inconclusive"
        ),
    }


def vuong_lognormal_test(
    grouping: GroupedSupport,
    pure_fit: GroupedFit,
    lognormal_fit: GroupedFit,
) -> dict[str, float | int | str]:
    """Compare the two nonnested grouped models using Vuong's statistic."""

    observed = grouping.observed
    differences = np.log(pure_fit.probabilities) - np.log(
        lognormal_fit.probabilities
    )
    event_count = float(observed.sum())
    mean_difference = float(np.dot(observed, differences) / event_count)
    variance = float(
        np.dot(observed, (differences - mean_difference) ** 2) / event_count
    )
    normalized = np.sqrt(event_count) * mean_difference / np.sqrt(variance)
    p_value = float(2.0 * stats.norm.sf(abs(normalized)))
    if p_value > REJECTION_THRESHOLD:
        result = "inconclusive"
    elif normalized > 0:
        result = "power_law_favored"
    else:
        result = "lognormal_favored"
    return {
        "comparison": "power_law_vs_lognormal",
        "test": "vuong_grouped_likelihood_ratio",
        "statistic": float(normalized),
        "p_value": p_value,
        "bootstrap_replicates": 0,
        "exceedances": "",
        "result": result,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    data_root = repo / "Data_fibrils" / "Avalanche_force_grouped" / "runs"
    cache_root = repo / "Data_fibrils" / "Avalanche_force_grouped" / "analysis_cache"
    output = repo / "Reviews" / "Issue5_avalanche_statistics"
    output.mkdir(parents=True, exist_ok=True)

    seed_sequence = np.random.SeedSequence(RANDOM_SEED)
    random_streams = iter(seed_sequence.spawn(len(TS_VALUES) * 2 * 4))
    goodness_rows: list[dict] = []
    comparison_rows: list[dict] = []

    for ts in TS_VALUES:
        condition = load_or_build_cache(data_root, cache_root, ts)
        for include_terminal in (False, True):
            terminal = "included" if include_terminal else "excluded"
            counts = condition.fibril_counts(
                include_terminal=include_terminal
            ).sum(axis=0)
            grouping = logarithmic_grouping(counts)
            fits = {
                model: fit_model(grouping, grouping.observed, model)
                for model in MODELS
            }
            for model in MODELS:
                rng = np.random.default_rng(next(random_streams))
                result = model_goodness_of_fit(
                    grouping,
                    fits[model],
                    replicates=BOOTSTRAP_REPLICATES,
                    rng=rng,
                )
                goodness_rows.append(
                    {
                        "ts": ts,
                        "terminal_rupture": terminal,
                        "model": model,
                        "events": int(grouping.observed.sum()),
                        "minimum_size": MINIMUM_SIZE,
                        "maximum_size": int(round(grouping.right_edges[-1] - 1.0)),
                        "requested_bins": BIN_COUNT,
                        "represented_bins": int(grouping.observed.size),
                        **result,
                    }
                )
                print(
                    f"Ts={ts}, terminal={terminal}, model={model}: "
                    f"p={result['p_value']:.6g}, {result['decision_at_0.1']}",
                    flush=True,
                )

            comparison_rows.append(
                {
                    "ts": ts,
                    "terminal_rupture": terminal,
                    **nested_cutoff_test(
                        grouping,
                        fits["power_law"],
                        fits["power_law_cutoff"],
                        replicates=BOOTSTRAP_REPLICATES,
                        rng=np.random.default_rng(next(random_streams)),
                    ),
                }
            )
            comparison_rows.append(
                {
                    "ts": ts,
                    "terminal_rupture": terminal,
                    **vuong_lognormal_test(
                        grouping,
                        fits["power_law"],
                        fits["lognormal"],
                    ),
                }
            )
            print(
                f"Ts={ts}, terminal={terminal}: comparisons complete",
                flush=True,
            )

    write_csv(output / "binned_density_model_gof.csv", goodness_rows)
    write_csv(output / "binned_density_model_comparisons.csv", comparison_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

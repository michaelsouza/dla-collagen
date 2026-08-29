#!/usr/bin/env python3
"""Goodness-of-fit tests for logarithmically binned avalanche densities.

The test uses all collective events (s >= 2), with 100 logarithmic bins.  A
truncated discrete power law is integrated over each bin, and a multinomial
deviance compares the resulting binned density with the observed density.  The
p-value is calibrated by a parametric bootstrap in which the nuisance exponent
is re-estimated for every synthetic binned sample.

The analysis is repeated for precursor clusters alone and after adding the
clusters recorded on the terminal rupture row.  The fitted exponent is an
internal nuisance parameter and is deliberately not reported by this script.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import optimize

from Code.Data_analysis.run_avalanche_statistics import load_or_build_cache


TS_VALUES = (2, 8, 32)
BIN_COUNT = 100
MINIMUM_SIZE = 2
BOOTSTRAP_REPLICATES = 2_500
REJECTION_THRESHOLD = 0.1
RANDOM_SEED = 20260731


@dataclass(frozen=True)
class GroupedSupport:
    """Observed bin counts and the integer sizes assigned to each bin."""

    observed: np.ndarray
    size_to_bin: np.ndarray
    log_sizes: np.ndarray
    left_edges: np.ndarray
    right_edges: np.ndarray


def logarithmic_grouping(counts: np.ndarray) -> GroupedSupport:
    """Group the complete s >= 2 support into equal log10-width bins."""

    nonzero = np.flatnonzero(counts[MINIMUM_SIZE:]) + MINIMUM_SIZE
    if nonzero.size == 0:
        raise ValueError("no collective avalanche events were found")
    maximum_size = int(nonzero[-1])
    sizes = np.arange(MINIMUM_SIZE, maximum_size + 1, dtype=np.int64)
    edges = np.geomspace(
        float(MINIMUM_SIZE), float(maximum_size + 1), BIN_COUNT + 1
    )
    raw_bin = np.searchsorted(edges, sizes, side="right") - 1
    raw_bin = np.clip(raw_bin, 0, BIN_COUNT - 1)

    represented = np.bincount(raw_bin, minlength=BIN_COUNT) > 0
    remap = np.full(BIN_COUNT, -1, dtype=np.int64)
    remap[represented] = np.arange(int(represented.sum()))
    size_to_bin = remap[raw_bin]
    observed = np.bincount(
        size_to_bin,
        weights=counts[sizes].astype(np.float64),
        minlength=int(represented.sum()),
    )
    return GroupedSupport(
        observed=observed,
        size_to_bin=size_to_bin,
        log_sizes=np.log(sizes.astype(np.float64)),
        left_edges=edges[:-1][represented],
        right_edges=edges[1:][represented],
    )


def grouped_power_law_probabilities(
    grouping: GroupedSupport, exponent: float
) -> np.ndarray:
    """Integrate a truncated discrete power law over each logarithmic bin."""

    log_weights = -exponent * grouping.log_sizes
    log_weights -= float(log_weights.max())
    weights = np.exp(log_weights)
    probabilities = np.bincount(
        grouping.size_to_bin,
        weights=weights,
        minlength=grouping.observed.size,
    )
    return probabilities / probabilities.sum()


def fit_grouped_power_law(
    grouping: GroupedSupport, observed: np.ndarray
) -> tuple[float, np.ndarray]:
    """Fit the grouped model by multinomial maximum likelihood."""

    def negative_log_likelihood(exponent: float) -> float:
        probabilities = grouped_power_law_probabilities(grouping, exponent)
        return -float(np.dot(observed, np.log(probabilities)))

    result = optimize.minimize_scalar(
        negative_log_likelihood,
        bounds=(0.01, 10.0),
        method="bounded",
        options={"xatol": 1e-10},
    )
    if not result.success:
        raise RuntimeError(f"grouped power-law fit failed: {result.message}")
    exponent = float(result.x)
    return exponent, grouped_power_law_probabilities(grouping, exponent)


def multinomial_deviance(observed: np.ndarray, probabilities: np.ndarray) -> float:
    """Return the likelihood-ratio deviance from the saturated binned model."""

    expected = float(observed.sum()) * probabilities
    nonzero = observed > 0
    return 2.0 * float(
        np.sum(observed[nonzero] * np.log(observed[nonzero] / expected[nonzero]))
    )


def bootstrap_goodness_of_fit(
    grouping: GroupedSupport, *, replicates: int, seed: int
) -> dict[str, float | int | str]:
    """Calibrate binned-density lack of fit by parametric bootstrap."""

    observed = grouping.observed.astype(np.int64)
    _, fitted_probabilities = fit_grouped_power_law(grouping, observed)
    observed_deviance = multinomial_deviance(observed, fitted_probabilities)
    event_count = int(observed.sum())
    rng = np.random.default_rng(seed)
    exceedances = 0
    for _ in range(replicates):
        synthetic = rng.multinomial(event_count, fitted_probabilities)
        _, synthetic_probabilities = fit_grouped_power_law(grouping, synthetic)
        synthetic_deviance = multinomial_deviance(
            synthetic, synthetic_probabilities
        )
        exceedances += synthetic_deviance >= observed_deviance

    p_value = (exceedances + 1.0) / (replicates + 1.0)
    monte_carlo_error = float(np.sqrt(p_value * (1.0 - p_value) / replicates))
    return {
        "events": event_count,
        "minimum_size": MINIMUM_SIZE,
        "maximum_size": int(round(grouping.right_edges[-1] - 1.0)),
        "requested_bins": BIN_COUNT,
        "represented_bins": int(grouping.observed.size),
        "nonempty_bins": int(np.count_nonzero(grouping.observed)),
        "deviance": observed_deviance,
        "bootstrap_replicates": replicates,
        "exceedances": exceedances,
        "p_value": p_value,
        "monte_carlo_standard_error": monte_carlo_error,
        "decision_at_0.1": (
            "reject_power_law" if p_value <= REJECTION_THRESHOLD else "not_rejected"
        ),
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
    child_seeds = seed_sequence.spawn(len(TS_VALUES) * 2)
    rows: list[dict] = []
    seed_index = 0
    for ts in TS_VALUES:
        condition = load_or_build_cache(data_root, cache_root, ts)
        for include_terminal in (False, True):
            counts = condition.fibril_counts(
                include_terminal=include_terminal
            ).sum(axis=0)
            grouping = logarithmic_grouping(counts)
            result = bootstrap_goodness_of_fit(
                grouping,
                replicates=BOOTSTRAP_REPLICATES,
                seed=int(child_seeds[seed_index].generate_state(1)[0]),
            )
            seed_index += 1
            row = {
                "ts": ts,
                "terminal_rupture": "included" if include_terminal else "excluded",
                **result,
            }
            rows.append(row)
            print(
                f"Ts={ts}, terminal={row['terminal_rupture']}: "
                f"deviance={row['deviance']:.6g}, "
                f"p={row['p_value']:.6g} "
                f"({row['exceedances']}/{BOOTSTRAP_REPLICATES}), "
                f"{row['decision_at_0.1']}",
                flush=True,
            )

    write_csv(output / "binned_density_power_law_gof.csv", rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

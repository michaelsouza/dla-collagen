"""Joint high-Ts stretched-cutoff model with fibril-block inference."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

import numpy as np
from scipy import optimize

from clauset_pooled.models import (
    ModelFit,
    _stretched_cutoff_log_normalization,
    fit_stretched_cutoff_power_law,
    log_probabilities,
)
from clauset_pooled.alternative_gof import sample_model_counts

from .analysis import FibrilHistograms, _empirical_cdf_arrays


@dataclass(frozen=True)
class JointStretchedCutoffFit:
    xmin: int
    ts_values: tuple[int, ...]
    alpha: float
    beta: float
    scales: tuple[float, ...]
    log_likelihood: float
    n_tail: tuple[int, ...]
    ks: tuple[float, ...]

    def model_for(self, index: int) -> ModelFit:
        return ModelFit(
            model="stretched_cutoff_power_law",
            xmin=self.xmin,
            parameters={
                "alpha": self.alpha,
                "scale": self.scales[index],
                "beta": self.beta,
            },
            log_likelihood=float("nan"),
            ks=self.ks[index],
            n_tail=self.n_tail[index],
            parameter_count=3,
        )


@dataclass(frozen=True)
class JointXminSelection:
    """Common-support selection by the simultaneous KS criterion."""

    selected: JointStretchedCutoffFit
    candidates: tuple[JointStretchedCutoffFit, ...]


@dataclass(frozen=True)
class JointBootstrapReplicate:
    replicate: int
    xmin: int
    gof_xmin: int
    alpha: float
    beta: float
    scales: tuple[float, ...]
    centered_ks: tuple[float, ...]
    maximum_centered_ks: float


@dataclass(frozen=True)
class JointBlockGoodnessOfFit:
    observed: JointStretchedCutoffFit
    joint_p_value: float
    condition_p_values: tuple[float, ...]
    joint_exceedances: int
    condition_exceedances: tuple[int, ...]
    replicates: int
    bootstrap: tuple[JointBootstrapReplicate, ...]


@dataclass(frozen=True)
class JointParametricGoodnessOfFit:
    observed: JointStretchedCutoffFit
    joint_p_value: float
    condition_p_values: tuple[float, ...]
    joint_exceedances: int
    condition_exceedances: tuple[int, ...]
    replicates: int
    synthetic_ks: tuple[tuple[float, ...], ...]


def _tail_arrays(histogram: np.ndarray, xmin: int) -> tuple[np.ndarray, np.ndarray]:
    sizes = np.flatnonzero(histogram)
    sizes = sizes[sizes >= xmin]
    if sizes.size == 0:
        raise ValueError("empty stretched-cutoff tail")
    return sizes, histogram[sizes]


def _cdf_arrays(fit: ModelFit, maximum: int) -> tuple[np.ndarray, np.ndarray]:
    support = np.arange(fit.xmin, maximum + 1, dtype=np.int64)
    after = np.cumsum(np.exp(log_probabilities(fit, support)))
    before = np.concatenate(([0.0], after[:-1]))
    return after, before


def fit_joint_stretched_cutoff(
    datasets: tuple[FibrilHistograms, ...],
    *,
    xmin: int = 8,
    initial: JointStretchedCutoffFit | None = None,
) -> JointStretchedCutoffFit:
    """Fit common alpha/beta and one cutoff scale per Ts by exact discrete MLE."""
    if len(datasets) < 2:
        raise ValueError("joint fit requires at least two conditions")
    if len({data.ts for data in datasets}) != len(datasets):
        raise ValueError("joint fit requires distinct Ts values")
    arrays = [_tail_arrays(data.pooled, xmin) for data in datasets]
    total_events = sum(int(frequencies.sum()) for _, frequencies in arrays)

    def unpack(parameters: np.ndarray) -> tuple[float, float, np.ndarray]:
        return (
            1.0 + float(np.exp(parameters[0])),
            float(np.exp(parameters[1])),
            np.exp(parameters[2:]),
        )

    def objective(parameters: np.ndarray) -> float:
        alpha, beta, scales = unpack(parameters)
        total = 0.0
        for (sizes, frequencies), scale in zip(arrays, scales, strict=True):
            try:
                normalization = _stretched_cutoff_log_normalization(
                    alpha, float(scale), beta, xmin
                )
            except RuntimeError:
                return 1e300
            log_probabilities_local = (
                -alpha * np.log(sizes / float(xmin))
                - (sizes / scale) ** beta
                - normalization
            )
            total -= float(np.dot(frequencies, log_probabilities_local))
        return total / total_events if np.isfinite(total) else 1e300

    bounds = (
        (np.log(0.01), np.log(50.0)),
        (np.log(0.25), np.log(5.0)),
        *((np.log(float(xmin)), np.log(100_000.0)),) * len(datasets),
    )
    if initial is None:
        individual = [
            fit_stretched_cutoff_power_law(data.pooled, xmin) for data in datasets
        ]
        alpha = float(np.median([fit.parameters["alpha"] for fit in individual]))
        beta = float(np.median([fit.parameters["beta"] for fit in individual]))
        scales = [fit.parameters["scale"] for fit in individual]
    else:
        alpha, beta, scales = initial.alpha, initial.beta, initial.scales
    start = np.array(
        [np.log(max(alpha - 1.0, 0.01)), np.log(beta), *np.log(scales)]
    )
    result = optimize.minimize(
        objective,
        start,
        method="L-BFGS-B",
        bounds=bounds,
        options={"maxiter": 2000, "ftol": 1e-12, "gtol": 1e-7},
    )
    if not result.success or not np.isfinite(result.fun):
        raise RuntimeError(f"joint stretched-cutoff optimization failed: {result.message}")
    alpha, beta, scales_array = unpack(result.x)
    n_tail = []
    ks_values = []
    for data, scale in zip(datasets, scales_array, strict=True):
        histogram = data.pooled
        maximum = int(np.flatnonzero(histogram)[-1])
        empirical_after, empirical_before = _empirical_cdf_arrays(
            histogram[: maximum + 1], xmin
        )
        temporary = ModelFit(
            model="stretched_cutoff_power_law",
            xmin=xmin,
            parameters={"alpha": alpha, "scale": float(scale), "beta": beta},
            log_likelihood=float("nan"),
            ks=float("nan"),
            n_tail=int(histogram[xmin:].sum()),
            parameter_count=3,
        )
        model_after, model_before = _cdf_arrays(temporary, maximum)
        ks_values.append(
            float(max(
                np.max(np.abs(empirical_after - model_after)),
                np.max(np.abs(empirical_before - model_before)),
            ))
        )
        n_tail.append(int(histogram[xmin:].sum()))
    return JointStretchedCutoffFit(
        xmin=xmin,
        ts_values=tuple(data.ts for data in datasets),
        alpha=alpha,
        beta=beta,
        scales=tuple(float(scale) for scale in scales_array),
        log_likelihood=-float(result.fun) * total_events,
        n_tail=tuple(n_tail),
        ks=tuple(ks_values),
    )


def _common_xmin_candidates(
    datasets: tuple[FibrilHistograms, ...],
    *,
    minimum_xmin: int,
    minimum_tail: int,
    maximum_xmin: int | None,
) -> tuple[int, ...]:
    if minimum_xmin < 1:
        raise ValueError("minimum_xmin must be positive")
    if minimum_tail < 1:
        raise ValueError("minimum_tail must be positive")
    upper_limits = []
    for data in datasets:
        tail_counts = np.cumsum(data.pooled[::-1], dtype=np.int64)[::-1]
        eligible = np.flatnonzero(tail_counts >= minimum_tail)
        if eligible.size == 0:
            raise ValueError(
                f"Ts={data.ts}: no xmin candidate has {minimum_tail} tail events"
            )
        upper_limits.append(int(eligible[-1]))
    upper = min(upper_limits)
    if maximum_xmin is not None:
        upper = min(upper, maximum_xmin)
    if upper < minimum_xmin:
        raise ValueError("no common xmin candidate satisfies the tail constraint")
    return tuple(range(minimum_xmin, upper + 1))


def select_joint_stretched_cutoff_xmin(
    datasets: tuple[FibrilHistograms, ...],
    *,
    minimum_xmin: int = 1,
    minimum_tail: int = 1000,
    maximum_xmin: int | None = None,
    candidates: tuple[int, ...] | None = None,
    initial_candidates: tuple[JointStretchedCutoffFit, ...] | None = None,
    validate: bool = True,
) -> JointXminSelection:
    """Select a common xmin by minimizing the maximum condition-wise KS.

    Every candidate receives a joint exact-discrete MLE with common alpha and
    beta and one cutoff scale per condition.  The maximum KS makes the
    selection criterion match the simultaneous goodness-of-fit statistic.
    """
    if candidates is None:
        candidates = _common_xmin_candidates(
            datasets,
            minimum_xmin=minimum_xmin,
            minimum_tail=minimum_tail,
            maximum_xmin=maximum_xmin,
        )
    else:
        candidates = tuple(sorted(set(int(value) for value in candidates)))
        if not candidates or candidates[0] < 1:
            raise ValueError("xmin candidates must be positive")
        for data in datasets:
            for xmin in candidates:
                if int(data.pooled[xmin:].sum()) < minimum_tail:
                    raise ValueError(
                        f"Ts={data.ts}: xmin={xmin} has fewer than "
                        f"{minimum_tail} tail events"
                    )

    if initial_candidates is not None:
        initial_by_xmin = {fit.xmin: fit for fit in initial_candidates}
        if set(initial_by_xmin) != set(candidates):
            raise ValueError("initial candidate fits do not match xmin candidates")
        fits = [
            fit_joint_stretched_cutoff(
                datasets, xmin=xmin, initial=initial_by_xmin[xmin]
            )
            for xmin in candidates
        ]
        selected = min(fits, key=lambda fit: (max(fit.ks), fit.xmin))
        return JointXminSelection(selected=selected, candidates=tuple(fits))

    # Starting a six-parameter optimization cold at xmin=1 is unnecessarily
    # difficult because the singleton-dominated body is strongly misspecified.
    # Fit an interior anchor once, then warm-start both exhaustive sweeps.  This
    # changes only numerical initialization; every integer candidate is still
    # evaluated and the winner is independently validated below.
    anchor_index = len(candidates) // 2
    fits_by_xmin: dict[int, JointStretchedCutoffFit] = {}
    anchor = fit_joint_stretched_cutoff(
        datasets, xmin=candidates[anchor_index], initial=None
    )
    fits_by_xmin[anchor.xmin] = anchor

    initial = anchor
    for xmin in reversed(candidates[:anchor_index]):
        initial = fit_joint_stretched_cutoff(
            datasets, xmin=xmin, initial=initial
        )
        fits_by_xmin[xmin] = initial

    initial = anchor
    for xmin in candidates[anchor_index + 1:]:
        initial = fit_joint_stretched_cutoff(
            datasets, xmin=xmin, initial=initial
        )
        fits_by_xmin[xmin] = initial

    fits = [fits_by_xmin[xmin] for xmin in candidates]

    # A final multi-start fit guards the selected result against a warm-start
    # local optimum.  If it improves the likelihood, retain the validated MLE.
    preliminary = min(fits, key=lambda fit: (max(fit.ks), fit.xmin))
    if validate:
        validated = fit_joint_stretched_cutoff(
            datasets, xmin=preliminary.xmin, initial=None
        )
        if validated.log_likelihood > preliminary.log_likelihood + 1e-6:
            fits[candidates.index(preliminary.xmin)] = validated
    selected = min(fits, key=lambda fit: (max(fit.ks), fit.xmin))
    return JointXminSelection(selected=selected, candidates=tuple(fits))


def fit_joint_block_gof(
    datasets: tuple[FibrilHistograms, ...],
    *,
    xmin: int = 8,
    replicates: int = 199,
    seed: int = 161803,
    initial: JointStretchedCutoffFit | None = None,
) -> JointBlockGoodnessOfFit:
    """Centered block GOF for the common-shape high-Ts model."""
    if replicates < 1:
        raise ValueError("replicates must be positive")
    observed = fit_joint_stretched_cutoff(
        datasets, xmin=xmin, initial=initial
    )
    empirical = []
    modeled = []
    maxima = []
    for index, data in enumerate(datasets):
        maximum = int(np.flatnonzero(data.pooled)[-1])
        maxima.append(maximum)
        empirical.append(_empirical_cdf_arrays(data.pooled[: maximum + 1], xmin))
        modeled.append(_cdf_arrays(observed.model_for(index), maximum))
    rng = np.random.default_rng(seed)
    condition_exceedances = np.zeros(len(datasets), dtype=np.int64)
    joint_exceedances = 0
    records = []
    observed_maximum = max(observed.ks)
    for replicate in range(replicates):
        resampled = []
        for data in datasets:
            indices = rng.integers(0, data.fibrils, size=data.fibrils)
            counts = data.counts[indices]
            resampled.append(
                FibrilHistograms(ts=data.ts, seeds=data.seeds, counts=counts)
            )
        fitted = fit_joint_stretched_cutoff(
            tuple(resampled), xmin=xmin, initial=observed
        )
        statistics = []
        for index, data in enumerate(resampled):
            bootstrap_empirical = _empirical_cdf_arrays(
                data.pooled[: maxima[index] + 1], xmin
            )
            bootstrap_model = _cdf_arrays(fitted.model_for(index), maxima[index])
            statistic = float(max(
                np.max(np.abs(
                    (bootstrap_empirical[0] - empirical[index][0])
                    - (bootstrap_model[0] - modeled[index][0])
                )),
                np.max(np.abs(
                    (bootstrap_empirical[1] - empirical[index][1])
                    - (bootstrap_model[1] - modeled[index][1])
                )),
            ))
            statistics.append(statistic)
        maximum_statistic = max(statistics)
        condition_exceedances += np.asarray(statistics) >= np.asarray(observed.ks)
        joint_exceedances += maximum_statistic >= observed_maximum
        records.append(JointBootstrapReplicate(
            replicate=replicate,
            xmin=fitted.xmin,
            gof_xmin=xmin,
            alpha=fitted.alpha,
            beta=fitted.beta,
            scales=fitted.scales,
            centered_ks=tuple(statistics),
            maximum_centered_ks=maximum_statistic,
        ))
    return JointBlockGoodnessOfFit(
        observed=observed,
        joint_p_value=(joint_exceedances + 1) / (replicates + 1),
        condition_p_values=tuple(
            float((value + 1) / (replicates + 1))
            for value in condition_exceedances
        ),
        joint_exceedances=joint_exceedances,
        condition_exceedances=tuple(int(value) for value in condition_exceedances),
        replicates=replicates,
        bootstrap=tuple(records),
    )


def _selected_block_batch(
    arguments: tuple[
        tuple[FibrilHistograms, ...],
        JointXminSelection,
        int,
        tuple[tuple[int, int], ...],
    ]
) -> tuple[JointBootstrapReplicate, ...]:
    datasets, observed_selection, minimum_tail, replicate_seeds = arguments
    observed_by_xmin = {
        fit.xmin: fit for fit in observed_selection.candidates
    }
    maxima = [int(np.flatnonzero(data.pooled)[-1]) for data in datasets]
    observed_empirical: dict[int, list[tuple[np.ndarray, np.ndarray]]] = {}
    observed_modeled: dict[int, list[tuple[np.ndarray, np.ndarray]]] = {}
    for xmin, fitted in observed_by_xmin.items():
        observed_empirical[xmin] = [
            _empirical_cdf_arrays(data.pooled[: maximum + 1], xmin)
            for data, maximum in zip(datasets, maxima, strict=True)
        ]
        observed_modeled[xmin] = [
            _cdf_arrays(fitted.model_for(index), maximum)
            for index, maximum in enumerate(maxima)
        ]

    records = []
    all_candidates = tuple(observed_by_xmin)
    for replicate, child_seed in replicate_seeds:
        rng = np.random.default_rng(child_seed)
        resampled = []
        for data in datasets:
            indices = rng.integers(0, data.fibrils, size=data.fibrils)
            resampled.append(FibrilHistograms(
                ts=data.ts,
                seeds=data.seeds,
                counts=data.counts[indices],
            ))
        resampled_tuple = tuple(resampled)
        valid_candidates = tuple(
            xmin for xmin in all_candidates
            if all(
                int(data.pooled[xmin:].sum()) >= minimum_tail
                for data in resampled_tuple
            )
        )
        initial_candidates = tuple(
            observed_by_xmin[xmin] for xmin in valid_candidates
        )
        selection = select_joint_stretched_cutoff_xmin(
            resampled_tuple,
            candidates=valid_candidates,
            minimum_tail=minimum_tail,
            initial_candidates=initial_candidates,
            validate=False,
        )

        candidate_statistics = []
        for fitted in selection.candidates:
            xmin = fitted.xmin
            statistics = []
            for index, (data, maximum) in enumerate(
                zip(resampled_tuple, maxima, strict=True)
            ):
                empirical = _empirical_cdf_arrays(
                    data.pooled[: maximum + 1], xmin
                )
                modeled = _cdf_arrays(fitted.model_for(index), maximum)
                reference_empirical = observed_empirical[xmin][index]
                reference_modeled = observed_modeled[xmin][index]
                statistics.append(float(max(
                    np.max(np.abs(
                        (empirical[0] - reference_empirical[0])
                        - (modeled[0] - reference_modeled[0])
                    )),
                    np.max(np.abs(
                        (empirical[1] - reference_empirical[1])
                        - (modeled[1] - reference_modeled[1])
                    )),
                )))
            candidate_statistics.append((max(statistics), xmin, statistics))
        _, gof_xmin, selected_statistics = min(candidate_statistics)
        fitted = selection.selected
        records.append(JointBootstrapReplicate(
            replicate=replicate,
            xmin=fitted.xmin,
            gof_xmin=gof_xmin,
            alpha=fitted.alpha,
            beta=fitted.beta,
            scales=fitted.scales,
            centered_ks=tuple(selected_statistics),
            maximum_centered_ks=max(selected_statistics),
        ))
    return tuple(records)


def fit_joint_selected_block_gof(
    datasets: tuple[FibrilHistograms, ...],
    *,
    minimum_xmin: int = 1,
    minimum_tail: int = 1000,
    maximum_xmin: int | None = None,
    replicates: int = 199,
    seed: int = 161803,
    workers: int = 1,
) -> tuple[JointBlockGoodnessOfFit, JointXminSelection]:
    """Selection-adjusted centered block GOF for the joint tail model."""
    if replicates < 1 or workers < 1:
        raise ValueError("replicates and workers must be positive")
    observed_selection = select_joint_stretched_cutoff_xmin(
        datasets,
        minimum_xmin=minimum_xmin,
        minimum_tail=minimum_tail,
        maximum_xmin=maximum_xmin,
    )
    children = np.random.SeedSequence(seed).spawn(replicates)
    replicate_seeds = tuple(
        (index, int(child.generate_state(1, dtype=np.uint64)[0]))
        for index, child in enumerate(children)
    )
    batches = tuple(
        tuple(replicate_seeds[offset::workers]) for offset in range(workers)
        if replicate_seeds[offset::workers]
    )
    arguments = tuple(
        (datasets, observed_selection, minimum_tail, batch) for batch in batches
    )
    if workers == 1:
        records = list(_selected_block_batch(arguments[0]))
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            nested = executor.map(_selected_block_batch, arguments)
            records = [record for batch in nested for record in batch]
    records.sort(key=lambda record: record.replicate)

    observed = observed_selection.selected
    observed_ks = np.asarray(observed.ks)
    statistics = np.asarray([record.centered_ks for record in records])
    condition_exceedances = np.sum(statistics >= observed_ks[None, :], axis=0)
    joint_exceedances = int(np.sum(
        np.max(statistics, axis=1) >= float(np.max(observed_ks))
    ))
    result = JointBlockGoodnessOfFit(
        observed=observed,
        joint_p_value=(joint_exceedances + 1) / (replicates + 1),
        condition_p_values=tuple(
            float((value + 1) / (replicates + 1))
            for value in condition_exceedances
        ),
        joint_exceedances=joint_exceedances,
        condition_exceedances=tuple(int(value) for value in condition_exceedances),
        replicates=replicates,
        bootstrap=tuple(records),
    )
    return result, observed_selection


def _one_joint_parametric_replica(
    arguments: tuple[JointStretchedCutoffFit, tuple[int, ...], int]
) -> tuple[float, ...]:
    observed, tail_counts, seed = arguments
    rng = np.random.default_rng(seed)
    synthetic_datasets = []
    for index, (ts, count) in enumerate(
        zip(observed.ts_values, tail_counts, strict=True)
    ):
        sampled = sample_model_counts(
            count, observed.model_for(index), rng=rng
        )
        maximum = max(sampled)
        histogram = np.zeros(maximum + 1, dtype=np.int64)
        for size, frequency in sampled.items():
            histogram[size] = frequency
        synthetic_datasets.append(FibrilHistograms(
            ts=ts,
            seeds=np.array([0], dtype=np.int64),
            counts=histogram[None, :],
        ))
    fitted = fit_joint_stretched_cutoff(
        tuple(synthetic_datasets), xmin=observed.xmin, initial=observed
    )
    return fitted.ks


def fit_joint_parametric_gof(
    datasets: tuple[FibrilHistograms, ...],
    *,
    xmin: int = 8,
    replicates: int = 999,
    seed: int = 271828,
    workers: int = 1,
    initial: JointStretchedCutoffFit | None = None,
) -> JointParametricGoodnessOfFit:
    """Literal iid parametric-bootstrap sensitivity for the joint model."""
    if replicates < 1 or workers < 1:
        raise ValueError("replicates and workers must be positive")
    observed = fit_joint_stretched_cutoff(
        datasets, xmin=xmin, initial=initial
    )
    seeds = [
        int(child.generate_state(1, dtype=np.uint64)[0])
        for child in np.random.SeedSequence(seed).spawn(replicates)
    ]
    arguments = [
        (observed, observed.n_tail, child_seed) for child_seed in seeds
    ]
    if workers == 1:
        synthetic = [_one_joint_parametric_replica(value) for value in arguments]
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            synthetic = list(executor.map(
                _one_joint_parametric_replica,
                arguments,
                chunksize=max(1, replicates // (workers * 8)),
            ))
    synthetic_array = np.asarray(synthetic)
    observed_ks = np.asarray(observed.ks)
    condition_exceedances = np.sum(
        synthetic_array >= observed_ks[None, :], axis=0
    )
    joint_exceedances = int(np.sum(
        np.max(synthetic_array, axis=1) >= float(np.max(observed_ks))
    ))
    return JointParametricGoodnessOfFit(
        observed=observed,
        joint_p_value=(joint_exceedances + 1) / (replicates + 1),
        condition_p_values=tuple(
            float((value + 1) / (replicates + 1))
            for value in condition_exceedances
        ),
        joint_exceedances=joint_exceedances,
        condition_exceedances=tuple(int(value) for value in condition_exceedances),
        replicates=replicates,
        synthetic_ks=tuple(tuple(float(value) for value in row) for row in synthetic),
    )

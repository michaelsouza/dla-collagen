"""Clauset fitting with fibrils as independent resampling blocks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import duckdb
import numpy as np
from scipy import special, stats

from clauset_pooled.models import (
    ModelFit,
    fit_cutoff_power_law,
    fit_exponential,
    fit_lognormal,
    fit_power_law_model,
    fit_stretched_cutoff_power_law,
    log_probabilities,
)
from clauset_pooled.power_law import (
    PowerLawFit,
    fit_alpha,
    power_law_cdf,
    select_xmin,
)


@dataclass(frozen=True)
class FibrilHistograms:
    """Dense event counts for independent fibril geometries at one Ts."""

    ts: int
    seeds: np.ndarray
    counts: np.ndarray

    @property
    def pooled(self) -> np.ndarray:
        return self.counts.sum(axis=0, dtype=np.int64)

    @property
    def fibrils(self) -> int:
        return int(self.counts.shape[0])


@dataclass(frozen=True)
class BootstrapFit:
    replicate: int
    xmin: int
    alpha: float
    ks: float
    n_tail: int
    tail_fraction: float
    centered_ks: float


@dataclass(frozen=True)
class BlockPowerLawResult:
    observed: PowerLawFit
    p_value: float
    exceedances: int
    replicates: int
    alpha_ci: tuple[float, float]
    xmin_ci: tuple[float, float]
    tail_fraction: float
    maximum_size: int
    scaling_decades: float
    bootstrap: tuple[BootstrapFit, ...]


@dataclass(frozen=True)
class ModelComparison:
    first: str
    second: str
    log_likelihood_ratio: float
    cluster_statistic: float | None
    p_value: float | None
    favored: str
    test: str


@dataclass(frozen=True)
class BlockModelGoodnessOfFit:
    model: str
    xmin: int
    ks: float
    p_value: float
    exceedances: int
    replicates: int
    centered_ks: tuple[float, ...]
    bootstrap: tuple["BlockModelBootstrapFit", ...]


@dataclass(frozen=True)
class BlockModelBootstrapFit:
    replicate: int
    ks: float
    centered_ks: float
    parameters: dict[str, float]


@dataclass(frozen=True)
class ModelXminSelection:
    """Condition-specific support selected by minimum KS for one model."""

    selected: ModelFit
    candidates: tuple[ModelFit, ...]


def available_ts(database: str | Path) -> list[int]:
    connection = duckdb.connect(str(database), read_only=True)
    try:
        return [
            int(row[0])
            for row in connection.execute(
                "SELECT DISTINCT ts FROM fibril_histograms ORDER BY ts"
            ).fetchall()
        ]
    finally:
        connection.close()


def load_fibril_histograms(database: str | Path, ts: int) -> FibrilHistograms:
    """Load local preterminal event counts, retaining fibril identity."""
    connection = duckdb.connect(str(database), read_only=True)
    try:
        rows = connection.execute(
            """
            SELECT seed, avalanche_size, event_count
            FROM fibril_histograms
            WHERE ts = ? AND NOT is_terminal_step
            ORDER BY seed, avalanche_size
            """,
            [ts],
        ).fetchall()
    finally:
        connection.close()
    if not rows:
        raise ValueError(f"Ts={ts}: no preterminal avalanche events")
    seeds = np.array(sorted({int(row[0]) for row in rows}), dtype=np.int64)
    maximum = max(int(row[1]) for row in rows)
    counts = np.zeros((seeds.size, maximum + 1), dtype=np.int64)
    seed_index = {int(seed): index for index, seed in enumerate(seeds)}
    for seed, size, count in rows:
        if int(size) < 1 or int(count) < 1:
            raise ValueError(f"Ts={ts}: nonpositive size or count in cache")
        counts[seed_index[int(seed)], int(size)] = int(count)
    if np.any(counts.sum(axis=1) == 0):
        raise ValueError(f"Ts={ts}: fibril without preterminal events")
    return FibrilHistograms(ts=ts, seeds=seeds, counts=counts)


def _empirical_cdf_arrays(histogram: np.ndarray, xmin: int) -> tuple[np.ndarray, np.ndarray]:
    tail = histogram[xmin:].astype(np.int64, copy=False)
    n = int(tail.sum())
    if n == 0:
        raise ValueError("empty bootstrap tail")
    cumulative = np.cumsum(tail, dtype=np.int64)
    after = cumulative / n
    before = (cumulative - tail) / n
    return after, before


def _model_cdf_arrays(xmin: int, alpha: float, maximum: int) -> tuple[np.ndarray, np.ndarray]:
    support = np.arange(xmin, maximum + 1, dtype=np.int64)
    return (
        power_law_cdf(support, xmin=xmin, alpha=alpha),
        power_law_cdf(support - 1, xmin=xmin, alpha=alpha),
    )


def fit_block_power_law(
    data: FibrilHistograms,
    *,
    minimum_xmin: int = 1,
    minimum_tail: int = 1000,
    replicates: int = 999,
    seed: int = 12738,
) -> BlockPowerLawResult:
    """Fit Clauset and calibrate KS with a centered fibril-block bootstrap.

    The observed xmin is selected by Clauset's KS rule. The absolute-fit test
    is conditional on that selected support. Bootstrap fibrils are refitted at
    fixed xmin for the centered empirical-process KS, while a full xmin
    reselection is retained for parameter-uncertainty intervals.
    """
    if replicates < 1:
        raise ValueError("replicates must be positive")
    pooled = data.pooled
    observed = select_xmin(
        pooled, minimum_xmin=minimum_xmin, minimum_tail=minimum_tail
    )
    total = int(pooled.sum())
    maximum = int(np.flatnonzero(pooled)[-1])
    empirical_after, empirical_before = _empirical_cdf_arrays(
        pooled, observed.xmin
    )
    model_after, model_before = _model_cdf_arrays(
        observed.xmin, observed.alpha, maximum
    )
    observed_ks = float(
        max(
            np.max(np.abs(empirical_after - model_after)),
            np.max(np.abs(empirical_before - model_before)),
        )
    )
    if not np.isclose(observed_ks, observed.ks, rtol=1e-8, atol=1e-10):
        raise RuntimeError("dense and sparse KS implementations disagree")

    rng = np.random.default_rng(seed)
    fits: list[BootstrapFit] = []
    exceedances = 0
    for replicate in range(replicates):
        indices = rng.integers(0, data.fibrils, size=data.fibrils)
        histogram = data.counts[indices].sum(axis=0, dtype=np.int64)
        alpha, _ = fit_alpha(histogram, observed.xmin)
        bootstrap_after, bootstrap_before = _empirical_cdf_arrays(
            histogram, observed.xmin
        )
        bootstrap_model_after, bootstrap_model_before = _model_cdf_arrays(
            observed.xmin, alpha, maximum
        )
        centered_ks = float(
            max(
                np.max(
                    np.abs(
                        (bootstrap_after - empirical_after)
                        - (bootstrap_model_after - model_after)
                    )
                ),
                np.max(
                    np.abs(
                        (bootstrap_before - empirical_before)
                        - (bootstrap_model_before - model_before)
                    )
                ),
            )
        )
        exceedances += centered_ks >= observed.ks
        selected = select_xmin(
            histogram,
            minimum_xmin=minimum_xmin,
            minimum_tail=minimum_tail,
        )
        fits.append(
            BootstrapFit(
                replicate=replicate,
                xmin=selected.xmin,
                alpha=selected.alpha,
                ks=selected.ks,
                n_tail=selected.n_tail,
                tail_fraction=selected.n_tail / int(histogram.sum()),
                centered_ks=centered_ks,
            )
        )
    alphas = np.array([fit.alpha for fit in fits])
    xmins = np.array([fit.xmin for fit in fits])
    p_value = (exceedances + 1) / (replicates + 1)
    return BlockPowerLawResult(
        observed=observed,
        p_value=float(p_value),
        exceedances=exceedances,
        replicates=replicates,
        alpha_ci=tuple(float(value) for value in np.quantile(alphas, [0.025, 0.975])),
        xmin_ci=tuple(float(value) for value in np.quantile(xmins, [0.025, 0.975])),
        tail_fraction=observed.n_tail / total,
        maximum_size=maximum,
        scaling_decades=float(np.log10(maximum / observed.xmin)),
        bootstrap=tuple(fits),
    )


def _cluster_vuong(
    data: FibrilHistograms,
    first: ModelFit,
    second: ModelFit,
) -> ModelComparison:
    support = np.arange(first.xmin, data.counts.shape[1], dtype=np.int64)
    difference = log_probabilities(first, support) - log_probabilities(second, support)
    contributions = data.counts[:, first.xmin:] @ difference
    ratio = float(contributions.sum())
    standard_error = float(contributions.std(ddof=1) / np.sqrt(data.fibrils))
    if standard_error == 0.0:
        statistic = float(np.sign(contributions.mean()) * np.inf)
        p_value = 0.0
    else:
        statistic = float(contributions.mean() / standard_error)
        p_value = float(2.0 * stats.t.sf(abs(statistic), df=data.fibrils - 1))
    return ModelComparison(
        first=first.model,
        second=second.model,
        log_likelihood_ratio=ratio,
        cluster_statistic=statistic,
        p_value=p_value,
        favored=first.model if ratio > 0 else second.model,
        test="two-sided cluster-robust Vuong; fibril contributions",
    )


def fit_competing_models(
    data: FibrilHistograms,
    xmin: int,
) -> tuple[dict[str, ModelFit], tuple[ModelComparison, ...]]:
    """Fit alternatives on the same support and compare independent fibrils."""
    histogram = data.pooled
    models = {
        "power_law": fit_power_law_model(histogram, xmin),
        "cutoff_power_law": fit_cutoff_power_law(histogram, xmin),
        "lognormal": fit_lognormal(histogram, xmin),
        "exponential": fit_exponential(histogram, xmin),
    }
    power = models["power_law"]
    comparisons = [
        _cluster_vuong(data, power, models[name])
        for name in ("lognormal", "exponential")
    ]
    cutoff = models["cutoff_power_law"]
    likelihood_ratio = 2.0 * (cutoff.log_likelihood - power.log_likelihood)
    comparisons.append(
        ModelComparison(
            first="power_law",
            second="cutoff_power_law",
            log_likelihood_ratio=power.log_likelihood - cutoff.log_likelihood,
            cluster_statistic=likelihood_ratio,
            p_value=float(special.gammaincc(0.5, likelihood_ratio / 2.0)),
            favored="cutoff_power_law" if likelihood_ratio > 0 else "power_law",
            test=(
                "descriptive Wilks reference only; boundary/nesting means the "
                "cluster-aware decision requires cutoff goodness-of-fit"
            ),
        )
    )
    return models, tuple(comparisons)


def _fit_named_model(
    histogram: np.ndarray,
    model: str,
    xmin: int,
    *,
    initial: ModelFit | None = None,
) -> ModelFit:
    if model == "power_law":
        return fit_power_law_model(histogram, xmin)
    if model == "cutoff_power_law":
        return fit_cutoff_power_law(
            histogram,
            xmin,
            initial=initial.parameters if initial is not None else None,
        )
    if model == "lognormal":
        return fit_lognormal(
            histogram,
            xmin,
            initial=initial.parameters if initial is not None else None,
        )
    if model == "exponential":
        return fit_exponential(histogram, xmin)
    if model == "stretched_cutoff_power_law":
        return fit_stretched_cutoff_power_law(
            histogram,
            xmin,
            initial=initial.parameters if initial is not None else None,
        )
    raise ValueError(f"unsupported model: {model}")


def select_model_xmin(
    data: FibrilHistograms,
    *,
    model: str,
    minimum_xmin: int = 1,
    maximum_xmin: int | None = None,
    minimum_tail: int = 1000,
) -> ModelXminSelection:
    """Select a separate lower cutoff by the model's minimum KS distance.

    Adjacent candidates are warm-started because their empirical tails differ
    by only one integer size.  The provisional winner is then fitted again
    from the model's full default set of starting values, which protects the
    selected result against a warm-start local optimum.
    """
    if minimum_xmin < 1:
        raise ValueError("minimum_xmin must be positive")
    if minimum_tail < 1:
        raise ValueError("minimum_tail must be positive")
    pooled = data.pooled
    tail_counts = np.cumsum(pooled[::-1], dtype=np.int64)[::-1]
    eligible = np.flatnonzero(tail_counts >= minimum_tail)
    if eligible.size == 0:
        raise ValueError(
            f"Ts={data.ts}: no xmin candidate has {minimum_tail} tail events"
        )
    upper = int(eligible[-1])
    if maximum_xmin is not None:
        upper = min(upper, maximum_xmin)
    if upper < minimum_xmin:
        raise ValueError("no xmin candidate satisfies the tail constraint")

    candidates = tuple(range(minimum_xmin, upper + 1))
    anchor_index = len(candidates) // 2
    fits_by_xmin: dict[int, ModelFit] = {}
    anchor = _fit_named_model(pooled, model, candidates[anchor_index])
    fits_by_xmin[anchor.xmin] = anchor

    initial = anchor
    for xmin in reversed(candidates[:anchor_index]):
        initial = _fit_named_model(pooled, model, xmin, initial=initial)
        fits_by_xmin[xmin] = initial

    initial = anchor
    for xmin in candidates[anchor_index + 1:]:
        initial = _fit_named_model(pooled, model, xmin, initial=initial)
        fits_by_xmin[xmin] = initial

    fits = [fits_by_xmin[xmin] for xmin in candidates]
    provisional = min(fits, key=lambda fit: (fit.ks, fit.xmin))
    validated = _fit_named_model(pooled, model, provisional.xmin)
    if validated.log_likelihood > provisional.log_likelihood + 1e-6:
        fits[candidates.index(provisional.xmin)] = validated
    selected = min(fits, key=lambda fit: (fit.ks, fit.xmin))
    return ModelXminSelection(selected=selected, candidates=tuple(fits))


def _generic_model_cdf_arrays(
    fit: ModelFit,
    maximum: int,
) -> tuple[np.ndarray, np.ndarray]:
    support = np.arange(fit.xmin, maximum + 1, dtype=np.int64)
    probabilities = np.exp(log_probabilities(fit, support))
    after = np.cumsum(probabilities)
    before = np.concatenate(([0.0], after[:-1]))
    return after, before


def fit_block_model_gof(
    data: FibrilHistograms,
    *,
    model: str,
    xmin: int,
    replicates: int = 499,
    seed: int = 12738,
) -> BlockModelGoodnessOfFit:
    """Centered fibril-block absolute-fit test on a fixed common support."""
    if replicates < 1:
        raise ValueError("replicates must be positive")
    pooled = data.pooled
    maximum = int(np.flatnonzero(pooled)[-1])
    observed = _fit_named_model(pooled, model, xmin)
    empirical_after, empirical_before = _empirical_cdf_arrays(pooled, xmin)
    model_after, model_before = _generic_model_cdf_arrays(observed, maximum)
    observed_ks = float(
        max(
            np.max(np.abs(empirical_after - model_after)),
            np.max(np.abs(empirical_before - model_before)),
        )
    )
    if not np.isclose(observed_ks, observed.ks, rtol=1e-7, atol=1e-9):
        raise RuntimeError(
            f"dense and sparse KS disagree for {model}: "
            f"{observed_ks} != {observed.ks}"
        )
    rng = np.random.default_rng(seed)
    centered_statistics: list[float] = []
    bootstrap_fits: list[BlockModelBootstrapFit] = []
    exceedances = 0
    for replicate in range(replicates):
        indices = rng.integers(0, data.fibrils, size=data.fibrils)
        histogram = data.counts[indices].sum(axis=0, dtype=np.int64)
        fitted = _fit_named_model(
            histogram, model, xmin, initial=observed
        )
        bootstrap_after, bootstrap_before = _empirical_cdf_arrays(
            histogram, xmin
        )
        bootstrap_model_after, bootstrap_model_before = _generic_model_cdf_arrays(
            fitted, maximum
        )
        statistic = float(
            max(
                np.max(
                    np.abs(
                        (bootstrap_after - empirical_after)
                        - (bootstrap_model_after - model_after)
                    )
                ),
                np.max(
                    np.abs(
                        (bootstrap_before - empirical_before)
                        - (bootstrap_model_before - model_before)
                    )
                ),
            )
        )
        centered_statistics.append(statistic)
        bootstrap_fits.append(
            BlockModelBootstrapFit(
                replicate=replicate,
                ks=fitted.ks,
                centered_ks=statistic,
                parameters=dict(fitted.parameters),
            )
        )
        exceedances += statistic >= observed.ks
    return BlockModelGoodnessOfFit(
        model=model,
        xmin=xmin,
        ks=observed.ks,
        p_value=float((exceedances + 1) / (replicates + 1)),
        exceedances=exceedances,
        replicates=replicates,
        centered_ks=tuple(centered_statistics),
        bootstrap=tuple(bootstrap_fits),
    )

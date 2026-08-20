"""Discrete candidate distributions for the Issue 14 analysis.

The primary Araújo discretization is the exact difference of the survival
function in Eq. (4) of Araújo et al. (2003).  Its normalization telescopes on
the infinite integer support and therefore needs no numerical upper cutoff.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping
from typing import Callable

import numpy as np
from scipy import optimize, special, stats


Array = np.ndarray
Histogram = np.ndarray | Mapping[int, int]


@dataclass(frozen=True)
class FitResult:
    model: str
    xmin: int
    parameters: dict[str, float]
    log_likelihood: float
    ks: float
    tail_ad: float
    n: int
    parameter_count: int
    converged: bool
    optimizer_message: str

    @property
    def aic(self) -> float:
        return 2.0 * self.parameter_count - 2.0 * self.log_likelihood

    @property
    def bic(self) -> float:
        return np.log(self.n) * self.parameter_count - 2.0 * self.log_likelihood


def observed_arrays(counts: Histogram, xmin: int) -> tuple[Array, Array]:
    if isinstance(counts, Mapping):
        items = sorted(
            (int(size), int(frequency))
            for size, frequency in counts.items()
            if frequency and int(size) >= xmin
        )
        if not items or any(size < 1 or frequency < 1 for size, frequency in items):
            raise ValueError("histogram mapping must contain positive sizes and frequencies")
        return (
            np.asarray([size for size, _ in items], dtype=np.int64),
            np.asarray([frequency for _, frequency in items], dtype=np.int64),
        )
    values = np.asarray(counts)
    if values.ndim != 1 or np.any(values < 0):
        raise ValueError("counts must be a one-dimensional nonnegative array")
    if not np.all(values == np.rint(values)):
        raise ValueError("counts must contain integer frequencies")
    sizes = np.flatnonzero(values)
    selected = sizes >= xmin
    sizes = sizes[selected].astype(np.int64)
    frequencies = values[sizes].astype(np.int64)
    if frequencies.sum() == 0:
        raise ValueError(f"no observations at s >= {xmin}")
    return sizes, frequencies


def _log_survival_araujo(
    x: Array, *, boundary: float, alpha: float, eta: float, s0: float
) -> Array:
    x = np.asarray(x, dtype=float)
    return (
        -alpha * np.log(x / boundary)
        - np.exp(eta * np.log(x / s0))
        + np.exp(eta * np.log(boundary / s0))
    )


def _log_survival_derivatives(
    x: Array, *, boundary: float, alpha: float, eta: float, s0: float
) -> Array:
    """Derivatives of log survival w.r.t. (alpha, log(eta), log(s0))."""
    x = np.asarray(x, dtype=float)
    x_eta = np.exp(eta * np.log(x / s0))
    b_eta = np.exp(eta * np.log(boundary / s0))
    return np.column_stack(
        (
            -np.log(x / boundary),
            -eta * (x_eta * np.log(x / s0) - b_eta * np.log(boundary / s0)),
            eta * (x_eta - b_eta),
        )
    )


def araujo_logpmf(
    sizes: Array,
    *,
    xmin: int,
    alpha: float,
    eta: float,
    s0: float,
    discretization: str = "survival_difference",
) -> Array:
    """Log PMF of the conditional discrete Araújo model.

    ``survival_difference`` assigns the continuous interval ``[s,s+1)`` to
    integer ``s``. ``integrated_density`` is the prespecified sensitivity that
    integrates the continuous density over ``[s-1/2,s+1/2)``.
    """
    sizes = np.asarray(sizes, dtype=float)
    if alpha <= 0.0 or eta <= 0.0 or s0 <= 0.0:
        return np.full(sizes.shape, -np.inf)
    if discretization == "survival_difference":
        boundary = float(xmin)
        left, right = sizes, sizes + 1.0
    elif discretization == "integrated_density":
        boundary = xmin - 0.5
        left, right = sizes - 0.5, sizes + 0.5
    else:
        raise ValueError(f"unknown Araújo discretization: {discretization}")
    log_left = _log_survival_araujo(
        left, boundary=boundary, alpha=alpha, eta=eta, s0=s0
    )
    log_right = _log_survival_araujo(
        right, boundary=boundary, alpha=alpha, eta=eta, s0=s0
    )
    ratio = np.minimum(log_right - log_left, -np.finfo(float).eps)
    return log_left + np.log(-np.expm1(ratio))


def araujo_score(
    sizes: Array,
    *,
    xmin: int,
    alpha: float,
    eta: float,
    s0: float,
    discretization: str = "survival_difference",
) -> Array:
    """Score of each log PMF value for (alpha, log eta, log s0)."""
    sizes = np.asarray(sizes, dtype=float)
    if discretization == "survival_difference":
        boundary, left, right = float(xmin), sizes, sizes + 1.0
    elif discretization == "integrated_density":
        boundary, left, right = xmin - 0.5, sizes - 0.5, sizes + 0.5
    else:
        raise ValueError(f"unknown Araújo discretization: {discretization}")
    log_left = _log_survival_araujo(
        left, boundary=boundary, alpha=alpha, eta=eta, s0=s0
    )
    log_right = _log_survival_araujo(
        right, boundary=boundary, alpha=alpha, eta=eta, s0=s0
    )
    left_score = _log_survival_derivatives(
        left, boundary=boundary, alpha=alpha, eta=eta, s0=s0
    )
    right_score = _log_survival_derivatives(
        right, boundary=boundary, alpha=alpha, eta=eta, s0=s0
    )
    ratio = np.exp(np.minimum(log_right - log_left, -np.finfo(float).eps))
    return left_score - ratio[:, None] * (right_score - left_score) / (
        1.0 - ratio[:, None]
    )


def araujo_cdf(
    sizes: Array,
    *,
    xmin: int,
    alpha: float,
    eta: float,
    s0: float,
    discretization: str = "survival_difference",
) -> tuple[Array, Array]:
    sizes = np.asarray(sizes, dtype=float)
    if discretization == "survival_difference":
        boundary, before_x, after_x = float(xmin), sizes, sizes + 1.0
    elif discretization == "integrated_density":
        boundary, before_x, after_x = xmin - 0.5, sizes - 0.5, sizes + 0.5
    else:
        raise ValueError(f"unknown Araújo discretization: {discretization}")
    before = -np.expm1(
        _log_survival_araujo(
            before_x, boundary=boundary, alpha=alpha, eta=eta, s0=s0
        )
    )
    after = -np.expm1(
        _log_survival_araujo(
            after_x, boundary=boundary, alpha=alpha, eta=eta, s0=s0
        )
    )
    return np.clip(after, 0.0, 1.0), np.clip(before, 0.0, 1.0)


def power_law_logpmf(sizes: Array, *, xmin: int, alpha: float) -> Array:
    if alpha <= 1.0:
        return np.full(np.asarray(sizes).shape, -np.inf)
    return -alpha * np.log(sizes) - np.log(special.zeta(alpha, float(xmin)))


def power_law_cdf(
    sizes: Array, *, xmin: int, alpha: float
) -> tuple[Array, Array]:
    sizes = np.asarray(sizes, dtype=float)
    zeta = special.zeta(alpha, float(xmin))
    after = 1.0 - special.zeta(alpha, sizes + 1.0) / zeta
    before = 1.0 - special.zeta(alpha, sizes) / zeta
    return np.clip(after, 0.0, 1.0), np.clip(before, 0.0, 1.0)


def lognormal_logpmf(
    sizes: Array, *, xmin: int, mu: float, sigma: float
) -> Array:
    if sigma <= 0.0:
        return np.full(np.asarray(sizes).shape, -np.inf)
    sizes = np.asarray(sizes, dtype=float)
    lower = (np.log(sizes - 0.5) - mu) / sigma
    upper = (np.log(sizes + 0.5) - mu) / sigma
    mass = special.ndtr(upper) - special.ndtr(lower)
    normalization = special.ndtr(-(np.log(xmin - 0.5) - mu) / sigma)
    if not np.isfinite(normalization) or normalization <= 0.0:
        return np.full(sizes.shape, -np.inf)
    return np.log(np.maximum(mass, np.finfo(float).tiny)) - np.log(normalization)


def lognormal_cdf(
    sizes: Array, *, xmin: int, mu: float, sigma: float
) -> tuple[Array, Array]:
    sizes = np.asarray(sizes, dtype=float)
    boundary = (np.log(xmin - 0.5) - mu) / sigma
    norm = special.ndtr(-boundary)
    before = (
        special.ndtr((np.log(sizes - 0.5) - mu) / sigma) - special.ndtr(boundary)
    ) / norm
    after = (
        special.ndtr((np.log(sizes + 0.5) - mu) / sigma) - special.ndtr(boundary)
    ) / norm
    return np.clip(after, 0.0, 1.0), np.clip(before, 0.0, 1.0)


def _cutoff_probabilities(
    maximum: int, *, xmin: int, alpha: float, rate: float, tolerance: float = 1e-11
) -> tuple[Array, float]:
    """Return probabilities through ``maximum`` and their infinite normalizer.

    For alpha >= 0 the ratio of successive unnormalized masses is bounded by
    exp(-rate), giving a rigorous geometric upper bound on the omitted tail.
    """
    if alpha < 0.0 or rate <= 0.0:
        return np.full(maximum - xmin + 1, np.nan), np.nan
    end = max(maximum + 1, xmin + 128)
    total = 0.0
    chunks: list[Array] = []
    start = xmin
    q = np.exp(-rate)
    while True:
        support = np.arange(start, end, dtype=float)
        weights = np.exp(-alpha * np.log(support / xmin) - rate * (support - xmin))
        chunks.append(weights)
        total += float(weights.sum())
        next_weight = np.exp(
            -alpha * np.log(end / xmin) - rate * (end - xmin)
        )
        tail_bound = next_weight / (1.0 - q)
        if tail_bound <= tolerance * total:
            break
        if end - xmin > 2_000_000:
            raise RuntimeError("cutoff-power-law normalization did not converge")
        start, end = end, xmin + 2 * (end - xmin)
    weights = np.concatenate(chunks)
    return weights[: maximum - xmin + 1] / total, total


def cutoff_logpmf(
    sizes: Array, *, xmin: int, alpha: float, rate: float
) -> Array:
    sizes = np.asarray(sizes, dtype=np.int64)
    _, normalization = _cutoff_probabilities(
        int(sizes[-1]), xmin=xmin, alpha=alpha, rate=rate
    )
    return (
        -alpha * np.log(sizes / float(xmin))
        - rate * (sizes - xmin)
        - np.log(normalization)
    )


def cutoff_cdf(
    sizes: Array, *, xmin: int, alpha: float, rate: float
) -> tuple[Array, Array]:
    sizes = np.asarray(sizes, dtype=np.int64)
    probabilities, _ = _cutoff_probabilities(
        int(sizes[-1]), xmin=xmin, alpha=alpha, rate=rate
    )
    cumulative = np.cumsum(probabilities)
    after = cumulative[sizes - xmin]
    before = np.where(sizes == xmin, 0.0, cumulative[sizes - xmin - 1])
    return after, before


def two_population_logpmf(
    sizes: Array,
    *,
    xmin: int,
    weight_body: float,
    alpha: float,
    mu: float,
    sigma: float,
) -> Array:
    sizes = np.asarray(sizes, dtype=float)
    if not (0.0 < weight_body < 1.0 and alpha > 1.0 and sigma > 0.0):
        return np.full(sizes.shape, -np.inf)
    log_body = power_law_logpmf(sizes, xmin=xmin, alpha=alpha)
    log_large = lognormal_logpmf(sizes, xmin=xmin, mu=mu, sigma=sigma)
    return np.logaddexp(
        np.log(weight_body) + log_body, np.log1p(-weight_body) + log_large
    )


def two_population_cdf(
    sizes: Array,
    *,
    xmin: int,
    weight_body: float,
    alpha: float,
    mu: float,
    sigma: float,
) -> tuple[Array, Array]:
    sizes = np.asarray(sizes, dtype=float)
    body_after, body_before = power_law_cdf(
        sizes.astype(np.int64), xmin=xmin, alpha=alpha
    )
    large_after, large_before = lognormal_cdf(
        sizes, xmin=xmin, mu=mu, sigma=sigma
    )
    return (
        weight_body * body_after + (1.0 - weight_body) * large_after,
        weight_body * body_before + (1.0 - weight_body) * large_before,
    )


def discrete_diagnostics(
    frequencies: Array, model_after: Array, model_before: Array
) -> tuple[float, float]:
    n = int(frequencies.sum())
    empirical_after = np.cumsum(frequencies, dtype=np.int64) / n
    empirical_before = (np.cumsum(frequencies) - frequencies) / n
    ks = max(
        float(np.max(np.abs(empirical_after - model_after))),
        float(np.max(np.abs(empirical_before - model_before))),
    )
    variance = np.clip(model_after * (1.0 - model_after), 1.0 / n, None)
    tail_ad = float(np.sqrt(np.mean((empirical_after - model_after) ** 2 / variance)))
    return ks, tail_ad


def _best_result(
    objective: Callable[[Array], float],
    starts: list[Array],
    bounds: tuple[tuple[float, float], ...],
    jac: Callable[[Array], Array] | None = None,
) -> optimize.OptimizeResult:
    attempts = [
        optimize.minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=bounds,
            jac=jac,
            options={"maxiter": 2500, "ftol": 1e-12, "gtol": 1e-7},
        )
        for start in starts
    ]
    finite = [item for item in attempts if np.isfinite(item.fun)]
    if not finite:
        raise RuntimeError("all optimization starts returned non-finite objectives")
    return min(finite, key=lambda item: item.fun)


def _fit_araujo(
    counts: Histogram,
    xmin: int,
    *,
    discretization: str,
    initial: dict[str, float] | None,
) -> FitResult:
    sizes, frequencies = observed_arrays(counts, xmin)
    n = int(frequencies.sum())

    def unpack(x: Array) -> tuple[float, float, float]:
        return float(x[0]), float(np.exp(x[1])), float(np.exp(x[2]))

    def objective(x: Array) -> float:
        alpha, eta, s0 = unpack(x)
        values = araujo_logpmf(
            sizes,
            xmin=xmin,
            alpha=alpha,
            eta=eta,
            s0=s0,
            discretization=discretization,
        )
        return -float(np.dot(frequencies, values))

    def gradient(x: Array) -> Array:
        alpha, eta, s0 = unpack(x)
        score = araujo_score(
            sizes,
            xmin=xmin,
            alpha=alpha,
            eta=eta,
            s0=s0,
            discretization=discretization,
        )
        return -np.dot(frequencies, score)

    maximum = int(sizes[-1])
    if initial is None:
        starts = [
            np.array([alpha, np.log(eta), np.log(s0)])
            for alpha in (0.08, 0.3, 1.0, 2.0)
            for eta in (0.7, 1.5, 3.0)
            for s0 in (max(2.0, maximum / 10), max(3.0, maximum / 2), maximum)
        ]
    else:
        base = np.array(
            [initial["alpha"], np.log(initial["eta"]), np.log(initial["s0"])]
        )
        starts = [base, base + np.array([0.0, 0.08, -0.08])]
    bounds = ((1e-5, 20.0), (np.log(0.15), np.log(12.0)), (np.log(0.5), np.log(1e7)))
    result = _best_result(objective, starts, bounds, jac=gradient)
    alpha, eta, s0 = unpack(result.x)
    after, before = araujo_cdf(
        sizes,
        xmin=xmin,
        alpha=alpha,
        eta=eta,
        s0=s0,
        discretization=discretization,
    )
    ks, tail_ad = discrete_diagnostics(frequencies, after, before)
    name = "araujo" if discretization == "survival_difference" else "araujo_integrated"
    return FitResult(
        name,
        xmin,
        {"alpha": alpha, "tau": alpha + 1.0, "eta": eta, "s0": s0},
        -float(result.fun),
        ks,
        tail_ad,
        n,
        3,
        bool(result.success),
        str(result.message),
    )


def _fit_power_law(counts: Histogram, xmin: int) -> FitResult:
    sizes, frequencies = observed_arrays(counts, xmin)
    n = int(frequencies.sum())
    log_sizes = float(np.dot(frequencies, np.log(sizes)))

    def objective(alpha: float) -> float:
        return alpha * log_sizes + n * np.log(special.zeta(alpha, float(xmin)))

    result = optimize.minimize_scalar(
        objective, bounds=(1.000001, 100.0), method="bounded", options={"xatol": 1e-10}
    )
    alpha = float(result.x)
    after, before = power_law_cdf(sizes, xmin=xmin, alpha=alpha)
    ks, tail_ad = discrete_diagnostics(frequencies, after, before)
    return FitResult(
        "power_law",
        xmin,
        {"alpha": alpha},
        -float(result.fun),
        ks,
        tail_ad,
        n,
        1,
        bool(result.success),
        str(result.message),
    )


def _fit_cutoff(
    counts: Histogram, xmin: int, *, initial: dict[str, float] | None
) -> FitResult:
    sizes, frequencies = observed_arrays(counts, xmin)

    def unpack(x: Array) -> tuple[float, float]:
        return float(np.exp(x[0])), float(np.exp(x[1]))

    def objective(x: Array) -> float:
        alpha, rate = unpack(x)
        try:
            values = cutoff_logpmf(sizes, xmin=xmin, alpha=alpha, rate=rate)
        except RuntimeError:
            return float("inf")
        return -float(np.dot(frequencies, values))

    if initial is None:
        starts = [
            np.array([np.log(alpha), np.log(rate)])
            for alpha in (0.1, 1.0, 2.5)
            for rate in (0.001, 0.01, 0.1)
        ]
    else:
        starts = [
            np.array([np.log(initial["alpha"]), np.log(initial["rate"])]),
        ]
    result = _best_result(
        objective,
        starts,
        ((np.log(1e-6), np.log(100.0)), (np.log(1e-4), np.log(10.0))),
    )
    alpha, rate = unpack(result.x)
    after, before = cutoff_cdf(sizes, xmin=xmin, alpha=alpha, rate=rate)
    ks, tail_ad = discrete_diagnostics(frequencies, after, before)
    return FitResult(
        "cutoff_power_law",
        xmin,
        {"alpha": alpha, "rate": rate},
        -float(result.fun),
        ks,
        tail_ad,
        int(frequencies.sum()),
        2,
        bool(result.success),
        str(result.message),
    )


def _fit_lognormal(
    counts: Histogram, xmin: int, *, initial: dict[str, float] | None
) -> FitResult:
    sizes, frequencies = observed_arrays(counts, xmin)
    mean_log = float(np.average(np.log(sizes), weights=frequencies))
    sd_log = max(float(np.sqrt(np.average((np.log(sizes) - mean_log) ** 2, weights=frequencies))), 0.1)

    def objective(x: Array) -> float:
        return -float(
            np.dot(
                frequencies,
                lognormal_logpmf(sizes, xmin=xmin, mu=float(x[0]), sigma=float(np.exp(x[1]))),
            )
        )

    if initial is None:
        starts = [np.array([mean_log + shift, np.log(sd_log * scale)]) for shift in (-1.0, 0.0, 1.0) for scale in (0.7, 1.3)]
    else:
        starts = [np.array([initial["mu"], np.log(initial["sigma"])])]
    result = _best_result(
        objective,
        starts,
        ((np.log(xmin - 0.5) - 25.0, np.log(int(sizes[-1]) + 0.5) + 10.0), (np.log(0.02), np.log(30.0))),
    )
    mu, sigma = float(result.x[0]), float(np.exp(result.x[1]))
    after, before = lognormal_cdf(sizes, xmin=xmin, mu=mu, sigma=sigma)
    ks, tail_ad = discrete_diagnostics(frequencies, after, before)
    return FitResult(
        "lognormal",
        xmin,
        {"mu": mu, "sigma": sigma},
        -float(result.fun),
        ks,
        tail_ad,
        int(frequencies.sum()),
        2,
        bool(result.success),
        str(result.message),
    )


def _fit_two_population(
    counts: Histogram, xmin: int, *, initial: dict[str, float] | None
) -> FitResult:
    sizes, frequencies = observed_arrays(counts, xmin)
    n = int(frequencies.sum())
    cumulative = np.cumsum(frequencies)

    def unpack(x: Array) -> tuple[float, float, float, float]:
        return (
            float(special.expit(x[0])),
            float(1.0 + np.exp(x[1])),
            float(x[2]),
            float(np.exp(x[3])),
        )

    def objective(x: Array) -> float:
        weight, alpha, mu, sigma = unpack(x)
        values = two_population_logpmf(
            sizes,
            xmin=xmin,
            weight_body=weight,
            alpha=alpha,
            mu=mu,
            sigma=sigma,
        )
        return -float(np.dot(frequencies, values))

    if initial is None:
        starts = []
        for split_p in (0.90, 0.97, 0.99):
            index = min(int(np.searchsorted(cumulative, split_p * n)), len(sizes) - 2)
            large_sizes, large_counts = sizes[index + 1 :], frequencies[index + 1 :]
            mu = float(np.average(np.log(large_sizes), weights=large_counts))
            sigma = max(float(np.sqrt(np.average((np.log(large_sizes) - mu) ** 2, weights=large_counts))), 0.08)
            starts.append(
                np.array(
                    [special.logit(split_p), np.log(1.8 - 1.0), mu, np.log(sigma)]
                )
            )
    else:
        starts = [
            np.array(
                [
                    special.logit(initial["weight_body"]),
                    np.log(initial["alpha"] - 1.0),
                    initial["mu"],
                    np.log(initial["sigma"]),
                ]
            )
        ]
    result = _best_result(
        objective,
        starts,
        (
            (-14.0, 14.0),
            (np.log(1e-6), np.log(99.0)),
            (np.log(xmin + 0.5), np.log(int(sizes[-1]) + 0.5) + 5.0),
            (np.log(0.02), np.log(20.0)),
        ),
    )
    weight, alpha, mu, sigma = unpack(result.x)
    after, before = two_population_cdf(
        sizes,
        xmin=xmin,
        weight_body=weight,
        alpha=alpha,
        mu=mu,
        sigma=sigma,
    )
    ks, tail_ad = discrete_diagnostics(frequencies, after, before)
    return FitResult(
        "two_population",
        xmin,
        {
            "weight_body": weight,
            "alpha": alpha,
            "mu": mu,
            "sigma": sigma,
        },
        -float(result.fun),
        ks,
        tail_ad,
        n,
        4,
        bool(result.success),
        str(result.message),
    )


def fit_model(
    counts: Histogram,
    model: str,
    *,
    xmin: int = 2,
    initial: dict[str, float] | None = None,
) -> FitResult:
    """Fit one prespecified model to a size-indexed integer histogram."""
    if xmin < 1:
        raise ValueError("xmin must be positive")
    if model == "araujo":
        return _fit_araujo(
            counts, xmin, discretization="survival_difference", initial=initial
        )
    if model == "araujo_integrated":
        return _fit_araujo(
            counts, xmin, discretization="integrated_density", initial=initial
        )
    if model == "power_law":
        return _fit_power_law(counts, xmin)
    if model == "cutoff_power_law":
        return _fit_cutoff(counts, xmin, initial=initial)
    if model == "lognormal":
        return _fit_lognormal(counts, xmin, initial=initial)
    if model == "two_population":
        return _fit_two_population(counts, xmin, initial=initial)
    raise ValueError(f"unknown model: {model}")


def model_cdf(sizes: Array, fit: FitResult) -> tuple[Array, Array]:
    p = fit.parameters
    if fit.model in {"araujo", "araujo_integrated"}:
        return araujo_cdf(
            sizes,
            xmin=fit.xmin,
            alpha=p["alpha"],
            eta=p["eta"],
            s0=p["s0"],
            discretization=(
                "survival_difference"
                if fit.model == "araujo"
                else "integrated_density"
            ),
        )
    if fit.model == "power_law":
        return power_law_cdf(sizes, xmin=fit.xmin, alpha=p["alpha"])
    if fit.model == "cutoff_power_law":
        return cutoff_cdf(
            sizes, xmin=fit.xmin, alpha=p["alpha"], rate=p["rate"]
        )
    if fit.model == "lognormal":
        return lognormal_cdf(
            sizes, xmin=fit.xmin, mu=p["mu"], sigma=p["sigma"]
        )
    if fit.model == "two_population":
        return two_population_cdf(
            sizes,
            xmin=fit.xmin,
            weight_body=p["weight_body"],
            alpha=p["alpha"],
            mu=p["mu"],
            sigma=p["sigma"],
        )
    raise ValueError(f"unknown fitted model: {fit.model}")


def model_pmf(sizes: Array, fit: FitResult) -> Array:
    after, before = model_cdf(sizes, fit)
    return np.maximum(after - before, 0.0)


def finite_difference_gradient(
    function: Callable[[Array], float], point: Array, relative_step: float = 1e-6
) -> Array:
    """Central finite-difference gradient used by the implementation audit."""
    point = np.asarray(point, dtype=float)
    result = np.empty_like(point)
    for index in range(point.size):
        step = relative_step * max(1.0, abs(point[index]))
        upper, lower = point.copy(), point.copy()
        upper[index] += step
        lower[index] -= step
        result[index] = (function(upper) - function(lower)) / (2.0 * step)
    return result

"""Statistical analysis of local avalanche-cluster sizes.

The raw fracture output contains several independent rupture runs per file.  This
module keeps that hierarchy intact and separates the final, system-spanning
failure row from the preceding damage process.
"""

from __future__ import annotations

import csv
import hashlib
import inspect
import re
from concurrent.futures import ProcessPoolExecutor
from collections.abc import Mapping, Sequence
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import mpmath
import numpy as np
from scipy import sparse
from scipy import optimize, special


_FILE_NAME = re.compile(r"^ts_(?P<ts>\d+)_seed_(?P<seed>\d+)_m_(?P<m>\d+)\.txt$")
_RUN_SEPARATOR = re.compile(r"^-+(?P<run_id>\d+)\s*$")
_SIZE_FIELD = re.compile(r"^(?:0|[1-9][0-9]*(?:-[1-9][0-9]*)*)$")
_HEADER = (
    "f,num_active_particles,num_deleted_particles,total_deleted_rods,"
    "avalanche_sizes"
)


@dataclass(frozen=True)
class ParsedAvalancheFile:
    """Avalanche counts from one fibril, with one sparse row per rupture run."""

    source: Path
    ts: int
    fibril_seed: int
    weibull_m: int
    initial_particles: int
    source_bytes: int
    source_sha256: str
    run_ids: tuple[int, ...]
    preterminal_counts: sparse.csr_matrix
    terminal_counts: sparse.csr_matrix

    def aggregate_counts(self, *, include_terminal: bool = False) -> np.ndarray:
        """Return exact integer-size frequencies, indexed directly by size."""

        counts = np.asarray(self.preterminal_counts.sum(axis=0)).ravel()
        if include_terminal:
            counts = counts + np.asarray(self.terminal_counts.sum(axis=0)).ravel()
        return counts.astype(np.int64, copy=False)


@dataclass(frozen=True)
class DistributionFit:
    """Maximum-likelihood fit to an exact integer-valued tail."""

    model: str
    xmin: int
    parameters: dict[str, float]
    log_likelihood: float
    ks: float
    n: float
    diagnostics: dict[str, float | bool | str] = field(default_factory=dict)


@dataclass(frozen=True)
class PowerLawGoodnessOfFit:
    """Semiparametric Clauset goodness-of-fit result."""

    observed_fit: DistributionFit
    p_value: float
    exceedances: int
    replicates: int
    monte_carlo_standard_error: float
    synthetic_xmins: tuple[int, ...]
    synthetic_tail_counts: tuple[int, ...]
    synthetic_ks: tuple[float, ...]


@dataclass(frozen=True)
class CutoffLikelihoodRatioTest:
    """Parametric-bootstrap test for the cutoff nested at ``lambda=0``."""

    observed_likelihood_ratio: float
    p_value: float
    exceedances: int
    replicates: int
    monte_carlo_standard_error: float
    synthetic_likelihood_ratios: tuple[float, ...]


@dataclass(frozen=True)
class ParametricGoodnessOfFit:
    """Fixed-support parametric-bootstrap goodness-of-fit result."""

    observed_fit: DistributionFit
    p_value: float
    exceedances: int
    replicates: int
    monte_carlo_standard_error: float
    synthetic_ks: tuple[float, ...]


@dataclass(frozen=True)
class AvalancheCondition:
    """Validated fracture outputs for all fibrils at one ``Ts`` value."""

    ts: int
    files: tuple[ParsedAvalancheFile, ...]

    @property
    def fibril_seeds(self) -> tuple[int, ...]:
        return tuple(item.fibril_seed for item in self.files)

    @property
    def width(self) -> int:
        return max(item.preterminal_counts.shape[1] for item in self.files)

    def _file_matrix(
        self, item: ParsedAvalancheFile, include_terminal: bool
    ) -> sparse.csr_matrix:
        matrix = item.preterminal_counts
        if include_terminal:
            matrix = matrix + item.terminal_counts
        missing = self.width - matrix.shape[1]
        if missing:
            matrix = sparse.hstack(
                [matrix, sparse.csr_matrix((matrix.shape[0], missing), dtype=np.int64)],
                format="csr",
            )
        return matrix

    def run_counts(self, *, include_terminal: bool = False) -> sparse.csr_matrix:
        return sparse.vstack(
            [self._file_matrix(item, include_terminal) for item in self.files],
            format="csr",
        )

    def fibril_counts(self, *, include_terminal: bool = False) -> np.ndarray:
        rows = []
        for item in self.files:
            matrix = self._file_matrix(item, include_terminal)
            rows.append(np.asarray(matrix.sum(axis=0)).ravel())
        return np.asarray(rows, dtype=np.int64)

    def aggregate_counts(self, *, include_terminal: bool = False) -> np.ndarray:
        return self.fibril_counts(include_terminal=include_terminal).sum(axis=0)


def _parse_sizes(value: str) -> tuple[int, ...]:
    value = value.strip()
    if _SIZE_FIELD.fullmatch(value) is None:
        raise ValueError(f"malformed avalanche_sizes field: {value!r}")
    if value == "0":
        return ()
    return tuple(int(part) for part in value.split("-"))


def _rows_to_csr(rows: list[Counter[int]], width: int) -> sparse.csr_matrix:
    row_indices: list[int] = []
    column_indices: list[int] = []
    values: list[int] = []
    for row_index, counts in enumerate(rows):
        for size, count in counts.items():
            row_indices.append(row_index)
            column_indices.append(size)
            values.append(count)
    return sparse.csr_matrix(
        (values, (row_indices, column_indices)),
        shape=(len(rows), width),
        dtype=np.int64,
    )


def parse_avalanche_file(
    path: str | Path, *, expected_runs: int | None = None
) -> ParsedAvalancheFile:
    """Parse one fracture-output file without flattening its independent runs."""

    source = Path(path)
    match = _FILE_NAME.match(source.name)
    if match is None:
        raise ValueError(f"unrecognized avalanche filename: {source.name}")

    run_ids = [0]
    preterminal_rows: list[Counter[int]] = [Counter()]
    terminal_rows: list[Counter[int]] = [Counter()]
    maximum_size = 0
    header_seen = False
    run_has_rows = False
    terminal_seen = False
    initial_particles: int | None = None
    previous_force: float | None = None
    previous_active: int | None = None
    previous_deleted: int | None = None

    with source.open(newline="", encoding="utf-8") as stream:
        for line_number, raw_line in enumerate(stream, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            if stripped == _HEADER:
                if header_seen:
                    raise ValueError(f"{source}:{line_number}: repeated header")
                if run_has_rows or line_number != 1:
                    raise ValueError(f"{source}:{line_number}: misplaced header")
                header_seen = True
                continue
            if not header_seen:
                raise ValueError(f"{source}:{line_number}: missing or invalid header")

            separator = _RUN_SEPARATOR.match(stripped)
            if separator is not None:
                next_run_id = int(separator.group("run_id"))
                expected_run_id = run_ids[-1] + 1
                if next_run_id != expected_run_id:
                    raise ValueError(
                        f"{source}:{line_number}: expected run separator "
                        f"{expected_run_id}, found {next_run_id}"
                    )
                if not run_has_rows or not terminal_seen:
                    raise ValueError(
                        f"{source}:{line_number}: separator starts before run "
                        f"{run_ids[-1]} has a terminal row"
                    )
                run_ids.append(next_run_id)
                preterminal_rows.append(Counter())
                terminal_rows.append(Counter())
                run_has_rows = False
                terminal_seen = False
                previous_force = None
                previous_active = None
                previous_deleted = None
                continue

            if terminal_seen:
                raise ValueError(
                    f"{source}:{line_number}: data found after terminal row in "
                    f"run {run_ids[-1]}"
                )
            try:
                fields = next(csv.reader([raw_line], strict=True))
            except csv.Error as error:
                raise ValueError(f"{source}:{line_number}: invalid CSV: {error}") from error
            if len(fields) != 5:
                raise ValueError(f"{source}:{line_number}: expected five CSV fields")
            try:
                force = float(fields[0])
                active_particles = int(fields[1])
                deleted_particles = int(fields[2])
                total_deleted_rods = int(fields[3])
                sizes = _parse_sizes(fields[4])
            except ValueError as error:
                raise ValueError(f"{source}:{line_number}: {error}") from error
            if not np.isfinite(force) or force < 0:
                raise ValueError(f"{source}:{line_number}: invalid force {force}")
            if min(active_particles, deleted_particles, total_deleted_rods) < 0:
                raise ValueError(f"{source}:{line_number}: negative count")

            if not run_has_rows:
                if (
                    not np.isclose(force, 0.0, rtol=0.0, atol=1e-12)
                    or deleted_particles != 0
                    or total_deleted_rods != 0
                    or sizes
                    or active_particles <= 0
                ):
                    raise ValueError(
                        f"{source}:{line_number}: invalid initial state for run "
                        f"{run_ids[-1]}"
                    )
                if initial_particles is None:
                    initial_particles = active_particles
                elif active_particles != initial_particles:
                    raise ValueError(
                        f"{source}:{line_number}: initial particle count changed "
                        f"from {initial_particles} to {active_particles}"
                    )
            else:
                assert previous_force is not None
                assert previous_active is not None
                assert previous_deleted is not None
                if not np.isclose(force, previous_force + 0.5, rtol=0.0, atol=1e-12):
                    raise ValueError(
                        f"{source}:{line_number}: force does not advance by 0.5"
                    )
                if active_particles > previous_active:
                    raise ValueError(
                        f"{source}:{line_number}: active particle count increased"
                    )
                if deleted_particles < previous_deleted:
                    raise ValueError(
                        f"{source}:{line_number}: deleted particle count decreased"
                    )

            assert initial_particles is not None
            if active_particles + deleted_particles != initial_particles:
                raise ValueError(
                    f"{source}:{line_number}: active and deleted particles do not "
                    "sum to the initial count"
                )
            if sum(sizes) != total_deleted_rods:
                raise ValueError(
                    f"{source}:{line_number}: cluster-size sum {sum(sizes)} "
                    f"does not equal total_deleted_rods {total_deleted_rods}"
                )
            if sizes:
                maximum_size = max(maximum_size, max(sizes))
                target = terminal_rows[-1] if active_particles == 0 else preterminal_rows[-1]
                target.update(sizes)
            run_has_rows = True
            terminal_seen = active_particles == 0
            previous_force = force
            previous_active = active_particles
            previous_deleted = deleted_particles

    if not header_seen:
        raise ValueError(f"{source}: missing header")
    if not run_has_rows or not terminal_seen:
        raise ValueError(f"{source}: final run is empty or lacks a terminal row")

    if expected_runs is not None and len(run_ids) != expected_runs:
        raise ValueError(
            f"{source}: expected {expected_runs} runs, found {len(run_ids)}"
        )

    width = maximum_size + 1
    with source.open("rb") as binary_stream:
        source_sha256 = hashlib.file_digest(binary_stream, "sha256").hexdigest()
    assert initial_particles is not None
    return ParsedAvalancheFile(
        source=source,
        ts=int(match.group("ts")),
        fibril_seed=int(match.group("seed")),
        weibull_m=int(match.group("m")),
        initial_particles=initial_particles,
        source_bytes=source.stat().st_size,
        source_sha256=source_sha256,
        run_ids=tuple(run_ids),
        preterminal_counts=_rows_to_csr(preterminal_rows, width),
        terminal_counts=_rows_to_csr(terminal_rows, width),
    )


def load_avalanche_condition(
    directory: str | Path,
    *,
    ts: int,
    expected_fibrils: int | None = 50,
    expected_runs: int | None = 1_000,
) -> AvalancheCondition:
    """Load and validate every raw ``.txt`` output for one condition."""

    root = Path(directory)
    paths = sorted(root.glob("*.txt"))
    if expected_fibrils is not None and len(paths) != expected_fibrils:
        raise ValueError(
            f"{root}: expected {expected_fibrils} fibril files, found {len(paths)}"
        )
    parsed = [parse_avalanche_file(path, expected_runs=expected_runs) for path in paths]
    if any(item.ts != ts for item in parsed):
        raise ValueError(f"{root}: contains a file with Ts different from {ts}")
    seeds = [item.fibril_seed for item in parsed]
    if len(set(seeds)) != len(seeds):
        raise ValueError(f"{root}: duplicate fibril seed")
    weibull_values = {item.weibull_m for item in parsed}
    if len(weibull_values) > 1:
        raise ValueError(f"{root}: mixed Weibull moduli")
    return AvalancheCondition(ts=ts, files=tuple(sorted(parsed, key=lambda item: item.fibril_seed)))


def avalanche_parser_signature() -> str:
    """Hash the source section that defines raw-data parsing and aggregation."""

    parts = (
        "avalanche-parser-schema-v2",
        _FILE_NAME.pattern,
        _RUN_SEPARATOR.pattern,
        _SIZE_FIELD.pattern,
        _HEADER,
        inspect.getsource(ParsedAvalancheFile),
        inspect.getsource(AvalancheCondition),
        inspect.getsource(_parse_sizes),
        inspect.getsource(_rows_to_csr),
        inspect.getsource(parse_avalanche_file),
        inspect.getsource(load_avalanche_condition),
    )
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


HistogramLike = np.ndarray | Mapping[int, int | float]


def _as_count_vector(counts: np.ndarray) -> np.ndarray:
    vector = np.asarray(counts, dtype=float)
    if vector.ndim != 1 or vector.size < 2:
        raise ValueError("counts must be a one-dimensional size-indexed vector")
    if not np.all(np.isfinite(vector)) or np.any(vector < 0):
        raise ValueError("counts must be finite and nonnegative")
    return vector


def _histogram_arrays(counts: HistogramLike) -> tuple[np.ndarray, np.ndarray]:
    if isinstance(counts, Mapping):
        items = sorted((int(size), float(count)) for size, count in counts.items() if count)
        if not items:
            raise ValueError("histogram contains no observations")
        sizes = np.asarray([item[0] for item in items], dtype=np.int64)
        frequencies = np.asarray([item[1] for item in items], dtype=float)
        if np.any(sizes < 1) or len(np.unique(sizes)) != len(sizes):
            raise ValueError("histogram sizes must be distinct positive integers")
        if np.any(frequencies < 0) or not np.all(np.isfinite(frequencies)):
            raise ValueError("histogram counts must be finite and nonnegative")
        return sizes, frequencies
    vector = _as_count_vector(np.asarray(counts))
    sizes = np.flatnonzero(vector > 0).astype(np.int64)
    if sizes.size == 0:
        raise ValueError("histogram contains no observations")
    return sizes, vector[sizes]


def _discrete_ks(
    sizes: np.ndarray,
    frequencies: np.ndarray,
    model_cdf,
) -> float:
    """KS distance including the empty integer gaps between observed sizes."""

    n = float(frequencies.sum())
    cumulative = np.cumsum(frequencies) / n
    after = np.abs(cumulative - model_cdf(sizes))
    before_empirical = (np.cumsum(frequencies) - frequencies) / n
    before = np.abs(before_empirical - model_cdf(sizes - 1))
    return float(max(np.max(after), np.max(before)))


def fit_discrete_power_law(
    counts: HistogramLike, *, xmin: int, compute_ks: bool = True
) -> DistributionFit:
    """Fit ``p(s) = s**(-gamma) / zeta(gamma, xmin)`` by exact MLE."""

    all_sizes, all_frequencies = _histogram_arrays(counts)
    if xmin < 1:
        raise ValueError("xmin must be positive")
    start = int(np.searchsorted(all_sizes, xmin))
    return _fit_power_law_arrays(
        all_sizes, all_frequencies, start, xmin, compute_ks=compute_ks
    )


def _fit_power_law_arrays(
    all_sizes: np.ndarray,
    all_frequencies: np.ndarray,
    start: int,
    xmin: int,
    *,
    n: float | None = None,
    sum_log_sizes: float | None = None,
    compute_ks: bool = True,
) -> DistributionFit:
    sizes = all_sizes[start:].astype(float, copy=False)
    frequencies = all_frequencies[start:]
    if n is None:
        n = float(frequencies.sum())
    else:
        n = float(n)
    if n <= 0:
        raise ValueError("no observations at or above xmin")
    if sum_log_sizes is None:
        sum_log_sizes = float(np.dot(frequencies, np.log(sizes)))

    def negative_log_likelihood(gamma: float) -> float:
        normalization = special.zeta(gamma, float(xmin))
        if not np.isfinite(normalization) or normalization <= 0:
            return np.inf
        return n * np.log(normalization) + gamma * sum_log_sizes

    result = optimize.minimize_scalar(
        negative_log_likelihood,
        method="bounded",
        bounds=(1.0 + 1e-10, 50.0),
        options={"xatol": 1e-13, "maxiter": 1000},
    )
    if not result.success or not np.isfinite(result.fun):
        raise RuntimeError(f"power-law optimization failed: {result.message}")
    gamma = float(result.x)

    def model_cdf(values: np.ndarray) -> np.ndarray:
        values = np.asarray(values, dtype=float)
        result = 1.0 - special.zeta(gamma, values + 1.0) / special.zeta(
            gamma, float(xmin)
        )
        return np.where(values < xmin, 0.0, result)

    ks = (
        _discrete_ks(sizes.astype(np.int64), frequencies, model_cdf)
        if compute_ks
        else float("nan")
    )
    return DistributionFit(
        model="power_law",
        xmin=xmin,
        parameters={"gamma": gamma},
        log_likelihood=-float(result.fun),
        ks=ks,
        n=n,
    )


def select_power_law_xmin(
    counts: HistogramLike,
    *,
    xmin_min: int = 2,
    min_tail: int = 1_000,
    fibril_counts: np.ndarray | None = None,
    min_fibrils: int = 0,
) -> DistributionFit:
    """Select the observed integer ``xmin`` that minimizes the discrete KS."""

    sizes, frequencies = _histogram_arrays(counts)
    if xmin_min < 1:
        raise ValueError("xmin_min must be positive")
    if min_tail < 1:
        raise ValueError("min_tail must be positive")
    by_fibril: np.ndarray | None = None
    if fibril_counts is not None:
        by_fibril = np.asarray(fibril_counts, dtype=float)
        if by_fibril.ndim != 2:
            raise ValueError("fibril_counts must be a matrix")
        if sizes[-1] >= by_fibril.shape[1]:
            raise ValueError("fibril_counts must span the aggregate histogram")
        if np.any(by_fibril < 0) or not np.all(np.isfinite(by_fibril)):
            raise ValueError("fibril_counts must be finite and nonnegative")

    tail_counts = np.cumsum(frequencies[::-1])[::-1]
    tail_log_sums = np.cumsum(
        (frequencies * np.log(sizes))[::-1]
    )[::-1]
    eligible = sizes >= xmin_min
    candidate_indices = np.flatnonzero(eligible)
    allowed_indices: list[int] = []
    for candidate_index in candidate_indices:
        candidate = int(sizes[candidate_index])
        tail_count = float(tail_counts[candidate_index])
        if tail_count < min_tail:
            continue
        if by_fibril is not None and min_fibrils:
            contributors = int(np.count_nonzero(by_fibril[:, candidate:].sum(axis=1)))
            if contributors < min_fibrils:
                continue
        allowed_indices.append(int(candidate_index))
    if not allowed_indices:
        raise ValueError("no xmin candidate satisfies the tail constraints")

    # Heavy-tailed synthetic samples can contain thousands of distinct candidate
    # cutoffs.  Screen those candidates on exact MLEs and a dense set of tail
    # quantiles, then recompute the complete discrete KS for every finalist.
    # Small empirical supports continue to use exhaustive evaluation.
    screened_ks: np.ndarray | None = None
    if len(allowed_indices) > 256:
        screened_ks = _screen_power_law_candidates(
            sizes,
            frequencies,
            tail_counts,
            tail_log_sums,
            np.asarray(allowed_indices, dtype=np.int64),
        )
        ranked = np.argsort(screened_ks)[:128]
        finalist_positions = set(range(min(64, len(allowed_indices))))
        for position in ranked:
            for neighbor in (int(position) - 1, int(position), int(position) + 1):
                if 0 <= neighbor < len(allowed_indices):
                    finalist_positions.add(neighbor)
        evaluation_indices = [allowed_indices[position] for position in finalist_positions]
    else:
        evaluation_indices = allowed_indices

    fits: list[DistributionFit] = []
    for candidate_index in evaluation_indices:
        candidate = int(sizes[candidate_index])
        tail_count = float(tail_counts[candidate_index])
        fits.append(
            _fit_power_law_arrays(
                sizes,
                frequencies,
                int(candidate_index),
                int(candidate),
                n=float(tail_count),
                sum_log_sizes=float(tail_log_sums[candidate_index]),
            )
        )
    if screened_ks is not None:
        incumbent = min(fits, key=lambda fit: (fit.ks, fit.xmin))
        # The screen evaluates a subset of CDF points, so it is a lower bound
        # on the complete KS at its numerically optimized gamma.  The 5e-4
        # guard is over three orders of magnitude larger than the observed
        # CDF change from the batch-MLE numerical error.  Evaluate every
        # candidate whose lower bound could therefore beat the incumbent.
        certified_positions = np.flatnonzero(screened_ks <= incumbent.ks + 5e-4)
        already_evaluated = set(evaluation_indices)
        for position in certified_positions:
            candidate_index = allowed_indices[int(position)]
            if candidate_index in already_evaluated:
                continue
            candidate = int(sizes[candidate_index])
            fits.append(
                _fit_power_law_arrays(
                    sizes,
                    frequencies,
                    candidate_index,
                    candidate,
                    n=float(tail_counts[candidate_index]),
                    sum_log_sizes=float(tail_log_sums[candidate_index]),
                )
            )
    return min(fits, key=lambda fit: (fit.ks, fit.xmin))


def _screen_power_law_candidates(
    sizes: np.ndarray,
    frequencies: np.ndarray,
    tail_counts: np.ndarray,
    tail_log_sums: np.ndarray,
    candidate_indices: np.ndarray,
) -> np.ndarray:
    """Fast candidate screen; finalists are always recomputed exhaustively."""

    xmins = sizes[candidate_indices].astype(float)
    n = tail_counts[candidate_indices]
    mean_log = tail_log_sums[candidate_indices] / n
    denominator = tail_log_sums[candidate_indices] - n * np.log(xmins - 0.5)
    gamma = 1.0 + n / denominator
    for _ in range(12):
        step = 1e-4 * np.maximum(1.0, gamma)
        log_zeta = np.log(special.zeta(gamma, xmins))
        log_zeta_plus = np.log(special.zeta(gamma + step, xmins))
        log_zeta_minus = np.log(special.zeta(gamma - step, xmins))
        model_mean_log = -(log_zeta_plus - log_zeta_minus) / (2.0 * step)
        model_variance_log = (
            log_zeta_plus - 2.0 * log_zeta + log_zeta_minus
        ) / step**2
        update = (model_mean_log - mean_log) / model_variance_log
        gamma = np.maximum(1.0 + 1e-9, gamma + update)
        if float(np.max(np.abs(update))) < 1e-9:
            break

    cumulative = np.cumsum(frequencies)
    previous = np.where(
        candidate_indices > 0, cumulative[candidate_indices - 1], 0.0
    )
    quantiles = np.linspace(0.0, 1.0, 65)
    targets = previous[:, None] + n[:, None] * quantiles[None, :]
    quantile_indices = np.searchsorted(cumulative, targets.ravel()).reshape(targets.shape)
    quantile_indices = np.maximum(quantile_indices, candidate_indices[:, None])
    quantile_indices = np.minimum(quantile_indices, len(sizes) - 1)
    first_indices = np.minimum(
        candidate_indices[:, None] + np.arange(32)[None, :], len(sizes) - 1
    )
    evaluation_indices = np.concatenate((first_indices, quantile_indices), axis=1)
    evaluation_sizes = sizes[evaluation_indices]
    empirical_after = (
        cumulative[evaluation_indices] - previous[:, None]
    ) / n[:, None]
    empirical_before = (
        cumulative[evaluation_indices]
        - frequencies[evaluation_indices]
        - previous[:, None]
    ) / n[:, None]
    normalization = special.zeta(gamma, xmins)
    model_after = 1.0 - special.zeta(
        gamma[:, None], evaluation_sizes + 1.0
    ) / normalization[:, None]
    model_before = 1.0 - special.zeta(
        gamma[:, None], evaluation_sizes
    ) / normalization[:, None]
    return np.maximum(
        np.max(np.abs(empirical_after - model_after), axis=1),
        np.max(np.abs(empirical_before - model_before), axis=1),
    )


def sample_discrete_power_law_counts(
    n: int,
    *,
    gamma: float,
    xmin: int,
    rng: np.random.Generator,
) -> dict[int, int]:
    """Sample an exact Hurwitz power law directly as a sparse histogram."""

    if n < 0:
        raise ValueError("n must be nonnegative")
    if gamma <= 1.0 or xmin < 1:
        raise ValueError("the discrete power law requires gamma > 1 and xmin >= 1")
    result: Counter[int] = Counter()

    def split_finite(lower: int, upper: int, count: int) -> None:
        if count == 0:
            return
        if lower == upper:
            result[lower] += count
            return
        midpoint = (lower + upper) // 2
        total_mass = special.zeta(gamma, float(lower)) - special.zeta(
            gamma, float(upper + 1)
        )
        left_mass = special.zeta(gamma, float(lower)) - special.zeta(
            gamma, float(midpoint + 1)
        )
        probability = float(np.clip(left_mass / total_mass, 0.0, 1.0))
        left_count = int(rng.binomial(count, probability))
        split_finite(lower, midpoint, left_count)
        split_finite(midpoint + 1, upper, count - left_count)

    lower = int(xmin)
    remaining = int(n)
    while remaining:
        tail_ratio = special.zeta(gamma, float(2 * lower)) / special.zeta(
            gamma, float(lower)
        )
        block_probability = float(np.clip(1.0 - tail_ratio, 0.0, 1.0))
        block_count = int(rng.binomial(remaining, block_probability))
        split_finite(lower, 2 * lower - 1, block_count)
        remaining -= block_count
        lower *= 2
        if lower.bit_length() > 1024:
            raise RuntimeError("power-law sampler failed to terminate")
    return dict(sorted(result.items()))


def _sample_semiparametric_power_law(
    counts: HistogramLike,
    fit: DistributionFit,
    *,
    xmin_min: int,
    rng: np.random.Generator,
) -> dict[int, int]:
    sizes, frequencies = _histogram_arrays(counts)
    if not np.allclose(frequencies, np.rint(frequencies), rtol=0.0, atol=1e-9):
        raise ValueError("Clauset bootstrap requires integer event counts")
    selected = sizes >= xmin_min
    sizes = sizes[selected]
    frequencies = np.rint(frequencies[selected]).astype(np.int64)
    total = int(frequencies.sum())
    observed_tail = int(frequencies[sizes >= fit.xmin].sum())
    synthetic_tail = int(rng.binomial(total, observed_tail / total))
    synthetic_body = total - synthetic_tail

    result: Counter[int] = Counter()
    body_mask = sizes < fit.xmin
    if synthetic_body:
        body_frequencies = frequencies[body_mask]
        if body_frequencies.sum() == 0:
            raise RuntimeError("semiparametric body is empty but received observations")
        allocations = rng.multinomial(
            synthetic_body, body_frequencies / body_frequencies.sum()
        )
        result.update(
            {
                int(size): int(count)
                for size, count in zip(sizes[body_mask], allocations, strict=True)
                if count
            }
        )
    result.update(
        sample_discrete_power_law_counts(
            synthetic_tail,
            gamma=fit.parameters["gamma"],
            xmin=fit.xmin,
            rng=rng,
        )
    )
    return dict(sorted(result.items()))


def clauset_power_law_gof(
    counts: HistogramLike,
    *,
    xmin_min: int = 2,
    min_tail: int = 1_000,
    replicates: int = 2_500,
    seed: int = 12_738,
    fibril_counts: np.ndarray | None = None,
    min_fibrils: int = 0,
    workers: int = 1,
) -> PowerLawGoodnessOfFit:
    """Run the semiparametric discrete goodness-of-fit test of Clauset et al."""

    if replicates < 1:
        raise ValueError("replicates must be positive")
    observed = select_power_law_xmin(
        counts,
        xmin_min=xmin_min,
        min_tail=min_tail,
        fibril_counts=fibril_counts,
        min_fibrils=min_fibrils,
    )
    if workers < 1:
        raise ValueError("workers must be positive")
    sizes, frequencies = _histogram_arrays(counts)
    integer_histogram = {
        int(size): int(round(frequency))
        for size, frequency in zip(sizes, frequencies, strict=True)
        if frequency
    }
    child_seeds = np.random.SeedSequence(seed).spawn(replicates)
    arguments = [
        (integer_histogram, observed, xmin_min, min_tail, child_seed)
        for child_seed in child_seeds
    ]
    if workers == 1:
        synthetic_fits = [_clauset_gof_replica(argument) for argument in arguments]
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            synthetic_fits = list(
                executor.map(
                    _clauset_gof_replica,
                    arguments,
                    chunksize=max(1, replicates // (workers * 16)),
                )
            )
    exceedances = sum(fit.ks >= observed.ks for fit in synthetic_fits)
    p_value = (exceedances + 1.0) / (replicates + 1.0)
    standard_error = float(np.sqrt(p_value * (1.0 - p_value) / replicates))
    return PowerLawGoodnessOfFit(
        observed_fit=observed,
        p_value=p_value,
        exceedances=exceedances,
        replicates=replicates,
        monte_carlo_standard_error=standard_error,
        synthetic_xmins=tuple(fit.xmin for fit in synthetic_fits),
        synthetic_tail_counts=tuple(int(fit.n) for fit in synthetic_fits),
        synthetic_ks=tuple(fit.ks for fit in synthetic_fits),
    )


def _clauset_gof_replica(arguments) -> DistributionFit:
    counts, observed, xmin_min, min_tail, seed = arguments
    rng = np.random.default_rng(seed)
    synthetic = _sample_semiparametric_power_law(
        counts, observed, xmin_min=xmin_min, rng=rng
    )
    return select_power_law_xmin(
        synthetic,
        xmin_min=xmin_min,
        min_tail=min_tail,
    )


def hierarchical_resample_counts(
    run_counts_by_fibril: Sequence[sparse.csr_matrix],
    *,
    rng: np.random.Generator,
) -> np.ndarray:
    """Resample fibrils, then complete rupture runs within each selected fibril."""

    return hierarchical_resample_fibril_counts(
        run_counts_by_fibril, rng=rng
    ).sum(axis=0)


def hierarchical_resample_fibril_counts(
    run_counts_by_fibril: Sequence[sparse.csr_matrix],
    *,
    rng: np.random.Generator,
) -> np.ndarray:
    """Return one histogram row for each resampled fibril block."""

    if not run_counts_by_fibril:
        raise ValueError("at least one fibril is required")
    matrices = [sparse.csr_matrix(matrix) for matrix in run_counts_by_fibril]
    if any(matrix.shape[0] == 0 for matrix in matrices):
        raise ValueError("every fibril must contain at least one run")
    width = max(matrix.shape[1] for matrix in matrices)
    sampled_rows = np.zeros((len(matrices), width), dtype=np.int64)
    selected_fibrils = rng.integers(0, len(matrices), size=len(matrices))
    for row_index, fibril_index in enumerate(selected_fibrils):
        matrix = matrices[int(fibril_index)]
        run_weights = rng.multinomial(
            matrix.shape[0],
            np.full(matrix.shape[0], 1.0 / matrix.shape[0]),
        )
        sampled = np.asarray(run_weights @ matrix).ravel().astype(np.int64)
        sampled_rows[row_index, : matrix.shape[1]] = sampled
    return sampled_rows


def equal_fibril_weight_counts(
    fibril_counts: np.ndarray, *, min_size: int = 2
) -> np.ndarray:
    """Build a weighted histogram with identical total weight for each fibril."""

    matrix = np.asarray(fibril_counts, dtype=float)
    if matrix.ndim != 2 or min_size < 1 or min_size >= matrix.shape[1]:
        raise ValueError("invalid fibril count matrix or minimum size")
    selected = matrix.copy()
    selected[:, :min_size] = 0.0
    totals = selected.sum(axis=1)
    if np.any(totals <= 0):
        raise ValueError("each fibril must contribute at least one selected event")
    target_total = float(totals.sum() / len(totals))
    return (selected / totals[:, None] * target_total).sum(axis=0)


def fit_discrete_exponential(counts: HistogramLike, *, xmin: int) -> DistributionFit:
    """Fit the exact geometric distribution on integers ``s >= xmin``."""

    all_sizes, all_frequencies = _histogram_arrays(counts)
    if xmin < 1:
        raise ValueError("xmin must be positive")
    selected = all_sizes >= xmin
    integer_sizes = all_sizes[selected]
    sizes = integer_sizes.astype(float)
    frequencies = all_frequencies[selected]
    n = float(frequencies.sum())
    if n <= 0:
        raise ValueError("no observations at or above xmin")
    total_excess = float(np.dot(frequencies, sizes - xmin))
    if total_excess == 0:
        rate = np.inf
        log_likelihood = 0.0
        model_cdf = lambda values: np.where(np.asarray(values) < xmin, 0.0, 1.0)
    else:
        q = total_excess / (n + total_excess)
        rate = -float(np.log(q))
        log_likelihood = n * np.log1p(-q) + total_excess * np.log(q)
        model_cdf = lambda values: np.where(
            np.asarray(values) < xmin,
            0.0,
            1.0 - q ** (np.asarray(values) - xmin + 1.0),
        )
    return DistributionFit(
        model="exponential",
        xmin=xmin,
        parameters={"lambda": rate},
        log_likelihood=float(log_likelihood),
        ks=_discrete_ks(integer_sizes, frequencies, model_cdf),
        n=n,
    )


def _log_difference(log_larger: np.ndarray, log_smaller: np.ndarray) -> np.ndarray:
    ratio = np.exp(np.minimum(0.0, log_smaller - log_larger))
    return log_larger + np.log1p(-ratio)


def _log_normal_bin_mass(
    sizes: np.ndarray, mu: float, sigma: float
) -> np.ndarray:
    lower = (np.log(sizes - 0.5) - mu) / sigma
    upper = (np.log(sizes + 0.5) - mu) / sigma
    result = np.empty_like(sizes)
    left = upper <= 0
    right = lower >= 0
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
        mass = special.ndtr(upper[middle]) - special.ndtr(lower[middle])
        result[middle] = np.log(mass)
    return result


def fit_discrete_lognormal(counts: HistogramLike, *, xmin: int) -> DistributionFit:
    """Fit a rounded lognormal, conditioned on integer ``s >= xmin``."""

    all_sizes, all_frequencies = _histogram_arrays(counts)
    if xmin < 1:
        raise ValueError("xmin must be positive")
    selected = all_sizes >= xmin
    integer_sizes = all_sizes[selected]
    sizes = integer_sizes.astype(float)
    frequencies = all_frequencies[selected]
    n = float(frequencies.sum())
    if n <= 0:
        raise ValueError("no observations at or above xmin")
    log_sizes = np.log(sizes)
    initial_mu = float(np.dot(frequencies, log_sizes) / n)
    initial_variance = float(np.dot(frequencies, (log_sizes - initial_mu) ** 2) / n)
    initial_sigma = max(np.sqrt(initial_variance), 0.1)

    def unpack(parameters: np.ndarray) -> tuple[float, float, float]:
        gamma_like, log_curvature = map(float, parameters)
        curvature = float(np.exp(log_curvature))
        sigma = float(1.0 / np.sqrt(2.0 * curvature))
        mu = float((1.0 - gamma_like) / (2.0 * curvature))
        return mu, sigma, curvature

    def negative_log_likelihood(parameters: np.ndarray) -> float:
        mu, sigma, _ = unpack(parameters)
        log_mass = _log_normal_bin_mass(sizes, float(mu), sigma)
        boundary = (np.log(xmin - 0.5) - mu) / sigma
        log_normalizer = special.log_ndtr(-boundary)
        value = -float(np.dot(frequencies, log_mass - log_normalizer)) / n
        return value if np.isfinite(value) else np.inf

    initial_curvature = 1.0 / (2.0 * initial_sigma**2)
    initial_gamma_like = 1.0 - initial_mu / initial_sigma**2
    try:
        power_gamma = fit_discrete_power_law(counts, xmin=xmin).parameters["gamma"]
    except (ValueError, RuntimeError):
        power_gamma = max(initial_gamma_like, 1.01)
    starts = (
        np.array([initial_gamma_like, np.log(initial_curvature)]),
        np.array([power_gamma, np.log(0.01)]),
        np.array([power_gamma, np.log(1e-4)]),
        np.array([max(0.1, power_gamma - 0.5), np.log(0.1)]),
    )
    log_curvature_lower = np.log(1e-8)
    results = [
        optimize.minimize(
            negative_log_likelihood,
            start,
            method="L-BFGS-B",
            bounds=((-50.0, 50.0), (log_curvature_lower, np.log(1_250.0))),
            options={"ftol": 1e-12, "gtol": 1e-8, "maxiter": 1000},
        )
        for start in starts
    ]
    valid_transformed_results = [
        item for item in results if item.success and np.isfinite(item.fun)
    ]
    transformed_result = (
        min(valid_transformed_results, key=lambda item: item.fun)
        if valid_transformed_results
        else None
    )

    def direct_negative_log_likelihood(parameters: np.ndarray) -> float:
        mu = float(parameters[0])
        sigma = float(np.exp(parameters[1]))
        log_mass = _log_normal_bin_mass(sizes, mu, sigma)
        boundary = (np.log(xmin - 0.5) - mu) / sigma
        value = -float(
            np.dot(frequencies, log_mass - special.log_ndtr(-boundary))
        ) / n
        return value if np.isfinite(value) else np.inf

    direct_starts = (
        np.array([initial_mu, np.log(initial_sigma)]),
        np.array([np.log(float(xmin)), np.log(0.25)]),
        np.array([np.log(float(xmin)), np.log(1.0)]),
        np.array([np.log(float(np.average(sizes, weights=frequencies))), np.log(0.1)]),
    )
    direct_results = [
        optimize.minimize(
            direct_negative_log_likelihood,
            start,
            method="L-BFGS-B",
            bounds=((-100.0, 50.0), (np.log(0.005), np.log(100.0))),
            options={"ftol": 1e-12, "gtol": 1e-8, "maxiter": 1000},
        )
        for start in direct_starts
    ]
    valid_direct_results = [
        item for item in direct_results if item.success and np.isfinite(item.fun)
    ]
    direct_result = (
        min(valid_direct_results, key=lambda item: item.fun)
        if valid_direct_results
        else None
    )
    if transformed_result is None and direct_result is None:
        messages = "; ".join(
            str(item.message) for item in (*results, *direct_results)
        )
        raise RuntimeError(f"lognormal optimization failed: {messages}")
    if direct_result is not None and (
        transformed_result is None or direct_result.fun < transformed_result.fun
    ):
        result = direct_result
        mu = float(result.x[0])
        sigma = float(np.exp(result.x[1]))
        curvature = 1.0 / (2.0 * sigma**2)
        gamma_like = 1.0 - mu / sigma**2
        parameterization = "mu_sigma"
    else:
        result = transformed_result
        mu, sigma, curvature = unpack(result.x)
        gamma_like = float(result.x[0])
        parameterization = "gamma_curvature"
    boundary = (np.log(xmin - 0.5) - mu) / sigma
    log_normalizer = special.log_ndtr(-boundary)

    def model_cdf(values: np.ndarray) -> np.ndarray:
        values = np.asarray(values, dtype=float)
        safe_values = np.maximum(values, xmin)
        upper = (np.log(safe_values + 0.5) - mu) / sigma
        result = -np.expm1(special.log_ndtr(-upper) - log_normalizer)
        return np.where(values < xmin, 0.0, result)

    return DistributionFit(
        model="lognormal",
        xmin=xmin,
        parameters={"mu": mu, "sigma": sigma},
        log_likelihood=-float(result.fun) * n,
        ks=_discrete_ks(integer_sizes, frequencies, model_cdf),
        n=n,
        diagnostics={
            "lognormal_gamma_like": gamma_like,
            "lognormal_curvature": curvature,
            "lognormal_parameterization": parameterization,
            "boundary_solution": bool(
                (parameterization == "gamma_curvature" and curvature < 1e-6)
                or (
                    parameterization == "gamma_curvature"
                    and abs(gamma_like) > 49.999
                )
                or (parameterization == "mu_sigma" and sigma > 99.9)
                or (parameterization == "mu_sigma" and abs(mu) > 99.9)
            ),
        },
    )


def _cutoff_log_normalizer(gamma: float, rate: float, xmin: int) -> float:
    if rate <= 1e-12:
        if gamma <= 1.0:
            return np.inf
        return float(np.log(special.zeta(gamma, float(xmin))))

    if xmin <= 10 and gamma < 8.0 and rate < 2e-4:
        z = float(np.exp(-rate))
        polylogarithm = mpmath.fp.polylog(gamma, z)
        if isinstance(polylogarithm, complex):
            polylogarithm = polylogarithm.real
        prefix_support = np.arange(1, xmin, dtype=float)
        prefix = float(
            np.sum(prefix_support ** -gamma * np.exp(-rate * prefix_support))
        )
        normalization = float(polylogarithm) - prefix
        if normalization > 0.0 and np.isfinite(normalization):
            return float(np.log(normalization))

    # Direct scaled summation is fast in the regime where the cutoff matters.
    # Near the nested lambda=0 boundary, LerchPhi avoids an impractically long
    # truncation and cancellation from subtracting a polylogarithm prefix.
    span = int(np.ceil(40.0 / rate))
    if span <= 200_000:
        upper = xmin + max(64, span)
        support = np.arange(xmin, upper + 1, dtype=float)
        log_relative = -gamma * np.log(support / xmin) - rate * (support - xmin)
        relative_sum = float(np.exp(log_relative).sum())
        return -gamma * np.log(float(xmin)) - rate * xmin + np.log(relative_sum)

    with mpmath.workdps(40):
        z = mpmath.exp(-rate)
        normalization = z**xmin * mpmath.lerchphi(z, gamma, xmin)
        return float(mpmath.log(normalization))


def fit_cutoff_power_law(
    counts: HistogramLike, *, xmin: int, compute_ks: bool = True
) -> DistributionFit:
    """Fit ``p(s) proportional to s^-gamma exp(-lambda*s)`` exactly."""

    all_sizes, all_frequencies = _histogram_arrays(counts)
    if xmin < 1:
        raise ValueError("xmin must be positive")
    selected = all_sizes >= xmin
    integer_sizes = all_sizes[selected]
    sizes = integer_sizes.astype(float)
    frequencies = all_frequencies[selected]
    n = float(frequencies.sum())
    if n <= 0:
        raise ValueError("no observations at or above xmin")
    sum_log_sizes = float(np.dot(frequencies, np.log(sizes)))
    sum_sizes = float(np.dot(frequencies, sizes))

    def negative_log_likelihood(parameters: np.ndarray) -> float:
        gamma = float(parameters[0])
        rate = float(np.exp(parameters[1]))
        log_normalizer = _cutoff_log_normalizer(gamma, rate, xmin)
        value = n * log_normalizer + gamma * sum_log_sizes + rate * sum_sizes
        return value if np.isfinite(value) else np.inf

    power_law = fit_discrete_power_law(counts, xmin=xmin, compute_ks=compute_ks)
    power_gamma = power_law.parameters["gamma"]
    starts = (
        np.array([max(0.05, power_gamma - 0.5), np.log(0.01)]),
        np.array([max(0.05, power_gamma - 1.0), np.log(0.05)]),
        np.array([power_gamma, np.log(0.001)]),
    )
    results = [
        optimize.minimize(
            negative_log_likelihood,
            start,
            method="L-BFGS-B",
            bounds=((0.0, 50.0), (np.log(1e-10), np.log(10.0))),
            options={"ftol": 1e-12, "gtol": 1e-7, "maxiter": 500},
        )
        for start in starts
    ]
    valid_results = [item for item in results if item.success and np.isfinite(item.fun)]
    if not valid_results:
        raise RuntimeError("cutoff power-law optimization failed")
    result = min(valid_results, key=lambda item: item.fun)

    if power_law.log_likelihood >= -float(result.fun) - 1e-8:
        gamma = power_gamma
        rate = 0.0
        log_likelihood = power_law.log_likelihood
        model_cdf = lambda values: np.where(
            np.asarray(values) < xmin,
            0.0,
            1.0
            - special.zeta(gamma, np.asarray(values, dtype=float) + 1.0)
            / special.zeta(gamma, float(xmin)),
        )
    else:
        gamma = float(result.x[0])
        rate = float(np.exp(result.x[1]))
        log_likelihood = -float(result.fun)
        log_normalizer = _cutoff_log_normalizer(gamma, rate, xmin)

        def model_cdf(values: np.ndarray) -> np.ndarray:
            values = np.asarray(values, dtype=np.int64)
            result = np.zeros(values.shape, dtype=float)
            selected = values >= xmin
            if not np.any(selected):
                return result
            largest_needed = int(values[selected].max())
            numerical_cap = xmin + max(64, int(np.ceil(40.0 / rate)))
            upper = min(largest_needed, numerical_cap, 2_000_000)
            support = np.arange(xmin, upper + 1, dtype=float)
            probabilities = np.exp(
                -gamma * np.log(support) - rate * support - log_normalizer
            )
            cumulative = np.cumsum(probabilities)
            indices = np.minimum(values[selected], upper) - xmin
            result[selected] = cumulative[indices]
            return np.clip(result, 0.0, 1.0)

    return DistributionFit(
        model="cutoff_power_law",
        xmin=xmin,
        parameters={"gamma": gamma, "lambda": rate},
        log_likelihood=log_likelihood,
        ks=(
            _discrete_ks(integer_sizes, frequencies, model_cdf)
            if compute_ks
            else float("nan")
        ),
        n=n,
        diagnostics={"boundary_solution": bool(rate == 0.0)},
    )


def fit_stretched_exponential(counts: HistogramLike, *, xmin: int) -> DistributionFit:
    """Fit a rounded stretched exponential (Weibull) on integers ``s >= xmin``.

    Table 1 of Clauset, Shalizi and Newman (2009) lists four alternatives to the
    pure power law; this is the fourth.  The continuous survival function is
    ``S(x) = exp(-rate * x**beta)``, so the probability of the integer ``k`` is
    the mass of the bin ``[k - 1/2, k + 1/2]``, conditioned on the tail:

        P(k) = [S(k - 1/2) - S(k + 1/2)] / S(xmin - 1/2)

    The same half-integer binning as the lognormal fit is used, so the two
    alternatives are conditioned on an identical support and their likelihoods
    are directly comparable.  ``beta = 1`` recovers the exponential.
    """

    all_sizes, all_frequencies = _histogram_arrays(counts)
    if xmin < 1:
        raise ValueError("xmin must be positive")
    selected = all_sizes >= xmin
    integer_sizes = all_sizes[selected]
    sizes = integer_sizes.astype(float)
    frequencies = all_frequencies[selected]
    n = float(frequencies.sum())
    if n <= 0:
        raise ValueError("no observations at or above xmin")
    boundary = float(xmin) - 0.5

    def log_mass(values: np.ndarray, beta: float, rate: float) -> np.ndarray:
        lower = -rate * np.power(values - 0.5, beta)
        upper = -rate * np.power(values + 0.5, beta)
        return _log_difference(lower, upper)

    def negative_log_likelihood(parameters: np.ndarray) -> float:
        beta = float(np.exp(parameters[0]))
        rate = float(np.exp(parameters[1]))
        if not (np.isfinite(beta) and np.isfinite(rate)) or beta <= 0 or rate <= 0:
            return np.inf
        log_tail = -rate * boundary ** beta
        value = -float(np.dot(frequencies, log_mass(sizes, beta, rate))) + n * log_tail
        return value if np.isfinite(value) else np.inf

    # A moment start: beta near 1 (exponential) with the rate that matches the
    # observed mean excess, then a couple of stretched starts.
    mean_excess = max(float(np.dot(frequencies, sizes) / n) - boundary, 1e-3)
    starts = [
        np.array([0.0, np.log(1.0 / mean_excess)]),
        np.array([np.log(0.5), np.log(1.0 / np.sqrt(mean_excess))]),
        np.array([np.log(0.3), np.log(0.5)]),
    ]
    best = None
    for start in starts:
        result = optimize.minimize(
            negative_log_likelihood, start, method="Nelder-Mead",
            options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 4000})
        if best is None or result.fun < best.fun:
            best = result
    if best is None or not np.isfinite(best.fun):
        raise RuntimeError("stretched exponential optimization failed")

    beta = float(np.exp(best.x[0]))
    rate = float(np.exp(best.x[1]))
    log_tail = -rate * boundary ** beta

    def model_cdf(values):
        values = np.asarray(values, dtype=float)
        survival = -rate * np.power(np.maximum(values + 0.5, 0.5), beta)
        return np.where(values < xmin, 0.0, 1.0 - np.exp(survival - log_tail))

    return DistributionFit(
        model="stretched_exponential",
        xmin=xmin,
        parameters={"beta": beta, "lambda": rate},
        log_likelihood=float(-best.fun),
        ks=_discrete_ks(integer_sizes, frequencies, model_cdf),
        n=n,
    )


def vuong_likelihood_ratio(
    first: DistributionFit,
    second: DistributionFit,
    counts: HistogramLike,
) -> tuple[float, float, float]:
    """Normalized log-likelihood ratio for two NON-nested fits, and its p-value.

    Implements equation (C.6) of Clauset, Shalizi and Newman (2009): the
    per-observation log-likelihood differences have a standard deviation that
    sets the scale of the total, and the normalized ratio is asymptotically
    standard normal under the null that both models are equally close to the
    truth.  Returns ``(log_likelihood_ratio, normalized_ratio, p_value)``; a
    POSITIVE ratio favours ``first``.

    Do not call this for the power law against its own cutoff -- those are
    nested and the statistic is degenerate (Appendix C.1).
    """

    if first.xmin != second.xmin:
        raise ValueError("both fits must share xmin")
    sizes, frequencies = _histogram_arrays(counts)
    selected = sizes >= first.xmin
    sizes = sizes[selected]
    frequencies = frequencies[selected].astype(float)
    n = float(frequencies.sum())
    if n <= 0:
        raise ValueError("no observations at or above xmin")

    difference = (distribution_log_probabilities(first, sizes)
                  - distribution_log_probabilities(second, sizes))
    ratio = float(np.dot(frequencies, difference))
    mean = ratio / n
    variance = float(np.dot(frequencies, (difference - mean) ** 2) / n)
    if variance <= 0:
        return ratio, 0.0, 1.0
    normalized = ratio / np.sqrt(n * variance)
    p_value = float(special.erfc(abs(normalized) / np.sqrt(2.0)))
    return ratio, float(normalized), p_value


def fit_competing_models(
    counts: HistogramLike, *, xmin: int
) -> dict[str, DistributionFit]:
    """Fit every preregistered family to the identical integer tail."""

    fits = (
        fit_discrete_power_law(counts, xmin=xmin),
        fit_cutoff_power_law(counts, xmin=xmin),
        fit_discrete_lognormal(counts, xmin=xmin),
        fit_discrete_exponential(counts, xmin=xmin),
        fit_stretched_exponential(counts, xmin=xmin),
    )
    tail_sizes, tail_frequencies = _histogram_arrays(counts)
    expected_n = float(tail_frequencies[tail_sizes >= xmin].sum())
    if any(fit.xmin != xmin or not np.isclose(fit.n, expected_n) for fit in fits):
        raise RuntimeError("candidate models were not fitted on a common support")
    return {fit.model: fit for fit in fits}


def cutoff_power_law_likelihood_ratio_test(
    counts: HistogramLike,
    *,
    xmin: int,
    replicates: int = 2_500,
    seed: int = 12_738,
    workers: int = 1,
) -> CutoffLikelihoodRatioTest:
    """Calibrate pure-power-law versus cutoff LR under the fitted pure law."""

    if replicates < 1 or workers < 1:
        raise ValueError("replicates and workers must be positive")
    power_law = fit_discrete_power_law(counts, xmin=xmin, compute_ks=False)
    cutoff = fit_cutoff_power_law(counts, xmin=xmin, compute_ks=False)
    observed_lr = 2.0 * max(
        0.0, cutoff.log_likelihood - power_law.log_likelihood
    )
    n = int(round(power_law.n))
    child_seeds = np.random.SeedSequence(seed).spawn(replicates)
    arguments = [
        (n, power_law.parameters["gamma"], xmin, child_seed)
        for child_seed in child_seeds
    ]
    if workers == 1:
        synthetic_lrs = [_cutoff_lr_replica(argument) for argument in arguments]
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            synthetic_lrs = list(
                executor.map(
                    _cutoff_lr_replica,
                    arguments,
                    chunksize=max(1, replicates // (workers * 16)),
                )
            )
    exceedances = int(np.count_nonzero(np.asarray(synthetic_lrs) >= observed_lr))
    p_value = (exceedances + 1.0) / (replicates + 1.0)
    standard_error = float(np.sqrt(p_value * (1.0 - p_value) / replicates))
    return CutoffLikelihoodRatioTest(
        observed_likelihood_ratio=observed_lr,
        p_value=p_value,
        exceedances=exceedances,
        replicates=replicates,
        monte_carlo_standard_error=standard_error,
        synthetic_likelihood_ratios=tuple(synthetic_lrs),
    )


def _cutoff_lr_replica(arguments) -> float:
    n, gamma, xmin, seed = arguments
    rng = np.random.default_rng(seed)
    counts = sample_discrete_power_law_counts(n, gamma=gamma, xmin=xmin, rng=rng)
    power_law = fit_discrete_power_law(counts, xmin=xmin, compute_ks=False)
    cutoff = fit_cutoff_power_law(counts, xmin=xmin, compute_ks=False)
    return 2.0 * max(0.0, cutoff.log_likelihood - power_law.log_likelihood)


def distribution_log_probabilities(
    fit: DistributionFit, sizes: np.ndarray
) -> np.ndarray:
    """Evaluate a fitted discrete PMF on integer sizes."""

    values = np.asarray(sizes, dtype=float)
    if values.ndim != 1 or np.any(values != np.floor(values)):
        raise ValueError("sizes must be a one-dimensional integer array")
    result = np.full(values.shape, -np.inf, dtype=float)
    selected = values >= fit.xmin
    support = values[selected]
    if fit.model == "power_law":
        gamma = fit.parameters["gamma"]
        result[selected] = -gamma * np.log(support) - np.log(
            special.zeta(gamma, float(fit.xmin))
        )
    elif fit.model == "cutoff_power_law":
        gamma = fit.parameters["gamma"]
        rate = fit.parameters["lambda"]
        result[selected] = (
            -gamma * np.log(support)
            - rate * support
            - _cutoff_log_normalizer(gamma, rate, fit.xmin)
        )
    elif fit.model == "lognormal":
        mu = fit.parameters["mu"]
        sigma = fit.parameters["sigma"]
        boundary = (np.log(fit.xmin - 0.5) - mu) / sigma
        result[selected] = _log_normal_bin_mass(support, mu, sigma) - special.log_ndtr(
            -boundary
        )
    elif fit.model == "exponential":
        rate = fit.parameters["lambda"]
        if np.isinf(rate):
            result[selected] = np.where(support == fit.xmin, 0.0, -np.inf)
        else:
            result[selected] = np.log(-np.expm1(-rate)) - rate * (
                support - fit.xmin
            )
    elif fit.model == "stretched_exponential":
        beta = fit.parameters["beta"]
        rate = fit.parameters["lambda"]
        boundary = float(fit.xmin) - 0.5
        lower = -rate * np.power(support - 0.5, beta)
        upper = -rate * np.power(support + 0.5, beta)
        result[selected] = _log_difference(lower, upper) + rate * boundary ** beta
    else:
        raise ValueError(f"unsupported fitted model: {fit.model}")
    return result


def distribution_cdf(fit: DistributionFit, sizes: np.ndarray) -> np.ndarray:
    """Evaluate the fitted discrete CDF, conditioned on ``s >= xmin``."""

    values = np.asarray(sizes, dtype=np.int64)
    if values.ndim != 1:
        raise ValueError("sizes must be one-dimensional")
    result = np.zeros(values.shape, dtype=float)
    selected = values >= fit.xmin
    if not np.any(selected):
        return result
    support = values[selected]
    if fit.model == "power_law":
        gamma = fit.parameters["gamma"]
        result[selected] = 1.0 - special.zeta(gamma, support + 1.0) / special.zeta(
            gamma, float(fit.xmin)
        )
    elif fit.model == "exponential":
        rate = fit.parameters["lambda"]
        if np.isinf(rate):
            result[selected] = 1.0
        else:
            result[selected] = 1.0 - np.exp(-rate * (support - fit.xmin + 1))
    elif fit.model == "lognormal":
        mu = fit.parameters["mu"]
        sigma = fit.parameters["sigma"]
        boundary = (np.log(fit.xmin - 0.5) - mu) / sigma
        upper = (np.log(support + 0.5) - mu) / sigma
        result[selected] = -np.expm1(
            special.log_ndtr(-upper) - special.log_ndtr(-boundary)
        )
    elif fit.model == "cutoff_power_law":
        gamma = fit.parameters["gamma"]
        rate = fit.parameters["lambda"]
        if rate == 0.0:
            result[selected] = 1.0 - special.zeta(
                gamma, support + 1.0
            ) / special.zeta(gamma, float(fit.xmin))
        else:
            largest_needed = int(support.max())
            numerical_cap = fit.xmin + max(64, int(np.ceil(40.0 / rate)))
            upper = min(largest_needed, numerical_cap, 2_000_000)
            complete_support = np.arange(fit.xmin, upper + 1, dtype=float)
            log_normalizer = _cutoff_log_normalizer(gamma, rate, fit.xmin)
            cumulative = np.cumsum(
                np.exp(
                    -gamma * np.log(complete_support)
                    - rate * complete_support
                    - log_normalizer
                )
            )
            indices = np.minimum(support, upper) - fit.xmin
            result[selected] = cumulative[indices]
    elif fit.model == "stretched_exponential":
        beta = fit.parameters["beta"]
        rate = fit.parameters["lambda"]
        boundary = float(fit.xmin) - 0.5
        result[selected] = -np.expm1(
            -rate * np.power(support + 0.5, beta) + rate * boundary ** beta
        )
    else:
        raise ValueError(f"unsupported fitted model: {fit.model}")
    return np.clip(result, 0.0, 1.0)


def _samples_to_histogram(samples: np.ndarray) -> dict[int, int]:
    sizes, counts = np.unique(np.asarray(samples, dtype=np.int64), return_counts=True)
    return {
        int(size): int(count)
        for size, count in zip(sizes, counts, strict=True)
        if count
    }


def _sample_cutoff_power_law_counts(
    n: int, fit: DistributionFit, *, rng: np.random.Generator
) -> dict[int, int]:
    gamma = fit.parameters["gamma"]
    rate = fit.parameters["lambda"]
    if rate == 0.0:
        return sample_discrete_power_law_counts(
            n, gamma=gamma, xmin=fit.xmin, rng=rng
        )

    required_span = max(64, int(np.ceil(45.0 / rate)))
    if required_span > 2_000_000:
        if gamma <= 1.0:
            raise RuntimeError("cutoff sampler requires an impractically long support")
        accepted: Counter[int] = Counter()
        remaining = n
        while remaining:
            proposal = sample_discrete_power_law_counts(
                remaining, gamma=gamma, xmin=fit.xmin, rng=rng
            )
            for size, count in proposal.items():
                kept = int(
                    rng.binomial(
                        count,
                        np.exp(-rate * (size - fit.xmin)),
                    )
                )
                if kept:
                    accepted[size] += kept
                    remaining -= kept
        return dict(sorted(accepted.items()))

    upper = fit.xmin + required_span
    support = np.arange(fit.xmin, upper + 1, dtype=np.int64)
    probabilities = np.exp(distribution_log_probabilities(fit, support))
    finite_mass = float(probabilities.sum())
    if finite_mass > 1.0 + 1e-10:
        raise RuntimeError("cutoff sampler probabilities exceed one")
    tail_probability = max(0.0, 1.0 - finite_mass)
    probability_vector = np.append(probabilities, tail_probability)
    probability_vector /= probability_vector.sum()
    allocation = rng.multinomial(n, probability_vector)
    result = Counter(
        {
            int(size): int(count)
            for size, count in zip(support, allocation[:-1], strict=True)
            if count
        }
    )
    tail_count = int(allocation[-1])
    if tail_count:
        success_probability = -np.expm1(-rate)
        accepted_tail: list[int] = []
        while len(accepted_tail) < tail_count:
            needed = tail_count - len(accepted_tail)
            proposed = upper + rng.geometric(success_probability, size=needed * 2)
            acceptance = (proposed / float(upper + 1)) ** -gamma
            accepted_tail.extend(
                proposed[rng.random(proposed.size) < acceptance].tolist()
            )
        result.update(accepted_tail[:tail_count])
    return dict(sorted(result.items()))


def sample_fitted_distribution_counts(
    n: int,
    fit: DistributionFit,
    *,
    rng: np.random.Generator,
) -> dict[int, int]:
    """Sample an exact integer histogram from a fitted tail distribution.

    Extremely weak cutoff fits with ``gamma <= 1`` and support spans above two
    million integers are rejected as computationally impractical.
    """

    if n < 0:
        raise ValueError("sample size must be nonnegative")
    if n == 0:
        return {}
    if fit.model == "power_law":
        return sample_discrete_power_law_counts(
            n,
            gamma=fit.parameters["gamma"],
            xmin=fit.xmin,
            rng=rng,
        )
    if fit.model == "cutoff_power_law":
        return _sample_cutoff_power_law_counts(n, fit, rng=rng)
    if fit.model == "exponential":
        rate = fit.parameters["lambda"]
        if np.isinf(rate):
            return {fit.xmin: n}
        success_probability = -np.expm1(-rate)
        samples = fit.xmin + rng.geometric(success_probability, size=n) - 1
        return _samples_to_histogram(samples)
    if fit.model == "lognormal":
        mu = fit.parameters["mu"]
        sigma = fit.parameters["sigma"]
        lower = (np.log(fit.xmin - 0.5) - mu) / sigma
        uniforms = np.maximum(rng.random(n), np.finfo(float).tiny)
        log_normal_survival = special.log_ndtr(-lower) + np.log(uniforms)
        normal_values = -special.ndtri_exp(log_normal_survival)
        log_values = mu + sigma * normal_values
        if np.any(log_values > np.log(np.iinfo(np.int64).max - 1.0)):
            raise RuntimeError("sampled lognormal size exceeds int64 range")
        samples = np.floor(np.exp(log_values) + 0.5).astype(np.int64)
        samples = np.maximum(samples, fit.xmin)
        return _samples_to_histogram(samples)
    raise ValueError(f"unsupported fitted model: {fit.model}")


def _fit_named_distribution(
    counts: HistogramLike, *, model: str, xmin: int
) -> DistributionFit:
    if model == "power_law":
        return fit_discrete_power_law(counts, xmin=xmin)
    if model == "cutoff_power_law":
        return fit_cutoff_power_law(counts, xmin=xmin)
    if model == "lognormal":
        return fit_discrete_lognormal(counts, xmin=xmin)
    if model == "exponential":
        return fit_discrete_exponential(counts, xmin=xmin)
    raise ValueError(f"unsupported fitted model: {model}")


def _parametric_gof_replica(arguments) -> float:
    n, observed_fit, seed = arguments
    rng = np.random.default_rng(seed)
    synthetic = sample_fitted_distribution_counts(n, observed_fit, rng=rng)
    return _fit_named_distribution(
        synthetic,
        model=observed_fit.model,
        xmin=observed_fit.xmin,
    ).ks


def parametric_distribution_gof(
    counts: HistogramLike,
    *,
    model: str,
    xmin: int,
    replicates: int = 2_500,
    seed: int = 12_738,
    workers: int = 1,
) -> ParametricGoodnessOfFit:
    """Test absolute fit by a fixed-support, refitted parametric bootstrap."""

    if replicates < 1 or workers < 1:
        raise ValueError("replicates and workers must be positive")
    sizes, frequencies = _histogram_arrays(counts)
    tail_frequencies = frequencies[sizes >= xmin]
    if not np.allclose(
        tail_frequencies,
        np.rint(tail_frequencies),
        rtol=0.0,
        atol=1e-9,
    ):
        raise ValueError(
            "parametric goodness of fit requires integer event frequencies"
        )
    observed = _fit_named_distribution(counts, model=model, xmin=xmin)
    n = int(round(observed.n))
    child_seeds = np.random.SeedSequence(seed).spawn(replicates)
    arguments = [(n, observed, child_seed) for child_seed in child_seeds]
    if workers == 1:
        synthetic_ks = [_parametric_gof_replica(item) for item in arguments]
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            synthetic_ks = list(
                executor.map(
                    _parametric_gof_replica,
                    arguments,
                    chunksize=max(1, replicates // (workers * 16)),
                )
            )
    exceedances = int(np.count_nonzero(np.asarray(synthetic_ks) >= observed.ks))
    p_value = (exceedances + 1.0) / (replicates + 1.0)
    standard_error = float(np.sqrt(p_value * (1.0 - p_value) / replicates))
    return ParametricGoodnessOfFit(
        observed_fit=observed,
        p_value=p_value,
        exceedances=exceedances,
        replicates=replicates,
        monte_carlo_standard_error=standard_error,
        synthetic_ks=tuple(float(value) for value in synthetic_ks),
    )

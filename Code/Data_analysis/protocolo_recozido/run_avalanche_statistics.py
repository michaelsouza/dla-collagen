#!/usr/bin/env python3
"""Run the preregistered avalanche-cluster distribution analysis.

The primary estimand pools preterminal connected clusters with s >= 2.  The
same fits are repeated with terminal rows included and with equal total weight
per fibril.  Raw outputs are validated before a sparse cache is created; no
event-size binning is used.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import multiprocessing
import platform
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import mpmath
import numpy as np
import scipy
from scipy import sparse

from Code.Data_analysis.avalanche_statistics import (
    DistributionFit,
    avalanche_parser_signature,
    clauset_power_law_gof,
    cutoff_power_law_likelihood_ratio_test,
    distribution_cdf,
    distribution_log_probabilities,
    equal_fibril_weight_counts,
    fit_competing_models,
    hierarchical_resample_fibril_counts,
    load_avalanche_condition,
    parametric_distribution_gof,
    select_power_law_xmin,
)


CACHE_SCHEMA_VERSION = 2
MANIFEST_SCHEMA_VERSION = 2
DEFAULT_TS = (2, 8, 32)
_HIERARCHICAL_CONTEXT: dict[str, object] | None = None


def _cache_signature(ts: int) -> dict[str, object]:
    return {
        "schema_version": CACHE_SCHEMA_VERSION,
        "parser_signature": avalanche_parser_signature(),
        "ts": ts,
        "expected_fibrils": 50,
        "expected_runs_per_fibril": 1_000,
        "terminal_partition": "num_active_particles == 0",
        "row_order": "ascending fibril_seed, then ascending run_id",
        "columns": "exact integer connected-cluster size",
    }


@dataclass(frozen=True)
class CachedCondition:
    ts: int
    fibril_seeds: tuple[int, ...]
    initial_particles: tuple[int, ...]
    run_offsets: tuple[int, ...]
    preterminal: sparse.csr_matrix
    terminal: sparse.csr_matrix
    sources: tuple[dict[str, object], ...]

    def matrix(self, *, include_terminal: bool) -> sparse.csr_matrix:
        return self.preterminal + self.terminal if include_terminal else self.preterminal

    def run_matrices(self, *, include_terminal: bool) -> list[sparse.csr_matrix]:
        matrix = self.matrix(include_terminal=include_terminal)
        return [
            matrix[start:stop]
            for start, stop in zip(self.run_offsets[:-1], self.run_offsets[1:], strict=True)
        ]

    def fibril_counts(self, *, include_terminal: bool) -> np.ndarray:
        return np.asarray(
            [
                np.asarray(block.sum(axis=0)).ravel()
                for block in self.run_matrices(include_terminal=include_terminal)
            ],
            dtype=np.int64,
        )


def _source_stats(directory: Path) -> list[dict[str, int | str]]:
    rows = []
    for path in sorted(directory.glob("*.txt")):
        stat = path.stat()
        rows.append(
            {
                "name": path.name,
                "bytes": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
        )
    return rows


def _cache_paths(cache_root: Path, ts: int) -> tuple[Path, Path, Path]:
    prefix = cache_root / f"ts_{ts}"
    return (
        prefix.with_name(prefix.name + "_manifest.json"),
        prefix.with_name(prefix.name + "_preterminal.npz"),
        prefix.with_name(prefix.name + "_terminal.npz"),
    )


def _load_cache(
    directory: Path, cache_root: Path, ts: int
) -> CachedCondition | None:
    manifest_path, preterminal_path, terminal_path = _cache_paths(cache_root, ts)
    if not all(path.exists() for path in (manifest_path, preterminal_path, terminal_path)):
        return None
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if manifest.get("cache_signature") != _cache_signature(ts):
        return None
    if manifest.get("source_stats") != _source_stats(directory):
        return None
    try:
        stored_sources = {
            Path(item["path"]).name: item for item in manifest["sources"]
        }
    except (KeyError, TypeError):
        return None
    if any(
        name not in stored_sources
        or _sha256(directory / name) != stored_sources[name]["sha256"]
        for name in (item["name"] for item in manifest["source_stats"])
    ):
        return None
    try:
        fibril_seeds = tuple(int(value) for value in manifest["fibril_seeds"])
        initial_particles = tuple(
            int(value) for value in manifest["initial_particles"]
        )
        run_offsets = tuple(int(value) for value in manifest["run_offsets"])
        preterminal = sparse.load_npz(preterminal_path).tocsr()
        terminal = sparse.load_npz(terminal_path).tocsr()
    except (KeyError, TypeError, ValueError, OSError):
        return None
    if (
        len(fibril_seeds) != 50
        or len(initial_particles) != len(fibril_seeds)
        or len(run_offsets) != len(fibril_seeds) + 1
        or run_offsets[0] != 0
        or any(stop - start != 1_000 for start, stop in zip(run_offsets[:-1], run_offsets[1:], strict=True))
        or preterminal.shape != terminal.shape
        or preterminal.shape[0] != run_offsets[-1]
    ):
        return None
    return CachedCondition(
        ts=ts,
        fibril_seeds=fibril_seeds,
        initial_particles=initial_particles,
        run_offsets=run_offsets,
        preterminal=preterminal,
        terminal=terminal,
        sources=tuple(manifest["sources"]),
    )


def _build_cache(directory: Path, cache_root: Path, ts: int) -> CachedCondition:
    print(f"[Ts={ts}] validating 50 raw fibril files", flush=True)
    condition = load_avalanche_condition(
        directory, ts=ts, expected_fibrils=50, expected_runs=1_000
    )
    preterminal = condition.run_counts(include_terminal=False)
    all_events = condition.run_counts(include_terminal=True)
    terminal = (all_events - preterminal).tocsr()
    run_counts = [len(item.run_ids) for item in condition.files]
    run_offsets = np.concatenate(([0], np.cumsum(run_counts))).astype(int)
    sources = tuple(
        {
            "path": str(item.source),
            "bytes": item.source_bytes,
            "sha256": item.source_sha256,
            "ts": item.ts,
            "fibril_seed": item.fibril_seed,
            "weibull_m": item.weibull_m,
            "runs": len(item.run_ids),
            "initial_particles": item.initial_particles,
        }
        for item in condition.files
    )
    cache_root.mkdir(parents=True, exist_ok=True)
    manifest_path, preterminal_path, terminal_path = _cache_paths(cache_root, ts)
    sparse.save_npz(preterminal_path, preterminal, compressed=True)
    sparse.save_npz(terminal_path, terminal, compressed=True)
    manifest = {
        "cache_signature": _cache_signature(ts),
        "source_stats": _source_stats(directory),
        "fibril_seeds": list(condition.fibril_seeds),
        "initial_particles": [item.initial_particles for item in condition.files],
        "run_offsets": run_offsets.tolist(),
        "sources": list(sources),
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"[Ts={ts}] validated and cached", flush=True)
    return CachedCondition(
        ts=ts,
        fibril_seeds=condition.fibril_seeds,
        initial_particles=tuple(item.initial_particles for item in condition.files),
        run_offsets=tuple(run_offsets),
        preterminal=preterminal,
        terminal=terminal,
        sources=sources,
    )


def load_or_build_cache(
    data_root: Path, cache_root: Path, ts: int
) -> CachedCondition:
    directory = data_root / f"ts_{ts}"
    cached = _load_cache(directory, cache_root, ts)
    if cached is not None:
        print(f"[Ts={ts}] using validated sparse cache", flush=True)
        return cached
    return _build_cache(directory, cache_root, ts)


def _tail_contributors(
    matrix: sparse.csr_matrix, run_offsets: tuple[int, ...], xmin: int
) -> tuple[int, int]:
    contributing_runs = np.asarray(matrix[:, xmin:].getnnz(axis=1)).ravel() > 0
    fibrils = sum(
        bool(np.any(contributing_runs[start:stop]))
        for start, stop in zip(run_offsets[:-1], run_offsets[1:], strict=True)
    )
    return int(fibrils), int(np.count_nonzero(contributing_runs))


def _fit_row(
    *,
    ts: int,
    include_terminal: bool,
    weighting: str,
    fit: DistributionFit,
    collective_events: float,
) -> dict[str, object]:
    row: dict[str, object] = {
        "ts": ts,
        "terminal": "included" if include_terminal else "excluded",
        "weighting": weighting,
        "model": fit.model,
        "xmin": fit.xmin,
        "n_tail": fit.n,
        "tail_fraction": fit.n / collective_events,
        "log_likelihood": fit.log_likelihood,
        "ks": fit.ks,
    }
    row.update(fit.parameters)
    row.update(fit.diagnostics)
    return row


def analyze_observed(condition: CachedCondition) -> tuple[list[dict], list[dict]]:
    inventory_rows: list[dict] = []
    fit_rows: list[dict] = []
    terminal_histogram = np.asarray(condition.terminal.sum(axis=0)).ravel()
    terminal_event_count = int(terminal_histogram.sum())
    terminal_collective_count = int(terminal_histogram[2:].sum())
    terminal_mass = int(
        np.dot(
            np.arange(condition.terminal.shape[1]),
            terminal_histogram,
        )
    )
    included_collective_count = int(
        np.asarray(
            (condition.preterminal + condition.terminal).sum(axis=0)
        ).ravel()[2:].sum()
    )

    for include_terminal in (False, True):
        matrix = condition.matrix(include_terminal=include_terminal)
        by_fibril = condition.fibril_counts(include_terminal=include_terminal)
        pooled = by_fibril.sum(axis=0)
        all_events = float(pooled.sum())
        singleton_events = float(pooled[1])
        collective_events = float(pooled[2:].sum())
        nonzero_sizes = np.flatnonzero(pooled)
        inventory_rows.append(
            {
                "ts": condition.ts,
                "terminal": "included" if include_terminal else "excluded",
                "fibrils": len(condition.fibril_seeds),
                "runs": condition.preterminal.shape[0],
                "all_clusters": int(all_events),
                "singletons": int(singleton_events),
                "singleton_fraction": singleton_events / all_events,
                "collective_clusters_s_ge_2": int(collective_events),
                "s_max": int(nonzero_sizes[-1]),
                "terminal_clusters_all_sizes": terminal_event_count,
                "terminal_collective_clusters_s_ge_2": terminal_collective_count,
                "terminal_fraction_of_included_collective_clusters": (
                    terminal_collective_count / included_collective_count
                ),
                "terminal_cluster_mass_all_sizes": terminal_mass,
            }
        )

        for weighting in ("pooled_events", "equal_fibril"):
            counts = (
                pooled
                if weighting == "pooled_events"
                else equal_fibril_weight_counts(by_fibril, min_size=2)
            )
            power_law = select_power_law_xmin(
                counts,
                xmin_min=2,
                min_tail=1_000,
                fibril_counts=by_fibril,
                min_fibrils=25,
            )
            fits = fit_competing_models(counts, xmin=power_law.xmin)
            contributors_fibrils, contributors_runs = _tail_contributors(
                matrix, condition.run_offsets, power_law.xmin
            )
            smax = int(np.flatnonzero(counts)[-1])
            for fit in fits.values():
                row = _fit_row(
                    ts=condition.ts,
                    include_terminal=include_terminal,
                    weighting=weighting,
                    fit=fit,
                    collective_events=float(counts[2:].sum()),
                )
                row.update(
                    {
                        "tail_fibrils": contributors_fibrils,
                        "tail_runs": contributors_runs,
                        "s_max": smax,
                        "tail_span_decades": np.log10(smax / power_law.xmin),
                        "delta_log_likelihood_vs_power_law": (
                            fit.log_likelihood - fits["power_law"].log_likelihood
                        ),
                    }
                )
                fit_rows.append(row)
            print(
                f"[Ts={condition.ts}] terminal={include_terminal} "
                f"weighting={weighting}: xmin={power_law.xmin}, "
                f"gamma={power_law.parameters['gamma']:.6g}",
                flush=True,
            )
    return inventory_rows, fit_rows


def run_leave_one_fibril_out(
    condition: CachedCondition,
) -> tuple[list[dict], list[dict]]:
    summaries: list[dict] = []
    fold_rows: list[dict] = []
    for include_terminal in (False, True):
        label = "included" if include_terminal else "excluded"
        by_fibril = condition.fibril_counts(include_terminal=include_terminal)
        pooled = by_fibril.sum(axis=0)
        selected = select_power_law_xmin(
            pooled,
            xmin_min=2,
            min_tail=1_000,
            fibril_counts=by_fibril,
            min_fibrils=25,
        )
        total_predictive: dict[str, float] = {
            model: 0.0
            for model in (
                "power_law",
                "cutoff_power_law",
                "lognormal",
                "exponential",
            )
        }
        for fibril_index, (seed, held_out) in enumerate(
            zip(condition.fibril_seeds, by_fibril, strict=True)
        ):
            training = pooled - held_out
            fits = fit_competing_models(training, xmin=selected.xmin)
            support = np.flatnonzero(held_out)
            support = support[support >= selected.xmin]
            frequencies = held_out[support]
            for model, fit in fits.items():
                predictive_log_likelihood = float(
                    np.dot(
                        frequencies,
                        distribution_log_probabilities(fit, support),
                    )
                )
                total_predictive[model] += predictive_log_likelihood
                fold_rows.append(
                    {
                        "ts": condition.ts,
                        "terminal": label,
                        "fibril_index": fibril_index,
                        "fibril_seed": seed,
                        "xmin": selected.xmin,
                        "model": model,
                        "held_out_tail_events": int(frequencies.sum()),
                        "predictive_log_likelihood": predictive_log_likelihood,
                    }
                )
        for model, predictive_log_likelihood in total_predictive.items():
            summaries.append(
                {
                    "ts": condition.ts,
                    "terminal": label,
                    "xmin": selected.xmin,
                    "model": model,
                    "predictive_log_likelihood": predictive_log_likelihood,
                    "delta_predictive_log_likelihood_vs_power_law": (
                        predictive_log_likelihood - total_predictive["power_law"]
                    ),
                }
            )
    return summaries, fold_rows


def run_power_law_gof(
    condition: CachedCondition,
    *,
    replicates: int,
    workers: int,
    master_seed: int,
) -> tuple[list[dict], list[dict]]:
    summary_rows: list[dict] = []
    replica_rows: list[dict] = []
    for include_terminal in (False, True):
        by_fibril = condition.fibril_counts(include_terminal=include_terminal)
        counts = by_fibril.sum(axis=0)
        seed = master_seed + 10_000 * condition.ts + int(include_terminal)
        label = "included" if include_terminal else "excluded"
        print(
            f"[Ts={condition.ts}] Clauset GOF, terminal={label}, "
            f"B={replicates}, workers={workers}",
            flush=True,
        )
        result = clauset_power_law_gof(
            counts,
            xmin_min=2,
            min_tail=1_000,
            replicates=replicates,
            seed=seed,
            workers=workers,
        )
        summary_rows.append(
            {
                "ts": condition.ts,
                "terminal": label,
                "weighting": "pooled_events",
                "xmin_selection": "iid_clauset_without_fibril_constraint",
                "dependence_assumption": "iid_cluster_events",
                "inference_role": "secondary_marginal_diagnostic",
                "replicates": result.replicates,
                "seed": seed,
                "xmin": result.observed_fit.xmin,
                "gamma": result.observed_fit.parameters["gamma"],
                "ks": result.observed_fit.ks,
                "n_tail": result.observed_fit.n,
                "exceedances": result.exceedances,
                "p_value": result.p_value,
                "monte_carlo_standard_error": result.monte_carlo_standard_error,
            }
        )
        replica_rows.extend(
            {
                "ts": condition.ts,
                "terminal": label,
                "replicate": index,
                "xmin": xmin,
                "n_tail": n_tail,
                "ks": ks,
            }
            for index, (xmin, n_tail, ks) in enumerate(
                zip(
                    result.synthetic_xmins,
                    result.synthetic_tail_counts,
                    result.synthetic_ks,
                    strict=True,
                ),
                start=1,
            )
        )
        print(
            f"[Ts={condition.ts}] terminal={label}: "
            f"p={result.p_value:.6g} ({result.exceedances}/{replicates})",
            flush=True,
        )
    return summary_rows, replica_rows


def _empirical_tail_cdf(counts: np.ndarray, xmin: int, grid: np.ndarray) -> np.ndarray:
    tail_n = float(counts[xmin:].sum())
    if tail_n <= 0:
        raise ValueError("bootstrap replicate contains no observations on the fixed tail")
    dense = np.zeros(int(grid[-1]) - xmin + 1, dtype=float)
    available = min(len(dense), max(0, counts.size - xmin))
    if available:
        dense[:available] = counts[xmin : xmin + available]
    return np.cumsum(dense) / tail_n


def _hierarchical_replica(seed: np.random.SeedSequence) -> dict[str, float]:
    if _HIERARCHICAL_CONTEXT is None:
        raise RuntimeError("hierarchical bootstrap worker was not initialized")
    context = _HIERARCHICAL_CONTEXT
    rng = np.random.default_rng(seed)
    sampled_by_fibril = hierarchical_resample_fibril_counts(
        context["run_matrices"], rng=rng
    )
    counts = sampled_by_fibril.sum(axis=0)
    selected_fit = select_power_law_xmin(
        counts,
        xmin_min=2,
        min_tail=1_000,
        fibril_counts=sampled_by_fibril,
        min_fibrils=25,
    )
    selected_fits = fit_competing_models(counts, xmin=selected_fit.xmin)
    fixed_fits = fit_competing_models(counts, xmin=context["xmin"])
    fixed_power_law = fixed_fits["power_law"]
    grid = context["grid"]
    empirical_cdf = _empirical_tail_cdf(counts, context["xmin"], grid)
    collective_events = float(counts[2:].sum())
    row: dict[str, float] = {
        "selected_xmin": float(selected_fit.xmin),
        "selected_gamma": selected_fit.parameters["gamma"],
        "selected_n_tail": selected_fit.n,
        "selected_tail_fraction": selected_fit.n / collective_events,
        "fixed_gamma": fixed_power_law.parameters["gamma"],
        "fixed_power_law_ks": fixed_power_law.ks,
    }
    for model, fit in selected_fits.items():
        row[f"selected_ll_{model}"] = fit.log_likelihood
        for parameter, value in fit.parameters.items():
            row[f"selected_{model}_{parameter}"] = value
    for model, fit in fixed_fits.items():
        residual = empirical_cdf - distribution_cdf(fit, grid)
        row[f"centered_ks_{model}"] = float(
            np.max(np.abs(residual - context["observed_residuals"][model]))
        )
        row[f"ll_{model}"] = fit.log_likelihood
        row[f"delta_ll_{model}_vs_power_law"] = (
            fit.log_likelihood - fixed_power_law.log_likelihood
        )
        for parameter, value in fit.parameters.items():
            row[f"{model}_{parameter}"] = value
    return row


def run_hierarchical_bootstrap(
    condition: CachedCondition,
    *,
    replicates: int,
    workers: int,
    master_seed: int,
) -> tuple[list[dict], list[dict]]:
    global _HIERARCHICAL_CONTEXT
    summaries: list[dict] = []
    rows: list[dict] = []
    for include_terminal in (False, True):
        label = "included" if include_terminal else "excluded"
        run_matrices = condition.run_matrices(include_terminal=include_terminal)
        counts = np.asarray(
            sparse.vstack(run_matrices, format="csr").sum(axis=0)
        ).ravel()
        by_fibril = condition.fibril_counts(include_terminal=include_terminal)
        observed_selected = select_power_law_xmin(
            counts,
            xmin_min=2,
            min_tail=1_000,
            fibril_counts=by_fibril,
            min_fibrils=25,
        )
        observed_fits = fit_competing_models(counts, xmin=observed_selected.xmin)
        observed_power_law = observed_fits["power_law"]
        grid = np.arange(observed_selected.xmin, len(counts), dtype=np.int64)
        observed_empirical_cdf = _empirical_tail_cdf(
            counts, observed_selected.xmin, grid
        )
        observed_residuals = {
            model: observed_empirical_cdf - distribution_cdf(fit, grid)
            for model, fit in observed_fits.items()
        }
        observed_ks_by_model = {
            model: float(np.max(np.abs(residual)))
            for model, residual in observed_residuals.items()
        }
        observed_ks = observed_ks_by_model["power_law"]
        _HIERARCHICAL_CONTEXT = {
            "run_matrices": run_matrices,
            "xmin": observed_selected.xmin,
            "grid": grid,
            "observed_residuals": observed_residuals,
        }
        seed = master_seed + 20_000 * condition.ts + int(include_terminal)
        child_seeds = np.random.SeedSequence(seed).spawn(replicates)
        print(
            f"[Ts={condition.ts}] hierarchical bootstrap, terminal={label}, "
            f"B={replicates}, workers={workers}",
            flush=True,
        )
        if workers == 1:
            replica_results = [_hierarchical_replica(item) for item in child_seeds]
        else:
            with ProcessPoolExecutor(
                max_workers=workers,
                mp_context=multiprocessing.get_context("fork"),
            ) as executor:
                replica_results = list(
                    executor.map(
                        _hierarchical_replica,
                        child_seeds,
                        chunksize=max(1, replicates // (workers * 16)),
                    )
                )
        summary: dict[str, object] = {
            "ts": condition.ts,
            "terminal": label,
            "weighting": "hierarchical_fibril_then_run",
            "replicates": replicates,
            "seed": seed,
            "observed_xmin": observed_selected.xmin,
            "observed_gamma": observed_selected.parameters["gamma"],
            "observed_ks": observed_ks,
        }
        for model, model_observed_ks in observed_ks_by_model.items():
            centered = np.asarray(
                [item[f"centered_ks_{model}"] for item in replica_results]
            )
            exceedances = int(np.count_nonzero(centered >= model_observed_ks))
            hierarchical_p = (exceedances + 1.0) / (replicates + 1.0)
            summary[f"observed_ks_{model}"] = model_observed_ks
            summary[f"centered_ks_exceedances_{model}"] = exceedances
            summary[f"hierarchical_ks_p_value_{model}"] = hierarchical_p
        numeric_keys = sorted(replica_results[0])
        for key in numeric_keys:
            values = np.asarray([item[key] for item in replica_results], dtype=float)
            lower, median, upper = np.percentile(values, [2.5, 50.0, 97.5])
            summary[f"{key}_ci_lower"] = lower
            summary[f"{key}_median"] = median
            summary[f"{key}_ci_upper"] = upper
        summaries.append(summary)
        rows.extend(
            {
                "ts": condition.ts,
                "terminal": label,
                "replicate": index,
                **replica,
            }
            for index, replica in enumerate(replica_results, start=1)
        )
        print(
            f"[Ts={condition.ts}] terminal={label}: hierarchical KS "
            f"p_PL={summary['hierarchical_ks_p_value_power_law']:.6g}",
            flush=True,
        )
    _HIERARCHICAL_CONTEXT = None
    return summaries, rows


def run_cutoff_likelihood_ratio_bootstrap(
    condition: CachedCondition,
    *,
    replicates: int,
    workers: int,
    master_seed: int,
) -> tuple[list[dict], list[dict]]:
    summaries: list[dict] = []
    replica_rows: list[dict] = []
    for include_terminal in (False, True):
        label = "included" if include_terminal else "excluded"
        by_fibril = condition.fibril_counts(include_terminal=include_terminal)
        counts = by_fibril.sum(axis=0)
        power_law = select_power_law_xmin(
            counts,
            xmin_min=2,
            min_tail=1_000,
            fibril_counts=by_fibril,
            min_fibrils=25,
        )
        seed = master_seed + 30_000 * condition.ts + int(include_terminal)
        print(
            f"[Ts={condition.ts}] cutoff LR bootstrap, terminal={label}, "
            f"B={replicates}, workers={workers}",
            flush=True,
        )
        result = cutoff_power_law_likelihood_ratio_test(
            counts,
            xmin=power_law.xmin,
            replicates=replicates,
            seed=seed,
            workers=workers,
        )
        summaries.append(
            {
                "ts": condition.ts,
                "terminal": label,
                "weighting": "pooled_events",
                "xmin": power_law.xmin,
                "replicates": replicates,
                "seed": seed,
                "observed_likelihood_ratio": result.observed_likelihood_ratio,
                "exceedances": result.exceedances,
                "p_value": result.p_value,
                "monte_carlo_standard_error": result.monte_carlo_standard_error,
            }
        )
        replica_rows.extend(
            {
                "ts": condition.ts,
                "terminal": label,
                "replicate": index,
                "likelihood_ratio": likelihood_ratio,
            }
            for index, likelihood_ratio in enumerate(
                result.synthetic_likelihood_ratios, start=1
            )
        )
        print(
            f"[Ts={condition.ts}] terminal={label}: cutoff LR "
            f"p={result.p_value:.6g}",
            flush=True,
        )
    return summaries, replica_rows


def run_alternative_model_gof(
    condition: CachedCondition,
    *,
    replicates: int,
    workers: int,
    master_seed: int,
    include_terminal_sensitivity: bool,
) -> tuple[list[dict], list[dict]]:
    """Run fixed-common-support absolute GOF tests for alternative families."""

    summaries: list[dict] = []
    replica_rows: list[dict] = []
    terminal_rules = (False, True) if include_terminal_sensitivity else (False,)
    models = ("cutoff_power_law", "lognormal", "exponential")
    for include_terminal in terminal_rules:
        label = "included" if include_terminal else "excluded"
        by_fibril = condition.fibril_counts(include_terminal=include_terminal)
        counts = by_fibril.sum(axis=0)
        selected = select_power_law_xmin(
            counts,
            xmin_min=2,
            min_tail=1_000,
            fibril_counts=by_fibril,
            min_fibrils=25,
        )
        for model_index, model in enumerate(models, start=1):
            seed = (
                master_seed
                + 40_000 * condition.ts
                + 100 * model_index
                + int(include_terminal)
            )
            print(
                f"[Ts={condition.ts}] alternative GOF, model={model}, "
                f"terminal={label}, B={replicates}, workers={workers}",
                flush=True,
            )
            result = parametric_distribution_gof(
                counts,
                model=model,
                xmin=selected.xmin,
                replicates=replicates,
                seed=seed,
                workers=workers,
            )
            summary: dict[str, object] = {
                "ts": condition.ts,
                "terminal": label,
                "weighting": "pooled_events",
                "model": model,
                "xmin": selected.xmin,
                "xmin_selection": "observed_power_law_with_25_fibril_minimum",
                "bootstrap_support": "fixed_at_observed_power_law_xmin",
                "dependence_assumption": "iid_tail_cluster_events",
                "inference_role": (
                    "secondary_marginal_diagnostic_interpreted_with_"
                    "hierarchical_centered_ks"
                ),
                "n_tail": result.observed_fit.n,
                "ks": result.observed_fit.ks,
                "replicates": result.replicates,
                "seed": seed,
                "exceedances": result.exceedances,
                "p_value": result.p_value,
                "monte_carlo_standard_error": result.monte_carlo_standard_error,
            }
            synthetic_ks = np.asarray(result.synthetic_ks, dtype=float)
            synthetic_ks_median = float(np.median(synthetic_ks))
            summary.update(
                {
                    "synthetic_ks_median": synthetic_ks_median,
                    "synthetic_ks_95th_percentile": float(
                        np.percentile(synthetic_ks, 95.0)
                    ),
                    "observed_to_synthetic_median_ks_ratio": (
                        result.observed_fit.ks / synthetic_ks_median
                        if synthetic_ks_median > 0.0
                        else float("inf")
                    ),
                }
            )
            summary.update(result.observed_fit.parameters)
            summary.update(result.observed_fit.diagnostics)
            summaries.append(summary)
            replica_rows.extend(
                {
                    "ts": condition.ts,
                    "terminal": label,
                    "model": model,
                    "replicate": index,
                    "ks": ks,
                }
                for index, ks in enumerate(result.synthetic_ks, start=1)
            )
            print(
                f"[Ts={condition.ts}] model={model}, terminal={label}: "
                f"p={result.p_value:.6g} "
                f"({result.exceedances}/{replicates})",
                flush=True,
            )
    return summaries, replica_rows


def _write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    temporary = path.with_name(f".{path.name}.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def _checkpoint_path(path: Path) -> Path:
    return path.with_name(f".{path.stem}.partial{path.suffix}")


def _write_csv_checkpoint(path: Path, rows: list[dict]) -> None:
    _write_csv(_checkpoint_path(path), rows)


def _clear_csv_checkpoint(path: Path) -> None:
    _checkpoint_path(path).unlink(missing_ok=True)


def _sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _analysis_files_snapshot() -> dict[str, dict[str, str]]:
    module_path = Path(__file__).with_name("avalanche_statistics.py")
    return {
        "module": {
            "path": "Code/Data_analysis/avalanche_statistics.py",
            "sha256": _sha256(module_path),
        },
        "runner": {
            "path": "Code/Data_analysis/run_avalanche_statistics.py",
            "sha256": _sha256(Path(__file__)),
        },
    }


def _software_snapshot() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "mpmath": mpmath.__version__,
    }


def _artifact_metadata(output: Path, paths: list[Path]) -> list[dict[str, object]]:
    artifacts: list[dict[str, object]] = []
    for path in paths:
        if not path.exists():
            continue
        record: dict[str, object] = {
            "path": str(path.relative_to(output)),
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        if path.suffix == ".csv":
            with path.open(encoding="utf-8") as stream:
                record["rows"] = max(sum(1 for _ in stream) - 1, 0)
        artifacts.append(record)
    return artifacts


def _stage_record(
    *,
    completed_utc: str,
    scope: dict[str, object],
    analysis_files: dict[str, dict[str, str]],
    software: dict[str, str],
    sources: list[dict],
    artifacts: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "completed_utc": completed_utc,
        "scope": copy.deepcopy(scope),
        "software": copy.deepcopy(software),
        "analysis_files": copy.deepcopy(analysis_files),
        "sources": copy.deepcopy(sources),
        "artifacts": copy.deepcopy(artifacts),
    }


def _migrate_legacy_manifest(
    legacy: dict[str, object],
    output: Path,
    *,
    original_sha256: str | None = None,
) -> dict[str, object]:
    """Import the former single-run manifest without changing its provenance."""

    if legacy.get("manifest_schema_version") == MANIFEST_SCHEMA_VERSION:
        return copy.deepcopy(legacy)
    created_utc = str(legacy.get("created_utc", "unknown"))
    analysis_scope = dict(legacy.get("analysis_scope", {}))
    analysis_files = copy.deepcopy(legacy.get("analysis_files", {}))
    software = copy.deepcopy(legacy.get("software", {}))
    sources = copy.deepcopy(legacy.get("sources", []))

    def legacy_stage(scope: dict[str, object], filenames: list[str]) -> dict[str, object]:
        stage = _stage_record(
            completed_utc=created_utc,
            scope=scope,
            analysis_files=analysis_files,
            software=software,
            sources=sources,
            artifacts=_artifact_metadata(output, [output / name for name in filenames]),
        )
        stage["migrated_from_manifest_schema"] = 1
        return stage

    stages: dict[str, dict[str, object]] = {}
    observed_files = ["inventory.csv", "observed_model_fits.csv"]
    if all((output / name).exists() for name in observed_files):
        stages["observed"] = legacy_stage(analysis_scope, observed_files)

    gof_replicates = int(analysis_scope.get("clauset_gof_replicates", 0) or 0)
    gof_files = ["power_law_gof.csv", "power_law_gof_replicates.csv"]
    if gof_replicates and all((output / name).exists() for name in gof_files):
        stages["power_law_gof:power_law_gof"] = legacy_stage(
            {
                "ts": analysis_scope.get("ts", []),
                "replicates": gof_replicates,
                "seed": analysis_scope.get("bootstrap_master_seed"),
                "xmin_selection": "iid_clauset_without_fibril_constraint",
            },
            gof_files,
        )

    hierarchical_replicates = int(
        analysis_scope.get("hierarchical_bootstrap_replicates", 0) or 0
    )
    hierarchical_files = [
        "hierarchical_bootstrap.csv",
        "hierarchical_bootstrap_replicates.csv",
    ]
    if hierarchical_replicates and all(
        (output / name).exists() for name in hierarchical_files
    ):
        stages["hierarchical_bootstrap"] = legacy_stage(
            {
                "ts": analysis_scope.get("ts", []),
                "replicates": hierarchical_replicates,
                "seed": analysis_scope.get("bootstrap_master_seed"),
            },
            hierarchical_files,
        )

    cutoff_replicates = int(
        analysis_scope.get("cutoff_likelihood_ratio_bootstrap_replicates", 0) or 0
    )
    cutoff_files = [
        "cutoff_likelihood_ratio_bootstrap.csv",
        "cutoff_likelihood_ratio_bootstrap_replicates.csv",
    ]
    if cutoff_replicates and all((output / name).exists() for name in cutoff_files):
        stages["cutoff_likelihood_ratio_bootstrap"] = legacy_stage(
            {
                "ts": analysis_scope.get("ts", []),
                "replicates": cutoff_replicates,
                "seed": analysis_scope.get("bootstrap_master_seed"),
            },
            cutoff_files,
        )

    result: dict[str, object] = {
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "stages": stages,
        "invocations": [],
        "legacy_import": {"created_utc": created_utc},
    }
    if original_sha256 is not None:
        result["legacy_import"]["original_manifest_sha256"] = original_sha256
    return result


def _merge_manifest_data(
    existing: dict[str, object],
    *,
    stage_updates: dict[str, dict[str, object]],
    invocation: dict[str, object],
) -> dict[str, object]:
    merged = copy.deepcopy(existing)
    merged["manifest_schema_version"] = MANIFEST_SCHEMA_VERSION
    stages = dict(merged.get("stages", {}))
    stages.update(copy.deepcopy(stage_updates))
    merged["stages"] = stages
    invocations = list(merged.get("invocations", []))
    invocations.append(copy.deepcopy(invocation))
    merged["invocations"] = invocations
    merged["updated_utc"] = invocation.get("completed_utc")
    return merged


def _load_prior_manifest(output: Path) -> dict[str, object]:
    path = output / "run_manifest.json"
    if not path.exists():
        return {
            "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
            "stages": {},
            "invocations": [],
        }
    raw = path.read_bytes()
    existing = json.loads(raw.decode("utf-8"))
    return _migrate_legacy_manifest(
        existing,
        output,
        original_sha256=hashlib.sha256(raw).hexdigest(),
    )


def _write_run_manifest(output: Path, manifest: dict[str, object]) -> None:
    path = output / "run_manifest.json"
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def parse_arguments() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ts", nargs="+", type=int, default=list(DEFAULT_TS))
    parser.add_argument(
        "--data-root",
        type=Path,
        default=repo_root / "Data_fibrils" / "Avalanche_force_grouped" / "runs",
    )
    parser.add_argument(
        "--cache-root",
        type=Path,
        default=repo_root
        / "Data_fibrils"
        / "Avalanche_force_grouped"
        / "analysis_cache",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "Reviews" / "Issue5_avalanche_statistics",
    )
    parser.add_argument("--gof-replicates", type=int, default=0)
    parser.add_argument("--hierarchical-replicates", type=int, default=0)
    parser.add_argument("--cutoff-lr-replicates", type=int, default=0)
    parser.add_argument("--alternative-gof-replicates", type=int, default=0)
    parser.add_argument(
        "--alternative-gof-include-terminal",
        action="store_true",
        help="Also run the costly alternative-model GOF on terminal-inclusive data.",
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=12_738)
    parser.add_argument("--lofo", action="store_true")
    parser.add_argument(
        "--gof-tag",
        default="power_law_gof",
        help="Output basename for GOF CSV files.",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    arguments.output.mkdir(parents=True, exist_ok=True)
    started_utc = datetime.now(timezone.utc).isoformat()
    analysis_files = _analysis_files_snapshot()
    software = _software_snapshot()
    prior_manifest = _load_prior_manifest(arguments.output)
    all_inventory: list[dict] = []
    all_fits: list[dict] = []
    all_sources: list[dict] = []
    all_gof: list[dict] = []
    all_gof_replicas: list[dict] = []
    all_hierarchical: list[dict] = []
    all_hierarchical_replicas: list[dict] = []
    all_cutoff_lr: list[dict] = []
    all_cutoff_lr_replicas: list[dict] = []
    all_alternative_gof: list[dict] = []
    all_alternative_gof_replicas: list[dict] = []
    all_lofo: list[dict] = []
    all_lofo_folds: list[dict] = []

    for ts in arguments.ts:
        condition = load_or_build_cache(arguments.data_root, arguments.cache_root, ts)
        inventory, fits = analyze_observed(condition)
        all_inventory.extend(inventory)
        all_fits.extend(fits)
        all_sources.extend(condition.sources)
        if arguments.lofo:
            lofo, lofo_folds = run_leave_one_fibril_out(condition)
            all_lofo.extend(lofo)
            all_lofo_folds.extend(lofo_folds)
            _write_csv_checkpoint(
                arguments.output / "leave_one_fibril_out.csv", all_lofo
            )
            _write_csv_checkpoint(
                arguments.output / "leave_one_fibril_out_folds.csv",
                all_lofo_folds,
            )
        if arguments.gof_replicates:
            gof, replicas = run_power_law_gof(
                condition,
                replicates=arguments.gof_replicates,
                workers=arguments.workers,
                master_seed=arguments.seed,
            )
            all_gof.extend(gof)
            all_gof_replicas.extend(replicas)
            _write_csv_checkpoint(
                arguments.output / f"{arguments.gof_tag}.csv", all_gof
            )
            _write_csv_checkpoint(
                arguments.output / f"{arguments.gof_tag}_replicates.csv",
                all_gof_replicas,
            )
        if arguments.hierarchical_replicates:
            hierarchical, hierarchical_replicas = run_hierarchical_bootstrap(
                condition,
                replicates=arguments.hierarchical_replicates,
                workers=arguments.workers,
                master_seed=arguments.seed,
            )
            all_hierarchical.extend(hierarchical)
            all_hierarchical_replicas.extend(hierarchical_replicas)
            _write_csv_checkpoint(
                arguments.output / "hierarchical_bootstrap.csv",
                all_hierarchical,
            )
            _write_csv_checkpoint(
                arguments.output / "hierarchical_bootstrap_replicates.csv",
                all_hierarchical_replicas,
            )
        if arguments.cutoff_lr_replicates:
            cutoff_lr, cutoff_lr_replicas = run_cutoff_likelihood_ratio_bootstrap(
                condition,
                replicates=arguments.cutoff_lr_replicates,
                workers=arguments.workers,
                master_seed=arguments.seed,
            )
            all_cutoff_lr.extend(cutoff_lr)
            all_cutoff_lr_replicas.extend(cutoff_lr_replicas)
            _write_csv_checkpoint(
                arguments.output / "cutoff_likelihood_ratio_bootstrap.csv",
                all_cutoff_lr,
            )
            _write_csv_checkpoint(
                arguments.output
                / "cutoff_likelihood_ratio_bootstrap_replicates.csv",
                all_cutoff_lr_replicas,
            )
        if arguments.alternative_gof_replicates:
            alternative_gof, alternative_gof_replicas = run_alternative_model_gof(
                condition,
                replicates=arguments.alternative_gof_replicates,
                workers=arguments.workers,
                master_seed=arguments.seed,
                include_terminal_sensitivity=(
                    arguments.alternative_gof_include_terminal
                ),
            )
            all_alternative_gof.extend(alternative_gof)
            all_alternative_gof_replicas.extend(alternative_gof_replicas)
            _write_csv_checkpoint(
                arguments.output / "alternative_model_gof.csv",
                all_alternative_gof,
            )
            _write_csv_checkpoint(
                arguments.output / "alternative_model_gof_replicates.csv",
                all_alternative_gof_replicas,
            )

    inventory_path = arguments.output / "inventory.csv"
    fits_path = arguments.output / "observed_model_fits.csv"
    _write_csv(inventory_path, all_inventory)
    _write_csv(fits_path, all_fits)
    optional_artifacts: dict[str, list[Path]] = {}
    if arguments.lofo:
        paths = [
            arguments.output / "leave_one_fibril_out.csv",
            arguments.output / "leave_one_fibril_out_folds.csv",
        ]
        _write_csv(paths[0], all_lofo)
        _write_csv(paths[1], all_lofo_folds)
        _clear_csv_checkpoint(paths[0])
        _clear_csv_checkpoint(paths[1])
        optional_artifacts["leave_one_fibril_out"] = paths
    if arguments.gof_replicates:
        paths = [
            arguments.output / f"{arguments.gof_tag}.csv",
            arguments.output / f"{arguments.gof_tag}_replicates.csv",
        ]
        _write_csv(paths[0], all_gof)
        _write_csv(paths[1], all_gof_replicas)
        _clear_csv_checkpoint(paths[0])
        _clear_csv_checkpoint(paths[1])
        optional_artifacts[f"power_law_gof:{arguments.gof_tag}"] = paths
    if arguments.hierarchical_replicates:
        paths = [
            arguments.output / "hierarchical_bootstrap.csv",
            arguments.output / "hierarchical_bootstrap_replicates.csv",
        ]
        _write_csv(paths[0], all_hierarchical)
        _write_csv(paths[1], all_hierarchical_replicas)
        _clear_csv_checkpoint(paths[0])
        _clear_csv_checkpoint(paths[1])
        optional_artifacts["hierarchical_bootstrap"] = paths
    if arguments.cutoff_lr_replicates:
        paths = [
            arguments.output / "cutoff_likelihood_ratio_bootstrap.csv",
            arguments.output / "cutoff_likelihood_ratio_bootstrap_replicates.csv",
        ]
        _write_csv(paths[0], all_cutoff_lr)
        _write_csv(paths[1], all_cutoff_lr_replicas)
        _clear_csv_checkpoint(paths[0])
        _clear_csv_checkpoint(paths[1])
        optional_artifacts["cutoff_likelihood_ratio_bootstrap"] = paths
    if arguments.alternative_gof_replicates:
        paths = [
            arguments.output / "alternative_model_gof.csv",
            arguments.output / "alternative_model_gof_replicates.csv",
        ]
        _write_csv(paths[0], all_alternative_gof)
        _write_csv(paths[1], all_alternative_gof_replicas)
        _clear_csv_checkpoint(paths[0])
        _clear_csv_checkpoint(paths[1])
        optional_artifacts["alternative_model_gof"] = paths

    completed_utc = datetime.now(timezone.utc).isoformat()
    common_rules: dict[str, object] = {
        "ts": arguments.ts,
        "collective_event_minimum_size": 2,
        "primary_terminal_rule": "exclude every cluster on active_particles=0 row",
        "terminal_sensitivity": "include every cluster on that row",
        "primary_weighting": "pooled events",
        "weighting_sensitivity": "equal total weight per fibril",
        "xmin_rule": "minimum exact discrete KS over observed sizes",
        "minimum_tail_events": 1_000,
        "minimum_tail_fibrils": 25,
    }
    stage_updates = {
        "observed": _stage_record(
            completed_utc=completed_utc,
            scope=common_rules,
            analysis_files=analysis_files,
            software=software,
            sources=all_sources,
            artifacts=_artifact_metadata(
                arguments.output, [inventory_path, fits_path]
            ),
        )
    }
    for stage_name, paths in optional_artifacts.items():
        scope = dict(common_rules)
        scope.update(
            {
                "workers": arguments.workers,
                "bootstrap_master_seed": arguments.seed,
            }
        )
        if stage_name.startswith("power_law_gof:"):
            scope.update(
                {
                    "replicates": arguments.gof_replicates,
                    "xmin_selection": "iid_clauset_without_fibril_constraint",
                    "dependence_assumption": "iid_cluster_events",
                    "inference_role": "secondary_marginal_diagnostic",
                }
            )
        elif stage_name == "hierarchical_bootstrap":
            scope["replicates"] = arguments.hierarchical_replicates
        elif stage_name == "cutoff_likelihood_ratio_bootstrap":
            scope["replicates"] = arguments.cutoff_lr_replicates
        elif stage_name == "alternative_model_gof":
            scope.update(
                {
                    "replicates": arguments.alternative_gof_replicates,
                    "models": [
                        "cutoff_power_law",
                        "lognormal",
                        "exponential",
                    ],
                    "bootstrap_support": "fixed_at_observed_power_law_xmin",
                    "dependence_assumption": "iid_tail_cluster_events",
                    "inference_role": (
                        "secondary_marginal_diagnostic_interpreted_with_"
                        "hierarchical_centered_ks"
                    ),
                    "include_terminal_sensitivity": (
                        arguments.alternative_gof_include_terminal
                    ),
                }
            )
        stage_updates[stage_name] = _stage_record(
            completed_utc=completed_utc,
            scope=scope,
            analysis_files=analysis_files,
            software=software,
            sources=all_sources,
            artifacts=_artifact_metadata(arguments.output, paths),
        )
    invocation = {
        "started_utc": started_utc,
        "completed_utc": completed_utc,
        "ts": arguments.ts,
        "gof_replicates": arguments.gof_replicates,
        "hierarchical_replicates": arguments.hierarchical_replicates,
        "cutoff_likelihood_ratio_replicates": arguments.cutoff_lr_replicates,
        "alternative_model_gof_replicates": arguments.alternative_gof_replicates,
        "alternative_gof_include_terminal": (
            arguments.alternative_gof_include_terminal
        ),
        "lofo": arguments.lofo,
        "workers": arguments.workers,
        "bootstrap_master_seed": arguments.seed,
        "analysis_files": analysis_files,
    }
    run_manifest = _merge_manifest_data(
        prior_manifest,
        stage_updates=stage_updates,
        invocation=invocation,
    )
    _write_run_manifest(arguments.output, run_manifest)
    print(f"Observed outputs written to {arguments.output}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

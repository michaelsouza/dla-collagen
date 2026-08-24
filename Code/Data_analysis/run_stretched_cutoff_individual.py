#!/usr/bin/env python3
"""Analyze a separately selected stretched-cutoff tail for every Ts."""

from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from scipy import stats

from clauset_hierarchical.analysis import (
    BlockModelGoodnessOfFit,
    FibrilHistograms,
    _cluster_vuong,
    available_ts,
    fit_block_model_gof,
    load_fibril_histograms,
    select_model_xmin,
)
from clauset_pooled.models import (
    ModelFit,
    fit_cutoff_power_law,
    fit_exponential,
    fit_lognormal,
    fit_power_law_model,
    fit_stretched_cutoff_power_law,
    log_probabilities,
)


REPOSITORY = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE = (
    REPOSITORY / "Data_avalanches_all_fibrils" / "derived"
    / "avalanche_analysis_v1.duckdb"
)
DEFAULT_OUTPUT = (
    REPOSITORY / "Data_avalanches_all_fibrils" / "reproduction"
    / "stretched_cutoff_individual_all_ts"
)
MODELS = (
    "exponential",
    "power_law",
    "cutoff_power_law",
    "lognormal",
    "stretched_cutoff_power_law",
)
MODEL_LABELS = {
    "exponential": "exponencial",
    "power_law": "potência pura",
    "cutoff_power_law": "potência + corte exponencial",
    "lognormal": "lognormal",
    "stretched_cutoff_power_law": "potência + corte estendido",
}


def format_ts_axis(axis: plt.Axes, ts_values: list[int] | np.ndarray) -> None:
    axis.set_xscale("log", base=2)
    axis.set_xticks(ts_values)
    axis.set_xticklabels([str(value) for value in ts_values], rotation=35)


@dataclass(frozen=True)
class ConditionResult:
    ts: int
    total_events: int
    maximum_size: int
    selected: ModelFit
    xmin_candidates: tuple[ModelFit, ...]
    fits: tuple[ModelFit, ...]
    goodness: tuple[BlockModelGoodnessOfFit, ...]


def _fit_models(histogram: np.ndarray, xmin: int) -> tuple[ModelFit, ...]:
    return (
        fit_exponential(histogram, xmin),
        fit_power_law_model(histogram, xmin),
        fit_cutoff_power_law(histogram, xmin),
        fit_lognormal(histogram, xmin),
        fit_stretched_cutoff_power_law(histogram, xmin),
    )


def analyze_condition(
    database: str,
    ts: int,
    minimum_xmin: int,
    maximum_xmin: int | None,
    minimum_tail: int,
    replicates: int,
    seed: int,
) -> ConditionResult:
    data = load_fibril_histograms(database, ts)
    selection = select_model_xmin(
        data,
        model="stretched_cutoff_power_law",
        minimum_xmin=minimum_xmin,
        maximum_xmin=maximum_xmin,
        minimum_tail=minimum_tail,
    )
    fits = _fit_models(data.pooled, selection.selected.xmin)
    selected = fits[-1]
    goodness = tuple(
        fit_block_model_gof(
            data,
            model=model,
            xmin=selection.selected.xmin,
            replicates=replicates,
            seed=seed,
        )
        for model in MODELS
    )
    if not np.isclose(
        selected.ks, goodness[-1].ks, rtol=1e-7, atol=1e-9
    ):
        raise RuntimeError("selected fit and block-GOF fit disagree")
    return ConditionResult(
        ts=ts,
        total_events=int(data.pooled.sum()),
        maximum_size=int(np.flatnonzero(data.pooled)[-1]),
        selected=selected,
        xmin_candidates=tuple(
            selected if fit.xmin == selected.xmin else fit
            for fit in selection.candidates
        ),
        fits=fits,
        goodness=goodness,
    )


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parameter_interval(
    goodness: BlockModelGoodnessOfFit, parameter: str
) -> tuple[float, float]:
    values = np.asarray(
        [replicate.parameters[parameter] for replicate in goodness.bootstrap]
    )
    return tuple(float(value) for value in np.quantile(values, (0.025, 0.975)))


def monte_carlo_interval(
    goodness: BlockModelGoodnessOfFit,
) -> tuple[float, float]:
    interval = stats.binomtest(
        goodness.exceedances, goodness.replicates
    ).proportion_ci(confidence_level=0.95, method="exact")
    return float(interval.low), float(interval.high)


def model_fit_rows(results: list[ConditionResult]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for result in results:
        for fit, goodness in zip(result.fits, result.goodness, strict=True):
            mc_low, mc_high = monte_carlo_interval(goodness)
            row: dict[str, object] = {
                "ts": result.ts,
                "model": fit.model,
                "model_label": MODEL_LABELS[fit.model],
                "xmin": fit.xmin,
                "n_total": result.total_events,
                "n_tail": fit.n_tail,
                "tail_fraction": fit.n_tail / result.total_events,
                "maximum_size": result.maximum_size,
                "scaling_decades": math.log10(result.maximum_size / fit.xmin),
                "parameter_count": fit.parameter_count,
                "log_likelihood": fit.log_likelihood,
                "aic": 2 * fit.parameter_count - 2 * fit.log_likelihood,
                "bic": fit.parameter_count * math.log(fit.n_tail) - 2 * fit.log_likelihood,
                "ks": fit.ks,
                "block_gof_p": goodness.p_value,
                "block_gof_exceedances": goodness.exceedances,
                "block_gof_replicates": goodness.replicates,
                "block_gof_mc_ci_low": mc_low,
                "block_gof_mc_ci_high": mc_high,
                "adequate_at_0_10": goodness.p_value > 0.10,
                **fit.parameters,
            }
            for parameter in fit.parameters:
                low, high = parameter_interval(goodness, parameter)
                row[f"{parameter}_ci_low"] = low
                row[f"{parameter}_ci_high"] = high
            rows.append(row)
    return rows


def bootstrap_rows(results: list[ConditionResult]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for result in results:
        for goodness in result.goodness:
            for replicate in goodness.bootstrap:
                rows.append({
                    "ts": result.ts,
                    "model": goodness.model,
                    "xmin": goodness.xmin,
                    "replicate": replicate.replicate,
                    "ks": replicate.ks,
                    "centered_ks": replicate.centered_ks,
                    **replicate.parameters,
                })
    return rows


def xmin_rows(results: list[ConditionResult]) -> list[dict[str, object]]:
    return [
        {
            "ts": result.ts,
            "xmin": fit.xmin,
            "n_tail": fit.n_tail,
            "log_likelihood": fit.log_likelihood,
            "ks": fit.ks,
            **fit.parameters,
        }
        for result in results
        for fit in result.xmin_candidates
    ]


def comparison_rows(
    database: Path, results: list[ConditionResult]
) -> list[dict[str, object]]:
    """Compare the equal-complexity cutoff and lognormal alternatives."""
    rows: list[dict[str, object]] = []
    for result in results:
        data = load_fibril_histograms(database, result.ts)
        fits = {fit.model: fit for fit in result.fits}
        comparison = _cluster_vuong(
            data, fits["cutoff_power_law"], fits["lognormal"]
        )
        rows.append({
            "ts": result.ts,
            "xmin": result.selected.xmin,
            "first": comparison.first,
            "second": comparison.second,
            "log_likelihood_ratio": comparison.log_likelihood_ratio,
            "cluster_t": comparison.cluster_statistic,
            "p_value": comparison.p_value,
            "favored_by_pooled_likelihood": comparison.favored,
            "test": comparison.test,
        })
    return rows


def plot_ccdfs(
    database: Path, results: list[ConditionResult], path: Path
) -> None:
    columns = 2
    rows = math.ceil(len(results) / columns)
    figure, axes = plt.subplots(
        rows, columns, figsize=(10, 3.7 * rows), constrained_layout=True,
        squeeze=False,
    )
    for axis, result in zip(axes.flat, results, strict=False):
        data = load_fibril_histograms(database, result.ts)
        histogram = data.pooled
        fit = result.selected
        maximum = result.maximum_size
        support = np.arange(fit.xmin, maximum + 1)
        tail = histogram[fit.xmin:maximum + 1]
        empirical = np.cumsum(tail[::-1], dtype=np.int64)[::-1] / fit.n_tail
        probabilities = np.exp(log_probabilities(fit, support))
        model = 1.0 - np.concatenate(([0.0], np.cumsum(probabilities[:-1])))
        block_p = next(
            goodness.p_value for goodness in result.goodness
            if goodness.model == "stretched_cutoff_power_law"
        )
        axis.loglog(support, empirical, ".", ms=2.5, label="empírica")
        axis.loglog(support, model, lw=1.5, label="modelo")
        axis.set_title(
            rf"$T_s={result.ts}$; $s_{{min}}={fit.xmin}$; "
            rf"$p_{{bloco}}={block_p:.3f}$"
        )
        axis.set_xlabel(r"$s$")
        axis.set_ylabel(rf"$P(S\geq s\mid S\geq {fit.xmin})$")
        axis.xaxis.set_major_locator(mticker.LogLocator(base=10, numticks=4))
        axis.xaxis.set_minor_formatter(mticker.NullFormatter())
    for axis in axes.flat[len(results):]:
        axis.set_visible(False)
    axes.flat[0].legend(fontsize=8)
    figure.savefig(path, dpi=200)
    plt.close(figure)


def plot_parameter(
    results: list[ConditionResult],
    parameter: str,
    ylabel: str,
    path: Path,
) -> None:
    ts_values = np.asarray([result.ts for result in results])
    estimates = []
    lows = []
    highs = []
    for result in results:
        goodness = next(
            item for item in result.goodness
            if item.model == "stretched_cutoff_power_law"
        )
        estimate = result.selected.parameters[parameter]
        low, high = parameter_interval(goodness, parameter)
        estimates.append(estimate)
        lows.append(low)
        highs.append(high)
    estimates_array = np.asarray(estimates)
    figure, axis = plt.subplots(figsize=(7.2, 4.5), constrained_layout=True)
    axis.errorbar(
        ts_values,
        estimates_array,
        yerr=(estimates_array - np.asarray(lows), np.asarray(highs) - estimates_array),
        fmt="o-",
        capsize=3,
        lw=1.25,
    )
    format_ts_axis(axis, ts_values)
    axis.set_xlabel(r"$T_s$")
    axis.set_ylabel(ylabel)
    axis.grid(alpha=0.25)
    figure.savefig(path, dpi=200)
    plt.close(figure)


def plot_model_gof(results: list[ConditionResult], path: Path) -> None:
    figure, axis = plt.subplots(figsize=(8.5, 5.0), constrained_layout=True)
    for model in MODELS:
        p_values = [
            next(item.p_value for item in result.goodness if item.model == model)
            for result in results
        ]
        axis.plot(
            [result.ts for result in results], p_values, "o-",
            label=MODEL_LABELS[model], lw=1.1,
        )
    axis.axhline(0.10, color="black", ls="--", lw=1, label="limiar 0,10")
    format_ts_axis(axis, [result.ts for result in results])
    axis.set_ylim(-0.02, 1.02)
    axis.set_xlabel(r"$T_s$")
    axis.set_ylabel(r"$p_{bloco}$")
    axis.grid(alpha=0.25)
    axis.legend(fontsize=8, ncol=2)
    figure.savefig(path, dpi=200)
    plt.close(figure)


def write_xmgrace_ccdfs(
    database: Path, results: list[ConditionResult], path: Path
) -> list[dict[str, object]]:
    """Write alternating empirical/model CCDF sets for direct Grace import."""
    manifest: list[dict[str, object]] = []
    with path.open("w", encoding="utf-8") as stream:
        stream.write("# Individual stretched-cutoff fits; xmgrace XY sets\n")
        stream.write("# Columns: avalanche_size conditional_CCDF\n")
        stream.write("# Sets alternate empirical data and fitted model.\n")
        for result_index, result in enumerate(results):
            data = load_fibril_histograms(database, result.ts)
            histogram = data.pooled
            fit = result.selected
            support = np.arange(fit.xmin, result.maximum_size + 1)
            tail = histogram[fit.xmin:result.maximum_size + 1]
            empirical = np.cumsum(tail[::-1], dtype=np.int64)[::-1] / fit.n_tail
            probabilities = np.exp(log_probabilities(fit, support))
            model = 1.0 - np.concatenate(([0.0], np.cumsum(probabilities[:-1])))
            for kind, values in (("empirical", empirical), ("model", model)):
                set_index = len(manifest)
                stream.write(
                    f"# S{set_index}: Ts={result.ts}; {kind}; xmin={fit.xmin}\n"
                )
                for size, value in zip(support, values, strict=True):
                    stream.write(f"{size:d} {value:.12g}\n")
                manifest.append({
                    "file": path.name,
                    "set": f"S{set_index}",
                    "ts": result.ts,
                    "content": kind,
                    "type": "xy",
                    "xmin": fit.xmin,
                    "points": support.size,
                })
                is_last = (
                    result_index == len(results) - 1 and kind == "model"
                )
                if not is_last:
                    stream.write("&\n")
    return manifest


def write_xmgrace_parameter(
    results: list[ConditionResult], parameter: str, path: Path
) -> None:
    """Write one asymmetric-error xydydy set for a fitted parameter."""
    with path.open("w", encoding="utf-8") as stream:
        stream.write("@type xydydy\n")
        stream.write(
            f"# Columns: Ts {parameter} error_below error_above; 95% block CI\n"
        )
        for result in results:
            goodness = next(
                item for item in result.goodness
                if item.model == "stretched_cutoff_power_law"
            )
            estimate = result.selected.parameters[parameter]
            low, high = parameter_interval(goodness, parameter)
            stream.write(
                f"{result.ts:d} {estimate:.12g} "
                f"{estimate - low:.12g} {high - estimate:.12g}\n"
            )


def write_xmgrace_model_gof(
    results: list[ConditionResult], path: Path
) -> list[dict[str, object]]:
    """Write one XY set per competing model's block goodness-of-fit values."""
    manifest: list[dict[str, object]] = []
    with path.open("w", encoding="utf-8") as stream:
        stream.write("# Block goodness-of-fit; one XY set per model\n")
        stream.write("# Columns: Ts p_block\n")
        for model_index, model in enumerate(MODELS):
            stream.write(f"# S{model_index}: {model}; {MODEL_LABELS[model]}\n")
            for result in results:
                goodness = next(
                    item for item in result.goodness if item.model == model
                )
                stream.write(f"{result.ts:d} {goodness.p_value:.12g}\n")
            manifest.append({
                "file": path.name,
                "set": f"S{model_index}",
                "ts": "all",
                "content": model,
                "type": "xy",
                "xmin": "condition-specific",
                "points": len(results),
            })
            if model_index != len(MODELS) - 1:
                stream.write("&\n")
    return manifest


def write_pooled_counts(
    database: Path, results: list[ConditionResult], package: Path
) -> None:
    """Write the complete preterminal pooled histogram for every condition."""
    for result in results:
        histogram = load_fibril_histograms(database, result.ts).pooled
        total = int(histogram.sum())
        path = package / f"pooled_counts_Ts_{result.ts}.dat"
        with path.open("w", encoding="utf-8") as stream:
            stream.write(f"# Ts = {result.ts}; local preterminal avalanches\n")
            stream.write(f"# total_events = {total}\n")
            stream.write("# Columns: s event_count probability\n")
            for size in np.flatnonzero(histogram):
                count = int(histogram[size])
                stream.write(f"{size:d} {count:d} {count / total:.17g}\n")


def write_xmgrace_package(
    database: Path, results: list[ConditionResult], output: Path
) -> None:
    """Create a self-describing package of figure data for Grace users."""
    package = output / "xmgrace_export"
    package.mkdir(parents=True, exist_ok=False)
    manifest = write_xmgrace_ccdfs(
        database, results, package / "individual_ccdf_xy.dat"
    )
    for parameter in ("alpha", "beta", "scale"):
        write_xmgrace_parameter(
            results, parameter, package / f"ts_vs_{parameter}_xydydy.dat"
        )
    manifest.extend(
        write_xmgrace_model_gof(results, package / "model_gof_xy.dat")
    )
    write_pooled_counts(database, results, package)
    write_csv(package / "sets_manifest.csv", manifest)
    shutil.copyfile(output / "model_fits.csv", package / "model_fits.csv")
    (package / "README.md").write_text(
        """# xmgrace export — individual stretched-cutoff fits

These plain-text files reproduce the numerical content of the report figures.
Comments begin with `#`; `&` separates Grace data sets.

- `individual_ccdf_xy.dat`: alternating empirical and fitted conditional CCDF
  sets. The exact S-number mapping is in `sets_manifest.csv`. Use logarithmic
  x and y axes.
- `ts_vs_alpha_xydydy.dat`, `ts_vs_beta_xydydy.dat`, and
  `ts_vs_scale_xydydy.dat`: estimate with asymmetric lower/upper 95% block
  bootstrap errors. Grace type `xydydy` is declared in each file. Use a base-2
  logarithmic x axis.
- `model_gof_xy.dat`: one XY set per candidate model. Add a horizontal
  reference line at p=0.10 and use a base-2 logarithmic x axis.
- `pooled_counts_Ts_<value>.dat`: complete preterminal pooled histogram for
  one condition. Columns are integer size `s`, integer `event_count`, and
  normalized `probability`. These include the body below the fitted `xmin`.
- `model_fits.csv`: full fit table, included for labels and auditability.

The CCDF is conditioned on each condition-specific selected `xmin`. Fits use
integer, unbinned, local preterminal avalanche sizes. The model is
`p(s) proportional to s^-alpha exp[-(s/scale)^beta]`.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--ts", dest="ts_values", action="append", type=int)
    parser.add_argument("--minimum-xmin", type=int, default=1)
    parser.add_argument("--maximum-xmin", type=int)
    parser.add_argument("--minimum-tail", type=int, default=1000)
    parser.add_argument("--replicates", type=int, default=999)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--seed", type=int, default=271828)
    args = parser.parse_args()

    if args.output.exists() and any(args.output.iterdir()):
        raise SystemExit(f"output directory is not empty: {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)
    ts_values = tuple(args.ts_values or available_ts(args.database))

    results: list[ConditionResult] = []
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                analyze_condition,
                str(args.database),
                ts,
                args.minimum_xmin,
                args.maximum_xmin,
                args.minimum_tail,
                args.replicates,
                args.seed + index * 10_000,
            ): ts
            for index, ts in enumerate(ts_values)
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            stretched_gof = next(
                item for item in result.goodness
                if item.model == "stretched_cutoff_power_law"
            )
            print(
                f"Ts={result.ts}: xmin={result.selected.xmin}, "
                f"KS={result.selected.ks:.6f}, p={stretched_gof.p_value:.4f}",
                flush=True,
            )
    results.sort(key=lambda result: result.ts)

    write_csv(args.output / "model_fits.csv", model_fit_rows(results))
    write_csv(args.output / "block_bootstrap.csv", bootstrap_rows(results))
    write_csv(args.output / "xmin_scan.csv", xmin_rows(results))
    write_csv(
        args.output / "model_comparisons.csv",
        comparison_rows(args.database, results),
    )
    plot_ccdfs(args.database, results, args.output / "individual_ccdf.png")
    plot_parameter(results, "alpha", r"$\alpha$", args.output / "ts_vs_alpha.png")
    plot_parameter(results, "beta", r"$\beta$", args.output / "ts_vs_beta.png")
    plot_parameter(results, "scale", r"$s_c$", args.output / "ts_vs_sc.png")
    plot_model_gof(results, args.output / "model_gof.png")
    write_xmgrace_package(args.database, results, args.output)

    metadata = {
        "model": "p(s) proportional to s^-alpha exp[-(s/sc)^beta]",
        "conditions": list(ts_values),
        "individual_analysis": True,
        "joint_model": False,
        "competing_models": list(MODELS),
        "xmin_selection": "separate minimum KS for the stretched-cutoff model",
        "minimum_xmin": args.minimum_xmin,
        "maximum_xmin": args.maximum_xmin,
        "minimum_tail": args.minimum_tail,
        "block_replicates": args.replicates,
        "block_unit": "fibril geometry",
        "gof_xmin_treatment": "fixed at each condition-specific selected xmin",
        "parameter_intervals": "95% percentile fibril-block bootstrap at fixed xmin",
        "relative_comparison": (
            "cluster-robust Vuong for equal-complexity cutoff-power-law "
            "versus lognormal"
        ),
        "adequacy_threshold": 0.10,
        "seed": args.seed,
        "database": str(args.database.resolve()),
    }
    (args.output / "analysis.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Observed-data model assessment for the two terminal populations."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .data import load_audited_counts
from .models import FitResult, fit_model, model_cdf, model_pmf, observed_arrays
from .synthetic import parametric_gof


PRIMARY_MODELS = ("araujo", "cutoff_power_law", "lognormal", "two_population")


def _flatten_fit(
    ts: int,
    population: str,
    fit: FitResult,
    gof: dict[str, float | int] | None,
) -> dict[str, object]:
    row: dict[str, object] = {
        "ts": ts,
        "population": population,
        "model": fit.model,
        "xmin": fit.xmin,
        "n": fit.n,
        "log_likelihood": fit.log_likelihood,
        "aic": fit.aic,
        "bic": fit.bic,
        "ks": fit.ks,
        "tail_ad": fit.tail_ad,
        "converged": fit.converged,
        "optimizer_message": fit.optimizer_message,
    }
    row.update({f"parameter_{key}": value for key, value in fit.parameters.items()})
    if gof:
        row.update({f"gof_{key}": value for key, value in gof.items()})
    return row


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _plot_population(
    output_dir: Path,
    population: str,
    counts_by_ts: dict[int, np.ndarray],
    fits: dict[tuple[int, str, str], FitResult],
    *,
    kind: str,
) -> None:
    colors = {
        "araujo": "#d1495b",
        "cutoff_power_law": "#00798c",
        "lognormal": "#edae49",
        "two_population": "#30638e",
    }
    figure, axes = plt.subplots(5, 2, figsize=(10.5, 15.5))
    figure.subplots_adjust(top=0.92, bottom=0.05, hspace=0.48, wspace=0.24)
    for axis, ts in zip(axes.flat, sorted(counts_by_ts), strict=True):
        counts = counts_by_ts[ts]
        sizes, frequencies = observed_arrays(counts, 2)
        empirical_pmf = frequencies / frequencies.sum()
        empirical_ccdf = 1.0 - (np.cumsum(frequencies) - frequencies) / frequencies.sum()
        if kind == "ccdf":
            axis.step(sizes, empirical_ccdf, where="post", color="black", linewidth=1.2, label="empirical")
        else:
            axis.scatter(sizes, empirical_pmf, s=7, color="black", alpha=0.65, label="empirical")
        support = np.arange(2, int(sizes[-1]) + 1)
        for model in PRIMARY_MODELS:
            fit = fits[(ts, population, model)]
            if kind == "ccdf":
                _, before = model_cdf(support, fit)
                values = 1.0 - before
            else:
                values = model_pmf(support, fit)
            axis.plot(support, values, color=colors[model], linewidth=1.0, label=model.replace("_", " "))
        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.set_title(rf"$T_s={ts}$")
        axis.grid(alpha=0.2)
        axis.set_xlabel("local event size s")
        axis.set_ylabel("CCDF" if kind == "ccdf" else "PMF")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.967),
        ncol=5,
        frameon=False,
    )
    title_population = "preterminal" if population == "sem_terminal" else "including terminal rupture"
    figure.suptitle(
        f"Exact unbinned {kind.upper()} - {title_population}, s >= 2",
        y=0.993,
    )
    figure.savefig(output_dir / f"observed_{kind}_{population}.png", dpi=180, bbox_inches="tight")
    plt.close(figure)


def _plot_residuals(
    output_dir: Path,
    population: str,
    counts_by_ts: dict[int, np.ndarray],
    fits: dict[tuple[int, str, str], FitResult],
) -> None:
    figure, axes = plt.subplots(5, 2, figsize=(10.5, 15.5))
    figure.subplots_adjust(top=0.92, bottom=0.05, hspace=0.48, wspace=0.24)
    for axis, ts in zip(axes.flat, sorted(counts_by_ts), strict=True):
        sizes, frequencies = observed_arrays(counts_by_ts[ts], 2)
        empirical = np.cumsum(frequencies) / frequencies.sum()
        for model, color in (("araujo", "#d1495b"), ("two_population", "#30638e")):
            after, _ = model_cdf(sizes, fits[(ts, population, model)])
            variance = np.clip(after * (1.0 - after), 1.0 / frequencies.sum(), None)
            axis.plot(sizes, (empirical - after) / np.sqrt(variance), color=color, linewidth=1.0, label=model.replace("_", " "))
        axis.axhline(0.0, color="black", linewidth=0.6)
        axis.set_xscale("log")
        axis.set_title(rf"$T_s={ts}$")
        axis.set_xlabel("local event size s")
        axis.set_ylabel(r"CDF residual / $\sqrt{F(1-F)}$")
        axis.grid(alpha=0.2)
    handles, labels = axes.flat[0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.967),
        ncol=2,
        frameon=False,
    )
    figure.suptitle(
        f"Tail-sensitive residual diagnostics - {population}",
        y=0.993,
    )
    figure.savefig(output_dir / f"observed_residuals_{population}.png", dpi=180, bbox_inches="tight")
    plt.close(figure)


def run_observed_analysis(
    counts_path: Path,
    output_dir: Path,
    *,
    seed: int = 20260818,
    bootstrap_replicates: int = 49,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    audited = load_audited_counts(counts_path)
    fits: dict[tuple[int, str, str], FitResult] = {}
    fit_rows: list[dict[str, object]] = []
    bootstrap_rows: list[dict[str, object]] = []
    sensitivity_rows: list[dict[str, object]] = []
    checkpoint_dir = output_dir / "checkpoints"
    checkpoint_dir.mkdir(exist_ok=True)

    for population in ("sem_terminal", "com_terminal"):
        for ts in sorted(key[0] for key in audited if key[1] == population):
            counts = audited[(ts, population)]
            print(f"observed fits: Ts={ts}, population={population}", flush=True)
            for model_index, model in enumerate(PRIMARY_MODELS):
                checkpoint_model = (
                    "two_population_powerlaw_body"
                    if model == "two_population"
                    else model
                )
                checkpoint = checkpoint_dir / f"ts_{ts}_{population}_{checkpoint_model}.json"
                saved = (
                    json.loads(checkpoint.read_text(encoding="utf-8"))
                    if checkpoint.exists()
                    else None
                )
                checkpoint_matches = saved is not None and (
                    int(saved["gof"].get("replicates", -1)) == bootstrap_replicates
                    or saved["gof"].get("status")
                    == "not_testable_nonfinite_boundary_mle"
                )
                if checkpoint_matches:
                    fit = FitResult(**saved["fit"])
                    summary = saved["gof"]
                    replicates = saved["replicates"]
                else:
                    fit = fit_model(counts, model, xmin=2)
                    lognormal_boundary = (
                        model == "lognormal"
                        and fit.parameters["mu"] < -10.0
                        and fit.parameters["sigma"] > 3.5
                    )
                    if lognormal_boundary:
                        summary = {
                            "replicates": 0,
                            "exceedances": 0,
                            "p_raw": float("nan"),
                            "p_add_one": float("nan"),
                            "p_ci_low": float("nan"),
                            "p_ci_high": float("nan"),
                            "status": "not_testable_nonfinite_boundary_mle",
                        }
                        replicates = []
                    else:
                        summary, replicates = parametric_gof(
                            counts,
                            fit,
                            rng=np.random.default_rng(
                                seed
                                + 100 * ts
                                + 10 * (population == "com_terminal")
                                + model_index
                            ),
                            replicates=bootstrap_replicates,
                        )
                        summary["status"] = "completed"
                    checkpoint.write_text(
                        json.dumps(
                            {
                                "fit": asdict(fit),
                                "gof": summary,
                                "replicates": replicates,
                            },
                            indent=2,
                        )
                        + "\n",
                        encoding="utf-8",
                    )
                fits[(ts, population, model)] = fit
                fit_rows.append(_flatten_fit(ts, population, fit, summary))
                for row in replicates:
                    bootstrap_rows.append(
                        {"ts": ts, "population": population, "model": model, **row}
                    )
            sensitivity_checkpoint = (
                checkpoint_dir / f"ts_{ts}_{population}_discretization.json"
            )
            if sensitivity_checkpoint.exists():
                sensitivity_row = json.loads(
                    sensitivity_checkpoint.read_text(encoding="utf-8")
                )
            else:
                integrated = fit_model(counts, "araujo_integrated", xmin=2)
                primary = fits[(ts, population, "araujo")]
                sensitivity_row = {
                    "ts": ts,
                    "population": population,
                    "primary_alpha": primary.parameters["alpha"],
                    "integrated_alpha": integrated.parameters["alpha"],
                    "primary_eta": primary.parameters["eta"],
                    "integrated_eta": integrated.parameters["eta"],
                    "primary_s0": primary.parameters["s0"],
                    "integrated_s0": integrated.parameters["s0"],
                    "primary_log_likelihood": primary.log_likelihood,
                    "integrated_log_likelihood": integrated.log_likelihood,
                    "primary_ks": primary.ks,
                    "integrated_ks": integrated.ks,
                }
                sensitivity_checkpoint.write_text(
                    json.dumps(sensitivity_row, indent=2) + "\n", encoding="utf-8"
                )
            sensitivity_rows.append(sensitivity_row)

    # Parametric interval estimates are model-based event-level intervals only.
    groups: dict[tuple[int, str, str], list[dict[str, object]]] = {}
    for row in bootstrap_rows:
        groups.setdefault((int(row["ts"]), str(row["population"]), str(row["model"])), []).append(row)
    interval_rows: list[dict[str, object]] = []
    for key, rows in groups.items():
        parameter_names = sorted({name.removeprefix("parameter_") for row in rows for name in row if name.startswith("parameter_")})
        for parameter in parameter_names:
            values = np.asarray([float(row[f"parameter_{parameter}"]) for row in rows if f"parameter_{parameter}" in row])
            interval_rows.append(
                {
                    "ts": key[0],
                    "population": key[1],
                    "model": key[2],
                    "parameter": parameter,
                    "estimate": fits[key].parameters[parameter],
                    "bootstrap_median": float(np.median(values)),
                    "ci_2_5": float(np.quantile(values, 0.025)),
                    "ci_97_5": float(np.quantile(values, 0.975)),
                    "uncertainty_scope": "parametric iid-event; not hierarchical by fibril",
                }
            )

    _write_csv(output_dir / "observed_model_fits.csv", fit_rows)
    _write_csv(output_dir / "observed_bootstrap_replicates.csv", bootstrap_rows)
    _write_csv(output_dir / "observed_parameter_intervals.csv", interval_rows)
    _write_csv(output_dir / "discretization_sensitivity.csv", sensitivity_rows)

    for population in ("sem_terminal", "com_terminal"):
        selected = {ts: values for (ts, label), values in audited.items() if label == population}
        _plot_population(output_dir, population, selected, fits, kind="ccdf")
        _plot_population(output_dir, population, selected, fits, kind="pmf")
        _plot_residuals(output_dir, population, selected, fits)

    decisions: list[dict[str, object]] = []
    for population in ("sem_terminal", "com_terminal"):
        for ts in sorted(key[0] for key in audited if key[1] == population):
            rows = [row for row in fit_rows if row["ts"] == ts and row["population"] == population]
            best = min(rows, key=lambda row: float(row["bic"]))
            araujo = next(row for row in rows if row["model"] == "araujo")
            adequate = float(araujo["gof_p_ci_high"]) > 0.1 and float(araujo["gof_p_add_one"]) > 0.1
            if adequate:
                decision = "adequate on the full prespecified support"
            elif best["model"] == "araujo":
                decision = "relatively better but absolutely rejected"
            else:
                decision = "not supported"
            decisions.append(
                {
                    "ts": ts,
                    "population": population,
                    "araujo_decision": decision,
                    "best_bic_model": best["model"],
                    "delta_bic_araujo_from_best": float(araujo["bic"]) - float(best["bic"]),
                    "araujo_gof_p_add_one": araujo["gof_p_add_one"],
                    "araujo_gof_ci_high": araujo["gof_p_ci_high"],
                }
            )
    _write_csv(output_dir / "scientific_decisions.csv", decisions)
    summary = {
        "master_seed": seed,
        "bootstrap_replicates_per_fit": bootstrap_replicates,
        "primary_population": "sem_terminal",
        "sensitivity_population": "com_terminal",
        "support": "all exact integer event sizes s >= 2",
        "models": list(PRIMARY_MODELS),
        "uncertainty_warning": (
            "Intervals and parametric goodness-of-fit operate on aggregated event counts. "
            "They do not preserve fibril/realization identity and must not be used as "
            "hierarchical uncertainty for a manuscript claim."
        ),
        "mechanistic_boundary": (
            "Araújo et al. describe backbone mass between two sites in critical 2D "
            "percolation. Here s is a connected local-damage cluster during driven "
            "3D fibril rupture. Relative empirical fit does not transfer the percolation "
            "mechanism, exponent-fractal-dimension relation, SOC, or universality."
        ),
    }
    (output_dir / "observed_analysis_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    return summary

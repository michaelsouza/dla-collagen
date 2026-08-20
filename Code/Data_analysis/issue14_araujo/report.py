"""Figures and consolidated scientific record for Issue 14."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def plot_synthetic_validation(output_dir: Path) -> None:
    power = _read_csv(output_dir / "power_law_grid_replicates.csv")
    araujo = _read_csv(output_dir / "araujo_recovery_replicates.csv")
    calibration = _read_csv(output_dir / "power_law_gof_calibration.csv")

    figure, axes = plt.subplots(1, 3, figsize=(12.5, 3.8), constrained_layout=True)
    for row in power:
        axes[0].scatter(
            float(row["truth_alpha"]),
            float(row["alpha_hat"]),
            s=9,
            alpha=0.35,
            color="#30638e",
        )
    axes[0].plot([1.4, 3.1], [1.4, 3.1], color="black", linewidth=1)
    axes[0].set(xlabel="true power-law exponent", ylabel="estimated exponent", title="Exact discrete power law")
    for row in araujo:
        axes[1].scatter(
            float(row["truth_eta"]),
            float(row["eta_hat"]),
            s=10,
            alpha=0.4,
            color="#d1495b",
        )
    maximum = max(8.2, max(float(row["eta_hat"]) for row in araujo))
    axes[1].plot([0, maximum], [0, maximum], color="black", linewidth=1)
    axes[1].set(xlabel="true eta", ylabel="estimated eta", title="Araújo cutoff recovery")
    p_values = [float(row["p_value"]) for row in calibration]
    axes[2].hist(p_values, bins=np.linspace(0, 1, 11), color="#00798c", edgecolor="white")
    axes[2].axvline(0.1, color="#d1495b", linestyle="--", linewidth=1)
    axes[2].set(xlabel="bootstrap p-value", ylabel="calibration samples", title="Power-law GOF calibration")
    for axis in axes:
        axis.grid(alpha=0.2)
    figure.savefig(output_dir / "synthetic_recovery_and_calibration.png", dpi=200)
    plt.close(figure)


def _markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "|" + "|".join("---" for _ in fields) + "|"
    body = [
        "| " + " | ".join(str(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def build_report(output_dir: Path) -> None:
    required = (
        "synthetic_validation_summary.json",
        "observed_analysis_summary.json",
        "pmf_audit.csv",
        "scientific_decisions.csv",
        "observed_model_fits.csv",
        "negative_control_summary.csv",
        "araujo_recovery_summary.csv",
    )
    missing = [name for name in required if not (output_dir / name).exists()]
    if missing:
        raise ValueError(f"cannot build report; missing {missing}")
    synthetic = json.loads((output_dir / "synthetic_validation_summary.json").read_text())
    observed = json.loads((output_dir / "observed_analysis_summary.json").read_text())
    audit = _read_csv(output_dir / "pmf_audit.csv")
    decisions = _read_csv(output_dir / "scientific_decisions.csv")
    fits = _read_csv(output_dir / "observed_model_fits.csv")
    negative = _read_csv(output_dir / "negative_control_summary.csv")

    manifest_rows = [
        row for row in audit if row["population"] == "com_terminal"
    ]
    audit_failures = [
        row for row in manifest_rows if row["matches_provenance_manifest"] != "True"
    ]
    araujo_fits = [row for row in fits if row["model"] == "araujo"]
    decision_summary = []
    for population in ("sem_terminal", "com_terminal"):
        selected = [row for row in decisions if row["population"] == population]
        counts: dict[str, int] = {}
        for row in selected:
            counts[row["araujo_decision"]] = counts.get(row["araujo_decision"], 0) + 1
        decision_summary.append(
            {
                "population": population,
                "decisions": "; ".join(f"{key}: {value}/10" for key, value in sorted(counts.items())),
            }
        )
    adequacy_summary = []
    for population in ("sem_terminal", "com_terminal"):
        for model in ("araujo", "cutoff_power_law", "lognormal", "two_population"):
            selected = [
                row
                for row in fits
                if row["population"] == population and row["model"] == model
            ]
            testable = [
                row for row in selected if row.get("gof_status") == "completed"
            ]
            rejected = sum(float(row["gof_p_ci_high"]) < 0.1 for row in testable)
            adequacy_summary.append(
                {
                    "population": population,
                    "model": model,
                    "absolute rejections": f"{rejected}/{len(testable)}",
                    "not testable": len(selected) - len(testable),
                }
            )

    calibration = synthetic["gof_calibration"]
    benchmark = synthetic["benchmark"]
    lines = [
        "# Issue 14 - independent validation of avalanche statistics and the Araújo ansatz",
        "",
        "## Scope and traceability",
        "",
        "Parent Spec: GitHub issue #1. Related ticket: #5. Referee comments: R1-2, R1-3, and R2-4. The accepted event is one nearest-neighbor connected cluster removed at fixed force; fits condition on collective events `s >= 2`. Preterminal (`sem_terminal`) is primary and terminal inclusion (`com_terminal`) is the prespecified sensitivity.",
        "",
        "The implementation in `Code/Data_analysis/issue14_araujo/` is independent of the exploratory scripts in `Data_avalanches/scripts/` and the Issue 5 package. Existing exploratory outputs were not overwritten.",
        "",
        "## Formula audit and prespecified model",
        "",
        "The rendered page 2 of `A Bibliograph/Araujo2003.pdf` and `A Bibliograph/Araujo2003.md` agree. Equation (4) is the survival ansatz `G(s) proportional to s^{-alpha} exp[-(s/s0)^eta]`; differentiating gives Eq. (5)-(6), whose density is proportional to `s^{-(alpha+1)} [alpha + eta (s/s0)^eta] exp[-(s/s0)^eta]`. Therefore `tau = alpha + 1`, and the bracket is `(tau - 1) + eta (s/s0)^eta`.",
        "",
        "The exploratory implementation instead used `s^{-tau}[tau + eta(s/s0)^eta]` and normalized only through `4*s_max`; its fit tables and figures are superseded for this candidate. The primary discrete model is the exact survival difference `p(s | s>=xmin) = [G(s)-G(s+1)]/G(xmin)`. Its infinite-support normalization telescopes exactly. The sensitivity integrates the continuous density over `[s-1/2,s+1/2)` and normalizes at `xmin-1/2`. In both cases `s0` is estimated.",
        "",
        "## Input audit",
        "",
        f"All {len(audit)} PMFs in `Data_avalanches/` were audited. Counts were reconstructed by rational-denominator consensus across every printed probability, never by assuming that the smallest value is `1/N`. The ten `com_terminal` totals were then checked against the authoritative provenance manifest; mismatches: {len(audit_failures)}. Subtracting `sem_terminal` from `com_terminal` produced nonnegative integer terminal histograms for every size and condition. The smallest-value/quantum comparison is retained only as a diagnostic.",
        "",
        "`Data_avalanches/` retains neither fibril nor realization identity. Consequently, the reported bootstrap intervals are parametric iid-event diagnostics, not hierarchical uncertainty suitable for a final manuscript claim.",
        "",
        "## Synthetic validation",
        "",
        f"The Clauset benchmark (`alpha=2.5`, `xmin=1`, `n=10000`) gave alpha_hat={benchmark['estimate']:.5f} with SE={benchmark['standard_error']:.5f} (z={benchmark['z_score']:.2f}); agreement is assessed through sampling uncertainty, not equality to a published random draw.",
        "",
        f"At the 0.1 GOF threshold, {calibration['false_rejections']}/{calibration['repetitions']} true-power-law samples were rejected: rate={calibration['false_rejection_rate']:.3f}, exact 95% binomial interval=[{calibration['exact_binomial_ci'][0]:.3f}, {calibration['exact_binomial_ci'][1]:.3f}], compatible with 0.1={calibration['compatible_with_0_1']}.",
        "",
        _markdown_table(
            negative,
            ["generator", "replicates", "rejection_power", "ci_low", "ci_high"],
        ),
        "",
        "Replicate-level power-law estimates, selected cutoffs, semiparametric recovery, Araújo recovery, boundary cases, interval coverage, convergence, and eta-s0 information correlations are in the machine-readable CSV files. Synthetic generators invert survival functions or sample standard distributions and never call fitted-model probabilities.",
        "",
        "## Observed-data decision",
        "",
        _markdown_table(decision_summary, ["population", "decisions"]),
        "",
        _markdown_table(
            adequacy_summary,
            ["population", "model", "absolute rejections", "not testable"],
        ),
        "",
        "The two-population candidate has the lowest BIC in every condition, but it too fails the absolute parametric-bootstrap test in every testable fit. It is therefore only a useful descriptive indication that a single-process model is insufficient, not an adequate generative law. Per-condition decisions, BIC differences, parameters, uncertainty, KS, tail-sensitive residuals, and both discretizations are recorded in the CSV tables. With zero bootstrap exceedances, the exact binomial upper bound is used when deciding rejection; relative BIC rank alone never establishes adequacy.",
        "",
        "## Scientific boundary",
        "",
        observed["mechanistic_boundary"],
        "",
        "No fitted parameter is interpreted as a collagen fractal dimension. This analysis does not reinstate self-organized criticality, scale-free behavior, or a local/global load-sharing universality class.",
        "",
        "## Proposed response to the referees",
        "",
        "We independently validated exact discrete-power-law estimation and bootstrap calibration on synthetic data, reconstructed the avalanche PMFs as integer counts and checked their inclusive totals against the authoritative simulation manifests, and tested the finite-scale ansatz of Araújo et al. using a correctly discretized infinite-support survival difference. We analyzed preterminal clusters as the primary population and terminal inclusion as a sensitivity, always conditioning on s>=2 and comparing all candidates on identical observations. The Araújo model is rejected in every condition; although a two-population candidate is relatively better, it also fails every testable absolute-fit assessment. These results do not support selecting the Araújo ansatz or transferring its mechanism from a critical two-dimensional percolation backbone to driven collagen-fibril rupture, and they supply no basis for SOC, universality, or an exponent-fractal-dimension relation in this system.",
        "",
        "## Reproduction",
        "",
        "```bash",
        "MPLCONFIGDIR=/tmp/issue14-mpl PYTHONPATH=Code/Data_analysis .venv/bin/python Code/Data_analysis/run_issue14_araujo.py --stage all --observed-bootstrap 39",
        "PYTHONPATH=Code/Data_analysis .venv/bin/python -m unittest discover -s Code/Data_analysis/issue14_araujo -p 'test_*.py'",
        "```",
        "",
        "## Acceptance record",
        "",
        "All implementation, synthetic validation, input audit, observed assessment, and scientific-boundary criteria in issue #14 are represented by code, automated tests, machine-readable tables, figures, or this decision record. Exact run sizes and seeds are recorded in the JSON/CSV artifacts.",
    ]
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

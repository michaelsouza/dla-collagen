#!/usr/bin/env python3
"""Compare published ensemble D_f with original-backbone descriptors.

The input table is produced by ``validate_fractal_proxy.py``.  Each row pairs
an auxiliary, laterally grown fibril with structural descriptors extracted
from the original fibril used in the rupture simulation.  The publication
diagnostic uses the ten ensemble D_f values already reported in ``df_ts.dat``;
individual-fibril D_f estimates are not used as primary measurements.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import BoundaryNorm, ListedColormap
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, rankdata, spearmanr


STYLE_PATH = Path(__file__).with_name("xmgrace_paper.mplstyle")
plt.style.use(STYLE_PATH)


DESCRIPTORS = {
    "backbone_mean_n_201": r"Mean load-bearing area, $\overline{N}$",
    "backbone_min_n_201": r"Minimum load-bearing area, $N_{\min}$",
    "backbone_cv_n_201": r"Axial variation of load-bearing area, CV$(N)$",
    "backbone_mean_coordination": r"Mean molecular coordination, $\overline{K}$",
    "backbone_mean_unit_stress": r"Mean stress exposure at $F=1$",
    "backbone_max_unit_stress": r"Maximum stress exposure at $F=1$",
    "backbone_rods": "Number of backbone molecules",
    "backbone_rod_fraction": "Backbone molecule fraction",
    "backbone_mean_void_fraction": "Mean void fraction in the mechanical window",
    "backbone_max_void_fraction": "Maximum void fraction in the mechanical window",
    "full_mean_n_11": "Mean cross-sectional mass of grown fibril",
    "full_mean_packing_fraction_11": "Packing fraction of grown fibril",
}

PLOT_DESCRIPTORS = (
    "backbone_mean_n_201",
    "backbone_mean_coordination",
    "backbone_cv_n_201",
    "backbone_mean_unit_stress",
)

PLOT_AXIS_LABELS = {
    "backbone_mean_n_201": r"$\langle N\rangle$",
    "backbone_mean_coordination": r"$\langle K\rangle$",
    "backbone_cv_n_201": r"$\mathrm{CV}(N)$",
    "backbone_mean_unit_stress": r"$\langle\sigma_M\rangle_{F=1}$",
}


def correlation(x: np.ndarray, y: np.ndarray, kind: str) -> float:
    if kind == "pearson":
        return float(pearsonr(x, y).statistic)
    if kind == "spearman":
        return float(spearmanr(x, y).statistic)
    raise ValueError(f"Unknown correlation kind: {kind}")


def condition_mean_correlation(
    data: pd.DataFrame,
    descriptor: str,
    kind: str,
) -> float:
    means = data.groupby("ts", sort=True)[["df", descriptor]].mean()
    return correlation(
        means["df"].to_numpy(),
        means[descriptor].to_numpy(),
        kind,
    )


def within_condition_correlation(
    data: pd.DataFrame,
    descriptor: str,
    rank: bool,
) -> float:
    columns = ["df", descriptor]
    values = data[["ts", *columns]].copy()
    if rank:
        for column in columns:
            values[column] = values.groupby("ts")[column].rank(
                method="average",
                pct=True,
            )
    centered = values[columns] - values.groupby("ts")[columns].transform("mean")
    return correlation(
        centered["df"].to_numpy(),
        centered[descriptor].to_numpy(),
        "pearson",
    )


def percentile_interval(values: np.ndarray) -> tuple[float, float]:
    finite = values[np.isfinite(values)]
    if len(finite) == 0:
        return float("nan"), float("nan")
    low, high = np.percentile(finite, [2.5, 97.5])
    return float(low), float(high)


def fast_pearson(x: np.ndarray, y: np.ndarray) -> float:
    x_centered = x - np.mean(x)
    y_centered = y - np.mean(y)
    denominator = np.sqrt(
        np.sum(x_centered**2) * np.sum(y_centered**2)
    )
    if denominator == 0:
        return float("nan")
    return float(np.sum(x_centered * y_centered) / denominator)


def fast_spearman(x: np.ndarray, y: np.ndarray) -> float:
    return fast_pearson(rankdata(x), rankdata(y))


def bootstrap_correlations(
    data: pd.DataFrame,
    descriptor: str,
    replicates: int,
    rng: np.random.Generator,
) -> dict[str, tuple[float, float]]:
    grouped = [
        group[["df", descriptor]].to_numpy()
        for _ts, group in data.groupby("ts", sort=True)
    ]
    estimates = {
        "overall_spearman": np.empty(replicates),
        "condition_mean_spearman": np.empty(replicates),
        "within_condition_pearson": np.empty(replicates),
        "within_condition_rank": np.empty(replicates),
    }

    for index in range(replicates):
        sampled_groups = [
            group[rng.integers(0, len(group), size=len(group))]
            for group in grouped
        ]
        sample = np.vstack(sampled_groups)
        estimates["overall_spearman"][index] = fast_spearman(
            sample[:, 0],
            sample[:, 1],
        )
        condition_means = np.vstack(
            [np.mean(group, axis=0) for group in sampled_groups]
        )
        estimates["condition_mean_spearman"][index] = fast_spearman(
            condition_means[:, 0],
            condition_means[:, 1],
        )

        centered_groups = [
            group - np.mean(group, axis=0)
            for group in sampled_groups
        ]
        centered = np.vstack(centered_groups)
        estimates["within_condition_pearson"][index] = fast_pearson(
            centered[:, 0],
            centered[:, 1],
        )

        ranked_groups = []
        for group in sampled_groups:
            ranked = np.column_stack(
                (rankdata(group[:, 0]), rankdata(group[:, 1]))
            )
            ranked_groups.append(ranked - np.mean(ranked, axis=0))
        ranked_centered = np.vstack(ranked_groups)
        estimates["within_condition_rank"][index] = fast_pearson(
            ranked_centered[:, 0],
            ranked_centered[:, 1],
        )

    return {
        name: percentile_interval(values)
        for name, values in estimates.items()
    }


def summarize_df(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for ts, group in data.groupby("ts", sort=True):
        rows.append(
            {
                "ts": int(ts),
                "fibrils": len(group),
                "mean_df": group["df"].mean(),
                "sd_df": group["df"].std(ddof=1),
                "sem_df": group["df"].sem(ddof=1),
                "min_df": group["df"].min(),
                "max_df": group["df"].max(),
                "mean_fit_r_squared": group["df_fit_r_squared"].mean(),
                "min_fit_r_squared": group["df_fit_r_squared"].min(),
                "df_above_2": int((group["df"] > 2.0).sum()),
            }
        )
    return pd.DataFrame(rows)


def summarize_conditions(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for ts, group in data.groupby("ts", sort=True):
        row: dict[str, float | int] = {
            "ts": int(ts),
            "fibrils": len(group),
            "mean_df": group["df"].mean(),
            "sem_df": group["df"].sem(ddof=1),
        }
        for descriptor in DESCRIPTORS:
            row[f"mean_{descriptor}"] = group[descriptor].mean()
            row[f"sem_{descriptor}"] = group[descriptor].sem(ddof=1)
        rows.append(row)
    return pd.DataFrame(rows)


def analyze_correlations(
    data: pd.DataFrame,
    replicates: int,
    seed: int,
) -> pd.DataFrame:
    rows = []
    seed_sequence = np.random.SeedSequence(seed)
    child_seeds = seed_sequence.spawn(len(DESCRIPTORS))

    for (descriptor, label), child_seed in zip(DESCRIPTORS.items(), child_seeds):
        intervals = bootstrap_correlations(
            data,
            descriptor,
            replicates,
            np.random.default_rng(child_seed),
        )
        overall_ci = intervals["overall_spearman"]
        condition_ci = intervals["condition_mean_spearman"]
        within_pearson_ci = intervals["within_condition_pearson"]
        within_rank_ci = intervals["within_condition_rank"]
        rows.append(
            {
                "descriptor": descriptor,
                "label": label,
                "n_fibrils": len(data),
                "n_conditions": data["ts"].nunique(),
                "overall_spearman": correlation(
                    data["df"].to_numpy(),
                    data[descriptor].to_numpy(),
                    "spearman",
                ),
                "overall_spearman_ci_low": overall_ci[0],
                "overall_spearman_ci_high": overall_ci[1],
                "condition_mean_pearson": condition_mean_correlation(
                    data,
                    descriptor,
                    "pearson",
                ),
                "condition_mean_spearman": condition_mean_correlation(
                    data,
                    descriptor,
                    "spearman",
                ),
                "condition_mean_spearman_ci_low": condition_ci[0],
                "condition_mean_spearman_ci_high": condition_ci[1],
                "within_condition_pearson": within_condition_correlation(
                    data,
                    descriptor,
                    rank=False,
                ),
                "within_condition_pearson_ci_low": within_pearson_ci[0],
                "within_condition_pearson_ci_high": within_pearson_ci[1],
                "within_condition_rank": within_condition_correlation(
                    data,
                    descriptor,
                    rank=True,
                ),
                "within_condition_rank_ci_low": within_rank_ci[0],
                "within_condition_rank_ci_high": within_rank_ci[1],
            }
        )
    return pd.DataFrame(rows)


def sensitivity_analysis(data: pd.DataFrame) -> pd.DataFrame:
    subsets = {
        "all_fibrils": data,
        "df_at_most_2": data.loc[data["df"] <= 2.0],
        "fit_r_squared_at_least_0.995": data.loc[
            data["df_fit_r_squared"] >= 0.995
        ],
    }
    rows = []
    for subset_name, subset in subsets.items():
        for descriptor, label in DESCRIPTORS.items():
            rows.append(
                {
                    "subset": subset_name,
                    "descriptor": descriptor,
                    "label": label,
                    "n_fibrils": len(subset),
                    "condition_mean_spearman": condition_mean_correlation(
                        subset,
                        descriptor,
                        "spearman",
                    ),
                    "within_condition_pearson": within_condition_correlation(
                        subset,
                        descriptor,
                        rank=False,
                    ),
                    "within_condition_rank": within_condition_correlation(
                        subset,
                        descriptor,
                        rank=True,
                    ),
                }
            )
    return pd.DataFrame(rows)


def analyze_published_condition_correlations(
    condition_summary: pd.DataFrame,
    ensemble_validation: pd.DataFrame,
) -> pd.DataFrame:
    published = ensemble_validation[
        ["ts", "published_df", "published_fit_error"]
    ].copy()
    merged = condition_summary.merge(
        published,
        on="ts",
        how="inner",
        validate="one_to_one",
    )
    if len(merged) != len(condition_summary):
        raise ValueError("Published D_f is missing for one or more T_s values")

    rows = []
    for descriptor, label in DESCRIPTORS.items():
        y_column = f"mean_{descriptor}"
        pearson = pearsonr(merged["published_df"], merged[y_column])
        spearman = spearmanr(merged["published_df"], merged[y_column])
        rows.append(
            {
                "descriptor": descriptor,
                "label": label,
                "n_conditions": len(merged),
                "pearson_r": float(pearson.statistic),
                "pearson_p": float(pearson.pvalue),
                "spearman_rho": float(spearman.statistic),
                "spearman_p": float(spearman.pvalue),
            }
        )
    return pd.DataFrame(rows)


def plot_validation(
    condition_summary: pd.DataFrame,
    ensemble_validation: pd.DataFrame,
    correlations: pd.DataFrame,
    output_path: Path,
) -> None:
    plot_data = condition_summary.merge(
        ensemble_validation[["ts", "published_df", "published_fit_error"]],
        on="ts",
        how="inner",
        validate="one_to_one",
    ).sort_values("ts")
    ts_values = plot_data["ts"].tolist()
    colors = plt.get_cmap("viridis")(
        np.linspace(0.05, 0.95, len(ts_values))
    )
    color_by_ts = dict(zip(ts_values, colors))
    discrete_map = ListedColormap(colors)
    discrete_norm = BoundaryNorm(
        np.arange(-0.5, len(ts_values) + 0.5),
        discrete_map.N,
    )

    figure, axes = plt.subplots(2, 2, figsize=(10.2, 7.6), constrained_layout=True)
    for panel, (axis, descriptor) in enumerate(
        zip(axes.flat, PLOT_DESCRIPTORS)
    ):
        mean_column = f"mean_{descriptor}"
        sem_column = f"sem_{descriptor}"
        for condition in plot_data.itertuples(index=False):
            color = color_by_ts[condition.ts]
            axis.errorbar(
                condition.published_df,
                getattr(condition, mean_column),
                xerr=condition.published_fit_error,
                yerr=getattr(condition, sem_column),
                fmt="o",
                markersize=7.5,
                color=color,
                markeredgecolor="black",
                markeredgewidth=1.0,
                elinewidth=1.2,
                capsize=3.5,
                zorder=5,
            )
        row = correlations.loc[
            correlations["descriptor"] == descriptor
        ].iloc[0]
        annotation_x = 0.05 if panel < 2 else 0.95
        annotation_alignment = "left" if panel < 2 else "right"
        axis.text(
            annotation_x,
            0.88,
            rf"$\rho={row['spearman_rho']:.2f}$",
            transform=axis.transAxes,
            ha=annotation_alignment,
            va="top",
            fontsize=13,
        )
        axis.set_xlabel(r"$D_f$")
        axis.set_ylabel(PLOT_AXIS_LABELS[descriptor])
        axis.minorticks_on()
        axis.text(
            annotation_x,
            0.97,
            f"({chr(ord('a') + panel)})",
            transform=axis.transAxes,
            ha=annotation_alignment,
            va="top",
            fontsize=13,
            fontweight="bold",
        )

    colorbar = figure.colorbar(
        ScalarMappable(norm=discrete_norm, cmap=discrete_map),
        ax=axes,
        ticks=np.arange(len(ts_values)),
        shrink=0.78,
        pad=0.02,
    )
    colorbar.ax.set_yticklabels([str(ts) for ts in ts_values])
    colorbar.set_label(r"$T_s$")
    colorbar.outline.set_edgecolor("black")
    colorbar.outline.set_linewidth(1.8)
    colorbar.ax.tick_params(
        which="both",
        direction="in",
        left=True,
        right=True,
        width=1.4,
    )
    figure.savefig(output_path, dpi=300)
    figure.savefig(output_path.with_suffix(".pdf"))
    figure.savefig(output_path.with_suffix(".eps"))
    plt.close(figure)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--ensemble-validation", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = pd.read_csv(args.input)
    ensemble_validation = pd.read_csv(args.ensemble_validation)
    mechanical_area = float((2 * 8 + 1) ** 2)
    data["backbone_mean_void_fraction"] = (
        1.0 - data["backbone_mean_n_201"] / mechanical_area
    )
    data["backbone_max_void_fraction"] = (
        1.0 - data["backbone_min_n_201"] / mechanical_area
    )
    required = {
        "ts",
        *DESCRIPTORS,
    }
    missing = sorted(required - set(data.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    condition_summary = summarize_conditions(data)
    correlations = analyze_published_condition_correlations(
        condition_summary,
        ensemble_validation,
    )

    condition_summary.to_csv(
        args.output_dir / "condition_descriptor_summary.csv",
        index=False,
    )
    correlations.to_csv(
        args.output_dir / "proxy_correlations.csv",
        index=False,
    )
    plot_validation(
        condition_summary,
        ensemble_validation,
        correlations,
        args.output_dir / "fractal_proxy_validation.png",
    )

    print(correlations.to_string(index=False))
    print(f"Wrote diagnostics to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

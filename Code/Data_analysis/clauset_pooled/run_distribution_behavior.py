#!/usr/bin/env python3
"""Run nonparametric behavior analyses on complete local-avalanche sizes."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform

from .distribution_behavior import (
    ccdf_crossings,
    characteristic_size,
    lorenz_curve,
    normalized_quantile_distance,
    split_two_scales,
    top_event_damage_share,
)
from .full_distribution import distribution_distance, histogram_quantiles
from .power_law import read_size_histogram


TOP_FRACTIONS = (0.10, 0.01, 0.001, 0.0001)


def _write(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _silhouette(distance: np.ndarray, labels: np.ndarray) -> float:
    values: list[float] = []
    for index, label in enumerate(labels):
        same = np.flatnonzero(labels == label)
        same = same[same != index]
        if same.size == 0:
            values.append(0.0)
            continue
        within = float(distance[index, same].mean())
        between = min(
            float(distance[index, labels == other].mean())
            for other in np.unique(labels)
            if other != label
        )
        values.append((between - within) / max(within, between))
    return float(np.mean(values))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    paths = sorted(
        args.input_dir.glob("ts_*.txt"),
        key=lambda path: int(path.stem.removeprefix("ts_")),
    )
    if not paths:
        raise SystemExit("no ts_*.txt input files")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    histograms: dict[int, np.ndarray] = {}
    splits = {}
    summary_rows: list[dict[str, object]] = []
    lorenz_rows: list[dict[str, object]] = []
    for path in paths:
        ts = int(path.stem.removeprefix("ts_"))
        histogram = read_size_histogram(path, minimum_size=2)
        histograms[ts] = histogram
        split = split_two_scales(histogram, minimum_size=2)
        splits[ts] = split
        quantiles = histogram_quantiles(histogram, (0.50, 0.90, 0.99, 0.999))
        row: dict[str, object] = {
            "ts": ts,
            "n_events_s_ge_2": int(histogram.sum()),
            "total_avalanche_size": int(
                np.dot(np.arange(histogram.size, dtype=np.int64), histogram)
            ),
            "q50": quantiles[0],
            "q90": quantiles[1],
            "q99": quantiles[2],
            "q999": quantiles[3],
            "q99_over_q90": quantiles[2] / quantiles[1],
            "q999_over_q90": quantiles[3] / quantiles[1],
            "characteristic_size_s2_over_s1": characteristic_size(histogram),
            **asdict(split),
        }
        for fraction in TOP_FRACTIONS:
            actual, damage = top_event_damage_share(histogram, fraction)
            label = str(fraction).replace(".", "p")
            row[f"top_{label}_actual_event_fraction"] = actual
            row[f"top_{label}_size_share"] = damage
        summary_rows.append(row)
        event_fraction, size_fraction = lorenz_curve(histogram, points=1001)
        lorenz_rows.extend(
            {
                "ts": ts,
                "event_fraction": event,
                "cumulative_size_fraction": size,
            }
            for event, size in zip(event_fraction, size_fraction, strict=True)
        )
        print(
            f"Ts={ts}: split {split.small_maximum}|{split.large_minimum}; "
            f"large={split.large_fraction:.5f}",
            flush=True,
        )

    ts_values = sorted(histograms)
    crossing_rows: list[dict[str, object]] = []
    for first_ts, second_ts in zip(ts_values, ts_values[1:]):
        crossings = ccdf_crossings(histograms[first_ts], histograms[second_ts])
        if not crossings:
            crossing_rows.append(
                {
                    "ts_first": first_ts,
                    "ts_second": second_ts,
                    "crossing_index": "",
                    "size_before_crossing": "",
                    "difference_before": "",
                    "difference_after": "",
                }
            )
        else:
            crossing_rows.extend(
                {
                    "ts_first": first_ts,
                    "ts_second": second_ts,
                    "crossing_index": index,
                    "size_before_crossing": size,
                    "difference_before": before,
                    "difference_after": after,
                }
                for index, (size, before, after) in enumerate(crossings, start=1)
            )

    large_distance_rows: list[dict[str, object]] = []
    js_matrix = np.zeros((len(ts_values), len(ts_values)), dtype=float)
    for first_index, first_ts in enumerate(ts_values):
        for second_index in range(first_index + 1, len(ts_values)):
            second_ts = ts_values[second_index]
            distance = normalized_quantile_distance(
                histograms[first_ts],
                histograms[second_ts],
                first_minimum=splits[first_ts].large_minimum,
                second_minimum=splits[second_ts].large_minimum,
            )
            large_distance_rows.append(
                {
                    "ts_first": first_ts,
                    "ts_second": second_ts,
                    "both_ts_ge_512": first_ts >= 512,
                    "normalized_log_quantile_distance": distance,
                }
            )
            js = distribution_distance(
                histograms[first_ts], histograms[second_ts], minimum_size=2
            ).jensen_shannon
            js_matrix[first_index, second_index] = js_matrix[second_index, first_index] = js

    linkage = hierarchy.linkage(squareform(js_matrix), method="average")
    regime_rows: list[dict[str, object]] = []
    scores: dict[int, float] = {}
    labels_by_k: dict[int, np.ndarray] = {}
    for groups in range(2, 7):
        labels = hierarchy.fcluster(linkage, groups, criterion="maxclust")
        labels_by_k[groups] = labels
        scores[groups] = _silhouette(js_matrix, labels)
    selected_groups = max(scores, key=scores.get)
    for groups in range(2, 7):
        for ts, label in zip(ts_values, labels_by_k[groups], strict=True):
            regime_rows.append(
                {
                    "number_of_groups": groups,
                    "selected_by_maximum_silhouette": groups == selected_groups,
                    "mean_silhouette": scores[groups],
                    "ts": ts,
                    "cluster": int(label),
                }
            )

    _write(args.output_dir / "avalanche_behavior_summary.csv", summary_rows)
    _write(args.output_dir / "avalanche_lorenz.csv", lorenz_rows)
    _write(args.output_dir / "avalanche_ccdf_crossings.csv", crossing_rows)
    _write(args.output_dir / "avalanche_large_scale_distances.csv", large_distance_rows)
    _write(args.output_dir / "avalanche_regime_clustering.csv", regime_rows)
    np.savetxt(
        args.output_dir / "avalanche_regime_linkage.csv",
        linkage,
        delimiter=",",
        header="cluster_first,cluster_second,distance,cluster_size",
        comments="",
    )
    (args.output_dir / "avalanche_behavior_run.json").write_text(
        json.dumps(
            {
                "population": "pooled local avalanche sizes s>=2",
                "methods": [
                    "exact weighted moments and quantiles",
                    "top-event size concentration and Lorenz curves",
                    "two-means partition minimizing weighted log-size variance",
                    "adjacent empirical CCDF crossings",
                    "median-normalized log-quantile distances for upper groups",
                    "average-linkage clustering of Jensen-Shannon distances",
                ],
                "selected_regime_count": selected_groups,
                "silhouette_by_group_count": scores,
                "force_or_other_fibril_metrics": "not used",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Rupture-run data layer

`read_avalanche_runs.py` reads the simulator output in
`Data_avalanches_all_fibrils/runs` as a stream. Each source file represents
one fibril geometry and contains 1,000 rupture realizations. Realization zero
starts immediately after the CSV header; subsequent realizations start after
a numbered marker such as `----------------------------------------------1`.
The raw files remain authoritative. Parsing preserves every connected cluster,
including size-one clusters and clusters in the terminal force step;
statistical filtering is an explicit downstream choice.

## Commands

From the repository root, using the project environment:

```sh
.venv/bin/python Code/Data_analysis/read_avalanche_runs.py summary
.venv/bin/python Code/Data_analysis/read_avalanche_runs.py summary --minimum-size 2 --exclude-terminal-step
.venv/bin/python Code/Data_analysis/read_avalanche_runs.py events --output /tmp/events.csv
.venv/bin/python Code/Data_analysis/read_avalanche_runs.py build-cache \
  --output Data_avalanches_all_fibrils/derived/avalanche_runs_v1
.venv/bin/python Code/Data_analysis/read_avalanche_runs.py build-analysis-db
```

`summary` validates while counting. `events` exports a selected view to CSV;
its defaults (`s >= 2`, terminal included) do not affect raw parsing or the
cache. `build-cache` always stores all events. Its destination must be new and
outside `Data_avalanches_all_fibrils/runs`; construction happens in a sibling
temporary directory which is atomically renamed only after success.

## Parquet schema

The cache has a `dataset.json` descriptor and three logical datasets:

- `manifest`: one row per raw file, including schema version, source-relative
  path, byte size, nanosecond mtime, SHA-256, condition, fibril ID, and counts.
- `force_steps`: one row per force level, including `realization`,
  `step_index`, force, particle counts, number of deleted rods, event count,
  terminal flag, and source path/line.
- `avalanche_events`: one row per connected deletion cluster, including its
  size and index within the force step, terminal flag, and source path/line.
- `run_summary`: one row per realization, with step and event counts, terminal
  force, singleton count, terminal-event count, and maximum avalanche size.
- `run_histograms`: event counts by fibril, realization, terminal flag, and
  avalanche size. This is the compact input for nested/bootstrap analyses.

The two large datasets use only the Hive partitions `ts` and
`weibull_modulus`. `seed`/`fibril_id` and `realization` remain ordinary columns
for hierarchical analyses. Query directly with DuckDB, for example:

```sql
SELECT ts, weibull_modulus, count(*)
FROM read_parquet('Derived/rupture-v1/avalanche_events/**/*.parquet',
                  hive_partitioning = true)
WHERE avalanche_size >= 2 AND NOT is_terminal_step
GROUP BY ALL;
```

Schema version `1.1.0` describes the normalized representation. Rebuild the
cache if any manifest fingerprint differs from the raw source.

## DuckDB analysis database

`build-analysis-db` creates
`Data_avalanches_all_fibrils/derived/avalanche_analysis_v1.duckdb` atomically.
It materializes `source_manifest`, `run_summary`, `run_histograms`,
`fibril_histograms`, and `pooled_histograms`. The detailed `force_steps` and
`avalanche_events` relations are views over the canonical Parquet cache, so
the database and `avalanche_runs_v1/` directory must remain together in their
recorded locations. The original TXT files remain authoritative.

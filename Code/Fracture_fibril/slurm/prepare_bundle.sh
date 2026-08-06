#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)"
EXTENDED_DIR="$REPO_ROOT/Data_fibrils/Avalanche_force_grouped/extended"
BUNDLE_DIR="${1:-$REPO_ROOT/cluster_bundle}"
ARCHIVE_PATH="${2:-${BUNDLE_DIR}.tar.gz}"
FRACTURE_DIR="$REPO_ROOT/Code/Fracture_fibril"
if [[ -n "${TS_VALUES_CSV:-}" ]]; then
    IFS=',' read -r -a TS_VALUES <<< "$TS_VALUES_CSV"
else
    TS_VALUES=(8192 4096 1024 512 128 64)
fi

if ((${#TS_VALUES[@]} == 0)); then
    echo "Informe pelo menos um Ts em TS_VALUES_CSV." >&2
    exit 2
fi

mkdir -p "$BUNDLE_DIR/code" "$BUNDLE_DIR/inputs" "$BUNDLE_DIR/logs" \
    "$BUNDLE_DIR/results"

cp -- "$FRACTURE_DIR/stress_strain_ava.py" "$BUNDLE_DIR/code/"
cp -- "$FRACTURE_DIR/slurm/run_array.sbatch" "$BUNDLE_DIR/"
cp -- "$FRACTURE_DIR/slurm/submit.sh" "$BUNDLE_DIR/"

manifest="$BUNDLE_DIR/manifest.tsv"
manifest_tmp="$manifest.tmp"
: > "$manifest_tmp"

for ts in "${TS_VALUES[@]}"; do
    mapfile -t dat_files < <(
        find "$EXTENDED_DIR" -maxdepth 1 -type f \
            -name "ts_${ts}_seed_*.dat" -print | sort
    )

    if ((${#dat_files[@]} != 50)); then
        echo "Ts=$ts: esperadas 50 fibrilas, encontradas ${#dat_files[@]}." >&2
        exit 1
    fi

    mkdir -p "$BUNDLE_DIR/inputs/ts_${ts}" "$BUNDLE_DIR/results/ts_${ts}"

    for dat_file in "${dat_files[@]}"; do
        base_name="$(basename -- "$dat_file")"
        cp -- "$dat_file" "$BUNDLE_DIR/inputs/ts_${ts}/$base_name"
        printf '%s\t%s\n' "$ts" "inputs/ts_${ts}/$base_name" >> "$manifest_tmp"
    done
done

mv -- "$manifest_tmp" "$manifest"

task_count="$(wc -l < "$manifest")"
expected_tasks=$((${#TS_VALUES[@]} * 50))
if ((task_count != expected_tasks)); then
    echo "Manifesto inválido: esperadas $expected_tasks tarefas, encontradas $task_count." >&2
    exit 1
fi

echo "Bundle pronto em: $BUNDLE_DIR"
echo "Tarefas: $task_count (ordem: ${TS_VALUES[*]})"

archive_parent="$(cd -- "$(dirname -- "$ARCHIVE_PATH")" && pwd)"
archive_name="$(basename -- "$ARCHIVE_PATH")"
bundle_parent="$(cd -- "$(dirname -- "$BUNDLE_DIR")" && pwd)"
bundle_name="$(basename -- "$BUNDLE_DIR")"
tar -C "$bundle_parent" -czf "$archive_parent/$archive_name" "$bundle_name"

echo "Arquivo único para upload: $archive_parent/$archive_name"

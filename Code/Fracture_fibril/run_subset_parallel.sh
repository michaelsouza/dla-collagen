#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
EXTENDED_DIR="$REPO_ROOT/Data_fibrils/Avalanche_force_grouped/extended"
RUNS_DIR="$REPO_ROOT/Data_fibrils/Avalanche_force_grouped/runs"
FRACTURE_SCRIPT="$REPO_ROOT/Code/Fracture_fibril/stress_strain_ava.py"

M_VALUE="${M_VALUE:-2}"
N_REPS="${N_REPS:-1000}"
NUM_JOBS="${NUM_JOBS:-8}"
DRY_RUN="${DRY_RUN:-0}"

if (($# != 3)); then
    echo "Uso: $0 TS POSICAO_INICIAL QUANTIDADE" >&2
    echo "Exemplo: $0 16 26 25" >&2
    exit 2
fi

ts="$1"
start_position="$2"
count="$3"

for value in "$ts" "$start_position" "$count" "$M_VALUE" "$N_REPS" "$NUM_JOBS"; do
    if [[ ! "$value" =~ ^[1-9][0-9]*$ ]]; then
        echo "Todos os argumentos e parâmetros devem ser inteiros positivos." >&2
        exit 2
    fi
done
if [[ "$DRY_RUN" != 0 && "$DRY_RUN" != 1 ]]; then
    echo "DRY_RUN deve ser 0 ou 1." >&2
    exit 2
fi
if ! command -v parallel >/dev/null 2>&1; then
    echo "GNU Parallel não encontrado." >&2
    exit 1
fi

mapfile -t dat_files < <(
    find "$EXTENDED_DIR" -maxdepth 1 -type f \
        -name "ts_${ts}_seed_*.dat" -print |
        sort -V
)

if ((${#dat_files[@]} != 50)); then
    echo "Ts=$ts: esperadas 50 fibrilas, encontradas ${#dat_files[@]}." >&2
    exit 1
fi

start_index=$((start_position - 1))
end_index=$((start_index + count))
if ((end_index > ${#dat_files[@]})); then
    echo "O intervalo solicitado ultrapassa as ${#dat_files[@]} fibrilas." >&2
    exit 2
fi
selected_files=("${dat_files[@]:start_index:count}")

echo "Ts=$ts: posições $start_position a $end_index, ${#selected_files[@]} fibrilas."
printf '  %s\n' "${selected_files[@]##*/}"

if ((DRY_RUN == 1)); then
    exit 0
fi

run_dir="$RUNS_DIR/ts_${ts}"
mkdir -p "$run_dir"

run_dbs=()
for dat_file in "${selected_files[@]}"; do
    python3 -c \
        'import sys; sys.path.insert(0, sys.argv[2]); import stress_strain_ava as s; s.read_or_create_ssd(sys.argv[1])' \
        "$dat_file" "$REPO_ROOT/Code/Fracture_fibril"

    source_db="${dat_file%.dat}.db"
    if [[ ! -f "$source_db" ]]; then
        echo "Banco não foi criado: $source_db" >&2
        exit 1
    fi
    cp -- "$source_db" "$run_dir/"
    run_dbs+=("$run_dir/${source_db##*/}")
done

worklist="$(mktemp "$run_dir/subset_worklist.XXXXXX.tsv")"
trap 'rm -f -- "$worklist"' EXIT

complete=0
partial=0
not_started=0
for db_file in "${run_dbs[@]}"; do
    output_file="${db_file%.db}_m_${M_VALUE}.txt"
    log_file="${db_file%.db}.log"
    completed_runs=0

    if [[ -s "$output_file" ]]; then
        separators="$(
            grep -c '^----------------------------------------------[0-9][0-9]*$' \
                "$output_file" || true
        )"
        completed_runs=$((separators + 1))
    fi

    if ((completed_runs >= N_REPS)); then
        complete=$((complete + 1))
        continue
    fi
    if ((completed_runs > 0)); then
        partial=$((partial + 1))
    else
        not_started=$((not_started + 1))
    fi
    printf '%s\t%d\t%s\n' \
        "$db_file" "$completed_runs" "$log_file" >> "$worklist"
done

pending=$((partial + not_started))
echo "Ts=$ts: $complete concluídas, $partial parciais, $not_started não iniciadas."

if ((pending == 0)); then
    touch "$run_dir/BATCH_SUBSET_${start_position}_${end_index}_COMPLETE"
    exit 0
fi

export FRACTURE_SCRIPT M_VALUE N_REPS
joblog="$run_dir/subset_${start_position}_${end_index}_joblog_$(date +%Y%m%d_%H%M%S).tsv"
parallel -j "$NUM_JOBS" --halt soon,fail=1 --joblog "$joblog" \
    --colsep '\t' \
    'nice -n 10 python3 -u "$FRACTURE_SCRIPT" -file {1} -m "$M_VALUE" -n "$N_REPS" -start {2} >> {3} 2>&1' \
    :::: "$worklist"

incomplete=0
for db_file in "${run_dbs[@]}"; do
    output_file="${db_file%.db}_m_${M_VALUE}.txt"
    completed_runs=0
    if [[ -s "$output_file" ]]; then
        separators="$(
            grep -c '^----------------------------------------------[0-9][0-9]*$' \
                "$output_file" || true
        )"
        completed_runs=$((separators + 1))
    fi
    if ((completed_runs < N_REPS)); then
        incomplete=$((incomplete + 1))
    fi
done

if ((incomplete > 0)); then
    echo "Ts=$ts: $incomplete tarefas ainda incompletas." >&2
    exit 1
fi

touch "$run_dir/BATCH_SUBSET_${start_position}_${end_index}_COMPLETE"
echo "Ts=$ts: subconjunto concluído."

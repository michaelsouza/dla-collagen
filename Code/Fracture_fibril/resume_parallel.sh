#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
RUNS_DIR="$REPO_ROOT/Data_fibrils/Avalanche_force_grouped/runs"
FRACTURE_SCRIPT="$REPO_ROOT/Code/Fracture_fibril/stress_strain_ava.py"

M_VALUE="${M_VALUE:-2}"
N_REPS="${N_REPS:-1000}"
NUM_JOBS="${NUM_JOBS:-8}"
DRY_RUN="${DRY_RUN:-0}"

if (($# == 0)); then
    echo "Uso: $0 TS [TS ...]" >&2
    echo "Exemplo: N_REPS=1000 NUM_JOBS=8 $0 32" >&2
    exit 2
fi

if ! command -v parallel >/dev/null 2>&1; then
    echo "GNU Parallel não encontrado." >&2
    exit 1
fi

for value in "$M_VALUE" "$N_REPS" "$NUM_JOBS"; do
    if [[ ! "$value" =~ ^[1-9][0-9]*$ ]]; then
        echo "M_VALUE, N_REPS e NUM_JOBS devem ser inteiros positivos." >&2
        exit 2
    fi
done
if [[ "$DRY_RUN" != 0 && "$DRY_RUN" != 1 ]]; then
    echo "DRY_RUN deve ser 0 ou 1." >&2
    exit 2
fi

export FRACTURE_SCRIPT M_VALUE N_REPS

for ts in "$@"; do
    if [[ ! "$ts" =~ ^[0-9]+$ ]]; then
        echo "Valor inválido de Ts: $ts" >&2
        exit 2
    fi

    run_dir="$RUNS_DIR/ts_${ts}"
    if [[ ! -d "$run_dir" ]]; then
        echo "Diretório de execução não encontrado: $run_dir" >&2
        exit 1
    fi

    mapfile -t db_files < <(
        find "$run_dir" -maxdepth 1 -type f \
            -name "ts_${ts}_seed_*.db" -print |
            sort
    )
    if ((${#db_files[@]} != 50)); then
        echo "Ts=$ts: esperados 50 bancos, encontrados ${#db_files[@]}." >&2
        exit 1
    fi

    worklist="$(mktemp "$run_dir/resume_worklist.XXXXXX.tsv")"
    trap 'rm -f -- "$worklist"' EXIT

    complete=0
    partial=0
    not_started=0
    for db_file in "${db_files[@]}"; do
        output_file="${db_file%.db}_m_${M_VALUE}.txt"
        log_file="${db_file%.db}.log"
        completed_runs=0

        if [[ -f "$output_file" ]]; then
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
    echo "Ts=$ts: $complete concluídas, $partial parciais, " \
        "$not_started não iniciadas."

    if ((pending == 0)); then
        touch "$run_dir/BATCH_COMPLETE"
        rm -f -- "$worklist"
        trap - EXIT
        echo "Ts=$ts: nenhuma tarefa pendente."
        continue
    fi

    if ((DRY_RUN == 1)); then
        column -t -s $'\t' "$worklist"
        rm -f -- "$worklist"
        trap - EXIT
        continue
    fi

    joblog="$run_dir/resume_joblog_$(date +%Y%m%d_%H%M%S).tsv"
    parallel -j "$NUM_JOBS" --halt soon,fail=1 --joblog "$joblog" \
        --colsep '\t' \
        'nice -n 10 python3 -u "$FRACTURE_SCRIPT" -file {1} -m "$M_VALUE" -n "$N_REPS" -start {2} >> {3} 2>&1' \
        :::: "$worklist"

    incomplete=0
    for db_file in "${db_files[@]}"; do
        output_file="${db_file%.db}_m_${M_VALUE}.txt"
        if [[ ! -f "$output_file" ]]; then
            incomplete=$((incomplete + 1))
            continue
        fi
        separators="$(
            grep -c '^----------------------------------------------[0-9][0-9]*$' \
                "$output_file" || true
        )"
        completed_runs=$((separators + 1))
        if ((completed_runs < N_REPS)); then
            incomplete=$((incomplete + 1))
        fi
    done

    if ((incomplete > 0)); then
        echo "Ts=$ts: $incomplete tarefas ainda incompletas." >&2
        exit 1
    fi

    touch "$run_dir/BATCH_COMPLETE"
    rm -f -- "$worklist"
    trap - EXIT
    echo "Ts=$ts: lote retomado e concluído."
done

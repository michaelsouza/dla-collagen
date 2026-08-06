#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
EXTENDED_DIR="$REPO_ROOT/Data_fibrils/Avalanche_force_grouped/extended"
RUNS_DIR="$REPO_ROOT/Data_fibrils/Avalanche_force_grouped/runs"
FRACTURE_SCRIPT="$REPO_ROOT/Code/Fracture_fibril/stress_strain_ava.py"

M_VALUE="${M_VALUE:-2}"
N_REPS="${N_REPS:-1000}"
NUM_JOBS="${NUM_JOBS:-8}"

if (($# == 0)); then
    echo "Uso: $0 TS [TS ...]" >&2
    echo "Exemplo: N_REPS=1000 NUM_JOBS=8 $0 2 8 32" >&2
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

export FRACTURE_SCRIPT M_VALUE N_REPS

for ts in "$@"; do
    if [[ ! "$ts" =~ ^[0-9]+$ ]]; then
        echo "Valor inválido de Ts: $ts" >&2
        exit 2
    fi

    mapfile -t dat_files < <(
        find "$EXTENDED_DIR" -maxdepth 1 -type f \
            -name "ts_${ts}_seed_*.dat" -print |
            sort
    )

    if ((${#dat_files[@]} != 50)); then
        echo "Ts=$ts: esperadas 50 fibrilas, encontradas ${#dat_files[@]}." >&2
        exit 1
    fi

    run_dir="$RUNS_DIR/ts_${ts}"
    joblog="$run_dir/parallel_joblog.tsv"
    mkdir -p "$run_dir"

    if [[ -e "$joblog" ]] ||
        compgen -G "$run_dir/ts_${ts}_seed_*_m_${M_VALUE}.txt" >/dev/null; then
        echo "Ts=$ts: o diretório de execução já contém resultados." >&2
        exit 1
    fi

    echo "Ts=$ts: preparando os 50 bancos."
    db_files=()
    for dat_file in "${dat_files[@]}"; do
        python3 -c \
            'import sys; sys.path.insert(0, sys.argv[2]); import stress_strain_ava as s; s.read_or_create_ssd(sys.argv[1])' \
            "$dat_file" "$REPO_ROOT/Code/Fracture_fibril"

        db_file="${dat_file%.dat}.db"
        if [[ ! -f "$db_file" ]]; then
            echo "Banco não foi criado: $db_file" >&2
            exit 1
        fi
        db_files+=("$db_file")
    done

    cp -- "${db_files[@]}" "$run_dir/"

    mapfile -t run_dbs < <(
        find "$run_dir" -maxdepth 1 -type f \
            -name "ts_${ts}_seed_*.db" -print |
            sort
    )

    if ((${#run_dbs[@]} != 50)); then
        echo "Ts=$ts: esperados 50 bancos no diretório de execução." >&2
        exit 1
    fi

    echo "Ts=$ts: iniciando $N_REPS realizações por fibrila em $NUM_JOBS processos."
    parallel -j "$NUM_JOBS" --halt soon,fail=1 --joblog "$joblog" \
        'nice -n 10 python3 -u "$FRACTURE_SCRIPT" -file {} -m "$M_VALUE" -n "$N_REPS" > {.}.log 2>&1' \
        ::: "${run_dbs[@]}"

    touch "$run_dir/BATCH_COMPLETE"
    echo "Ts=$ts: lote concluído."
done

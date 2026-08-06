#!/usr/bin/env bash

#SBATCH --job-name=collagen
#SBATCH --array=0-299%150
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=4-00:00:00
#SBATCH --output=logs/slurm-%A_%a.out
#SBATCH --error=logs/slurm-%A_%a.err

set -euo pipefail

BUNDLE_DIR="${SLURM_SUBMIT_DIR:?Submeta o job a partir do diretório do bundle}"
MANIFEST="$BUNDLE_DIR/manifest.tsv"
M_VALUE="${M_VALUE:-2}"
N_REPS="${N_REPS:-1000}"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export OPENBLAS_CORETYPE=generic
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

if [[ ! -s "$MANIFEST" ]]; then
    echo "Manifesto não encontrado ou vazio: $MANIFEST" >&2
    exit 1
fi

line_number=$((SLURM_ARRAY_TASK_ID + 1))
line="$(sed -n "${line_number}p" "$MANIFEST")"
if [[ -z "$line" ]]; then
    echo "Não existe a linha $line_number no manifesto." >&2
    exit 1
fi

IFS=$'\t' read -r ts relative_dat <<< "$line"
input_dat="$BUNDLE_DIR/$relative_dat"
base_name="$(basename -- "$input_dat" .dat)"
result_dir="$BUNDLE_DIR/results/ts_${ts}"
final_result="$result_dir/${base_name}_m_${M_VALUE}.txt"

if [[ ! -s "$input_dat" ]]; then
    echo "Entrada não encontrada ou vazia: $input_dat" >&2
    exit 1
fi

mkdir -p "$result_dir"
if [[ -s "$final_result" ]]; then
    echo "Resultado já concluído; tarefa ignorada: $final_result"
    exit 0
fi

task_tmp="${SLURM_TMPDIR:-/tmp}/collagen-${SLURM_JOB_ID}-${SLURM_ARRAY_TASK_ID}"
mkdir -p "$task_tmp"
cleanup() {
    rm -rf -- "$task_tmp"
}
trap cleanup EXIT

cp -- "$input_dat" "$task_tmp/"
local_dat="$task_tmp/$(basename -- "$input_dat")"

echo "Início: $(date --iso-8601=seconds)"
echo "Ts=$ts entrada=$relative_dat repetições=$N_REPS m=$M_VALUE"

python3 -u "$BUNDLE_DIR/code/stress_strain_ava.py" \
    -file "$local_dat" -m "$M_VALUE" -n "$N_REPS"

local_result="${local_dat%.dat}_m_${M_VALUE}.txt"
if [[ ! -s "$local_result" ]]; then
    echo "A simulação terminou sem produzir resultado." >&2
    exit 1
fi

result_tmp="$result_dir/.${base_name}_m_${M_VALUE}.${SLURM_JOB_ID}.tmp"
cp -- "$local_result" "$result_tmp"
mv -- "$result_tmp" "$final_result"

echo "Fim: $(date --iso-8601=seconds)"
echo "Resultado: $final_result"

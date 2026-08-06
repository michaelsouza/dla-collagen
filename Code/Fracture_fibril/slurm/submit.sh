#!/usr/bin/env bash

set -euo pipefail

BUNDLE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$BUNDLE_DIR"

mkdir -p logs results

if [[ ! -s manifest.tsv ]]; then
    echo "manifest.tsv não encontrado. Prepare e transfira o bundle primeiro." >&2
    exit 1
fi

task_count="$(wc -l < manifest.tsv)"
if ((task_count <= 0)); then
    echo "O manifesto não contém tarefas." >&2
    exit 1
fi

max_concurrent="${MAX_CONCURRENT:-50}"
if [[ ! "$max_concurrent" =~ ^[1-9][0-9]*$ ]]; then
    echo "MAX_CONCURRENT deve ser um inteiro positivo." >&2
    exit 2
fi

array_end=$((task_count - 1))
array_spec="0-${array_end}%${max_concurrent}"

# Opções específicas do cluster podem ser passadas normalmente, por exemplo:
# ./submit.sh --account=meu_projeto --partition=cpu
echo "Submetendo $task_count tarefas; máximo simultâneo: $max_concurrent."
sbatch "$@" --array="$array_spec" run_array.sbatch

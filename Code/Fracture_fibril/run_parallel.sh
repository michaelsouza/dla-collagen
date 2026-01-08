#!/bin/bash

# --- Configuração Geral ---
# Diretório onde seus arquivos .db estão.
FILES_DIR="." 
# Valor de 'm' para usar.
M_VALUE=2
# Número de repetições DENTRO de cada script Python.
N_REPS=1000

# --- CONFIGURAÇÃO DE NÚCLEOS ---
# Escolha UMA das opções abaixo e comente as outras.
#
# Opção 1: Usar um número FIXO de núcleos. (Ex: 8)
NUM_CORES_TO_USE=8

# Opção 2: Usar uma PORCENTAGEM dos núcleos. (Ex: "75%")
# NUM_CORES_TO_USE="75%"

# Opção 3: Usar TODOS os núcleos MENOS 2 (recomendado para manter o PC usável).
# NUM_CORES_TO_USE="-2"

# Opção 4: Usar TODOS os núcleos disponíveis (pode deixar o PC lento para outras tarefas).
# NUM_CORES_TO_USE=0
# ---------------------------------

# Encontra todos os arquivos .db no diretório atual, sem descer para subdiretórios.
INPUT_FILES=$(find "$FILES_DIR" -maxdepth 1 -name "*.db")

if [ -z "$INPUT_FILES" ]; then
    echo "AVISO: Nenhum arquivo .db encontrado no diretório local. Saindo."
    exit 1
fi

echo "Iniciando a paralelização..."
echo "Usando a configuração de núcleos: $NUM_CORES_TO_USE"
echo "--------------------------------------------------"

# O comando GNU Parallel agora usa a variável $NUM_CORES_TO_USE na flag -j.
parallel -j"$NUM_CORES_TO_USE" --bar \
    'python stress_strain_ava.py -file {} -m '"$M_VALUE"' -n '"$N_REPS" \
    ::: $INPUT_FILES

echo "--------------------------------------------------"
echo "Paralelização concluída."
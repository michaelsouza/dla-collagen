#!/bin/bash

# Define nome do ambiente virtual
VENV_NAME="venv_dla"

echo "=== Iniciando configuração do ambiente ==="

# Verifica se python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: python3 não encontrado."
    exit 1
fi

# Cria o ambiente virtual se não existir
if [ ! -d "$VENV_NAME" ]; then
    echo "Criando ambiente virtual '$VENV_NAME'..."
    python3 -m venv $VENV_NAME
else
    echo "Ambiente virtual '$VENV_NAME' já existe."
fi

# Ativa o ambiente
source $VENV_NAME/bin/activate

# Atualiza pip
echo "Atualizando pip..."
pip install --upgrade pip

# Instala dependências
if [ -f "requirements.txt" ]; then
    echo "Instalando dependências do requirements.txt..."
    pip install -r requirements.txt
else
    echo "Aviso: requirements.txt não encontrado."
fi

echo "=== Configuração concluída! ==="
echo "Para ativar o ambiente manualmente, use: source $VENV_NAME/bin/activate"

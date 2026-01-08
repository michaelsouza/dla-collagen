# DLA Collagen

Este repositório contém códigos para simulação de DLA (Diffusion Limited Aggregation) focada na gênese de colágeno, incluindo simulações em C++ e análises de dados em Python.

## Estrutura do Projeto

- **Code/**: Contém o código fonte principal.
  - `Dla/`: Implementações da simulação DLA em C++ e scripts relacionados.
  - `Data_analysis/`: Scripts Python e Notebooks Jupyter para análise das propriedades mecânicas e estruturais.
- **Data_fibrils/**: Diretório destinado ao armazenamento dos dados gerados.
- **makefile**: Arquivo para compilar o código C++.
- **requirements.txt**: Lista de dependências Python.
- **setup.sh**: Script para configuração automática do ambiente.

## Pré-requisitos

- Python 3.8 ou superior
- Compilador C++ (g++)
- Make (opcional)

## Instalação e Configuração

Para preparar o ambiente de desenvolvimento em uma nova máquina:

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd dla-collagen
    ```

2.  **Execute o script de configuração:**
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

    Isso criará um ambiente virtual (`venv_dla`) e instalará as dependências.

3.  **Ative o ambiente manualmente (sempre que for trabalhar):**
    ```bash
    source venv_dla/bin/activate
    ```

## Compilação (C++)

Para compilar o código C++ principal:

```bash
make
```

Isso gerará o executável `fast_dla`.

## Análise de Dados

Com o ambiente ativo, execute o Jupyter Notebook:

```bash
jupyter notebook
```

Navegue até a pasta `Code/Data_analysis/` para acessar os notebooks.

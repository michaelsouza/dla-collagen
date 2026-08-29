# Simulações de fratura e avalanches

Este diretório contém a versão canônica do programa de fratura:

```text
Code/Fracture_fibril/stress_strain_ava.py
```

Não use as cópias antigas em `/home/robert/Robert_ava/` ou em
`Data_fibrils/Data/`. Elas não contêm a correção que agrupa, em uma única
etapa de força, todas as moléculas removidas antes de identificar as
avalanches espaciais.

## Localização das fibrilas

O arquivo compactado que será versionado junto ao código está em:

```text
Data_fibrils/fibrilas_publicadas_artigo_10Ts_nb30000.zip
```

Partindo da raiz do repositório, extraia-o com:

```bash
mkdir -p Data_fibrils/Avalanche_force_grouped
unzip Data_fibrils/fibrilas_publicadas_artigo_10Ts_nb30000.zip \
  -d Data_fibrils/Avalanche_force_grouped
```

Os dados de trabalho ficam em:

```text
Data_fibrils/Avalanche_force_grouped/compact/   # dados extraídos do ZIP
Data_fibrils/Avalanche_force_grouped/extended/  # dados estendidos usados na fratura
```

Para gerar os arquivos estendidos, execute:

```bash
python3 Code/Data_analysis/extend_fibrils_batch.py \
  Data_fibrils/Avalanche_force_grouped/compact \
  Data_fibrils/Avalanche_force_grouped/extended
```

Os arquivos produzidos seguem o padrão:

```text
ts_<TS>_seed_<SEED>.dat
```

## Preparação

O programa é escrito em Python e não precisa ser compilado. Execute os
comandos a partir da raiz do repositório:

```bash
cd /home/robert/Documentos/GitHub/dla-collagen
python3 -m pip install -r requirements.txt
```

Para executar várias fibrilas simultaneamente, também é necessário ter o GNU
Parallel instalado.

## Executar todas as fibrilas de um único \(T_s\)

Use `run_parallel.sh`, informando o \(T_s\). `N_REPS` é o número de
realizações por fibrila e `NUM_JOBS` é o número de fibrilas executadas em
paralelo:

```bash
N_REPS=1000 NUM_JOBS=8 \
  bash Code/Fracture_fibril/run_parallel.sh 8192
```

Mais de um \(T_s\) pode ser informado. Nesse caso, os lotes são executados
sequencialmente:

```bash
N_REPS=1000 NUM_JOBS=8 \
  bash Code/Fracture_fibril/run_parallel.sh 8 32 64
```

O script exige exatamente 50 fibrilas para cada \(T_s\), cria os bancos
necessários e deixa os resultados isolados em:

```text
Data_fibrils/Avalanche_force_grouped/runs/ts_<TS>/
```

Cada fibrila produz um arquivo:

```text
ts_<TS>_seed_<SEED>_m_2.txt
```

Para evitar perda acidental, `run_parallel.sh` recusa executar quando o
diretório já contém resultados.

## Retomar um lote interrompido

Depois de uma interrupção, use `resume_parallel.sh` com os mesmos valores de
`N_REPS`, `M_VALUE` e `NUM_JOBS` do lote original:

```bash
N_REPS=1000 M_VALUE=2 NUM_JOBS=8 \
  bash Code/Fracture_fibril/resume_parallel.sh 32
```

O script conta as realizações já gravadas em cada arquivo, preserva fibrilas
concluídas, continua arquivos parciais a partir da próxima realização e inicia
as fibrilas restantes. Para inspecionar a lista sem executar:

```bash
DRY_RUN=1 N_REPS=1000 M_VALUE=2 NUM_JOBS=8 \
  bash Code/Fracture_fibril/resume_parallel.sh 32
```

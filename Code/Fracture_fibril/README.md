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
Code/Fracture_fibril/compact.zip
```

Partindo da raiz do repositório, extraia-o com:

```bash
mkdir -p Data_fibrils/Avalanche_force_grouped
unzip Code/Fracture_fibril/compact.zip \
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

No exemplo abaixo, altere apenas `TS`, `N` e `JOBS`. `N` é o número de
realizações por fibrila e `JOBS` é o número de fibrilas executadas em
paralelo.

```bash
TS=8192
N=1000
JOBS=8
EXTENDED=Data_fibrils/Avalanche_force_grouped/extended
RUN_DIR=Data_fibrils/Avalanche_force_grouped/runs/ts_${TS}

mkdir -p "$RUN_DIR"

for fibril in "$EXTENDED"/ts_${TS}_seed_*.dat; do
  python3 -c 'import sys; sys.path.insert(0, "Code/Fracture_fibril"); import stress_strain_ava as s; s.read_or_create_ssd(sys.argv[1])' "$fibril"
done

cp "$EXTENDED"/ts_${TS}_seed_*.db "$RUN_DIR"/

parallel -j "$JOBS" --bar \
  "python3 Code/Fracture_fibril/stress_strain_ava.py -file {} -m 2 -n $N" \
  ::: "$RUN_DIR"/ts_${TS}_seed_*.db
```

O primeiro laço converte cada fibrila estendida em um arquivo `.db`. As
cópias dos bancos e os resultados ficam isolados em:

```text
Data_fibrils/Avalanche_force_grouped/runs/ts_<TS>/
```

Cada fibrila produz um arquivo:

```text
ts_<TS>_seed_<SEED>_m_2.txt
```

Repetir o comando no mesmo diretório substitui os resultados anteriores.

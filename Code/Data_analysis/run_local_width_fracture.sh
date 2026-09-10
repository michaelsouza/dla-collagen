#!/usr/bin/env bash
# Fratura local dos cilindros periodicos em dois recortes, para F_rup contra a largura.
#
# Le:      $CYL/dla_per216_mode_s_ts_<TS>_nb_60000_seed_<SEED>_.dat (T_s em $TS, 5 sementes)
#          Reviews/PhaseC_periodic_cylinder/open_periodic_cylinder.py, Code/Data_analysis/extend_fibrils_batch.py,
#          Code/Fracture_fibril/fiber_bundle_ava.py
# Escreve: $WORK/opened/, $WORK/extended/ (com os .db), $WORK/w17/ts_<TS>/..., $WORK/w41/ts_<TS>/...,
#          $WORK/json/, $WORK/logs/, $WORK/check/ (determinismo); depois copia w17/ e w41/ para
#          Reviews/N18_df_ten_ts/width_fracture_raw/ e chama summarize_width_fracture.py
# Chamado: à mão, para N18 (Estado_revisao_ER12738.md), depois de run_periodic_cylinder_grid.sh:
#          CYL=<cilindros> WORK=<scratch>/fracture Code/Data_analysis/run_local_width_fracture.sh
#
# Estagios: A abre (y -= 108), renomeia para o padrao dla_mode_s_ts_..., que o
# extend exige, e estende; B fratura 17x17 (-half-width 8); C fratura 41x41
# (-half-width 20), menos processos por causa da RAM (1-2 GB cada); D resume.
# Um -legacy-dir por janela, porque o nome do arquivo legado nao carrega a
# janela. Semente de fratura 101, para nao repetir as realizacoes da escada de
# 2026-09-02 (que usou 1). Idempotente: pula (cilindro, janela) cujo legado ja
# tem $NREAL realizacoes; se tem menos, retoma com -start.
set -euo pipefail
CYL="${CYL:?CYL=<diretorio dos cilindros>}"
WORK="${WORK:?WORK=<diretorio de trabalho>}"
TS="${TS:-2 32 128 8192}"
SEEDS="${SEEDS:-900001 900002 900003 900004 900005}"
NREAL="${NREAL:-10}"
M="${M:-2}"
FSEED="${FSEED:-101}"
JOBS17="${JOBS17:-20}"
JOBS41="${JOBS41:-12}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PY="$ROOT/.venv/bin/python"
mkdir -p "$WORK/opened" "$WORK/extended" "$WORK/w17" "$WORK/w41" "$WORK/json" "$WORK/logs" "$WORK/check"
export CYL WORK NREAL M FSEED ROOT PY

pares() { for ts in $TS; do for s in $SEEDS; do printf '%s %s\n' "$ts" "$s"; done; done; }

# --- A: abrir, renomear, estender
prepara() {
    local ts="$1" seed="$2"
    local src="$CYL/dla_per216_mode_s_ts_${ts}_nb_60000_seed_${seed}_.dat"
    local aberto="$WORK/opened/dla_mode_s_ts_${ts}_nb_60000_seed_${seed}__open.dat"
    local ext="$WORK/extended/ts_${ts}_seed_${seed}.dat"
    [ -s "$ext" ] && { echo "pula prep ts=$ts seed=$seed"; return 0; }
    "$PY" "$ROOT/Reviews/PhaseC_periodic_cylinder/open_periodic_cylinder.py" 216 "$src" > /dev/null
    mv "${src%.dat}_open.dat" "$aberto"
    "$PY" "$ROOT/Code/Data_analysis/extend_fibrils_batch.py" "$WORK/opened" "$WORK/extended" \
        --pattern "$(basename "$aberto")" > /dev/null
    [ -s "$ext" ] || { echo "extend falhou para ts=$ts seed=$seed"; return 1; }
    echo "prep ts=$ts seed=$seed ok"
}
export -f prepara
pares | xargs -P "$JOBS17" -L1 bash -c 'prepara "$0" "$1"'

# --- B e C: fratura
fratura() {
    local ts="$1" seed="$2" hw="$3" tag="$4"
    local ext="$WORK/extended/ts_${ts}_seed_${seed}.dat"
    local leg="$WORK/$tag/ts_${ts}/ts_${ts}_seed_${seed}_m_${M}.txt"
    local feitas=0
    [ -f "$leg" ] && feitas=$(grep -c '^0,' "$leg" || true)
    if [ "$feitas" -ge "$NREAL" ]; then echo "pula $tag ts=$ts seed=$seed"; return 0; fi
    nice -n 10 "$PY" -u "$ROOT/Code/Fracture_fibril/fiber_bundle_ava.py" -file "$ext" -n "$NREAL" -m "$M" \
        -seed "$FSEED" -half-width "$hw" -half-length 100 -legacy-dir "$WORK/$tag" \
        -out "$WORK/json/ts_${ts}_seed_${seed}_${tag}.json" -start "$feitas" \
        > "$WORK/logs/ts_${ts}_seed_${seed}_${tag}.log" 2>&1
    echo "$tag ts=$ts seed=$seed: $(grep -c 'run ' "$WORK/logs/ts_${ts}_seed_${seed}_${tag}.log") realizacoes"
}
export -f fratura
pares | xargs -P "$JOBS17" -L1 bash -c 'fratura "$0" "$1" 8 w17'
pares | xargs -P "$JOBS41" -L1 bash -c 'fratura "$0" "$1" 20 w41'

# --- determinismo: 128/900001, 17x17, semente 1, uma realizacao, contra a escada de 2026-09-02
if [ -s "$WORK/extended/ts_128_seed_900001.dat" ] && [ ! -s "$WORK/check/ts_128/ts_128_seed_900001_m_2.txt" ]; then
    "$PY" "$ROOT/Code/Fracture_fibril/fiber_bundle_ava.py" -file "$WORK/extended/ts_128_seed_900001.dat" \
        -n 1 -m 2 -seed 1 -half-width 8 -half-length 100 -legacy-dir "$WORK/check" > "$WORK/logs/check.log" 2>&1
fi
if [ -s "$WORK/check/ts_128/ts_128_seed_900001_m_2.txt" ]; then
    ref="$ROOT/Reviews/PhaseC_periodic_cylinder/avalanche_ladder_raw/ts128_w17.txt"
    n=$(grep -n -m1 '^-' "$ref" | cut -d: -f1); n=$((n - 1))
    if diff -q <(head -n "$n" "$ref") "$WORK/check/ts_128/ts_128_seed_900001_m_2.txt" > /dev/null; then
        echo "determinismo: primeira realizacao identica a escada de 2026-09-02 ($n linhas)"
    else
        echo "determinismo: DIFERE da escada de 2026-09-02"
    fi
fi

# --- D: copiar o bruto e resumir
DEST="$ROOT/Reviews/N18_df_ten_ts/width_fracture_raw"
mkdir -p "$DEST"
cp -r "$WORK/w17" "$WORK/w41" "$DEST/"
"$PY" "$ROOT/Code/Data_analysis/summarize_width_fracture.py" \
    --dirs "w17=$DEST/w17" "w41=$DEST/w41" "ladder=$ROOT/Reviews/PhaseC_periodic_cylinder/avalanche_ladder_raw"

#!/usr/bin/env bash
# Gera cilindros periodicos (grade T_s x sementes) nesta maquina, em paralelo.
#
# Le:      Code/Dla/fast_dla2.cpp (compila em $BIN se faltar)
# Escreve: $OUT/dla_per216_mode_s_ts_<TS>_nb_60000_seed_<SEED>_.dat (um por par),
#          $OUT/logs/ts_<TS>_seed_<SEED>.log, $OUT/gen_timing.csv,
#          $OUT/checksums.sha256, $OUT/provenance.txt
# Chamado: à mão, para N18 (Estado_revisao_ER12738.md):
#          JOBS=25 Code/Data_analysis/run_periodic_cylinder_grid.sh <OUT>
#          Grade por ambiente: TS_LIST (padrao: os dez T_s) e SEED_LIST (padrao:
#          900001-900005). Ex.: as 10 sementes extras de 2026-09-10 em cinco T_s:
#          TS_LIST="8192 4096 16 8 2" SEED_LIST="900006 ... 900015" JOBS=25 ... <OUT>
#
# Receita: a do cabecalho de Reviews/PhaseC_periodic_cylinder/df_wide_cylinders.csv
# (fast_dla2 do commit 17cfc1f, -mode s -rng fast -period 216, nb = 60000, sem
# -jumps nem -coverstop). Sementes 900001-900005, as mesmas de 2026-09-01, para
# que os 15 cilindros ja medidos sirvam de conferencia. Idempotente: pula o par
# cujo .dat ja tem 60000 moleculas. gen_timing.csv e checksums.sha256 sao
# reconstruidos por glob no fim, sobre TODOS os .dat/logs de $OUT (os de rodadas
# anteriores continuam la). Os .dat nao sao versionados; a receita e o sha256
# gravados aqui os reproduzem bit a bit.
set -euo pipefail
OUT="${1:?uso: run_periodic_cylinder_grid.sh <diretorio de saida>}"
JOBS="${JOBS:-25}"
# T_s alto primeiro: se for mais lento, comeca cedo
TS_LIST="${TS_LIST:-8192 4096 1024 512 128 64 32 16 8 2}"
SEED_LIST="${SEED_LIST:-900001 900002 900003 900004 900005}"
NB=60000
PERIOD=216
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BIN="${BIN:-$OUT/../bin/fast_dla2}"
mkdir -p "$OUT/logs" "$(dirname "$BIN")"

if [ ! -x "$BIN" ]; then
    g++ -std=c++17 -O2 "$ROOT/Code/Dla/fast_dla2.cpp" -o "$BIN"
fi
{
    echo "data: $(date -Is)"
    echo "commit: $(git -C "$ROOT" rev-parse HEAD)"
    echo "fast_dla2.cpp ultimo commit: $(git -C "$ROOT" log -1 --format=%h -- Code/Dla/fast_dla2.cpp)"
    echo "diff local em fast_dla2.cpp: $(git -C "$ROOT" diff --stat Code/Dla/fast_dla2.cpp | wc -l) linhas"
    echo "compilador: $(g++ --version | head -1)"
    echo "receita: fast_dla2 -ts T -mode s -num_bind $NB -seed S -rng fast -period $PERIOD"
} > "$OUT/provenance.txt"

completo() {  # 1 se o arquivo existe com NB moleculas
    [ -f "$1" ] && [ "$(grep -c '^uid' "$1")" -ge "$NB" ]
}
export BIN OUT NB PERIOD
export -f completo
gera() {
    local ts="$1" seed="$2"
    local f="$OUT/dla_per${PERIOD}_mode_s_ts_${ts}_nb_${NB}_seed_${seed}_.dat"
    if completo "$f"; then echo "pula  ts=$ts seed=$seed"; return 0; fi
    rm -f "$f"
    nice -n 10 "$BIN" -ts "$ts" -mode s -num_bind "$NB" -seed "$seed" -rng fast \
        -period "$PERIOD" -output_dir "$OUT" > "$OUT/logs/ts_${ts}_seed_${seed}.log" 2>&1
    echo "feito ts=$ts seed=$seed $(grep elapsed "$OUT/logs/ts_${ts}_seed_${seed}.log")"
}
export -f gera

for ts in $TS_LIST; do
    for seed in $SEED_LIST; do
        printf '%s %s\n' "$ts" "$seed"
    done
done | xargs -P "$JOBS" -L1 bash -c 'gera "$0" "$1"'

# tempos, checksums e conferencia (reconstruidos por glob sobre tudo em $OUT)
n_grade=$(( $(echo $TS_LIST | wc -w) * $(echo $SEED_LIST | wc -w) ))
{
    echo "ts,seed,seconds"
    for l in "$OUT"/logs/ts_*_seed_*.log; do
        b=$(basename "$l" .log); ts=${b#ts_}; ts=${ts%%_*}; seed=${b##*seed_}
        s=$(sed -n 's/^elapsed \.* \([0-9.]*\) s$/\1/p' "$l")
        echo "$ts,$seed,$s"
    done | sort -t, -k1,1n -k2,2n
} > "$OUT/gen_timing.csv"
( cd "$OUT" && sha256sum dla_per*_.dat > checksums.sha256 )

n=0; ruim=0
for f in "$OUT"/dla_per*_.dat; do
    n=$((n + 1))
    if ! completo "$f"; then echo "INCOMPLETO: $f"; ruim=$((ruim + 1)); fi
    if awk -v P="$PERIOD" '$1 ~ /^uid/ && ($4 < 0 || $4 >= P) {bad=1} END {exit bad}' "$f"; then :; else
        echo "y fora de [0,$PERIOD): $f"; ruim=$((ruim + 1)); fi
done
echo "arquivos: $n (grade desta rodada: $n_grade)  problemas: $ruim"
[ "$n" -ge "$n_grade" ] && [ "$ruim" -eq 0 ]

#!/usr/bin/env bash
# Serie de tamanhos: fibrilas livres com nb de 3.750 a 120.000 em T_s = 2 e 8192.
#
# Le:      $DLA_PROJECT/campaign/bin/fast_dla2 (binario da campanha)
# Escreve: $DLA_PROJECT/campaign/analysis/scaling/dla_mode_s_ts_<TS>_nb_<NB>_seed_777_.dat
#          e uma linha "TIME <ts> <nb> <segundos>" por fibrila no .out do SLURM
# Chamado: sbatch --account=solverbrict --partition=cpu_amd Code/cluster/sdumont2nd/run_nb_scaling_series.sbatch
#
# Foi o job 580370 (2026-08-27, 1h08), fonte de R ~ nb^0,29 e t ~ nb^1,49 na §4
# do relatorio da campanha e do custo de "1,6 milhao de moleculas, 43 h" citado
# nas respostas. Submetido na epoca a partir de uma copia em
# $DLA_PROJECT/campaign/scaling.sbatch; esta e a versao limpa que ficou na raiz
# do clone, fora do git, ate 2026-09-10. Semente unica (777): nao ha barra de erro.
#SBATCH --job-name=dla-scaling
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=04:00:00
set -euo pipefail
cd "$HOME/gitrepos/dla-collagen"
source Code/cluster/sdumont2nd/env.sh
W="$DLA_PROJECT/campaign/analysis/scaling"
BIN="$DLA_PROJECT/campaign/bin/fast_dla2"
mkdir -p "$W"
run() {
    local ts="$1" nb="$2" start finish
    start=$(date +%s.%N)
    "$BIN" -mode s -ts "$ts" -num_bind "$nb" -seed 777 \
           -jumps 1 -coverstop 1 -rng fast -output_dir "$W" >/dev/null 2>&1
    finish=$(date +%s.%N)
    printf 'TIME %s %s %.1f\n' "$ts" "$nb" "$(echo "$finish - $start" | bc)"
}
export -f run
export BIN W
for ts in 2 8192; do
    for nb in 3750 7500 15000 30000 60000 120000; do
        printf '%s %s\n' "$ts" "$nb"
    done
done | xargs -n2 -P 12 bash -c 'run "$0" "$1"'

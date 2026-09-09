#!/bin/bash
# Teste de 2026-08-30: a fibrila ENGORDA ou so ESTICA ao receber 4x mais moleculas?
#
# Le:      $DLA_PROJECT/campaign/bin/fast_dla2
# Escreve: $DLA_PROJECT/nb_scaling_test/ts<TS>_nb<NB>.dat (3 T_s x 2 nb, semente 900001)
#          e a tabela de R_max, particulas por camada e comprimento no .out do SLURM
# Chamado: sbatch Code/cluster/sdumont2nd/run_nb_scaling_test.sbatch
#
# Foi o job 584509 (1h09). Resultado em Reviews/PhaseC_periodic_cylinder/nb_scaling_test.md
# e na decisao 2026-08-30_diametro_e_dimensao_fractal.md: com 4x mais moleculas o
# raio sobe 1,2-1,4x e o comprimento dobra. Ficou so em $DLA_PROJECT ate 2026-09-10.
#SBATCH --job-name=nb_scaling
#SBATCH --partition=cpu_amd
#SBATCH --account=solverbrict
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --time=06:00:00
#SBATCH --output=%x_%j.out
# Testa se a fibrila ENGORDA ou so ESTICA ao receber mais moleculas.
# Roda 3 Ts x 2 valores de nb; mede R_max na regiao central |y|<=90.
set -u
P="$HOME/scratch/dla-collagen"
BIN="$P/campaign/bin/fast_dla2"
OUT="$P/nb_scaling_test"
TMP="${SLURM_TMPDIR:-${TMPDIR:-/tmp}}/nbscal.$$"
mkdir -p "$TMP" "$OUT"

for ts in 2 128 8192; do
  for nb in 30000 120000; do
    ( d="$TMP/ts${ts}_nb${nb}"; mkdir -p "$d"
      "$BIN" -ts $ts -mode s -num_bind $nb -seed 900001 \
             -rng fast -jumps 1 -coverstop 1 -output_dir "$d" > "$d/gen.log" 2>&1
      f=$(ls "$d"/*.dat 2>/dev/null | head -1)
      [ -n "$f" ] && cp "$f" "$OUT/ts${ts}_nb${nb}.dat"
    ) &
  done
done
wait

echo "=== RESULTADO: R_max na regiao central |y|<=90 ==="
printf "%-7s %-9s %-10s %-12s %-10s\n" ts nb R_max part/camada comprimento
for ts in 2 128 8192; do
  for nb in 30000 120000; do
    f="$OUT/ts${ts}_nb${nb}.dat"
    [ -s "$f" ] || { printf "%-7s %-9s FALTANDO\n" $ts $nb; continue; }
    awk -v ts=$ts -v nb=$nb "\$1 ~ /^uid/ {
        y=\$4+0; if(y<lo||NR==2)lo=y; if(y>hi)hi=y
        if(y>=-90 && y<=90){ c[y]++; r=sqrt(\$3*\$3+\$5*\$5); if(r>R)R=r } }
      END{ for(y=-90;y<=90;y++) if(y in c){s+=c[y]; n++}
        printf \"%-7s %-9s %-10.1f %-12.0f %-10d\n\", ts, nb, R, s/n, hi-lo+1 }" "$f"
  done
done
rm -rf "$TMP"

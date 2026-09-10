# N18: dez sementes extras em cinco $T_s$ para testar as quedas de $D_2$

**Data:** 2026-09-10 (noite)
**Afeta:** N18 (`Reviews/N18_df_ten_ts/`), a figura de $D_f$ de correlação do artigo
**Dados:** `Reviews/N18_df_ten_ts/df_periodic_by_seed.csv`, `df_periodic_summary.csv`
(regenerados com 100 cilindros); cópia dos `.dat` em
`Data_fibrils/periodic_cylinders_216_nb60000_10Ts_5seeds_plus_10seeds_5Ts.tar.gz` (fora do git)
**Cita:** `Reviews/decision_log/2026-09-10_D2_corrigida_como_figura_do_artigo.md`,
`Reviews/decision_log/2026-09-10_N18_peso_do_ajuste_e_dimensao_de_correlacao.md`

> Entrada de registro. **Append-only** — não editar.

## O que foi gerado

Cinquenta cilindros periódicos novos: sementes 900006–900015 em
$T_s \in \{2, 8, 16, 4096, 8192\}$, mesma receita dos 50 de madrugada
(`fast_dla2.cpp` do commit `17cfc1f`, `-mode s -num_bind 60000 -rng fast -period 216`),
por `Code/Data_analysis/run_periodic_cylinder_grid.sh` com
`TS_LIST="8192 4096 16 8 2" SEED_LIST="900006 … 900015" JOBS=25`, nesta máquina
(32 núcleos), das 19:20:50 às ~19:35:20: **14,5 min de parede**. Tempo médio por
cilindro com 25 em paralelo: 526 s ($T_s = 2$), 454 (8), 361 (16), 113 (4096),
138 (8192). Os 50 antigos ficaram intactos (sha256 iguais aos do README). Esses
cinco $T_s$ passam a ter 15 sementes; $T_s \in \{32, 64, 128, 512, 1024\}$
continuam com 5. Os sha256 dos 100 estão em `Reviews/N18_df_ten_ts/README.md`.

`measure_df_periodic_ten_ts.py` foi generalizado para descobrir as sementes por
glob (exige $\ge 5$ por $T_s$; coluna `n_seeds` do summary); a conferência dura
dos 15 cilindros de 2026-09-01 continua e passou (75 valores, 0 fora de $10^{-3}$).

## Motivo

Com 5 sementes pareadas, $D_2$ (correlação, $4 \le r \le \bar R/3$) caía de
$T_s = 2$ para $16$ em $-0{,}020 \pm 0{,}008$ e de $4096$ para $8192$ em
$-0{,}009 \pm 0{,}004$ (versão corrigida por disco). A pergunta: essas quedas
sobrevivem a 15 sementes, ou eram flutuação de 5?

## Resultado do teste pareado (diferença média entre $T_s$, mesma semente, ± EP)

| quantidade | par | 5 sementes | 15 sementes |
|:--|:--|--:|--:|
| `corr_primary` (bruta) | 2 → 16 | $-0{,}025 \pm 0{,}008$, 5/5 caem | $-0{,}032 \pm 0{,}004$, **15/15 caem** ($t = -7{,}4$) |
| `corr_primary_corrected` | 2 → 16 | $-0{,}020 \pm 0{,}008$, 4/5 caem | $-0{,}027 \pm 0{,}005$, **14/15 caem** ($t = -5{,}5$) |
| `corr_primary` (bruta) | 4096 → 8192 | $-0{,}009 \pm 0{,}004$, 4/5 caem | $-0{,}002 \pm 0{,}002$, 8/15 caem ($t = -0{,}8$) |
| `corr_primary_corrected` | 4096 → 8192 | $-0{,}009 \pm 0{,}005$, 4/5 caem | $-0{,}002 \pm 0{,}003$, 8/15 caem ($t = -0{,}8$) |

Leitura: a queda de $2 \to 16$ é real e ficou mais nítida (todas as sementes
caem, seis erros-padrão). A queda de $4096 \to 8192$ **não sobreviveu**: com 15
sementes é $-0{,}002 \pm 0{,}003$, metade das sementes sobe — era flutuação de 5.
Os dois $T_s$ altos são o mesmo valor, $D_2$ corrigida $1{,}925 \pm 0{,}002$.

## $D_2$ corrigida por $T_s$ com 100 cilindros (`df_periodic_summary.csv`)

| $T_s$ | `n_seeds` | $D_2$ bruta | disco | $D_2$ corrigida |
|--:|--:|--:|--:|--:|
| 2 | 15 | 1,703 ± 0,002 | 1,953 | 1,751 ± 0,003 |
| 8 | 15 | 1,686 ± 0,003 | 1,950 | 1,736 ± 0,003 |
| 16 | 15 | 1,671 ± 0,003 | 1,947 | 1,724 ± 0,003 |
| 32 | 5 | 1,684 ± 0,006 | 1,943 | 1,741 ± 0,007 |
| 64 | 5 | 1,710 ± 0,005 | 1,942 | 1,769 ± 0,004 |
| 128 | 5 | 1,747 ± 0,004 | 1,939 | 1,808 ± 0,004 |
| 512 | 5 | 1,828 ± 0,004 | 1,936 | 1,893 ± 0,004 |
| 1024 | 5 | 1,848 ± 0,006 | 1,933 | 1,915 ± 0,006 |
| 4096 | 15 | 1,858 ± 0,001 | 1,932 | 1,926 ± 0,001 |
| 8192 | 15 | 1,856 ± 0,002 | 1,933 | 1,924 ± 0,002 |

Nos cinco $T_s$ ampliados a média moveu-se no máximo 0,007 (em $T_s = 16$:
1,731 → 1,724) e o erro-padrão caiu pela metade, como se espera de $5 \to 15$.
Os outros cinco $T_s$ são os mesmos números de antes. Figuras de
`Reviews/N18_df_ten_ts/figures/` e a figura do manuscrito em `xmgrace/`
regeneradas a partir destes CSVs.

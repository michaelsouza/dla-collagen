# N18: quarenta sementes em $T_s = 16$ para testar o vale de $D_f$

**Data:** 2026-09-10 (noite, logo depois das dez sementes extras)
**Afeta:** N18 (`Reviews/N18_df_ten_ts/`), a figura de $D_f$ de correlação do artigo
**Dados:** `Reviews/N18_df_ten_ts/df_periodic_by_seed.csv`, `df_periodic_summary.csv`
(regenerados com 125 cilindros); cópia dos `.dat` em
`Data_fibrils/periodic_cylinders_216_nb60000_10Ts_5to40seeds.tar.gz` (47 MB, fora do
git; substitui `..._5seeds_plus_10seeds_5Ts.tar.gz`, apagado)
**Cita:** `Reviews/decision_log/2026-09-10_N18_dez_sementes_extras_em_cinco_ts.md`

> Entrada de registro. **Append-only** — não editar.

## O que foi gerado

Vinte e cinco cilindros periódicos novos: sementes 900016–900040 só em
$T_s = 16$, mesma receita dos 100 anteriores (`fast_dla2.cpp` do commit `17cfc1f`,
`-mode s -num_bind 60000 -rng fast -period 216`), por
`Code/Data_analysis/run_periodic_cylinder_grid.sh` com `TS_LIST=16
SEED_LIST="900016 … 900040" JOBS=25`, nesta máquina (32 núcleos), das 19:56:50
às 20:03:15: **6 min 25 s de parede**; 328 s por cilindro em média (máximo 369 s)
com 25 em paralelo. Os 100 antigos ficaram intactos (sha256 iguais aos do README
anterior). $T_s = 16$ passa a ter 40 sementes; $T_s \in \{2, 8, 4096, 8192\}$
continuam com 15 e os outros cinco com 5. Os 125 sha256 estão em
`Reviews/N18_df_ten_ts/README.md`. A medida (`measure_df_periodic_ten_ts.py`,
1 min 40 s com 10 processos) repetiu a conferência dos 15 cilindros de
2026-09-01: 75 valores, 0 fora de $10^{-3}$.

## Motivo

Com 15 sementes pareadas, `corr_primary` caía de $T_s = 2$ para $16$ em
$-0{,}032 \pm 0{,}004$ (15/15 sementes) e de $8$ para $16$ em $-0{,}015 \pm 0{,}005$:
um vale em $T_s = 16$ abaixo do DLA plano. Michael quis saber se o vale é real
ou artefato das 15 sementes — em particular, se um lote novo de sementes dá o
mesmo número.

## Resultado dos testes (`df_periodic_by_seed.csv`)

Não pareado = Welch entre as 40 sementes de $T_s = 16$ e as 15 do outro $T_s$;
pareado = mesma semente, as 15 comuns (900001–900015); EP = erro-padrão.

| quantidade | comparação | diferença $16 -$ outro ± EP | $t$ | $p$ |
|:--|:--|--:|--:|--:|
| `corr_primary` | contra $T_s = 2$, Welch (40 vs 15) | $-0{,}028 \pm 0{,}003$ | $-9{,}2$ | $3 \times 10^{-10}$ |
| `corr_primary` | contra $T_s = 2$, pareado (15) | $-0{,}032 \pm 0{,}004$, 15/15 caem | $-7{,}4$ | $3 \times 10^{-6}$ |
| `corr_primary` | contra $T_s = 8$, Welch (40 vs 15) | $-0{,}011 \pm 0{,}004$ | $-2{,}9$ | $0{,}008$ |
| `corr_primary` | contra $T_s = 8$, pareado (15) | $-0{,}015 \pm 0{,}005$, 11/15 caem | $-3{,}3$ | $0{,}006$ |
| `gyr_primary` | contra $T_s = 2$, Welch (40 vs 15) | $-0{,}031 \pm 0{,}014$ | $-2{,}2$ | $0{,}03$ |
| `gyr_primary` | contra $T_s = 2$, pareado (15) | $-0{,}036 \pm 0{,}024$, 11/15 caem | $-1{,}5$ | $0{,}16$ |
| `gyr_primary` | contra $T_s = 8$, Welch (40 vs 15) | $-0{,}020 \pm 0{,}011$ | $-1{,}8$ | $0{,}08$ |
| `gyr_primary` | contra $T_s = 8$, pareado (15) | $-0{,}024 \pm 0{,}018$, 12/15 caem | $-1{,}4$ | $0{,}2$ |

Lote de sementes em $T_s = 16$ (as 15 primeiras contra as 25 novas):

| quantidade | 900001–900015 (15) | 900016–900040 (25) | novo − antigo ± EP | Welch $t$, $p$ |
|:--|--:|--:|--:|:--|
| `corr_primary` | $1{,}6714 \pm 0{,}0031$ | $1{,}6779 \pm 0{,}0021$ | $+0{,}007 \pm 0{,}004$ | $1{,}8$, $0{,}09$ |
| `gyr_primary` | $1{,}660 \pm 0{,}019$ | $1{,}666 \pm 0{,}010$ | $+0{,}007 \pm 0{,}021$ | $0{,}3$, $0{,}75$ |

Leitura. O vale de $D_2$ em $T_s = 16$ é real: contra $T_s = 2$ fica em nove
erros-padrão com 40 sementes, e contra $T_s = 8$ em três. O lote novo de 25
sementes dá $1{,}678 \pm 0{,}002$, dentro de dois EP das 15 primeiras
($1{,}671 \pm 0{,}003$); a média de 40 subiu 0,004 (1,6714 → 1,6755) e o EP caiu
de 0,0031 para 0,0018, como se espera de $15 \to 40$. Na giração o vale tem o
mesmo sinal e tamanho ($-0{,}03$), mas a dispersão entre sementes é dez vezes
maior (as 40 vão de 1,56 a 1,82, sem valor atípico isolado), e por isso fica em
dois EP: a giração na ordem de adesão não resolve diferenças de 0,03 com 40
sementes; a correlação resolve. Nada muda na leitura de N18: o regime
$T_s \le 32$ continua DLA plano, com $D_2$ bruta em 1,68–1,70.

## $D_f$ por $T_s$ com 125 cilindros (`df_periodic_summary.csv`)

| $T_s$ | `n_seeds` | `gyr_primary` (giração, 40–2500) | `corr_primary` ($D_2$ bruta, 4–$\bar R/3$) |
|--:|--:|--:|--:|
| 2 | 15 | 1,695 ± 0,011 | 1,703 ± 0,002 |
| 8 | 15 | 1,684 ± 0,006 | 1,686 ± 0,003 |
| 16 | 40 | 1,664 ± 0,009 | 1,675 ± 0,002 |
| 32 | 5 | 1,702 ± 0,026 | 1,684 ± 0,006 |
| 64 | 5 | 1,761 ± 0,006 | 1,710 ± 0,005 |
| 128 | 5 | 1,816 ± 0,013 | 1,747 ± 0,004 |
| 512 | 5 | 1,970 ± 0,010 | 1,828 ± 0,004 |
| 1024 | 5 | 1,974 ± 0,010 | 1,848 ± 0,006 |
| 4096 | 15 | 1,974 ± 0,006 | 1,858 ± 0,001 |
| 8192 | 15 | 1,980 ± 0,005 | 1,856 ± 0,002 |

Antes, com 15 sementes, $T_s = 16$ dava $1{,}660 \pm 0{,}019$ (giração) e
$1{,}671 \pm 0{,}003$ (correlação). Os outros nove $T_s$ são os mesmos números.
Figuras de `Reviews/N18_df_ten_ts/figures/` e os projetos xmgrace
(`df_corr_vs_ts.*`, `df_gyr_vs_ts.*`) regenerados a partir destes CSVs.

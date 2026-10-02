# Dados do N18 para o xmgrace

## `df_corr_vs_ts.*` — figura escolhida para o manuscrito (2026-09-10)

Michael decidiu em 2026-09-10 que esta é a única figura de $D_f$ do N18 que vai
para o artigo: a dimensão de correlação **bruta** contra $T_s$ (curva sem correção de borda, referências em 2 e 1,71; decisão de 2026-09-10 à noite, pela simplicidade), rótulo $D_f$, uma série só,
azul, rótulos em en-US (registro
`Reviews/decision_log/2026-09-10_D2_corrigida_como_figura_do_artigo.md`).

**Gerado por:** `Code/Data_analysis/build_df_corr_vs_ts_xmgrace.py`, que escreve os
`.dat`, o `.agr` (primeira versão; dali em diante editado no xmgrace) e o
`df_corr_vs_ts.pdf` de conferência.
**Fonte:** `../df_periodic_summary.csv`, colunas `corr_primary_mean`
e `_se`, produzidas por `measure_df_periodic_ten_ts.py` sobre os 125 cilindros (40 sementes em $T_s = 16$; 15 em $T_s = 2, 8, 4096, 8192$; 5 nos outros)
periódicos (receita e sha256 em `../README.md`).

| arquivo | séries | tipo | conteúdo |
|:--|:--|:--|:--|
| `df_corr_vs_ts_xydy.dat` | 1 | `xydy` | $T_s$, $D_f$ (correlação, bruta), erro-padrão sobre sementes |
| `df_reference_lines_xy.dat` | 2 | `xy` | linhas em 2 (disco uniforme) e 1,71 (DLA plano) |

Eixo $x$ logarítmico, $y$ linear de 1,6 a 2,05. Como $D_2$ foi calculada:
`../README.md` §1 e `../relatorio_N18.qmd`, seção "Dimensão de correlação".

## `df_by_ts_xydy.dat` — os quatro estimadores (interno)

Blocos: giração $40 \le N \le N_{\max}/2$ (30 pontos por oitava), correlação
corrigida, massa–raio relativa, massa–raio fixa 4–8; `xydy` com erro-padrão entre
sementes. Escrito por `measure_df_periodic_ten_ts.py`. Não tem `.agr`.

## `frup_per_rod_by_width_xydy.dat` — $F_{rup}/R$ contra a largura (interno)

Escrito por `summarize_width_fracture.py`; ver `../README.md` §3.

## `df_gyr_vs_ts.*` — a mesma figura com o raio de giração (interno)

`build_df_corr_vs_ts_xmgrace.py --estimator gyr`: $D_f$ da giração na ordem de
adesão ($40 \le N \le N_{\max}/2$, 30 pontos por oitava; coluna `gyr_primary`),
mesmo estilo e mesmas referências, para comparar com a curva do artigo. Não vai
para o manuscrito.

## `trunk_geometry_vs_ts.*`, `geometry_during_fracture_{F,Frup}.*` — geometria do tronco (en-US, interno)

`build_trunk_geometry_xmgrace.py`, a partir de `../trunk_geometry_by_ts.csv` e
`../geometry_during_fracture_curves.csv`. Dois eixos y = dois gráficos na mesma
VIEW: G0 (eixo esquerdo, $\langle N\rangle$, segmentos por camada, linha cheia) e
G1 (eixo direito, $\langle K\rangle$, coordenação, tracejada; sem moldura nem eixo
x), na notação do artigo. Até 2026-10-01 as letras estavam trocadas: o antigo
`*_K_xydy.dat` é o atual `*_N_xydy.dat` e vice-versa. Um `.dat` por eixo:

| arquivo | séries | tipo |
|:--|:--|:--|
| `trunk_geometry_vs_ts_{N,K}_xydy.dat` | bastões que portam carga (`xydy`, EP entre sementes); todos os bastões (`xy`) | — |
| `geometry_during_fracture_{F,Frup}_{N,K}_xydy.dat` | uma por $T_s$ (2, 8, 16, 32, 64, 128), valor/inicial e EP/inicial | `xydy` |

Nas figuras da dinâmica as barras estão desligadas (`ERRORBAR OFF`); os `.dat`
as carregam. Cores viridis mapeadas em 30–35; G0 azul (20) e vermelho (21) na
figura inicial.

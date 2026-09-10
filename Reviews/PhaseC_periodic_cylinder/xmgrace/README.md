# Curva massa–raio dos cilindros periódicos largos — dados para o xmgrace

**Figura interna** (não entra no manuscrito): $\langle m(R)\rangle$ contra $R$
em log-log, uma série por $T_s \in \{2, 128, 8192\}$, sobre os mesmos quinze
cilindros de `../df_wide_cylinders.csv` (5 sementes por condição, `nb`=60.000,
período 216, 5.000 partículas por seção). Pedida por Michael em 2026-09-09
para ver a curva inteira que os $D_f$ daquela tabela resumem.

**Gerado por:** `Code/Data_analysis/export_periodic_cylinder_mass_radius_xmgrace.py`
(os `.dat` e o CSV) e `Code/Data_analysis/build_mass_radius_xmgrace_project.py`
(o `.agr` e o PDF).
**Fonte:** os `.dat` dos cilindros, regenerados nesta máquina em 2026-09-09 com
a receita do cabeçalho de `../df_wide_cylinders.csv` (`fast_dla2` do commit
`17cfc1f`, `-mode s -rng fast -period 216`), porque o cluster estava fora de
alcance. Os arquivos brutos não são versionados: 10 min por cilindro em
$T_s=2$, e a receita os reproduz bit a bit.

**Prova de que são os mesmos cilindros do cluster:** nos quinze, o $D_f$ da
janela fixa $4$–$8$ e o da relativa $0{,}15R$–$0{,}5R$ coincidem com as colunas
registradas **à quarta casa** — o script se recusa a escrever se não
coincidirem. O `R_max` daquele CSV, por outro lado, fica 2–4% abaixo da maior
distância de partícula ao centro da seção medida aqui; foi gravado por outra
regra que o script de 2026-09-01 não registrou. Isso não afeta nenhum $D_f$
de janela fixa ou relativa, que não dependem de $R_{\max}$.

## Os arquivos

| arquivo | conteúdo |
|:--|:--|
| `mass_radius_by_ts_xy.dat` | 3 séries `xy`, $R$ de 1 até o maior $R_{\max}$ da condição; média sobre 12 seções × 5 sementes |
| `mass_radius_curves.csv` | o mesmo, com o desvio-padrão entre as 60 seções |
| `mass_radius_by_ts.agr`, `.pdf` | o projeto e a impressão; `S0`–`S2` curvas, `S3`–`S5` símbolos esparsos com a legenda, `S6`–`S7` retas-guia $R^2$ e $R^{1{,}68}$ |

## O que a curva mostra

| $R$ | $T_s=2$ | $T_s=128$ | $T_s=8192$ |
|--:|--:|--:|--:|
| 3 | 6,9 | 19,5 | 20,9 |
| 10 | 68 | 208 | 223 |
| 30 | 440 | 1.405 | 1.928 |
| 60 | 1.408 | 4.086 | 4.890 |
| 150 | 4.954 | — | — |

As três curvas saturam em 5.000, a massa da seção. $T_s=128$ e $8192$ quase
coincidem até $R\approx20$ e só se separam perto da borda; $T_s=2$ fica um
fator 3 abaixo em todo o alcance, com inclinação menor. Nenhuma das três é
uma reta em todo o intervalo: a inclinação local cai conforme $R$ se aproxima
da borda, e é isso que faz o $D_f$ depender da janela (ver `../README.md` §4c e
`../df_local_slopes_wide.csv`).

## Raio de giração na ordem de crescimento (2026-09-09)

Segunda figura, pedida por Michael: `gyration_by_ts.pdf`, com `gyration_by_ts_xy.dat`
e `gyration_by_ts.agr`. Gerada por `Code/Data_analysis/export_periodic_cylinder_gyration_xmgrace.py`
e `build_gyration_xmgrace_project.py`, sobre os mesmos quinze cilindros.

**Método.** O `uid` é a ordem de adesão. Em cada seção, tomam-se os bastões
que a cruzam na ordem em que aderiram e calcula-se o raio de giração $R_g(N)$
das posições $(x,z)$ dos $N$ primeiros. Em crescimento fractal, $N \sim R_g^{D_f}$
(Witten & Sander 1981). $D_f$ é a inclinação de $\log N$ contra $\log R_g$,
ajustada por semente sobre a média das 12 seções; a tabela traz média e
erro-padrão entre as cinco sementes. Cada seção tem cerca de 5.000 bastões, e
$N$ vai de 1 a esse valor: são 2,1 décadas em $N$, contra ~1,2 em $R$ no
método massa–raio.

**Resultado** (`../df_gyration_wide_cylinders.csv`; inclinações por oitava em
`../df_gyration_local_slopes.csv`):

| $T_s$ | $N$ 40–320 | $N$ 320–5000 | $N$ 40–5000 | massa–raio, janela relativa |
|--:|--:|--:|--:|--:|
| 2 | 1,68 ± 0,06 | 1,73 ± 0,02 | **1,71 ± 0,01** | 1,675 ± 0,023 |
| 128 | 1,96 ± 0,01 | 1,70 ± 0,02 | 1,73 ± 0,01 | 1,691 ± 0,047 |
| 8192 | 1,99 ± 0,01 | 1,90 ± 0,02 | **1,93 ± 0,01** | 1,955 ± 0,012 |

Em $T_s=2$ a inclinação local fica entre 1,67 e 1,77 em todas as oitavas de
$N=40$ a $5000$: um patamar de duas décadas em 1,71, o valor do DLA plano. Em
$T_s=8192$ fica em 1,93–2,03 até $N\approx1280$ e cai a 1,86 na última oitava,
que é a periferia. Em $T_s=128$ há dois regimes nítidos: 1,96–1,99 até
$N\approx300$ (o miolo compacto) e 1,60–1,76 dali em diante (a periferia
aberta que cresceu por último). É a mesma leitura do §4c — o miolo é compacto e
a borda não —, agora vista na ordem em que a seção cresceu.

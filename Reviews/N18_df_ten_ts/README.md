# N18 — $D_f$ nos dez $T_s$, escalas mecânicas em $m$, $F_{rup}$ contra a largura

Trabalho **interno** de 2026-09-10, feito nesta máquina (32 núcleos), sem cluster.
N7 e N12 estão fechados no manuscrito; nada daqui entra no artigo sem decisão nova.
Registro: `Reviews/decision_log/2026-09-10_N18_df_dez_ts_e_escalas_mecanicas.md`.
Relatório em prosa: `relatorio_N18.qmd` (renderizar com `quarto render relatorio_N18.qmd`; HTML e PDF fora do git).

## Os cilindros

Cento e vinte e cinco cilindros periódicos: dez $T_s \in \{2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192\}$
× cinco sementes (900001–900005) gerados na madrugada de 2026-09-10, mais dez
sementes extras (900006–900015) em $T_s \in \{2, 8, 16, 4096, 8192\}$ geradas na
noite de 2026-09-10 (registro `../decision_log/2026-09-10_N18_dez_sementes_extras_em_cinco_ts.md`),
mais 25 sementes (900016–900040) só em $T_s = 16$, geradas logo depois
(registro `../decision_log/2026-09-10_N18_quarenta_sementes_em_ts_16.md`);
$T_s = 16$ tem portanto 40 sementes, $T_s \in \{2, 8, 4096, 8192\}$ têm 15 e os
outros cinco têm 5. `nb` = 60.000,
período 216, gerados por `Code/Data_analysis/run_periodic_cylinder_grid.sh`
(grade por `TS_LIST` e `SEED_LIST`) com o `fast_dla2.cpp` do commit
`17cfc1f` (árvore em `438fd6f`, sem diff local), `g++ 13.3 -O2`, receita
`-ts T -mode s -num_bind 60000 -seed S -rng fast -period 216`. Tempo por cilindro,
com 25 em paralelo: de 85 s ($T_s = 1024$) a 470 s ($T_s = 2$).

Os `.dat` **não são versionados**. Reprodução bit a bit pela receita: os 15 de
$T_s = 2, 128, 8192$ reproduzem os 75 valores de `../PhaseC_periodic_cylinder/df_wide_cylinders.csv`
e `df_gyration_wide_cylinders.csv` a $10^{-3}$ (`identity_check_15_cylinders.csv`;
o script se recusa a escrever se não). Cópia de segurança em
`Data_fibrils/periodic_cylinders_216_nb60000_10Ts_5to40seeds.tar.gz`
(125 cilindros, fora do git). Os sha256 dos 125 estão no fim deste README.

## Seção transversal e métodos

A seção é a do artigo (`paper_PRE.tex:141`) e de `measure_df_periodic.py`: na camada
$L$ entram as moléculas cujo bastão de 18 cruza o plano $y = L$, um ponto $(x, z)$
por molécula; $L = 0, 18, \dots, 198$ (12 seções por anel); toda molécula cai em
exatamente uma seção, ~5.000 por seção. Média sobre seções e depois sobre sementes;
erro = erro-padrão entre as sementes do $T_s$ (coluna `n_seeds` do summary: 40, 15 ou 5).
Confirmado com Michael em 2026-09-10.

- **Raio de giração na ordem de crescimento** (regra principal): `uid` é a ordem de
  adesão; $R_g(N)$ dos $N$ primeiros pontos da seção; $N \sim R_g^{D_f}$; ajuste de
  $\log N$ contra $\log R_g$ em $40 \le N \le N_{\max}/2 = 2500$ (1,8 década), com
  30 pontos por oitava igualmente espaçados em $\log N$ (peso corrigido na segunda
  rodada; ver §1).
- **Massa–raio**: $m(R)$ em torno do centro de massa da seção; janelas relativa
  $0{,}15\bar R \le r \le 0{,}5\bar R$, fixa $4 \le r \le 8$, faixa cheia $5 \le r \le R_{\max}$.
- **Dimensão de correlação** $D_2$ da seção final, $C(r)$ sobre todos os pares,
  $4 \le r \le \bar R/3$, com controle de disco uniforme para a borda (segunda rodada).
- Inclinações locais por oitava em $N$, por meia década em $r$ (correlação) e por
  faixa de $r$ (massa–raio) em `df_periodic_local_slopes.csv`: sobre a curva média
  da semente (`slope_mean`, EP entre sementes) e por seção (`slope_section_*`,
  EP sobre 12 × $n$ seções, 60, 180 ou 480). Figura: `figures/local_slope_curves.png`.

Script: `Code/Data_analysis/measure_df_periodic_ten_ts.py`.

## 1. $D_f$ por $T_s$ (`df_periodic_summary.csv`)

| $T_s$ | $n$ | $\bar R$ | giração 40–2500 (30/oitava) | (todos os $N$) | giração 40–320 | giração 320–5000 | $D_2$ 4–$\bar R/3$ bruta | disco | $D_2$ corrigida | m–r relativa |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 2 | 15 | 163 | **1,695 ± 0,011** | 1,701 | 1,69 ± 0,02 | 1,71 ± 0,01 | 1,703 ± 0,002 | 1,953 | 1,751 ± 0,003 | 1,690 ± 0,011 |
| 8 | 15 | 143 | **1,684 ± 0,006** | 1,693 | 1,66 ± 0,02 | 1,71 ± 0,01 | 1,686 ± 0,003 | 1,950 | 1,736 ± 0,003 | 1,693 ± 0,013 |
| 16 | 40 | 126 | **1,664 ± 0,009** | 1,681 | 1,65 ± 0,01 | 1,71 ± 0,01 | 1,675 ± 0,002 | 1,948 | 1,728 ± 0,002 | 1,673 ± 0,009 |
| 32 | 5 | 105 | **1,702 ± 0,026** | 1,662 | 1,82 ± 0,02 | 1,65 ± 0,02 | 1,684 ± 0,006 | 1,943 | 1,741 ± 0,007 | 1,617 ± 0,025 |
| 64 | 5 | 94 | **1,761 ± 0,006** | 1,704 | 1,89 ± 0,03 | 1,67 ± 0,02 | 1,710 ± 0,005 | 1,942 | 1,769 ± 0,004 | 1,591 ± 0,021 |
| 128 | 5 | 86 | **1,816 ± 0,013** | 1,742 | 1,96 ± 0,01 | 1,69 ± 0,02 | 1,747 ± 0,004 | 1,939 | 1,808 ± 0,004 | 1,690 ± 0,021 |
| 512 | 5 | 75 | **1,970 ± 0,010** | 1,931 | 2,01 ± 0,02 | 1,84 ± 0,01 | 1,828 ± 0,004 | 1,936 | 1,893 ± 0,004 | 1,899 ± 0,011 |
| 1024 | 5 | 69 | **1,974 ± 0,010** | 1,956 | 1,99 ± 0,01 | 1,91 ± 0,01 | 1,848 ± 0,006 | 1,933 | 1,915 ± 0,006 | 1,946 ± 0,009 |
| 4096 | 15 | 67 | **1,974 ± 0,006** | 1,962 | 2,00 ± 0,01 | 1,94 ± 0,01 | 1,858 ± 0,001 | 1,932 | 1,926 ± 0,001 | 1,963 ± 0,003 |
| 8192 | 15 | 66 | **1,980 ± 0,005** | 1,966 | 1,99 ± 0,01 | 1,94 ± 0,01 | 1,856 ± 0,002 | 1,933 | 1,924 ± 0,002 | 1,958 ± 0,003 |

**Peso do ajuste (corrigido na segunda rodada de 2026-09-10).** A primeira
rodada ajustava a reta sobre todos os $N$ inteiros da janela: 2.200 pontos acima
de 300 e 260 abaixo, logo o "principal" media a periferia. Agora a reta usa 30
pontos por oitava, igualmente espaçados em $\log N$ (coluna "todos os $N$" = valor
antigo, só para comparação). Nos extremos muda 0,01–0,02; no cotovelo, até 0,07
($T_s = 128$: 1,74 → 1,82). É a diferença entre pesar a periferia e pesar a curva.

**Dimensão de correlação $D_2$** (nova na segunda rodada): $C(r)$ = fração dos
pares de pontos da seção final a distância $\le r$; $D_2$ = inclinação de
$\log C$ contra $\log r$ em $4 \le r \le \bar R/3$ (~1 década). Não depende de
centro nem da ordem de adesão, e usa todos os pares. Tem efeito de borda: um
disco uniforme com o mesmo $n$ e o mesmo $\bar R$ (coluna "disco", 12 por
cilindro) dá 1,93–1,95 em vez de 2 só por tamanho finito; a coluna "corrigida" é
medido − disco + 2. Mesmo corrigida, $D_2$ fica em 1,92 no regime compacto, abaixo
dos 1,97 da giração: porque $D_2$ pesa **todos** os pares da seção final, miolo e
periferia juntos, e a periferia é DLA até $T_s = 8192$ (giração 320–5000 dá 1,92).
A giração na ordem de adesão separa miolo de periferia; $D_2$ é a média dos dois.
Barra de $D_2$ entre sementes de 0,001–0,007: é o estimador mais reprodutível,
mas a barra não mede a escolha de janela. Inclinação local dos dois estimadores,
com barra sobre 12 × $n$ seções: `figures/local_slope_curves.png`.

**Leitura.** Duas famílias, não uma curva suave: de $T_s = 2$ a $128$ a regra
principal fica em 1,68–1,70 (o DLA plano), de $64$ a $128$ sobe (1,76, 1,82) e de
$512$ em diante fica em 1,97 (compacto). A janela do miolo (40–320) e a da periferia (320–5000) mostram por quê:
o miolo compacta primeiro. As inclinações locais por oitava em $N$
(`df_periodic_local_slopes.csv`) dão o $N$ em que a seção deixa de ser compacta,
lido como a primeira oitava com inclinação abaixo de 1,85:

| $T_s$ | 2–16 | 32 | 64 | 128 | 512 | 1024 | 4096 | 8192 |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| miolo compacto até $N \approx$ | < 40 | 320 | 320 | 320–640 | 1280 | 1280 | > 2560 | 2560 |

Ou seja: o crescimento é compacto até um $N_c(T_s)$ e DLA dali em diante, e
$N_c$ cresce com $T_s$. Uma janela fixa em $N$ ou em $r$ mede a fração de miolo que
ela cobre, e é isso que o "$D_f$ intermediário" sempre foi. Nas fibrilas livres
(~300 moléculas por seção) as janelas cabem dentro do miolo a partir de
$T_s \approx 64$, e por isso lá o platô parece começar em 128 (relatório §4); com
5.000 moléculas por seção a janela 40–2500 só é toda miolo a partir de 512.

A janela relativa massa–raio concorda com a giração nos extremos (1,675 / 1,955)
e no salto; a fixa 4–8 vê só o miolo e dá ~1,95 já em $T_s = 32$; a faixa cheia
inclui a saturação e fica abaixo de tudo. Nenhuma delas é "a" dimensão fractal
em $32 \le T_s \le 128$, porque ali não há uma só.

## 2. Escalas mecânicas em $m$ e convergência em $T_s$

`Code/Data_analysis/analyze_frup_m_scaling.py` sobre `N9_damage_curves/` e os 50
`.npz` de `N10_cascade_survival/` (só dados existentes). Saídas
`frup_m_separability.csv`, `statistics_two_way_decomposition.csv`,
`cascade_stats_by_condition.csv`.

**$F_{rup}$ separa em $A(T_s)\,g(m)$.** Com $g(m)$ = média geométrica de
$F(T_s,m)/F(T_s,2)$ sobre $T_s \ge 16$:

| $m$ | 1 | 2 | 3 | 5 | 10 |
|:--|--:|--:|--:|--:|--:|
| $g(m)$ empírico | 0,588 | 1 | 1,221 | 1,437 | 1,616 |
| ELS $\sigma^*(m)/\sigma^*(2)$, $\sigma^* = \tfrac{m}{m+1}(m+1)^{-1/m}$ | 0,650 | 1 | 1,228 | 1,513 | 1,858 |

Espalhamento máx/mín de $F_{rup}$ sobre os cinco $m$, por $T_s$: bruto 2,7–3,9;
depois de dividir por $g(m)$: **1,41 (2), 1,12 (8), 1,03 (16), ≤ 1,02 de 32 a 8192**;
depois de dividir pelo nulo ELS: 1,14–1,16 em todo $T_s \ge 16$. Os resíduos em
$\log F$ ficam dentro do erro-padrão para $T_s \ge 32$ (máx 0,011 contra EP ~0,01)
e fora dele em $T_s = 2$ (0,26) e $8$ (0,10). A decomposição em dois fatores dá
parcela de interação 0,2% para $F_{rup}$ e $f_{rup}/N$, 0,4% para $\varphi$
preterminal, 2% para a fração terminal — e **26–40% para a fração de cascatas
unitárias, p90, p99 e tamanho médio**. Conclusão medida: $m$ sai como fator da
força e do dano no regime compacto, não sai da forma da distribuição de cascatas.
O desvio de $g(m)$ em relação ao ELS (−10% em $m=1$, −13% em $m=10$) é a assinatura
do canal local $K_i$ (relatório §5 já dizia "não é ELS puro").

**Onde cada grandeza satura em $T_s$** (`df_vs_mechanics_by_ts.csv`; menor $T_s$
a partir do qual tudo fica a 5% do valor em 8192):

| grandeza | satura em |
|:--|--:|
| $D_f$ giração | 512 |
| $D_f$ massa–raio relativa | 1024 |
| moléculas no tronco 17×17 | 512 |
| $F_{rup}/N$, $m = 2$ | 512 |
| $\varphi$ preterminal, $m = 2$ | 32 |
| fração de cascatas $s = 1$ | 2 (varia 2,6% em toda a grade) |
| p99 das cascatas, $m = 2$ | 16 (cai de 35 em $T_s = 2$ a 13 em 16; depois 11–13) |

$D_f$ e $F_{rup}/N$ saturam juntos, em 512 — mas os dois seguem o mesmo confundidor,
a compactação da seção (N12: $N \sim R^{D_f}$ por construção). O dano preterminal
satura muito antes (32), e a cauda das cascatas (p99) em 16: a estatística de
avalanches é a mesma de $T_s = 16$ em diante, enquanto $D_f$ ainda é DLA até 128.
"Convergir junto" vale para $D_f$ e força; não para dano nem avalanches, que
convergem antes.

## 3. $F_{rup}$ contra a largura

`Code/Data_analysis/run_local_width_fracture.sh`: os cilindros de $T_s \in \{2, 32, 128, 8192\}$
(5 sementes) abertos em $y = \pm 108$, estendidos e fraturados pelo motor da campanha
(`fiber_bundle_ava.py`, $m = 2$, semente de fratura 101, 10 realizações) em dois
recortes: 17×17 (`-half-width 8`, o tronco publicado) e 41×41 (`-half-width 20`).
Custo: 17×17 em segundos; 41×41 de 73 s ($T_s = 32$) a 280 s ($T_s = 128$) por
realização, 12 processos em paralelo, 1 h 10 no total. Determinismo conferido: a
primeira realização de 128/900001 em 17×17 com semente 1 é **byte a byte** igual
ao primeiro bloco de `../PhaseC_periodic_cylinder/avalanche_ladder_raw/ts128_w17.txt`.
Brutos em `width_fracture_raw/`; resumo por `summarize_width_fracture.py`.

$R$ = moléculas portantes (soma exata das removidas; a escada estimava $P_0/16{,}6$).
Erro-padrão sobre as médias por semente:

| $T_s$ | recorte | $R$ | $F_{rup}$ | $F_{rup}/R$ | fração terminal | p99 preterminal | máx. preterminal |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 2 | 17×17 | 649 | 170 ± 14 | 0,262 ± 0,019 | 0,815 | 27 | 34 |
| 2 | 41×41 | 2.108 | 544 ± 30 | 0,260 ± 0,012 | 0,701 | 69 | 150 |
| 32 | 17×17 | 1.811 | 992 ± 75 | 0,547 ± 0,037 | 0,896 | 9,0 | 16 |
| 32 | 41×41 | 7.263 | 3.802 ± 156 | 0,524 ± 0,022 | 0,887 | 13,0 | 57 |
| 128 | 17×17 | 2.281 | 1.480 ± 40 | 0,649 ± 0,016 | 0,898 | 10,3 | 21 |
| 128 | 41×41 | 11.369 | 7.684 ± 201 | 0,676 ± 0,010 | 0,896 | 10,4 | 49 |
| 8192 | 17×17 | 2.405 | 1.683 ± 86 | 0,700 ± 0,036 | 0,895 | 10,1 | 20 |
| 8192 | 41×41 | 13.575 | 9.779 ± 93 | 0,721 ± 0,008 | 0,898 | 11,2 | 50 |

Escada de 02/09 (uma semente, 900001, semente de fratura 1), para continuidade:
$T_s = 128$: $F_{rup}/R$ = 0,682 (17), 0,649 (41), 0,649 (81), 0,638 (181);
$T_s = 8192$: 0,605 (17), 0,703 (141).

**Resposta.** $F_{rup}$ é **extensiva** em $R$: de 17×17 para 41×41, $R$ cresce
3,3–5,7× e $F_{rup}$ cresce 3,2–5,8×; a força por molécula portante muda de
−4% a +4%, dentro do erro, em todos os quatro $T_s$. Junto com a escada (25× em
$R$ em $T_s = 128$, −7% em $F_{rup}/R$), a resposta é sim: como a distribuição de
avalanches, $F_{rup}/R$ não depende da largura. O que depende é $R$, e $R$ é o que
$T_s$ muda no tronco 17×17 (602 → 2.321 moléculas).

**O que a rodada acrescentou, e a escada não tinha visto.** A invariância da
*cauda* das cascatas com a largura foi estabelecida em $T_s = 128$ e $8192$ e
**vale lá** (p99 ×1,01 e ×1,11). Não vale na estrutura aberta: em $T_s = 2$ o p99
preterminal vai de 27 a 69 (×2,6), o máximo de 34 a 150 (×4,5) e a fração
terminal cai de 0,82 a 0,70; em $T_s = 32$ o p99 sobe ×1,4. No regime DLA o
corte das cascatas **cresce com a largura**, isto é, é de tamanho finito. Isso não
contradiz o manuscrito, que afirma o corte intrínseco na grade de tronco 17×17 e
a invariância em tamanho para $T_s = 128$; mas é uma ressalva a registrar: a
frase "o corte é dinâmico, não de tamanho finito" está demonstrada para a
seção compacta, não para a aberta. Cinco sementes × dez realizações, um só
passo de largura (3,3×): suficiente para ver o sinal, não para medir o expoente.

## Checksums dos 125 cilindros (sha256)

```
2702e316ab81a30178d97bb89d3fe9fc3ab10f22232112b87f654878d4f057c1  dla_per216_mode_s_ts_1024_nb_60000_seed_900001_.dat
972ee6cd555394dc2f6653f032178baa6dad9b4f70ff08dc6e13b36290cc8c77  dla_per216_mode_s_ts_1024_nb_60000_seed_900002_.dat
271443ee48e90f2c688211b1b6f5a0d66b6b238bee5f4798f6f70b15ec2c32f1  dla_per216_mode_s_ts_1024_nb_60000_seed_900003_.dat
5514ed369b4d169e29101f20ad281aadd0698183aee3dd1e97adbd69548c5708  dla_per216_mode_s_ts_1024_nb_60000_seed_900004_.dat
54b91312a7ba69574bb4a26538c96a69e3245b5f94732a91a6b63a085c58ec9d  dla_per216_mode_s_ts_1024_nb_60000_seed_900005_.dat
c448a3ee37d714a6abeb0b0146e5c3553f2b6fca678904834eb2b6e40896eaf3  dla_per216_mode_s_ts_128_nb_60000_seed_900001_.dat
7501a674985c27e68455fa6120732019c4b4e3c70c22d9cb3607beffbcb75a1a  dla_per216_mode_s_ts_128_nb_60000_seed_900002_.dat
ff7ef7fb0f7b5c59dc95128438e505de86ceb6ca356f858968dae831d975c24f  dla_per216_mode_s_ts_128_nb_60000_seed_900003_.dat
427e7ad9080cccd0508c0df18f82388943799136fce2ea3c072679e6f65b638c  dla_per216_mode_s_ts_128_nb_60000_seed_900004_.dat
bd86e820be858020ad7dba38c5eb859ad4678fc740c0a3279de4f8ca2c658325  dla_per216_mode_s_ts_128_nb_60000_seed_900005_.dat
8c2a579e483531de382084b32e7c847490b0ad9ef43cd844d50aa13570c8303f  dla_per216_mode_s_ts_16_nb_60000_seed_900001_.dat
55d018c7c8e5ca035375118b03717e7d4804b67a4c6c727078ca5a1baef396d7  dla_per216_mode_s_ts_16_nb_60000_seed_900002_.dat
d9ffc59be2c142f769791796b277accf41fc1ef35b6555e2df56b261beefeaca  dla_per216_mode_s_ts_16_nb_60000_seed_900003_.dat
bd9ac711ed939714e1e66c16e9f467c5a75177ed21ea0a274545db02ada98f4e  dla_per216_mode_s_ts_16_nb_60000_seed_900004_.dat
2c69f7f336d4ce7ad83d80e249cce48db4953c02a02b2b33ac955f434fbb6ef0  dla_per216_mode_s_ts_16_nb_60000_seed_900005_.dat
cede52b2da6dea7e7523082d15a9586dafdfce732cd352b417ac7c5c28ffeeb0  dla_per216_mode_s_ts_16_nb_60000_seed_900006_.dat
f7bd43bcee436b3c51e50d1691c662f5e155e0a873566ee3d9f6eb75731b483a  dla_per216_mode_s_ts_16_nb_60000_seed_900007_.dat
803aac44d449101f07f5cd966c7917b6fba717dfc96c5e239ab8265fdd4a2428  dla_per216_mode_s_ts_16_nb_60000_seed_900008_.dat
5b3e499755e0966bc392bdc54d9375d67589e936ee14272f1a2e614d49103c09  dla_per216_mode_s_ts_16_nb_60000_seed_900009_.dat
43c4a012730c659909781ab47d2491ff80e63c66bd6db3a9e8bb3910af414413  dla_per216_mode_s_ts_16_nb_60000_seed_900010_.dat
04cabb0afbd299eff7d6b388b32b74a12725dbd3e7df370631e95490839953c1  dla_per216_mode_s_ts_16_nb_60000_seed_900011_.dat
9976539bdb3f917bafb3806d317e348928b3191149edc816d6b15686cbf8efe4  dla_per216_mode_s_ts_16_nb_60000_seed_900012_.dat
3d9c1b678a0a99aea6537ebf0e49fdddc7070ea93255752367dc302455436c3c  dla_per216_mode_s_ts_16_nb_60000_seed_900013_.dat
682cd9eb7e003e58777fa394a6a3d5b62251fdbe1a951850f68e01e5a85e8c1f  dla_per216_mode_s_ts_16_nb_60000_seed_900014_.dat
12b32f009bf832009f03e9a55f138b918c3ce022f2b7473c950fa7b218d1e0a8  dla_per216_mode_s_ts_16_nb_60000_seed_900015_.dat
3690a8384d9e4e639310d36f6a6f24c0c4bdfb5eb93a1e61a5ba634524857d84  dla_per216_mode_s_ts_16_nb_60000_seed_900016_.dat
ab93183356ebc390cbde65658717689c1567a06e9f93d82172e2320155fb4236  dla_per216_mode_s_ts_16_nb_60000_seed_900017_.dat
556219ec934258b9e259ed974fb83e07fbebf317bb371b49525acba5ec4d7f9e  dla_per216_mode_s_ts_16_nb_60000_seed_900018_.dat
cb0486aec83a0e7d0b6823d5611cddede99d6b00d0df2d436bd10198bbbe1234  dla_per216_mode_s_ts_16_nb_60000_seed_900019_.dat
17b0c52cb591ebaf8b221eb126bd162d556f9291e0d3464c30c6324896d6a714  dla_per216_mode_s_ts_16_nb_60000_seed_900020_.dat
7aa102b789bc65116f070c754cd8e10a5767e2318306743eac00e366bc58ea27  dla_per216_mode_s_ts_16_nb_60000_seed_900021_.dat
335e89dafdc7b9d3c9c4e83c18e6958e330e98c615ec0277746bdaba2712a9a3  dla_per216_mode_s_ts_16_nb_60000_seed_900022_.dat
2fc34bc8e44ad805cb5040d51745f9c600362eeb357312e857648bf4321ba4e3  dla_per216_mode_s_ts_16_nb_60000_seed_900023_.dat
766f47b83b86e3ea00354d4f2066408b76afe4673006cf7e0c04a015e04fbe5c  dla_per216_mode_s_ts_16_nb_60000_seed_900024_.dat
30fd6858204167376ece0fbf6ca72f9e72206eadc7bd414441e4aa63a308f324  dla_per216_mode_s_ts_16_nb_60000_seed_900025_.dat
505880a264eac05a44b28fb7d6d435a9c660f24374f67b1cdba30944f2c2343e  dla_per216_mode_s_ts_16_nb_60000_seed_900026_.dat
9abcd169e3fa36c6a55ee957aafdb7a7bff491423b2a29b9cf44ff7261dffc41  dla_per216_mode_s_ts_16_nb_60000_seed_900027_.dat
4f65bfa9cd132faf837cef2b6aed53e51415323ae9b30a93c71b2a6319a1d433  dla_per216_mode_s_ts_16_nb_60000_seed_900028_.dat
95d78b2c1905b864c1248b7ebcd11d9570c92e799fb210caedca7ce90f8d6c10  dla_per216_mode_s_ts_16_nb_60000_seed_900029_.dat
875a7083efb18cb06f9e365d9791c3ca8ceb60e666ec3171213ac5bc9f221c3d  dla_per216_mode_s_ts_16_nb_60000_seed_900030_.dat
3d526dfb6e07d47d7938335426fc920a5a7110b1c4e5439ed838485bb99cb3f8  dla_per216_mode_s_ts_16_nb_60000_seed_900031_.dat
a17c146955edd1990fbb24d4f95b56ef3c62600026c50f5ff223221533371d1c  dla_per216_mode_s_ts_16_nb_60000_seed_900032_.dat
db88c4d1e044250c03c56cab4fec71ffcd474efef0bf1e62b11733d27e63fda3  dla_per216_mode_s_ts_16_nb_60000_seed_900033_.dat
0c5fec211517dd8f60d155763c1c84a9e93bc11bfe6603b2e1abafb7d1dd4c82  dla_per216_mode_s_ts_16_nb_60000_seed_900034_.dat
a35e8587f9faa0f047540f03270faffe7ef5707525e5c75f5629f7e8e1717f3b  dla_per216_mode_s_ts_16_nb_60000_seed_900035_.dat
ec11a920783154406a02eac010e3ba0807686e42926e30067d05d2f135f57e6e  dla_per216_mode_s_ts_16_nb_60000_seed_900036_.dat
fe5bf1301adda479de0df2b475941f0006325b8e2d1f7b4567aff3a59a35b0ee  dla_per216_mode_s_ts_16_nb_60000_seed_900037_.dat
a00857ad3f589522e35bf04bd12b1262741e15b0f573201e940d41b7700ce82d  dla_per216_mode_s_ts_16_nb_60000_seed_900038_.dat
bd125f7a018153af73ebedc53ff321de5970bcf417ec993f8e15329be1ed8bcb  dla_per216_mode_s_ts_16_nb_60000_seed_900039_.dat
5e1d5a07b2045b47f512cec33e6c330959084423db3dec3d12abb5ed57fa8842  dla_per216_mode_s_ts_16_nb_60000_seed_900040_.dat
da0fda6ab91e3a7aff0f8dea49a02a3e6f0c143782327c9ed4f167f319dbcd71  dla_per216_mode_s_ts_2_nb_60000_seed_900001_.dat
3cbee5d0a068f444591a67e2b9fc99d23d7250a0be9faee9c6050627bc67ce6e  dla_per216_mode_s_ts_2_nb_60000_seed_900002_.dat
70b40dabf360aaf5d0d452ebe58385de48e63ed8891a75d820638d1b10b1932a  dla_per216_mode_s_ts_2_nb_60000_seed_900003_.dat
63efccb6d864fb861e64f8fe994f88e35e9f02913d2b555aee569bb17e6bbba3  dla_per216_mode_s_ts_2_nb_60000_seed_900004_.dat
24d345abcf9559832bd348cb0a9da575b1c8a6568372be3c884e831cee05b4d1  dla_per216_mode_s_ts_2_nb_60000_seed_900005_.dat
8904621f0eb07253b20a29db08ad83b7e50ff9a4732e4acc7c0061c33221090f  dla_per216_mode_s_ts_2_nb_60000_seed_900006_.dat
f3b286005c73066ce9474e78176e6d49d4a7718103b59f5e0393fe6a65b7f56c  dla_per216_mode_s_ts_2_nb_60000_seed_900007_.dat
5234582cb71ffba9876f0b3c970adc4829654489553c1ff5a75a4b4a9e696a1b  dla_per216_mode_s_ts_2_nb_60000_seed_900008_.dat
59b22cf0be1ea80822f1c9e4572d33089ef7ff219dbcd73e005061646fabad14  dla_per216_mode_s_ts_2_nb_60000_seed_900009_.dat
0897a5a730dca5daca458d78596068d474aec472a339bfaba76e7edfa55d22ea  dla_per216_mode_s_ts_2_nb_60000_seed_900010_.dat
465dbb26553a5e563a73307280f09675951ff37780d4fd370a4ccb36158a5b34  dla_per216_mode_s_ts_2_nb_60000_seed_900011_.dat
eafcbb54a57f8ce608af22ef8ede88838366b82518967de970dfed3ee3b86448  dla_per216_mode_s_ts_2_nb_60000_seed_900012_.dat
15cb7dcad81953d88aa58d88a1660b7c44bd5704fc6418e5b5ef0cdfea72eeca  dla_per216_mode_s_ts_2_nb_60000_seed_900013_.dat
8f03be0d1a8e7b2f29751249e182e3fec3f5ed8b2fe7fb3283c1484ff52efd6a  dla_per216_mode_s_ts_2_nb_60000_seed_900014_.dat
3574ea280f50a20f005a355e7dc8acdb5d0ddeee7dfdf1868dae7da9bcc6daaf  dla_per216_mode_s_ts_2_nb_60000_seed_900015_.dat
b3c6b7040e909af28568452695d4804a238826047348bd80ca2ed03d0ea4ab0a  dla_per216_mode_s_ts_32_nb_60000_seed_900001_.dat
044f4c7b0d625dfda68ee97405db4274ce4deadac21634ad03541d62f95604e3  dla_per216_mode_s_ts_32_nb_60000_seed_900002_.dat
aa5ba0ad6934b2e12a0b535a70b68490873a027cbdae788835f69b4bd86c9ac1  dla_per216_mode_s_ts_32_nb_60000_seed_900003_.dat
440ba91041cff65b5bd5c94e821f19dd7a65ec1329a8fd4332b8822c7d22f08f  dla_per216_mode_s_ts_32_nb_60000_seed_900004_.dat
cfc844441dcb1b3382fc83b9a3bcbf9f14ef6b8af79f63140192c7e284a8c5e7  dla_per216_mode_s_ts_32_nb_60000_seed_900005_.dat
cbca3e7e043e288a423649d8cc73d9c60dfd20c7f323e506bfeb492d3f44deee  dla_per216_mode_s_ts_4096_nb_60000_seed_900001_.dat
9f75e4d09d9c8fe61d01e73b8984f6c5d5487fd768c827cc87b5027e9efe9160  dla_per216_mode_s_ts_4096_nb_60000_seed_900002_.dat
3e8b982c6b3b2928256d76a03ba0c2608e6e525919d052ed4a23c45b81a3f56e  dla_per216_mode_s_ts_4096_nb_60000_seed_900003_.dat
6ca8dc28296e68c29002ea5b7dfc4470bf7b9c0c48c645ea82d52e72c20febe7  dla_per216_mode_s_ts_4096_nb_60000_seed_900004_.dat
fb93c4c56ae3b3a6497e4b5b9baa7a2fcfa8a01dab5cce3ab034d9091a6d8659  dla_per216_mode_s_ts_4096_nb_60000_seed_900005_.dat
940de981445191936a3308e712749840c6a0f8fec190461b5b0053fd4fa180f6  dla_per216_mode_s_ts_4096_nb_60000_seed_900006_.dat
a11f32f94aaf9a30a7478a2ad30be581fa0117aa078ba41750fcea63d8353b28  dla_per216_mode_s_ts_4096_nb_60000_seed_900007_.dat
26c02f666a40fc53af355cf5323345e665a9efd5f4556b975b097a1b9b6ed3ba  dla_per216_mode_s_ts_4096_nb_60000_seed_900008_.dat
074193c6559cb0e5a2ee06d81860a01efac5e57d535f0b931ed36a867a6d3c1c  dla_per216_mode_s_ts_4096_nb_60000_seed_900009_.dat
0bd83c86cb83c947026fc3eb9e62f98ac867710174f11be6a95e87398b359136  dla_per216_mode_s_ts_4096_nb_60000_seed_900010_.dat
7e75caa5bb1e7e409f5f4d92088c7e780266ea6c55181f7675a1d15a42ffe56e  dla_per216_mode_s_ts_4096_nb_60000_seed_900011_.dat
2565349949a14055268ac0f0690f24d2100289b3c2649b3d6be778a1e5eac3f2  dla_per216_mode_s_ts_4096_nb_60000_seed_900012_.dat
0599ddcb8017cb8bb543a5665461812778aee46a31535fa07b2e22c12542919b  dla_per216_mode_s_ts_4096_nb_60000_seed_900013_.dat
01c786b6ba6cb933a072f8bef1d3682e193e0d529d32fe55470a9eae042c8132  dla_per216_mode_s_ts_4096_nb_60000_seed_900014_.dat
8a626bb348a174b0beec927b74f6a9cb6e0fb97bcf5a32bca98cd0356a41ea23  dla_per216_mode_s_ts_4096_nb_60000_seed_900015_.dat
d4eed1a98ef816aa7f68cd974cf6b9ad17b1ba3028cc4e12a26d5141290e1644  dla_per216_mode_s_ts_512_nb_60000_seed_900001_.dat
99782a89ce1df79d47da3bcd8e5b437c1e4db990ab8c1d0094527f4fc45eeb71  dla_per216_mode_s_ts_512_nb_60000_seed_900002_.dat
4ea0d30be2d67647d7e365306f4bf4c4697079191c2c73022df120c66afbc7f7  dla_per216_mode_s_ts_512_nb_60000_seed_900003_.dat
8417f2f8a47835036496ddcf43c270792c188a0ee37e0dbd001737ae17e6a2cd  dla_per216_mode_s_ts_512_nb_60000_seed_900004_.dat
e515f6d313e607ed1d3265e789a724ca9196ce7aa8f2809177c3be01ecbb9da9  dla_per216_mode_s_ts_512_nb_60000_seed_900005_.dat
c9838a6bf24c41ebaf81f4960a8f19a9e558d8d26d3f11fa6d9243a99c07ba9e  dla_per216_mode_s_ts_64_nb_60000_seed_900001_.dat
2876e26fd47182f29989ce1782668903782910a05f7fb6fabf2afb537736254e  dla_per216_mode_s_ts_64_nb_60000_seed_900002_.dat
97ccac9f57db771a4fbe6b734f0b5022bb439dd610ce510c41289578bd851bd5  dla_per216_mode_s_ts_64_nb_60000_seed_900003_.dat
673fadb3e9105c9f73cfdaad7aaee063c21f9201a53e9ca907d6f514893f34ad  dla_per216_mode_s_ts_64_nb_60000_seed_900004_.dat
9fed4f09863327e7d674fd08d6c93afc8542ec581c024e41d4aa3b03f8129623  dla_per216_mode_s_ts_64_nb_60000_seed_900005_.dat
e62902811c7402a5c44e5b9a5391b2fe4538dc8254541e19be6f1455a5969a11  dla_per216_mode_s_ts_8192_nb_60000_seed_900001_.dat
3471a2aa1741cce87b056b061024fb10a9eb8173c75fae033b8315ceade131bc  dla_per216_mode_s_ts_8192_nb_60000_seed_900002_.dat
f4cfad06bcf0c6e05f4fdf7f8bec3422bfc325084d73a721f713a7509f669348  dla_per216_mode_s_ts_8192_nb_60000_seed_900003_.dat
19a5cd400208c122668ba3906f978d1343b14371383ab18f867aaa595fac982d  dla_per216_mode_s_ts_8192_nb_60000_seed_900004_.dat
3d2bf7ae6077c7a72fbff7c696434364b7bc54eebddea7e4d4736ce742c0b26d  dla_per216_mode_s_ts_8192_nb_60000_seed_900005_.dat
fa07bf84becadcc704c8fb310b07df97c6f5cb4e8408edc2987a54a0f15b60f1  dla_per216_mode_s_ts_8192_nb_60000_seed_900006_.dat
56056af603b26c136db96f6d6b670ac95da96df97987240af403795fed2553dd  dla_per216_mode_s_ts_8192_nb_60000_seed_900007_.dat
b43d0616c4f02b12136fad74a3b6d3cc25d84bd6a193196780dde60e56ad0c9f  dla_per216_mode_s_ts_8192_nb_60000_seed_900008_.dat
431ecef4c32bdba3e0d9251e8942b709b5a3a9292aa6a9b0c7d75d2e461979c2  dla_per216_mode_s_ts_8192_nb_60000_seed_900009_.dat
f03b4cdcd823e31a2fd9990bf05304385c4a19deb1d564d7b5683eb94656bbc6  dla_per216_mode_s_ts_8192_nb_60000_seed_900010_.dat
fba26f2ac9483d2df80cfaadf36c6b39a04923a613ca9b2dcd4e7dbd9471da23  dla_per216_mode_s_ts_8192_nb_60000_seed_900011_.dat
76bf912e47d47d79c7c4aaef2f7e5ae3bd2b059c0508484603f0f30524ddb894  dla_per216_mode_s_ts_8192_nb_60000_seed_900012_.dat
2d199be08784e37742d22bbd9bbc9da7ea82e0e6447f6f3451f3d00f0aabe726  dla_per216_mode_s_ts_8192_nb_60000_seed_900013_.dat
ab180650e2c70a3d7f9851b7c778e296578911ed86bff4a8b9dbe11f1ef06d09  dla_per216_mode_s_ts_8192_nb_60000_seed_900014_.dat
fb0b9498233b7e32c4b930c9dab3f1594e24eef795df3934fd99f9f5fb495d51  dla_per216_mode_s_ts_8192_nb_60000_seed_900015_.dat
0c2b5a8d93f14f06e66e61aa6eac3fed051201e21f38fc932addd0a27d156963  dla_per216_mode_s_ts_8_nb_60000_seed_900001_.dat
abd60011c38e63730d813e5eb359b00c02913ac5065a2aecbbf4ae86b860fd2d  dla_per216_mode_s_ts_8_nb_60000_seed_900002_.dat
857a47da5c05586a505ad370f6aec5227d9a2017ba911deab4285647fdf12acc  dla_per216_mode_s_ts_8_nb_60000_seed_900003_.dat
a9c70075713f3667cc6c3e24b5130713a339b9df0e1f461288c56d55f8f3cfdb  dla_per216_mode_s_ts_8_nb_60000_seed_900004_.dat
da6dee9c6770f2389fdcf7ae55412e87e607ad24bde3a2968a2b18ffe379a775  dla_per216_mode_s_ts_8_nb_60000_seed_900005_.dat
6cc181f921fcd7e5ef3619ed2952a3444179296b38b5bc7b1e2b2c4c1c547923  dla_per216_mode_s_ts_8_nb_60000_seed_900006_.dat
d4eaf64692b4b1bb3b9a2d5e2978c88ebfcf1385c29b7deb9bc598fcfbe16336  dla_per216_mode_s_ts_8_nb_60000_seed_900007_.dat
cd54207be2f424a1832c691d0f569fac9d5ed479b052b218081656476b60e536  dla_per216_mode_s_ts_8_nb_60000_seed_900008_.dat
a4a79f257c345a111daa3dbe36c71df241e67006e293ed67be46ae3727059537  dla_per216_mode_s_ts_8_nb_60000_seed_900009_.dat
1bd8b83403de971e70dc1b03633f954194731598f1fd01a8a195a9d12c5ee8d5  dla_per216_mode_s_ts_8_nb_60000_seed_900010_.dat
e0dcc2fb81bbd5bc16ab28ea3a9919e61d116102bf050c40ae85222f4e9736b7  dla_per216_mode_s_ts_8_nb_60000_seed_900011_.dat
a938534432664cb0edc80ec62803b29e0f10f7b10605740f5a065cecea33e2f4  dla_per216_mode_s_ts_8_nb_60000_seed_900012_.dat
60eeb022aef77ac05fdbc5ec4a8ec0eab8c9040e5c98a8d8ef80b6907fe7e80b  dla_per216_mode_s_ts_8_nb_60000_seed_900013_.dat
900e6b957c597115553b321d618a34282da0ef56c283197e11eff5b8b495a952  dla_per216_mode_s_ts_8_nb_60000_seed_900014_.dat
2990fb1acc984a3c83fe857f79aca2fdf728357bf94e5c4c2cb8701e067af4aa  dla_per216_mode_s_ts_8_nb_60000_seed_900015_.dat
```

### Figuras só com a dimensão de correlação (`figures/corr_*.png`)

Geradas por `plot_n18_figures.py` (`figuras_correlacao`), lendo só os CSVs:
`corr_curves.png` ($C(r)$ por $T_s$, com o disco uniforme e a faixa $4 \le r \le 22$
da janela), `corr_local_slope.png` ($d\log C/d\log r$ por meia década, barra sobre
12 × $n$ seções, disco tracejado) e `corr_df_vs_ts.png` ($D_2$ bruta, disco e corrigida
contra $T_s$).

## 4. Candidatas a proxy geométrico de $F_{rup}$, semente a semente (2026-09-10, noite)

Pergunta de Michael: dá para justificar $D_f$ como proxy das propriedades
mecânicas? Teste que remove o confundidor $T_s$: nos 20 cilindros fraturados
(4 $T_s$ × 5 sementes, recortes 17×17 e 41×41), cada candidata calculada no
próprio tronco (cache `.db` do motor) contra $F_{rup}/R$ da mesma semente.
Script `Code/Data_analysis/test_trunk_predictors_of_frup.py`; tabelas
`trunk_predictors_by_seed.csv` e `trunk_predictors_correlations.csv`.

Candidatas: $D_f$ da semente (correlação e giração), $\bar R$; ocupação das
camadas $n(y)$ (média, mínimo, mínimo/média, CV, $\langle 1/n \rangle$);
coordenação $K_i$ do bastão (média, mediana, harmônica, fração $\le 5$, fração
0); e um proxy do próprio modelo, $F^* = [\langle (s_i/K_i)^m \rangle]^{-1/m}$
com $s_i = \langle 1/n \rangle$ nas camadas do bastão e $m = 2$.

**Resultado: nenhuma candidata prevê $F_{rup}/R$ dentro de $T_s$ nos dois
recortes.** Pearson dos z-scores agrupados (20 pares por recorte):

| candidata | 17×17 | 41×41 |
|:--|--:|--:|
| coordenação média | +0,51 ($p = 0{,}02$) | +0,09 |
| $F^*$ por bastão | +0,41 ($p = 0{,}07$) | +0,03 |
| $n_{\min}$ das camadas | +0,15 | +0,41 ($p = 0{,}07$) |
| $D_f$ correlação | +0,26 | +0,13 |
| $D_f$ giração | +0,04 | +0,01 |

Com 16 candidatas × 2 recortes, um $p = 0{,}02$ isolado é o que se espera ao
acaso, e o sinal não se repete no outro recorte. **Através de $T_s$** todas dão
Spearman $\pm 0{,}8$–$1{,}0$, inclusive $\bar R$: é o eixo comum, não previsão.

Dois fatos laterais medidos de passagem: (i) o $F^*$ do modelo superestima
$F_{rup}/R$ por um fator quase constante, 2,8 em $T_s = 2$ e 2,2–2,4 nos
demais, ou seja, a média de $p_i$ capta 85% da variação em $T_s$ mas não a
dispersão entre sementes; (ii) no tronco DLA ($T_s = 2$) só 81% (17×17) e 63%
(41×41) dos bastões chegam a romper — os demais não portam carga —, contra
99% em $T_s \ge 32$ (`R_measured_over_R_db`).

## 5. Geometria do tronco: inicial por $T_s$ e durante a fratura (2026-09-10, noite)

Definições, na notação do artigo: $N$ = número de segmentos de molécula na
camada $y$ (o $N(i)$ de $\sigma(i) = F/N(i)$, partilha de carga); $K$ = número de
partículas vizinhas do bastão (a coordenação $K$ de $\sigma^{th} = K\sigma_c X$).
**Até 2026-10-01 as duas letras estavam trocadas** neste README, nos CSVs
(colunas `K_*` ↔ `N_*`), nos `.dat` e nas figuras; o conteúdo não mudou, só
os nomes (registro `../decision_log/2026-10-01_N18_notacao_K_N_trocada.md`).

**Inicial, recorte 41×41** (`measure_trunk_geometry_by_ts.py` →
`trunk_geometry_by_{seed,ts}.csv`, `figures/trunk_geometry_vs_ts.png`), 5
sementes por $T_s$, bastões que portam carga: $\langle N\rangle$ vai de 178
($T_s = 2$) a 1150 ($\ge 512$); $\langle K\rangle$ de 25,8 a 52,1. As duas
saturam em 512, como $D_f$. O filtro de caminho de carga descarta 37% dos
bastões do recorte em $T_s = 2$, 16% em 8, 7% em 16, 1% em 32 e < 0,5% de 64 em
diante: na estrutura aberta, uma boa parte do que está dentro do recorte não
liga as duas extremidades.

**Durante a fratura, recorte 17×17, $m = 2$, $T_s \in \{2, 8, 16, 32, 64, 128\}$**
(`trace_geometry_during_fracture.py` → `geometry_during_fracture_{curves,by_realization}.csv`,
`figures/geometry_during_fracture.png`; 10 realizações × 5 sementes, semente
de fratura 101, mesmo protocolo de `fiber_bundle_ava.py`, instrumentado para
gravar as médias após cada cascata). Normalizado pelo valor inicial:

| $T_s$ | $N_0$ | $K_0$ | $N/N_0$ no último estado preterminal | $K/K_0$ idem |
|--:|--:|--:|--:|--:|
| 2 | 55 | 27,2 | 0,83 | 1,05 |
| 64 | 182 | 46,1 | 0,92 | 1,01 |
| 128 | 194 | 47,7 | 0,93 | 1,01 |

$\langle N\rangle$ só cai: são as moléculas que saem. $\langle K\rangle$ dos
sobreviventes **sobe** durante o carregamento, 5% em $T_s = 2$ e 1% nas
compactas: os bastões que rompem primeiro são os de poucos vizinhos, e a
população que resta fica mais coordenada que a inicial. Em $T_s = 2$ a queda
de $N$ é quase linear em $F/F_{rup}$; nas compactas, quase nada acontece até
$F/F_{rup} \approx 0{,}5$ e a perda se concentra no fim. Em $F$ absoluto,
$T_s = 2$ termina em $F \approx 230$ enquanto 64 e 128 mal começaram.

Em 2026-10-01 o CSV ganhou $T_s = 1024$ e $8192$ (pedido de coautor, para a
saturação), e as linhas dos seis $T_s$ originais saíram idênticas. Em 1024 e
8192, $N/N_0$ no fim fica em 0,93 e 0,92, igual a 128, e $K/K_0$ tem máximo de
1,012. Os `.dat` de duas colunas dos oito $T_s$ estão em
`xmgrace/geometry_during_fracture_two_column/`.
`figures/geometry_during_fracture.png` agora traz os oito $T_s$; os `.agr` e as
figuras en-US continuam com seis.

Versões en-US, em três arquivos separados (`plot_trunk_geometry_figures_en.py`,
lê só os CSVs): `figures/trunk_geometry_vs_ts_en.png`,
`figures/geometry_during_fracture_F_en.png` (F absoluto) e
`figures/geometry_during_fracture_Frup_en.png` (F/F_rup).

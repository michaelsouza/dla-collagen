# N18: $D_f$ nos dez $T_s$ com cilindros periódicos, $m$ como fator, e $F_{rup}$ contra a largura

**Data:** 2026-09-10
**Afeta:** N7 e N12 (corrobora e delimita; ambos seguem fechados no manuscrito), N17 (delimita a invariância em tamanho ao regime compacto), I9
**Dados:** `Reviews/N18_df_ten_ts/` (README, CSVs, `width_fracture_raw/`, `xmgrace/`, `figures/`); relatório em `Reviews/N18_df_ten_ts/relatorio_N18.qmd`
**Onde rodou:** nesta máquina (32 núcleos), cluster instável; 50 cilindros em 40 min, 400 fraturas 41×41 em 1 h 10

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## As três perguntas de Michael

1. $D_f$ por massa–raio e por raio de giração nos dez $T_s$, na fibrila engrossada com fronteira periódica, e qual intervalo de $r$ usar.
2. $D_f$ converge em $T_s$ junto com as propriedades mecânicas? Dá para tirar $m$ como variável?
3. A distribuição de avalanches não depende da largura; e $F_{rup}$?

## Decisões de método, tomadas antes de olhar os números

- **Seção transversal = a do artigo** (`paper_PRE.tex:141`; `measure_df_periodic.py`): na camada $L$ entram as moléculas cujo bastão cruza $y = L$, um ponto $(x,z)$ por molécula, $L = 0, 18, \dots, 198$ (12 seções por anel de 216). Michael confirmou em 2026-09-10 depois de eu ter proposto uma partição por base da molécula; a partição por base foi descartada porque não é a regra validada, e as duas são estatisticamente equivalentes.
- **Regra principal de $D_f$: raio de giração na ordem de crescimento**, ajuste de $\log N$ contra $\log R_g$ em $40 \le N \le N_{\max}/2$. Motivo: 1,8 década sem depender de $R_{\max}$, contra 1,2 do massa–raio. As demais janelas (40–320, 320–5000, relativa $0{,}15R$–$0{,}5R$, fixa 4–8, faixa cheia) entram como colunas de sensibilidade, e as inclinações locais por oitava também.
- **Conferência dura**: os 15 cilindros de 2026-09-01 ($T_s = 2, 128, 8192$) tinham de reproduzir os 75 valores registrados a $10^{-3}$; o script não escreve se não. Reproduziram. A primeira realização da fratura 128/900001 em 17×17 com semente 1 tinha de ser byte a byte igual à escada de 02/09. Foi.
- Para a largura: fraturar aqui, 17×17 e 41×41, $T_s \in \{2, 32, 128, 8192\}$, $m = 2$, 5 sementes × 10 realizações, semente de fratura 101 (a escada usou 1, e as realizações não podem se repetir ao juntar). Sem 81×81: custo de dias.

## O que se mediu

**1. $D_f$.** Duas famílias, não uma curva: giração 40–2500 dá 1,66–1,74 de $T_s = 2$ a 128 e 1,93–1,96 de 512 a 8192, com barra 0,01–0,02. A janela do miolo (40–320) sobe a partir de $T_s = 32$ e a da periferia (320–5000) só a partir de 512: **o miolo compacta primeiro**. As inclinações locais dão o $N_c(T_s)$ em que a seção deixa de ser compacta: $< 40$ até $T_s = 16$; 320 em 32 e 64; 320–640 em 128; 1280 em 512 e 1024; $\ge 2560$ em 4096 e 8192. O "$D_f$ intermediário" sempre foi a fração de miolo que a janela cobre. Nas fibrilas livres (300 por seção) isso acontece em $T_s \approx 64$; com 5.000 por seção, em 512. Massa–raio relativa concorda nos extremos (1,675 / 1,955) e cai a 1,59 no cotovelo ($T_s = 64$), onde cruza $N_c$. Faixa cheia $5 \le r \le R_{\max}$ inclui a saturação e fica abaixo de tudo (1,54–1,78), como Michael pediu para ver.

**2. $m$ e convergência.** $F_{rup}(T_s, m) = A(T_s)\,g(m)$ com $g = 0{,}588, 1, 1{,}221, 1{,}437, 1{,}616$: espalhamento residual $\le 1{,}02$ para $T_s \ge 32$, 1,41 em $T_s = 2$. O nulo ELS $\sigma^* = \frac{m}{m+1}(m+1)^{-1/m}$ reduz o espalhamento a 1,14–1,16 e não colapsa; o desvio ($-10\%$ em $m = 1$, $-13\%$ em $m = 10$) é o canal local $K_i$. Decomposição em dois fatores: interação 0,2% para $F_{rup}$, 0,4% para $\varphi$ preterminal, 2% para a fração terminal, **19–40% para frac1, p90, p99 e tamanho médio**. $m$ sai como fator da força e do dano no regime compacto; não sai da forma das cascatas. Saturação em $T_s$: $D_f$ e $F_{rup}/N$ em 512 (mesmo confundidor, $N \sim R^{D_f}$); $\varphi$ preterminal em 32; p99 em 16; fração unitária plana desde 2.

**3. Largura.** De 17×17 a 41×41, $R$ cresce 3,3–5,7× e $F_{rup}$ 3,2–5,8×: $F_{rup}/R$ muda de $-4\%$ a $+4\%$, dentro do erro, nos quatro $T_s$; com a escada de 02/09, $-7\%$ em 25×. **Sim, $F_{rup}/R$ não depende da largura.** Mas a cauda das cascatas só é invariante na seção compacta: em $T_s = 128$ e 8192 o p99 fica em 10–11 (a escada confirmada com 5 sementes); em $T_s = 2$ vai de 27 a 69, o máximo de 34 a 150, e a fração terminal cai de 0,82 a 0,70. **No regime DLA o corte das cascatas cresce com a largura.**

## O que decorre

- N7 e N12 seguem fechados no manuscrito, e nada daqui entra no artigo pela regra de intervenção mínima (2026-09-03). Estes resultados sustentam a frase de limitação de $D_f$ e a resposta a R1-4 com mais força do que antes: o crossover DLA → compacto agora tem $N_c(T_s)$ medido em cinco sementes.
- **Delimitação de N17.** A invariância em tamanho da distribuição de cascatas, escrita na carta (R1-2, escada de 02/09), foi medida em $T_s = 128$ e vale em 128 e 8192. Não vale em $T_s = 2$. A carta fala da escada em $T_s = 128$ e não generaliza; o manuscrito afirma o corte na grade 17×17. Nenhum dos dois precisa mudar, mas quem for estender a afirmação para a estrutura aberta vai encontrar efeito de tamanho finito. Fica registrado aqui para não ser redescoberto.
- $m$ pode ser removido como variável da força e do dano por $g(m)$, com o ELS como referência. Se um dia entrar no artigo, é como uma frase e uma coluna, não como figura.

## Rastreabilidade

| número | origem |
|:--|:--|
| $D_f$ por $T_s$ e janela, inclinações locais | `N18_df_ten_ts/df_periodic_{summary,by_seed,local_slopes}.csv` |
| conferência dos 15 cilindros | `N18_df_ten_ts/identity_check_15_cylinders.csv` |
| $g(m)$, ELS, resíduos, interação | `N18_df_ten_ts/frup_m_separability.csv`, `statistics_two_way_decomposition.csv` |
| saturação em $T_s$ | `N18_df_ten_ts/df_vs_mechanics_by_ts.csv` |
| $F_{rup}$, $R$, p99 por recorte | `N18_df_ten_ts/width_fracture_{summary,by_realization}.csv`, brutos em `width_fracture_raw/` |
| receita e sha256 dos 50 cilindros | `N18_df_ten_ts/README.md`; cópia em `Data_fibrils/periodic_cylinders_216_nb60000_10Ts_5seeds.tar.gz` (fora do git) |
| scripts | `Code/Data_analysis/{run_periodic_cylinder_grid.sh, measure_df_periodic_ten_ts.py, analyze_frup_m_scaling.py, compare_df_with_mechanical_scales.py, run_local_width_fracture.sh, summarize_width_fracture.py, plot_n18_figures.py}` |

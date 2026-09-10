# N18, segunda rodada: peso do ajuste de $D_f$ corrigido e dimensão de correlação

**Data:** 2026-09-10 (tarde)
**Afeta:** N18 (corrige os valores de $D_f$ no cotovelo; não muda os dois patamares); N7 e N12 seguem fechados
**Dados:** `Reviews/N18_df_ten_ts/` (mesmos 50 cilindros; CSVs reescritos; `curves_corr_by_ts.csv` e `figures/local_slope_curves.png` novos)
**Cita:** `Reviews/decision_log/2026-09-10_N18_df_dez_ts_e_escalas_mecanicas.md`

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## O que Michael pediu

Crítica ao método de conversão dos dados em $D_f$, e depois: (1) corrigir o peso
do ajuste, (2) aplicar a dimensão de correlação, (3) gerar a curva de inclinação
local.

## O erro encontrado e medido antes de corrigir

A reta de $\log R_g$ contra $\log N$ era ajustada com um ponto por $N$ inteiro
entre 40 e 2500: 2.200 pontos acima de 300 e 260 abaixo. O mínimo quadrado dava
o peso todo à década de cima, e o "$D_f$ principal" media a periferia. Refeito
com 30 pontos por oitava, igualmente espaçados em $\log N$, sobre as curvas
médias já gravadas:

| $T_s$ | 2 | 32 | 64 | 128 | 512 | 8192 |
|:--|--:|--:|--:|--:|--:|--:|
| todos os $N$ (entrada anterior) | 1,701 | 1,662 | 1,704 | 1,742 | 1,931 | 1,954 |
| 30 por oitava (esta entrada) | 1,692 | 1,702 | 1,761 | 1,816 | 1,970 | 1,974 |

Diferença até 0,07 contra barra de 0,01–0,02. Os dois patamares não mudam de
leitura (1,69 e 1,97); o cotovelo muda de posição: a subida começa em $T_s = 64$,
não em 128. A entrada anterior dizia "1,66–1,74 até 128"; o correto é 1,68–1,70
até 32 e 1,76–1,82 em 64–128, e esses dois **não são dimensões**, são médias de
uma curva com cotovelo. A regra principal passa a ser giração com peso uniforme em
$\log N$; as colunas `*_allpts` guardam o valor antigo e servem só à conferência
contra `df_gyration_wide_cylinders.csv` (2026-09-09), que continua a reproduzir a
$10^{-3}$.

## Dimensão de correlação

$C(r)$ = fração dos pares da seção final a distância $\le r$; $D_2$ = inclinação
de $\log C$ contra $\log r$ em $4 \le r \le \bar R/3$, ~1 década. Sem centro e sem
ordem de adesão. Controle de borda: disco uniforme com o mesmo $n$ e $\bar R$ por
seção dá 1,93–1,95, não 2; `corr_*_corrected` = medido − disco + 2. Resultado:
1,73–1,75 na estrutura aberta, 1,92 na compacta, sempre entre miolo e periferia
da giração. Motivo, medido: a periferia é DLA até $T_s = 8192$ (giração 320–5000
dá 1,92 lá) e $D_2$ pesa todos os pares. A correlação é a média miolo+periferia;
a giração na ordem de adesão separa os dois. Barra entre sementes de 0,001–0,007.

## Inclinação local por seção

`df_periodic_local_slopes.csv` agora traz, além da inclinação sobre a curva média
da semente, a média e o erro-padrão sobre as 60 seções de cada $T_s$
(`slope_section_*`), para giração (oitavas em $N$), correlação e disco (meias
décadas em $r$) e massa–raio. `figures/local_slope_curves.png` desenha as duas
curvas. $N_c(T_s)$ da entrada anterior não muda (as inclinações por oitava não
dependem do peso).

## O que decorre

- Nada muda no manuscrito: ele afirma os dois limites (1,71 e 2) e a frase de
  limitação, e os dois limites ficam mais firmes, com três estimadores.
- Em relatórios internos, $D_f$ em $64 \le T_s \le 128$ deve ser reportado como
  $N_c$, não como um número.
- Para a barra de $D_f$: o erro-padrão entre sementes mede reprodutibilidade; a
  escolha de janela e de peso muda o valor mais do que a barra. Reportar sempre a
  inclinação local ao lado.

## Rastreabilidade

| número | origem |
|:--|:--|
| $D_f$ com os dois pesos, $D_2$ bruta, disco, corrigida | `N18_df_ten_ts/df_periodic_{summary,by_seed}.csv` |
| inclinações locais por seção | `N18_df_ten_ts/df_periodic_local_slopes.csv` |
| $C(r)$ médio por $T_s$ e do disco | `N18_df_ten_ts/curves_corr_by_ts.csv` |
| scripts | `Code/Data_analysis/measure_df_periodic_ten_ts.py`, `plot_n18_figures.py` |

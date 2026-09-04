# Figura 7 do manuscrito revisado — dados para o xmgrace

**Alimenta:** `Paper/figure_7.pdf`, chamado em `Paper/paper_PRE.tex` e impresso
como **Figura 7**.

**Gerado por:** `Code/Data_analysis/export_figure_7_xmgrace.py`
**Fonte:** `Reviews/N9_damage_curves/damage_summary.csv` e
`Reviews/N9_damage_curves/damage_ts<TS>_m2_curve_norm.csv`, ambos produzidos por
`extract_damage_curves.py` e `summarize_damage_curves.py` a partir do job 590854
(SDumont2, partição `cpu_amd`).

Substitui a Figura 7 do artigo submetido, que mostrava os ajustes da Eq. (5) e os
parâmetros $\alpha$ e $\beta$ contra $T_s$. A Eq. (5) saiu do manuscrito: ajustada
sobre as curvas do protocolo quenched ela dá $\beta \le 0$.

## Os arquivos

| arquivo | séries | tipo do Grace |
|:--|:--|:--|
| `figure_7a_f_rup_vs_ts_xydy.dat` | 5, uma por $m = 1, 2, 3, 5, 10$ | `xydy` |
| `figure_7b_phi_vs_u_xydy.dat` | 4, uma por $T_s = 2, 32, 128, 8192$ | `xydy` |

Comentários começam com `#`; `&` separa conjuntos. O tipo está declarado em cada
bloco, então o xmgrace lê a terceira coluna como barra de erro sem configuração
extra.

## Como montar cada painel

**(a) $F_{\mathrm{rup}}$ contra $T_s$.** Colunas: $T_s$, média, desvio padrão
sobre as $10^4$ realizações da condição. Eixo $x$ **logarítmico base 2** (a grade
é $2^1$ a $2^{13}$), eixo $y$ linear de 0 a ~1800. A leitura é que a força cresce
uma ordem de grandeza e satura: para $m=2$, de $150{,}6 \pm 35{,}9$ em $T_s = 2$
a $1532{,}4 \pm 217{,}5$ em $8192$, com $83\%$ da subida já em $T_s = 128$.

**(b) $\varphi$ contra $F/F_{\mathrm{rup}}$.** Colunas: $u$, média, desvio
padrão. Ambos os eixos lineares, $x$ de 0 a 1 e $y$ de 0 a ~0,25. As três curvas
de $T_s \ge 32$ praticamente coincidem (último ponto preterminal $0{,}126$,
$0{,}121$, $0{,}123$) e a de $T_s = 2$ fica claramente acima ($0{,}222$) — o
colapso é o resultado do painel.

**O ponto em $u = 1$ está fora de propósito.** Ali $\varphi = 1$ por construção:
é a cascata terminal, que remove de uma vez o que restou do esqueleto. Incluí-lo
desenharia um salto vertical que não é dano preterminal. O salto é o resultado
descrito no texto, não parte da curva.

## O projeto `.agr`

`figure_7.agr`, versionado aqui ao lado dos `.dat`, e `Paper/figure_7.pdf` gerado
dele. A primeira versão saiu de `Code/Data_analysis/build_xmgrace_projects.py`,
que monta o projeto a partir dos `.dat` e imprime em EPS pelo `gracebat`; daí em
diante ele é editado no próprio xmgrace, que é o ambiente dos coautores. Rodar o
script de novo **sobrescreve** o `.agr`, então ajustes feitos na interface se
perdem — depois do primeiro ajuste manual, o `.agr` passa a ser a fonte.

**Símbolos do painel (b).** As séries se distinguem pelo símbolo, não pela cor:
os azuis da rampa são próximos demais. Como a curva tem 200 pontos, o `.agr`
guarda cada série em dois conjuntos: `S0`–`S3` são as curvas completas, sem
símbolo e sem legenda; `S4`–`S7` são só símbolos, num ponto a cada 20 (índices
deslocados de 5 por série para que os símbolos de curvas sobrepostas se
intercalem), e carregam a legenda. Os pontos de `S4`–`S7` são um subconjunto
dos `.dat` acima, escolhido por `build_xmgrace_projects.py`; não há arquivo
separado para eles.

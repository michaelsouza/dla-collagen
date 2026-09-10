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

## Figura de colapso em $m$ (`frup_collapse.*`, 2026-09-10, interna)

Une a Figura 7(a) sem barra de erro a dois insets. **Não substitui nada no
manuscrito**: é a figura pedida por Michael para ver, num painel só, que $m$ sai
de $F_{\mathrm{rup}}$ como fator.

**Gerado por:** `Code/Data_analysis/build_frup_collapse_figure_xmgrace.py`, que
escreve os `.dat`, o `.agr` e o `frup_collapse.pdf` de conferência.
**Fonte:** `damage_summary.csv` (job 590854), a mesma da Figura 7(a).

| arquivo | séries | tipo | conteúdo |
|:--|:--|:--|:--|
| `frup_collapse_main_xy.dat` | 5, $m = 1, 2, 3, 5, 10$ | `xy` | $\log_{10} T_s$, $\langle F_{\mathrm{rup}}\rangle$ |
| `frup_collapse_ratio_xy.dat` | 5 | `xy` | $\log_{10} T_s$, $F_{\mathrm{rup}}/F_{\mathrm{sat}}$ |
| `frup_collapse_fsat_vs_m_xy.dat` | 2 | `xy` | os cinco $F_{\mathrm{sat}}(m)$ medidos; a curva $a(1-e^{-m/b})$ amostrada |

$F_{\mathrm{sat}}(m)$ é o valor **medido** em $T_s = 8192$, não o $a$ do ajuste
($a = 2503 \pm 31$, $b = 2{,}18 \pm 0{,}07$; o ajuste erra 2–3% em $m = 1$ e 5 e
fica só como guia no inset). Razão máx/mín de $F_{\mathrm{rup}}/F_{\mathrm{sat}}$
entre os cinco $m$: 1,40 em $T_s = 2$, 1,12 em 8, 1,03 em 16, $\le 1{,}025$ de
32 em diante — é o mesmo resultado de `../../N18_df_ten_ts/frup_m_separability.csv`,
normalizado pelo plateau em vez de por $m = 2$.

Estilo: um azul só (cor 4) com preenchimento azul-claro (cor 20), símbolos
círculo, quadrado, diamante, triângulo, triângulo à esquerda, fonte 3 nos
rótulos, como na Figura 7(a) de Michael. Página 720×600; gráfico principal G0,
inset esquerdo G1, inset direito G2.

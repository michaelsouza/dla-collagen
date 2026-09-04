# Figura 8 do manuscrito revisado — dados para o xmgrace

**Exportado em 2026-09-03** a partir de `Reviews/N10_cascade_survival/cascades_npz/`,
que traz **as cinquenta condições** da campanha copiadas do Lustre (5,9 MB;
originais de 26 de agosto, 15h53). Ficam versionadas aqui para que a figura e as
afirmações sobre a grade sejam reproduzíveis nesta máquina, sem VPN.

Na grade inteira, $6{,}1\times10^{7}$ cascatas preterminais: a fração de eventos
unitários vai de $0{,}545$ a $0{,}779$ e é maioria nas cinquenta condições; o p99
vai de 8 a 43 moléculas. São esses os números que o parágrafo da estatística do
manuscrito cita.

**Este export achou um erro no texto do manuscrito**, corrigido no mesmo dia: a
resposta a R1-2 afirmava invariância da distribuição em $m$, com números que na
verdade eram da escada de tamanho. Ver
`decision_log/2026-09-03_correcao_invariancia_em_m.md`.

**Alimenta:** `Paper/figure_8.pdf`, rótulo `fig_8`, impresso como **Figura 8**.

Os três nomes concordam desde 2026-09-03, quando o rótulo e o arquivo foram
renomeados de 9 para 8. A figura de $\Psi$ que antes ocupava o nome
`figure_8.pdf` saiu do manuscrito; ela existe nos commits `dad428e` e `ecc4ac7`.

**Gerado por:** `Code/Data_analysis/export_figure_8_xmgrace.py`
**Fonte:** `$DLA_PROJECT/campaign/analysis/cascades/casc_ts<TS>_m<M>_pre.npz` —
matriz esparsa cuja soma no eixo 0 dá a contagem de cascatas por tamanho, com o
índice igual ao tamanho. É o mesmo esquema que `plot_survival_by_ts.py` lê para a
Figura 5.2 do relatório da campanha.

Substitui a Figura 9 do artigo submetido — a que mostrava $P(s)$ em log-log com
ajuste de reta e $\gamma(T_s)$, e que agora é a Figura 8. O ajuste saiu: o teste de Clauset rejeita a lei
de potência pura em 48 das 50 condições, e acima do menor tamanho ajustável resta
menos de uma década.

## O que se mediu

| série | fração de cascatas unitárias | p99 | cascatas |
|:--|--:|--:|--:|
| $T_s=2$, $m=2$ | 0,716 | 35 | 499.967 |
| $T_s=16$, $m=2$ | 0,726 | 13 | 943.327 |
| $T_s=128$, $m=2$ | 0,724 | 12 | 1.533.784 |
| $T_s=1024$, $m=2$ | 0,716 | 12 | 1.535.921 |
| $T_s=8192$, $m=2$ | 0,712 | 13 | 1.589.010 |
| $T_s=128$, $m=1$ | 0,778 | 8 | 3.071.545 |
| $T_s=128$, $m=3$ | 0,668 | 14 | 1.129.963 |
| $T_s=128$, $m=5$ | 0,617 | 16 | 925.371 |
| $T_s=128$, $m=10$ | 0,585 | 19 | 799.181 |

O painel (a) mostra as quatro curvas de $T_s \ge 16$ praticamente sobrepostas e a
de $T_s = 2$ claramente acima. O painel (b) mostra que estreitar a desordem
desloca peso dos eventos unitários para o corte — e que o corte não desaparece.

## Como rodar de novo

No cluster, com o ambiente carregado:

```bash
python3 Code/Data_analysis/export_figure_8_xmgrace.py
```

Ou localmente, depois de copiar os dez `.npz` das condições usadas
($T_s = 2, 16, 128, 1024, 8192$ com $m=2$; e $T_s=128$ com $m = 1,2,3,5,10$):

```bash
python3 Code/Data_analysis/export_figure_8_xmgrace.py --cascades <diretorio>
```

## O que ele escreve

| arquivo | séries | tipo do Grace |
|:--|:--|:--|
| `figure_8a_survival_by_ts_xy.dat` | 5, uma por $T_s = 2, 16, 128, 1024, 8192$ ($m=2$) | `xy` |
| `figure_8b_survival_by_m_xy.dat` | 5, uma por $m = 1, 2, 3, 5, 10$ ($T_s = 128$) | `xy` |

Colunas: tamanho de cascata $s$ e $P(S > s)$. **Ambos os eixos logarítmicos.**
A cascata terminal de cada realização está excluída, e pontos com
$P(S>s) \le 3\times10^{-7}$ são descartados, porque ali a cauda é um evento
único — o mesmo piso usado na Figura 5.2 do relatório.

Sem ajuste, deliberadamente: o painel (a) mostra que as curvas de $T_s \ge 16$
quase coincidem, e o (b) que a forma muda pouco com $m$. As duas coisas são o
resultado. Nenhum expoente é reportado no manuscrito revisado.

## O projeto `.agr`

`figure_8.agr`, versionado aqui ao lado dos `.dat`, e `Paper/figure_8.pdf` gerado
dele. A primeira versão saiu de `Code/Data_analysis/build_xmgrace_projects.py`,
que monta o projeto a partir dos `.dat` e imprime em EPS pelo `gracebat`; daí em
diante ele é editado no próprio xmgrace, que é o ambiente dos coautores. Rodar o
script de novo **sobrescreve** o `.agr`, então ajustes feitos na interface se
perdem — depois do primeiro ajuste manual, o `.agr` passa a ser a fonte.

**Símbolos.** As séries se distinguem pelo símbolo, não pela cor: os azuis da
rampa são próximos demais. Como cada curva tem de 93 a 271 pontos, o `.agr`
guarda cada série em dois conjuntos por painel: `S0`–`S4` são as curvas
completas, sem símbolo e sem legenda; `S5`–`S9` são só símbolos, em cerca de
cinco valores de $s$ por década (deslocados de um quinto de passo por série,
para intercalar), e carregam a legenda. O `SYMBOL SKIP` do Grace conta índices,
o que em eixo log amontoaria os símbolos à direita — por isso a escolha é feita
no script. Os pontos de `S5`–`S9` são um subconjunto dos `.dat` acima, escolhido
por `build_xmgrace_projects.py`; não há arquivo separado para eles.

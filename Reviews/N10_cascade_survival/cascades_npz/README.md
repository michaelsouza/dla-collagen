# Cascatas preterminais da campanha quenched — cópia local

Os **cinquenta** arquivos `casc_ts<TS>_m<M>_pre.npz` da campanha, copiados em
2026-09-03 de

    /petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign/analysis/cascades

no SDumont2. Os originais são de 26 de agosto de 2026, 15h53, e somam 5,9 MB.

**Por que estão versionados.** Sem eles, qualquer afirmação sobre a grade — "a
fração de cascatas unitárias é maioria nas cinquenta condições", "o p99 vai de 8
a 43" — só é conferível com VPN e acesso ao Lustre. Foi essa distância que deixou
passar três vezes um número da escada de tamanho apresentado como número da
varredura em $m$ (`decision_log/2026-09-03_correcao_invariancia_em_m.md`). 5,9 MB
é barato pelo que compra.

**Produzidos por** `Code/Data_analysis/extract_cascades.py`, a partir de
`$DLA_PROJECT/campaign/avalanches/runs`. Cada arquivo é uma matriz esparsa CSR
com **uma linha por realização** e **uma coluna por tamanho de cascata**: o
índice da coluna *é* o tamanho. Somar no eixo 0 dá a contagem de cascatas por
tamanho, que é o que `export_figure_8_xmgrace.py` lê.

**`_pre` é preterminal.** A cascata terminal de cada realização — a que leva a
última molécula — fica em `_term.npz`, que **não** foi copiado: ela não é evento
crítico e está fora de toda a estatística do manuscrito. `_fibril.npy`, que diz a
qual fibrila cada linha pertence e serve ao bootstrap de blocos, também ficou lá.

## Cascatas preterminais por condição

| $T_s$ | $m=1$ | $m=2$ | $m=3$ | $m=5$ | $m=10$ |
|--:|--:|--:|--:|--:|--:|
| 2 | 612.263 | 499.967 | 459.719 | 432.683 | 399.303 |
| 8 | 1.152.155 | 743.352 | 621.229 | 548.200 | 491.297 |
| 16 | 1.659.406 | 943.327 | 747.517 | 640.364 | 565.479 |
| 32 | 2.276.579 | 1.204.642 | 922.887 | 776.333 | 680.250 |
| 64 | 2.785.342 | 1.408.344 | 1.052.041 | 870.109 | 754.190 |
| 128 | 3.071.545 | 1.533.784 | 1.129.963 | 925.371 | 799.181 |
| 512 | 3.202.072 | 1.565.768 | 1.130.065 | 909.987 | 780.166 |
| 1024 | 3.179.314 | 1.535.921 | 1.102.881 | 884.310 | 758.958 |
| 4096 | 3.238.109 | 1.559.388 | 1.115.769 | 888.769 | 762.434 |
| 8192 | 3.278.834 | 1.589.010 | 1.135.825 | 903.597 | 772.718 |

Total: **61.000.717** cascatas, que é o $6{,}1\times10^{7}$ citado no manuscrito.

`sha256` do conjunto, concatenado na ordem alfabética dos nomes:
`983823b047e27885f32f6aa2c6711397`

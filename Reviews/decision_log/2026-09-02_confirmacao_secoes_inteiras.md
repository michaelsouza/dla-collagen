# Confirmação: as seções inteiras não movem o corte das avalanches

**Data:** 2026-09-02 (tarde)
**Complementa:** `2026-09-02_corte_das_avalanches_e_dinamico.md`, que deixou
as seções inteiras como pendentes de confirmação

> Entrada de registro. **Append-only** — não editar.

As duas fraturas de seção inteira terminaram — 1h54 cada, exatamente o custo
$N^{2}$ previsto — e confirmam a conclusão da entrada anterior, agora sobre
**1,4 década em $N$ e duas arquiteturas**:

| condição | janela | moléculas | fração tam. 1 | p90 | p99 | terminal / $N$ |
|:--|:--|---:|---:|---:|---:|---:|
| $T_s=128$ | 17×17 | 2.372 | 0,75 | 2 | 10 | 0,88 |
| | 41×41 | 12.023 | 0,75 | 3 | 11 | 0,87 |
| | 81×81 | 37.536 | 0,76 | 3 | 11 | 0,88 |
| | **181×181** | **59.763** | **0,74** | **3** | **9** | **0,88** |
| $T_s=8192$ | 17×17 | 2.453 | 0,73 | 3 | 14 | 0,88 |
| | **141×141** | **59.794** | **0,76** | **3** | **12** | **0,88** |

Vinte e cinco vezes mais moléculas, em uma condição de *crossover* (128) e em
uma compacta (8192), e a forma da distribuição não muda. O único número que
varia é o máximo isolado de uma realização (174 na seção inteira de 128), e a
realização que o produziu tem o **menor** p99 de toda a escada (9): é a cauda
extrema sendo amostrada uma vez, não o corpo da distribuição se deslocando.

Nada a acrescentar à leitura da entrada anterior; ela vale agora com a
confirmação que pedia. N17 fecha. Dados em
`PhaseC_periodic_cylinder/avalanche_ladder_ts128.csv` e
`avalanche_ladder_ts8192.csv`.

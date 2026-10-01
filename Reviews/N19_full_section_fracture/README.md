# N19 — Ruptura da seção inteira (sem recorte em x, z), com o motor em arrays

**Pergunta de Michael (2026-09-10, noite):** simular a ruptura sem limitar x e z.
**Decisões:** acelerar o motor antes; $T_s \in \{2, 32, 128, 8192\}$; $|y| \le 100$
(201 camadas, o comprimento publicado); 5 sementes × 10 realizações; $m = 2$;
semente de fratura 101 (a mesma do N18); nesta máquina.

## 1. O motor em arrays (`Code/Fracture_fibril/load_path_arrays.py`)

O motor legado (`stress_strain_ava.py`) varre todas as partículas em objetos
Python a cada passo de cascata e reconstrói o dicionário de bastões: O($R$) por
passo, com o número de passos $\propto R$, e 1 a 2 GB de RAM. Na seção inteira
(~58 mil bastões, ~1 M partículas) isso dava **1 h 54 por realização** (escada
de 02/09). O módulo novo guarda o tronco em CSR e faz a mesma varredura em
`numba`; `fiber_bundle_ava.py -engine arrays` (padrão desde 2026-09-11) usa-o em
`fail_at`; o protocolo, o sorteio de $X_i$, a matriz de contatos e o resto do
`FibrilSystem` não mudam. `stress_strain_ava.py` (campanha do cluster) não muda.

**Semântica preservada, incluindo a ordem de iteração dos `set`s do legado**
(emulada com `list(set(...).copy())`, ver cabeçalho do módulo): a ordem dentro
do bastão muda os últimos bits de $\langle 1/n\rangle$ e por isso de $F^*$; a
ordem dentro da camada muda o caminho de carga no empate documentado. Sem a
emulação de camada, 38 dos 40 troncos do N18 davam um caminho de carga inicial
diferente (2% dos bastões em $T_s = 2$); com ela, tudo bate.

**Equivalência medida** (`engine_equivalence.csv`, `compare_fracture_engines.py`):

| referência | realizações | resultado |
|:--|--:|:--|
| escada 02/09, $T_s = 128$, 17×17, semente 1 | 5 | byte a byte igual (`test_load_path_arrays.py`) |
| escada 02/09, $T_s = 128$, **181×181**, semente 1 | 1 | byte a byte igual; 115 s contra 1 h 54 |
| N18, 17×17 e 41×41, 4 $T_s$ × 5 sementes, semente 101 | 400 | **40/40 arquivos idênticos** |

Tempos por realização (segundos; legado dos logs do N18):

| recorte | $T_s = 2$ | 32 | 128 | 8192 |
|:--|--:|--:|--:|--:|
| 17×17, legado → arrays | 0,5–1,0 → 0,04 | 5–8 → 0,15 | 9–10 → 0,27 | 9–10 → 0,2–0,35 |
| 41×41, legado → arrays | 6–11 → 0,2 | 84–119 → 1,1–1,5 | 235–289 → 2,2–2,9 | 327–362 → 3,6–4,4 |
| seção inteira, arrays | 44 | — | 115 (181×181) | — |

Testes: `pytest Code/Fracture_fibril/` (16, incluindo os 6 novos de
`test_load_path_arrays.py`; o byte a byte da escada roda com `DLA_EXTENDED`
apontando para os troncos estendidos).

## 2. Campanha da seção inteira (`raw/wfull/`, `width_fracture_*.csv`, `figures/`)

**Receita.** Os 20 troncos estendidos de $T_s \in \{2, 32, 128, 8192\}$, sementes
900001–900005 (cilindros do N18, abertos em $y = \pm 108$ e estendidos), sem
recorte em $x, z$ (`-half-width 200`; o raio máximo da seção é 165), $|y| \le 100$
(201 camadas), $m = 2$, semente de fratura 101, 10 realizações por tronco, motor
em arrays. `Code/Data_analysis/run_local_width_fracture.sh` com `FULL=1 RUN_D=0
JOBSFULL=12`, 2026-09-10 23:27 → 2026-09-11 00:39 (**1 h 12 de parede**; 82 a
328 s por realização com 12 processos concorrentes; 1,4 GB de pico por
processo ao ler o `.db`). Brutos em `raw/wfull/ts_<T>/*.txt.gz` (11 MB; os
sha256 dos textos descomprimidos em `raw/wfull/checksums_uncompressed.sha256`).
Resumo por `summarize_width_fracture.py --out Reviews/N19_full_section_fracture`
com os recortes 17×17 e 41×41 do N18 e a escada de 02/09; figuras por
`plot_n19_figures.py`.

**Bastões que portam carga na seção inteira** (dos ~58,4 mil dentro de $|y| \le 100$):

| $T_s$ | 2 | 32 | 128 | 8192 |
|:--|--:|--:|--:|--:|
| $R$ (médio) | 33 501 | 56 657 | 58 162 | 58 301 |
| fração descartada pelo caminho de carga | 43% | 3% | 0,4% | 0,2% |

**$F_{rup}/R$ contra a largura** (5 sementes × 10 realizações; ± = EP entre sementes):

| $T_s$ | 17×17 | 41×41 | seção inteira | largura da seção |
|:--|--:|--:|--:|--:|
| 2 | 0,262 ± 0,019 | 0,260 ± 0,012 | **0,231 ± 0,002** | 335 |
| 32 | 0,547 ± 0,037 | 0,524 ± 0,022 | 0,535 ± 0,004 | 218 |
| 128 | 0,649 ± 0,016 | 0,676 ± 0,010 | 0,662 ± 0,006 | 178 |
| 8192 | 0,700 ± 0,036 | 0,721 ± 0,008 | 0,714 ± 0,003 | 139 |

Nas seções compactas ($T_s \ge 32$) $F_{rup}/R$ é invariante à largura dentro de
±4%, de 17×17 (2,4 mil bastões) à seção inteira (58 mil), 25× em $R$; a escada
de uma semente de 02/09 (0,64–0,65 em $T_s = 128$; 0,70 em 8192) cai dentro da
mesma faixa. Em $T_s = 2$ a seção inteira dá **12% a menos** por bastão que os
recortes (0,231 contra 0,26, sete erros-padrão): a periferia ramificada que o
recorte excluía entra no caminho de carga e é mais fraca por bastão.

**Cascatas contra a largura** (médias por realização; máximo sobre as 50):

| $T_s$ | largura | $R$ | cascatas preterminais | p99 | maior (média) | maior (máx.) | fração terminal |
|:--|--:|--:|--:|--:|--:|--:|--:|
| 2 | 17 | 649 | 41 | 27,0 | 34 | 90 | 0,82 |
| 2 | 41 | 2 108 | 151 | 68,8 | 150 | 397 | 0,70 |
| 2 | 335 | 33 501 | 2 226 | **103,6** | **1 105** | **3 051** | **0,62** |
| 32 | 17 | 1 811 | 116 | 9,0 | 16 | 44 | 0,90 |
| 32 | 41 | 7 263 | 455 | 13,0 | 57 | 135 | 0,89 |
| 32 | 218 | 56 657 | 3 784 | 13,8 | 225 | 538 | 0,87 |
| 128 | 17 | 2 281 | 140 | 10,3 | 21 | 79 | 0,90 |
| 128 | 41 | 11 369 | 704 | 10,4 | 49 | 137 | 0,90 |
| 128 | 178 | 58 162 | 3 595 | 11,8 | 144 | 437 | 0,89 |
| 8192 | 17 | 2 405 | 149 | 10,1 | 20 | 41 | 0,90 |
| 8192 | 41 | 13 575 | 805 | 11,2 | 50 | 161 | 0,90 |
| 8192 | 139 | 58 301 | 3 341 | 12,1 | 149 | 531 | 0,90 |

Leitura, em duas partes que não se confundem:

- **Seções compactas ($T_s \ge 32$): a distribuição é invariante ao tamanho, o
  máximo não.** O p99 fica em 9–14 de 17×17 à seção inteira, e a fração terminal
  em 0,87–0,90. A maior cascata cresce com $R$ (20 → 50 → 150 na média), mas
  cresce menos que $R$ (máximo/$R$: 0,8% → 0,4% → 0,26%) e o número de cascatas
  por realização cresce 24×: é o máximo de uma amostra maior de uma mesma
  distribuição, não uma distribuição que se alarga. É o que o N17 e a carta
  (R1-2) afirmam, agora com 5 sementes e 25× em $R$.
- **Estrutura aberta ($T_s = 2$): a distribuição inteira se alarga com o
  tamanho.** O p99 vai de 27 a 69 a 104; a maior cascata média de 34 a 150 a
  1 105 (máximo 3 051, 9% de $R$); a fração terminal cai de 0,82 a 0,62. Não há
  sinal de saturação até a seção inteira. No regime DLA o corte das cascatas é
  de tamanho finito, e o manuscrito, que afirma o corte no 17×17, não deve
  estender a afirmação à estrutura aberta sem esta ressalva.

Figuras: `figures/frup_and_cascades_by_width.png` (os quatro painéis acima) e
`figures/cascade_size_distribution_by_width.png` (máximo e p99 por realização
contra $R$, $T_s = 2$ e 128).

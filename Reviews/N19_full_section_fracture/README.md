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

# N19: motor de fratura em arrays e ruptura da seção inteira

**Data:** 2026-09-11
**Afeta:** N17 (delimita: a invariância em tamanho da distribuição de cascatas vale nas seções compactas, não na aberta), N18 (corrobora $F_{rup} \propto R$ e a descoberta do corte crescente em $T_s = 2$), I9; o motor de `fiber_bundle_ava.py` de agora em diante
**Dados:** `Reviews/N19_full_section_fracture/` (README, `engine_equivalence.csv`, `width_fracture_{by_realization,summary}.csv`, `raw/wfull/*.txt.gz`, `figures/`)
**Cita:** `Reviews/decision_log/2026-09-10_N18_df_dez_ts_e_escalas_mecanicas.md`, `2026-09-02` (escada de larguras, Fase C)

> Entrada de registro. **Append-only** — não editar.

## Pergunta e decisões

Michael: gerar dados de ruptura sem limitar $x$ e $z$. Decisões dele: acelerar
o motor antes; $T_s \in \{2, 32, 128, 8192\}$; $|y| \le 100$ e 10 realizações;
nesta máquina.

## Motor

`Code/Fracture_fibril/load_path_arrays.py`: o mesmo caminho de carga de
`filter_rids`, em arrays CSR e `numba`; `fiber_bundle_ava.py -engine arrays` é
o padrão. O ganho (60× na seção inteira: 115 s contra 1 h 54) vem da
representação, não do algoritmo. **O que foi preciso para a igualdade byte a
byte:** emular a ordem de iteração dos `set`s do CPython dentro do bastão
(últimos bits de $\langle 1/n\rangle$, logo de $F^*$) e dentro da camada (empate
entre vizinhos no sweep; sem isso 38 dos 40 troncos do N18 davam um caminho de
carga inicial diferente, 2% dos bastões em $T_s = 2$). Com a emulação: 40/40
arquivos do N18 (400 realizações) e as escadas 17×17 e 181×181 de 02/09
idênticos. Registrado aqui porque é uma dependência de implementação que o
modelo carregava sem saber: o resultado do legado depende da ordem de hash de
ints do CPython, determinística mas não documentada até hoje.

## Resultado da seção inteira (README §2)

- $F_{rup}/R$ invariante à largura (±4%) para $T_s \ge 32$ até 25× em $R$; em
  $T_s = 2$ a seção inteira dá 0,231 contra 0,26 nos recortes (−12%, 7 EP): a
  periferia ramificada porta carga e é mais fraca por bastão.
- Só 57% dos bastões de $T_s = 2$ dentro de $|y| \le 100$ portam carga (97–99,8%
  nos outros).
- **Cascatas:** nas seções compactas o p99 fica em 9–14 e a fração terminal em
  0,87–0,90 da 17×17 à seção inteira; o máximo cresce menos que $R$ (amostra
  maior, mesma distribuição). Em $T_s = 2$ a distribuição inteira se alarga: p99
  27 → 69 → 104, maior cascata média 34 → 150 → 1 105, fração terminal 0,82 →
  0,62, sem saturação. **No regime DLA o corte das cascatas é de tamanho finito.**

## O que decorre

- N17 e a carta (R1-2) ficam como estão: afirmam a invariância na seção
  compacta ($T_s = 128$), e ela se confirma com 5 sementes. O manuscrito afirma
  o corte no 17×17 e não generaliza. Quem estender a afirmação à estrutura
  aberta encontra crescimento com o tamanho; fica registrado.
- Nada entra no manuscrito sem decisão nova (regra de 2026-09-03).
- Os brutos (11 MB gz) ficam no diretório; com o motor novo a campanha refaz-se
  em 1 h, então versioná-los é escolha de Michael no commit.

## Rastreabilidade

| número | origem |
|:--|:--|
| equivalência e tempos dos motores | `N19_full_section_fracture/engine_equivalence.csv`; `compare_fracture_engines.py` |
| $F_{rup}/R$, p99, máximo, fração terminal por largura | `N19_full_section_fracture/width_fracture_{summary,by_realization}.csv` |
| brutos | `N19_full_section_fracture/raw/wfull/` (+ sha256) |
| scripts | `Code/Fracture_fibril/{load_path_arrays,fiber_bundle_ava,test_load_path_arrays}.py`; `Code/Data_analysis/{run_local_width_fracture.sh,summarize_width_fracture.py,plot_n19_figures.py,compare_fracture_engines.py}` |

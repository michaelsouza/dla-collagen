# Manuscrito ER12738 como foi submetido

Cópia congelada do que os dois revisores leram. **Não editar.** A revisão viva
está em `Paper/paper_PRE.tex`; o estado dela, em
`Reviews/Estado_revisao_ER12738.md`.

Existe porque a carta ponto a ponto (nó N14) cita trechos literais do que foi
submetido, e o arquivo vivo já não os contém.

## Origem

Tudo veio do commit `5d2d272` (2026-07-23), o último estado do manuscrito antes
de qualquer edição de revisão:

| aqui | origem em `5d2d272` |
|:--|:--|
| `paper_PRE.tex` | `Paper/paper_PRE.tex` |
| `paper_PRE.pdf` | `Paper/paper_PRE.pdf` (19 páginas) |
| `apssamp.bib` | `Paper/apssamp.bib` |
| `Figures/figure_1.pdf` … `figure_9.pdf` | `Paper/Figures/` |

O mesmo texto aparece antes como `Paper/PRE/paper_PRE_new.tex` no commit
`0f487d6`; as duas versões diferem apenas no prefixo `Figures/` dos caminhos de
figura.

## Por que esta é a versão submetida

Cinco afirmações citadas textualmente nos pareceres (`Reviews/Referees.md`)
estão neste arquivo e **não** estão no manuscrito atual:

| citado pelo revisor | onde está aqui |
|:--|:--|
| $\gamma$ de $2{,}31 \pm 0{,}05$ a $2{,}80 \pm 0{,}04$, cruzando o $5/2$ | conclusão e Fig. 9 |
| "quantitative bridge" entre estrutura e estatística de falha | último parágrafo da discussão |
| transição de load sharing local para global | conclusão |
| especulação sobre enfisema e aneurisma | conclusão |
| ensemble de 10 fibrilas por $T_s$ | seção de fratura |

## Reproduzir

```
latexmk -pdf paper_PRE.tex
```

Compila sem erro e sem referência quebrada, dando as mesmas 19 páginas do
`paper_PRE.pdf` arquivado (conferido em 2026-09-03).

## O que mudou desde então

O arquivo vivo tem 452 linhas contra as 363 daqui. Pelo `latexdiff`, são 46
blocos removidos e 52 acrescentados. A figura 8 daqui ($\Psi$ contra força normalizada) foi retirada,
e uma figura nova entrou como 7 ($D_f$ contra descritores do backbone),
deslocando a numeração das figuras 7 a 9.

Parte dessas edições já está superada pelas medições posteriores — a Eq. (6)
atual ajusta um expoente que N10 e N11 decidiram não afirmar, e o texto do
$D_f$ como proxy validado precisa virar leitura de *crossover* por causa de N7.

# Correção: a distribuição de cascatas não é invariante em $m$; o 0,72–0,76 é da escada de tamanho

**Data:** 2026-09-03
**Corrige:** a prosa de R1-2 em `Reviews/Respostas_ER12738.qmd` (§4.2, §4.3, §4.4)
e o parágrafo da estatística, o resumo e a conclusão de `Paper/paper_PRE.tex`
**Afeta:** N10; a resposta R1-2; a Fig. 9 do manuscrito revisado
**Achado ao:** exportar os `.dat` da Fig. 9 e conferir os números contra o texto

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## O que estava errado

A resposta a R1-2 listava **três invariâncias** do corte da distribuição de
cascatas, e a primeira dizia:

> First, the shape of the distribution is insensitive to the disorder: across
> $m = 1$ to $10$ at fixed geometry, the fraction of single-molecule cascades
> stays between 0.72 and 0.76 and the 99th percentile of the cascade size
> between 8 and 20.

O intervalo $0{,}72$–$0{,}76$ **não é da varredura em $m$.** É a coluna `frac_1`
da escada de janelas da Fase C — $0{,}745$ a $0{,}760$ em
`avalanche_ladder_ts128.csv` e $0{,}731$ a $0{,}762$ em `_ts8192.csv` —, isto é, a
invariância de **tamanho do corpo de prova**. A prosa colou o número de uma
invariância na outra.

Medido nas cascatas da campanha, a $T_s = 128$, com $m$ de 1 a 10:

| $m$ | fração de cascatas unitárias | p99 | cascatas preterminais |
|--:|--:|--:|--:|
| 1 | 0,778 | 8 | 3.071.545 |
| 2 | 0,724 | 12 | 1.533.784 |
| 3 | 0,668 | 14 | 1.129.963 |
| 5 | 0,617 | 16 | 925.371 |
| 10 | 0,585 | 19 | 799.181 |

A fração unitária cai 19 pontos e o p99 mais que dobra. Isso **não** é
insensibilidade. O p99 de 8 a 19 é compatível com o "8 a 20" que a prosa
afirmava, então metade da frase estava certa e metade não — que é o tipo de erro
que passa por revisão.

## Por que o erro é o oposto do que parecia

Ele **enfraquecia** o argumento em vez de inflá-lo, o que é raro e por isso vale
registrar. A dependência em $m$ é exatamente o mecanismo que a resposta a R1-3
usa contra universalidade: limiares mais próximos falham juntos, então desordem
estreita dá cascatas maiores, e é por isso que o expoente ajustado varia quase
uma unidade com $m$ em geometria fixa. Afirmar invariância em $m$ contradizia a
§5.2 do mesmo documento, que afirma o contrário — e o revisor tinha as duas
frases para comparar.

O que de fato é invariante, e é o que o texto passa a dizer:

- **Em arquitetura, acima de $T_s \approx 16$** ($m=2$): $P(S>5)$ entre $0{,}037$
  e $0{,}042$ e p99 de 12 a 13, contra $0{,}077$ e 35 em $T_s = 2$.
- **Em tamanho**, fator 25 no número de moléculas: fração unitária $0{,}72$–$0{,}76$.
- **O corte existe em toda a grade.** Estreitar a desordem desloca peso dos
  eventos unitários para o corte; nunca o remove. Nenhuma condição é livre de
  escala.

## O que decorre

- **Exportar a figura é uma checagem, não uma tarefa mecânica.** O erro estava no
  texto desde o rascunho de R1-2 e sobreviveu à revisão do documento, ao corte
  dos seis itens voluntários e à escrita do manuscrito. Caiu no primeiro momento
  em que alguém pediu os números na forma de duas colunas.
- **Número emprestado de outra medição carrega a etiqueta errada.** Vale a mesma
  regra de `2026-09-03_correcao_atribuicao_weibull_literatura.md`: o dado estava
  certo, a atribuição não. O teste que pega isso é perguntar de qual CSV a coluna
  veio — e a rastreabilidade de R1-2 agora tem uma linha por invariância, cada
  uma nomeando seu arquivo.
- **N10 não muda de conclusão.** O corte continua sendo propriedade do modelo, a
  lei de potência pura continua rejeitada em 48 de 50 condições, e o manuscrito
  continua não reportando expoente.

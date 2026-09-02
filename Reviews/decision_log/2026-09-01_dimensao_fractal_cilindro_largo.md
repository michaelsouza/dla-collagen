# A dimensão fractal medida num cilindro 17 vezes mais gordo — e o que ela diz

**Data:** 2026-09-01
**Afeta:** N7 (corrobora o fechamento), N15 (muda o alvo), I9 (lado estrutural), N17 / Fase C

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## Quem chegou primeiro

Isto não é um achado novo. O `Reviews/quenched_campaign_report/README.md` §4,
escrito noutra sessão, já mostrou sobre as fibrilas da campanha que o $D_f$
publicado depende da janela de ajuste e que os valores do meio da grade são um
*crossover* entre dois regimes, não uma dimensão que varia. Aquele texto fecha
N7. Esta entrada registra uma confirmação **por outro caminho**, e o que ela
acrescenta.

## O que foi feito, em palavras simples

O gerador ganhou um modo em que a fibrila não tem pontas: o eixo dá a volta,
como um anel, e toda molécula lançada engorda a seção em vez de esticar o
comprimento. Com isso, com o mesmo custo de uma fibrila comum, obtém-se uma
seção transversal com 5.000 partículas em vez de 300 — e o raio vai de ~20 para
70 a 160 unidades de rede.

Antes de usar, verificou-se que esse anel reproduz a estrutura local da fibrila
comum (coordenação e encaixes iguais dentro de 2%, cinco sementes, três
condições — ver `PhaseC_periodic_cylinder/README.md` §4b). Depois mediu-se o
$D_f$ nele, pelo mesmo método do artigo, com cinco sementes por condição.

## O que saiu

| $T_s$ | raio | alcance do ajuste | $D_f$ (regra que se sustenta) | publicado |
|---:|---:|---:|---:|---:|
| 2 | 161 | 1,5 década | **1,675 ± 0,023** | 1,708 |
| 128 | 86 | 1,2 década | **1,964 ± 0,041** (miolo) — e nenhuma regra dá 1,79 | 1,790 |
| 8192 | 68 | 1,1 década | **1,955 ± 0,012** | 1,963 |

Nos extremos o anel bate com o relatório à terceira casa e com o artigo. No
meio da grade, bate com o relatório (1,96) e **não com o artigo (1,79)** — o
valor publicado não sai de nenhuma regra objetiva, nem na fibrila comum nem no
anel.

## O que o anel acrescentou

**Primeiro, alcance.** Em $T_s=2$ o ajuste cobre 1,5 década — contra 0,9 na
fibrila comum — e devolve 1,675 ± 0,023: o valor de um agregado DLA plano, agora
medido sobre um intervalo de escala de verdade.

**Segundo, uma prova de que $T_s=128$ não é fractal.** Uma regra de janela
"proporcional ao tamanho" ($0{,}15R$ a $0{,}5R$) deveria devolver o mesmo número
em objetos de tamanhos diferentes se a estrutura fosse a mesma em todas as
escalas. Devolve 1,95 na fibrila comum e 1,69 no anel. A explicação é
geométrica: na fibrila pequena a janela cai no miolo denso; no anel grande cai
na zona onde a densidade já está caindo. **A regra dá números diferentes porque
o objeto é diferente em escalas diferentes.** As inclinações locais, com barra
de erro entre sementes, descem sem parar: 1,93 → 1,87 → 1,78 → 1,67 → 1,73 →
1,41 → 0,48. Não há patamar; há um miolo compacto com uma casca.

**Terceiro, um controle de objeto.** Uma fibrila comum gerada pelo mesmo
binário e medida pelo mesmo script dá, em $T_s=128$, os mesmos números que o
anel sob cada regra (faixa cheia 1,58 contra 1,58; miolo 1,94 contra 1,96). A
distância ao publicado é a janela, não a geometria periódica.

## Uma ressalva

A janela de miolo ($r=4$ a $8$) em $T_s=2$ varia 0,23 entre sementes: oito
unidades de raio numa seção aberta contêm poucas dezenas de partículas, e o eixo
do anel carrega a coluna que o semeou. Nessa condição a regra que se sustenta é
a proporcional, que bate com o relatório em 0,001. Registrado para ninguém
tropeçar nisso depois.

## O que decorre

- **N7:** fechado pelo relatório; esta medição corrobora com objeto
  independente e *ensemble*. A frase para o manuscrito é a do relatório: em
  $T_s$ baixo há um agregado DLA com $D_f \approx 1{,}68$; conforme $T_s$ cresce
  o regime fractal encolhe até desaparecer e a seção vira sólido ($D = 2$).
- **N15:** validar o gerador novo "contra o $D_f$ publicado" perdeu o sentido,
  porque o publicado é uma escolha de janela. O alvo passa a ser a estrutura
  local (coordenação, encaixes) e os $D_f$ sob regra uniforme do relatório.
- **I9, lado estrutural:** resolvido por reformulação, não por alargamento. Não
  se afirma mais uma dimensão ajustada sobre meia década; descreve-se o
  *crossover*, que é o que os dados contêm.
- **Fase C:** a parte do $D_f$ está feita. O que ela ainda deve é a parte das
  avalanches — se o corte em ~90 se move quando o corpo de prova tem 50 vezes
  mais moléculas. O anel de $T_s=128$ fraturado pela janela padrão reproduz a
  campanha; a fratura pela seção inteira está em execução.

Dados: `PhaseC_periodic_cylinder/df_wide_cylinders.csv` e
`df_local_slopes_wide.csv`, com a receita de regeneração no cabeçalho.

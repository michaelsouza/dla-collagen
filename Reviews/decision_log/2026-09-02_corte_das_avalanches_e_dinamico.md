# O corte das avalanches é do modelo, não do tamanho da fibrila

**Data:** 2026-09-02
**Fecha:** a parte das avalanches da Fase C (N17); o lado mecânico da I9
**Afeta:** N10, N11, N12

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## A pergunta, em palavras simples

Quando a fibrila simulada é puxada até romper, ela solta "avalanches" — grupos de
moléculas que quebram juntas. Na campanha, quase três quartos dessas avalanches
têm uma molécula só, 99% têm até uma dúzia, e a maior de todas tem uns 90.
Depois vem um estouro final que leva quase 90% da fibrila de uma vez.

A dúvida era: **isso é assim porque o modelo é assim, ou porque a fibrila é
pequena demais para caber avalanches maiores?** Se fosse a segunda coisa, tudo
que o artigo diz sobre a estatística de ruptura seria efeito de caixa.

## Como se testou

Pegou-se **uma única fibrila larga** — o cilindro periódico de $T_s=128$ com
5.000 partículas por seção — e fraturou-se a mesma fibrila por janelas de corte
cada vez maiores: 17×17 (o padrão da campanha), 41×41 e 81×81. Só a janela muda;
a estrutura é a mesma. O motor de fratura é o de produção, sem alteração.

Antes de ver os degraus grandes, escreveu-se o que cada hipótese prevê
(`PhaseC_periodic_cylinder/README.md` §4d): se o corte for do modelo, a forma da
distribuição não muda com a janela; se for do tamanho, o p99 cresce e a fração
do estouro final cai.

## O que saiu

| janela | moléculas | fração de tamanho 1 | p90 | p99 | fração no estouro final |
|:--|---:|---:|---:|---:|---:|
| 17×17 | 2.372 | 0,75 | 2 | 10 | 0,88 |
| 41×41 | 12.023 | 0,75 | 3 | 11 | 0,87 |
| 81×81 | 37.536 | 0,76 | 3 | 11 | 0,88 |
| campanha (referência) | 2.2–2.3 mil | 0,72 | 3 | 12 | 0,88 |

**Quinze vezes mais moléculas e nada se move.** A previsão de "é o tamanho" está
refutada sobre 1,2 década. E mesmo a maior avalanche isolada saturou: 39 → 127 →
121 — não cresceu do 41×41 para o 81×81 apesar de três vezes mais material.

## O que isso significa

1. **A faixa de uma década das avalanches é propriedade do modelo.** Não há
   fibrila grande o bastante para fazê-la crescer. Isso é um **resultado**, não
   uma limitação: descreve como este sistema rompe — quase tudo em estouros
   unitários, e depois um colapso quase total de uma vez. Fratura frágil
   localizada, sem regime crítico.

2. **A I9 tinha duas metades com causas diferentes.** O alcance curto do $D_f$
   era mesmo falta de tamanho, e engordar a fibrila resolveu
   (`2026-09-01_dimensao_fractal_cilindro_largo.md`). O alcance curto das
   avalanches não era — e engordar não mudou nada. O manuscrito pode dizer as
   duas coisas com a mesma honestidade.

3. **Para R1-2 e R2-4** (retirada da linguagem de SOC): a resposta deixa de ser
   "removemos o termo" e passa a ser "medimos: o corte não depende de $m$, não
   depende de $T_s$ acima de 16, e não depende do tamanho do corpo de prova sobre
   uma década". Três invariâncias medidas valem mais que qualquer recuo textual.

4. **Para N10 e N11:** confirma o que já estava indicado — não se ajusta expoente
   sobre uma década, e a comparação com $5/2$ não tem objeto. O que se reporta é
   a forma da distribuição, que é estável.

## Ressalvas

- Uma condição de $T_s$ (128) e uma fibrila; 5, 3 e 2 realizações por janela. As
  estatísticas de forma são estáveis com esses números (p99 por realização
  fica entre 6 e 14 em todas as janelas), mas o máximo isolado não é — por isso
  foi excluído do critério antes de ver os dados.
- As seções inteiras (181×181 em $T_s=128$; 141×141 em $T_s=8192$) seguem em
  execução, de 3 a 6 horas cada. São confirmação: o teste já está decidido sobre
  1,2 década, e uma condição compacta diferente ($T_s=8192$) daria a segunda
  arquitetura.

## Dois erros operacionais desta sessão, para não repetir

O carregador de fibrilas construía vizinhanças por todos-os-pares e teria
levado horas numa seção inteira; foi trocado por *hash* espacial com resultado
idêntico (commit `ab128dc`). E, ao relançar as fraturas, um caminho de log
montado à mão apontou para o arquivo errado: por 40 minutos acreditei que o
81×81 tinha morrido quando ele havia terminado normalmente. O sintoma — log
vazio — tinha outra explicação (saída bufferizada), e o arquivo de resultado
estava lá o tempo todo. **Verificar o artefato, não o log.**

Dados: `PhaseC_periodic_cylinder/avalanche_ladder_ts128.csv`; método em
`summarize_avalanche_ladder.py`.

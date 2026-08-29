# Fase C — cilindro periódico: o corte das avalanches é física ou é tamanho de caixa?

Plano de validação escrito em 2026-08-27. As medições da §1 foram feitas sobre a
campanha quenched em `$DLA_PROJECT/campaign` (SDumont2), já completa: 10 $T_s$ ×
200 fibrilas × 5 valores de $m$ = 10.000 arquivos de avalanche, 2.000 fibrilas.

## 1. Por que esta fase existe

Quatro medições feitas sobre a campanha, nesta ordem. Cada uma responde à
anterior.

### 1.1 O corpo de prova é 2% a 8% do que se gera

O corte para a fratura (`stress_strain_ava.py:408`: $|x|\le8$, $|y|\le100$,
$|z|\le8$) seguido da extração do backbone deixa muito menos material do que se
imagina. Média sobre 20 fibrilas × 50 realizações, $m=2$:

| $T_s$ | partículas | moléculas | % das 30.000 | partículas/molécula |
|---:|---:|---:|---:|---:|
| 2 | 10.051 | 600 | 2,0% | 16,7 |
| 8 | 15.264 | 920 | 3,1% | 16,6 |
| 16 | 20.105 | 1.212 | 4,0% | 16,6 |
| 32 | 27.311 | 1.647 | 5,5% | 16,6 |
| 64 | 33.073 | 1.995 | 6,7% | 16,6 |
| 128 | 35.960 | 2.166 | 7,2% | 16,6 |
| 512 | 37.492 | 2.265 | 7,5% | 16,6 |
| 1024 | 38.058 | 2.297 | 7,7% | 16,6 |
| 4096 | 38.494 | 2.326 | 7,8% | 16,6 |
| 8192 | 37.663 | 2.283 | 7,6% | 16,5 |

A razão partículas/molécula fica em 16,5–16,7 nas dez condições — coerente com
bastões de 18 l.u. truncados nas bordas $y=\pm100$. Serve de teste de sanidade
da contagem.

Consequência imediata: **o número 30.000 não pode ser usado para descrever o
objeto mecânico.** Ele descreve a fibrila (objeto sobre o qual $D_f$ é medido);
o objeto fraturado tem $10^3$ moléculas e, na calibração lateral
(1 l.u. = 1,5 nm), é um prisma de $25{,}5\times25{,}5\times300$ nm.

### 1.2 A faixa dinâmica das avalanches é de uma década

Avalanches excluindo o evento terminal, $m=2$:

| $T_s$ | $N$ moléculas | frac. tam. 1 | p90 | p99 | maior não-terminal | evento terminal |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 600 | 72% | 4 | 32 | 147 | 462 (77% do sistema) |
| 32 | 1.647 | 72% | 3 | 12 | 89 | 1.436 (87%) |
| 128 | 2.166 | 72% | 3 | 12 | 91 | 1.905 (88%) |
| 1024 | 2.297 | 72% | 3 | 12 | 97 | 2.011 (88%) |
| 8192 | 2.283 | 71% | 3 | 13 | 72 | 1.988 (87%) |

Com a janela de ajuste do manuscrito ($s_{\min}\approx20$), a faixa vai de 20 a
~90: **0,56 a 0,87 décadas**. Abrindo para $s_{\min}=1$, o nominal chega a ~2
décadas, mas 72% da massa está em $s=1$ e o p99 é 12.

A distribuição é **bimodal**: chuvisco de eventos unitários, e então um único
evento terminal que leva 77% a 88% do sistema. É ruptura frágil localizada.

**Quantidade de dados não é o gargalo.** São 148 mil eventos em 20 fibrilas, e a
campanha completa tem dez vezes isso. A precisão é excelente; o que falta é
faixa de tamanhos. São coisas diferentes, e a Fase B dimensionou a campanha para
a primeira.

### 1.3 Não é escolha de $m$

Varredura completa em $T_s=128$:

| $m$ | frac. tam. 1 | p99 | maior não-terminal | evento terminal |
|---:|---:|---:|---:|---:|
| 1 | 78% | 8 | 89 | 79% do sistema |
| 2 | 72% | 12 | 91 | 88% |
| 3 | 66% | 14 | 68 | 90% |
| 5 | 61% | 17 | 69 | 91% |
| 10 | 57% | 20 | 62 | 91% |

O p99 anda de 8 a 20 — meia década — enquanto o maior evento *diminui*. A faixa
de uma década vale nas 50 combinações de $(T_s, m)$ medidas.

### 1.4 Não é o corte lateral, e não há teto para subir

Moléculas por seção transversal, por fibrila, com cortes de larguras diferentes
(média de 5 fibrilas, $|y|\le90$):

| $T_s$ | **±8 (atual)** | ±12 | ±16 | ±24 | fibrila inteira | teto de ganho |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | **61** | 118 | 185 | 279 | 308 | 5,1× |
| 32 | **134** | 219 | 271 | 295 | 295 | 2,2× |
| 128 | **176** | 269 | 290 | 295 | 295 | 1,7× |
| 8192 | **192** | 283 | 289 | 289 | 289 | 1,5× |

A coluna "fibrila inteira" é praticamente constante — 308, 295, 295, 289. Faz
sentido: são sempre 30.000 moléculas distribuídas num comprimento parecido, de
modo que o material disponível por seção é fixo em ~300. O $T_s$ decide apenas
se ele fica espalhado num anel ralo ou apertado num cilindro denso.

**Alargar o corte tem teto de 1,5× a 5×.** E o 5,1× de $T_s=2$ é otimista: o que
está fora do tronco naquela condição são galhos ramificados que a extração do
backbone removeria de qualquer forma.

O corte também não está limitando as avalanches hoje: em $T_s=128$ o sistema tem
2.166 moléculas e a maior avalanche é 91 — 4% do sistema. E ao longo da grade
$N$ cresce 3,9× enquanto a maior avalanche **cai** (147 → 72).

## 2. As duas explicações concorrentes

**(A) Seção transversal pequena demais.** Com poucos elementos por seção, a
queda de $N(i)$ ao remover algumas moléculas eleva a tensão nas restantes o
bastante para disparar o colapso da seção. Seções mais gordas permitiriam
cascatas maiores antes da ruptura, e mais décadas.

**(B) Elo mais fraco em série.** O tronco é uma pilha de ~200 camadas, ou ~12
seções independentes dado que os bastões têm 18 l.u. A ruptura ocorre na seção
mais fraca. Aumentar $N$ por seção faz cada seção convergir para a média
(flutuação cai com $1/\sqrt{N}$), o que torna as seções mais parecidas entre si
e o colapso mais simultâneo — menos décadas, não mais.

Os dados da §1.4 favorecem (B): a seção já triplicou ao longo da grade (61 →
192) e a ruptura ficou mais abrupta (terminal de 77% → 87%). A seção mais fraca
passou de 23% abaixo da média em $T_s=2$ para 19% abaixo em $T_s=8192$.

**Mas $T_s$ muda arquitetura e seção ao mesmo tempo.** O teste é confundido. Só
um experimento que varie a seção com a arquitetura fixa decide.

## 3. Desenho proposto

Gerar um **cilindro periódico em $y$** com lançamento externo, e **abrir o
cilindro** antes da fratura.

- **Periodicidade em $y$** elimina pontas e afunilamento — que o corte já
  descartava — e permite gastar todas as moléculas na seção transversal em vez
  de no comprimento.
- **Lançamento externo preservado** (sorteio de $y$ uniforme no período e ângulo,
  a raio fixo) mantém o bloqueio lateral, que é o mecanismo que faz o DLA ser
  DLA. É o que o tubo fechado destruiria.
- **Abertura antes da fratura** devolve dois extremos livres, de modo que o
  motor de fratura roda **sem nenhuma alteração**: o corte em $|y|\le100$ e a
  extração do backbone de ponta a ponta continuam válidos como estão.

Ganho de escala: cada molécula ocupa 18 camadas, então 30.000 moléculas dão
540.000 fatias. Espalhadas nas ~3.800 camadas de hoje, dão ~300 por seção; num
período de 216, dão **~2.500 por seção** — 13× mais, ao mesmo custo. Em
diâmetro, a seção passa de 17 para ~65 l.u.

Notas de desenho:

- **Período 216** (= 12×18 = 54×4) ou 180. Não 201: o período precisa fechar com
  o comprimento do bastão (18) e com a regra de fixação em múltiplos de 4, senão
  a emenda quebra o padrão de encaixe.
- **Onde abrir é indiferente** — no cilindro periódico todo $y$ é equivalente.
  Isso é melhor que hoje, onde o tronco fica na região central, a mais velha e
  mais engrossada, portanto não típica.
- **Os bastões truncados voltam** no plano de abertura. É desejável: reproduz o
  mesmo tipo de borda dos corpos de prova da campanha, preservando
  comparabilidade.

## 4. Plano de validação

### 4.1 Densidade é variável de controle, não resultado

Hoje a densidade do tronco **emerge** de $n_b=30.000$ com um dado $T_s$: 61
moléculas por seção em $T_s=2$, 192 em $T_s=8192$. Num cilindro de 216 camadas,
lançar 30.000 moléculas produziria densidade muito maior, e a comparação com o
tronco atual não significaria nada — tudo diferiria já pela densidade.

**Procedimento:** ajustar $n_b$ até a densidade por camada bater com a da
campanha (tolerância 2%), na mesma condição de $T_s$; só então comparar as
demais grandezas.

### 4.2 Grandezas e tolerâncias, fixadas antes de olhar

| Grandeza | Fonte de comparação | Tolerância para "bate" |
|:--|:--|:--|
| moléculas por seção | §1.4 desta nota | 2% (é a variável de controle) |
| coordenação $\langle K\rangle$ | campanha, mesma $T_s$ | 5% |
| área de seção $\langle N\rangle$ | campanha, mesma $T_s$ | 5% |
| $D_f$ em seção transversal | `validate_fractal_proxy.py` | 0,02 em valor absoluto |
| $F_{rup}$ | campanha, mesma $T_s$ | dentro da barra de erro da Fase B |
| p99 e maior avalanche não-terminal | §1.2 desta nota | dentro da barra de erro da Fase B |
| fração do evento terminal | §1.2 desta nota | 3 pontos percentuais |

O motivo de fixar a lista antes é evitar o resultado sempre favorável: comparar
dez grandezas, ver nove baterem e declarar validado.

### 4.3 Tamanhos de amostra

As grandezas não têm todas a mesma variabilidade entre fibrilas, e isso decide
quantas fibrilas são necessárias.

- **Estruturais** ($K$, $N$, densidade, $D_f$): são médias sobre milhares de
  moléculas dentro de cada fibrila. **5 fibrilas por condição bastam** para
  enxergar diferenças de poucos por cento.
- **Mecânicas** ($F_{rup}$, cauda das avalanches): a Fase B mediu a dispersão —
  com 20 fibrilas, SE($\gamma$) fica entre 0,027 e 0,060. **20 fibrilas × 50
  realizações por condição**, que é exatamente o desenho do piloto da Fase B,
  de modo que o poder estatístico já é conhecido e a comparação é direta.

Com menos que isso, a conclusão "não afetou" seria indistinguível de "não
consegui ver". É o principal risco deste plano.

### 4.4 Condições e previsão registrada

Três condições: $T_s = 2$, $128$, $8192$ — as duas pontas e o meio.

**Previsão, registrada antes de rodar:** as pontas da fibrila bloqueiam
moléculas que iriam para o meio, e esse bloqueio pesa mais onde a estrutura é
aberta e ramificada. Portanto **espera-se concordância em $T_s=8192$ e é em
$T_s=2$ que pode falhar**. Se o resultado for o oposto, alguma suposição deste
plano está errada e cabe investigar antes de prosseguir.

Depois da validação no tamanho atual, dois passos:

1. **Auto-correlação pela volta.** Gerar com período 216 e 432 e comparar
   densidade e coordenação. Se o período curto for insuficiente, o cilindro
   enxerga a si mesmo pela imagem periódica.
2. **Engordar** a seção até ~65 l.u. e medir se o corte das avalanches se move.

## 5. Decisão conforme o resultado

O teste de tamanho finito compara cilindro fino com cilindro gordo, **dentro da
família periódica**. Ele não depende da validação contra a campanha:

| Validação | Teste de tamanho | O que se pode afirmar |
|:--|:--|:--|
| passa | corte se move com a seção | explicação (A); os números do artigo são de tamanho finito e precisam ser requalificados |
| passa | corte fica parado | explicação (B); o corte é dinâmico, e isso vira resultado positivo contra R1-2 / R2-4 |
| falha | qualquer | a pergunta é respondida dentro de um modelo aparentado; a diferença em relação à campanha vira achado sobre o papel das pontas |

Nos três casos sai resultado. É o que justifica rodar.

## 6. Custo

Geração: 10,6 min-núcleo por fibrila em $n_b=30.000$ (Fase B). Vinte fibrilas em
três condições ≈ **11 CPU-h**. Fratura: 9,2 s por realização × 50 × 60 fibrilas
≈ **8 CPU-h**. O cilindro gordo custa 2–3× por fibrila.

Total da validação abaixo de **20 CPU-h** — meia hora em 24 núcleos. Não há
motivo para economizar em número de fibrilas.

Comparação: obter a mesma seção transversal por fibrilas maiores exigiria
$n_b=300.000$, ~10× o custo atual por fibrila, 1 a 3 h cada.

## 7. Pendências de implementação

1. Modo periódico em `fast_dla2.cpp`: fronteira em $y$, lançamento cilíndrico,
   raio de morte radial. A CLI e o formato de saída devem permanecer.
2. Escritor que abre o cilindro num plano e emite no esquema `extended`, para
   que `worker_fracture.sh` consuma sem alteração.
3. Verificação de que o padrão de encaixe (staggers 0D–4D) não quebra na emenda
   com período 216.

## 8. Relação com a DAG

Esta fase é a montante de **N10** (reanálise estatística), **N11** (expoente
frente a $5/2$) e **N12** (estatuto da relação $D_f \leftrightarrow$ ruptura).

A §1.2 já basta para questionar N11: um expoente ajustado sobre 0,7 décadas não
sustenta comparação com um valor de campo médio. E a §1.1 expõe um
confundimento novo para N12 — ao correr a grade de $T_s$, o número de moléculas
do corpo de prova varia 3,9× junto com $D_f$, de modo que as duas quantidades
não são descritores independentes. Alargar o corte até a fibrila inteira
tornaria a seção ~300 em todas as condições e isolaria arquitetura de tamanho;
é barato, e independente desta fase.

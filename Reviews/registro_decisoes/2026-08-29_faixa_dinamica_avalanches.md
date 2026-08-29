# A campanha fechou e a faixa dinâmica virou o problema

**Data:** 2026-08-29  
**Origem:** §17 de `DAG_dependencias_revisao.md`, dividida em 2026-08-29.

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

Medições sobre `$DLA_PROJECT/campaign` no SDumont2. Detalhamento e plano
experimental em `Reviews/PhaseC_cilindro_periodico/`.

#### Mudança de estado que a DAG não registrava

**N16 está concluído.** A campanha tem **10.000 arquivos de avalanche** (1.000
por $T_s$, 2.000 por valor de $m$) e **2.000 fibrilas** — 10 $T_s$ × 200
fibrilas × 5 valores de $m$, exatamente o plano da §16. A §2 ainda dava N16 como
"bloqueado por N15", quatro dias depois de o obstáculo de submissão da §16 ter
sido contornado. **Nada detectou essa defasagem** — ver §18.

**N5 está atendido pelos dados.** A varredura é $m \in \{1,2,3,5,10\}$. O que
resta em N5 é textual: delimitar qual sub-faixa tem respaldo experimental na
literatura de fibrila única, e escrever. Deixa de ser decisão de produção.

**N15 não foi verificado nesta sessão.** A campanha usou o gerador otimizado,
mas não conferi se a validação de $D_f$ em escala foi executada.

#### O achado que reordena N10, N11 e N12

Quatro medições, em ordem:

1. **O corpo de prova é 2% a 8% do que se gera.** O corte
   ($|x|\le8$, $|y|\le100$, $|z|\le8$) mais o backbone deixam **600 moléculas em
   $T_s=2$ e 2.326 em $T_s=4096$**, contra 30.000 lançadas. A razão
   partículas/molécula fica em 16,5–16,7 nas dez condições, coerente com bastões
   de 18 l.u. truncados na borda.
2. **A faixa dinâmica das avalanches é de uma década.** Excluindo o evento
   terminal: **72% das avalanches têm tamanho 1**, p99 = 12, e a maior
   não-terminal é ~90. Com a janela do manuscrito ($s_{\min}\approx20$) isso dá
   **0,56 a 0,87 décadas**. Então vem um evento terminal único que leva **77% a
   88% do sistema**. A distribuição é bimodal: ruptura frágil localizada.
3. **Não é escolha de $m$.** Nas cinco condições de $m$ em $T_s=128$, o p99 anda
   de 8 a 20 e a maior avalanche *diminui* (89 → 62). A faixa de uma década vale
   nas 50 combinações $(T_s, m)$ medidas.
4. **Não é o corte lateral.** A fibrila inteira tem ~300 moléculas por seção
   transversal em **todas** as condições (308 / 295 / 295 / 289). Alargar o
   corte tem teto de 1,5× a 5×; a hipótese de seção maior precisaria de ~10×.

#### Consequências por nó

| Nó | Consequência |
|:--|:--|
| **N10** | Ajustar lei de potência com corte sobre 0,7 décadas não se sustenta. `Clauset2009` passa a ser a autoridade para **não** afirmar. O alvo muda: descrever a distribuição como ela é (bimodal, dominada por eventos unitários) em vez de estimar expoente. |
| **N11** | Comparar expoente a $5/2$ sobre menos de uma década não é defensável. **Provavelmente encerra N11 como afirmação quantitativa** — coerente com a recusa de atribuir classe de universalidade que já está no texto. |
| **N12** | **Confundimento novo.** Ao correr a grade de $T_s$, o número de moléculas do corpo de prova varia 3,9× *junto* com $D_f$. Com janela fixa, $N \sim R^{D_f}$ por construção: os dois não são descritores independentes, e a Fig. 7 os correlaciona separadamente. |
| **N4** | **Reforçado, e de defensivo passa a positivo.** A retirada de SOC deixa de ser concessão e passa a ser resultado medido: corte insensível a $N$ e a $m$, ruptura num evento terminal único. |

#### Reordenação de prioridade

A Fase B dimensionou a campanha para reduzir a incerteza de $\gamma$. A medição
mostra que **precisão nunca foi o gargalo** — são 148 mil eventos em 20 fibrilas,
e a campanha tem dez vezes isso. O gargalo é faixa de tamanhos, que amostragem
não compra. São coisas diferentes e foram confundidas.

#### Experimento proposto (Fase C)

Cilindro periódico em $y$ com lançamento externo, aberto antes da fratura para o
motor de fratura rodar sem alteração. Ganho: ~2.500 moléculas por seção contra
192 hoje, **ao mesmo custo**, porque o comprimento deixa de consumir massa.
Plano de validação, tolerâncias e previsões em
`Reviews/PhaseC_cilindro_periodico/README.md`.

Experimento barato e independente: alargar o corte até a fibrila inteira deixa a
seção em ~300 em todas as condições e isola arquitetura de tamanho — resolve o
confundimento de N12 apenas reprocessando fibrilas que já estão no cluster.

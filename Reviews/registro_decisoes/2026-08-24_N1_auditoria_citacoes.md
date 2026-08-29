# N1 — auditoria de citações e qualificação física de $T_s$

**Data:** 2026-08-24  
**Origem:** §9 de `DAG_dependencias_revisao.md`, dividida em 2026-08-29.

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

Auditoria de N1 contra as fontes em `Bibliograph/`. Edições cirúrgicas em
`Paper/paper_PRE.tex` e `Carta_Resposta/Response_to_Referees.tex`; ambos
compilam sem citações indefinidas.

#### Princípio adotado

**Corrigir no manuscrito, não narrar na carta.** O revisor não levantou os erros
de citação. Como o texto revisado vai marcado em `\rev`, a correção já é
visível por construção; anunciá-la na carta apenas convidaria R1 — que já
auditou Zapperi/SOC — a reauditar as demais referências. Só se declara erro
próprio quando ele sustentava uma afirmação de que o revisor depende, o que não
é o caso em R1-1.

#### Correções de citação (silenciosas)

1. *"driven by electrostatic forces"* citando `Parkinson1995` e `Kadler1987`.
   Ambas dizem o contrário: montagem entrópica por liberação de água ligada
   (está no título de `Kadler1987`). Corrigido para entrópica na origem,
   modulada eletrostaticamente, com `Jiang2004` e `Morozova2018`.
   Nota: a frase **não** estava marcada em `\rev` no commit `5d2d272`, logo é
   texto original — o revisor a leu e não a comentou.
2. Atribuição de $T_s$: a fonte primária é `Garci1991` (García-Ruiz e Otálora),
   que introduz o tempo de difusão $T_s$; `Parkinson1995` o aplica ao colágeno e
   credita `Garci1991`. Acrescentado ao "Following..." — `Garci1991` já era
   citado no mesmo parágrafo, então o reforço é natural.

#### Qualificação física de $T_s$ (três frases, seção do modelo)

- $T_s$ = tentativas de difusão lateral por evento de deposição ⇒ razão entre
  os tempos de deposição e de salto superficial.
- Limite sequencial justificado pela estimativa de `Parkinson1995` (Appendix):
  na concentração crítica ~0,5 µg/ml, ~10 moléculas por segundo perto o
  bastante para colidir — número da própria fonte, não nosso.
- Direção do mapeamento, antes ausente, como consequência definicional:
  incorporação mais rápida frente à mobilidade ⇒ $T_s$ efetivo menor.

#### Limitação restaurada

O commit `779ee04` apagara a ressalva de regulação celular *in vivo*, sem o
revisor pedir. Restaurada em forma curta com `Kadler1996`, `Canty2005`,
`Kadler2008`.

#### Descartado deliberadamente (fragilidades autoinfligidas)

- **Critério $L_s$ vs. perímetro.** Garci1991 ($L_f>2L_s$) e Parkinson1995
  (saturação quando se explora a circunferência) explicariam nosso platô, mas
  não o testamos, e Parkinson satura em $T_s\approx100$ enquanto nós saturamos
  em $T_s\geq512$. Invocá-lo criaria a pergunta "por que 512?" sem resposta.
  Reconsiderar **apenas** se a medição do perímetro por $T_s$ for feita (N7).
- **"3,6 décadas da razão".** `Parkinson1995` define trial como direção
  sorteada *mesmo se rejeitada*, logo os saltos efetivos não são lineares em
  $T_s$ e a contagem de décadas não é de uma razão física.
- **Exemplo 32 °C/37 °C de `Yang2009`.** Mede diâmetro de fibrila e
  arquitetura de rede, não empacotamento intrafibrilar, que é o que $D_f$ mede.
  A direção foi mantida apenas como consequência definicional do modelo.

#### Pendência

Medir perímetro/raio da seção transversal por $T_s$ e testar o critério
$L_s\sim P$. Pertence ao pipeline de N7.

> **Correção (2026-08-29).** Esta pendência foi registrada como bloqueada por
> ausência das fibrilas brutas nesta máquina. **A afirmação era falsa**: as
> fibrilas publicadas, nas dez condições, estão em
> `Data_fibrils/fibrilas_publicadas_artigo_10Ts_nb30000.zip` (antes
> `Code/Fracture_fibril/compact.zip`). Foi delas que saíram as medições de raio
> da §17. O bloqueio não existe; a medição pode ser feita agora. Ver §18.

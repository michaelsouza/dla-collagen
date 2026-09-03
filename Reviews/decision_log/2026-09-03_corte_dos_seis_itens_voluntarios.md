# Os seis itens voluntários foram cortados

**Data:** 2026-09-03
**Decide:** os seis itens da §13.2 de `Reviews/Respostas_ER12738.qmd` saem, todos
**Cita:** `2026-09-03_intervencao_minima_e_base_congelada.md`, que os enumerou e
deixou a decisão aberta
**Afeta:** as respostas R2-1, R1-2, R1-3, R1-4 e R1-5; a @tbl-plano; a tabela de
figuras e a de inconsistências de `Reviews/Estado_revisao_ER12738.md`
**Desbloqueia:** I6, I13, I14

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## A decisão

Nenhum dos seis itens classificados como **nossos** entra no manuscrito ou na
carta. A classificação de intervenções da §13 fica, na prática, com dois valores:
**pedida** e **forçada**.

| # | Item | Onde estava | Corte |
|:--|:--|:--|:--|
| 1 | recálculo de $D_f$ sob janela uniforme | manuscrito, 138–146, 148–153, 81, 265 | sai; ficam os valores publicados e a Fig. 3 |
| 2 | escada de tamanho e cilindro periódico | manuscrito, 252–257 | sai do artigo, fica na carta |
| 3 | ajuste descritivo com corte esticado | manuscrito, Fig. 8 | sai; nenhuma figura reporta expoente |
| 4 | descritores do esqueleto por $T_s$ | manuscrito, inserção após 185 | sai |
| 5 | validação contra Hemmer & Hansen | carta §2.3 | fica na carta, não sobe para o artigo |
| 6 | números da varredura em $\Delta F$ | carta §2.2 e §2.3 | saem; fica o argumento |

## Por quê

A razão é uma só, e é a da entrada anterior: o artigo volta para os dois
revisores que já demonstraram auditar o que está escrito. Conteúdo que nenhuma
crítica pede não compra resposta e adiciona item examinável. A conta é
assimétrica — o ganho de um argumento extra é marginal, o custo de um erro nele é
uma terceira rodada.

O que esta entrada acrescenta é que **dois dos seis cortes corrigem incoerência,
não apenas encurtam**:

- O item 3 reportava $\gamma$, $s_c$ e $\eta$ numa figura, enquanto a §4.2 e a
  §5.3 do mesmo documento decidem não reportar expoente com menos de uma década
  acima de $s_{\min}$. Cortá-lo põe o manuscrito de acordo com a §5 do
  `AGENTS.md`.
- O item 6 citava, numa carta de resposta, números cujo CSV não está no
  repositório (I14). Cortá-los põe a carta de acordo com a regra de
  rastreabilidade do mesmo parágrafo do `AGENTS.md`.

## O que o corte custou, item por item

**O item 1 é o único caro.** O manuscrito passa a publicar $D_f = 1{,}708 \to
1{,}963$ e o platô em $T_s \ge 512$ sabendo que, sob janela uniforme, os mesmos
dados dão $1{,}90$ em $T_s = 64$, $1{,}95$ em $128$, e o platô se antecipa para
$\approx 128$. Silenciar isso numa crítica que é *sobre a metodologia de $D_f$*
seria omissão, então o corte não é silêncio: o manuscrito ganha uma frase
dizendo que o ajuste tem menos de uma década e que nessa extensão a inclinação
depende da janela escolhida. É o que R1-4 pede — *"discussed as an assumption
with its limitations"* — e é verdade sob qualquer critério de janela.

**O item 1 arrastou a resposta a R1-5, que foi reescrita.** A versão anterior
afirmava que as transições estrutural e mecânica coincidem em $T_s \approx 128$,
e não em 512; a metade estrutural dessa afirmação só existia com o recálculo. A
resposta nova não substitui a coincidência por uma mais precisa: **retira-a.** O
argumento passa a ser que a coincidência do submetido tinha metade mecânica num
platô de $\gamma$ lido sobre faixa inadequada, que não se reporta mais — logo não
resta nada com que $D_f$ coincida. Isso é mais forte do que corrigir o número,
porque é exatamente o que o revisor apontou como excessivo.

**Os itens 2 e 4 custam argumento, não correção.** A refutação do corte por
tamanho finito e os descritores do esqueleto ($\langle N\rangle$ de $50{,}0$ a
$188{,}2$, $\langle K\rangle$ de $25{,}5$ a $50{,}4$, preenchimento até $0{,}94$)
eram bons e ficam fora do artigo, sobrevivendo na carta e no relatório da
campanha. Um leitor do artigo sozinho não os vê.

## Três inconsistências deixam de bloquear

Não por resolução — porque o corte tirou do texto o que dependia delas. Se um
corte for revertido, a inconsistência correspondente volta.

- **I6.** O Spearman de $D_f$ contra os descritores do esqueleto ($0{,}997$;
  $0{,}997$; $-0{,}778$; $-0{,}979$) **não existe no artigo submetido** —
  conferido: zero ocorrências de "Spearman" e zero dos quatro valores em
  `Paper/submitted_ER12738/paper_PRE.tex`. A tabela e a figura de correlações
  existiam só na revisão descartada, e o item 4 as manteve fora. Não há o que
  reconciliar com o CSV.
- **I13.** Os dois critérios de contagem da década ($R_{max}$ dando
  $0{,}57$–$0{,}90$; $R/2$ dando $0{,}38$–$0{,}74$) não precisam ser
  desempatados, porque a frase de limitação diz "menos de uma década", verdade
  sob os dois. Escolher um seria necessário se um número exato entrasse no texto.
- **I14.** O CSV da varredura em $\Delta F$ segue ausente, e agora isso não
  bloqueia nada: a carta não cita mais $92{,}6 \to 188{,}0$ nem p99 $8 \to 89$.

Restam **I7** (o `% TODO Issue #5`, que some ao reescrever R1-2) e **I11** (a
carta cita, em R1-6, o parágrafo de limitações anterior à auditoria N1; o texto
correto está em `179f7ea`).

## O tamanho que sobrou

Vinte e dois blocos mudam no manuscrito, dois ficam como estão, e a única
inserção de parágrafo novo é a da linha 185, que R2-2 pede explicitamente. Das
nove figuras, duas trocam de conteúdo — a 7, cujos ajustes da Eq. (5) não
sobrevivem, e a 9, cujo ajuste de lei de potência foi retirado —, a 8 do
submetido sai com $\Psi$ e a 9 assume seu número. Restam dois conjuntos `.dat` a
exportar para o xmgrace, não três.

# O manuscrito revisado nasce do submetido, sob intervenção mínima

**Data:** 2026-09-03
**Decide:** N13 passa a editar `Paper/submitted_ER12738/paper_PRE.tex`, não
`Paper/paper_PRE.tex`
**Afeta:** N1, N3, N4, N6 (texto), N13, N14; a §1 e a nova §13 de
`Reviews/Respostas_ER12738.qmd`; a seção "Trechos que ainda mudam" de
`Reviews/Estado_revisao_ER12738.md`
**Fecha por não precisar:** I13, se o item 1 da §13.2 for cortado
**Pode fechar:** I14, se o item 6 da §13.2 for cortado

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## A decisão

O manuscrito revisado é construído a partir de uma cópia de
`Paper/submitted_ER12738/paper_PRE.tex`, e recebe apenas as intervenções
listadas na §13 de `Reviews/Respostas_ER12738.qmd`. `Paper/paper_PRE.tex` — a
revisão em andamento, 187 linhas de diff à frente do submetido, com N1, N4 e N6
já escritos e marcados em `\rev{}` — deixa de ser base.

Cada intervenção é classificada em **pedida** (uma crítica pede), **forçada**
(nenhuma crítica pede, mas a linha afirma o que as novas medições refutam) ou
**nossa**. As duas primeiras entram; a terceira é decidida item por item.

## Por quê

**Conteúdo novo é superfície nova para criticar.** Um artigo em segunda rodada
é lido pelos mesmos dois revisores, que já demonstraram auditar o que está
escrito: o Revisor 1 conferiu nossas citações e nos pegou atribuindo SOC a
Zapperi1997a e Zapperi1999, que não o mencionam. Cada parágrafo, número ou
método que entra sem que uma crítica o peça é um item que eles podem examinar e
que não compra resposta nenhuma. A conta é assimétrica: o benefício de um
argumento extra é marginal, o custo de um erro nele é uma terceira rodada.

**A regra é executável, e é por isso que ela vale.** "Alteração mínima" como
intenção não decide nada; como classificação linha a linha, decide. A §13
consolidou as onze tabelas `x.4` em 25 blocos ordenados pela linha da base: 23
mudam, um fica como está, um é inserção nova. Só um deles é inteiramente nosso,
e outros três carregam uma metade nossa. Sem a lista, "mínimo" seria um adjetivo.

## O que a lista revelou, e que as onze tabelas escondiam

**Duas linhas têm mais de um dono.** A linha 250 é apontada por cinco críticas
(R1-3, R1-4, R1-5, R1-7, R2-2) e todas dizem retirar o parágrafo — não há
conflito. Mas a linha 185 recebe três inserções (R2-1, R2-2, R1-4) e a linha 261
recebe quatro instruções (R1-6, R1-1, R1-5, R1-2). Editando crítica a crítica,
esses dois parágrafos seriam reescritos três e quatro vezes. Resolvidos na §13.1:
185 é uma frase alterada mais uma inserção, porque o parágrafo dos dois canais de
R2-2 já contém a leitura de limiar que R2-1 pede; 261 é uma substituição, porque
os dois parágrafos de §11.3 já atendem às quatro instruções.

**Uma incoerência interna.** A §4.2 e a §5.3 decidem não reportar expoente de
lei de potência — menos de uma década acima de $s_{\min}$, o que a §5 do
`AGENTS.md` proíbe afirmar. E a Fig. 8 nova reportava $\gamma$, $s_c$ e $\eta$
do ajuste descritivo. É o item 3 da §13.2.

**Um acoplamento que não estava dito.** A resposta a R1-5 (§8.3) afirma que a
transição estrutural e a mecânica coincidem em $T_s \approx 128$, e não em 512.
A metade estrutural dessa afirmação só existe se $D_f$ for recalculado sob janela
uniforme, que é o item 1 da §13.2 e é conteúdo nosso, não pedido. Cortar o item 1
obriga a reescrever a resposta a R1-5.

## O custo, que é real

**A decisão desescreve N1, N4 e N6.** Esses três nós estavam fechados no
`Estado_revisao` *porque o texto estava em `Paper/paper_PRE.tex`* — N1 em `:137`,
N4 por zero ocorrências de SOC, N6 em `:347`. Descartando o arquivo, as decisões
continuam fechadas e o texto sai. Não se perde: está no commit `179f7ea`, e as
três linhas da tabela de nós agora dizem de onde reaplicá-lo e em que linha da
base ele entra. O mesmo vale para N3, cujo parágrafo dos dois canais foi escrito
na revisão e **não existe no submetido** — a §12.2 afirmava que ele "já afirmava
isso", o que era falso a respeito da base.

E o texto descartado é, em boa parte, exatamente o que a intervenção mínima
pediria: retirar SOC de duas linhas, um parágrafo de fundamentação de $T_s$, dois
de limitações. Reaplicá-lo de `179f7ea` custa pouco; a decisão não é jogá-lo
fora, é deixar de tratá-lo como base.

## O que a regra não alcança

Ela reduz o texto novo do manuscrito, não o da carta. Cinco das onze respostas
exigem contar o que foi medido — Clauset em 50 condições, a varredura em $m$, a
escada de tamanho, as curvas de dano — e encurtar isso seria responder menos.

E há um piso: cinco respostas retiram afirmação do submetido e três substituem
resultado por resultado recalculado sob o protocolo quenched (Figs. 7, 8 e 9).
Esse tamanho não é escolha nossa; é o tamanho do que os revisores acertaram.

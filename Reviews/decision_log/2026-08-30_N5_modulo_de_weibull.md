# N5 — o módulo de Weibull $m$: por que a literatura não pode fixá-lo

**Data:** 2026-08-30
**Fecha:** N5 (crítica R1-3, sensibilidade ao módulo de Weibull)

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## A pergunta

R1-3 pediu análise de sensibilidade a $m$. A carta recusava, citando
Parkinson1997 como justificativa para $m=2$ — e a fonte diz o oposto
(ver `2026-08-24_N5_parkinson_varre_m.md`).

## O que a literatura entrega

Quatro fontes primárias, todas conferidas no PDF em `Bibliography/`. Números
reproduzíveis por `Reviews/N5_weibull_modulus/estimate_m_from_literature.py`.

| Fonte | Objeto | $n$ | $m$ |
|:--|:--|---:|---:|
| Quigley2018 (dados brutos, ajuste MLE nosso) | tendão bovino: flexor / extensor | 38 | 5,5 / 4,4 |
| Svensson2013 (Tabela 3, cinco grupos) | cauda de rato + patelar humano | — | 2,2 a 5,4 |
| Yang2012 (texto) | Aquiles bovino, isolada, em PBS | 11 | 7,2 |
| Yamamoto2017 | cauda de camundongo, 47–310 MPa | 26 | resistência cai com o diâmetro, $R=-0{,}57$ |

**No nível da fibrila, $m$ fica entre 2 e 7, concentrado em 4–5.**

Nenhuma das quatro mede fibrila **reconstituída in vitro**, que é a procedência
do modelo. Para esse objeto não há medida de dispersão de resistência.

## Correção — um erro de segunda mão, e como foi pego

A síntese preliminar afirmava que Yang2012 media fibrilas *reconstituídas in
vitro* com diâmetro controlado em $305\pm10$ nm, e usava isso para tratá-lo como
a fonte mais relevante. **As três afirmações eram falsas.** Vieram da discussão
do Yamamoto2017, não do artigo.

O Yang2012 diz, na seção 2.1: *"a suspension of collagen fibrils was prepared
from bovine Achilles tendon collagen type I (Sigma-Aldrich) by homogenization
and filtration... We therefore use the term **native** collagen fibrils."* São
extraídas de tendão. E o "$305\pm10$ nm" é a legenda de **uma** fibrila, onde o
$\pm10$ é a incerteza da medição, não a dispersão da amostra.

Foi pego por uma pergunta simples — *"temos os artigos salvos aqui?"* — que
expôs que três das cinco estimativas eram de segunda mão. É o mesmo modo de
falha de `2026-08-24_N1_auditoria_citacoes.md`, e o R1 já auditou citações neste
manuscrito. **Nenhum número entra na carta sem estar conferido no PDF primário.**

## A medição que decide

A pergunta certa não é "qual $m$ a literatura indica", e sim "a dispersão que os
experimentos medem consegue distinguir $m$?". Decompus a dispersão de $F_{rup}$
do próprio modelo, em $T_s=128$, 20 fibrilas × 50 realizações por condição:

| $m$ | $F_{rup}$ médio | CV total | CV do sorteio | CV da arquitetura |
|---:|---:|---:|---:|---:|
| 1 | 753 | **0,129** | 0,083 | 0,099 |
| 2 | 1269 | **0,126** | 0,060 | 0,111 |
| 3 | 1546 | **0,125** | 0,048 | 0,116 |
| 5 | 1814 | **0,127** | 0,037 | 0,122 |
| 10 | 2035 | **0,129** | 0,027 | 0,126 |

O CV do sorteio cai com $m$ (aproximadamente $1/\sqrt{m}$); o da arquitetura
sobe, porque limiares uniformes deixam a estrutura decidir sozinha. **Os dois se
compensam: o CV total fica em 0,127 para todos os $m$.**

**Consequência:** a dispersão de resistência *entre fibrilas* — exatamente o que
os experimentos medem — não carrega informação sobre $m$ neste modelo. A
informação está na variação ao repetir **a mesma** fibrila, e não se rompe a
mesma fibrila duas vezes. Nenhum experimento do tipo que existe pode fixar $m$.

Parkinson1997 tinha razão em 1997 e continua tendo; agora sabemos por quê.

## Decisão

**$m = 2$ permanece, com estatuto trocado: de *o valor* para *o caso
ilustrativo* de uma varredura.**

1. Nenhum valor tem apoio empírico — demonstrado acima, não suposto. Trocar 2
   por 4 seria trocar um número sem base por outro.
2. É o extremo mais desordenado da faixa varrida. Conclusões que valem em $m=1$
   e em $m=10$ valem no meio, e já medimos que valem.
3. Continuidade com a linhagem de Parkinson1997 e com o texto já escrito.
4. Trocar exigiria regenerar figuras sem ganho científico.

**Cuidado obrigatório:** $m$ move $F_{rup}$ por um fator 2,7 (753 → 2035), então
figura com eixo de força absoluto muda de escala com $m$. Reportar **força
normalizada**, como Parkinson1997 fez (ver `2026-08-24_N5_parkinson_varre_m.md`).

## Texto para a carta

> Varremos $m$ de 1 a 10. Medidas de tração em fibrila única isolada de tendão
> [Quigley2018; Svensson2013; Yang2012; Yamamoto2017] implicam módulos de Weibull
> entre 2 e 7 no nível da fibrila; para fibrilas reconstituídas in vitro, que é o
> objeto do modelo, não há medida equivalente. Mostramos ainda que a dispersão de
> resistência entre fibrilas é insensível a $m$ no modelo, de modo que esse tipo
> de medida não poderia fixá-lo. As conclusões são estáveis em toda a faixa
> varrida.

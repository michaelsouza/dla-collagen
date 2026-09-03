# Correção: as fontes não reportam módulo de Weibull; nós o derivamos

**Data:** 2026-09-03
**Corrige:** a tabela da seção "O que a literatura entrega" de
`2026-08-30_N5_modulo_de_weibull.md`
**Afeta:** N5, N11; a resposta R1-3 em `Reviews/Respostas_ER12738.qmd`
**Abre:** I12 (registrada como resolvida no mesmo dia)

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## O que estava errado

A entrada de 2026-08-30 traz a tabela abaixo sob o título "O que a literatura
entrega", com a coluna final rotulada $m$:

| Fonte | Objeto | $n$ | $m$ |
|:--|:--|---:|---:|
| Quigley2018 (dados brutos, ajuste MLE nosso) | tendão bovino: flexor / extensor | 38 | 5,5 / 4,4 |
| Svensson2013 (Tabela 3, cinco grupos) | cauda de rato + patelar humano | — | 2,2 a 5,4 |
| Yang2012 (texto) | Aquiles bovino, isolada, em PBS | 11 | 7,2 |

Só a primeira linha diz de onde vem o número. As outras duas **parecem valores
reportados pelas fontes, e não são.** Nenhuma das duas reporta módulo de
Weibull:

- **Yang2012 não contém a palavra "Weibull" uma única vez** (conferido em
  `Bibliography/Yang2012.md`, contagem zero). O que ele traz, na seção 3.2, é
  *"The failure of all tested native collagen fibrils (n = 11) occurred at
  11%–15% strain with a stress at break of 60 ± 10 MPa"*. O $7{,}2$ é
  $1{,}2/\mathrm{CV} = 1{,}2/(10/60)$, calculado por nós.
- **Svensson2013** entra pela mesma rota: médias e desvios da Tabela 3, cada um
  convertido por $m \approx 1{,}2/\mathrm{CV}$.

O dado de entrada está certo — o $60 \pm 10$ MPa foi conferido no PDF primário,
como o cabeçalho de `estimate_m_from_literature.py` exige. O erro é de
**atribuição**, não de medição.

## Onde o erro chegou, e onde não chegou

**Não chegou ao script.** `Reviews/N5_weibull_modulus/estimate_m_from_literature.py`
sempre separou os dois estimadores em blocos rotulados — "A · média±DP
reportados (aproximação CV)" e "B · Quigley2018, valores individuais (máxima
verossimilhança)". A saída dele é honesta. **Foi a prosa que fundiu os dois.**

**Chegou ao documento de respostas**, na decisão e na resposta de R1-3, esta
última em forma de frase que iria para a carta:

> …because literature estimates of the Weibull modulus in single collagen
> fibrils range between 2 and 7 (Svensson et al. 2013; Yang et al. 2012;
> Quigley et al. 2018)…

Corrigido hoje em `Reviews/Respostas_ER12738.qmd`: a resposta agora distingue o
ajuste de máxima verossimilhança (só Quigley2018, $n=38$) da derivação por
$m \approx 1{,}2/\mathrm{CV}$ (Svensson2013 e Yang2012), diz que nenhum módulo
de Weibull foi reportado para fibrila única, e acrescenta a ressalva que decide
o escopo: nenhuma dessas medições é de fibrila **reconstituída in vitro**, que é
a procedência do modelo, então $m$ é varrido e não calibrado.

## Por que isto importa mais do que parece

É a **terceira** vez que Yang2012 é lido de segunda mão neste projeto. A §
"Correção" de `2026-08-30_N5_modulo_de_weibull.md` documenta as duas primeiras:
a síntese preliminar afirmava que ele media fibrilas reconstituídas in vitro com
diâmetro controlado em $305 \pm 10$ nm, e as três afirmações eram falsas, vindas
da discussão do Yamamoto2017.

E o alvo era a carta. O Revisor 1 **já auditou nossas citações** e nos pegou
citando Zapperi1997a e Zapperi1999 para SOC quando as duas não mencionam SOC.
Uma frase atribuindo módulos de Weibull a duas fontes que não os reportam é
exatamente o convite para ele repetir o exercício — e desta vez com razão.

## O que decorre

- **A regra do `AGENTS.md` §5 vale para a derivação, não só para a citação.**
  "Ao citar uma fonte, abra a fonte" pegou os erros de conteúdo. Este era de
  tipo diferente: a fonte foi aberta, o número dela está certo, e ainda assim a
  frase mente sobre o que ela reporta. O teste que pega isso é: *a fonte usa
  esta palavra?* Para "Weibull" em Yang2012, a resposta é não.
- **Todo número derivado carrega o estimador no nome.** Na rastreabilidade de
  R1-3, as duas rotas agora são linhas separadas, uma dizendo "por máxima
  verossimilhança" e a outra "derivado da dispersão por
  $m \approx 1{,}2/\mathrm{CV}$, não reportado pelas fontes".
- **N5 não muda de estado.** A conclusão da entrada de 2026-08-30 — que a
  literatura não fixa $m$ e que a dispersão medida não o distingue — fica de
  pé, e na verdade fica mais forte: se nem módulo de Weibull há para fibrila
  única, menos ainda há para fibrila reconstituída.

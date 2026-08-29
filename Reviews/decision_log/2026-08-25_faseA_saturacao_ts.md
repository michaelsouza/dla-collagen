# Fase A — a grade de $T_s$ não pode ser reduzida

**Data:** 2026-08-25  
**Origem:** §14 de `DAG_dependencias_revisao.md`, dividida em 2026-08-29.

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

Detalhes e dados em `Reviews/PhaseA_ts_saturation/`.

**Pergunta:** se a difusão superficial cobre todo o componente acessível, mais
$T_s$ não muda nada, e com `-coverstop` o gerador para de consumir
aleatoriedade — então duas condições acima da cobertura dariam fibrilas
bit-idênticas, permitindo eliminá-las da campanha.

**Resposta: não.** Em `nb=30000`, a cobertura vai de 0% ($T_s=2$) a 82,9%
($T_s=8192$), sem atingir 100% em nenhuma condição. Com 17% das moléculas ainda
esgotando o orçamento no topo da grade, nenhum par de condições é idêntico.
**A grade permanece com as 10 condições publicadas.**

Três achados colaterais:

1. **A cobertura depende do tamanho.** Em `nb=2000` a cobertura em $T_s=8192$ é
   99,8%; em `nb=30000` cai para 82,9% — o componente cresce com o perímetro e
   o tempo de cobertura de um passeio aleatório vai com $O(n^2)$. Qualquer
   argumento de saturação por cobertura é dependente do tamanho.
2. **A cobertura não explica o platô onde o artigo o situa.** Em $T_s=512$ só
   9,8% das moléculas cobriram.
3. **Os $D_f$ publicados dependem de uma janela de ajuste por condição.**
   Tentei medir $D_f$ com janela comum para testar a saturação; validado contra
   as fibrilas publicadas, o cálculo falhou (1,83/1,93/1,93 contra
   1,708/1,790/1,965). A causa é geométrica: o raio da fibrila cai de ~33 para
   ~14 ao longo da grade, então nenhuma janela fixa serve às duas pontas. É por
   isso que `validate_fractal_proxy.py` lê a janela de um projeto xmgrace por
   $T_s$. **A afirmação de saturação de $D_f$ não pode ser separada dessa
   escolha de janela sem reanálise** — pendência de N7, não da Fase A.

#### Correção de registro

Uma leitura preliminar em `nb=2000` sugeria cobertura de 99,8% em $T_s=8192$ e
foi comunicada como confirmação da hipótese de saturação. A medição em escala de
produção reduz isso a 82,9% e a conclusão não se sustenta na forma forte. O que
sobrevive é o mecanismo qualitativo (cobertura cresce com $T_s$ e satura o
efeito da difusão) e a constatação de que ele é dependente do tamanho.

#### Estado dos itens do plano

| Item | Estado |
|:--|:--|
| A1 — teste de identidade por cobertura | executado; **não dispara** — grade mantida |
| A2 — estatística de cobertura | executado; tabela arquivada |
| C1 — escritor no esquema legado | **concluído** (`31e8dfe`), parser aceita |
| N7 — janela de ajuste de $D_f$ | **nova pendência** identificada aqui |

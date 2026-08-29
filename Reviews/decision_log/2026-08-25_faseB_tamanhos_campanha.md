# Fase B — tamanhos da campanha, medidos

**Data:** 2026-08-25  
**Origem:** §16 de `DAG_dependencias_revisao.md`, dividida em 2026-08-29.

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

Piloto no SDumont2: 10 $T_s$ × 20 fibrilas × 50 realizações, $m=2$, protocolo
quenched. 10.000 realizações, 1.619.315 eventos. Relatório completo em
`$DLA_PROJECT/pilot/convergence.json`.

#### Realizações por fibrila: 50, não 100

O ICC medido é **0,19–0,35**, ou seja $\sigma^2_{dentro}\approx3\sigma^2_{entre}$.
A regra $n_{real}\geq10(1-\rho)/\rho$ dá 19 a 43 conforme a condição; a pior é
$T_s=8192$ com 43.

**Decisão: $n_{real}=50$.** Fica acima do pior caso com margem, e corta a
campanha de fratura pela metade frente às 100 do plano.

Nota sobre a leitura do ICC: um ICC baixo significa que a variância *dentro* da
fibrila domina, o oposto do que eu supunha ao argumentar que mais fibrilas
sempre batem mais realizações. O argumento de orçamento fixo continua válido
para estimar médias, mas a cauda precisa de eventos, e eventos vêm de
realizações — é essa tensão que fixa $n_{real}$ em 50 em vez de 1.

#### Fibrilas por condição: 200 confirmado

Com 20 fibrilas, SE($\gamma$) fica entre 0,027 e 0,060 (mediana 0,040), contra o
alvo de 0,020 do plano. Como SE $\propto 1/\sqrt{n_{fib}}$:

| $T_s$ | SE com 20 | fibrilas p/ SE=0,02 |
|---:|---:|---:|
| 2 | 0,0344 | 59 |
| 8 | 0,0601 | **180** |
| 16 | 0,0559 | 156 |
| 32 | 0,0380 | 72 |
| 64 | 0,0298 | 44 |
| 128 | 0,0411 | 84 |
| 512 | 0,0540 | 146 |
| 1024 | 0,0411 | 84 |
| 4096 | 0,0274 | 38 |
| 8192 | 0,0339 | 57 |

O teto de 200 do plano cobre a pior condição ($T_s=8$, 180). **O número não era
chute — agora está justificado por medição.** A parada sequencial da §B2 permite
encerrar $T_s=4096$ com ~38 fibrilas e $T_s=8$ só em 180.

O SE relativo da média já está em 0,8–3,5%, bem abaixo do alvo de 5%.

#### Custo de produção, com números medidos

- fratura: 9,2 s por realização (16 min para 50 itens × 50 realizações em 24 núcleos);
- memória: MaxRSS 4,2 GB por tarefa de 24 processos, ~175 MB por processo;
- geração: 10,6 min-núcleo por fibrila.

Campanha: 10 $T_s$ × 200 fibrilas × 50 realizações × 5 valores de $m$ =
500.000 realizações ≈ **1278 CPU-h**, metade do estimado no plano.

#### Valores de $\gamma$ — provisórios, não usar

O piloto reporta $\gamma$ subindo de 2,10 ($T_s=2$) a ~2,85 ($T_s=64$) e
estabilizando em 2,74–2,85 para $T_s\geq64$. **Não são os valores do artigo:**
o estimador da Fase B é um Hill discreto com $s_{\min}=5$ fixo, escolhido para
estudar dispersão, não para estimar a cauda. A estimativa definitiva sai de N10,
com seleção objetiva de $s_{\min}$ e comparação de famílias.

O que se pode dizer é estrutural: existe platô, e ele começa bem antes de
$T_s=512$.

#### Obstáculo operacional em aberto

Cinco submissões mostraram que **apenas os índices 0 e 1 de cada array rodam**;
com 4 tarefas, as de índice 2 e 3 sempre falham em `launch failed requeued held`.
Com 2 tarefas, nunca falha. Não há limite por nó na configuração
(`MaxCPUsPerNode=UNLIMITED`, `MaxTRESPerNode` vazio) e havia 344 núcleos livres.
**Causa desconhecida.**

Isso inviabiliza o plano de 40 tarefas × 48 núcleos: sobrariam 96 núcleos e a
fratura levaria ~27 h em vez de ~1,3 h. A saída a testar antes da produção são
**vários arrays independentes de 2 tarefas**, para verificar se o padrão é por
array.

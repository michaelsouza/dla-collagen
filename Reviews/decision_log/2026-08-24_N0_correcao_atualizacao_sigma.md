# N0 — correção da atualização de $\sigma$

**Data:** 2026-08-24  
**Origem:** §10 de `DAG_dependencias_revisao.md`, dividida em 2026-08-29.

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

#### O defeito

`Rod.prob_break` usava o sinalizador `updated` como porta de correção. Ele só
era limpo quando a **vizinhança da própria haste** mudava
(`Particle.innactive` → `Rod.del_neigh_pid`). Mas uma haste perde área de seção
transversal quando **qualquer** molécula que compartilha uma de suas camadas é
removida, vizinha ou não. Nesses casos `update_force` apenas reescalava o
$\sigma_M$ antigo por $F/F_{old}$.

Consequência: $\sigma_M$ ficava **sistematicamente abaixo** do exato $F/N(i)$,
em 99% das hastes, crescendo com o dano acumulado ($T_s=128$):

| $F$ | desvio médio | p05 | fração subestimada |
|---:|---:|---:|---:|
| 20 | −0,01% | −0,0% | 84% |
| 100 | −2,60% | −10,6% | 99% |
| 160 | −9,02% | −25,5% | 99% |

Com $m=2$, isso subestima $P_R$ em ~17% em carga alta.

#### Por que é um defeito, e não uma escolha de modelagem

Parkinson et al. 1997, o protocolo de referência que o artigo cita, é explícito
(`Bibliograph/Parkinson1997.md:84`): *"After the rods had been assessed and the
appropriate particles removed, the skeleton was reassessed and **the stress
re-evaluated**."* Sem elasticidade, essa reavaliação **é** o passo de relaxação
da linhagem de fratura desordenada que ele invoca
(`Parkinson1997.md:41`). O cache omitia parte dele.

#### Impacto medido (código antigo vs. recomputação exata, pareado)

| $T_s$ | $F_{rup}$ | nº avalanches | média | p99 | máx |
|---:|---:|---:|---:|---:|---:|
| 2 | −27,8% | −32,1% | −7,5% | +11,8% | −21,3% |
| 128 | −14,9% | −20,8% | −15,3% | −33,3% | −61,3% |
| 8192 | −13,5% | −19,3% | +3,1% | −9,0% | −14,3% |

Robusto: força de ruptura e número de avalanches caem em todos os regimes.
Não robusto: o efeito sobre a distribuição de tamanhos varia em sinal e
magnitude; 1 fibrila e 10–12 realizações não bastam para caracterizá-lo.
A ordenação em $T_s$ sobrevive nas duas versões.

#### A correção

`Code/Fracture_fibril/stress_strain_ava.py`:

1. `prob_break` sempre recalcula $\sigma$ (o sinalizador `updated` deixa de ser
   porta de correção);
2. `update_sigma` calcula $\sigma_M = F\langle 1/N(i)\rangle$ diretamente —
   isso também conserta um caso de borda em que $K=0$ fazia `update_force`
   retornar antes de aplicar o reescalonamento por $F$;
3. `layer_ids()` memoiza a lista de camadas da haste, que é constante enquanto
   a haste está ativa.

#### Verificação

- Auditoria de $\sigma$ reexecutada: desvio cai de $\sim10^{-2}$ para
  $\sim10^{-16}$ em todas as forças.
- Dois testes de regressão novos em `test_stress_strain_ava.py`;
  confirmado que **falham** em `HEAD` (código antigo dá $\sigma=2{,}5$ onde o
  exato é $3{,}33$). Suíte: 4/4.
- O código corrigido reproduz **dígito a dígito** a referência independente
  calculada antes com o código antigo + recomputação forçada
  ($F_{rup}=149{,}20833\ldots$, 1455 avalanches, média $4{,}410309\ldots$).
- Sem custo de desempenho: 138,4 s contra 138,6 s do código antigo, porque a
  memoização compensa o recálculo. A variante ingênua levava 204 s.

#### Pendências

- Recomputar toda a mecânica: Figs. 8, 9, 10, $\alpha$, $\beta$, e a Issue #5
  inteira. Estimativa: 10 $T_s$ × 50 fibrilas × 1000 realizações ≈ 500 mil
  realizações × ~7 s ≈ 40 CPU-dias.
- Antes disso, medir o efeito sobre $\gamma$ e $s_c$ especificamente: se a
  cauda for insensível, a Issue #5 sobrevive e só as Figs. 8 e 10 mudam.
- As medições de N2 (sensibilidade a $\Delta F$ e ao critério de parada) foram
  feitas com o código antigo e precisam ser refeitas.

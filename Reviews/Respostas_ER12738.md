# Respostas aos revisores — ER12738

**Base:** `Paper/submitted_ER12738/paper_PRE.tex` (o que os revisores leram; as
linhas citadas abaixo são desse arquivo e não se movem).
**Destino:** `Carta_Resposta/Response_to_Referees.tex` (N14) e as intervenções
mínimas no manuscrito (N13).
**Estado:** rascunho em construção — ver a tabela no fim.

Cada crítica tem quatro blocos. **A crítica**, literal. **A decisão**, em
português, com o nó e o registro que a sustenta. **A resposta**, em inglês,
já no texto que vai para a carta. **Rastreabilidade**: cada número com sua
origem, e as linhas do submetido que a resposta obriga a mudar — essa lista é
o que N13 executa, e nada entra no manuscrito fora dela.

Ordem de escrita: R2-1 e R2-3 primeiro, porque definem limiar, cascata e
avalanche, que todas as outras respostas usam.

---

## R2-1 — Loading protocol and stability of the system

### A crítica

> My main concern is the loading protocol. Equation (4) defines the probability
> of failure. As long as fibers carry load, this probability remains finite.
> This seems to imply that, at any finite load, the bundle would fail after a
> finite time, with a characteristic time depending on the load level. The
> authors state that during a sweep through the system, each fiber is given a
> chance to fail according to Eq. (4), and if no failure occurs, the external
> load is increased. This procedure appears somewhat artificial. If I
> understand the model correctly, the bundle is not fully relaxed after a
> sweep: failure could continue in a subsequent sweep at the same load level.
> Moreover, fiber removal increases $\sigma_M$ and decreases $K$, both of which
> increase the rupture probability $P_R$. Thus, the system does not seem to be
> in a stable state when the external load is further increased. The authors
> should clarify this point in the manuscript.

### A decisão

O revisor está certo, e a objeção **não se responde — dissolve-se**. Testamos
a preocupação dele antes de decidir: com o código corrigido (N0), a regra
recozida não tem limite quase-estático — $F_{rup}$ é linear em $\log\Delta F$
(92,6 → 188,0 para $\Delta F$ de 0,0625 a 2,0) e o p99 das avalanches vai de
8 a 89. A estatística era propriedade do $\Delta F$, não da fibrila.

Adotamos o protocolo padrão de fiber bundle com desordem congelada (registro
`decision_log/2026-08-24_adocao_protocolo_quenched.md`, nó N2): cada molécula
sorteia uma vez uma resistência $X_i$ com $P(X \le x) = x^m$; o limiar é
$\sigma^{th}_i = K_i \sigma_c X_i$ — **a mesma expressão da Eq. (4)**, lida
como distribuição de resistência em vez de probabilidade por varredura. A
força sobe exatamente até o menor $F^*_i = K_i \sigma_c X_i / a_i$; a cascata a
$F$ fixo é determinística e termina sozinha. Não há $\Delta F$, varredura nem
critério de parada, então não há "estado não relaxado" a que aumentar a carga.

O que a mudança preserva: a regra de carga uniforme por seção (Eqs. 2–3), a
resistência proporcional à coordenação (N3), o corpo de prova, o esqueleto
ativo e o critério de ruptura. O que ela muda nos resultados: **todos os
números mecânicos** do submetido (Figs. 7–9) foram refeitos sob o protocolo
novo, com 200 fibrilas × 50 realizações por condição e $m \in \{1,2,3,5,10\}$.

### A resposta

We thank the Referee for this observation, which identifies a genuine defect
of the original loading rule. We tested the concern directly. With the removal
rule of Eq. (4) applied in sweeps at fixed force, the rupture force and the
avalanche statistics depend on the force increment $\Delta F$ without
approaching a limit: over five octaves of $\Delta F$ (0.0625 to 2.0), the mean
rupture force grows approximately linearly with $\log \Delta F$ (from 92.6 to
188.0) and the 99th percentile of the avalanche size grows from 8 to 89. The
original protocol therefore measured a property of the loading schedule rather
than of the fibril, exactly as the Referee suspected: a sweep with no removals
does not establish a stable state, and further sweeps at the same force would
continue to remove molecules.

We have replaced the protocol by the standard quasi-static fiber-bundle
scheme with quenched disorder, keeping the physical content of Eq. (4). Each
molecule $i$ draws once, before loading, a strength variable $X_i \in [0,1]$
with cumulative distribution $P(X \le x) = x^m$, and fails when its mean
stress exceeds the threshold $\sigma^{\mathrm{th}}_i = K_i \sigma_c X_i$, where
$K_i$ is its current coordination. Under this rule the probability that a
molecule with coordination $K_i$ fails at stress $\sigma$ is
$(\sigma / K_i \sigma_c)^m$, which is Eq. (4) reinterpreted as a strength
distribution; the coordination-dependent weakening channel of the original
model is preserved. Because $\sigma_{M,i} = F a_i$ with
$a_i = \langle 1/N(l) \rangle$ over the cross-sections spanned by the molecule,
each molecule has a well-defined failure force $F^*_i = K_i \sigma_c X_i / a_i$.
The external force is raised continuously to the smallest $F^*_i$ in the
system; at that fixed force, every molecule whose threshold is exceeded is
removed, loads and coordinations are recomputed, molecules that lost their
connection to both ends are removed, and the cascade is repeated until no
molecule is above threshold. The cascade terminates deterministically. There
is no force increment, no sweep, and no stopping criterion, so the state
reached before each increase of the force is stable by construction: every
remaining molecule satisfies $F^*_i > F$.

The new protocol was validated against the exactly solvable case: fed with an
equal-load-sharing bundle with uniformly distributed thresholds, the same
cascade engine reproduces the burst distribution $D(s) \sim s^{-5/2}$ of
Hemmer and Hansen, with deviations below 2% up to $s = 8$ in a run of 150
bundles of 4000 fibers. The model description, Fig. 6, and all mechanical
results (Figs. 7–9 and the associated text) have been rewritten and recomputed
under this protocol, with 200 independent fibrils and 50 rupture realizations
per fibril for each value of $T_s$, and for five values of the Weibull modulus,
$m \in \{1, 2, 3, 5, 10\}$. The model no longer has a physical time or a dwell
time at fixed load, and we do not interpret it as describing creep, fatigue,
or delayed rupture.

### Rastreabilidade

| número | origem |
|:--|:--|
| $F_{rup}$ 92,6 → 188,0; p99 8 → 89 para $\Delta F$ 0,0625 → 2,0 | `decision_log/2026-08-24_adocao_protocolo_quenched.md` — **CSV da varredura a localizar antes de ir para a carta** |
| desvio < 2% até $s=8$, 150 × 4000, contra Hemmer & Hansen | idem; teste em `Code/Fracture_fibril/test_fiber_bundle_ava.py` |
| 200 fibrilas × 50 realizações × 5 $m$ por $T_s$; 10.000 arquivos | `decision_log/2026-08-29_faixa_dinamica_avalanches.md` |
| protocolo implementado | `Code/Fracture_fibril/fiber_bundle_ava.py` |

Linhas do submetido que mudam:

| linha | trecho | intervenção |
|:--|:--|:--|
| 185 | "The corresponding failure threshold is $K\sigma_c$ …" | acrescentar a variável $X_i$ e a leitura de limiar |
| 187–193 | Eq. (4) e "Here, we set $m=2$ …" | reescrever como distribuição de resistência; $m$ como parâmetro varrido (com N5) |
| 202 | "For a given force $F$, we evaluate $P_R$ … increased by $\Delta F = 0.5$ …" | substituir pelo parágrafo de carga extremal e cascata |
| 207 | legenda da Fig. 6 (a) "removal probability … random number $u$" | adaptar ao limiar |
| 211 | "ensemble of $10$ distinct fibrils … $10^3$ independent rupture simulations" | 200 fibrilas × 50 realizações; cinco valores de $m$ |

---

## R2-3 — Definition of avalanches

### A crítica

> Since load sharing according to Eq. (2) is global within a cross section, it
> seems that no particular stress concentration can develop around failed
> (removed) fibers in that cross section. If this interpretation is correct,
> then the definition of avalanches may require further justification. If the
> stress field is not localized around failed clusters, it is not obvious why
> avalanches should be defined as steps in the growth of connected failed
> clusters. An alternative, and possibly more natural, definition would be to
> regard an avalanche as the set of fibers that fail between two consecutive
> increments of the external force. The authors should make this aspect of the
> work clearer.

### A decisão

Adotamos a definição do revisor, e sob o protocolo novo ela deixa de ser uma
escolha: **a cascata a $F$ fixo é a avalanche** (N8 dissolvido, registro
`2026-08-25_consolidacao_da_dag.md`). Ela inclui as moléculas que passaram do
limiar e as que perderam o caminho de carga em consequência, porque as duas
coisas acontecem na mesma resposta ao mesmo aumento de força — é a unidade
causal, e é o que "avalanche" significa na literatura de fiber bundle. A
decomposição em aglomerados conexos fica nos dados como diagnóstico de
localização (12% a 25% das cascatas se partem em mais de um aglomerado), mas
sai do manuscrito como observável primário; com ela saem $\Psi$ e a Fig. 8 do
submetido. A cascata terminal — uma por realização, que leva 77% a 88% do
sistema — é excluída da distribuição.

### A resposta

We agree with the Referee, and we have adopted the definition suggested. Under
the quasi-static protocol described in our response to Point 1, the external
force is raised only until the next molecule reaches its threshold, and at
that fixed force a deterministic cascade follows: molecules above threshold
are removed, loads and coordinations are updated, molecules that lost their
load path are removed, and the cycle repeats until the configuration is
stable. The avalanche is the total number of molecules removed in one such
cascade, irrespective of their spatial arrangement. This is the set of fibers
that fail between two consecutive increases of the external force, and it is
the standard avalanche of fiber-bundle models. It contains no free parameter:
its extent is fixed by the model, not by a force increment or by a
connectivity criterion.

The Referee's reasoning about the stress field is correct for our model. The
stress released by a removed molecule is shared uniformly among the molecules
that remain in the cross-sections it occupied (Eq. 2), and the only local
effect of a removal is the loss of one contact for each of its neighbors,
which lowers their thresholds through $K$. Spatially disconnected removals in
the same cascade are nevertheless causally linked, because each was triggered
by the same force increase or by the redistribution that followed; partitioning
a cascade into connected clusters would discard that link. We therefore no
longer use the connected cluster as the avalanche. The quantity $\Psi$ and the
former Fig. 8, which were built on the cluster definition, have been removed.
The decomposition of cascades into connected clusters remains available as a
diagnostic of damage localization — between 12% and 25% of the cascades,
depending on $T_s$ and $m$, consist of more than one connected cluster — but
it is not used in the statistical analysis.

The final cascade of each realization, which eliminates the last continuous
load path and removes the remainder of the backbone in one event (between 77%
and 88% of the molecules, depending on the condition), is a single terminal
event and not part of the preterminal avalanche process; it is excluded from
the distributions analyzed in the revised Section on avalanche statistics.

### Rastreabilidade

| número | origem |
|:--|:--|
| 12% a 25% das cascatas com mais de um aglomerado | `Reviews/quenched_campaign_report/README.md` §5.1 |
| cascata terminal leva 77% a 88% do sistema | `decision_log/2026-08-29_faixa_dinamica_avalanches.md`; confirmado em `2026-09-02_confirmacao_secoes_inteiras.md` (0,87–0,88) |
| extração da cascata como observável | `Code/Data_analysis/extract_cascades.py` |

Linhas do submetido que mudam:

| linha | trecho | intervenção |
|:--|:--|:--|
| 230 | "We define a cluster as any group of two or more adjacent molecules … $\Psi$ … Fig. 8" | substituir pela definição de cascata; retirar $\Psi$ |
| 233–238 | Fig. 8 ($\Psi$ contra $F_n$) | retirar a figura; renumerar 9 → 8 |
| 240 | "we define the avalanche size, $s$, as the cluster size" | tamanho da cascata; excluir a terminal |

---

## Estado do documento

| Crítica | Nó | Resposta | Insumos prontos? |
|:--|:--|:--|:--|
| R2-1 | N2 | rascunho acima | sim; falta localizar o CSV da varredura em $\Delta F$ |
| R2-3 | N2/N8 | rascunho acima | sim |
| R1-2 | N4, N10 | a escrever | sim — relatório §5.2–5.4, registros de 2026-09-02 |
| R1-3 | N5, N11 | a escrever | sim — relatório §5.4 (tabela de $\gamma$ por $m$) |
| R2-4 | N4, N10 | a escrever | sim — junto com R1-2 |
| R1-4 | N7 | a escrever | sim — `Reviews/N7_fractal_proxy/df_published_fibrils_by_window.csv` (medido 2026-09-03), relatório §4, cilindro largo |
| R1-5 | N12 | a escrever | sim — relatório §6, Fase C |
| R1-1 | N1 | reaproveitar a carta atual | sim |
| R1-6 | N6 | reaproveitar a carta atual | sim |
| R2-2 | N3 | reaproveitar a carta atual, vocabulário de limiar | sim |
| R1-7 | N9 | a escrever | **não** — espera `extract_damage_curves.py` rodar no cluster |

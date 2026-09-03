# Respostas aos revisores — ER12738

**Base:** `Paper/submitted_ER12738/paper_PRE.tex` (o que os revisores leram; as
linhas citadas abaixo são desse arquivo e não se movem).
**Destino:** `Carta_Resposta/Response_to_Referees.tex` (N14) e as intervenções
mínimas no manuscrito (N13).
**Estado:** rascunho completo para revisão de Michael — ver a tabela no fim.

Cada crítica tem quatro blocos. **A crítica**, literal. **A decisão**, em
português, com o nó e o registro que a sustenta. **A resposta**, em inglês,
já no texto que vai para a carta. **Rastreabilidade**: cada número com sua
origem, e as linhas do submetido que a resposta obriga a mudar — essa lista é
o que N13 executa, e nada entra no manuscrito fora dela.

Ordem: R2-1 e R2-3 primeiro, porque definem limiar, cascata e avalanche;
depois a estatística (R1-2, R1-3, R2-4), a estrutura (R1-4), a associação
(R1-5), a curva de dano (R1-7); por fim as três que só reaproveitam texto.

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
| $F_{rup}$ 92,6 → 188,0; p99 8 → 89 para $\Delta F$ 0,0625 → 2,0 | `decision_log/2026-08-24_adocao_protocolo_quenched.md` — **CSV da varredura não está no repositório; localizar ou retirar os números da carta** |
| desvio < 2% até $s=8$, 150 × 4000, contra Hemmer & Hansen | idem; teste em `Code/Fracture_fibril/test_fiber_bundle_ava.py` |
| 200 fibrilas × 50 realizações × 5 $m$ por $T_s$ | `Reviews/N9_damage_curves/damage_summary.csv` (10.000 realizações em cada uma das 50 condições) |
| protocolo implementado | `Code/Fracture_fibril/fiber_bundle_ava.py` |

Linhas do submetido que mudam:

| linha | trecho | intervenção |
|:--|:--|:--|
| 185 | "The corresponding failure threshold is $K\sigma_c$ …" | acrescentar a variável $X_i$ e a leitura de limiar |
| 187–193 | Eq. (4) e "Here, we set $m=2$ …" | reescrever como distribuição de resistência; $m$ como parâmetro varrido (com R1-3) |
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
submetido. A cascata terminal — uma por realização, que leva 66% a 91% do
sistema conforme a condição — é excluída da distribuição.

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
load path and removes the remainder of the backbone in one event (between 66%
and 91% of the molecules, depending on $T_s$ and $m$), is a single terminal
event and not part of the preterminal avalanche process; it is excluded from
the distributions analyzed in the revised Section on avalanche statistics.

### Rastreabilidade

| número | origem |
|:--|:--|
| 12% a 25% das cascatas com mais de um aglomerado | `Reviews/quenched_campaign_report/README.md` §5.1 |
| cascata terminal leva 66% a 91% do sistema | `Reviews/N9_damage_curves/damage_summary.csv`, coluna `terminal_fraction_mean` (0,658 em $T_s=2$, $m=1$; 0,911 em $T_s=64$, $m=10$) |
| extração da cascata como observável | `Code/Data_analysis/extract_cascades.py` |

Linhas do submetido que mudam:

| linha | trecho | intervenção |
|:--|:--|:--|
| 230 | "We define a cluster as any group of two or more adjacent molecules … $\Psi$ … Fig. 8" | substituir pela definição de cascata; retirar $\Psi$ |
| 233–238 | Fig. 8 ($\Psi$ contra $F_n$) | retirar a figura; renumerar 9 → 8 |
| 240 | "we define the avalanche size, $s$, as the cluster size" | tamanho da cascata; excluir a terminal |

---

## R1-2 — Attribution of Self-Organized Criticality; statistical validation

### A crítica

> The authors claim that the rupture process exhibits SOC on the basis that the
> avalanche size distribution follows a power law. This reasoning is
> insufficient. SOC requires that a system spontaneously evolves toward a
> critical state without external tuning of a control parameter, the canonical
> example being the Bak-Tang-Wiesenfeld sandpile. In the present model, the
> external force $F$ is continuously increased by the experimenter until failure
> occurs. The system is driven, not self-organizing.
>
> Critically, two of the papers the authors themselves cite to support the SOC
> claim (refs. [42] and [43], Zapperi et al., PRL 1997 and PRE 1999) make no
> reference to SOC. Instead, Zapperi et al. explicitly characterize the
> breakdown point as a first-order transition and draw an analogy with spinodal
> nucleation, a fundamentally different phenomenology. The correct terminology
> for the dynamics observed here is "avalanche statistics in driven disordered
> fracture," not SOC.
>
> Furthermore, the power-law regime in Fig. 9(a) spans at most two orders of
> magnitude in avalanche size, a marginal range. No statistical validation of
> the power-law hypothesis is presented (e.g., maximum likelihood estimation of
> the exponent, Kolmogorov-Smirnov test, or comparison with alternative
> distributions following the methodology of Clauset et al., SIAM Review 51,
> 661, 2009). The claim of scale-free behavior therefore rests on
> insufficiently rigorous grounds.

### A decisão

Duas metades. **SOC** (N4, fechado): o termo sai de todo o manuscrito, e a
resposta é positiva, não concessiva — o que substitui SOC é uma medição, não
um recuo. **Estatística** (N10): aplicamos o procedimento de Clauset às
cascatas preterminais das 50 condições e o resultado é que **a lei de
potência pura é rejeitada em 48 de 50**; a distribuição tem corte intrínseco,
e três invariâncias medidas dizem que o corte é do modelo — não muda com
$m$, não muda com $T_s$ acima de 16, e não muda quando o corpo de prova tem
25 vezes mais moléculas (Fase C, N17). A faixa útil acima de $s_{min}$ é de
menos de uma década; por isso **não se reporta expoente** como resultado, e
sim a forma da distribuição (registros `2026-08-29_faixa_dinamica_avalanches.md`,
`2026-09-02_corte_das_avalanches_e_dinamico.md`, `2026-09-02_confirmacao_secoes_inteiras.md`;
relatório §5.2–5.4). O controle de percolação da carta atual sai: ele
defendia a recuperação de um expoente que já não afirmamos.

### A resposta

We agree with the Referee on both points and have revised the manuscript
accordingly.

*Terminology.* The process is externally driven and irreversible, and the
avalanche statistics do not by themselves indicate self-organization. We have
removed every reference to Self-Organized Criticality from the abstract,
introduction, results, and conclusion, and we now describe the process as
avalanche dynamics in driven disordered fracture. We also thank the Referee
for pointing out that Refs. [42] and [43] do not support the original claim;
those citations have been corrected.

*Statistical analysis.* Under the revised protocol (Points 1 and 3 of the
Second Referee), we analyzed the raw, integer-valued sizes of all preterminal
cascades — $6.1 \times 10^7$ events over ten values of $T_s$ and five values
of the Weibull modulus $m$, i.e. fifty conditions with 200 fibrils and 50
realizations each — following Clauset, Shalizi and Newman. For each condition
the lower threshold $s_{\min}$ was selected by minimizing the discrete
Kolmogorov–Smirnov distance, the exponent was estimated by exact discrete
maximum likelihood, the pure power law was tested by a semiparametric
goodness-of-fit with 2500 synthetic replicas, and it was compared with the
four alternatives of Clauset et al. by normalized likelihood ratios. The pure
power law is rejected ($p < 0.1$) in 48 of the 50 conditions; in 47 of them no
synthetic replica reached the observed KS distance. It loses the likelihood
comparison against the lognormal and the stretched exponential in 49 of 50
conditions. The distributions therefore have an intrinsic cutoff, and we no
longer describe the process as scale-free.

The cutoff is a property of the model, not of the sample. Three measurements
establish this. First, the shape of the distribution is insensitive to the
disorder: across $m = 1$ to $10$ at fixed geometry, the fraction of
single-molecule cascades stays between 0.72 and 0.76 and the 99th percentile
of the cascade size between 8 and 20. Second, it is insensitive to the
architecture above $T_s \approx 16$: the survival functions for $T_s = 16$,
128, 1024 and 8192 nearly coincide, and the fitted cutoff scale stabilizes
(for $m=2$, $s_c \approx 51$ from $T_s = 128$ onward). Third, and most
important, it is insensitive to the system size. Fracturing one wide fibril
through cross-sections of $17\times17$, $41\times41$, $81\times81$ and
$181\times181$ lattice units — from 2,400 to 60,000 molecules, a factor of 25
— leaves the fraction of unit cascades (0.74–0.76), the 90th percentile (2–3)
and the 99th percentile (9–11) unchanged; the same holds for a compact
architecture ($T_s = 8192$, $17\times17$ against $141\times141$). A finite-size
cutoff would have moved with the sample; this one does not.

Because the range of cascade sizes above $s_{\min}$ spans less than one decade
in every condition — about 72% of the preterminal cascades have size one, the
99th percentile is about 12, and the largest preterminal cascade is of order
90 — we do not report a power-law exponent as a result of this work, nor
compare one with theoretical values. What the data support, and what the
revised manuscript states, is the shape of the distribution: a heavy body
dominated by single-molecule events, a cutoff at a few tens of molecules that
is fixed by the model, and a single terminal cascade that removes most of the
backbone. Among the parametric families we tested, the one that describes the
body and the cutoff region best is a power law with a stretched-exponential
cutoff, $p(s) \propto s^{-\gamma}\exp[-(s/s_c)^{\eta}]$, which gives the
smallest KS distance in 34 of the 50 conditions; we use it only as a
descriptive fit, and the revised Fig. 8 shows the empirical survival functions
together with it. The fitted $\eta$ varies between 1.1 and 5.2 across the
grid, which is one more reason not to read any of these parameters as a
universal exponent.

### Rastreabilidade

| número | origem |
|:--|:--|
| $6{,}1\times10^7$ cascatas preterminais; 50 condições | relatório §5, Figura 5.1 (61 000 717) |
| lei pura rejeitada 48/50; 47 com $p=0$; perde para log-normal e esticada em 49/50 | relatório §5.2; `$DLA_PROJECT/campaign/analysis/cascades/cascade_stats_clauset.csv` |
| fração unitária 0,72–0,76; p99 8–20 em $m$ | `2026-08-29_faixa_dinamica_avalanches.md` (item 3); `Reviews/PhaseC_periodic_cylinder/avalanche_ladder_ts128.csv` |
| colapso acima de $T_s=16$; $s_c\approx51$ ($m=2$) de 128 em diante | relatório §5.3, Figura 5.2, e tabela de $s_c$ em §5.4 |
| escada de tamanho 17×17 → 181×181; $T_s=8192$ 17×17 → 141×141 | `2026-09-02_confirmacao_secoes_inteiras.md`; `avalanche_ladder_ts128.csv`, `avalanche_ladder_ts8192.csv` |
| 72% tamanho 1; p99 = 12; máxima ~90 | `2026-08-29_faixa_dinamica_avalanches.md` (item 2) |
| Araújo melhor KS em 34/50; $\eta$ 1,13–5,19 | relatório §5.3–5.4; `Reviews/quenched_campaign_report/fig5-1_araujo_ajustes.csv` |

Linhas do submetido que mudam:

| linha | trecho | intervenção |
|:--|:--|:--|
| 81 | resumo: "a hallmark of Self-Organized Criticality (SOC) … lacks a characteristic scale … crossing the mean-field … universality" | reescrever a segunda metade do resumo |
| 100 | intro: "characteristic of Self-Organized Criticality (SOC)" | retirar |
| 240 | "from the viewpoint of avalanche statistics~\cite{Bak1987}" | trocar a citação; definição de cascata (R2-3) |
| 242–248 | Eq. (6) e "$\gamma = 2.31 \pm 0.05$ … $2.80 \pm 0.04$ … plateau for $T_s \geq 512$" | substituir pelo parágrafo da forma da distribuição e das três invariâncias |
| 252–257 | Fig. 9 e legenda | figura nova: sobrevivência por $T_s$ ($m=2$) e a escada de tamanho |
| 261 | "rupture follows scale-free avalanche dynamics" | retirar |
| 265 | conclusão: "remains scale-free, $P(s)\sim s^{-\gamma}$ … $\gamma=2.31$ … $2.80$ … plateau" | reescrever |

---

## R1-3 — Interpretation of $\gamma > 5/2$; Weibull modulus; ensemble size

### A crítica

> The authors interpret their measured exponent $\gamma \approx 2.8$ (at high
> $T_s$) as evidence of a regime beyond equal load sharing (ELS), signaling a
> crossover to global load-sharing universality. This interpretation is
> incorrect. In fiber bundle models, $\gamma = 5/2$ is the exact mean-field
> result for ELS, the limiting case of maximally global stress redistribution
> (Hemmer & Hansen 1992; Daniels 1945). There is no established theoretical
> framework that predicts or interprets exponents above $5/2$ in this context.
> Moreover, Pradhan, Hansen & Chakrabarti (2010) demonstrate that within ELS,
> the avalanche exponent undergoes a crossover from $\gamma = 5/2$ to
> $\gamma = 3/2$ near the critical breakdown point. That is, as stress
> redistribution becomes maximally global near rupture, the exponent
> DECREASES, not increases. […] The observed deviation from $5/2$ is more
> plausibly attributable to finite-size effects, limited ensemble statistics
> (10 fibrils per $T_s$ value), the restricted range over which the power law
> is fitted, or the specific definition of avalanche adopted in the model. A
> sensitivity analysis with respect to the Weibull modulus $m$ (fixed at $m = 2$
> throughout, following ref. [35]) would also help assess the robustness of
> the exponents.

### A decisão

Concordamos, e o revisor acertou também no diagnóstico: das quatro causas que
ele lista, **três estão confirmadas** — a definição de avalanche (R2-3), a
faixa restrita de ajuste (menos de uma década) e a estatística de 10 fibrilas.
Só o efeito de tamanho finito foi testado e descartado (Fase C). A varredura
em $m$ que ele pediu foi feita, $m \in \{1,2,3,5,10\}$ (N5, registro
`2026-08-30_N5_modulo_de_weibull.md`), e é o argumento mais forte de todos:
em geometria fixa, o expoente efetivo vai de 2,83 ($m=1$) a 1,91 ($m=10$) —
$\gamma$ depende da desordem tanto quanto da arquitetura, então nenhum valor
dele identifica uma classe de universalidade. O 5/2 cai entre $m=1$ e $m=2$,
e escolher o $m$ que o cruza seria ajuste a posteriori. **N11 encerra como
não-afirmação**: a comparação com 5/2 sai do manuscrito. O que fica em
$m$: a literatura de fibrila única dá $m$ entre 2 e 7 (Quigley2018 5,5/4,4;
Svensson2013 2,2–5,4; Yang2012 7,2); reportamos a grade inteira e usamos
$m=2$ como caso ilustrativo, para comparação com Parkinson1997.

### A resposta

We thank the Referee and agree. The comparison of the fitted slope with the
equal-load-sharing value $5/2$, and its interpretation as a crossover toward
global load sharing, were not justified and have been removed from the
manuscript. Of the four explanations the Referee proposes for the deviation
from $5/2$, three turned out to be correct: the avalanche definition (see our
response to Point 3 of the Second Referee), the restricted fitting range, and
the ensemble size. The fourth, finite size, we tested and excluded (see Point
2 above): the distribution does not change when the specimen is enlarged by a
factor of 25 in the number of molecules.

We performed the sensitivity analysis with respect to the Weibull modulus
that the Referee requested, over $m \in \{1, 2, 3, 5, 10\}$, for every value
of $T_s$, with 200 fibrils and 50 realizations per condition. The result
settles the question. At fixed geometry the effective tail exponent of the
descriptive fit depends strongly on $m$: for the most compact fibrils
($T_s = 8192$) it decreases from $2.83 \pm 0.01$ at $m = 1$ to $2.45 \pm 0.01$
at $m = 2$, $2.19 \pm 0.02$ at $m = 3$, $1.98 \pm 0.03$ at $m = 5$ and
$1.91 \pm 0.01$ at $m = 10$; for the most open fibrils ($T_s = 2$) it ranges
from $1.87$ to $2.06$. Narrower disorder (larger $m$) produces heavier tails,
as expected when many thresholds lie close together and fail in the same
cascade. The value $5/2$ falls between $m = 1$ and $m = 2$ in the compact
regime, but selecting the value of $m$ that reproduces a theoretical exponent
would be an a posteriori adjustment, and we do not do it. An exponent that
depends on the disorder as much as on the architecture cannot identify a
load-sharing universality class, and the revised manuscript makes no such
identification. Since the range of cascade sizes spans less than one decade
in every condition, we also do not present these exponents as results; the
manuscript reports the shape of the distribution and its invariances instead.

Two further points support this reading. Our model is not an
equal-load-sharing bundle: its failure threshold
$F^*_i = K_i \sigma_c X_i / a_i$ contains a global channel, through the
occupancy of the cross-sections spanned by the molecule ($a_i$), and a local
one, through the number of active neighbors ($K_i$). And the same cascade
engine, when fed an equal-load-sharing bundle with uniform thresholds, does
recover the Hemmer–Hansen exponent $5/2$ (Point 1 of the Second Referee), so
the departure from $5/2$ in the fibrils is a property of their structure and
disorder, not of the estimator.

Regarding $m$ itself, measurements of the strength dispersion of individual
collagen fibrils give Weibull moduli between about 2 and 7 (Svensson et al.
2013; Yang et al. 2012; a maximum-likelihood fit to the raw data of Quigley et
al. 2018 gives 4.4–5.5). Our grid covers this range. We retain $m = 2$ as the
illustrative case in the figures, for continuity with Parkinson et al., and
report the full dependence on $m$ in the revised Fig. 8. Finally, the
ensemble has been enlarged from 10 fibrils and $10^3$ realizations per
$T_s$ to 200 fibrils and 50 realizations per fibril for each $(T_s, m)$.

### Rastreabilidade

| número | origem |
|:--|:--|
| $\gamma$ por $(T_s, m)$: 2,830±0,005 … 1,912±0,013 em 8192; 1,874–2,055 em 2 | relatório §5.4, tabela de $\gamma$; `fig5-1_araujo_ajustes.csv` |
| motor reproduz 5/2 em ELS uniforme | `Code/Fracture_fibril/test_fiber_bundle_ava.py`; `2026-08-24_adocao_protocolo_quenched.md` |
| $m$ na literatura: 5,5/4,4 (Quigley2018, MLE nosso), 2,2–5,4 (Svensson2013, Tab. 3), 7,2 (Yang2012) | `2026-08-30_N5_modulo_de_weibull.md`; `Reviews/N5_weibull_modulus/estimate_m_from_literature.py` — **conferir Yang2012 no PDF**: o registro avisa que houve erro de segunda mão nesse artigo |
| fator 25 em $N$ | `2026-09-02_confirmacao_secoes_inteiras.md` |

Linhas do submetido que mudam:

| linha | trecho | intervenção |
|:--|:--|:--|
| 193 | "Here, we set $m = 2$ following …" | $m$ varrido em $\{1,2,3,5,10\}$; $m=2$ ilustrativo |
| 211 | "ensemble of $10$ distinct fibrils … $10^3$" | 200 × 50 por $(T_s,m)$ |
| 248 | valores de $\gamma$ e platô | sai (com R1-2) |
| 250 | parágrafo "crossover from local to global load sharing … $\kappa_{\mathrm{eff}}$ … change in universality class" | retirar inteiro |
| 269 | conclusão: parágrafo do 5/2, LLS→GLS | retirar inteiro |

---

## R2-4 — Power-law statistics and SOC

### A crítica

> The interpretation of power-law statistics in terms of self-organized
> criticality should be treated with caution. In rupture processes the system
> is gradually destroyed, and there is no healing mechanism by which failed
> fibers could recover and carry load again. Therefore, the analogy with
> self-organized critical systems may be problematic unless it is carefully
> qualified. I suggest that the authors either provide a more detailed
> justification for this interpretation or reformulate the discussion in more
> cautious terms.

### A decisão

Mesma resposta de R1-2, curta: SOC sai; o que entra é a medição de que a
distribuição tem corte intrínseco e o processo termina num evento terminal
único — o oposto de um estado crítico mantido.

### A resposta

We agree, and we have removed the interpretation in terms of self-organized
criticality throughout. The Referee's argument is in fact borne out by the
data: with no healing, the process does not maintain a critical state — the
preterminal cascade-size distribution has an intrinsic cutoff at a few tens
of molecules that does not move with the specimen size, and every realization
ends in a single terminal cascade that removes 66% to 91% of the backbone at
once. The revised manuscript describes this as avalanche dynamics during
progressive damage in a driven disordered system, with the statistical
analysis detailed in our response to Point 2 of the First Referee.

### Rastreabilidade

Os mesmos itens de R1-2; a fração terminal vem de
`Reviews/N9_damage_curves/damage_summary.csv`. Linhas: as de R1-2.

---

## R1-4 — Cross-sectional fractal dimension and the 3D mechanical problem

### A crítica

> $D_f$ is estimated from 2D cross-sectional projections ($x$-$z$ plane), yet
> the backbone identification and the entire fracture simulation are
> three-dimensional. The relationship between the 2D cross-sectional $D_f$ and
> the 3D structural properties that govern mechanical response is not
> established. The authors use the 2D $D_f$ as a proxy for overall fibril
> compactness without justification. This connection should either be derived
> or explicitly discussed as an assumption with its limitations.

### A decisão

A carta atual (commit `521a284`) respondia com a Fig. 7 nova — quatro
correlações de Spearman entre $D_f$ e descritores do backbone — e concluía
"validação numérica direta do proxy". **N7 concluiu o contrário** e a resposta
inverte de sinal (relatório §4; registros `2026-08-30_diametro_e_dimensao_fractal.md`,
`2026-09-01_dimensao_fractal_cilindro_largo.md`; medição de hoje em
`Reviews/N7_fractal_proxy/df_published_fibrils_by_window.csv`):

1. O $D_f$ publicado é **escolha de janela**. As fibrilas têm raio de 15 a 40
   unidades de rede; o intervalo utilizável de um ajuste massa–raio tem 0,4 a
   0,7 década. Os ajustes publicados usaram janelas escolhidas condição a
   condição (`ensemble_curve_validation.csv` os reproduz exatamente); sob
   qualquer regra uniforme, as mesmas fibrilas dão 1,90–1,95 em $T_s = 64$ e
   128, onde o artigo publicou 1,76 e 1,79. O platô vai de $T_s \approx 512$
   para $\approx 128$.
2. A seção **deixa de ser fractal**. Num cilindro periódico 17× mais gordo,
   $T_s = 2$ dá $1{,}675 \pm 0{,}023$ sobre 1,5 década — DLA plano, medido de
   verdade; $T_s = 8192$ dá $1{,}955 \pm 0{,}012$; e em $T_s = 128$ não há
   patamar de inclinação local (1,93 → 0,48 do centro para a borda): é um
   miolo compacto com casca. Os valores intermediários publicados são um
   *crossover* geométrico entre duas fases, não uma dimensão que varia.
3. Logo $D_f$ **não é** o descritor mecânico. O que entra na fratura é a área
   portante $N(l)$ e a coordenação $K$ — e essas são medidas diretamente no
   backbone 3D. A Fig. 7 de correlações sai (com ela, I6 fecha por remoção); a
   Fig. 3 é refeita sob regra uniforme; e o texto passa a dizer: agregado DLA
   em $T_s$ baixo, sólido compacto a partir de $T_s \approx 128$, e a
   compactação medida por $\langle N\rangle$, $\langle K\rangle$ e fração de
   preenchimento.

### A resposta

We thank the Referee for this criticism, which led us to re-examine the
fractal analysis itself, and we have changed both the analysis and the role
that $D_f$ plays in the paper.

*What the original $D_f$ measured.* The cross-sections of the simulated
fibrils have radii between 15 and 40 lattice units, so a mass–radius fit has
between 0.4 and 0.7 decades of usable range between the lattice cutoff and
the edge of the object. In the original analysis the fitting window was
chosen for each $T_s$ separately. When the same 550 cross-sections per
$T_s$ are refitted under a single objective rule — a fixed window
$4 \le r \le 8$, or a window proportional to the fibril radius,
$0.15R \le r \le 0.5R$ — the two rules agree with each other and disagree
with the original values in the middle of the range: for $T_s = 64$ and 128
they give $D_f = 1.90$–$1.95$ where the submitted manuscript reported 1.76
and 1.79. The local slope of the mass–radius curve is not constant in these
conditions, so the fitted value is a property of the window, and the plateau
of $D_f$ begins near $T_s \approx 128$ rather than at 512.

*What the cross-section is.* To measure $D_f$ over a genuine range of scales
we generated fibrils on a cylinder with periodic boundary conditions along
the axis, in which every added molecule widens the cross-section instead of
lengthening the fibril; their local structure (coordination and contact
geometry) agrees with that of the ordinary fibrils within 2%, and their radii
reach 70–160 lattice units. Over 1.5 decades, the $T_s = 2$ cross-section
gives $D_f = 1.675 \pm 0.023$, the value of a two-dimensional
diffusion-limited aggregate; the $T_s = 8192$ cross-section gives
$1.955 \pm 0.012$; and at $T_s = 128$ the local slope decreases monotonically
from 1.93 at the center to below 1 at the edge, with no plateau. The
intermediate cross-sections are therefore not self-similar objects with an
intermediate dimension: they are a compact core surrounded by an open rim.
Increasing $T_s$ shrinks the range of scales over which the DLA structure
exists until it disappears, and the cross-section becomes compact. The
revised Fig. 3 shows $D_f$ under the uniform window rule together with the
local-slope diagnostic, and the text describes the transition as a crossover
between two regimes — a fractal aggregate at low $T_s$ and a compact,
space-filling cross-section from $T_s \approx 128$ — rather than as a
continuously varying fractal dimension.

*Its role in the mechanical analysis.* We agree that a two-dimensional
fractal dimension is not the quantity that governs the three-dimensional
rupture model, and the revised manuscript no longer uses it as a proxy. The
quantities that enter the model are the load-bearing area of each
cross-section, $N(l)$, and the coordination of each molecule, $K$; both are
measured directly on the three-dimensional backbone, and we now report their
ensemble values with $T_s$: the mean load-bearing area of the specimen grows
from 50 to 188 molecular segments per cross-section and the mean coordination
from 25.5 to 50.4 between $T_s = 2$ and 8192, with most of the change
completed by $T_s \approx 128$; the filling fraction of the cross-section
keeps rising slowly to 0.94 at $T_s = 8192$. The correlation between $D_f$
and these descriptors, which we had considered presenting, adds nothing to
them: within a fixed specimen window the load-bearing area is a function of
the packing density by construction, and the mechanical results are discussed
in terms of the backbone descriptors themselves.

### Rastreabilidade

| número | origem |
|:--|:--|
| raios 15–40 u.r.; 0,4–0,7 década | `2026-08-30_diametro_e_dimensao_fractal.md` §4 (0,57–0,90 com o $R_{max}$ do manuscrito); relatório §4 (0,38–0,74 com $R/2$) — **harmonizar os dois critérios antes da carta** |
| ajustes publicados reproduzidos com janela por condição | `Reviews/N7_fractal_proxy/ensemble_curve_validation.csv` |
| 1,90–1,95 em $T_s=64$ e 128 sob regra uniforme (fibrilas publicadas) | `Reviews/N7_fractal_proxy/df_published_fibrils_by_window.csv` (abs_4_8: 1,903/1,952; rel: 1,921/1,954) |
| cilindro largo: 1,675±0,023 (1,5 década), 1,955±0,012, inclinação 1,93→0,48; estrutura local dentro de 2% | `2026-09-01_dimensao_fractal_cilindro_largo.md`; `Reviews/PhaseC_periodic_cylinder/df_wide_cylinders.csv`, `df_local_slopes_wide.csv` |
| $\langle N\rangle$ 50,0 → 188,2; $\langle K\rangle$ 25,5 → 50,4 | `Reviews/N7_fractal_proxy/condition_descriptor_summary.csv` (fibrilas publicadas, 50 por $T_s$) |
| preenchimento 0,82 (512) → 0,94 (8192) | relatório §3.2 e §6 |

Linhas do submetido que mudam:

| linha | trecho | intervenção |
|:--|:--|:--|
| 81 | resumo: "systematic evolution of the fibril's fractal dimension" | *crossover* de agregado fractal a seção compacta |
| 129 | "higher local packing density implies a greater number of intermolecular contacts … enhanced connectivity" | manter; é o que se mede agora em $\langle K\rangle$ |
| 138–146 | método de $D_f$ ("from $R_{min}=5$ to $R_{max}$") e "rises and saturates at $D_f=1.963$" | descrever a regra uniforme e a inclinação local; valores novos; platô em ≈128 |
| 148–153 | Fig. 3 e legenda | figura nova a partir de `df_published_fibrils_by_window.csv` e `df_published_mass_radius_curves.csv` |
| 250 | "$\rho(R)\sim R^{D_f-2}$ … approach $D_f\to2$" | sai com o parágrafo (R1-3) |
| 265 | conclusão: "rises from $D_f=1.708$ … to $1.963$" | reescrever com a leitura de *crossover* |
| — | descritores do backbone | **inserir** um parágrafo curto com $\langle N\rangle$, $\langle K\rangle$ e preenchimento por $T_s$, depois da definição de $K$ (linha 185) |

---

## R1-5 — The structural–mechanical connection is purely empirical

### A crítica

> The key result of the paper, that $D_f$ and $\gamma$ saturate together at
> $T_s \geq 512$, is presented as if it were a derived causal relationship. In
> fact, it is a numerical correlation observed in simulation. No theoretical
> framework is provided that connects the fractal dimension of the fibril
> cross-section to the avalanche exponent of the fracture process. The
> statement that "the fibril's fractal dimension serves as a quantitative
> bridge between structural compactness and failure statistics" (Conclusion)
> overstates what has been demonstrated. The authors should reframe this as an
> empirical observation and discuss what theoretical framework might, in the
> future, explain such a connection.

### A decisão

A relação sobrevive, mas no nível mais fraco (N12; relatório §6; registros
de 2026-09-02). Não existe função $\gamma(D_f)$: em geometria fixa $\gamma$
varia com $m$ de 2,83 a 1,91; $D_f$ satura em $T_s \approx 128$ enquanto o
preenchimento segue subindo, então a relação não é invertível; e o mecanismo
de fratura lê coordenação e ocupação, não autossimilaridade. A ponte de Araújo
(expoente de avalanche ↔ dimensão do esqueleto) não transfere: daria
$d_B = 0{,}70$–$1{,}07$, impossível (§5.5). O que fica é uma **assinatura
comum**: quatro grandezas independentes — razão de densidade, $D_f$ sob janela
uniforme, correlação de pares e o parâmetro de cauda — mudam de regime na
mesma faixa, $T_s \approx 128$; o diâmetro só para de encolher em 512 e o
preenchimento não satura na grade. A Fase C desfez o confundimento de tamanho
(25× em $N$ não move a estatística), então a associação é entre arquiteturas,
não entre tamanhos de corpo de prova. "Quantitative bridge" sai. O teste por
fibrila que a issue #8 pede fica como extensão: precisa do cluster e não muda
a resposta.

### A resposta

We agree with the Referee: the coincident evolution of the cross-sectional
structure and the avalanche statistics is an empirical observation within the
model, and the sentence describing $D_f$ as a "quantitative bridge" between
compactness and failure statistics has been removed. The revised results and
conclusion describe the observation, its limits, and what it does and does not
imply.

*What is observed.* Four independent quantities change regime in the same
range of $T_s$: the radial density contrast of the cross-section, the fractal
dimension measured under a uniform rule, the pair correlation of the packing,
and the tail parameters of the preterminal cascade distribution all stabilize
near $T_s \approx 128$. The fibril diameter stops shrinking only at
$T_s \approx 512$, and the filling fraction of the cross-section is still
rising at $T_s = 8192$. Losing the fractal regime and completing the
compaction are therefore not the same event, and the revised manuscript
reports the transition at $T_s \approx 128$ rather than the plateau at 512 of
the submitted version.

*Why it is not a relation between $D_f$ and $\gamma$.* Three facts prevent
reading the observation as a functional dependence of the avalanche
statistics on the fractal dimension. First, at fixed geometry the effective
tail exponent varies with the disorder parameter $m$ over a range (from
$2.83$ to $1.91$ at $T_s = 8192$) wider than its variation with $T_s$ at fixed
$m$; the avalanche statistics depend on the architecture and on the disorder,
$D_f$ on the architecture only. Second, $D_f$ saturates at $T_s \approx 128$
while the local packing continues to change, so several architectures with
the same $D_f$ have different mechanical responses. Third, the ingredients of
the rupture model are the load-bearing area and the coordination, which are
what the compaction changes; the fractal dimension is a description of the
low-$T_s$ cross-section, not a variable the mechanics can see. We also
examined whether the relation of Araújo et al. between the avalanche exponent
and the fractal dimension of a percolation backbone could provide the
theoretical framework the Referee asks for; it cannot, because the implied
backbone dimensions ($0.7$–$1.1$) are unphysical — that relation concerns a
static geometric object, while the cascades here are dynamic events of a
loading process.

*What it is not an artifact of.* Because the number of molecules in the
specimen varies together with $T_s$ (by a factor of 3.9 across the grid), we
checked whether the association could be a specimen-size effect. It is not:
fracturing the same wide fibril through cross-sections from $17\times17$ to
$181\times181$ lattice units, a factor of 25 in the number of molecules,
leaves the cascade statistics unchanged.

*Toward a framework.* A predictive connection would have to propagate the
architecture — cross-sectional heterogeneity of the load-bearing area and the
coordination field — into the stress redistribution and the cascade
statistics. Within the present model the natural variables for such a
connection are $\langle N \rangle$, its axial variation, and $\langle K
\rangle$, and the natural control variable of the mechanics is the disorder
$m$; a fractal dimension does not appear in it. A continuum treatment with
elastic force transmission would be needed to go beyond the empirical
statement, and we identify this as future work.

### Rastreabilidade

| número | origem |
|:--|:--|
| quatro observáveis mudam em ≈128; diâmetro em 512; preenchimento não satura | relatório §6 (tabela) |
| $\gamma$ 2,83 → 1,91 em $T_s=8192$ com $m$ | relatório §5.4 |
| Araújo: $d_B$ implícito 0,70–1,07; 40/50 com $d_B<1$ | relatório §5.5 |
| $N$ varia 3,9× com $T_s$; 25× não move a estatística | `2026-08-29_faixa_dinamica_avalanches.md`; `2026-09-02_confirmacao_secoes_inteiras.md` |

Linhas do submetido que mudam:

| linha | trecho | intervenção |
|:--|:--|:--|
| 250 | "the saturation of $\gamma$ for $T_s \ge 512$ coincides with $D_f \gtrsim 1.90$ …" | sai com o parágrafo |
| 261 | "the fibril's fractal dimension serves as a quantitative bridge …" | retirar; frase de associação empírica |
| 265–267 | conclusão: "plateau for $T_s\ge512$ that coincides with $D_f\gtrsim1.90$"; "joint increase of $D_f$ and $\gamma$ … crossover in the effective universality class" | reescrever: assinatura comum em ≈128, sem $\gamma(D_f)$ |

---

## R1-7 — The phenomenological damage function $f(F)$

### A crítica

> The phenomenological function $f(F)$ in Eq. (5) is purely empirical. Its
> form is not derived from the model and the physical interpretation of the
> parameters $\alpha$ and $\beta$, while discussed qualitatively, would benefit
> from more precise justification.

### A decisão

Medido hoje sobre as 50 condições (N9; `Reviews/N9_damage_curves/`,
job 590854 em `cpu_amd`): **a Eq. (5) não descreve a curva de dano do
protocolo novo.** O termo exponencial some — ajustado sobre a curva média,
$\beta$ vem negativo ou nulo e o erro é de 0,09 a 0,25 em $\varphi$. O que os
dados mostram é simples: o dano preterminal cresce quase linearmente com $F$
(lei de potência com $\alpha$ entre 0,7 e 1,35 sobre as realizações ainda
inteiras, erro < 0,02) até só **9% a 34%** do esqueleto, e então **uma cascata
terminal** leva o resto. A subida "exponencial" perto da ruptura na curva
média é a distribuição de $F_{rup}$ entre realizações (CV de 0,12 a 0,29),
não um mecanismo de amplificação de dano. Portanto: a Eq. (5), $\alpha$ e
$\beta$ saem; entram $F_{rup}$ por $T_s$ e $m$, a fração preterminal, e a
curva $\varphi(F/F_{rup})$, que colapsa acima de $T_s \approx 32$. O que o
submetido dizia sobre a força de ruptura crescer com $T_s$ **se mantém e
fica mais forte**: $F_{rup}$ sobe 10× de $T_s=2$ a 8192 (para $m=2$), 83%
disso até $T_s = 128$; por molécula do esqueleto, 2,6× — o efeito da
coordenação.

### A resposta

We thank the Referee. We agree that Eq. (5) was not derived from the model,
and under the revised loading protocol the question resolved itself: the
function no longer describes the data, and we have removed it together with
the parameters $\alpha$ and $\beta$.

Under quasi-static loading with quenched thresholds, the damage curve has a
different structure from the one the exponential term was meant to capture.
The fraction of molecules removed before rupture grows nearly linearly with
the applied force — over the realizations that are still intact, a power law
$\varphi \propto F^{\alpha}$ with $\alpha$ between 0.7 and 1.35 describes the
mean curve with a root-mean-square error below 0.02 in every condition — and
reaches only 9% to 34% of the backbone, depending on $T_s$ and $m$; the rest
is removed by the single terminal cascade. When the mean is taken over all
realizations, including those already broken, the curve rises steeply toward
unity near the mean rupture force, but this rise is the distribution of
rupture forces across realizations (coefficient of variation 0.12 to 0.29),
not an acceleration of damage within a fibril. Fitting Eq. (5) to that curve
gives a vanishing or negative $\beta$ and errors of 0.1 to 0.25 in $\varphi$.
There is therefore no late-stage amplification regime for $\beta$ to
parameterize, and no separate low-force regime for $\alpha$.

The revised Section reports what the protocol measures directly. The rupture
force increases monotonically with $T_s$ — for $m = 2$, from $151 \pm 36$ at
$T_s = 2$ to $1532 \pm 218$ at $T_s = 8192$, with 83% of the increase
completed by $T_s = 128$ — and with the disorder parameter, from $903$ at
$m = 1$ to $2495$ at $m = 10$ for the most compact fibrils. Per molecule of
the load-bearing backbone the rupture force grows by a factor of 2.6 between
the most open and the most compact fibrils, which is the direct mechanical
expression of the higher coordination of compact packings. The preterminal
damage fraction decreases from 22% to 12% (for $m = 2$) over the same range,
and the damage curves expressed against $F/F_{\mathrm{rup}}$ collapse for
$T_s \gtrsim 32$. The revised Fig. 7 shows the rupture force against $T_s$
for the five values of $m$ and the collapsed damage curves; the quantities
plotted have direct definitions in the model and require no phenomenological
form.

### Rastreabilidade

| número | origem |
|:--|:--|
| $\beta \le 0$, erro 0,09–0,25; lei de potência $\alpha$ 0,73–1,35, erro < 0,02 | `Reviews/N9_damage_curves/damage_condition_table.csv` (colunas `eq5_all_*`, `power_intact_*`) |
| fração preterminal 9%–34% | idem, `phi_preterminal` (0,342 em $T_s=2$, $m=1$; 0,089 em $T_s=64$, $m=10$) |
| $F_{rup}$ 150,6±35,9 → 1532,4±217,5 ($m=2$); 903 → 2495 em 8192 com $m$; CV 0,12–0,29 | `damage_summary.csv` |
| 83% da subida até $T_s=128$: $(1299-151)/(1532-151)$ | idem |
| por molécula 0,25 → 0,66 (2,6×) | `damage_condition_table.csv`, `f_rup_per_rod` |
| colapso de $\varphi(F/F_{rup})$: $\varphi(0{,}9)$ = 0,178 (2), 0,102 (32), 0,098 (128), 0,100 (8192) | idem, `phi_u090`; curvas em `damage_ts<TS>_m<M>_curve_norm.csv` |
| extração e tabela | `Code/Data_analysis/extract_damage_curves.py`, `summarize_damage_curves.py`; job 590854, SDumont2 `cpu_amd` |

Linhas do submetido que mudam:

| linha | trecho | intervenção |
|:--|:--|:--|
| 213–221 | $\varphi(F)$, "common functional form", Eq. (5), interpretação de $\alpha$ e $\beta$ | substituir pelo parágrafo de $F_{rup}$, fração preterminal e colapso |
| 223–228 | Fig. 7 (ajustes de Eq. 5; $\alpha$, $\beta$ contra $T_s$) | figura nova: $F_{rup}(T_s)$ por $m$; $\varphi$ contra $F/F_{rup}$ |
| 250 | "stabilization of the fit parameters $\alpha$ and $\beta$" | sai com o parágrafo |
| 265 | conclusão: "saturation of the damage-related parameters $\alpha$ and $\beta$" | retirar |

---

## R1-1 — Physical grounding of $T_s$ (reaproveita)

**Decisão:** N1 fechado; a resposta da carta atual vale, e o texto já existe
em `Paper/paper_PRE.tex:137` (razão deposição/salto; estimativa de
Parkinson1995 de ~10 moléculas por segundo) e `:349` (limitação: calibrar
$T_s$ exige escalas de tempo independentes; a fibrilogênese in vivo é
organizada pela célula). A especulação sobre enfisema e aneurisma sai.

**Resposta:** a de `Carta_Resposta/Response_to_Referees.tex`, Point 1, sem
alteração de conteúdo. Conferir em N14 que as duas citações literais batem
com o `.tex` final.

Linhas do submetido: 118 (inserir o trecho de `:137` do atual); 261 (inserir a
limitação, adaptada de `:349`); 271 (retirar "We speculate that compactness …
aneurysm"; manter a frase de trabalho futuro).

---

## R1-6 — Molecular aspect ratio (reaproveita)

**Decisão:** N6 fechado; parágrafo pronto em `Paper/paper_PRE.tex:347`.

**Resposta:** a da carta atual, Point 6. Linha do submetido: 261 (inserir o
parágrafo das idealizações antes de "Fracture is implemented …").

---

## R2-2 — Localized versus equal load sharing (reaproveita, vocabulário novo)

**Decisão:** N3 fechado; o parágrafo dos dois canais
(`Paper/paper_PRE.tex:230`) vale na substância — carga uniforme por seção,
resistência local por coordenação, nenhuma das duas classes — e só troca
"removal probability" por "threshold". A resposta da carta atual (Point 2)
também vale; a última frase passa a citar a cascata de R2-3.

Linhas do submetido: 185 (inserir o parágrafo dos dois canais depois da
definição de $K$, em vocabulário de limiar); 250 e 269 (saem com R1-3).

---

## Estado do documento

| Crítica | Nó | Resposta | Pendência antes da carta |
|:--|:--|:--|:--|
| R2-1 | N2 | rascunho | localizar o CSV da varredura em $\Delta F$ ou retirar 92,6 → 188,0 |
| R2-3 | N2/N8 | rascunho | — |
| R1-2 | N4, N10 | rascunho | figura nova (sobrevivência + escada) |
| R1-3 | N5, N11 | rascunho | conferir Yang2012 no PDF |
| R2-4 | N4 | rascunho | — |
| R1-4 | N7 | rascunho | harmonizar o critério de "décadas" (0,4–0,7 vs 0,57–0,90); Fig. 3 nova |
| R1-5 | N12 | rascunho | — (teste por fibrila é extensão) |
| R1-7 | N9 | rascunho | Fig. 7 nova |
| R1-1 | N1 | reaproveita | — |
| R1-6 | N6 | reaproveita | — |
| R2-2 | N3 | reaproveita | — |

Figuras do manuscrito revisado (numeração provisória): 1–2 inalteradas; **3**
$D_f$ sob regra uniforme + inclinação local; 4–6 inalteradas (legenda da 6
adaptada); **7** $F_{rup}$ e $\varphi(F/F_{rup})$; **8** sobrevivência das
cascatas por $T_s$ e escada de tamanho; **9** parâmetros do ajuste descritivo
por $m$ — ou fundida na 8. A Fig. 7 (correlações) e a Fig. 8 ($\Psi$) do
estado atual/submetido saem.

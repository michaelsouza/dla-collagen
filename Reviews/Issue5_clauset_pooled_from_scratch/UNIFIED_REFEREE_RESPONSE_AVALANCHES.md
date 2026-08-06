# Unified response on avalanche-size distributions

## Referee comments addressed

This response jointly addresses R1-2, the statistical basis of the power-law
claim; the avalanche-distribution part of R1-3, including the reported
exponents, ensemble size, and Weibull-modulus scope; and R2-4, concerning the
interpretation in terms of self-organized criticality. It also fixes the
terminology relevant to R2-3 by referring specifically to local avalanche
clusters.

## Proposed response to the referees

We thank the Referees for identifying that the original log--log regressions
were not sufficient to establish a power-law avalanche-size distribution. We
have therefore replaced the analysis based on binned frequencies with a new
analysis of the raw, integer-valued sizes of local avalanche clusters. A local
avalanche is one connected component of molecules removed at the same drive
level; disconnected components are counted as separate local events. The
revised dataset contains 50 distinct fibril geometries for each
of the ten values of the surface-relaxation parameter $T_s$, with 1000
stochastic rupture realizations per geometry. Thus, the revised ensemble has
five times the number of geometries used in the original analysis, totaling
50,000 rupture realizations per $T_s$. All distribution fits and tests use
the exact, unbinned discrete observations. The inferential analysis is
performed for nontrivial events $s\geq2$, while singletons are retained when
describing the composition of the complete event population.

We fitted a discrete pure power law

\[
p(s)\propto s^{-\alpha}, \qquad s\geq s_{\min},
\]

by exact maximum likelihood. For each $T_s$, $s_{\min}$ was selected by
minimizing the discrete Kolmogorov--Smirnov statistic with at least 1000 tail
observations. We then applied the semiparametric goodness-of-fit procedure of
Clauset *et al.* with 2500 synthetic replicas, re-estimating both
$s_{\min}$ and $\alpha$ in every replica. The pure power-law hypothesis is
rejected for every value of $T_s$ using the conservative criterion
$p\leq0.1$. The fitted values are:

| $T_s$ | $s_{\min}$ | fitted $\alpha$ | tail fraction among $s\geq2$ | goodness-of-fit $p$ |
|---:|---:|---:|---:|---:|
| 2 | 3 | 1.798 | 0.62894 | <0.0004 |
| 8 | 4 | 1.883 | 0.37262 | <0.0004 |
| 16 | 787 | 11.822 | 0.00245 | <0.0004 |
| 32 | 1177 | 37.282 | 0.00043 | <0.0004 |
| 64 | 1411 | 41.048 | 0.00031 | 0.0248 |
| 128 | 1490 | 38.502 | 0.00050 | <0.0004 |
| 512 | 1593 | 39.535 | 0.00061 | <0.0004 |
| 1024 | 1605 | 50.498 | 0.00032 | 0.0012 |
| 4096 | 1618 | 39.908 | 0.00051 | <0.0004 |
| 8192 | 1659 | 42.125 | 0.00067 | <0.0004 |

For $T_s\geq16$, the selected tails contain at most 0.245% of the
nontrivial events and span at most 0.160 decade. Consequently, the fitted
values of $\alpha$ are parameters of rejected models over extremely narrow
supports; they are not physical avalanche exponents. In particular, the
original values $\gamma\simeq2.31$--2.80 and their comparison with the
mean-field value $5/2$ are removed. The revised data do not support a trend
in a critical exponent or a crossover between load-sharing universality
classes.

We also compared the power law with a power law with exponential cutoff, a
discrete lognormal, and a discrete exponential on the same fitted tails.
Relative likelihood and information criteria often prefer the cutoff model,
with the lognormal nearly indistinguishable in several high-$T_s$ tails.
However, absolute parametric-bootstrap tests show that neither family is
adequate for all $T_s$. The cutoff power law and lognormal are plausible only
for selected, narrow tails; both are rejected at $T_s=2,16,4096$, and the
cutoff model is also rejected at $T_s=8$. Moreover, for $T_s\geq16$, the
power-law parameter of the cutoff family is negative, so the fitted density
rises toward a characteristic size before being cut off. This is not a
decreasing power-law scaling regime. We therefore do not select a universal
parametric family for the tails.

The complete distributions provide a more informative description. Across all
local events, the singleton probability increases from 0.765 at $T_s=2$ to
0.922 at $T_s=8192$. Conditional on $s\geq2$, the 90th percentile decreases
from 27 to 5, whereas the 99th percentile increases from 270 to approximately
1300. Thus, the distribution does not shift uniformly with $T_s$. Instead,
intermediate sizes lose probability while increasingly numerous small events
coexist with a small group of very large events.

We quantified this polarization without assuming a probability family. An
objective two-interval partition of the empirical distribution in $\log s$
places the separation at $9|10$ for $T_s=2$, increasing to $51|52$ at
high $T_s$. The fraction of nontrivial events in the upper group decreases
from 23.12% to approximately 1.77%, while its median grows from 23 to about
1345. The geometric mean of the small-event group remains close to 2.6--3.0.
Accordingly, the cumulative avalanche size becomes strongly concentrated: the
largest 10% of nontrivial events account for 69.63% of the summed sizes at
$T_s=2$ and 91.48% at $T_s=8192$; the largest 1% account for 20.64% and
59.16%, respectively. The nonparametric characteristic size
$\langle s^2\rangle/\langle s\rangle$ increases from 140.6 at $T_s=2$ to
approximately 1200 at high $T_s$.

The evolution becomes small at the largest relaxation values. For
$T_s\geq512$, $\langle s^2\rangle/\langle s\rangle$ lies between 1178 and
1215 and the median of the upper group lies between 1322 and 1356. After
normalizing each upper group by its median, the pairwise mean absolute
distance between log-quantiles is only 0.0115--0.0234. The full nontrivial
distributions in this range also have pairwise Jensen--Shannon distances below
0.027. We describe this result as an approximate empirical stabilization of
the high-$T_s$ distributions. We do not interpret the plateau or the
approximate collapse as evidence of a critical point, scale-free behavior, or
universality.

As an additional check, we fitted the complete $s\geq2$ distribution with a
five-parameter mixture intended to represent a decreasing small-event
component and a lognormal large-event component. Although this model reproduces
the visual two-scale structure and improves BIC over a single lognormal, it is
rejected at every $T_s$: none of 100 fitted bootstrap replicas per condition
has a KS statistic as large as the observed value. The exact one-sided 95%
upper bound is $p<0.0296$, and the observed KS statistic is 50--108 times the
largest synthetic value. This result confirms that the empirical separation
into two scales should not be promoted to a particular mixture distribution.

We have therefore revised the conclusion as follows: under the present local
event definition and for the simulated model with Weibull modulus $m=2$, the
avalanche-size distributions are discrete, finite-support, and progressively
polarized, with a small-event body coexisting with a rare upper-size group and
an approximate stabilization for $T_s\geq512$. The data reject a pure power
law at every $T_s$ and do not validate one alternative parametric family
across all conditions. Accordingly, the revised manuscript removes the claims
of self-organized criticality, scale-free behavior, a universal avalanche
exponent, and a load-sharing universality crossover.

The larger 50-geometry ensemble is the best dataset currently available, but
we do not present it as a formal convergence study in ensemble size. Likewise,
all simulations analyzed here use $m=2$. Repeating the complete simulation
campaign for additional Weibull moduli is computationally prohibitive within
this revision; therefore, we explicitly restrict the conclusion to $m=2$
and make no claim of robustness with respect to the Weibull modulus.

## Manuscript changes supported by this response

The avalanche section should be revised consistently with the response above:

1. Replace the binned log--log regressions and the plot of $\gamma(T_s)$ with
   exact empirical PMFs/CCDFs and goodness-of-fit results.
2. State the local connected-component definition of an avalanche and the
   analyzed support $s\geq2$; report singletons separately as part of the
   complete population.
3. Report the rejection of the pure power law for all ten $T_s$, including
   the fitted cutoff, tail fraction, and goodness-of-fit $p$-value.
4. Describe the positive empirical result using quantiles, concentration,
   characteristic size, and the two-scale partition, rather than assigning a
   new parametric family.
5. Describe the high-$T_s$ behavior as approximate stabilization, not as a
   critical plateau or universal regime.
6. Remove SOC, scale-free, universal-exponent, and $5/2$ load-sharing
   crossover claims, and restrict the reported scope to $m=2$.

## Evidence package

The numerical basis of this response is recorded in the same directory:

- `observed_power_law_fits.csv` and `power_law_gof_B2500.csv`: pure-power-law
  fits and absolute goodness-of-fit tests;
- `model_fits.csv`, `model_comparisons.csv`, and
  `alternative_model_gof_B2500.csv`: competing tail models;
- `full_distribution_summary.csv`, `full_distribution_pmf.csv`, and
  `full_distribution_pairwise_distances.csv`: exact complete distributions;
- `complete_mixture_gof_B100.csv`: rejected two-component model for the full
  $s\geq2$ support;
- `avalanche_behavior_summary.csv` and `avalanche_lorenz.csv`: empirical
  two-scale partition, concentration, and characteristic sizes;
- `avalanche_large_scale_distances.csv`, `avalanche_ccdf_crossings.csv`, and
  `avalanche_regime_clustering.csv`: stabilization and descriptive comparisons
  among $T_s$;
- `full_distribution_overview.pdf`, `avalanche_behavior_metrics.pdf`,
  `avalanche_large_scale_collapse.pdf`, and
  `avalanche_regime_dendrogram.pdf`: publication-ready visual summaries.

The consolidated methodological and decision record is in
`REFEREE_RESPONSE_EVIDENCE.md`; complete reproduction commands are in
`README.md`.

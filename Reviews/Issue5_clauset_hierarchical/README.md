# Issue #5 — discrete avalanche-tail reanalysis

## Scope and frozen choices

This analysis uses the complete event data from 50 independently generated
fibril geometries and 1,000 rupture realizations per geometry at each of the
ten values of $T_s$. An event is one spatially connected component removed at
one fixed-force step. Singleton events ($s=1$) are valid observations and are
retained. Events at the terminal rupture step are excluded from the primary
population. Temporally disconnected events are not aggregated.

The resulting population contains 300,538,797 preterminal local events. The
singleton fraction rises from 0.771 at $T_s=2$ to 0.923 at $T_s=8192$.

## Methods

For every $T_s$, the point fit follows Clauset, Shalizi, and Newman:

1. exact discrete maximum likelihood with Hurwitz-zeta normalization;
2. selection of $s_{min}$ by the discrete KS minimum;
3. at least 1,000 events in each candidate tail;
4. all competing models fitted on the same selected support.

Goodness of fit is reported in two ways because individual events are not
independent observations:

- **iid Clauset test:** the original semiparametric bootstrap, with a complete
  re-estimation of $s_{min}$ and $\alpha$ in 2,500 synthetic samples. It is a
  literal implementation of the published test, but its iid assumption is
  violated because runs share fibril geometry and events in one run share the
  damage history.
- **fibril-block test:** a centered empirical-process bootstrap that resamples
  the 50 fibril geometries as whole independent blocks. It uses 999 replicates
  per condition. The only result close to the decision threshold,
  $T_s=64$, was refined to 4,999 replicates using the same initial random
  sequence.

The decision threshold was fixed at $p\leq0.10$. A value above the threshold
means only that the fitted tail was not rejected; it does not prove a power
law. Power law with exponential cutoff, discrete lognormal, and discrete
exponential alternatives received fixed-support, fibril-block absolute-fit
tests. Non-nested relative comparisons use per-fibril likelihood
contributions. The pure-versus-cutoff Wilks statistic is retained only as a
descriptive number because the null is on a parameter boundary.

## Results

| $T_s$ | $s_{min}$ | $\hat\alpha$ (95% block interval) | tail fraction | decades | block $p$ | iid Clauset | decision |
|---:|---:|---:|---:|---:|---:|:---:|:---|
| 2 | 69 | 3.822 [3.186, 4.200] | 0.00248 | 0.80 | 0.476 | 0/2500 | dependence-sensitive; tail too short |
| 8 | 3 | 2.108 [2.087, 4.722] | 0.09269 | 2.33 | 0.001 | 0/2500 | rejected by both |
| 16 | 3 | 2.264 [2.204, 2.550] | 0.06256 | 2.33 | 0.002 | 0/2500 | rejected by both |
| 32 | 4 | 2.434 [2.387, 2.483] | 0.02492 | 2.17 | 0.047 | 0/2500 | rejected by both |
| 64 | 6 | 2.534 [2.484, 3.642] | 0.00835 | 1.95 | 0.1104 | 0/2500 | dependence-sensitive; marginal block result |
| 128 | 6 | 2.645 [2.602, 2.677] | 0.00665 | 1.91 | 0.003 | 0/2500 | rejected by both |
| 512 | 6 | 2.711 [2.680, 2.751] | 0.00599 | 1.82 | 0.221 | 0/2500 | dependence-sensitive |
| 1024 | 6 | 2.716 [2.662, 2.776] | 0.00597 | 1.86 | 0.053 | 0/2500 | rejected by both |
| 4096 | 6 | 2.697 [2.651, 2.749] | 0.00604 | 1.83 | 0.348 | 0/2500 | dependence-sensitive |
| 8192 | 8 | 2.682 [2.655, 3.882] | 0.00324 | 1.79 | 0.003 | 0/2500 | rejected by both |

The Monte Carlo 95% interval for the refined $T_s=64$ block exceedance
probability is [0.1017, 0.1192]. It is just above the fixed threshold, so this
condition is reported as marginal even though increasing the bootstrap
resolution changed its binary label.

The iid Clauset bootstrap produced zero exceedances in 2,500 replicates in
every condition. Conversely, the fibril-block test does not reject the fitted
tail at $T_s=2,64,512,4096$. This disagreement is the main scientific result:
power-law compatibility is sensitive to the assumed independent unit. The
fibril-block analysis is more appropriate for uncertainty across geometries,
but the result is not robust to the literal iid Clauset diagnostic requested
by the referee.

All three tested alternatives are also rejected by their fibril-block
absolute-fit tests in every condition. A relative likelihood advantage is not
treated as validation when the allegedly better model fails its own absolute
fit. In particular, the relative lognormal advantage at $T_s=4096$ does not
establish a lognormal tail because its block goodness-of-fit value is 0.005.

## Representation and stability diagnostics

Every selected tail receives events from all 50 fibrils. The number of
represented realizations ranges from 15,218 at $T_s=2$ to at least 41,674 in
all other conditions, so no tail is produced by one or two exceptional
geometries.

Random-subset fits with 10, 20, 30, 40, and 50 fibrils show that the central
estimates generally stabilize by 30–40 fibrils. There are important
exceptions. At $T_s=8$, omitting one fibril can move $s_{min}$ from 3 to 150
and $\alpha$ from 2.105 to 4.814. At $T_s=8192$, small subsets frequently
select $s_{min}=1$, although leave-one-fibril-out fits of the full ensemble
remain stable at $s_{min}=8$. These instabilities agree with the broad block
intervals and argue against interpreting every fitted exponent physically.

Across the 50 fibrils, the 99.9th percentile of preterminal event size has no
consistent positive association with the initial backbone size. Significant
correlations at $T_s=32$ and 64 are negative, not positive. This limited
within-condition check does not replace simulations at multiple system sizes,
so it cannot establish or exclude finite-size scaling.

## Scientific decision

The shortest defensible statement is:

> After terminal-step removal, exact discrete fits identify power-law-like
> preterminal tails. A fibril-block goodness-of-fit test does not reject those
> tails at $T_s=64,512,4096$ (and at $T_s=2$ over less than one decade), but
> the original iid Clauset bootstrap rejects them. Therefore the evidence is
> dependence-sensitive and does not establish a universal or scale-free
> avalanche law.

This result does not support Self-Organized Criticality, a load-sharing
universality class, or a universal exponent. The high-$T_s$ values near
$\alpha\simeq2.7$ may be reported as conditional tail-fit parameters, not as
validated critical exponents. All conclusions remain conditional on Weibull
modulus $m=2$.

### Exploratory finite-scale extension

A subsequent exploratory test fitted the discrete form
$p(s)\propto s^{-\alpha}\exp[-(s/s_c)^\beta]$ for
$T_s=512,1024,4096,8192$. The common lower cutoff was estimated for this model
by refitting all six parameters at every integer candidate and minimizing the
maximum KS across the four conditions. The selected value is $s_{min}=29$.

On that support, the joint model has common $\alpha=2.534$ and $\beta=2.547$
and condition-specific $s_c\simeq212$--243. Conditional on the selected
support, it is not rejected by either the 999-replicate fibril-block test
($p=0.981$) or the 999-replicate iid parametric sensitivity test ($p=0.558$).
This supports a compact finite-scale distribution with a power-law factor and
a pronounced cutoff, not a pure or scale-free power law. Full evidence is in
`stretched_cutoff_selected_xmin/README.md`; the earlier fixed-$s_{min}=8$
analysis is retained only as provenance.

## Evidence

- `final_power_law_fits.csv`: consolidated point fits, both goodness-of-fit
  decisions, Monte Carlo intervals, and final labels.
- `iid_clauset/`: 2,500 full-refit semiparametric Clauset replicates per
  condition.
- `refinements/Ts64_4999/`: higher-resolution block result for the only
  threshold-adjacent condition.
- `model_fits.csv`, `model_comparisons.csv`, and `model_gof.csv`: common-support
  competing-model evidence.
- `diagnostics/condition_diagnostics.csv`: tail representation, singleton
  fraction, and finite-size correlations.
- `diagnostics/ensemble_stability.csv` and
  `diagnostics/leave_one_fibril_out.csv`: ensemble-size sensitivity.
- `diagnostics/ccdf_power_law.png`,
  `diagnostics/ensemble_stability_alpha.png`, and
  `diagnostics/finite_size_q999.png`: visual diagnostics.
- `stretched_cutoff_high_ts/`: exploratory common-shape finite-cutoff model,
  with the superseded fixed-$s_{min}=8$ support.
- `stretched_cutoff_selected_xmin/`: current common-shape finite-cutoff model,
  model-specific cutoff selection, block and iid goodness-of-fit tests, and
  CCDF figures.

## Reproduction

```bash
PYTHONPATH=Code/Data_analysis .venv/bin/python \
  Code/Data_analysis/run_clauset_hierarchical.py \
  --replicates 999 --alternative-replicates 199

PYTHONPATH=Code/Data_analysis .venv/bin/python \
  Code/Data_analysis/run_clauset_iid_database.py \
  --replicates 2500 --workers 6

PYTHONPATH=Code/Data_analysis MPLCONFIGDIR=/tmp/dla-mpl \
  .venv/bin/python Code/Data_analysis/run_clauset_diagnostics.py \
  --repetitions 100

.venv/bin/python Code/Data_analysis/consolidate_clauset_results.py \
  --refinement \
  Reviews/Issue5_clauset_hierarchical/refinements/Ts64_4999
```

The implementation was checked with 44 automated tests. The synthetic tests
recover known discrete power-law, cutoff-power-law, lognormal, and exponential
parameters, verify bootstrap reproducibility, accept correctly generated
families in development samples, and reject a power law for a separated
exponential alternative.

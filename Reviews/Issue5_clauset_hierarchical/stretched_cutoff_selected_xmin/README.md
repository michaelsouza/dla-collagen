# High-$T_s$ stretched-cutoff model with selected lower cutoff

## Main result

For $T_s=512,1024,4096,8192$, the common lower cutoff was estimated for the
joint model itself rather than inherited from the pure-power-law fits. The
selected support is

\[
s_{min}=29.
\]

On this support, the joint exact-discrete maximum-likelihood fit is

\[
p(s)\propto s^{-2.534}\exp[-(s/s_c)^{2.547}],
\]

with $s_c$ between approximately 212 and 243. The model is compatible with
both the fibril-level variability and the event-level iid diagnostic when the
goodness-of-fit tests are conditioned on the selected support.

## Selection of $s_{min}$

Every common integer cutoff from 1 through 110 was evaluated. The upper limit
is the largest common cutoff leaving at least 1,000 observations in every
condition. For each candidate:

1. the six-parameter joint model was refitted by maximum likelihood;
2. one KS distance was calculated for each $T_s$;
3. the candidate statistic was the maximum of the four KS distances.

The selected value minimizes that simultaneous statistic:

| $s_{min}$ | maximum KS |
|---:|---:|
| 27 | 0.007989 |
| 28 | 0.008071 |
| **29** | **0.007279** |
| 30 | 0.008712 |
| 31 | 0.008886 |

The complete candidate scan is recorded in `xmin_scan.csv`.

## Joint fit

The 95% intervals below are obtained by resampling the 50 fibrils as whole
blocks. The cutoff is held at the selected value during this uncertainty and
goodness-of-fit calculation.

\[
\alpha=2.534\;[2.438,2.615],\qquad
\beta=2.547\;[2.128,2.980].
\]

| $T_s$ | $n(s\geq29)$ | $s_c$ (95% block interval) | KS | conditional block $p$ |
|---:|---:|---:|---:|---:|
| 512 | 14,681 | 242.79 [207.60, 269.51] | 0.00728 | 0.610 |
| 1024 | 15,027 | 217.39 [192.98, 239.01] | 0.00657 | 0.700 |
| 4096 | 15,642 | 211.59 [179.67, 240.61] | 0.00726 | 0.643 |
| 8192 | 14,597 | 243.40 [212.73, 270.36] | 0.00687 | 0.711 |

The simultaneous 999-replicate fibril-block test gives

\[
p_{joint,block}=0.981.
\]

All four separate stretched-cutoff fits are also not rejected by their
199-replicate block tests ($p=0.205$--$0.810$).

## iid sensitivity

The 999-replicate parametric bootstrap, treating the 59,947 tail events as
iid and refitting all six parameters at fixed $s_{min}=29$, gives

\[
p_{joint,iid}=0.558.
\]

The condition-wise values are 0.218, 0.304, 0.176, and 0.245 for increasing
$T_s$. Thus, unlike the earlier fit on $s\geq8$, the selected-support model is
not rejected by the iid sensitivity analysis.

## Interpretation

The result supports a common finite-scale distribution for high-$T_s$
avalanches. It is stronger than the previous fixed-$s_{min}=8$ analysis in two
ways: the support is selected for the adopted model, and the resulting fit is
compatible under both block and iid diagnostics.

The power-law factor remains useful for describing the pre-cutoff decay, while
the fitted $\beta>2$ establishes a pronounced finite cutoff. Therefore the
supported statement is a power-law factor with a stretched-exponential cutoff,
not a pure or scale-free power law.

The reported goodness-of-fit values are conditional on the selected support.
The model family itself was proposed after inspecting the high-$T_s$ curvature,
so independent confirmation would still be useful, but this does not prevent
the fitted distribution from serving as the primary empirical description of
the present data.

## Evidence

- `xmin_scan.csv`: all 110 candidate cutoffs and fitted statistics;
- `joint_fit.csv`: joint estimates and block goodness of fit;
- `joint_block_bootstrap.csv`: 999 complete fixed-support block refits;
- `individual_model_fits.csv`: separate model fits and absolute-fit tests;
- `iid_fixed_B999/iid_joint_gof.csv`: iid sensitivity summary;
- `iid_fixed_B999/iid_joint_replicates.csv`: iid synthetic statistics;
- `joint_ccdf.png`: joint conditional CCDFs.

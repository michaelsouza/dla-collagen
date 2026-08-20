# High-$T_s$ stretched-cutoff analysis

> **Superseded support choice.** This analysis fixed $s_{min}=8$ from the
> earlier pure-power-law fits. The current analysis estimates the lower cutoff
> for the stretched-cutoff model itself and selects $s_{min}=29$; see
> `../stretched_cutoff_selected_xmin/README.md`.

## Question and model

This exploratory analysis asks whether the four high-$T_s$ conditions share a
simple finite-scale tail. The candidate was fixed before this implementation
as

\[
p(s\mid s\geq8)=
\frac{s^{-\alpha}\exp[-(s/s_c)^\beta]}
{\sum_{k=8}^{\infty}k^{-\alpha}\exp[-(k/s_c)^\beta]}.
\]

The implementation uses the integer observations without binning, exact
discrete infinite-support normalization with a bounded remainder, and maximum
likelihood. The common support $s_{min}=8$ was fixed for
$T_s=512,1024,4096,8192$. Terminal-step events remain excluded and singletons
remain part of the empirical body outside the fitted support.

Because the family was chosen after inspecting the high-$T_s$ curvature, this
is an exploratory model even when it passes a goodness-of-fit test.

## Separate fits

| $T_s$ | $\alpha$ | $\beta$ | $s_c$ | KS | fibril-block $p$ | decision |
|---:|---:|---:|---:|---:|---:|:---|
| 512 | 2.6741 | 4.0055 | 272.90 | 0.00192 | 0.700 | not rejected |
| 1024 | 2.6491 | 3.1660 | 241.72 | 0.00503 | 0.070 | rejected |
| 4096 | 2.6488 | 3.2545 | 238.16 | 0.00329 | 0.305 | not rejected |
| 8192 | 2.6445 | 3.6794 | 277.19 | 0.01126 | 0.005 | rejected |

These tests use 199 centered fibril-block bootstrap replicates and refit all
three parameters. Thus, four unrelated condition-specific versions of the
family do not provide an adequate description at every high $T_s$.

## Joint common-shape fit

The prespecified parsimonious version shares $\alpha$ and $\beta$ across the
four conditions and estimates one $s_c(T_s)$ per condition. It has six
parameters rather than the twelve parameters of four separate fits.

The joint maximum-likelihood estimates are

\[
\alpha=2.6543,\qquad \beta=3.4401,
\]

with 95% fibril-block intervals $[2.6221,2.6854]$ and
$[3.0477,3.8266]$, respectively.

| $T_s$ | $s_c$ (95% block interval) | KS | conditional block $p$ |
|---:|---:|---:|---:|
| 512 | 265.53 [238.67, 288.93] | 0.00516 | 0.449 |
| 1024 | 244.12 [218.53, 267.97] | 0.00439 | 0.644 |
| 4096 | 240.26 [212.98, 264.29] | 0.00331 | 0.775 |
| 8192 | 280.90 [249.48, 311.40] | 0.00969 | 0.172 |

The simultaneous test uses the maximum KS across the four conditions and
refits all six parameters in each of 999 fibril-block replicates. It gives

\[
p_{joint,block}=0.381\quad (380/999\text{ exceedances}).
\]

Therefore the joint common-shape model is not rejected under fibril-block
inference, including at $T_s=8192$. The unrestricted individual fit and the
joint fit are distinct statistical hypotheses and estimators: the shared-shape
constraint regularizes the high-$s$ tail and is tested as one simultaneous
model. The result is not obtained by replacing the individual MLE with a
hand-selected parameter set.

The joint model loses only 12.06 log-likelihood units relative to the four
separate fits while using six fewer parameters. Its event-level BIC is lower
by 55.24, reported only as a descriptive parsimony measure because individual
events are dependent.

## Literal iid sensitivity

A second bootstrap generated all four tails from the fitted joint model and
refitted the six parameters in each of 999 synthetic data sets. Treating the
554,083 tail events as iid gives

\[
p_{joint,iid}=0.001\quad (0/999\text{ exceedances, plus-one estimate}).
\]

This disagreement mirrors the pure-power-law analysis. The iid test has very
high sensitivity to small systematic discrepancies but violates the data
hierarchy: realizations share fibril geometry and events within a realization
share damage history. The fibril-block result is the primary inference for
generalization across geometries; the iid rejection remains a required
sensitivity result.

## Scientific decision

The joint model supplies a simple, finite-scale description of the high-$T_s$
tails under the appropriate block analysis:

> For $T_s\geq512$, preterminal local-avalanche tails on $s\geq8$ are
> compatible with a common discrete form
> $s^{-2.654}\exp[-(s/s_c)^{3.440}]$, with a condition-dependent cutoff
> $s_c\simeq240$--281, when fibrils are treated as independent blocks.

This does not validate a pure power law or scale-free behavior. The fitted
$\beta>3$ indicates a sharp finite cutoff, and the result is exploratory and
sensitive to the iid assumption. It is suitable as a compact empirical model,
not as evidence for SOC or a load-sharing universality class.

## Evidence

- `individual_model_fits.csv`: common-support power law, exponential cutoff,
  lognormal, and stretched-cutoff fits.
- `joint_refinement_B999/joint_fit.csv`: final block goodness-of-fit results.
- `joint_refinement_B999/joint_block_bootstrap.csv`: all block replicates and
  parameter estimates.
- `iid_joint_B999/iid_joint_gof.csv`: literal iid parametric-bootstrap result.
- `iid_joint_B999/iid_joint_replicates.csv`: synthetic KS statistics.
- `individual_ccdf.png` and `joint_ccdf.png`: unbinned conditional CCDFs.

## Reproduction

```bash
PYTHONPATH=Code/Data_analysis MPLCONFIGDIR=/tmp/dla-mpl \
  .venv/bin/python Code/Data_analysis/run_stretched_cutoff_high_ts.py \
  --individual-replicates 199 --joint-replicates 199 \
  --output /tmp/stretched_cutoff_primary

PYTHONPATH=Code/Data_analysis MPLCONFIGDIR=/tmp/dla-mpl \
  .venv/bin/python Code/Data_analysis/run_stretched_cutoff_high_ts.py \
  --individual-replicates 1 --joint-replicates 999 \
  --output /tmp/stretched_cutoff_joint_B999

PYTHONPATH=Code/Data_analysis \
  .venv/bin/python Code/Data_analysis/run_stretched_cutoff_iid.py \
  --replicates 999 --workers 6 --output /tmp/stretched_cutoff_iid_B999
```

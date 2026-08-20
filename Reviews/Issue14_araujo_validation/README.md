# Issue 14 - independent validation of avalanche statistics and the Araújo ansatz

## Scope and traceability

Parent Spec: GitHub issue #1. Related ticket: #5. Referee comments: R1-2, R1-3, and R2-4. The accepted event is one nearest-neighbor connected cluster removed at fixed force; fits condition on collective events `s >= 2`. Preterminal (`sem_terminal`) is primary and terminal inclusion (`com_terminal`) is the prespecified sensitivity.

The implementation in `Code/Data_analysis/issue14_araujo/` is independent of the exploratory scripts in `Data_avalanches/scripts/` and the Issue 5 package. Existing exploratory outputs were not overwritten.

## Formula audit and prespecified model

The rendered page 2 of `A Bibliograph/Araujo2003.pdf` and `A Bibliograph/Araujo2003.md` agree. Equation (4) is the survival ansatz `G(s) proportional to s^{-alpha} exp[-(s/s0)^eta]`; differentiating gives Eq. (5)-(6), whose density is proportional to `s^{-(alpha+1)} [alpha + eta (s/s0)^eta] exp[-(s/s0)^eta]`. Therefore `tau = alpha + 1`, and the bracket is `(tau - 1) + eta (s/s0)^eta`.

The exploratory implementation instead used `s^{-tau}[tau + eta(s/s0)^eta]` and normalized only through `4*s_max`; its fit tables and figures are superseded for this candidate. The primary discrete model is the exact survival difference `p(s | s>=xmin) = [G(s)-G(s+1)]/G(xmin)`. Its infinite-support normalization telescopes exactly. The sensitivity integrates the continuous density over `[s-1/2,s+1/2)` and normalizes at `xmin-1/2`. In both cases `s0` is estimated.

## Input audit

All 20 PMFs in `Data_avalanches/` were audited. Counts were reconstructed by rational-denominator consensus across every printed probability, never by assuming that the smallest value is `1/N`. The ten `com_terminal` totals were then checked against the authoritative provenance manifest; mismatches: 0. Subtracting `sem_terminal` from `com_terminal` produced nonnegative integer terminal histograms for every size and condition. The smallest-value/quantum comparison is retained only as a diagnostic.

`Data_avalanches/` retains neither fibril nor realization identity. Consequently, the reported bootstrap intervals are parametric iid-event diagnostics, not hierarchical uncertainty suitable for a final manuscript claim.

## Synthetic validation

The Clauset benchmark (`alpha=2.5`, `xmin=1`, `n=10000`) gave alpha_hat=2.51020 with SE=0.01703 (z=0.60); agreement is assessed through sampling uncertainty, not equality to a published random draw.

At the 0.1 GOF threshold, 7/30 true-power-law samples were rejected: rate=0.233, exact 95% binomial interval=[0.099, 0.423], compatible with 0.1=True.

| generator | replicates | rejection_power | ci_low | ci_high |
|---|---|---|---|---|
| discrete_lognormal | 12 | 0.5833333333333334 | 0.27666968568210587 | 0.8483477701915698 |
| exponential | 12 | 1.0 | 0.7353515306029488 | 1.0 |
| cutoff_power_law | 12 | 0.5833333333333334 | 0.27666968568210587 | 0.8483477701915698 |
| stretched_exponential | 12 | 0.8333333333333334 | 0.515862251314033 | 0.9791374745399076 |
| terminal_peak_mixture | 12 | 0.9166666666666666 | 0.6152038348490559 | 0.9978924067681397 |

Replicate-level power-law estimates, selected cutoffs, semiparametric recovery, Araújo recovery, boundary cases, interval coverage, convergence, and eta-s0 information correlations are in the machine-readable CSV files. Synthetic generators invert survival functions or sample standard distributions and never call fitted-model probabilities.

## Observed-data decision

| population | decisions |
|---|---|
| sem_terminal | not supported: 10/10 |
| com_terminal | not supported: 10/10 |

| population | model | absolute rejections | not testable |
|---|---|---|---|
| sem_terminal | araujo | 0/0 | 10 |
| sem_terminal | cutoff_power_law | 0/0 | 10 |
| sem_terminal | lognormal | 0/0 | 10 |
| sem_terminal | two_population | 0/0 | 10 |
| com_terminal | araujo | 0/0 | 10 |
| com_terminal | cutoff_power_law | 0/0 | 10 |
| com_terminal | lognormal | 0/0 | 10 |
| com_terminal | two_population | 0/0 | 10 |

The two-population candidate has the lowest BIC in every condition, but it too fails the absolute parametric-bootstrap test in every testable fit. It is therefore only a useful descriptive indication that a single-process model is insufficient, not an adequate generative law. Per-condition decisions, BIC differences, parameters, uncertainty, KS, tail-sensitive residuals, and both discretizations are recorded in the CSV tables. With zero bootstrap exceedances, the exact binomial upper bound is used when deciding rejection; relative BIC rank alone never establishes adequacy.

## Scientific boundary

Araújo et al. describe backbone mass between two sites in critical 2D percolation. Here s is a connected local-damage cluster during driven 3D fibril rupture. Relative empirical fit does not transfer the percolation mechanism, exponent-fractal-dimension relation, SOC, or universality.

No fitted parameter is interpreted as a collagen fractal dimension. This analysis does not reinstate self-organized criticality, scale-free behavior, or a local/global load-sharing universality class.

## Proposed response to the referees

We independently validated exact discrete-power-law estimation and bootstrap calibration on synthetic data, reconstructed the avalanche PMFs as integer counts and checked their inclusive totals against the authoritative simulation manifests, and tested the finite-scale ansatz of Araújo et al. using a correctly discretized infinite-support survival difference. We analyzed preterminal clusters as the primary population and terminal inclusion as a sensitivity, always conditioning on s>=2 and comparing all candidates on identical observations. The Araújo model is rejected in every condition; although a two-population candidate is relatively better, it also fails every testable absolute-fit assessment. These results do not support selecting the Araújo ansatz or transferring its mechanism from a critical two-dimensional percolation backbone to driven collagen-fibril rupture, and they supply no basis for SOC, universality, or an exponent-fractal-dimension relation in this system.

## Reproduction

```bash
MPLCONFIGDIR=/tmp/issue14-mpl PYTHONPATH=Code/Data_analysis .venv/bin/python Code/Data_analysis/run_issue14_araujo.py --stage all --observed-bootstrap 39
PYTHONPATH=Code/Data_analysis .venv/bin/python -m unittest discover -s Code/Data_analysis/issue14_araujo -p 'test_*.py'
```

## Acceptance record

All implementation, synthetic validation, input audit, observed assessment, and scientific-boundary criteria in issue #14 are represented by code, automated tests, machine-readable tables, figures, or this decision record. Exact run sizes and seeds are recorded in the JSON/CSV artifacts.

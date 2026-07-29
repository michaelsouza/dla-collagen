# Handoff: ER12738 manuscript revision

This handoff records the current manuscript-revision state so that the work can
continue on another computer without relying on chat history.

## Start here

1. Check out `main` and update it with `git pull --ff-only origin main`.
2. Read `AGENTS.md`.
3. Read the umbrella [Revision Spec #1](https://github.com/michaelsouza/dla-collagen/issues/1).
4. Read the referee reports in `Reviews/Referees.md` and the current letter in
   `Reviews/Response_to_Referees.md`.
5. Inspect the current manuscript changes in `Paper/paper_PRE.tex`.

## Tracker state

Five of the eleven implementation issues are closed: #2, #3, #4, #9, and #10.
The umbrella Spec remains open by design.

Issue #7 is nearly complete. Issue #5 is the main remaining statistical
blocker. Issues #6 and #8 depend on #5; Issue #8 also depends on #7. The final
manuscript and response-letter checks remain in #11 and #12.

## Decisions already incorporated

The manuscript and response letter currently implement these decisions:

- `T_s` is an effective kinetic control parameter, without a one-to-one
  calibration to a single experimental variable.
- The zero-removal sweep is an operational stopping criterion, not an
  equilibrium or long-time stability condition.
- Spatially disconnected nearest-neighbor clusters removed at the same force
  are counted as separate local avalanches.
- Self-Organized Criticality and scale-free behavior are not claimed.
- The current binned avalanche slopes are descriptive until the discrete
  statistical reanalysis in Issue #5 is complete.
- The model is not assigned to the standard equal-load-sharing or
  local-load-sharing universality classes.
- Equation (5) is a phenomenological interpolation; `alpha` and `beta` are
  empirical shape parameters.
- The reduced molecular aspect ratio is acknowledged as a coarse-graining
  limitation.

## Issue #7 status

The new structural validation compares the ensemble cross-sectional fractal
dimension with four descriptors extracted from the three-dimensional
load-bearing backbone:

- mean load-bearing area;
- mean molecular coordination;
- axial coefficient of variation of the load-bearing area;
- mean molecular stress exposure at unit force.

The analysis scripts are:

- `Code/Data_analysis/validate_fractal_proxy.py`;
- `Code/Data_analysis/analyze_fractal_proxy_results.py`;
- `Code/Data_analysis/xmgrace_paper.mplstyle`.

The publication figure is
`Paper/Figures/fractal_proxy_validation.pdf`. The manuscript introduces the
descriptors after the fracture-model definitions and presents this figure as
Figure 7. The response to R1-4 is drafted in
`Reviews/Response_to_Referees.md`.

The current Spearman coefficients are 0.988 for mean load-bearing area, 1.000
for mean coordination, -0.782 for axial variation, and -0.964 for mean stress
exposure. These values must be regenerated after the missing `T_s=16` fibril is
added. The manuscript already states the intended final sample size of 50
fibrils per condition.

Before closing Issue #7:

1. Add the missing `T_s=16` fibril.
2. Rerun the structural analysis and replace Figure 7.
3. Confirm the four reported correlation coefficients.
4. Review the detailed wording and refine the conclusion about the role of
   `D_f`.
5. Record the final evidence and decision in GitHub Issue #7.

## Response-letter status

Eight of the eleven point-by-point responses have drafts. Three responses have
not yet been written:

- R1-3, interpretation of the avalanche exponent relative to 5/2;
- R1-5, empirical relation between `D_f` and rupture statistics;
- R2-2, the precise nature of load sharing in the model.

R1-4 needs only the final Issue #7 values. R1-2 and R2-4 must be updated after
the statistical reanalysis in Issue #5.

The value 5/2 must be described as the classical equal-load-sharing mean-field
reference, not as a universal upper bound. Any final exponent interpretation
must follow the accepted distributional model and uncertainty from Issue #5.

## Data and local execution state

Raw fibril files, simulation outputs, generated CSV tables, local diagnostic
plots, the `cluster_bundle` directory, and `cluster_bundle.tar.gz` are
intentionally absent from this handoff commit.

The interrupted `T_s=32` fracture batch was resumed on the original computer.
Its running outputs remain local and are not required for editing the
manuscript or response letter on the second computer.

Other uncommitted changes under `Code/Dla` and `Code/Fracture_fibril` were kept
out of this handoff because they are independent of the manuscript and
response-letter editing task.

## Validation

The manuscript was compiled after integrating the new text, figure, and
Spearman reference. The build completed with no undefined citations or
references. The new structural-validation figure appears as Figure 7 on page
13 of the compiled manuscript.

The only remaining Issue #7 validation is the rerun after the final `T_s=16`
fibril is available.

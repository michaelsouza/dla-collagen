# Hierarchical Clauset analysis

Local connected avalanches are analyzed before the terminal rupture step. The exact discrete power-law MLE and KS-selected lower cutoff follow Clauset et al.; goodness of fit is calibrated by a centered bootstrap that resamples the 50 fibril geometries as independent blocks.

| Ts | xmin | alpha (95% block CI) | pure p | cutoff p | lognormal p | exponential p | decades | decision |
|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| 64 | 6 | 2.5343 [2.4844, 3.6420] | 0.110 | 0.500 | 0.500 | 0.500 | 1.95 | pure_power_law_plausible |

A p-value at or above 0.10 makes the pure power law plausible; it does not prove it. Model comparisons use the same selected support. The pure-versus-cutoff Wilks value remains a descriptive reference because the models are nested at a boundary; cutoff plausibility is determined by its block-aware absolute-fit test.

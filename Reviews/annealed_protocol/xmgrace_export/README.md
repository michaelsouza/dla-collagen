# xmgrace export — individual stretched-cutoff fits

These plain-text files reproduce the numerical content of the report figures.
Comments begin with `#`; `&` separates Grace data sets.

- `individual_ccdf_xy.dat`: alternating empirical and fitted conditional CCDF
  sets. The exact S-number mapping is in `sets_manifest.csv`. Use logarithmic
  x and y axes.
- `ts_vs_alpha_xydydy.dat`, `ts_vs_beta_xydydy.dat`, and
  `ts_vs_scale_xydydy.dat`: estimate with asymmetric lower/upper 95% block
  bootstrap errors. Grace type `xydydy` is declared in each file. Use a base-2
  logarithmic x axis.
- `model_gof_xy.dat`: one XY set per candidate model. Add a horizontal
  reference line at p=0.10 and use a base-2 logarithmic x axis.
- `pooled_counts_Ts_<value>.dat`: complete preterminal pooled histogram for
  one condition. Columns are integer size `s`, integer `event_count`, and
  normalized `probability`. These include the body below the fitted `xmin`.
- `model_fits.csv`: full fit table, included for labels and auditability.

The CCDF is conditioned on each condition-specific selected `xmin`. Fits use
integer, unbinned, local preterminal avalanche sizes. The model is
`p(s) proportional to s^-alpha exp[-(s/scale)^beta]`.

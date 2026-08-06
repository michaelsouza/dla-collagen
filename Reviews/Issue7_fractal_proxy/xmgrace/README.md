# Figure 7 data for XMGrace

Each `.dat` file corresponds to one panel of the fractal-proxy figure and
contains ten one-point data sets, ordered by

`T_s = 2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192`.

The files use the XMGrace `xydxdy` data type. Their four columns are

1. published cross-sectional fractal dimension, `D_f`;
2. ensemble mean of the structural descriptor;
3. standard error of the mass-radius fit used to obtain `D_f`;
4. standard error of the descriptor mean across the fibrils.

The `T_s` value for each point is written in the comment immediately above
its data set. Keeping the points as separate sets allows their symbols and
error bars to receive the same individual colors used in the figure's color
scale.

The panel files are:

- `figure_7a_df_mean_N.dat`: mean load-bearing area, `<N>`;
- `figure_7b_df_mean_K.dat`: mean molecular coordination, `<K>`;
- `figure_7c_df_cv_N.dat`: axial coefficient of variation, `CV(N)`;
- `figure_7d_df_mean_stress_F1.dat`: mean molecular stress exposure at
  unit force, `<sigma_M>_(F=1)`.

The values come from `ensemble_curve_validation.csv` and
`condition_descriptor_summary.csv` in the parent directory, which are the
same tables read by `analyze_fractal_proxy_results.py` to generate the
current figure.

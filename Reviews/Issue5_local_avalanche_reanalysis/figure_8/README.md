# Figure 8 reproduction

This directory contains a reproducible reanalysis of the cluster-damage
fraction shown in manuscript Figure 8.

For each rupture realization, the rupture force is defined as
`F_rup = max(F)` and every event is assigned to one of 30 fixed bins using
`F_n = F/F_rup`. In each active realization-bin, the plotted quantity is

`Psi = (mass in connected clusters with s >= 2) / (total removed mass)`.

The reported curve is the mean of these per-realization fractions. The
terminal rupture row is included. Realizations without removals in a bin do
not enter that bin's mean, matching the active-event averaging in the source
notebook.

Files:

- `figure_8_all_curves.png` and `.pdf`: visualization for all available `Ts`.
- `figure_8_all_curves.csv`: mean, sample standard deviation, and active-run
  count for every curve and bin.
- `figure_8_selected_xmgrace.dat`: two-column `xy` sets for `Ts = 8, 32, 128,
  8192`, separated by `&` for direct import into xmgrace.
- `figure_8_ts_<Ts>.dat`: one two-column `xy` file for every available `Ts`,
  containing normalized-force midpoint and `Psi` in percent.

Regenerate from the repository root with:

```bash
python3 Code/Data_analysis/reproduce_figure_8.py
```

The old file-level normalization remains available with `--normalization file`,
but it is not used in the exported files here.

#!/usr/bin/env python3
"""D_f(T_s) ao lado das escalas mecanicas: onde cada grandeza satura em T_s.

Lê:      Reviews/N18_df_ten_ts/df_periodic_summary.csv
         Reviews/N9_damage_curves/damage_condition_table.csv (f_rup_per_rod, phi_preterminal, m = 2)
         Reviews/N9_damage_curves/damage_summary.csv (f_rup_mean, n_rods_mean, m = 2)
         Reviews/N18_df_ten_ts/cascade_stats_by_condition.csv (frac1, p99, m = 2)
Escreve: Reviews/N18_df_ten_ts/df_vs_mechanics_by_ts.csv
         Reviews/N18_df_ten_ts/figures/df_vs_mechanics.png
Chamado: à mão, depois de measure_df_periodic_ten_ts.py e analyze_frup_m_scaling.py

T_s de saturacao de uma grandeza: o menor T_s a partir do qual todos os T_s
maiores ficam a 5% do valor em T_s = 8192 (e, quando ha erro-padrao, tambem a
2 EP). Diz onde cada curva "para de subir"; nao afirma mecanismo.
"""
from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[2]
N18 = RAIZ / "Reviews" / "N18_df_ten_ts"
N9 = RAIZ / "Reviews" / "N9_damage_curves"
TS = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]


def satura(ts: list[int], v: np.ndarray, se: np.ndarray | None, tol: float = 0.05) -> int:
    ref = v[-1]
    for i, t in enumerate(ts):
        cauda = v[i:]
        perto = np.all(np.abs(cauda / ref - 1) <= tol)
        if se is not None:
            perto = perto and np.all(np.abs(cauda - ref) <= 2 * np.maximum(se[i:], se[-1]))
        if perto:
            return t
    return ts[-1]


def main() -> None:
    df = pd.read_csv(N18 / "df_periodic_summary.csv", comment="#").set_index("ts").loc[TS]
    cond = pd.read_csv(N9 / "damage_condition_table.csv").query("m == 2").set_index("ts").loc[TS]
    summ = pd.read_csv(N9 / "damage_summary.csv").query("m == 2").set_index("ts").loc[TS]
    casc = pd.read_csv(N18 / "cascade_stats_by_condition.csv").query("m == 2").set_index("ts").loc[TS]

    cols = {
        "D_f_gyration": (df["gyr_primary_mean"].values, df["gyr_primary_se"].values),
        "D_f_mass_radius_rel": (df["mr_rel_0p15R_0p5R_mean"].values, df["mr_rel_0p15R_0p5R_se"].values),
        "R_bar_section": (df["R_bar"].values, None),
        "n_rods_17x17": (summ["n_rods_mean"].values, None),
        "F_rup_m2": (summ["f_rup_mean"].values, summ["f_rup_sd"].values / np.sqrt(summ["n_fibrils"].values)),
        "F_rup_per_rod_m2": (cond["f_rup_per_rod"].values, None),
        "phi_preterminal_m2": (cond["phi_preterminal"].values, None),
        "frac1_m2": (casc["frac1"].values, None),
        "p99_m2": (casc["p99"].values.astype(float), None),
    }
    linhas = []
    for nome, (v, se) in cols.items():
        for i, t in enumerate(TS):
            linhas.append(dict(quantity=nome, ts=t, value=v[i], se=(se[i] if se is not None else np.nan),
                               ratio_to_8192=v[i] / v[-1]))
        linhas.append(dict(quantity=nome, ts="saturation_ts_5pct", value=satura(TS, v, se)))
    out = pd.DataFrame(linhas)
    out.to_csv(N18 / "df_vs_mechanics_by_ts.csv", index=False, float_format="%.5g")

    print(f"{'grandeza':>22} " + " ".join(f"{t:>7}" for t in TS) + "   satura em")
    for nome, (v, se) in cols.items():
        print(f"{nome:>22} " + " ".join(f"{x/v[-1]:7.3f}" for x in v) + f"   T_s = {satura(TS, v, se)}")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.style.use(RAIZ / "Code" / "Data_analysis" / "xmgrace_paper.mplstyle")
    fig, ax = plt.subplots(2, 2, figsize=(8, 6), sharex=True)
    ax = ax.ravel()
    ax[0].errorbar(TS, *cols["D_f_gyration"], fmt="o-", ms=3, label="giração, N 40–N/2")
    ax[0].errorbar(TS, *cols["D_f_mass_radius_rel"], fmt="s-", ms=3, label="massa–raio, 0,15R–0,5R")
    ax[0].set_ylabel("$D_f$"); ax[0].legend(fontsize=7)
    ax[1].plot(TS, cols["F_rup_per_rod_m2"][0], "o-", ms=3); ax[1].set_ylabel("$F_{rup}/N$, $m=2$")
    ax[2].plot(TS, cols["phi_preterminal_m2"][0], "o-", ms=3); ax[2].set_ylabel("$\\varphi$ preterminal, $m=2$")
    ax[3].plot(TS, cols["p99_m2"][0], "o-", ms=3, label="p99"); ax[3].plot(TS, 10 * cols["frac1_m2"][0], "s-", ms=3, label="10 × frac. $s=1$")
    ax[3].set_ylabel("cascatas, $m=2$"); ax[3].legend(fontsize=7)
    for a in ax:
        a.set_xscale("log")
    for a in ax[2:]:
        a.set_xlabel("$T_s$")
    fig.tight_layout()
    (N18 / "figures").mkdir(exist_ok=True)
    fig.savefig(N18 / "figures" / "df_vs_mechanics.png", dpi=200)


if __name__ == "__main__":
    main()

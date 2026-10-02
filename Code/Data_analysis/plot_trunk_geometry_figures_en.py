#!/usr/bin/env python3
"""Versoes en-US, em tres arquivos separados, das figuras de geometria do tronco.

Le so os CSVs ja calculados; nao refaz medida nem fratura.

Le:      Reviews/N18_df_ten_ts/trunk_geometry_by_ts.csv
         Reviews/N18_df_ten_ts/geometry_during_fracture_curves.csv
Escreve: Reviews/N18_df_ten_ts/figures/trunk_geometry_vs_ts_en.png
         Reviews/N18_df_ten_ts/figures/geometry_during_fracture_F_en.png
         Reviews/N18_df_ten_ts/figures/geometry_during_fracture_Frup_en.png
Chamado: à mão, depois de measure_trunk_geometry_by_ts.py e trace_geometry_during_fracture.py
"""
from __future__ import annotations

import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[2]
N18 = RAIZ / "Reviews" / "N18_df_ten_ts"
FIG = N18 / "figures"
AZUL, VERMELHO, FG = "#1F5F8B", "#C0392B", "#23373B"
CMAP = plt.get_cmap("viridis")


def inicial() -> None:
    agg = pd.read_csv(N18 / "trunk_geometry_by_ts.csv").set_index("ts")
    w = int(2 * agg.half_width.iloc[0] + 1)
    fig, ax1 = plt.subplots(figsize=(6.2, 4.2))
    ax2 = ax1.twinx()
    for ax, col, cor, mk, lab, short in [
            (ax1, "N_mean_load", AZUL, "o", r"$\langle N\rangle$, molecules per layer", r"$\langle N\rangle$"),
            (ax2, "K_mean_load", VERMELHO, "s", r"$\langle K\rangle$, neighbours per rod", r"$\langle K\rangle$")]:
        ax.errorbar(agg.index, agg[col], yerr=agg[f"{col}_se"], fmt=mk + "-", color=cor, ms=5, lw=1.3, capsize=3,
                    label=lab + ", load-bearing rods")
        ax.plot(agg.index, agg[col.replace("_load", "_all")], mk + ":", color=cor, ms=3, lw=0.8, mfc="none",
                label=short + ", all rods in the window")
        ax.set_ylabel(lab, color=cor); ax.tick_params(axis="y", colors=cor)
    ax1.set_xscale("log"); ax1.set_xlabel("$T_s$")
    ax1.set_title(f"{w}×{w}×201 trunk, initial geometry", fontsize=9, loc="left")
    h1, l1 = ax1.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, fontsize=6.5, frameon=False, loc="lower right")
    fig.tight_layout(); fig.savefig(FIG / "trunk_geometry_vs_ts_en.png", dpi=200); plt.close(fig)


def dinamica(kind: str, nome: str, xlab: str, titulo: str) -> None:
    cv = pd.read_csv(N18 / "geometry_during_fracture_curves.csv")
    cv = cv[cv.x_kind == kind]
    ts_list = sorted(cv.ts.unique())
    cores = {ts: CMAP(i / max(1, len(ts_list) - 1)) for i, ts in enumerate(ts_list)}
    fig, ax = plt.subplots(figsize=(6.6, 4.9))
    ax2 = ax.twinx()
    for ts in ts_list:
        q = cv[cv.ts == ts].sort_values("x")
        N0, K0 = q.N_mean.iloc[0], q.K_mean.iloc[0]
        ax.plot(q.x, q.N_mean / N0, "-", color=cores[ts], lw=1.6,
                label=f"$T_s={ts}$: $N_0$ = {N0:.0f}, $K_0$ = {K0:.1f}")
        ax.fill_between(q.x, (q.N_mean - q.N_se) / N0, (q.N_mean + q.N_se) / N0, color=cores[ts], alpha=0.2, lw=0)
        ax2.plot(q.x, q.K_mean / K0, "--", color=cores[ts], lw=1.6)
        ax2.fill_between(q.x, (q.K_mean - q.K_se) / K0, (q.K_mean + q.K_se) / K0, color=cores[ts], alpha=0.15, lw=0)
    ax.set_xlabel(xlab)
    ax.set_ylabel(r"$\langle N(F)\rangle / N_0$, molecules per layer (solid)")
    ax2.set_ylabel(r"$\langle K(F)\rangle / K_0$, neighbours per active rod (dashed)")
    ax.set_ylim(0.78, 1.02); ax2.set_ylim(0.98, 1.10)
    # legenda fora do grafico: dentro, ela cobre as curvas tracejadas de T_s baixo
    ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3)
    ax.set_title(titulo, fontsize=9, loc="left")
    fig.tight_layout(); fig.savefig(FIG / nome, dpi=200, bbox_inches="tight"); plt.close(fig)


def main() -> None:
    plt.style.use(RAIZ / "Code" / "Data_analysis" / "xmgrace_paper.mplstyle")
    inicial()
    base = "17×17 trunk, m = 2, 10 realizations × 5 seeds"
    dinamica("F", "geometry_during_fracture_F_en.png", "$F$", base + "; absolute force")
    dinamica("F_over_Frup", "geometry_during_fracture_Frup_en.png", "$F / F_{rup}$",
             base + "; force normalized by each realization's $F_{rup}$")
    print("ok:", FIG)


if __name__ == "__main__":
    main()

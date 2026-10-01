#!/usr/bin/env python3
"""Figuras do N19: F_rup/R e a cauda das cascatas contra a largura, ate a secao inteira.

Uma curva por T_s (2, 32, 128, 8192): recortes 17x17 e 41x41 (N18, 5 sementes x
10 realizacoes) e a secao inteira (N19, -half-width 200, mesma receita), mais os
pontos da escada de uma semente de 2026-09-02 (81, 181, 141) em aberto. Largura
da secao inteira = 2 R_max + 1 por T_s (df_periodic_summary.csv).

Le:      Reviews/N19_full_section_fracture/width_fracture_summary.csv
         Reviews/N19_full_section_fracture/width_fracture_by_realization.csv
Escreve: Reviews/N19_full_section_fracture/figures/frup_and_cascades_by_width.png
         Reviews/N19_full_section_fracture/figures/cascade_size_distribution_by_width.png
Chamado: à mão, depois de summarize_width_fracture.py --out Reviews/N19_full_section_fracture
"""
from __future__ import annotations

import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import NullFormatter

RAIZ = pathlib.Path(__file__).resolve().parents[2]
N19 = RAIZ / "Reviews" / "N19_full_section_fracture"
FIG = N19 / "figures"
CINZA, FG = "#7F8C8D", "#23373B"
CMAP = plt.get_cmap("viridis")


def main() -> int:
    s = pd.read_csv(N19 / "width_fracture_summary.csv", comment="#")
    r = pd.read_csv(N19 / "width_fracture_by_realization.csv", comment="#")
    plt.style.use(RAIZ / "Code" / "Data_analysis" / "xmgrace_paper.mplstyle")
    FIG.mkdir(exist_ok=True)
    ts_list = sorted(s.ts.unique())
    cores = {ts: CMAP(i / max(1, len(ts_list) - 1)) for i, ts in enumerate(ts_list)}

    fig, ax = plt.subplots(2, 2, figsize=(11, 8))
    ax = ax.ravel()
    paineis = [("F_rup_per_rod_mean", "F_rup_per_rod_se", "$F_{rup}/R$ (por molécula portante)"),
               ("p99_pre_mean", None, "p99 das cascatas preterminais (média por realização)"),
               ("max_pre", None, "maior cascata preterminal (máximo sobre realizações)"),
               ("terminal_frac_mean", None, "fração terminal $R_{term}/R$")]
    for a, (col, ecol, lab) in zip(ax, paineis):
        for ts in ts_list:
            loc = s[(s.ts == ts) & s.source.str.startswith("local")].sort_values("width")
            lad = s[(s.ts == ts) & s.source.str.startswith("ladder")].sort_values("width")
            if ecol:
                a.errorbar(loc.width, loc[col], yerr=loc[ecol], fmt="o-", color=cores[ts], ms=5, capsize=3, lw=1.2,
                           label=f"$T_s={ts}$, 5 sementes")
            else:
                a.plot(loc.width, loc[col], "o-", color=cores[ts], ms=5, lw=1.2, label=f"$T_s={ts}$, 5 sementes")
            if len(lad):
                a.plot(lad.width, lad[col], "s--", color=cores[ts], ms=4, lw=0.8, mfc="none",
                       label=f"$T_s={ts}$, escada 02/09 (1 semente)")
        a.set_xscale("log"); a.set_xlabel("largura do recorte (seção inteira = $2R_{max}+1$)")
        a.set_ylabel(lab)
        a.set_xticks([17, 41, 81, 141, 181, 331]); a.set_xticklabels(["17", "41", "81", "141", "181", "331"])
        a.xaxis.set_minor_formatter(NullFormatter())
    ax[1].set_yscale("log"); ax[2].set_yscale("log")
    ax[0].set_ylim(0, 0.85)
    ax[0].legend(fontsize=6, frameon=False, ncol=2)
    ax[1].set_ylabel("p99 das cascatas preterminais"); ax[2].set_ylabel("maior cascata preterminal")
    fig.tight_layout(w_pad=2.5, h_pad=2.0); fig.savefig(FIG / "frup_and_cascades_by_width.png", dpi=200); plt.close(fig)

    # distribuicao de tamanhos preterminais por largura, para T_s = 2 e 128 (se houver os brutos por realizacao: usa max/p99)
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for a, ts in zip(ax, [t for t in [2, 128] if t in ts_list]):
        q = r[(r.ts == ts) & r.source.str.startswith("local")]
        for w, cor in zip(sorted(q.width.unique()), [CMAP(0.15), CMAP(0.55), CMAP(0.9)]):
            g = q[q.width == w]
            a.scatter(g.R, g.max_pre, s=14, color=cor, label=f"largura {w}: máx. preterminal")
            a.scatter(g.R, g.p99_pre, s=14, marker="x", color=cor, label=f"largura {w}: p99")
        a.axhline(1, color=CINZA, lw=0.5)
        a.set_xscale("log"); a.set_yscale("log"); a.set_xlabel("$R$ (moléculas portantes da realização)")
        a.set_xticks([1e3, 3e3, 1e4, 3e4, 6e4]); a.set_xticklabels(["$10^3$", "$3\\times10^3$", "$10^4$", "$3\\times10^4$", "$6\\times10^4$"])
        a.xaxis.set_minor_formatter(NullFormatter())
        a.set_ylabel("tamanho de cascata"); a.set_title(f"$T_s = {ts}$", fontsize=9, loc="left")
        a.legend(fontsize=6, frameon=False)
    fig.tight_layout(); fig.savefig(FIG / "cascade_size_distribution_by_width.png", dpi=200); plt.close(fig)
    print("figuras em", FIG)
    return 0


if __name__ == "__main__":
    sys.exit(main())

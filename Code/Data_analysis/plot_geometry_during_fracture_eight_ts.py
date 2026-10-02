#!/usr/bin/env python3
"""Figura interna: <K>/K_0 (coordenacao) e <N>/N_0 (segmentos por camada) durante a fratura nos oito T_s, um painel por grandeza.

Mesmo dado de geometry_during_fracture.png, sem eixo y duplo: linhas = grandeza
(K, N_i), colunas = F absoluto e F/F_rup. Faixa = 1 EP entre realizacoes.

Lê:      Reviews/N18_df_ten_ts/geometry_during_fracture_curves.csv
Escreve: Reviews/N18_df_ten_ts/figures/geometry_during_fracture_eight_ts.png
Chamado: à mão, depois de trace_geometry_during_fracture.py --ts 2 8 16 32 64 128 1024 8192
"""
from __future__ import annotations

import pathlib

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[2]
N18 = RAIZ / "Reviews" / "N18_df_ten_ts"


def main() -> int:
    cv = pd.read_csv(N18 / "geometry_during_fracture_curves.csv")
    ts_list = sorted(cv.ts.unique())
    cores = plt.cm.viridis([i / (len(ts_list) - 1) * 0.92 for i in range(len(ts_list))])
    fig, ax = plt.subplots(2, 2, figsize=(11, 7.5), sharex="col", constrained_layout=True)
    for j, (kind, xlab) in enumerate([("F", r"$F$"), ("F_over_Frup", r"$F/F_{rup}$")]):
        for i, (col, ylab) in enumerate([("K", r"$\langle K(F)\rangle/\langle K_0\rangle$, coordination"),
                                         ("N", r"$\langle N(F)\rangle/\langle N_0\rangle$, segments per layer")]):
            a = ax[i, j]
            for ts, c in zip(ts_list, cores):
                q = cv[(cv.ts == ts) & (cv.x_kind == kind)].sort_values("x")
                v0 = q[f"{col}_mean"].iloc[0]
                y, e = q[f"{col}_mean"] / v0, q[f"{col}_se"] / v0
                novo = ts in (1024, 8192)
                a.plot(q.x, y, color=c, lw=2.4 if novo else 1.5, ls="-" if novo else "-",
                       label=rf"$T_s = {ts}$" + ("  (novo)" if novo else ""), zorder=3 if novo else 2)
                a.fill_between(q.x, y - e, y + e, color=c, alpha=0.15, lw=0)
            a.axhline(1, color="0.6", lw=0.8, zorder=1)
            a.grid(alpha=0.25)
            a.set_ylabel(ylab)
            if i == 1:
                a.set_xlabel(xlab)
    ax[0, 0].set_title(r"$F$ absoluto")
    ax[0, 1].set_title(r"$F$ normalizado por $F_{rup}$ da realização")
    h, l = ax[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="outside right center", frameon=False)
    fig.suptitle(r"Tronco 17×17, $m = 2$, 10 realizações × 5 sementes; faixa = 1 EP", fontsize=11)
    saida = N18 / "figures" / "geometry_during_fracture_eight_ts.png"
    fig.savefig(saida, dpi=150)
    print(saida.relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

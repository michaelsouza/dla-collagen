#!/usr/bin/env python3
"""Projetos .agr (en-US) das tres figuras de geometria do tronco, com dois eixos y.

Dois eixos y no xmgrace = dois graficos sobrepostos na mesma VIEW: G0 leva o
eixo esquerdo (K) e a moldura; G1 leva o eixo direito (N_i), sem moldura nem
eixo x. Series de G0 em linha cheia, de G1 tracejadas.

Le:      Reviews/N18_df_ten_ts/trunk_geometry_by_ts.csv
         Reviews/N18_df_ten_ts/geometry_during_fracture_curves.csv
Escreve: Reviews/N18_df_ten_ts/xmgrace/trunk_geometry_vs_ts_{K,N}_xydy.dat, .agr, .pdf
         Reviews/N18_df_ten_ts/xmgrace/geometry_during_fracture_{F,Frup}_{K,N}_xy.dat, .agr, .pdf
Chamado: à mão, depois de measure_trunk_geometry_by_ts.py e trace_geometry_during_fracture.py
"""
from __future__ import annotations

import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_xmgrace_projects import GROSSURA_EIXO, ROTULO, TIQUE, roda  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[2]
N18 = RAIZ / "Reviews" / "N18_df_ten_ts"
SAIDA = N18 / "xmgrace"
AZUL, VERMELHO = 20, 21
VIRIDIS = [(68, 1, 84), (65, 68, 135), (42, 120, 142), (34, 168, 132), (122, 209, 81), (253, 231, 37)]


def cores() -> list[str]:
    return [f'MAP COLOR {AZUL} TO (31, 95, 139), "steel"', f'MAP COLOR {VERMELHO} TO (192, 57, 43), "brick"'] + \
           [f'MAP COLOR {30 + i} TO ({r}, {g}, {b}), "viridis{i}"' for i, (r, g, b) in enumerate(VIRIDIS)]


def eixos_duplos(vista, xlab, ylab_esq, ylab_dir, cor_esq, cor_dir, mundo_esq, mundo_dir,
                 xfaixa, xmaj, ymaj_esq, ymaj_dir, xlog=False) -> list[str]:
    vx0, vy0, vx1, vy1 = vista
    b = []
    for g, ylab, cor, (y0, y1), ymaj in [(0, ylab_esq, cor_esq, mundo_esq, ymaj_esq),
                                          (1, ylab_dir, cor_dir, mundo_dir, ymaj_dir)]:
        b += [f"WITH G{g}", f"VIEW {vx0}, {vy0}, {vx1}, {vy1}",
              f"WORLD XMIN {xfaixa[0]}", f"WORLD XMAX {xfaixa[1]}", f"WORLD YMIN {y0}", f"WORLD YMAX {y1}",
              f'YAXIS LABEL "\\3{ylab}"', f"YAXIS LABEL CHAR SIZE {ROTULO * 0.8}", f"YAXIS LABEL COLOR {cor}",
              f"YAXIS TICKLABEL CHAR SIZE {TIQUE}", f"YAXIS TICKLABEL COLOR {cor}", f"YAXIS TICK COLOR {cor}",
              f"YAXIS TICK MAJOR {ymaj}", "YAXIS TICK MINOR TICKS 1",
              f"YAXIS BAR LINEWIDTH {GROSSURA_EIXO}", f"YAXIS TICK MAJOR LINEWIDTH {GROSSURA_EIXO}",
              f"YAXIS TICK MINOR LINEWIDTH {GROSSURA_EIXO}", "YAXIS TICK MAJOR SIZE 1.4", "YAXIS TICK MINOR SIZE 0.8",
              "LEGEND OFF"]
        if xlog:
            b += ["XAXES SCALE LOGARITHMIC"]
        if g == 0:
            b += [f"FRAME LINEWIDTH {GROSSURA_EIXO}", f'XAXIS LABEL "\\3{xlab}"', f"XAXIS LABEL CHAR SIZE {ROTULO}",
                  f"XAXIS TICKLABEL CHAR SIZE {TIQUE}", f"XAXIS BAR LINEWIDTH {GROSSURA_EIXO}",
                  f"XAXIS TICK MAJOR LINEWIDTH {GROSSURA_EIXO}", f"XAXIS TICK MINOR LINEWIDTH {GROSSURA_EIXO}",
                  f"XAXIS TICK MAJOR {xmaj}", "XAXIS TICK MINOR TICKS " + ("8" if xlog else "1"),
                  "XAXIS TICK MAJOR SIZE 1.4", "XAXIS TICK MINOR SIZE 0.8", "YAXIS TICK PLACE NORMAL",
                  "YAXIS TICKLABEL PLACE NORMAL", "YAXIS LABEL PLACE NORMAL"]
            if xlog:
                b += ["XAXIS TICKLABEL FORMAT POWER", "XAXIS TICKLABEL PREC 0"]
        else:
            b += ["FRAME LINESTYLE 0", "XAXIS TICK OFF", "XAXIS TICKLABEL OFF", "XAXIS BAR OFF",
                  "YAXIS TICK PLACE OPPOSITE", "YAXIS TICKLABEL PLACE OPPOSITE", "YAXIS LABEL PLACE OPPOSITE"]
    return b


def serie(g, i, cor, simbolo, tracejada, legenda="", tamanho=1.1, largura=2.4) -> list[str]:
    return [f"WITH G{g}", f"S{i} SYMBOL {simbolo}", f"S{i} SYMBOL SIZE {tamanho}", f"S{i} SYMBOL COLOR {cor}",
            f"S{i} SYMBOL FILL COLOR {cor}", f"S{i} SYMBOL FILL PATTERN {1 if simbolo else 0}",
            f"S{i} SYMBOL LINEWIDTH 2.0", f"S{i} LINE COLOR {cor}", f"S{i} LINE LINEWIDTH {largura}",
            f"S{i} LINE LINESTYLE {3 if tracejada else 1}", f"S{i} ERRORBAR COLOR {cor}",
            f"S{i} ERRORBAR SIZE 0.8", f"S{i} ERRORBAR LINEWIDTH 2.0", f'S{i} LEGEND "{legenda}"']


def figura_inicial() -> None:
    agg = pd.read_csv(N18 / "trunk_geometry_by_ts.csv").set_index("ts")
    w = int(2 * agg.half_width.iloc[0] + 1)
    for letra, col, lab in [("K", "K_mean", "molecules per layer"), ("N", "N_mean", "neighbours per rod")]:
        out = [f"# {w}x{w}x201 trunk, initial geometry: <{letra}> versus T_s, 5 seeds per T_s",
               f"# Set 0: load-bearing rods (after the load-path filter), columns T_s  mean  SE over seeds",
               f"# Set 1: all rods in the window, columns T_s  mean",
               f"# {lab}. Source: Reviews/N18_df_ten_ts/trunk_geometry_by_ts.csv. Log x axis.",
               "@type xydy", "# load-bearing"]
        out += [f"{ts} {r[col + '_load']:.4f} {r[col + '_load_se']:.4f}" for ts, r in agg.iterrows()] + ["&"]
        out += ["@type xy", "# all rods in window"]
        out += [f"{ts} {r[col + '_all']:.4f}" for ts, r in agg.iterrows()] + ["&"]
        (SAIDA / f"trunk_geometry_vs_ts_{letra}_xydy.dat").write_text("\n".join(out) + "\n", encoding="utf-8")
    b = ["PAGE SIZE 640, 460"] + cores()
    b += eixos_duplos((0.24, 0.18, 1.18, 0.92), "T\\ss\\N", "\\1<K>\\3, molecules per layer",
                      "\\1<N\\si\\N>\\3, neighbours per rod", AZUL, VERMELHO,
                      (100, 1300), (22, 56), (1.4, 13000), 10, 200, 5, xlog=True)
    b += serie(0, 0, AZUL, 1, False, "<K>, load-bearing rods") + serie(0, 1, AZUL, 1, False, "<K>, all rods", 0.6, 1.2)
    b += ["WITH G0", "S1 SYMBOL FILL PATTERN 0", "S1 LINE LINESTYLE 2"]
    b += serie(1, 0, VERMELHO, 2, False, "<N_i>, load-bearing rods") + serie(1, 1, VERMELHO, 2, False, "<N_i>, all rods", 0.6, 1.2)
    b += ["WITH G1", "S1 SYMBOL FILL PATTERN 0", "S1 LINE LINESTYLE 2",
          "WITH G0", "LEGEND ON", "LEGEND BOX LINESTYLE 0", "LEGEND BOX FILL PATTERN 0", "LEGEND CHAR SIZE 1.1",
          "LEGEND LOCTYPE VIEW", "LEGEND 0.72, 0.42",
          "WITH G1", "LEGEND ON", "LEGEND BOX LINESTYLE 0", "LEGEND BOX FILL PATTERN 0", "LEGEND CHAR SIZE 1.1",
          "LEGEND LOCTYPE VIEW", "LEGEND 0.72, 0.32"]
    roda(b, [[SAIDA / "trunk_geometry_vs_ts_K_xydy.dat"], [SAIDA / "trunk_geometry_vs_ts_N_xydy.dat"]],
         SAIDA / "trunk_geometry_vs_ts.agr", SAIDA / "trunk_geometry_vs_ts.pdf")


def figura_dinamica(kind: str, tag: str, xlab: str, xmax: float, xmaj: float) -> None:
    cv = pd.read_csv(N18 / "geometry_during_fracture_curves.csv")
    cv = cv[cv.x_kind == kind]
    ts_list = sorted(cv.ts.unique())
    legendas = []
    for letra, col in [("K", "K_mean"), ("N", "N_mean")]:
        out = [f"# 17x17 trunk, m = 2, 10 realizations x 5 seeds: <{letra}(F)>/{letra}_0 over active rods, x = {xlab}",
               f"# One set per T_s in the order {', '.join(map(str, ts_list))}; columns x  value/initial  SE/initial",
               "# Source: Reviews/N18_df_ten_ts/geometry_during_fracture_curves.csv"]
        for ts in ts_list:
            q = cv[cv.ts == ts].sort_values("x")
            v0 = q[col].iloc[0]
            if letra == "K":
                legendas.append(f"T\\ss\\N = {ts}: K\\s0\\N = {v0:.0f}")
            else:
                legendas[ts_list.index(ts)] += f", N\\s0\\N = {v0:.1f}"
            out += ["@type xydy", f"# T_s = {ts}, {letra}_0 = {v0:.4f}"]
            out += [f"{x:.5f} {v / v0:.6f} {e / v0:.6f}" for x, v, e in zip(q.x, q[col], q[col.replace('mean', 'se')])]
            out.append("&")
        (SAIDA / f"geometry_during_fracture_{tag}_{letra}_xydy.dat").write_text("\n".join(out) + "\n", encoding="utf-8")
    # pagina mais alta: a legenda de seis entradas fica abaixo do eixo x, fora das curvas
    b = ["PAGE SIZE 640, 600"] + cores()
    b += eixos_duplos((0.22, 0.36, 0.93, 0.95), xlab, "\\1<K(F)>/K\\s0\\N\\3 (solid)",
                      "\\1<N\\si\\N(F)>/N\\s0\\N\\3 (dashed)", 1, 1,
                      (0.78, 1.02), (0.98, 1.10), (0.0, xmax), xmaj, 0.05, 0.02)
    for i, ts in enumerate(ts_list):
        b += serie(0, i, 30 + i, 0, False, legendas[i], largura=2.4) + ["WITH G0", f"S{i} ERRORBAR OFF"]
        b += serie(1, i, 30 + i, 0, True, "", largura=2.4) + ["WITH G1", f"S{i} ERRORBAR OFF"]
    b += ["WITH G0", "LEGEND ON", "LEGEND BOX LINESTYLE 0", "LEGEND BOX FILL PATTERN 0", "LEGEND CHAR SIZE 0.95",
          "LEGEND LOCTYPE VIEW", "LEGEND 0.24, 0.215", "LEGEND VGAP 1", "LEGEND LENGTH 4"]
    roda(b, [[SAIDA / f"geometry_during_fracture_{tag}_K_xydy.dat"], [SAIDA / f"geometry_during_fracture_{tag}_N_xydy.dat"]],
         SAIDA / f"geometry_during_fracture_{tag}.agr", SAIDA / f"geometry_during_fracture_{tag}.pdf")


def main() -> None:
    SAIDA.mkdir(exist_ok=True)
    figura_inicial()
    cv = pd.read_csv(N18 / "geometry_during_fracture_curves.csv")
    fmax = float(cv[cv.x_kind == "F"].x.max())
    figura_dinamica("F", "F", "F", 100 * (int(fmax // 100) + 1), 500)
    figura_dinamica("F_over_Frup", "Frup", "F / F\\srup\\N", 1.0, 0.2)


if __name__ == "__main__":
    main()

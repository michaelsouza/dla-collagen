#!/usr/bin/env python3
"""Fig. 8 da versao dos coautores (2026-10-01) refeita com os dados corrigidos: <K>/<K0> e <N>/<N0> contra F.

Reproduz o estilo do figure_8.pdf deles (dois paineis, cores e simbolos padrao
do xmgrace, linha tracejada, legenda T_s em Times-BoldItalic), com a notacao do
artigo: (a) K = coordenacao media dos bastoes ativos; (b) N = segmentos por
camada, o N(i) de sigma = F/N(i). Ate 2026-10-01 nossos .dat tinham K e N
trocados, e a figura deles herdou o erro (registro
2026-10-01_N18_notacao_K_N_trocada.md). Oito T_s: os seis da figura e 1024 e
8192 para a saturacao; --ts muda a lista.

Lê:      Reviews/N18_df_ten_ts/geometry_during_fracture_curves.csv (x_kind == "F")
Escreve: Reviews/N18_df_ten_ts/xmgrace/figure_8_geometry_during_fracture/figure_8a_K_xy.dat,
         figure_8b_N_xy.dat, figure_8.agr, figure_8.pdf
Chamado: à mão, depois de trace_geometry_during_fracture.py --ts 2 8 16 32 64 128 1024 8192
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_xmgrace_projects import roda  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[2]
N18 = RAIZ / "Reviews" / "N18_df_ten_ts"
SAIDA = N18 / "xmgrace" / "figure_8_geometry_during_fracture"
# (cor, simbolo) do xmgrace por T_s; os seis primeiros copiam a figura dos coautores
ESTILO = {2: (1, 1), 8: (2, 2), 16: (3, 1), 32: (4, 4), 64: (11, 3), 128: (9, 6), 1024: (10, 5), 8192: (12, 7)}
BI = "\\f{Times-BoldItalic}"


def escreve_dat(cv: pd.DataFrame, ts_list: list[int], letra: str, destino: pathlib.Path) -> None:
    linhas = []
    for ts in ts_list:
        q = cv[cv.ts == ts].sort_values("x")
        v = q[f"{letra}_mean"] / q[f"{letra}_mean"].iloc[0]
        linhas += [f"{x:.5f} {y:.6f}" for x, y in zip(q.x, v)] + ["&"]
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def painel(g: int, vista: tuple, ylab: str, mundo_y: tuple, ymaj: float, rotulo: str, xmax: float,
           ts_list: list[int], legenda_xy: tuple) -> list[str]:
    x0, y0, x1, y1 = vista
    b = [f"WITH G{g}", f"G{g} ON", f"VIEW {x0}, {y0}, {x1}, {y1}",
         f"WORLD XMIN 0", f"WORLD XMAX {xmax}", f"WORLD YMIN {mundo_y[0]}", f"WORLD YMAX {mundo_y[1]}",
         "XAXIS TICK MAJOR 500", "XAXIS TICK MINOR TICKS 1", f"YAXIS TICK MAJOR {ymaj}", "YAXIS TICK MINOR TICKS 1",
         f'XAXIS LABEL "{BI}F"', "XAXIS LABEL CHAR SIZE 1.6",
         f'YAXIS LABEL "{ylab}"', "YAXIS LABEL CHAR SIZE 1.6",
         "XAXIS TICKLABEL CHAR SIZE 1.1", "YAXIS TICKLABEL CHAR SIZE 1.1",
         "FRAME LINEWIDTH 1.5", "XAXIS TICK MAJOR LINEWIDTH 1.5", "YAXIS TICK MAJOR LINEWIDTH 1.5"]
    for i, ts in enumerate(ts_list):
        cor, simb = ESTILO[ts]
        b += [f"S{i} SYMBOL {simb}", f"S{i} SYMBOL SIZE 0.7", f"S{i} SYMBOL COLOR {cor}",
              f"S{i} SYMBOL FILL PATTERN 1", f"S{i} SYMBOL FILL COLOR {cor}", f"S{i} SYMBOL LINEWIDTH 1.0",
              f"S{i} LINE TYPE 1", f"S{i} LINE LINESTYLE 3", f"S{i} LINE LINEWIDTH 1.0", f"S{i} LINE COLOR {cor}",
              f'S{i} LEGEND "{BI}T\\ss\\N = {ts}"']
    b += ["LEGEND ON", "LEGEND LOCTYPE VIEW", f"LEGEND {legenda_xy[0]}, {legenda_xy[1]}", "LEGEND CHAR SIZE 1.0",
          "LEGEND BOX LINESTYLE 1", "LEGEND BOX FILL PATTERN 1", "LEGEND VGAP 1", "LEGEND LENGTH 3",
          "WITH STRING", "STRING ON", "STRING LOCTYPE VIEW", f"STRING {x0 - 0.10}, {y1 + 0.02}",
          "STRING CHAR SIZE 1.3", f'STRING DEF "{BI}{rotulo}"']
    return b


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ts", type=int, nargs="+", default=list(ESTILO))
    a = ap.parse_args()
    cv = pd.read_csv(N18 / "geometry_during_fracture_curves.csv")
    cv = cv[cv.x_kind == "F"]
    falta = [t for t in a.ts if t not in set(cv.ts)]
    if falta:
        raise SystemExit(f"T_s ausentes do CSV: {falta}")
    SAIDA.mkdir(parents=True, exist_ok=True)
    dk, dn = SAIDA / "figure_8a_K_xy.dat", SAIDA / "figure_8b_N_xy.dat"
    escreve_dat(cv, a.ts, "K", dk)
    escreve_dat(cv, a.ts, "N", dn)
    fmax = float(cv[cv.ts.isin(a.ts)].x.max())
    xmax = 500 * (int(fmax // 500) + 1)
    b = ["PAGE SIZE 1000, 420"]
    b += painel(0, (0.12, 0.17, 1.17, 0.95), f"{BI}<K>/<K\\s0\\N>", (0.99, 1.07), 0.02, "(a)", xmax,
                a.ts, (0.93, 0.925))
    b += painel(1, (1.38, 0.17, 2.43, 0.95), f"{BI}<N>/<N\\s0\\N>", (0.76, 1.02), 0.05, "(b)", xmax,
                a.ts, (2.19, 0.55))
    roda(b, [[dk], [dn]], SAIDA / "figure_8.agr", SAIDA / "figure_8.pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

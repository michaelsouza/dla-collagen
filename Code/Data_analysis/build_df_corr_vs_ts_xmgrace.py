#!/usr/bin/env python3
"""Figura do manuscrito: dimensao de correlacao corrigida D_2 contra T_s (en-US).

Uma serie so, azul, com barra = erro-padrao entre as sementes (n_seeds do
summary: 40 em T_s = 16; 15 em T_s = 2, 8, 4096, 8192; 5 nos outros); linhas de
referencia em 2 (disco) e 1.71 (DLA plano). D_2 corrigida = D_2 medida em
4 <= r <= R_bar/3 na secao final, menos a do disco uniforme de mesmo n e R_bar,
mais 2 (controle de borda). Ver Reviews/N18_df_ten_ts/README.md, secao 1.

Le:      Reviews/N18_df_ten_ts/df_periodic_summary.csv
Com --estimator gyr, a mesma figura com o raio de giracao na ordem de adesao
(gyr_primary: log N contra log R_g, 40 <= N <= N_max/2, 30 pontos por oitava),
em df_gyr_vs_ts.*; e a figura de comparacao interna, nao a do artigo.

Escreve: Reviews/N18_df_ten_ts/xmgrace/df_corr_vs_ts_xydy.dat, df_reference_lines_xy.dat
         Reviews/N18_df_ten_ts/xmgrace/df_corr_vs_ts.agr  e  .pdf
         (--estimator gyr) Reviews/N18_df_ten_ts/xmgrace/df_gyr_vs_ts_xydy.dat, .agr, .pdf
Chamado: à mão, depois de measure_df_periodic_ten_ts.py
"""
import argparse
import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_xmgrace_projects import GROSSURA_EIXO, ROTULO, TIQUE, roda  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[2]
N18 = RAIZ / "Reviews" / "N18_df_ten_ts"
SAIDA = N18 / "xmgrace"
AZUL = 4
ESTIMADORES = {
    "corr": dict(col="corr_primary", stem="df_corr_vs_ts",
                 cab=["# Correlation dimension D_f of the fibril cross-section versus surface-diffusion parameter T_s",
                      "# Columns: T_s   D_f (correlation dimension, raw)   SE over seeds"],
                 metodo=["# D_f = slope of log C(r) vs log r for 4 <= r <= R_bar/3; C(r) = fraction of point pairs at distance <= r.",
                         "# No boundary correction; a uniform disc with the same n and R_bar gives 1.93-1.95 in this window."]),
    "gyr": dict(col="gyr_primary", stem="df_gyr_vs_ts",
                cab=["# Fractal dimension D_f from the radius of gyration in attachment order versus T_s",
                     "# Columns: T_s   D_f (gyration, N ~ R_g^D_f)   SE over seeds"],
                metodo=["# D_f = slope of log N vs log R_g(N) for the first N molecules of the section (uid order),",
                        "# 40 <= N <= N_max/2 = 2500, 30 fit points per octave equally spaced in log N."]),
}


def exporta(est: dict) -> list[tuple[int, float, float]]:
    col = est["col"]
    with open(N18 / "df_periodic_summary.csv", encoding="utf-8") as fh:
        linhas = list(csv.DictReader(l for l in fh if not l.startswith("#")))
    pontos = [(int(r["ts"]), float(r[f"{col}_mean"]), float(r[f"{col}_se"]))
              for r in linhas]
    n_por_ts = ", ".join(f"{r['ts']}: {r['n_seeds']}" for r in sorted(linhas, key=lambda r: int(r["ts"])))
    pontos.sort()
    out = est["cab"] + [
           f"# Seeds per T_s: {n_por_ts}",
           "# Periodic cylinders (period 216, nb = 60000), 12 sections per cylinder, ~5000 molecules per section."]
    out += est["metodo"]
    out += [f"# Source: Reviews/N18_df_ten_ts/df_periodic_summary.csv ({col}_mean, _se). Use a logarithmic x axis.",
            "@type xydy"]
    out += [f"{ts} {v:.4f} {e:.4f}" for ts, v, e in pontos] + ["&"]
    (SAIDA / f"{est['stem']}_xydy.dat").write_text("\n".join(out) + "\n", encoding="utf-8")
    ref = ["# Reference lines: uniform disc (2) and planar DLA (1.71)",
           "@type xy", "# disc", "1.4 2", "13000 2", "&", "@type xy", "# planar DLA", "1.4 1.71", "13000 1.71", "&"]
    (SAIDA / "df_reference_lines_xy.dat").write_text("\n".join(ref) + "\n", encoding="utf-8")
    return pontos


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--estimator", choices=sorted(ESTIMADORES), default="corr")
    est = ESTIMADORES[ap.parse_args().estimator]
    SAIDA.mkdir(exist_ok=True)
    pontos = exporta(est)
    b = ["PAGE SIZE 600, 450",
         "WITH G0", "VIEW 0.22, 0.18, 1.28, 0.92",
         f"FRAME LINEWIDTH {GROSSURA_EIXO}",
         "XAXES SCALE LOGARITHMIC", "WORLD XMIN 1.4", "WORLD XMAX 13000", "WORLD YMIN 1.6", "WORLD YMAX 2.05",
         "XAXIS TICK MAJOR 10", "XAXIS TICK MINOR TICKS 8",
         "XAXIS TICKLABEL FORMAT POWER", "XAXIS TICKLABEL PREC 0",
         "YAXIS TICK MAJOR 0.1", "YAXIS TICK MINOR TICKS 1",
         'XAXIS LABEL "\\3T\\ss\\N"', f"XAXIS LABEL CHAR SIZE {ROTULO}", f"XAXIS TICKLABEL CHAR SIZE {TIQUE}",
         'YAXIS LABEL "\\3D\\sf\\N"', f"YAXIS LABEL CHAR SIZE {ROTULO}", f"YAXIS TICKLABEL CHAR SIZE {TIQUE}"]
    for eixo in ("XAXIS", "YAXIS"):
        b += [f"{eixo} BAR LINEWIDTH {GROSSURA_EIXO}", f"{eixo} TICK MAJOR LINEWIDTH {GROSSURA_EIXO}",
              f"{eixo} TICK MINOR LINEWIDTH {GROSSURA_EIXO}", f"{eixo} TICK MAJOR SIZE 1.4", f"{eixo} TICK MINOR SIZE 0.8"]
    b += ["LEGEND OFF",
          "S0 SYMBOL 1", "S0 SYMBOL SIZE 1.3", f"S0 SYMBOL COLOR {AZUL}", f"S0 SYMBOL FILL COLOR {AZUL}",
          "S0 SYMBOL FILL PATTERN 1", "S0 SYMBOL LINEWIDTH 2.0",
          f"S0 LINE COLOR {AZUL}", "S0 LINE LINEWIDTH 2.6",
          "S0 ERRORBAR ON", f"S0 ERRORBAR COLOR {AZUL}", "S0 ERRORBAR SIZE 0.8", "S0 ERRORBAR LINEWIDTH 2.0",
          "S0 ERRORBAR RISER LINEWIDTH 2.0",
          "S1 SYMBOL 0", "S1 LINE LINESTYLE 3", "S1 LINE LINEWIDTH 1.5", "S1 LINE COLOR 1",
          "S2 SYMBOL 0", "S2 LINE LINESTYLE 2", "S2 LINE LINEWIDTH 1.5", "S2 LINE COLOR 1",
          "WITH STRING", "STRING ON", "STRING LOCTYPE WORLD", "STRING 1.8, 2.01", "STRING CHAR SIZE 1.4",
          "STRING FONT 0", 'STRING DEF "uniform disc, 2"',
          "WITH STRING", "STRING ON", "STRING LOCTYPE WORLD", "STRING 1.8, 1.64", "STRING CHAR SIZE 1.4",
          "STRING FONT 0", 'STRING DEF "planar DLA, 1.71"']
    roda(b, [[SAIDA / f"{est['stem']}_xydy.dat", SAIDA / "df_reference_lines_xy.dat"]],
         SAIDA / f"{est['stem']}.agr", SAIDA / f"{est['stem']}.pdf")
    for ts, v, e in pontos:
        print(f"  T_s = {ts:>5}  D_f = {v:.3f} +- {e:.3f}")


if __name__ == "__main__":
    main()

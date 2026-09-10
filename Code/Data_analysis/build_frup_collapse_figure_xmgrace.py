#!/usr/bin/env python3
"""Monta a figura de colapso de F_rup em m: F_rup(T_s) por m, com dois insets.

Grafico principal: F_rup contra log10 T_s, uma serie por m, sem barra de erro.
Inset esquerdo:    F_rup / F_sat contra log10 T_s, as cinco series colapsadas.
Inset direito:     F_sat contra m, cinco pontos e o ajuste a (1 - exp(-m/b)).
F_sat(m) e o valor medido em T_s = 8192, nao o parametro a do ajuste.

Le:      Reviews/N9_damage_curves/damage_summary.csv
Escreve: Reviews/N9_damage_curves/xmgrace/frup_collapse_main_xy.dat
         Reviews/N9_damage_curves/xmgrace/frup_collapse_ratio_xy.dat
         Reviews/N9_damage_curves/xmgrace/frup_collapse_fsat_vs_m_xy.dat
         Reviews/N9_damage_curves/xmgrace/frup_collapse.agr  e  frup_collapse.pdf
Chamado: à mão; refazer se damage_summary.csv mudar
"""
import csv
import math
import pathlib
import sys

import numpy as np
from scipy.optimize import curve_fit

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_xmgrace_projects import GROSSURA_EIXO, PAINEL, ROTULO, TIQUE, roda  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[2]
DADOS = RAIZ / "Reviews" / "N9_damage_curves"
SAIDA = DADOS / "xmgrace"

MODULOS = [1, 2, 3, 5, 10]
TS_SAT = 8192
# estilo da Figura 7(a) de Michael: um azul so, simbolos preenchidos num azul
# claro, fonte 3 (Times-BoldItalic) nos rotulos. Simbolos do Grace:
# 1 circulo, 2 quadrado, 3 diamante, 4 triangulo para cima, 5 para a esquerda
AZUL = 4
AZUL_CLARO = 20          # cor definida no batch: MAP COLOR 20
SIMBOLOS = [1, 2, 3, 4, 5]


def ler() -> dict[tuple[int, int], float]:
    return {(int(r["ts"]), int(r["m"])): float(r["f_rup_mean"])
            for r in csv.DictReader(open(DADOS / "damage_summary.csv"))}


def saturacao(m: float, a: float, b: float) -> float:
    return a * (1.0 - np.exp(-m / b))


def escreve_dats(F: dict) -> tuple[float, float]:
    ts_grade = sorted({ts for ts, _ in F})
    fsat = {m: F[(TS_SAT, m)] for m in MODULOS}

    cab = ["# Source: Reviews/N9_damage_curves/damage_summary.csv (job 590854, SDumont2)",
           "# Each point averages 10^4 realizations (200 fibrils x 50 draws).",
           "# One set per Weibull modulus, in the order m = " + ", ".join(map(str, MODULOS))]
    principal = ["# Main panel: mean rupture force versus log10 T_s (no error bar)",
                 "# Columns: log10(T_s)  <F_rup>"] + cab
    razao = [f"# Left inset: F_rup / F_sat versus log10 T_s, F_sat = F_rup at T_s = {TS_SAT}",
             "# Columns: log10(T_s)  <F_rup>/F_sat"] + cab
    for m in MODULOS:
        principal += ["@type xy", f"# m = {m}"]
        razao += ["@type xy", f"# m = {m}"]
        for ts in ts_grade:
            x = math.log10(ts)
            principal.append(f"{x:.6f} {F[(ts, m)]:.4f}")
            razao.append(f"{x:.6f} {F[(ts, m)] / fsat[m]:.6f}")
        principal.append("&")
        razao.append("&")

    ms = np.array(MODULOS, float)
    (a, b), cov = curve_fit(saturacao, ms, np.array([fsat[m] for m in MODULOS]),
                            p0=[2500.0, 3.0])
    ea, eb = np.sqrt(np.diag(cov))
    pontos = [f"# Right inset: F_sat versus m, F_sat = F_rup at T_s = {TS_SAT}",
              "# Set 0: the five measured values. Set 1: fit a*(1-exp(-m/b)) sampled",
              f"# a = {a:.1f} +- {ea:.1f}, b = {b:.3f} +- {eb:.3f}",
              "# Columns: m  F_sat"] + cab[:2]
    pontos += ["@type xy", "# measured"]
    pontos += [f"{m:d} {fsat[m]:.4f}" for m in MODULOS] + ["&"]
    pontos += ["@type xy", "# fit"]
    pontos += [f"{x:.3f} {saturacao(x, a, b):.4f}" for x in np.linspace(0.5, 11.0, 106)]
    pontos.append("&")

    for nome, linhas in [("frup_collapse_main_xy.dat", principal),
                         ("frup_collapse_ratio_xy.dat", razao),
                         ("frup_collapse_fsat_vs_m_xy.dat", pontos)]:
        (SAIDA / nome).write_text("\n".join(linhas) + "\n", encoding="utf-8")
        print(f"  {nome}: {linhas.count('&')} series")
    return a, b


def eixos(g: int, vista: tuple, xlab: str, ylab: str, rotulo: float, tique: float,
          mundo: tuple, xmaj: float, ymaj: float) -> list[str]:
    vx0, vy0, vx1, vy1 = vista
    x0, x1, y0, y1 = mundo
    return [f"WITH G{g}", f"VIEW {vx0}, {vy0}, {vx1}, {vy1}",
            f"WORLD XMIN {x0}", f"WORLD XMAX {x1}", f"WORLD YMIN {y0}", f"WORLD YMAX {y1}",
            f"FRAME LINEWIDTH {GROSSURA_EIXO}",
            f'XAXIS LABEL "\\3{xlab}"', f"XAXIS LABEL CHAR SIZE {rotulo}",
            f"XAXIS TICKLABEL CHAR SIZE {tique}",
            f"XAXIS BAR LINEWIDTH {GROSSURA_EIXO}",
            f"XAXIS TICK MAJOR LINEWIDTH {GROSSURA_EIXO}",
            f"XAXIS TICK MINOR LINEWIDTH {GROSSURA_EIXO}",
            f"XAXIS TICK MAJOR {xmaj}", "XAXIS TICK MINOR TICKS 1",
            "XAXIS TICK MAJOR SIZE 1.4", "XAXIS TICK MINOR SIZE 0.8",
            f'YAXIS LABEL "\\3{ylab}"', f"YAXIS LABEL CHAR SIZE {rotulo}",
            f"YAXIS TICKLABEL CHAR SIZE {tique}",
            f"YAXIS BAR LINEWIDTH {GROSSURA_EIXO}",
            f"YAXIS TICK MAJOR LINEWIDTH {GROSSURA_EIXO}",
            f"YAXIS TICK MINOR LINEWIDTH {GROSSURA_EIXO}",
            f"YAXIS TICK MAJOR {ymaj}", "YAXIS TICK MINOR TICKS 1",
            "YAXIS TICK MAJOR SIZE 1.4", "YAXIS TICK MINOR SIZE 0.8",
            "LEGEND OFF"]


def serie_m(g: int, i: int, legenda: str, tamanho: float, linha: float) -> list[str]:
    return [f"WITH G{g}",
            f"S{i} SYMBOL {SIMBOLOS[i]}", f"S{i} SYMBOL SIZE {tamanho}",
            f"S{i} SYMBOL COLOR {AZUL}", f"S{i} SYMBOL FILL COLOR {AZUL_CLARO}",
            f"S{i} SYMBOL FILL PATTERN 1",
            f"S{i} SYMBOL LINEWIDTH 2.0",
            f"S{i} LINE COLOR {AZUL}", f"S{i} LINE LINEWIDTH {linha}",
            f'S{i} LEGEND "{legenda}"']


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    F = ler()
    a, b = escreve_dats(F)

    # pagina 720 x 600: vista x em [0, 1.2], y em [0, 1]
    # o teto de y deixa a faixa superior do grafico livre para os dois insets:
    # a maior forca (2495) fica em 60% da altura
    b_ = ["PAGE SIZE 720, 600", f'MAP COLOR {AZUL_CLARO} TO (165, 190, 245), "lightblue"']
    b_ += eixos(0, (0.20, 0.14, 1.14, 0.94), "log\\s10\\N T\\ss\\N", "F\\srup\\N",
                ROTULO, TIQUE, (0.0, 4.2, 0.0, 4200.0), 1.0, 1000.0)
    b_ += ["LEGEND ON", "LEGEND BOX LINESTYLE 1", "LEGEND BOX FILL PATTERN 1",
           "LEGEND BOX FILL COLOR 0", "LEGEND CHAR SIZE 1.5",
           "LEGEND LOCTYPE VIEW", "LEGEND 0.31, 0.61"]
    for i, m in enumerate(MODULOS):
        b_ += serie_m(0, i, f"m = {m}", 1.3, 2.6)

    # inset esquerdo: colapso
    b_ += eixos(1, (0.33, 0.70, 0.66, 0.92), "log\\s10\\N T\\ss\\N", "F\\srup\\N / F\\ssat\\N",
                1.2, 1.0, (0.0, 4.2, 0.0, 1.15), 1.0, 0.5)
    for i, m in enumerate(MODULOS):
        b_ += serie_m(1, i, "", 0.75, 1.6)

    # inset direito: F_sat(m) e ajuste
    b_ += eixos(2, (0.80, 0.70, 1.13, 0.92), "m", "F\\ssat\\N",
                1.2, 1.0, (0.0, 11.5, 500.0, 2800.0), 5.0, 1000.0)
    b_ += ["WITH G2", "S0 SYMBOL 1", "S0 SYMBOL SIZE 0.8", "S0 SYMBOL COLOR 1",
           "S0 SYMBOL FILL COLOR 1", "S0 SYMBOL FILL PATTERN 1", "S0 LINE TYPE 0",
           "S1 SYMBOL 0", "S1 LINE COLOR 1", "S1 LINE LINEWIDTH 1.6",
           "WITH STRING", "STRING ON", "STRING LOCTYPE VIEW", "STRING 0.865, 0.725",
           "STRING CHAR SIZE 0.85", "STRING FONT 0",
           'STRING DEF "F\\ssat\\N = a (1 - e\\S-m/b\\N)"']
    roda(b_, [[SAIDA / "frup_collapse_main_xy.dat"],
              [SAIDA / "frup_collapse_ratio_xy.dat"],
              [SAIDA / "frup_collapse_fsat_vs_m_xy.dat"]],
         SAIDA / "frup_collapse.agr", SAIDA / "frup_collapse.pdf")
    print(f"  ajuste do inset: a = {a:.0f}, b = {b:.2f}")


if __name__ == "__main__":
    main()

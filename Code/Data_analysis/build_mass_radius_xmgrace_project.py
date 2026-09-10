#!/usr/bin/env python3
"""Monta o projeto .agr da curva massa-raio dos cilindros periodicos largos.

Le:      Reviews/PhaseC_periodic_cylinder/xmgrace/mass_radius_by_ts_xy.dat
Escreve: Reviews/PhaseC_periodic_cylinder/xmgrace/mass_radius_by_ts.agr
         Reviews/PhaseC_periodic_cylinder/xmgrace/mass_radius_by_ts.pdf
Chamado: à mão, depois de export_periodic_cylinder_mass_radius_xmgrace.py

Figura interna (nao entra no manuscrito): <m(R)> contra R em log-log, uma
serie por T_s, com duas retas-guia de inclinacao 2 (disco cheio) e 1,68
(DLA plano, o valor medido em T_s=2 na janela relativa). Estilo e funcoes
de build_xmgrace_projects.py.
"""
import pathlib
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_xmgrace_projects import (  # noqa: E402
    GROSSURA_EIXO, LEGENDA, PAINEL, ROTULO, TIQUE, RAIZ,
    blocos, cores, escreve_marcadores, esparso_log, marcador, roda, serie,
)

PASTA = RAIZ / "Reviews" / "PhaseC_periodic_cylinder" / "xmgrace"
TS = [2, 128, 8192]
# inclinacao, legenda, curva que ancora (indice em TS), fator vertical, estilo de linha
GUIAS = [(2.0, "R\\S2\\N", 2, 2.2, 3), (1.68, "R\\S1.68\\N", 0, 0.45, 2)]
R_GUIA = (3.0, 40.0)                                 # alcance das retas-guia


def moldura_unica(x_leg: float, y_leg: float) -> list[str]:
    """Um painel so, na mesma vista do painel (a) das figuras de duas colunas."""
    vx0, vy0, vx1, vy1 = 0.28, 0.30, 1.06, 0.86
    return ["WITH G0", f"VIEW {vx0}, {vy0}, {vx1}, {vy1}",
            f"FRAME LINEWIDTH {GROSSURA_EIXO}",
            'XAXIS LABEL "\\3R"', f"XAXIS LABEL CHAR SIZE {ROTULO}",
            f"XAXIS TICKLABEL CHAR SIZE {TIQUE}",
            f"XAXIS BAR LINEWIDTH {GROSSURA_EIXO}",
            f"XAXIS TICK MAJOR LINEWIDTH {GROSSURA_EIXO}",
            f"XAXIS TICK MINOR LINEWIDTH {GROSSURA_EIXO}",
            "XAXIS TICK MAJOR SIZE 1.4", "XAXIS TICK MINOR SIZE 0.8",
            'YAXIS LABEL "\\3<m(R)>"', f"YAXIS LABEL CHAR SIZE {ROTULO}",
            f"YAXIS TICKLABEL CHAR SIZE {TIQUE}",
            f"YAXIS BAR LINEWIDTH {GROSSURA_EIXO}",
            f"YAXIS TICK MAJOR LINEWIDTH {GROSSURA_EIXO}",
            f"YAXIS TICK MINOR LINEWIDTH {GROSSURA_EIXO}",
            "YAXIS TICK MAJOR SIZE 1.4", "YAXIS TICK MINOR SIZE 0.8",
            "XAXES SCALE LOGARITHMIC", "YAXES SCALE LOGARITHMIC",
            "WORLD XMIN 0.9", "WORLD XMAX 250", "WORLD YMIN 0.7", "WORLD YMAX 12000",
            "XAXIS TICK MAJOR 10", "XAXIS TICK MINOR TICKS 8",
            "YAXIS TICK MAJOR 10", "YAXIS TICK MINOR TICKS 8",
            "YAXIS TICKLABEL FORMAT POWER", "YAXIS TICKLABEL PREC 0",
            "LEGEND ON", "LEGEND BOX LINESTYLE 0", "LEGEND BOX FILL PATTERN 0",
            f"LEGEND CHAR SIZE {LEGENDA}", "LEGEND LOCTYPE VIEW",
            f"LEGEND {x_leg:.3f}, {y_leg:.3f}"]


def guia(s: int, inclinacao: float, legenda: str, curvas, ancora: int, fator: float,
         estilo: int) -> tuple[list[str], list[tuple[float, float]]]:
    """Reta de inclinacao dada, ancorada na curva `ancora` em R = R_GUIA[0] e
    deslocada de `fator` na vertical, para nao cobrir os pontos."""
    r0, r1 = R_GUIA
    m0 = next(m for r, m in curvas[ancora] if r == r0) * fator
    pontos = [(r0, m0), (r1, m0 * (r1 / r0) ** inclinacao)]
    cmds = ["WITH G0", f"S{s} LINE COLOR 1", f"S{s} LINE LINESTYLE {estilo}",
            f"S{s} LINE LINEWIDTH 2.0", f"S{s} SYMBOL 0", f'S{s} LEGEND "{legenda}"']
    return cmds, pontos


def main() -> None:
    if not shutil.which("gracebat"):
        sys.exit("gracebat nao encontrado (pacote grace)")
    dat = PASTA / "mass_radius_by_ts_xy.dat"
    curvas = blocos(dat)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        marcas = tmp / "marcadores.dat"
        escreve_marcadores(marcas, [esparso_log(p, i, len(TS)) for i, p in enumerate(curvas)])
        b = ["PAGE SIZE 500, 400"] + cores() + moldura_unica(0.36, 0.83)
        n = len(TS)
        for i, ts in enumerate(TS):
            b += serie(0, i, "", com_simbolo=False, barra=False)
            b += marcador(0, n + i, i, f"T\\ss\\N = {ts}")
        guias_pts = []
        for j, (incl, leg, anc, fator, estilo) in enumerate(GUIAS):
            cmds, pts = guia(2 * n + j, incl, leg, curvas, anc, fator, estilo)
            b += cmds
            guias_pts.append(pts)
        guias_dat = tmp / "guias.dat"
        escreve_marcadores(guias_dat, guias_pts)
        roda(b, [[dat, marcas, guias_dat]],
             PASTA / "mass_radius_by_ts.agr", PASTA / "mass_radius_by_ts.pdf")


if __name__ == "__main__":
    main()

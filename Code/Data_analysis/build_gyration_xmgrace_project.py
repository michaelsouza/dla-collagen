#!/usr/bin/env python3
"""Monta o projeto .agr de R_g(N) dos cilindros periodicos largos.

Le:      Reviews/PhaseC_periodic_cylinder/xmgrace/gyration_by_ts_xy.dat
Escreve: Reviews/PhaseC_periodic_cylinder/xmgrace/gyration_by_ts.agr
         Reviews/PhaseC_periodic_cylinder/xmgrace/gyration_by_ts.pdf
Chamado: à mão, depois de export_periodic_cylinder_gyration_xmgrace.py

Figura interna: <R_g(N)> contra N em log-log, uma serie por T_s, com duas
retas-guia N^{1/2} (disco cheio) e N^{1/1.70} (DLA plano). Mesma moldura e
mesmas funcoes de build_mass_radius_xmgrace_project.py.
"""
import pathlib
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_xmgrace_projects import (  # noqa: E402
    RAIZ, blocos, cores, escreve_marcadores, esparso_log, marcador, roda, serie,
)
from build_mass_radius_xmgrace_project import moldura_unica  # noqa: E402

PASTA = RAIZ / "Reviews" / "PhaseC_periodic_cylinder" / "xmgrace"
TS = [2, 128, 8192]
# expoente de N, legenda, curva que ancora (indice em TS), fator vertical, estilo
GUIAS = [(1 / 1.70, "N\\S1/1.70\\N", 0, 1.8, 2), (0.5, "N\\S1/2\\N", 2, 0.55, 3)]
N_GUIA = (40.0, 2000.0)


def guia(s, expoente, legenda, curvas, ancora, fator, estilo):
    n0, n1 = N_GUIA
    r0 = next(r for n, r in curvas[ancora] if n == n0) * fator
    pontos = [(n0, r0), (n1, r0 * (n1 / n0) ** expoente)]
    cmds = ["WITH G0", f"S{s} LINE COLOR 1", f"S{s} LINE LINESTYLE {estilo}",
            f"S{s} LINE LINEWIDTH 2.0", f"S{s} SYMBOL 0", f'S{s} LEGEND "{legenda}"']
    return cmds, pontos


def main() -> None:
    if not shutil.which("gracebat"):
        sys.exit("gracebat nao encontrado (pacote grace)")
    dat = PASTA / "gyration_by_ts_xy.dat"
    curvas = blocos(dat)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        marcas = tmp / "marcadores.dat"
        escreve_marcadores(marcas, [esparso_log(p, i, len(TS), por_decada=4)
                                    for i, p in enumerate(curvas)])
        b = ["PAGE SIZE 500, 400"] + cores() + moldura_unica(0.36, 0.83)
        b += ['XAXIS LABEL "\\3N"', 'YAXIS LABEL "\\3<R\\sg\\N(N)>"',
              "WORLD XMIN 0.9", "WORLD XMAX 8000", "WORLD YMIN 0.4", "WORLD YMAX 200",
              "YAXIS TICKLABEL FORMAT DECIMAL", "YAXIS TICKLABEL PREC 0"]
        n = len(TS)
        for i, ts in enumerate(TS):
            b += serie(0, i, "", com_simbolo=False, barra=False)
            b += marcador(0, n + i, i, f"T\\ss\\N = {ts}")
        guias_pts = []
        for j, (exp, leg, anc, fator, estilo) in enumerate(GUIAS):
            cmds, pts = guia(2 * n + j, exp, leg, curvas, anc, fator, estilo)
            b += cmds
            guias_pts.append(pts)
        guias_dat = tmp / "guias.dat"
        escreve_marcadores(guias_dat, guias_pts)
        roda(b, [[dat, marcas, guias_dat]],
             PASTA / "gyration_by_ts.agr", PASTA / "gyration_by_ts.pdf")


if __name__ == "__main__":
    main()

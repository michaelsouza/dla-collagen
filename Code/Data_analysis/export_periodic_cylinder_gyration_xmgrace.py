#!/usr/bin/env python3
"""D_f pelo raio de giracao na ordem de crescimento, cilindros periodicos largos.

Le:      dla_per216_mode_s_ts_<TS>_nb_60000_seed_<SEED>_.dat (diretorio via
         --cylinders; receita no cabecalho de
         Reviews/PhaseC_periodic_cylinder/df_wide_cylinders.csv)
Escreve: Reviews/PhaseC_periodic_cylinder/xmgrace/gyration_by_ts_xy.dat
         Reviews/PhaseC_periodic_cylinder/df_gyration_wide_cylinders.csv
         Reviews/PhaseC_periodic_cylinder/df_gyration_local_slopes.csv
Chamado: à mão, depois de gerar os cilindros (mesmos quinze de
         export_periodic_cylinder_mass_radius_xmgrace.py, que confere a
         identidade deles contra df_wide_cylinders.csv)

Metodo (Witten & Sander 1981; Vicsek 1992, cap. 2): o uid e a ordem de adesao.
Em cada secao transversal (uma a cada 18 camadas do anel, 12 por cilindro),
tomam-se os bastoes que a cruzam, na ordem em que aderiram, e calcula-se o
raio de giracao R_g(N) das posicoes (x, z) dos N primeiros. Num fractal de
crescimento, N ~ R_g^{D_f}. D_f e a inclinacao de log10 N contra log10 R_g.

R_g(N) e mediado sobre as 12 secoes de cada semente; o ajuste e feito por
semente e a tabela traz media e erro-padrao entre as cinco. Tres janelas em
N, fixadas antes de olhar o resultado por semente: 40-320 (miolo, meia decada
acima da rede), 320-5000 (periferia) e 40-5000 (tudo). A inclinacao local por
oitava de N vai no segundo CSV, para que a escolha da janela seja auditavel.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import re
import sys

import numpy as np

RAIZ = pathlib.Path(__file__).resolve().parents[2]
FASE_C = RAIZ / "Reviews" / "PhaseC_periodic_cylinder"
SAIDA_DAT = FASE_C / "xmgrace" / "gyration_by_ts_xy.dat"
SAIDA_DF = FASE_C / "df_gyration_wide_cylinders.csv"
SAIDA_LOCAL = FASE_C / "df_gyration_local_slopes.csv"

NOME = re.compile(r"dla_per(\d+)_mode_s_ts_(\d+)_nb_(\d+)_seed_(\d+)_\.dat$")
TS_ORDEM = [2, 128, 8192]
ALTURA = 18
JANELAS = {"N_40_320": (40, 320), "N_320_5000": (320, 5000), "N_40_5000": (40, 5000)}
OITAVAS = [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5000]


def bastoes_em_ordem(caminho: pathlib.Path) -> list[tuple[int, int, int, int]]:
    """(uid, x, y, z) na ordem de adesao."""
    out = []
    with open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            p = linha.split()
            if len(p) >= 5 and p[0].startswith("uid"):
                out.append((int(p[1]), int(p[2]), int(p[3]), int(p[4])))
    out.sort()
    return out


def rg_por_secao(bastoes, periodo: int) -> list[np.ndarray]:
    """R_g(N) de cada secao, N = 1 .. numero de bastoes que a cruzam."""
    curvas = []
    for camada in range(0, periodo, ALTURA):
        xz = np.array([(x, z) for _u, x, y, z in bastoes if (camada - y) % periodo < ALTURA], float)
        n = np.arange(1, len(xz) + 1)
        media = np.cumsum(xz, axis=0) / n[:, None]
        rg2 = np.cumsum(xz ** 2, axis=0).sum(axis=1) / n - (media ** 2).sum(axis=1)
        curvas.append(np.sqrt(np.maximum(rg2, 0.0)))
    return curvas


def media_por_n(curvas: list[np.ndarray]) -> np.ndarray:
    """Media de R_g em cada N sobre as curvas que chegam ate ele."""
    n_max = max(len(c) for c in curvas)
    soma, cont = np.zeros(n_max), np.zeros(n_max)
    for c in curvas:
        soma[: len(c)] += c
        cont[: len(c)] += 1
    return soma / cont


def inclinacao(rg: np.ndarray, lo: int, hi: int) -> float:
    n = np.arange(1, len(rg) + 1)
    w = (n >= lo) & (n <= hi) & (rg > 0)
    return float(np.polyfit(np.log10(rg[w]), np.log10(n[w]), 1)[0])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cylinders", type=pathlib.Path, required=True)
    args = ap.parse_args()

    por_ts: dict[int, dict[int, np.ndarray]] = {ts: {} for ts in TS_ORDEM}
    for f in sorted(args.cylinders.glob("dla_per*_.dat")):
        m = NOME.match(f.name)
        if not m:
            continue
        periodo, ts, _nb, seed = (int(g) for g in m.groups())
        por_ts[ts][seed] = media_por_n(rg_por_secao(bastoes_em_ordem(f), periodo))
        print(f"  T_s={ts:5d} seed={seed}  N_max={len(por_ts[ts][seed])}  "
              f"R_g(N_max)={por_ts[ts][seed][-1]:.2f}")

    linhas_df = [["Ts", "janela", "N_lo", "N_hi", "n_seeds", "df_mean", "df_se"] +
                 [f"df_seed_{i + 1}" for i in range(5)]]
    linhas_local = [["Ts", "N_lo", "N_hi", "df_local_mean", "df_local_se"]]
    linhas_dat = ["# Radius of gyration of the first N rods crossing a section, in attachment order",
                  "# Columns: N   <R_g(N)>   (mean over 12 sections x 5 seeds)",
                  "# Set order: T_s = 2, 128, 8192. Fractal growth: N ~ R_g^{D_f}.",
                  "# Use logarithmic axes on both.",
                  "@type xy"]
    for ts in TS_ORDEM:
        sementes = por_ts[ts]
        for nome, (lo, hi) in JANELAS.items():
            vals = [inclinacao(rg, lo, hi) for _s, rg in sorted(sementes.items())]
            linhas_df.append([ts, nome, lo, hi, len(vals), f"{np.mean(vals):.4f}",
                              f"{np.std(vals, ddof=1) / np.sqrt(len(vals)):.4f}"] + [f"{v:.4f}" for v in vals])
        for lo, hi in zip(OITAVAS[:-1], OITAVAS[1:]):
            vals = [inclinacao(rg, lo, hi) for rg in sementes.values()]
            linhas_local.append([ts, lo, hi, f"{np.mean(vals):.4f}",
                                 f"{np.std(vals, ddof=1) / np.sqrt(len(vals)):.4f}"])
        rg = media_por_n(list(sementes.values()))
        linhas_dat.append(f"# T_s = {ts}")
        linhas_dat += [f"{n} {r:.4f}" for n, r in enumerate(rg, start=1)]
        linhas_dat.append("&")

    SAIDA_DAT.parent.mkdir(exist_ok=True)
    SAIDA_DAT.write_text("\n".join(linhas_dat) + "\n", encoding="utf-8")
    cabecalho = ("# D_f pelo raio de giracao na ordem de crescimento, cilindros periodicos "
                 "largos (os mesmos de df_wide_cylinders.csv). Ajuste de log10 N contra "
                 "log10 R_g por semente; media e erro-padrao entre 5 sementes. "
                 "Gerado por export_periodic_cylinder_gyration_xmgrace.py em 2026-09-09.\n")
    for caminho, linhas in ((SAIDA_DF, linhas_df), (SAIDA_LOCAL, linhas_local)):
        with open(caminho, "w", newline="", encoding="utf-8") as fh:
            fh.write(cabecalho)
            csv.writer(fh).writerows(linhas)
    print("escrito:", *(p.relative_to(RAIZ) for p in (SAIDA_DAT, SAIDA_DF, SAIDA_LOCAL)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

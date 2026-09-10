#!/usr/bin/env python3
"""Curva massa-raio <m(R)> dos cilindros periodicos largos, para o xmgrace.

Le:      dla_per216_mode_s_ts_<TS>_nb_60000_seed_<SEED>_.dat (diretorio via
         --cylinders; receita de regeneracao no cabecalho de
         Reviews/PhaseC_periodic_cylinder/df_wide_cylinders.csv)
Escreve: Reviews/PhaseC_periodic_cylinder/xmgrace/mass_radius_by_ts_xy.dat
         Reviews/PhaseC_periodic_cylinder/xmgrace/mass_radius_curves.csv
Chamado: à mão, depois de gerar os cilindros; conferido contra as colunas
         fixa_4_8 e relativa_0p15R_0p5R de df_wide_cylinders.csv antes de
         escrever (o R_max daquele CSV foi gravado por outra regra e fica
         2-4% abaixo da distancia maxima de particula; os D_f, nao)

Mesmo metodo de measure_df_periodic.py (e do manuscrito, paper_PRE.tex:141):
secoes a cada 18 camadas do anel de periodo 216 (12 secoes), massa m(R) =
numero de particulas a distancia <= R do centro de massa da secao, media
sobre as secoes e sobre as sementes. Aqui R vai de 1 ate o maior R_max da
condicao, porque a figura mostra a curva inteira, inclusive a saturacao; a
janela de ajuste e assunto de df_wide_cylinders.csv, nao desta figura.
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
SAIDA = FASE_C / "xmgrace"
sys.path.insert(0, str(FASE_C))
from measure_df_periodic import carregar, particulas_por_camada  # noqa: E402

NOME = re.compile(r"dla_per(\d+)_mode_s_ts_(\d+)_nb_(\d+)_seed_(\d+)_\.dat$")
TS_ORDEM = [2, 128, 8192]
PASSO = 18


def secoes_do_cilindro(caminho: pathlib.Path, periodo: int) -> list[np.ndarray]:
    cam = particulas_por_camada(carregar(str(caminho)), periodo)
    return [cam[y] for y in range(0, periodo, PASSO) if y in cam]


def massa_por_secao(secoes: list[np.ndarray], raios: np.ndarray) -> tuple[np.ndarray, list[float]]:
    """Uma linha de m(R) por secao, e o raio maximo de cada secao."""
    massas, rmax = [], []
    for s in secoes:
        d = np.sort(np.sqrt(((s - s.mean(axis=0)) ** 2).sum(axis=1)))
        massas.append(np.searchsorted(d, raios, side="right").astype(float))
        rmax.append(float(d[-1]))
    return np.vstack(massas), rmax


def inclinacao(raios: np.ndarray, m: np.ndarray, lo: float, hi: float) -> float:
    w = (raios >= lo) & (raios <= hi) & (m > 0)
    return float(np.polyfit(np.log10(raios[w]), np.log10(m[w]), 1)[0])


def registrado_por_cilindro() -> dict[tuple[int, int], dict]:
    out = {}
    with open(FASE_C / "df_wide_cylinders.csv", encoding="utf-8") as fh:
        for row in csv.DictReader(l for l in fh if not l.startswith("#")):
            if row["objeto"] == "cilindro_periodico":
                out[(int(row["Ts"]), int(row["seed"]))] = row
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cylinders", type=pathlib.Path, required=True)
    args = ap.parse_args()

    registrado = registrado_por_cilindro()
    raios = np.arange(1.0, 200.0)
    por_ts: dict[int, list[np.ndarray]] = {ts: [] for ts in TS_ORDEM}
    r_max_por_ts: dict[int, list[float]] = {ts: [] for ts in TS_ORDEM}
    conferidos = 0
    for f in sorted(args.cylinders.glob("dla_per*_.dat")):
        m = NOME.match(f.name)
        if not m:
            continue
        periodo, ts, _nb, seed = (int(g) for g in m.groups())
        secoes = secoes_do_cilindro(f, periodo)
        massas, rmax = massa_por_secao(secoes, raios)
        media, r_medio = massas.mean(axis=0), float(np.mean(rmax))
        fixa = inclinacao(raios, media, 4.0, 8.0)
        rel = inclinacao(raios, media, 0.15 * r_medio, 0.5 * r_medio)
        ref = registrado.get((ts, seed))
        ok = (ref is not None
              and abs(fixa - float(ref["fixa_4_8"])) < 1e-3
              and abs(rel - float(ref["relativa_0p15R_0p5R"])) < 1e-3)
        conferidos += ok
        print(f"  T_s={ts:5d} seed={seed}  secoes={len(secoes):2d}  R_max={max(rmax):8.3f}  "
              f"D_f fixa={fixa:.4f} rel={rel:.4f}  registrado="
              f"{float(ref['fixa_4_8']):.4f}/{float(ref['relativa_0p15R_0p5R']):.4f}  "
              f"{'ok' if ok else 'DIFERE'}")
        por_ts[ts].append(massas)
        r_max_por_ts[ts].append(max(rmax))

    n_esperado = len(registrado)
    if conferidos != n_esperado:
        sys.exit(f"D_f confere em {conferidos} de {n_esperado} cilindros; nao escrevo.")

    SAIDA.mkdir(exist_ok=True)
    linhas_dat = ["# Mass-radius curve of the wide periodic cylinders (period 216, nb = 60000)",
                  "# Columns: R   <m(R)>   (mean over 12 sections x 5 seeds)",
                  "# Set order: T_s = 2, 128, 8192. Points stop at the largest R_max of",
                  "# the condition; m saturates at the section mass (5000) before that.",
                  "# Use logarithmic axes on both.",
                  "@type xy"]
    linhas_csv = [["ts", "R", "mean_mass", "sd_mass_over_sections", "n_sections"]]
    for ts in TS_ORDEM:
        todas = np.vstack(por_ts[ts])              # (n_secoes_total, n_raios)
        media, sd = todas.mean(axis=0), todas.std(axis=0, ddof=1)
        w = raios <= np.ceil(max(r_max_por_ts[ts]))
        linhas_dat.append(f"# T_s = {ts}")
        for r, mm, ss in zip(raios[w], media[w], sd[w]):
            linhas_dat.append(f"{r:g} {mm:.4f}")
            linhas_csv.append([ts, f"{r:g}", f"{mm:.4f}", f"{ss:.4f}", todas.shape[0]])
        linhas_dat.append("&")
    (SAIDA / "mass_radius_by_ts_xy.dat").write_text("\n".join(linhas_dat) + "\n", encoding="utf-8")
    with open(SAIDA / "mass_radius_curves.csv", "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(linhas_csv)
    print(f"escrito em {SAIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

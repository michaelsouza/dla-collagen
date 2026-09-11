#!/usr/bin/env python3
"""Geometria inicial do tronco por T_s: <K> (moleculas por camada) e <N_i> (vizinhos por bastao).

Recorte 41x41 (half_width 20) por padrao, |y| <= 100, no cache .db do motor de
fratura (criado se faltar). K = ocupacao da camada y, media sobre as 201
camadas; N_i = numero de particulas vizinhas do bastao i (o N da probabilidade
de ruptura), media sobre os bastoes. Duas versoes: todos os bastoes do recorte
(all) e so os que portam carga depois de filter_rids (load), que e o conjunto
que o motor fratura. Media sobre sementes; erro = erro-padrao entre sementes.

Le:      <extended>/ts_<T>_seed_<S>.dat (+ .db / _w20_l100.db)
Escreve: Reviews/N18_df_ten_ts/trunk_geometry_by_seed.csv
         Reviews/N18_df_ten_ts/trunk_geometry_by_ts.csv
         Reviews/N18_df_ten_ts/figures/trunk_geometry_vs_ts.png
Chamado: à mão, depois do estagio A de run_local_width_fracture.sh
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "Code" / "Fracture_fibril"))
import stress_strain_ava as S  # noqa: E402

N18 = RAIZ / "Reviews" / "N18_df_ten_ts"
NOME = re.compile(r"ts_(\d+)_seed_(\d+)\.dat$")
TS = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]


def geometria(ssd) -> dict:
    n_layer = np.array([len(l.pids) for l in ssd.layers.values()], float)
    N = np.array([len(r.neigh_pids) for r in ssd.rods.values()], float)
    return dict(R=len(N), K_mean=float(n_layer.mean()), K_min=float(n_layer.min()),
                N_mean=float(N.mean()), N_median=float(np.median(N)), frac_N_le_5=float(np.mean(N <= 5)))


def medir(args) -> dict:
    caminho, hw = args
    ts, seed = (int(g) for g in NOME.match(caminho.name).groups())
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        ssd = S.read_or_create_ssd(str(caminho), hw, 100)
        todos = geometria(ssd)
        ssd.filter_rids(reverse=False)
        ssd.filter_rids(reverse=True)
        carga = geometria(ssd)
    r = dict(ts=ts, seed=seed, half_width=hw)
    r.update({f"{k}_all": v for k, v in todos.items()})
    r.update({f"{k}_load": v for k, v in carga.items()})
    return r


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--extended", type=pathlib.Path, required=True)
    ap.add_argument("--half-width", type=int, default=20)
    ap.add_argument("--workers", type=int, default=10)
    a = ap.parse_args()
    arquivos = sorted(p for p in a.extended.glob("ts_*_seed_*.dat") if NOME.match(p.name))
    with Pool(a.workers) as pool:
        res = pool.map(medir, [(p, a.half_width) for p in arquivos])
    df = pd.DataFrame(res).sort_values(["ts", "seed"])
    df.to_csv(N18 / "trunk_geometry_by_seed.csv", index=False, float_format="%.5g")
    g = df.groupby("ts")
    cols = [c for c in df.columns if c not in ("ts", "seed", "half_width")]
    agg = g[cols].mean().join(g[cols].sem().add_suffix("_se")).join(g.size().rename("n_seeds"))
    agg["half_width"] = a.half_width
    agg = agg.loc[[t for t in TS if t in agg.index]]
    agg.to_csv(N18 / "trunk_geometry_by_ts.csv", float_format="%.5g")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.style.use(RAIZ / "Code" / "Data_analysis" / "xmgrace_paper.mplstyle")
    fig, ax1 = plt.subplots(figsize=(6.2, 4.2))
    ax2 = ax1.twinx()
    w = 2 * a.half_width + 1
    for ax, col, cor, mk, lab in [(ax1, "K_mean_load", "#1F5F8B", "o", r"$\langle K\rangle$, moléculas por camada"),
                                  (ax2, "N_mean_load", "#C0392B", "s", r"$\langle N_i\rangle$, vizinhos por bastão")]:
        ax.errorbar(agg.index, agg[col], yerr=agg[f"{col}_se"], fmt=mk + "-", color=cor, ms=5, lw=1.3, capsize=3, label=lab)
        ax.plot(agg.index, agg[col.replace("_load", "_all")], mk + ":", color=cor, ms=3, lw=0.8, mfc="none",
                label=lab.split(",")[0] + ", todos os bastões do recorte")
        ax.set_ylabel(lab, color=cor); ax.tick_params(axis="y", colors=cor)
    ax1.set_xscale("log"); ax1.set_xlabel("$T_s$")
    ax1.set_title(f"tronco {w}×{w}×201, geometria inicial; cheio = bastões que portam carga", fontsize=9, loc="left")
    h1, l1 = ax1.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, fontsize=6.5, frameon=False, loc="lower right")
    fig.tight_layout(); fig.savefig(N18 / "figures" / "trunk_geometry_vs_ts.png", dpi=200)
    print(agg[["n_seeds", "R_all", "R_load", "K_mean_all", "K_mean_load", "N_mean_all", "N_mean_load"]].round(2).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())

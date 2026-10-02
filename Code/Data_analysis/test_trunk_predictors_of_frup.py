#!/usr/bin/env python3
"""Candidatas geometricas a proxy de F_rup, testadas semente a semente nos troncos fraturados.

Para cada tronco (T_s, semente, recorte 17x17 ou 41x41) le o cache .db do motor
de fratura (particulas, bastoes com neigh_pids, camadas) e calcula grandezas
do proprio modelo: ocupacao das camadas n(y), coordenacao K_i de cada bastao
(numero de particulas vizinhas, o K_i do modelo), fator de tensao
s_i = <1/n>_camadas do bastao, e um proxy de forca do modelo,
F* = [ media_i (s_i / K_i)^m ]^(-1/m) com m = 2 (forca em que a probabilidade
media de ruptura por bastao chega a 1). Tambem D_f da semente (correlacao e
giracao, de df_periodic_by_seed.csv). Compara com F_rup/R medido na mesma
semente (media das 10 realizacoes).

Teste principal: Spearman DENTRO de cada (T_s, recorte), 5 sementes, e Pearson
dos z-scores agrupados dentro de (T_s, recorte) -- remove o confundidor T_s.
Teste secundario: Spearman ATRAVES de T_s (10 ou 4 pontos), que qualquer
funcao monotona de T_s passa.

Le:      <extended>/ts_<T>_seed_<S>.db, ts_<T>_seed_<S>_w20_l100.db (cache do motor)
         Reviews/N18_df_ten_ts/width_fracture_by_realization.csv
         Reviews/N18_df_ten_ts/df_periodic_by_seed.csv
Escreve: Reviews/N18_df_ten_ts/trunk_predictors_by_seed.csv
         Reviews/N18_df_ten_ts/trunk_predictors_correlations.csv
Chamado: à mão, depois de run_local_width_fracture.sh (que cria os .db)
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import sys

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

RAIZ = pathlib.Path(__file__).resolve().parents[2]
N18 = RAIZ / "Reviews" / "N18_df_ten_ts"
M = 2
NOME = re.compile(r"ts_(\d+)_seed_(\d+)(_w20_l100)?\.db$")


def ler_db(caminho: pathlib.Path) -> dict:
    part_lid, rods, layers = {}, {}, {}
    with open(caminho, encoding="utf-8") as fh:
        for row in fh:
            if row.startswith('{"pid"'):
                d = json.loads(row)
                part_lid[d["pid"]] = d["lid"]
            elif row.startswith('{"rid"'):
                d = json.loads(row)
                rods[d["rid"]] = (d["pids"], len(d["neigh_pids"]))
            elif row.startswith('{"lid"'):
                d = json.loads(row)
                layers[d["lid"]] = len(d["pids"])
    return dict(part_lid=part_lid, rods=rods, layers=layers)


def candidatas(db: dict) -> dict:
    n_layer = np.array([db["layers"][l] for l in sorted(db["layers"])], float)
    inv = {l: 1.0 / n for l, n in db["layers"].items()}
    N, s = [], []
    for pids, n_neigh in db["rods"].values():
        N.append(n_neigh)
        s.append(np.mean([inv[db["part_lid"][p]] for p in pids]))
    N, s = np.array(N, float), np.array(s)
    ok = N > 0
    ratio = np.where(ok, s / np.where(ok, N, 1.0), np.inf)        # bastao sem vizinho: p = 1 em qualquer F
    F_star = float(np.mean(ratio[ok] ** M) ** (-1.0 / M)) if ok.any() else float("nan")
    return dict(
        R=len(N),
        n_layers=len(n_layer),
        n_layer_mean=float(n_layer.mean()),
        n_layer_min=float(n_layer.min()),
        n_layer_min_over_mean=float(n_layer.min() / n_layer.mean()),
        n_layer_cv=float(n_layer.std(ddof=1) / n_layer.mean()),
        mean_inv_n_layer=float(np.mean(1.0 / n_layer)),
        coord_mean=float(N.mean()),
        coord_median=float(np.median(N)),
        coord_harmonic=float(len(N) / np.sum(1.0 / N[ok])) if ok.any() else float("nan"),
        frac_coord_le_5=float(np.mean(N <= 5)),
        frac_coord_0=float(np.mean(N == 0)),
        F_star_model_m2=F_star,
        F_star_per_rod=F_star / len(N),
        weakest_1pct_N_over_s=float(np.quantile(N[ok] / s[ok], 0.01)),
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--extended", type=pathlib.Path, required=True)
    a = ap.parse_args()

    linhas = []
    for db_path in sorted(a.extended.glob("ts_*_seed_*.db")):
        mt = NOME.match(db_path.name)
        if not mt:
            continue
        ts, seed = int(mt.group(1)), int(mt.group(2))
        width = 41 if mt.group(3) else 17
        c = candidatas(ler_db(db_path))
        linhas.append(dict(ts=ts, seed=seed, width=width, **c))
    cand = pd.DataFrame(linhas)
    if cand.empty:
        sys.exit("nenhum .db encontrado")

    w = pd.read_csv(N18 / "width_fracture_by_realization.csv", comment="#")
    w = w[w.source.astype(str).str.startswith("local")] if "source" in w else w
    med = w.groupby(["ts", "seed", "width"]).agg(F_rup=("F_rup", "mean"), R_measured=("R", "mean"),
                                                   n_real=("F_rup", "size")).reset_index()
    med["F_rup_per_rod"] = med.F_rup / med.R_measured
    df = pd.read_csv(N18 / "df_periodic_by_seed.csv", comment="#")[["ts", "seed", "corr_primary", "gyr_primary", "R_bar"]]
    tab = cand.merge(med, on=["ts", "seed", "width"]).merge(df, on=["ts", "seed"])
    # R_measured (soma dos bastoes rompidos na realizacao) fica abaixo dos bastoes
    # do .db: os que nunca rompem nao entram. Guarda-se a razao em vez de exigir igualdade.
    tab["R_measured_over_R_db"] = tab.R_measured / tab.R
    tab["F_rup_per_rod_db"] = tab.F_rup / tab.R
    tab = tab.sort_values(["width", "ts", "seed"])
    tab.to_csv(N18 / "trunk_predictors_by_seed.csv", index=False, float_format="%.6g")

    preditores = [c for c in cand.columns if c not in ("ts", "seed", "width", "R", "n_layers")] + ["corr_primary", "gyr_primary", "R_bar"]
    out = []
    for width, g in tab.groupby("width"):
        for p in preditores:
            # dentro de T_s: z-scores agrupados e Spearman por T_s
            z = g.groupby("ts")[[p, "F_rup_per_rod"]].transform(lambda x: (x - x.mean()) / x.std(ddof=1))
            okz = z.notna().all(axis=1)
            r_in, p_in = pearsonr(z[p][okz], z["F_rup_per_rod"][okz]) if okz.sum() > 3 else (np.nan, np.nan)
            por_ts = {ts: spearmanr(q[p], q.F_rup_per_rod)[0] for ts, q in g.groupby("ts")}
            sinais = sum(np.sign(v) for v in por_ts.values() if np.isfinite(v))
            # atraves de T_s (medias por T_s)
            m_ts = g.groupby("ts")[[p, "F_rup_per_rod"]].mean()
            s_across = spearmanr(m_ts[p], m_ts.F_rup_per_rod)[0]
            out.append(dict(width=width, predictor=p, n_pairs=int(okz.sum()),
                            within_ts_pearson_z=round(r_in, 3), within_ts_p=round(p_in, 3),
                            within_ts_spearman_by_ts=";".join(f"{ts}:{v:+.2f}" for ts, v in por_ts.items()),
                            within_ts_sign_sum=int(sinais), across_ts_spearman=round(s_across, 3)))
    res = pd.DataFrame(out).sort_values(["width", "within_ts_p"])
    res.to_csv(N18 / "trunk_predictors_correlations.csv", index=False)
    pd.set_option("display.width", 250)
    for width, g in res.groupby("width"):
        print(f"\n=== recorte {width}x{width}: dentro de T_s (z agrupado, n = {g.n_pairs.max()} pares; menos quando um preditor e constante num T_s) e atraves de T_s ===")
        print(g.drop(columns=["width", "n_pairs"]).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

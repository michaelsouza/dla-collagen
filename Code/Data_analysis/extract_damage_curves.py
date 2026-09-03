#!/usr/bin/env python3
"""Curvas de dano phi(F) e forças de ruptura da campanha quenched, por (T_s, m).

Lê:      $DLA_PROJECT/campaign/avalanches/runs/ts_<TS>/ts_<TS>_seed_<SEED>_m_<M>.txt
Escreve: <out>/damage_summary.csv                       (uma linha por condição)
         <out>/damage_ts<TS>_m<M>_realizations.csv      (uma linha por realização)
         <out>/damage_ts<TS>_m<M>_curve_norm.csv        (phi contra F/F_rup)
         <out>/damage_ts<TS>_m<M>_curve_abs.csv         (phi e sobrevivência contra F)
Chamado: à mão, via sbatch no SDumont2, para N9 (Estado_revisao_ER12738.md);
         o ajuste da Eq. (5) e a Fig. 8 do manuscrito revisado leem estes CSVs

Cada arquivo de corrida é uma fibrila com 50 realizações separadas por linhas
`-----N`; cada linha é um passo de carga: f, partículas ativas, partículas
removidas (acumulado), hastes removidas na cascata, tamanhos dos aglomerados.
A fração removida phi é medida em hastes (moléculas), como no manuscrito:
phi(F) = hastes removidas até F / hastes do esqueleto inicial, e o esqueleto
inicial é a soma de todas as cascatas da realização, porque a última linha
esvazia a fibrila. A cascata terminal está incluída: em F = F_rup, phi = 1.

    extract_damage_curves.py --runs-dir DIR --out DIR [--workers N]
"""
from __future__ import annotations

import argparse
import csv
import os
import re
from concurrent.futures import ProcessPoolExecutor

import numpy as np

NAME = re.compile(r"ts_(\d+)_seed_(\d+)_m_(\d+)\.txt")
SEP = re.compile(r"^-+\d+$")
U_GRID = np.linspace(0.0, 1.0, 201)   # F / F_rup
N_ABS = 400                           # pontos da grade absoluta, por condição


def read_file(path):
    """Lista de realizações; cada uma é (f, hastes_por_passo, particulas_iniciais)."""
    runs, f_list, rod_list, part0 = [], [], [], None
    with open(path) as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line or line.startswith("f,"):
                continue
            if SEP.match(line):
                runs.append((np.asarray(f_list), np.asarray(rod_list), part0))
                f_list, rod_list, part0 = [], [], None
                continue
            f_s, active_s, _deleted_s, rods_s, _rest = line.split(",", 4)
            if part0 is None:
                part0 = int(active_s)
            f_list.append(float(f_s))
            rod_list.append(int(rods_s))
    if f_list:
        runs.append((np.asarray(f_list), np.asarray(rod_list), part0))
    return runs


def phi_at(f, cum, query):
    """phi (função escada) avaliada nas forças `query`."""
    idx = np.searchsorted(f, query, side="right") - 1
    out = np.where(idx >= 0, cum[np.clip(idx, 0, len(cum) - 1)], 0.0)
    return out


def job(item):
    seed, path = item
    rows, norm_curves, steps = [], [], []
    for k, (f, rods, part0) in enumerate(read_file(path)):
        n_rods = int(rods.sum())
        if n_rods == 0 or len(f) < 2:
            continue
        cum = np.cumsum(rods) / n_rods
        f_rup = float(f[-1])
        nz = np.nonzero(rods)[0]
        rows.append(dict(seed=seed, realization=k, n_rods=n_rods,
                         n_particles0=part0, f_first=f"{float(f[nz[0]]):.6g}",
                         f_rup=f"{f_rup:.6g}", n_steps=int(len(nz)),
                         terminal_fraction=f"{rods[-1] / n_rods:.6f}"))
        norm_curves.append(phi_at(f / f_rup, cum, U_GRID))
        steps.append((f, cum))
    return seed, rows, np.asarray(norm_curves), steps


def write_csv(path, rows):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    by_cond = {}
    for root, _dirs, files in os.walk(args.runs_dir):
        for name in files:
            m = NAME.fullmatch(name)
            if m:
                key = (int(m.group(1)), int(m.group(3)))
                by_cond.setdefault(key, []).append(
                    (int(m.group(2)), os.path.join(root, name)))

    summary = []
    for (ts, mod) in sorted(by_cond):
        items = sorted(by_cond[(ts, mod)])
        with ProcessPoolExecutor(args.workers) as pool:
            out = list(pool.map(job, items, chunksize=4))

        rows = [r for _s, rs, _c, _st in out for r in rs]
        norm = np.vstack([c for _s, _rs, c, _st in out if len(c)])
        steps = [st for _s, _rs, _c, sts in out for st in sts]
        f_rup = np.array([float(r["f_rup"]) for r in rows])
        stem = f"{args.out}/damage_ts{ts}_m{mod}"
        write_csv(f"{stem}_realizations.csv", rows)

        write_csv(f"{stem}_curve_norm.csv", [
            dict(u=f"{u:.4f}", phi_mean=f"{mu:.6f}", phi_sd=f"{sd:.6f}", n=len(norm))
            for u, mu, sd in zip(U_GRID, norm.mean(axis=0), norm.std(axis=0, ddof=1))])

        f_grid = np.linspace(0.0, f_rup.max(), N_ABS)
        phi_all = np.vstack([phi_at(f, cum, f_grid) for f, cum in steps])
        intact = f_grid[None, :] < f_rup[:, None]
        n_intact = intact.sum(axis=0)
        with np.errstate(invalid="ignore"):
            phi_intact = np.where(n_intact > 0,
                                  (phi_all * intact).sum(axis=0) / np.maximum(n_intact, 1),
                                  np.nan)
        write_csv(f"{stem}_curve_abs.csv", [
            dict(F=f"{F:.4f}", phi_mean_all=f"{a:.6f}",
                 phi_mean_intact=("" if np.isnan(b) else f"{b:.6f}"),
                 survival=f"{s / len(f_rup):.6f}", n_intact=int(s))
            for F, a, b, s in zip(f_grid, phi_all.mean(axis=0), phi_intact, n_intact)])

        term = np.array([float(r["terminal_fraction"]) for r in rows])
        summary.append(dict(
            ts=ts, m=mod, n_fibrils=len(items), n_realizations=len(rows),
            n_rods_mean=f"{np.mean([r['n_rods'] for r in rows]):.1f}",
            f_first_mean=f"{np.mean([float(r['f_first']) for r in rows]):.4f}",
            f_rup_mean=f"{f_rup.mean():.4f}", f_rup_sd=f"{f_rup.std(ddof=1):.4f}",
            f_rup_cv=f"{f_rup.std(ddof=1) / f_rup.mean():.4f}",
            f_rup_median=f"{np.median(f_rup):.4f}",
            terminal_fraction_mean=f"{term.mean():.4f}"))
        print(f"ts={ts:<5} m={mod:<3} fibrilas={len(items):>4} runs={len(rows):>6} "
              f"F_rup={f_rup.mean():>9.2f}±{f_rup.std(ddof=1):<8.2f} "
              f"terminal={term.mean():.3f}", flush=True)

    write_csv(f"{args.out}/damage_summary.csv", summary)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""F_rup contra a largura do recorte: resume as fraturas locais e a escada de 2026-09-02.

Lê:      arquivos legados de fiber_bundle_ava.py, via --dirs ROTULO=DIR ...:
         <dir>/ts_<TS>/ts_<TS>_seed_<SEED>_m_<M>.txt (fraturas locais, janela no rotulo)
         Reviews/PhaseC_periodic_cylinder/avalanche_ladder_raw/ts<TS>_w<W>.txt (escada)
Escreve: Reviews/N18_df_ten_ts/width_fracture_by_realization.csv
         Reviews/N18_df_ten_ts/width_fracture_summary.csv
         Reviews/N18_df_ten_ts/xmgrace/frup_per_rod_by_width_xydy.dat
Chamado: Code/Data_analysis/run_local_width_fracture.sh (estagio D); à mão para so resumir

Por realizacao: R = soma da coluna total_deleted_rods (todas as linhas, inclusive
a terminal) = numero de moleculas portantes depois do filtro inicial do
esqueleto, porque o motor so para quando num_active == 0; F_rup = coluna f da
linha terminal; tamanhos preterminais = linhas com rods > 0 e ativos > 0.
O resumidor da escada (summarize_avalanche_ladder.py) estimava moleculas por
P0/16,6 (2372 para 128/900001 em 17x17); aqui a contagem e exata (2328). Erro-padrao sobre medias por semente quando
ha >= 2 sementes; senao sobre realizacoes, com a coluna se_basis dizendo qual.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import re
import sys

import numpy as np

RAIZ = pathlib.Path(__file__).resolve().parents[2]
OUT = RAIZ / "Reviews" / "N18_df_ten_ts"
NOME_LOCAL = re.compile(r"ts_(\d+)_seed_(\d+)_m_(\d+)\.txt$")
NOME_ESCADA = re.compile(r"ts(\d+)_w(\d+)\.txt$")
SEMENTE_ESCADA, M_ESCADA, FRATURA_SEED_ESCADA = 900001, 2, 1


def realizacoes(caminho: pathlib.Path) -> list[dict]:
    """Uma entrada por realizacao: P0, R, F_rup, tamanhos preterminais."""
    out, atual = [], None
    with open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            if linha.startswith("f,"):
                continue
            if linha.startswith("-"):
                continue
            c = linha.rstrip("\n").split(",")
            if len(c) < 4:
                continue
            if c[0] == "0":
                atual = dict(P0=int(c[1]), R=0, F_rup=float("nan"), pre=[])
                out.append(atual)
                continue
            ativos, rods = int(c[1]), int(c[3])
            atual["R"] += rods
            if ativos == 0:
                atual["F_rup"] = float(c[0])
                atual["terminal"] = rods
            elif rods > 0:
                atual["pre"].append(rods)
    return out


def coletar(dirs: dict[str, pathlib.Path]) -> list[dict]:
    linhas = []
    for rotulo, d in dirs.items():
        if rotulo == "ladder":
            for f in sorted(d.glob("ts*_w*.txt")):
                ts, w = (int(g) for g in NOME_ESCADA.match(f.name).groups())
                for k, r in enumerate(realizacoes(f)):
                    linhas.append(dict(source="ladder_2026-09-02", ts=ts, seed=SEMENTE_ESCADA, m=M_ESCADA,
                                       width=w, fracture_seed=FRATURA_SEED_ESCADA, realization=k, **_stats(r)))
        else:
            w = int(re.sub(r"\D", "", rotulo))          # w17 -> 17, w41 -> 41
            for f in sorted(d.glob("ts_*/ts_*_seed_*_m_*.txt")):
                ts, seed, m = (int(g) for g in NOME_LOCAL.match(f.name).groups())
                for k, r in enumerate(realizacoes(f)):
                    linhas.append(dict(source=f"local_{rotulo}", ts=ts, seed=seed, m=m, width=w,
                                       fracture_seed=101, realization=k, **_stats(r)))
    return linhas


def _stats(r: dict) -> dict:
    pre = np.asarray(r["pre"], float)
    return dict(P0=r["P0"], R=r["R"], F_rup=r["F_rup"], F_rup_per_rod=r["F_rup"] / r["R"],
                terminal=r.get("terminal", 0), terminal_frac=r.get("terminal", 0) / r["R"],
                n_pre=len(pre), max_pre=int(pre.max()) if len(pre) else 0,
                p99_pre=float(np.percentile(pre, 99)) if len(pre) else float("nan"),
                frac1_pre=float((pre == 1).mean()) if len(pre) else float("nan"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+", required=True, help="ROTULO=DIR, rotulo w17/w41/ladder")
    ap.add_argument("--out", type=pathlib.Path, default=OUT)
    a = ap.parse_args()
    dirs = {k: pathlib.Path(v) for k, v in (x.split("=", 1) for x in a.dirs)}
    linhas = coletar(dirs)
    if not linhas:
        sys.exit("nenhuma realizacao lida")

    # coerencia: R exato contra a estimativa P0/16,6 do README §4d (2372 para
    # 128/900001 em 17x17; o valor exato e 2328, e a razao P0/R fica em ~16,9
    # porque os bastoes cortados em |y| = 100 tem menos de 18 particulas)
    for l in linhas:
        assert 15.0 < l["P0"] / l["R"] < 18.0, (l["source"], l["ts"], l["seed"], l["P0"], l["R"])

    a.out.mkdir(exist_ok=True)
    (a.out / "xmgrace").mkdir(exist_ok=True)
    campos = list(linhas[0])
    with open(a.out / "width_fracture_by_realization.csv", "w", newline="", encoding="utf-8") as fh:
        fh.write("# Uma linha por realizacao. R = moleculas portantes (soma exata de total_deleted_rods). "
                 "Gerado por summarize_width_fracture.py em 2026-09-10.\n")
        w = csv.DictWriter(fh, fieldnames=campos); w.writeheader()
        for l in linhas:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in l.items()})

    resumo = []
    chaves = sorted({(l["ts"], l["width"], l["source"]) for l in linhas})
    for ts, width, source in chaves:
        g = [l for l in linhas if (l["ts"], l["width"], l["source"]) == (ts, width, source)]
        seeds = sorted({l["seed"] for l in g})
        def agg(campo):
            if len(seeds) >= 2:
                med = [np.mean([l[campo] for l in g if l["seed"] == s]) for s in seeds]
                return np.mean(med), np.std(med, ddof=1) / np.sqrt(len(med)), "seeds"
            v = [l[campo] for l in g]
            return np.mean(v), (np.std(v, ddof=1) / np.sqrt(len(v)) if len(v) > 1 else float("nan")), "realizations"
        f, fe, base = agg("F_rup"); fr, fre, _ = agg("F_rup_per_rod"); R, _, _ = agg("R")
        resumo.append(dict(ts=ts, width=width, source=source, n_seeds=len(seeds), n_real=len(g),
                           R_mean=f"{R:.1f}", F_rup_mean=f"{f:.1f}", F_rup_se=f"{fe:.1f}",
                           F_rup_per_rod_mean=f"{fr:.4f}", F_rup_per_rod_se=f"{fre:.4f}", se_basis=base,
                           terminal_frac_mean=f"{np.mean([l['terminal_frac'] for l in g]):.3f}",
                           frac1_pre_mean=f"{np.nanmean([l['frac1_pre'] for l in g]):.3f}",
                           p99_pre_mean=f"{np.nanmean([l['p99_pre'] for l in g]):.1f}",
                           max_pre=max(l["max_pre"] for l in g)))
    with open(a.out / "width_fracture_summary.csv", "w", newline="", encoding="utf-8") as fh:
        fh.write("# F_rup por (T_s, largura do recorte, fonte). Gerado por summarize_width_fracture.py em 2026-09-10.\n")
        w = csv.DictWriter(fh, fieldnames=list(resumo[0])); w.writeheader(); w.writerows(resumo)

    with open(a.out / "xmgrace" / "frup_per_rod_by_width_xydy.dat", "w", encoding="utf-8") as fh:
        fh.write("# F_rup per load-bearing molecule versus crop width, m = 2\n"
                 "# Columns: width (lattice units)   F_rup/R   SE\n"
                 "# One set per T_s (local runs pooled with the 2026-09-02 ladder where both exist)\n@type xydy\n")
        for ts in sorted({r["ts"] for r in resumo}):
            fh.write(f"# T_s = {ts}\n")
            for width in sorted({r["width"] for r in resumo if r["ts"] == ts}):
                g = [l for l in linhas if l["ts"] == ts and l["width"] == width]
                seeds = sorted({l["seed"] for l in g})
                med = [np.mean([l["F_rup_per_rod"] for l in g if l["seed"] == s]) for s in seeds]
                e = np.std(med, ddof=1) / np.sqrt(len(med)) if len(med) > 1 else float("nan")
                fh.write(f"{width} {np.mean(med):.4f} {e:.4f}\n")
            fh.write("&\n")

    print(f"{'Ts':>5} {'w':>4} {'fonte':>18} {'sem':>3} {'real':>4} {'R':>8} {'F_rup':>10} {'F/R':>14} {'term':>6} {'frac1':>6} {'p99':>5}")
    for r in resumo:
        print(f"{r['ts']:>5} {r['width']:>4} {r['source']:>18} {r['n_seeds']:>3} {r['n_real']:>4} {r['R_mean']:>8} "
              f"{r['F_rup_mean']:>7}±{r['F_rup_se']:<4} {r['F_rup_per_rod_mean']}±{r['F_rup_per_rod_se']} "
              f"{r['terminal_frac_mean']:>6} {r['frac1_pre_mean']:>6} {r['p99_pre_mean']:>5}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Equivalencia em massa do motor em arrays contra os arquivos legados do N18.

Roda fiber_bundle_ava.run_realizations(engine="arrays") com a mesma receita
do N18 (m = 2, semente de fratura 101, 10 realizacoes, -half-length 100) nos
20 troncos de T_s in {2, 32, 128, 8192} x 5 sementes, nos recortes 17x17
(half-width 8) e 41x41 (half-width 20), e compara byte a byte com
Reviews/N18_df_ten_ts/width_fracture_raw/w{17,41}/ts_<T>/ts_<T>_seed_<S>_m_2.txt,
produzidos pelo motor legado em 2026-09-10. Para cada arquivo diferente,
localiza a primeira linha divergente. Tempo do legado lido dos logs do N18
(linhas "run k/10: ... (Xs)"), se existirem.

Le:      <extended>/ts_<T>_seed_<S>.dat (+ .db), Reviews/N18_df_ten_ts/width_fracture_raw/
         <logs>/ts_<T>_seed_<S>_w{17,41}.log (opcional, tempos do legado)
Escreve: Reviews/N19_full_section_fracture/engine_equivalence.csv
Chamado: à mão, uma vez, antes da campanha da secao inteira (N19)
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import re
import sys
import tempfile
import time

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "Code" / "Fracture_fibril"))
from fiber_bundle_ava import run_realizations  # noqa: E402

RAW = RAIZ / "Reviews" / "N18_df_ten_ts" / "width_fracture_raw"
OUT = RAIZ / "Reviews" / "N19_full_section_fracture"
TS = [2, 32, 128, 8192]
SEEDS = [900001, 900002, 900003, 900004, 900005]
RECORTES = {"w17": 8, "w41": 20}


def tempo_legado(log: pathlib.Path) -> float | None:
    if not log.exists():
        return None
    t = [float(m) for m in re.findall(r"run \d+/\d+: .*\((\d+\.?\d*)s\)", log.read_text())]
    return sum(t) / len(t) if t else None


def primeira_diferenca(a: pathlib.Path, b: pathlib.Path) -> tuple[int, str, str]:
    la, lb = a.read_text().splitlines(), b.read_text().splitlines()
    for i, (x, y) in enumerate(zip(la, lb), start=1):
        if x != y:
            return i, x[:60], y[:60]
    return min(len(la), len(lb)) + 1, f"{len(la)} linhas", f"{len(lb)} linhas"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--extended", type=pathlib.Path, required=True)
    ap.add_argument("--logs", type=pathlib.Path, default=None)
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    linhas = []
    with tempfile.TemporaryDirectory() as tmp:
        for tag, hw in RECORTES.items():
            for ts in TS:
                for seed in SEEDS:
                    ref = RAW / tag / f"ts_{ts}" / f"ts_{ts}_seed_{seed}_m_2.txt"
                    dat = a.extended / f"ts_{ts}_seed_{seed}.dat"
                    novo = pathlib.Path(tmp) / tag / f"ts_{ts}" / f"ts_{ts}_seed_{seed}_m_2.txt"
                    t0 = time.time()
                    runs = run_realizations(str(dat), 10, m=2, seed=101, legacy_path=str(novo),
                                            half_width=hw, half_length=100, engine="arrays")
                    t_arr = (time.time() - t0) / 10
                    identico = novo.read_bytes() == ref.read_bytes()
                    linha = dict(window=tag, ts=ts, seed=seed, identical=int(identico),
                                 arrays_s_per_realization=round(t_arr, 3),
                                 legacy_s_per_realization=tempo_legado(a.logs / f"ts_{ts}_seed_{seed}_{tag}.log") if a.logs else None,
                                 F_rup_mean=round(sum(r["F_rupture"] for r in runs) / 10, 3),
                                 first_diff_line="", new="", legacy="")
                    if not identico:
                        i, x, y = primeira_diferenca(novo, ref)
                        linha.update(first_diff_line=i, new=x, legacy=y)
                    linhas.append(linha)
                    print(f"{tag} ts={ts:>5} seed={seed}: {'identico' if identico else 'DIFERE linha ' + str(linha['first_diff_line'])}  "
                          f"arrays {t_arr:.2f} s/real., legado {linha['legacy_s_per_realization']}", flush=True)
    with open(OUT / "engine_equivalence.csv", "w", newline="", encoding="utf-8") as fh:
        fh.write("# Motor em arrays (fiber_bundle_ava.py -engine arrays) contra os 400 arquivos legados de "
                 "Reviews/N18_df_ten_ts/width_fracture_raw (m=2, semente 101, 10 realizacoes). "
                 "Gerado por compare_fracture_engines.py.\n")
        w = csv.DictWriter(fh, fieldnames=list(linhas[0]))
        w.writeheader(); w.writerows(linhas)
    n_id = sum(l["identical"] for l in linhas)
    print(f"\n{n_id}/{len(linhas)} arquivos identicos (cada um com 10 realizacoes)")
    return 0 if n_id == len(linhas) else 1


if __name__ == "__main__":
    sys.exit(main())

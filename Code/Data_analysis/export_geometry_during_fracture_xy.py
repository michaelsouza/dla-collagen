#!/usr/bin/env python3
"""<K(F)>/K_0 e <N(F)>/N_0 em F absoluto, um .dat xy sem cabecalho por (grandeza, T_s).

Notacao do artigo: K = coordenacao media dos bastoes ativos, N = segmentos por
camada (o N(i) de sigma = F/N(i)). Pedido de coautor (2026-10-01): duas colunas
separadas por espaco, sem comentarios, para o xmgrace ler direto; os oito T_s,
os seis da Fig. 8 e 1024 e 8192 para a saturacao. Mesma normalizacao de
build_trunk_geometry_xmgrace.py (valor medio / valor medio em F = 0).

Lê:      Reviews/N18_df_ten_ts/geometry_during_fracture_curves.csv (x_kind == "F")
Escreve: Reviews/N18_df_ten_ts/xmgrace/geometry_during_fracture_two_column/{K,N}xF_T_s_<TS>.dat
Chamado: à mão, depois de trace_geometry_during_fracture.py --ts 2 8 16 32 64 128 1024 8192
"""
from __future__ import annotations

import argparse
import pathlib

import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[2]
N18 = RAIZ / "Reviews" / "N18_df_ten_ts"
SAIDA = N18 / "xmgrace" / "geometry_during_fracture_two_column"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ts", type=int, nargs="+", default=[2, 8, 16, 32, 64, 128, 1024, 8192])
    a = ap.parse_args()
    cv = pd.read_csv(N18 / "geometry_during_fracture_curves.csv")
    cv = cv[cv.x_kind == "F"]
    SAIDA.mkdir(parents=True, exist_ok=True)
    for ts in a.ts:
        q = cv[cv.ts == ts].sort_values("x")
        if q.empty:
            raise SystemExit(f"T_s = {ts} ausente do CSV; rode trace_geometry_during_fracture.py com ele")
        for letra in ("K", "N"):
            col = f"{letra}_mean"
            v0 = q[col].iloc[0]
            linhas = [f"{x:.5f} {v / v0:.6f}" for x, v in zip(q.x, q[col])]
            (SAIDA / f"{letra}xF_T_s_{ts}.dat").write_text("\n".join(linhas) + "\n", encoding="utf-8")
            print(f"T_s = {ts:5d} {letra}: {len(q)} pontos, F ate {q.x.max():7.1f}, {letra}_0 = {v0:8.3f}, "
                  f"min/inicial = {q[col].min() / v0:.4f}, max/inicial = {q[col].max() / v0:.4f}, "
                  f"final/inicial = {q[col].iloc[-1] / v0:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

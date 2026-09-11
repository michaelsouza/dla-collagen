#!/usr/bin/env python3
"""Dinamica da geometria durante a fratura: <K(F)> e <N_i(F)> sobre os bastoes ativos.

Mesmo motor e mesmo protocolo de fiber_bundle_ava.py (quase-estatico extremal,
cascatas deterministicas, desordem X ~ x^m, semente 101 + k), so que apos cada
cascata grava: F, bastoes ativos, <K> = ocupacao media das camadas ativas
(moleculas por camada) e <N_i> = coordenacao media dos bastoes ativos (numero
de particulas vizinhas em bastoes ainda ativos). Ponto inicial em F = 0 depois
do filtro de caminho de carga. As curvas-escada de cada realizacao sao
amostradas em F/F_rup numa grade uniforme e mediadas sobre realizacoes e
sementes; tambem em F absoluto, numa grade comum por T_s.

Le:      <extended>/ts_<T>_seed_<S>.dat (+ .db do recorte)
Escreve: Reviews/N18_df_ten_ts/geometry_during_fracture_curves.csv   (curvas medias por T_s)
         Reviews/N18_df_ten_ts/geometry_during_fracture_by_realization.csv (valores iniciais e finais)
         Reviews/N18_df_ten_ts/figures/geometry_during_fracture.png
Chamado: à mão, depois do estagio A de run_local_width_fracture.sh
"""
from __future__ import annotations

import argparse
import contextlib
import io
import pathlib
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "Code" / "Fracture_fibril"))
import stress_strain_ava as S  # noqa: E402
from fiber_bundle_ava import FibrilSystem, quasistatic_rupture  # noqa: E402

N18 = RAIZ / "Reviews" / "N18_df_ten_ts"
U = np.linspace(0.0, 1.0, 101)


class SistemaInstrumentado(FibrilSystem):
    def snapshot(self, F: float) -> None:
        act = self.active
        act_flat = act[self.flat_rod]
        counts = np.bincount(self.flat_lids[act_flat], minlength=self.L)
        K = self.C.dot(act.astype(float))
        self.trace.append((float(F), int(act.sum()),
                           float(counts[counts > 0].mean()) if counts.any() else 0.0,
                           float(K[act].mean()) if act.any() else 0.0))

    def begin_cascade(self, F):
        super().begin_cascade(F)

    def end_cascade(self, F, size):
        super().end_cascade(F, size)
        self.snapshot(F)


def escada(tr: np.ndarray, grade: np.ndarray, col: int) -> np.ndarray:
    """Valor da escada (ultimo snapshot com F <= f) em cada f da grade."""
    idx = np.searchsorted(tr[:, 0], grade, side="right") - 1
    idx = np.clip(idx, 0, len(tr) - 1)
    return tr[idx, col]


def realizacoes(args) -> list[dict]:
    caminho, ts, seed, n, m, fseed, hw = args
    with contextlib.redirect_stdout(io.StringIO()):
        ssd0 = S.read_or_create_ssd(str(caminho), hw, 100)
    ssd0.set_rods_exponent(m)
    out = []
    for k in range(n):
        rng = np.random.default_rng(fseed + k)
        sis = SistemaInstrumentado(ssd0.copy(), m=m, rng=rng)
        sis.trace = []
        sis.snapshot(0.0)
        events, F_rup = quasistatic_rupture(sis)
        tr = np.array(sis.trace)
        # a ultima cascata leva ativos a 0; a geometria "final" e a do ultimo estado com ativos > 0
        pre = tr[tr[:, 1] > 0]
        out.append(dict(ts=ts, seed=seed, realization=k, F_rup=F_rup, R0=int(tr[0, 1]),
                        K0=tr[0, 2], N0=tr[0, 3], K_pre=pre[-1, 2], N_pre=pre[-1, 3], R_pre=int(pre[-1, 1]),
                        trace=pre))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--extended", type=pathlib.Path, required=True)
    ap.add_argument("--ts", type=int, nargs="+", default=[2, 64, 128])
    ap.add_argument("--seeds", type=int, nargs="+", default=[900001, 900002, 900003, 900004, 900005])
    ap.add_argument("-n", type=int, default=10)
    ap.add_argument("-m", type=int, default=2)
    ap.add_argument("--fracture-seed", type=int, default=101)
    ap.add_argument("--half-width", type=int, default=8)
    ap.add_argument("--workers", type=int, default=15)
    a = ap.parse_args()
    tarefas = [(a.extended / f"ts_{ts}_seed_{s}.dat", ts, s, a.n, a.m, a.fracture_seed, a.half_width)
               for ts in a.ts for s in a.seeds]
    with Pool(a.workers) as pool:
        res = [r for lst in pool.map(realizacoes, tarefas) for r in lst]

    linhas = [{k: v for k, v in r.items() if k != "trace"} for r in res]
    pd.DataFrame(linhas).to_csv(N18 / "geometry_during_fracture_by_realization.csv", index=False, float_format="%.6g")

    curvas = []
    for ts in a.ts:
        rs = [r for r in res if r["ts"] == ts]
        # em F/F_rup
        Kn = np.array([escada(r["trace"], U * r["F_rup"], 2) for r in rs])
        Nn = np.array([escada(r["trace"], U * r["F_rup"], 3) for r in rs])
        Rn = np.array([escada(r["trace"], U * r["F_rup"], 1) for r in rs])
        # em F absoluto, ate o maior F_rup do T_s
        Fg = np.linspace(0.0, max(r["F_rup"] for r in rs), 101)
        Ka = np.array([np.where(Fg <= r["F_rup"], escada(r["trace"], Fg, 2), np.nan) for r in rs])
        Na = np.array([np.where(Fg <= r["F_rup"], escada(r["trace"], Fg, 3), np.nan) for r in rs])
        for i in range(len(U)):
            curvas.append(dict(ts=ts, x_kind="F_over_Frup", x=U[i], n=len(rs),
                               K_mean=Kn[:, i].mean(), K_se=Kn[:, i].std(ddof=1) / np.sqrt(len(rs)),
                               N_mean=Nn[:, i].mean(), N_se=Nn[:, i].std(ddof=1) / np.sqrt(len(rs)),
                               R_mean=Rn[:, i].mean()))
            alive = np.isfinite(Ka[:, i])
            if alive.sum() >= 3:
                curvas.append(dict(ts=ts, x_kind="F", x=Fg[i], n=int(alive.sum()),
                                   K_mean=np.nanmean(Ka[:, i]), K_se=np.nanstd(Ka[:, i], ddof=1) / np.sqrt(alive.sum()),
                                   N_mean=np.nanmean(Na[:, i]), N_se=np.nanstd(Na[:, i], ddof=1) / np.sqrt(alive.sum()),
                                   R_mean=np.nan))
    cv = pd.DataFrame(curvas)
    cv.to_csv(N18 / "geometry_during_fracture_curves.csv", index=False, float_format="%.6g")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.style.use(RAIZ / "Code" / "Data_analysis" / "xmgrace_paper.mplstyle")
    cmap = plt.get_cmap("viridis")
    cores = {ts: cmap(i / max(1, len(a.ts) - 1)) for i, ts in enumerate(a.ts)}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, kind, xlab in [(axes[0], "F", "$F$"), (axes[1], "F_over_Frup", "$F / F_{rup}$")]:
        ax2 = ax.twinx()
        # normalizado pelo valor inicial de cada T_s, senao T_s = 2 (K0 = 55) fica esmagado sob 128 (K0 = 194)
        for ts in a.ts:
            q = cv[(cv.ts == ts) & (cv.x_kind == kind)]
            K0, N0 = q.K_mean.iloc[0], q.N_mean.iloc[0]
            ax.plot(q.x, q.K_mean / K0, "-", color=cores[ts], lw=1.6, label=f"$T_s={ts}$: $K_0$ = {K0:.0f}, $N_0$ = {N0:.1f}")
            ax.fill_between(q.x, (q.K_mean - q.K_se) / K0, (q.K_mean + q.K_se) / K0, color=cores[ts], alpha=0.2, lw=0)
            ax2.plot(q.x, q.N_mean / N0, "--", color=cores[ts], lw=1.6)
            ax2.fill_between(q.x, (q.N_mean - q.N_se) / N0, (q.N_mean + q.N_se) / N0, color=cores[ts], alpha=0.15, lw=0)
        ax.set_xlabel(xlab); ax.set_ylabel(r"$\langle K(F)\rangle / K_0$, moléculas por camada (cheia)")
        ax2.set_ylabel(r"$\langle N_i(F)\rangle / N_0$, vizinhos por bastão ativo (tracejada)")
        ax.set_ylim(0.78, 1.02); ax2.set_ylim(0.98, 1.10)
        ax.legend(fontsize=7, frameon=False, loc="lower left")
    w = 2 * a.half_width + 1
    axes[0].set_title(f"(a) tronco {w}×{w}, m = {a.m}, {a.n} realizações × {len(a.seeds)} sementes; F absoluto", fontsize=9, loc="left")
    axes[1].set_title("(b) mesmo dado, F normalizado por F_rup da realização", fontsize=9, loc="left")
    fig.tight_layout(); fig.savefig(N18 / "figures" / "geometry_during_fracture.png", dpi=200)
    df = pd.DataFrame(linhas)
    print(df.groupby("ts")[["F_rup", "R0", "K0", "N0", "R_pre", "K_pre", "N_pre"]].mean().round(2).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())

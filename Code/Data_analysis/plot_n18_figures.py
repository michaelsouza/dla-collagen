#!/usr/bin/env python3
"""Figuras internas de N18 (slides e README): secoes, curvas R_g(N) e m(R), D_f(T_s), inclinacoes.

Lê:      <cylinders>/dla_per216_mode_s_ts_<TS>_nb_60000_seed_<SEED>_.dat (todos; 125 desde 2026-09-10)
         Reviews/N18_df_ten_ts/df_periodic_summary.csv
         Reviews/N18_df_ten_ts/df_periodic_local_slopes.csv
Escreve: Reviews/N18_df_ten_ts/curves_rg_by_ts.csv, curves_mr_by_ts.csv
         Reviews/N18_df_ten_ts/figures/{sections_by_ts,rg_curves,mr_curves,df_vs_ts,local_slopes,local_slope_curves,corr_curves,corr_local_slope,corr_df_vs_ts}.png
Chamado: à mão, depois de measure_df_periodic_ten_ts.py

Mesma secao e mesmos calculos de measure_df_periodic_ten_ts.py; aqui so se
guardam as curvas medias (12 secoes x n_seeds sementes) para desenhar.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from multiprocessing import Pool

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "Code" / "Data_analysis"))
from measure_df_periodic_ten_ts import NOME, RAIOS, SEEDS_REF, TS, secoes_em_ordem  # noqa: E402

N18 = RAIZ / "Reviews" / "N18_df_ten_ts"
FIG = N18 / "figures"
AZUL, VERMELHO, CINZA, FG = "#1F5F8B", "#C0392B", "#7F8C8D", "#23373B"
CMAP = plt.get_cmap("viridis")


def curvas(caminho: pathlib.Path) -> dict:
    periodo, ts, _nb, seed = (int(g) for g in NOME.match(caminho.name).groups())
    secoes = secoes_em_ordem(caminho, periodo)
    rg_curvas, massas = [], []
    for s in secoes:
        n = np.arange(1, len(s) + 1)
        media = np.cumsum(s, axis=0) / n[:, None]
        rg2 = np.cumsum(s ** 2, axis=0).sum(axis=1) / n - (media ** 2).sum(axis=1)
        rg_curvas.append(np.sqrt(np.maximum(rg2, 0.0)))
        d = np.sort(np.sqrt(((s - s.mean(axis=0)) ** 2).sum(axis=1)))
        massas.append(np.searchsorted(d, RAIOS, side="right").astype(float))
    n_max = max(len(c) for c in rg_curvas)
    soma, cont = np.zeros(n_max), np.zeros(n_max)
    for c in rg_curvas:
        soma[: len(c)] += c
        cont[: len(c)] += 1
    return dict(ts=ts, seed=seed, rg=soma / cont, rg_cont=cont, mr=np.mean(massas, axis=0),
                secao0=secoes[0])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cylinders", type=pathlib.Path, required=True)
    ap.add_argument("--workers", type=int, default=10)
    a = ap.parse_args()
    arquivos = sorted(p for p in a.cylinders.glob("dla_per*_.dat") if NOME.match(p.name))
    with Pool(a.workers) as pool:
        res = pool.map(curvas, arquivos)
    FIG.mkdir(exist_ok=True)
    plt.style.use(RAIZ / "Code" / "Data_analysis" / "xmgrace_paper.mplstyle")
    cores = {ts: CMAP(i / (len(TS) - 1)) for i, ts in enumerate(TS)}

    # --- curvas medias por T_s
    rg_ts, mr_ts, linhas_rg, linhas_mr = {}, {}, [], []
    for ts in TS:
        g = [r for r in res if r["ts"] == ts]
        n_max = min(len(r["rg"]) for r in g)
        rg = np.mean([r["rg"][:n_max] for r in g], axis=0)
        mr = np.mean([r["mr"] for r in g], axis=0)
        rg_ts[ts], mr_ts[ts] = rg, mr
        linhas_rg += [dict(ts=ts, N=n + 1, Rg=f"{v:.4f}") for n, v in enumerate(rg) if (n + 1) <= 5000]
        linhas_mr += [dict(ts=ts, R=int(r), m=f"{v:.3f}") for r, v in zip(RAIOS, mr) if v < mr.max()]
    pd.DataFrame(linhas_rg).to_csv(N18 / "curves_rg_by_ts.csv", index=False)
    pd.DataFrame(linhas_mr).to_csv(N18 / "curves_mr_by_ts.csv", index=False)

    # --- secoes: uma por T_s, cor = ordem de adesao
    fig, axs = plt.subplots(2, 5, figsize=(12, 5.2))
    for ax, ts in zip(axs.ravel(), TS):
        s = next(r for r in res if r["ts"] == ts and r["seed"] == SEEDS_REF[0])["secao0"]
        ordem = np.arange(len(s)) / len(s)
        ax.scatter(s[:, 0], s[:, 1], c=ordem, cmap="viridis", s=1.2, linewidths=0)
        ax.set_aspect("equal"); ax.set_xlim(-170, 170); ax.set_ylim(-170, 170)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(f"$T_s = {ts}$", fontsize=10, color=FG)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.suptitle("Uma seção por $T_s$ (semente 900001, camada $L=0$); cor = ordem de adesão (escuro = cedo)", fontsize=10, color=FG, y=0.985)
    fig.savefig(FIG / "sections_by_ts.png", dpi=180); plt.close(fig)

    # --- R_g(N)
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    for ts in TS:
        rg = rg_ts[ts]; N = np.arange(1, len(rg) + 1)
        ax.loglog(N[N <= 5000], rg[N <= 5000], color=cores[ts], lw=1.4, label=f"$T_s={ts}$")
    Ng = np.array([40, 2500])
    ax.loglog(Ng, 2.2 * (Ng / 40) ** (1 / 1.70) * rg_ts[2][39] / rg_ts[2][39], ":", color=FG, lw=1.2)
    ax.loglog(Ng, 0.45 * rg_ts[8192][39] * (Ng / 40) ** 0.5, "--", color=FG, lw=1.2)
    ax.text(2600, 2.2 * (2500 / 40) ** (1 / 1.70) * 0.85, "$N^{1/1{,}70}$", fontsize=9, color=FG, ha="left")
    ax.text(2600, 0.45 * rg_ts[8192][39] * (2500 / 40) ** 0.5 * 0.85, "$N^{1/2}$", fontsize=9, color=FG, ha="left")
    ax.axvspan(40, 2500, color=AZUL, alpha=0.06)
    ax.set_xlabel("$N$ (moléculas, ordem de adesão)"); ax.set_ylabel(r"$\langle R_g(N)\rangle$")
    ax.legend(fontsize=7, ncol=2, frameon=False)
    fig.tight_layout(); fig.savefig(FIG / "rg_curves.png", dpi=200); plt.close(fig)

    # --- m(R)
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    for ts in TS:
        mr = mr_ts[ts]; ok = mr < mr.max()
        ax.loglog(RAIOS[ok], mr[ok], color=cores[ts], lw=1.4, label=f"$T_s={ts}$")
    Rg_ = np.array([3, 40])
    ax.loglog(Rg_, 2.2 * mr_ts[8192][2] * (Rg_ / 3) ** 2, "--", color=FG, lw=1.2)
    ax.loglog(Rg_, 0.45 * mr_ts[2][2] * (Rg_ / 3) ** 1.68, ":", color=FG, lw=1.2)
    ax.set_xlabel("$R$"); ax.set_ylabel(r"$\langle m(R)\rangle$")
    ax.legend(fontsize=7, ncol=2, frameon=False)
    fig.tight_layout(); fig.savefig(FIG / "mr_curves.png", dpi=200); plt.close(fig)

    # --- D_f contra T_s
    sm = pd.read_csv(N18 / "df_periodic_summary.csv", comment="#").set_index("ts").loc[TS]
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    for col, lab, cor, mk in [("gyr_primary", "giração, $N$ 40–2500, 30 pts/oitava (principal)", VERMELHO, "o"),
                              ("gyr_N40_320", "giração, $N$ 40–320 (miolo)", AZUL, "^"),
                              ("gyr_N320_5000", "giração, $N$ 320–5000 (periferia)", AZUL, "v"),
                              ("corr_primary_corrected", "correlação $D_2$, $4 \\leq r \\leq \\bar R/3$, borda corrigida", "#2E8B57", "D"),
                              ("mr_rel_0p15R_0p5R", "massa–raio, $0{,}15R$–$0{,}5R$", CINZA, "s")]:
        ax.errorbar(TS, sm[f"{col}_mean"], yerr=sm[f"{col}_se"], fmt=mk + "-", color=cor, ms=4, lw=1, capsize=2, label=lab)
    ax.axhline(2.0, color=FG, lw=0.6, ls="--"); ax.axhline(1.71, color=FG, lw=0.6, ls=":")
    ax.text(2.2, 2.005, "disco, 2", fontsize=8, color=FG); ax.text(2.2, 1.715, "DLA plano, 1,71", fontsize=8, color=FG)
    ax.set_xscale("log"); ax.set_xlabel("$T_s$"); ax.set_ylabel("$D_f$"); ax.set_ylim(1.5, 2.1)
    ax.legend(fontsize=7, frameon=False, loc="lower right")
    fig.tight_layout(); fig.savefig(FIG / "df_vs_ts.png", dpi=200); plt.close(fig)

    # --- inclinacoes locais (giração, oitavas em N)
    loc = pd.read_csv(N18 / "df_periodic_local_slopes.csv", comment="#")
    g = loc[loc.method == "gyr"].pivot(index="ts", columns="window", values="slope_mean")
    cols = sorted(g.columns, key=lambda w: int(w.split("_")[0][1:]))
    g = g[cols].loc[TS]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    im = ax.imshow(g.values, cmap="RdBu_r", vmin=1.5, vmax=2.1, aspect="auto")
    ax.set_yticks(range(len(TS))); ax.set_yticklabels([str(t) for t in TS])
    ax.set_xticks(range(len(cols))); ax.set_xticklabels([c[1:].replace("_", "–") for c in cols], rotation=45, ha="right", fontsize=8)
    ax.set_xlabel("janela em $N$ (oitava)"); ax.set_ylabel("$T_s$")
    for i in range(len(TS)):
        for j in range(len(cols)):
            ax.text(j, i, f"{g.values[i, j]:.2f}", ha="center", va="center", fontsize=7,
                    color="white" if abs(g.values[i, j] - 1.8) > 0.2 else FG)
    fig.colorbar(im, ax=ax, label="inclinação local $d\\log N/d\\log R_g$")
    fig.tight_layout(); fig.savefig(FIG / "local_slopes.png", dpi=200); plt.close(fig)
    print("figuras em", FIG)


def figura_inclinacoes_locais() -> None:
    """Inclinacao local contra a escala, uma curva por T_s, barra = EP sobre 12 x n_seeds secoes.

    (a) giracao: d log N / d log R_g por oitava em N, na ordem de adesao.
    (b) correlacao: d log C / d log r por meia decada em r, na secao final;
        tracejado cinza = disco uniforme com o mesmo n e R_bar (so borda).
    Le so df_periodic_local_slopes.csv; nao precisa dos cilindros.
    """
    loc = pd.read_csv(N18 / "df_periodic_local_slopes.csv", comment="#")
    plt.style.use(RAIZ / "Code" / "Data_analysis" / "xmgrace_paper.mplstyle")
    cores = {ts: CMAP(i / (len(TS) - 1)) for i, ts in enumerate(TS)}
    fig, ax = plt.subplots(1, 2, figsize=(10, 4.0))

    def meio(w):
        lo, hi = w[1:].split("_")
        return float(np.sqrt(float(lo) * float(hi)))

    for metodo, a, xlab in [("gyr", ax[0], "$N$ (moléculas, ordem de adesão; ponto no meio da oitava)"),
                            ("corr", ax[1], "$r$ (ponto no meio da meia década)")]:
        g = loc[loc.method == metodo].copy()
        g["x"] = g.window.map(meio)
        for ts in TS:
            q = g[g.ts == ts].sort_values("x")
            a.errorbar(q.x, q.slope_section_mean, yerr=q.slope_section_se, fmt="o-", color=cores[ts],
                       ms=3.5, lw=1.1, capsize=2, label=f"$T_s={ts}$")
        a.axhline(2.0, color=FG, lw=0.6, ls="--"); a.axhline(1.71, color=FG, lw=0.6, ls=":")
        a.set_xscale("log"); a.set_xlabel(xlab); a.set_ylabel("inclinação local")
    d = loc[loc.method == "corr_disc"].copy(); d["x"] = d.window.map(meio)
    for ts, ls in [(2, "--"), (8192, "-.")]:
        q = d[d.ts == ts].sort_values("x")
        ax[1].plot(q.x, q.slope_section_mean, ls, color=CINZA, lw=1.2, label=f"disco uniforme, $\\bar R$ de $T_s={ts}$")
    ax[0].set_ylim(1.5, 2.2); ax[1].set_ylim(0.0, 2.2); ax[1].set_xlim(2.5, 200)
    ax[0].text(11, 2.005, "disco, 2", fontsize=8, color=FG); ax[0].text(11, 1.715, "DLA plano, 1,71", fontsize=8, color=FG)
    ax[0].legend(fontsize=6.5, frameon=False, ncol=2, loc="lower right")
    ax[1].legend(fontsize=6.5, frameon=False, ncol=2, loc="lower left")
    ax[0].set_title("(a) giração, $d\\log N / d\\log R_g$", fontsize=9, loc="left")
    ax[1].set_title("(b) correlação, $d\\log C / d\\log r$", fontsize=9, loc="left")
    fig.tight_layout(); fig.savefig(FIG / "local_slope_curves.png", dpi=200); plt.close(fig)
    print("figura de inclinacoes locais em", FIG)


def figuras_correlacao() -> None:
    """Tres figuras so com a dimensao de correlacao, lendo apenas os CSVs.

    corr_curves.png       C(r) contra r, uma curva por T_s, com o disco uniforme de referencia
    corr_local_slope.png  d log C / d log r por meia decada, barra sobre 12 x n_seeds secoes; disco tracejado
    corr_df_vs_ts.png     D_2 contra T_s: bruta, disco e corrigida (4 <= r <= R_bar/3)
    """
    plt.style.use(RAIZ / "Code" / "Data_analysis" / "xmgrace_paper.mplstyle")
    cores = {ts: CMAP(i / (len(TS) - 1)) for i, ts in enumerate(TS)}
    cc = pd.read_csv(N18 / "curves_corr_by_ts.csv", comment="#")
    loc = pd.read_csv(N18 / "df_periodic_local_slopes.csv", comment="#")
    sm = pd.read_csv(N18 / "df_periodic_summary.csv", comment="#").set_index("ts").loc[TS]

    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    for ts in TS:
        q = cc[cc.ts == ts]
        ax.loglog(q.r, q.C, color=cores[ts], lw=1.3, label=f"$T_s={ts}$")
    for ts, ls in [(2, "--"), (8192, "-.")]:
        q = cc[cc.ts == ts]
        ax.loglog(q.r, q.C_disc, ls, color=CINZA, lw=1.1, label=f"disco uniforme, $\\bar R$ de $T_s={ts}$")
    r_ = np.array([4, 40]); c0 = cc[(cc.ts == 8192) & (cc.r.round(2) == 4.0)].C.values
    c0 = float(c0[0]) if len(c0) else 1e-3
    ax.loglog(r_, c0 * 0.6 * (r_ / 4) ** 2, ":", color=FG, lw=1.0); ax.text(42, c0 * 0.6 * 100 * 0.9, "$r^{2}$", fontsize=8, color=FG)
    ax.loglog(r_, c0 * 0.25 * (r_ / 4) ** 1.71, ":", color=FG, lw=1.0); ax.text(42, c0 * 0.25 * 10 ** 1.71 * 0.8, "$r^{1{,}71}$", fontsize=8, color=FG)
    ax.axvspan(4, 22, color=AZUL, alpha=0.06)
    ax.set_xlabel("$r$"); ax.set_ylabel("$C(r)$ (fração dos pares a distância $\\leq r$)")
    ax.legend(fontsize=6.5, ncol=2, frameon=False, loc="lower right")
    fig.tight_layout(); fig.savefig(FIG / "corr_curves.png", dpi=200); plt.close(fig)

    def meio(w):
        lo, hi = w[1:].split("_"); return float(np.sqrt(float(lo) * float(hi)))
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    g = loc[loc.method == "corr"].copy(); g["x"] = g.window.map(meio)
    for ts in TS:
        q = g[g.ts == ts].sort_values("x")
        ax.errorbar(q.x, q.slope_section_mean, yerr=q.slope_section_se, fmt="o-", color=cores[ts], ms=3.5, lw=1.1, capsize=2, label=f"$T_s={ts}$")
    d = loc[loc.method == "corr_disc"].copy(); d["x"] = d.window.map(meio)
    for ts, ls in [(2, "--"), (8192, "-.")]:
        q = d[d.ts == ts].sort_values("x")
        ax.plot(q.x, q.slope_section_mean, ls, color=CINZA, lw=1.2, label=f"disco uniforme, $\\bar R$ de $T_s={ts}$")
    ax.axhline(2.0, color=FG, lw=0.6, ls="--"); ax.axhline(1.71, color=FG, lw=0.6, ls=":")
    ax.text(2.7, 2.01, "disco, 2", fontsize=8, color=FG); ax.text(2.7, 1.72, "DLA plano, 1,71", fontsize=8, color=FG)
    ax.set_xscale("log"); ax.set_xlim(2.5, 200); ax.set_ylim(0, 2.2)
    ax.set_xlabel("$r$ (ponto no meio da meia década)"); ax.set_ylabel("$d\\log C / d\\log r$")
    ax.legend(fontsize=6.5, ncol=2, frameon=False, loc="lower left")
    fig.tight_layout(); fig.savefig(FIG / "corr_local_slope.png", dpi=200); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    for col, lab, cor, mk in [("corr_primary", "$D_2$ bruta, $4 \\leq r \\leq \\bar R/3$", AZUL, "o"),
                              ("corr_primary_disc", "disco uniforme (só borda)", CINZA, "s"),
                              ("corr_primary_corrected", "$D_2$ corrigida = bruta − disco + 2", VERMELHO, "D")]:
        ax.errorbar(TS, sm[f"{col}_mean"], yerr=sm[f"{col}_se"], fmt=mk + "-", color=cor, ms=4, lw=1, capsize=2, label=lab)
    ax.axhline(2.0, color=FG, lw=0.6, ls="--"); ax.axhline(1.71, color=FG, lw=0.6, ls=":")
    ax.text(2.2, 2.005, "disco, 2", fontsize=8, color=FG); ax.text(2.2, 1.715, "DLA plano, 1,71", fontsize=8, color=FG)
    ax.set_xscale("log"); ax.set_xlabel("$T_s$"); ax.set_ylabel("$D_2$"); ax.set_ylim(1.5, 2.1)
    ax.legend(fontsize=7, frameon=False, loc="lower right")
    fig.tight_layout(); fig.savefig(FIG / "corr_df_vs_ts.png", dpi=200); plt.close(fig)
    print("figuras de correlacao em", FIG)


if __name__ == "__main__":
    main()
    figura_inclinacoes_locais()
    figuras_correlacao()


def figura_largura() -> None:
    """F_rup/R e p99 contra a largura do recorte (questao 3), se o resumo existir."""
    caminho = N18 / "width_fracture_summary.csv"
    if not caminho.exists():
        return
    s = pd.read_csv(caminho, comment="#")
    plt.style.use(RAIZ / "Code" / "Data_analysis" / "xmgrace_paper.mplstyle")
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.8))
    cores = {2: CMAP(0.0), 32: CMAP(0.33), 128: CMAP(0.6), 8192: CMAP(1.0)}
    for ts in sorted(s.ts.unique()):
        loc = s[(s.ts == ts) & s.source.str.startswith("local")].sort_values("width")
        lad = s[(s.ts == ts) & s.source.str.startswith("ladder")].sort_values("width")
        ax[0].errorbar(loc.width, loc.F_rup_per_rod_mean, yerr=loc.F_rup_per_rod_se, fmt="o-", color=cores.get(ts, CINZA),
                       ms=5, capsize=3, lw=1.2, label=f"$T_s={ts}$, 5 sementes")
        if len(lad):
            ax[0].plot(lad.width, lad.F_rup_per_rod_mean, "s--", color=cores.get(ts, CINZA), ms=4, lw=0.8, mfc="none",
                       label=f"$T_s={ts}$, escada 02/09 (1 semente)")
        ax[1].plot(loc.width, loc.p99_pre_mean, "o-", color=cores.get(ts, CINZA), ms=5, lw=1.2)
        if len(lad):
            ax[1].plot(lad.width, lad.p99_pre_mean, "s--", color=cores.get(ts, CINZA), ms=4, lw=0.8, mfc="none")
    ax[0].set_xscale("log"); ax[0].set_xlabel("largura do recorte (unidades de rede)"); ax[0].set_ylabel("$F_{rup}/R$ (por molécula portante)")
    ax[0].set_ylim(0, 0.85); ax[0].legend(fontsize=6, frameon=False, ncol=1)
    ax[1].set_xscale("log"); ax[1].set_xlabel("largura do recorte"); ax[1].set_ylabel("p99 preterminal (média por realização)")
    from matplotlib.ticker import NullFormatter
    for a in ax:
        a.set_xticks([17, 41, 81, 141, 181]); a.set_xticklabels(["17", "41", "81", "141", "181"])
        a.xaxis.set_minor_formatter(NullFormatter())
    fig.tight_layout(); fig.savefig(FIG / "frup_per_rod_by_width.png", dpi=200); plt.close(fig)
    print("figura de largura em", FIG)


if __name__ == "__main__":
    figura_largura()

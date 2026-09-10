#!/usr/bin/env python3
"""Da para tirar m como variavel? Separabilidade F_rup(T_s, m) = A(T_s) g(m) e afins.

Lê:      Reviews/N9_damage_curves/damage_summary.csv
         Reviews/N9_damage_curves/damage_condition_table.csv
         Reviews/N10_cascade_survival/cascades_npz/casc_ts<TS>_m<M>_pre.npz (50)
Escreve: Reviews/N18_df_ten_ts/frup_m_separability.csv
         Reviews/N18_df_ten_ts/statistics_two_way_decomposition.csv
         Reviews/N18_df_ten_ts/cascade_stats_by_condition.csv
         Reviews/N18_df_ten_ts/figures/frup_ratio_vs_m.png
Chamado: à mão, para N18 (Estado_revisao_ER12738.md); so dados existentes

O teste. Se a forca de ruptura separa em produto, log F(T_s, m) = log A(T_s)
+ log g(m) e a matriz de residuos de um modelo aditivo em log e nula dentro do
erro. g(m) e estimado pela media geometrica de F(T_s, m)/F(T_s, 2) sobre
T_s >= 16 (o regime compacto); A(T_s) = F(T_s, 2). O nulo de comparacao e a
forca por fibra do fiber bundle de carga igual (ELS) com limiares de CDF x^m em
[0, 1]: sigma*(m) = (m/(m+1)) (m+1)^(-1/m), o maximo de x [1 - x^m]. A mesma
decomposicao em dois fatores (escala log) e aplicada ao dano preterminal e a
estatistica das cascatas, para ver o que separa e o que nao separa. O erro
padrao de log F usa cv/sqrt(200): sao 200 fibrilas por condicao, e as 50
realizacoes por fibrila nao sao independentes da arquitetura.
"""
from __future__ import annotations

import csv
import pathlib

import numpy as np
import pandas as pd
import scipy.sparse as sp

RAIZ = pathlib.Path(__file__).resolve().parents[2]
N9 = RAIZ / "Reviews" / "N9_damage_curves"
NPZ = RAIZ / "Reviews" / "N10_cascade_survival" / "cascades_npz"
OUT = RAIZ / "Reviews" / "N18_df_ten_ts"
TS = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]
MS = [1, 2, 3, 5, 10]
TS_COMPACTO = [t for t in TS if t >= 16]


def sigma_els(m: float) -> float:
    return (m / (m + 1.0)) * (m + 1.0) ** (-1.0 / m)


def cascade_stats() -> pd.DataFrame:
    rows = []
    for ts in TS:
        for m in MS:
            M = sp.load_npz(NPZ / f"casc_ts{ts}_m{m}_pre.npz")
            c = np.asarray(M.sum(axis=0)).ravel().astype(float)   # indice = tamanho
            s = np.arange(len(c))
            tot = c.sum()
            cdf = np.cumsum(c) / tot
            rows.append(dict(ts=ts, m=m, n_cascades=int(tot),
                             frac1=c[1] / tot,
                             p90=int(s[np.searchsorted(cdf, 0.90)]),
                             p99=int(s[np.searchsorted(cdf, 0.99)]),
                             mean_size=(s * c).sum() / tot,
                             max_size=int(s[c > 0].max())))
    return pd.DataFrame(rows)


def two_way(tab: pd.DataFrame, col: str, log: bool = True) -> dict:
    """x_ij = mu + a_i + b_j + e_ij sobre a grade T_s x m; devolve parcela de
    variancia da interacao, max |e| e a matriz de residuos."""
    P = tab.pivot(index="ts", columns="m", values=col).loc[TS, MS]
    X = np.log(P.values) if log else P.values
    mu = X.mean()
    a = X.mean(axis=1, keepdims=True) - mu
    b = X.mean(axis=0, keepdims=True) - mu
    E = X - mu - a - b
    ss_tot = ((X - mu) ** 2).sum()
    return dict(interaction_share=float((E ** 2).sum() / ss_tot),
                row_share=float((a ** 2).sum() * X.shape[1] / ss_tot),
                col_share=float((b ** 2).sum() * X.shape[0] / ss_tot),
                max_abs_resid=float(np.abs(E).max()),
                resid=pd.DataFrame(E, index=TS, columns=MS))


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "figures").mkdir(exist_ok=True)
    summ = pd.read_csv(N9 / "damage_summary.csv")
    cond = pd.read_csv(N9 / "damage_condition_table.csv")
    casc = cascade_stats()
    casc.to_csv(OUT / "cascade_stats_by_condition.csv", index=False, float_format="%.6g")

    # --- separabilidade de F_rup
    F = summ.pivot(index="ts", columns="m", values="f_rup_mean").loc[TS, MS]
    CV = summ.pivot(index="ts", columns="m", values="f_rup_cv").loc[TS, MS]
    NFIB = summ.pivot(index="ts", columns="m", values="n_fibrils").loc[TS, MS]
    se_logF = CV / np.sqrt(NFIB)
    ratio = F.div(F[2], axis=0)
    g = np.exp(np.log(ratio.loc[TS_COMPACTO]).mean(axis=0))          # g(m), g(2) = 1
    resid = np.log(F) - np.log(F[[2]].values) - np.log(g.values)[None, :]
    els = pd.Series({m: sigma_els(m) / sigma_els(2) for m in MS})
    linhas = []
    for m in MS:
        linhas.append(dict(quantity="g_empirical", m=m, value=g[m]))
        linhas.append(dict(quantity="els_ratio_sigma_star", m=m, value=els[m]))
        linhas.append(dict(quantity="sigma_star_els", m=m, value=sigma_els(m)))
    for ts in TS:
        for m in MS:
            linhas.append(dict(quantity="ratio_to_m2", ts=ts, m=m, value=ratio.loc[ts, m]))
            linhas.append(dict(quantity="log_resid_empirical", ts=ts, m=m,
                               value=resid.loc[ts, m], se=se_logF.loc[ts, m]))
            linhas.append(dict(quantity="log_resid_els", ts=ts, m=m,
                               value=np.log(ratio.loc[ts, m] / els[m]), se=se_logF.loc[ts, m]))
    for ts in TS:
        linhas.append(dict(quantity="A_ts_frup_m2", ts=ts, value=F.loc[ts, 2]))
        r = F.loc[ts] / g
        linhas.append(dict(quantity="spread_after_g_maxmin", ts=ts, value=r.max() / r.min()))
        r2 = F.loc[ts] / els
        linhas.append(dict(quantity="spread_after_els_maxmin", ts=ts, value=r2.max() / r2.min()))
        linhas.append(dict(quantity="spread_raw_maxmin", ts=ts, value=F.loc[ts].max() / F.loc[ts].min()))
    pd.DataFrame(linhas).to_csv(OUT / "frup_m_separability.csv", index=False, float_format="%.6g")

    # --- decomposicao em dois fatores para varias estatisticas
    tab = summ.merge(cond[["ts", "m", "f_rup_per_rod", "phi_preterminal"]], on=["ts", "m"])
    tab = tab.merge(casc, on=["ts", "m"])
    dec = []
    for col in ["f_rup_mean", "f_rup_per_rod", "terminal_fraction_mean", "phi_preterminal",
                "frac1", "p90", "p99", "mean_size"]:
        d = two_way(tab, col, log=True)
        dec.append(dict(statistic=col, scale="log", interaction_share=d["interaction_share"],
                        ts_share=d["row_share"], m_share=d["col_share"],
                        max_abs_resid=d["max_abs_resid"],
                        max_abs_resid_ts_ge_16=float(np.abs(d["resid"].loc[TS_COMPACTO]).max().max()),
                        range_over_m_at_ts8192=float(tab[tab.ts == 8192][col].max() / tab[tab.ts == 8192][col].min()),
                        range_over_ts_at_m2=float(tab[tab.m == 2][col].max() / tab[tab.m == 2][col].min())))
    pd.DataFrame(dec).to_csv(OUT / "statistics_two_way_decomposition.csv", index=False, float_format="%.5g")

    # --- figura interna
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.style.use(RAIZ / "Code" / "Data_analysis" / "xmgrace_paper.mplstyle")
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    for ts in TS:
        ax[0].plot(MS, ratio.loc[ts], "o-", ms=3, lw=0.8, label=f"$T_s={ts}$")
    ax[0].plot(MS, g.values, "k--", lw=1.5, label="$g(m)$, $T_s\\geq16$")
    ax[0].plot(MS, els.values, "k:", lw=1.5, label="ELS $\\sigma^*(m)/\\sigma^*(2)$")
    ax[0].set_xlabel("$m$"); ax[0].set_ylabel("$F_{rup}(T_s,m)/F_{rup}(T_s,2)$")
    ax[0].set_xscale("log"); ax[0].legend(fontsize=6, ncol=2)
    for ts in TS:
        ax[1].plot(MS, resid.loc[ts], "o-", ms=3, lw=0.8, label=f"$T_s={ts}$")
    ax[1].axhline(0, color="k", lw=0.8)
    ax[1].set_xlabel("$m$"); ax[1].set_ylabel("$\\log F - \\log A(T_s) - \\log g(m)$")
    ax[1].set_xscale("log")
    fig.tight_layout()
    fig.savefig(OUT / "figures" / "frup_ratio_vs_m.png", dpi=200)

    # --- relatorio no terminal
    print("g(m) empirico (T_s>=16):", {m: round(float(g[m]), 4) for m in MS})
    print("ELS sigma*(m)/sigma*(2):", {m: round(float(els[m]), 4) for m in MS})
    print("\nspread max/min de F_rup por T_s: bruto | apos g(m) | apos ELS")
    for ts in TS:
        r = F.loc[ts] / g; r2 = F.loc[ts] / els
        print(f"  T_s={ts:5d}  {F.loc[ts].max()/F.loc[ts].min():.3f} | {r.max()/r.min():.3f} | {r2.max()/r2.min():.3f}")
    print("\nresiduo log (empirico), max |e| por T_s, contra EP tipico:")
    for ts in TS:
        print(f"  T_s={ts:5d}  max|e|={np.abs(resid.loc[ts]).max():.4f}  EP~{se_logF.loc[ts].mean():.4f}")
    print("\ndecomposicao em dois fatores (escala log):")
    print(pd.DataFrame(dec).to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    main()

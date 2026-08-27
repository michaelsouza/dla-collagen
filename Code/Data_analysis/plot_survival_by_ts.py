#!/usr/bin/env python3
"""Survival of the cascade size at fixed m, across T_s, against the Araujo fit."""
import csv, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import sparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avalanche_statistics import fit_generalized_cutoff, distribution_cdf

ROOT = "/petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign"
CASC = f"{ROOT}/analysis/cascades"
OUT = f"{CASC}/survival_m2.png"

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#10151c", "#3d4654", "#6d7787", "#e6e4e0"
RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]
M = 2
SHOWN = [2, 16, 128, 1024, 8192]

rows = {(int(r["ts"]), int(r["m"])): r
        for r in csv.DictReader(open(f"{CASC}/araujo_fits.csv"))}

fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.6, 5.0),
                             gridspec_kw=dict(width_ratios=[1.05, 1], wspace=0.24))
fig.patch.set_facecolor(SURFACE)

for idx, (ts, color) in enumerate(zip(SHOWN, RAMP)):
    r = rows[(ts, M)]
    xmin = int(r["xmin"])
    counts = np.asarray(sparse.load_npz(f"{CASC}/casc_ts{ts}_m{M}_pre.npz")
                        .sum(axis=0)).ravel()
    sizes = np.arange(len(counts))
    tail = sizes >= xmin
    emp = 1.0 - np.cumsum(counts[tail]) / counts[tail].sum()
    obs = sizes[tail]
    keep = emp > 3e-7
    fit = fit_generalized_cutoff(counts, xmin=xmin)

    # (a) data as points, fit as a line on a dense grid
    ax.plot(obs[keep], emp[keep], lw=0, marker="o", ms=3.0, color=color,
            alpha=.65, zorder=3)
    grid = np.unique(np.round(np.logspace(np.log10(xmin), np.log10(obs[keep].max()), 260)))
    model = 1.0 - distribution_cdf(fit, grid)
    good = model > 1e-7
    # The curves for T_s >= 16 almost coincide -- which is itself the result --
    # so a legend replaces direct labels here.
    ax.plot(grid[good], model[good], lw=1.8, color=color, zorder=4,
            solid_capstyle="round", label=f"$T_s$ = {ts}")

    # (b) ratio
    m_obs = 1.0 - distribution_cdf(fit, obs[keep])
    ratio = np.where(m_obs > 0, emp[keep] / np.maximum(m_obs, 1e-300), np.nan)
    bx.plot(obs[keep], ratio, lw=1.8, color=color, zorder=3, solid_capstyle="round")
    # Label where the curve leaves the flat band, where the five are far apart.
    # All five cross the same ratio at nearby s, so the labels are staggered
    # vertically by condition instead of sitting on the crossing.
    above = np.where(ratio > 2.2)[0]
    if len(above):
        k = above[0]
        bx.annotate(f"$T_s$={ts}", (obs[keep][k], ratio[k]),
                    textcoords="offset points", xytext=(9, 4 + 15 * (2 - idx)),
                    va="center", fontsize=9.5, color=color, zorder=5)

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_ylim(2e-7, 1.8)
ax.set_xlabel("tamanho da cascata,  $s$", fontsize=11.5, color=INK2)
ax.set_ylabel("$P(S \\geq s)$", fontsize=11.5, color=INK2)
ax.set_title("(a)  Sobrevivência e o ajuste de Araújo,  $m$ = 2",
             fontsize=12.5, color=INK, pad=12, loc="left")
ax.legend(frameon=False, fontsize=9.5, loc="lower left", labelcolor=INK2,
          handlelength=1.6, borderaxespad=1.1)
ax.annotate("pontos: dados    linha: ajuste", (0.975, 0.955), xycoords="axes fraction",
            ha="right", va="top", fontsize=9.5, color=MUTED)

bx.axhline(1.0, color=INK2, lw=1.2, ls=(0, (4, 3)), zorder=4)
bx.set_xscale("log"); bx.set_yscale("log")
bx.set_ylim(0.28, 30)
bx.set_xlim(1.7, 700)
bx.set_yticks([0.3, 0.5, 1, 2, 5, 10, 20])
bx.set_yticklabels(["0,3", "0,5", "1", "2", "5", "10", "20"])
bx.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
bx.set_xlabel("tamanho da cascata,  $s$", fontsize=11.5, color=INK2)
bx.set_ylabel("dados / ajuste", fontsize=11.5, color=INK2)
bx.set_title("(b)  Onde o ajuste erra", fontsize=12.5, color=INK, pad=12, loc="left")
bx.annotate("1 = ajuste exato", (0.035, 0.50), xycoords="axes fraction",
            fontsize=9.5, color=INK2)
bx.annotate("acima: o ajuste subestima\na frequência dos eventos grandes",
            (0.035, 0.95), xycoords="axes fraction", va="top",
            fontsize=9.5, color=MUTED)

for a in (ax, bx):
    a.set_facecolor(SURFACE)
    a.grid(True, color=GRID, lw=.8, zorder=0); a.set_axisbelow(True)
    for s in ("top", "right"): a.spines[s].set_visible(False)
    for s in ("left", "bottom"): a.spines[s].set_color(GRID)
    a.tick_params(colors=MUTED, labelsize=10, length=0)

fig.text(0.006, 0.017,
         "$m$ = 2, 200 fibrilas × 50 realizações por condição.  Ajuste: "
         "$p(s)\\propto s^{-\\gamma}\\exp[-(s/s_c)^{\\eta}]$ sobre $s \\geq x_{min}$, com $x_{min}$ "
         "escolhido por KS com piso de 5% na cauda.",
         fontsize=8.5, color=MUTED)
fig.subplots_adjust(left=0.068, right=0.965, top=0.90, bottom=0.155)
fig.savefig(OUT, dpi=175, facecolor=SURFACE)
print("wrote", OUT)
for ts in SHOWN:
    r = rows[(ts, M)]
    print(f"  ts={ts:>5} xmin={r['xmin']} gamma={float(r['gamma']):.3f} "
          f"eta={float(r['eta']):.2f} s_c={float(r['s_c']):.1f}")

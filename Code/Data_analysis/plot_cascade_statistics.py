#!/usr/bin/env python3
"""Figure: cascade-size statistics under the Clauset et al. (2009) procedure."""
import csv, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import sparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avalanche_statistics import (fit_competing_models, distribution_cdf)

ROOT = "/petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign"
CASC = f"{ROOT}/analysis/cascades"
OUT = f"{CASC}/cascade_statistics.png"

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#10151c", "#3d4654", "#6d7787", "#e6e4e0"
# The exponential is fitted too, but it is the one family the power law beats
# almost everywhere, so drawing it would only add a line nobody is choosing.
C = {"power_law": "#2a78d6", "cutoff_power_law": "#eb6834",
     "lognormal": "#1baf7a", "stretched_exponential": "#eda100"}
LAB = {"power_law": "lei de potência", "cutoff_power_law": "com corte",
       "lognormal": "log-normal", "stretched_exponential": "esticada"}
RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]
TS = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]
MS = [1, 2, 3, 5, 10]

rows = {(int(r["ts"]), int(r["m"])): r
        for r in csv.DictReader(open(f"{CASC}/cascade_stats_clauset.csv"))}

fig, (ax, bx, cx) = plt.subplots(
    1, 3, figsize=(15.2, 4.8),
    gridspec_kw=dict(width_ratios=[1.25, 1, 1], wspace=0.29))
fig.patch.set_facecolor(SURFACE)

# ---------- (a) CCDF with the four fitted families ----------
SHOW_TS, SHOW_M = 128, 2
pre = sparse.load_npz(f"{CASC}/casc_ts{SHOW_TS}_m{SHOW_M}_pre.npz")
counts = np.asarray(pre.sum(axis=0)).ravel()
xmin = int(rows[(SHOW_TS, SHOW_M)]["xmin"])
sizes = np.arange(len(counts))
tail = sizes >= xmin
n_tail = counts[tail].sum()
ccdf = 1.0 - np.cumsum(counts[tail]) / n_tail
obs = sizes[tail]
keep = ccdf > 0
ax.plot(obs[keep], ccdf[keep], lw=0, marker="o", ms=3.2, color=INK2,
        alpha=.55, zorder=3, label="dados")

models = fit_competing_models(counts, xmin=xmin)
grid = np.unique(np.round(np.logspace(np.log10(xmin), np.log10(obs.max()), 220)))
for name, fit in models.items():
    if name not in C:
        continue
    surv = 1.0 - distribution_cdf(fit, grid)
    good = surv > 1e-7
    ax.plot(grid[good], surv[good], lw=2, color=C[name], zorder=4,
            label=LAB[name], solid_capstyle="round")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_ylim(1e-6, 1.6)
ax.set_xlabel("tamanho da cascata,  $s$", fontsize=11.5, color=INK2)
ax.set_ylabel("$P(S \\geq s)$", fontsize=11.5, color=INK2)
ax.set_title(f"$T_s$={SHOW_TS}, $m$={SHOW_M}: a cauda é curva",
             fontsize=12.5, color=INK, pad=12, loc="left")
ax.legend(frameon=False, fontsize=9.5, loc="lower left", labelcolor=INK2)
ax.annotate(f"{int(n_tail):,} cascatas".replace(",", " "),
            (0.97, 0.95), xycoords="axes fraction", ha="right",
            fontsize=9.5, color=MUTED)

# ---------- (b) gamma of the cutoff model ----------
for m, color in zip(MS, RAMP):
    v = [float(rows[(t, m)]["cutf_gamma"]) for t in TS]
    e = [float(rows[(t, m)]["cutf_se_gamma"]) for t in TS]
    bx.errorbar(TS, v, yerr=e, lw=2, marker="o", ms=6, color=color,
                mec=SURFACE, mew=1.4, capsize=2.5, zorder=3)
    bx.annotate(f"$m$={m}", (TS[-1], v[-1]), textcoords="offset points",
                xytext=(8, 0), va="center", fontsize=9.5, color=color, zorder=5)
bx.axhline(2.5, color=MUTED, lw=1, ls=(0, (4, 3)), zorder=2)
bx.annotate("campo médio ELS, 5/2", (2.4, 2.5), textcoords="offset points",
            xytext=(0, 5), fontsize=9.5, color=MUTED, zorder=5)
bx.set_xscale("log", base=2); bx.set_xlim(1.6, 30000)
bx.set_xticks([2, 16, 128, 1024, 8192]); bx.set_xticklabels(["2","16","128","1024","8192"])
bx.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
bx.set_xticks(TS, minor=True); bx.tick_params(axis="x", which="minor", length=0)
bx.set_xlabel("difusão superficial,  $T_s$", fontsize=11.5, color=INK2)
bx.set_ylabel("$\\gamma$  (modelo com corte)", fontsize=11.5, color=INK2)
bx.set_ylim(1.55, 2.95)
bx.set_title("Expoente", fontsize=12.5, color=INK, pad=12, loc="left")

# ---------- (c) cutoff scale ----------
for m, color in zip(MS, RAMP):
    v = [float(rows[(t, m)]["cutf_sc"]) for t in TS]
    cx.plot(TS, v, lw=2, marker="o", ms=6, color=color, mec=SURFACE, mew=1.4, zorder=3)
    # m=5 and m=10 converge to the same cutoff, so their labels are nudged
    # apart rather than printed on top of each other.
    dy = {5: 7, 10: -8}.get(m, 0)
    cx.annotate(f"$m$={m}", (TS[-1], v[-1]), textcoords="offset points",
                xytext=(8, dy), va="center", fontsize=9.5, color=color, zorder=5)
cx.set_xscale("log", base=2); cx.set_xlim(1.6, 30000)
cx.set_yscale("log")
cx.set_xticks([2, 16, 128, 1024, 8192]); cx.set_xticklabels(["2","16","128","1024","8192"])
cx.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
cx.set_xticks(TS, minor=True); cx.tick_params(axis="x", which="minor", length=0)
cx.set_ylim(13, 260)
cx.set_yticks([15, 30, 60, 120, 240]); cx.set_yticklabels(["15","30","60","120","240"])
cx.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
cx.set_xlabel("difusão superficial,  $T_s$", fontsize=11.5, color=INK2)
cx.set_ylabel("escala de corte,  $s_c = 1/\\lambda$", fontsize=11.5, color=INK2)
cx.set_title("Onde a cauda termina", fontsize=12.5, color=INK, pad=12, loc="left")

for a in (ax, bx, cx):
    a.grid(True, color=GRID, lw=.8, zorder=0); a.set_axisbelow(True)
    for s in ("top", "right"): a.spines[s].set_visible(False)
    for s in ("left", "bottom"): a.spines[s].set_color(GRID)
    a.tick_params(colors=MUTED, labelsize=10, length=0)

fig.text(0.006, 0.018,
         "61 000 717 cascatas preterminais.  $x_{min}$ por minimização de KS com piso de 5% na cauda; "
         "MLE discreto exato; aderência por 2500 réplicas semiparamétricas (Clauset, Shalizi & Newman 2009).",
         fontsize=8.5, color=MUTED)
fig.subplots_adjust(left=0.052, right=0.962, top=0.90, bottom=0.175)
fig.savefig(OUT, dpi=175, facecolor=SURFACE)
print("wrote", OUT)

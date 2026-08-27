#!/usr/bin/env python3
"""Figure: local packing against density, and the pair correlation it implies.

Coordination and density are not independent.  In a random medium of density
phi an occupied site has 4*phi occupied neighbours, so coordination = phi -- a
diagonal of slope one.  The distance from that diagonal is the pair correlation
at unit distance, g(1) = coordination / phi, and it is what separates a
dendritic aggregate (locally dense, globally sparse) from a compact one.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm

ROOT = "/petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign"
SRC = f"{ROOT}/analysis/compaction/compaction.json"
OUT = f"{ROOT}/analysis/compaction/pair_correlation.png"

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#10151c", "#3d4654", "#6d7787", "#e6e4e0"
ACCENT, WASH = "#1c5cab", "#86b6ef"
# Single-hue sequential ramp, 100 -> 700, for the continuous magnitude T_s.
BLUES = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#1c5cab", "#0d366b"]
CMAP = LinearSegmentedColormap.from_list("dla_blues", BLUES)
TS = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]

res = json.load(open(SRC))
phi = np.array([res[str(t)]["phi"][0] for t in TS])
phi_e = np.array([res[str(t)]["phi"][1] for t in TS])
co = np.array([res[str(t)]["coord"][0] for t in TS])
co_e = np.array([res[str(t)]["coord"][1] for t in TS])
g1 = np.array([res[str(t)]["g1"][0] for t in TS])
g1_e = np.array([res[str(t)]["g1"][1] for t in TS])

fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.4, 5.0),
                             gridspec_kw=dict(width_ratios=[1.08, 1], wspace=0.26))
fig.patch.set_facecolor(SURFACE)
norm = LogNorm(2, 8192)

# ---------- (a) coordination against density ----------
ax.set_facecolor(SURFACE)
lim = (0.10, 0.85)
ax.plot(lim, lim, color=MUTED, lw=1.4, ls=(0, (4, 3)), zorder=2)
# The top-right corner holds the T_s = 8192 point; the diagonal is labelled
# below it, where nothing else sits.
ax.annotate("diagonal: meio aleatório,  $g(1)=1$", (0.82, 0.28), ha="right",
            va="center", fontsize=9.5, color=MUTED, zorder=5)
ax.plot(phi, co, lw=1.4, color=WASH, zorder=3)
ax.errorbar(phi, co, xerr=phi_e, yerr=co_e, fmt="none",
            ecolor=MUTED, elinewidth=1.1, capsize=2.5, zorder=4)
ax.scatter(phi, co, c=TS, cmap=CMAP, norm=norm, s=95, zorder=5,
           edgecolor=SURFACE, linewidth=1.6)
for t, x, y, dx, dy in ((2, phi[0], co[0], 10, -4), (8192, phi[-1], co[-1], 13, -9)):
    ax.annotate(f"$T_s$={t}", (x, y), textcoords="offset points", xytext=(dx, dy),
                ha="left" if dx > 0 else "right", fontsize=10, color=INK2, zorder=6)
ax.annotate("acima da diagonal:\nsítios ocupados se agrupam", (0.135, 0.72),
            fontsize=9.5, color=INK2, zorder=5)
ax.set_xlim(*lim); ax.set_ylim(*lim); ax.set_aspect("equal")
ax.set_xlabel("densidade da seção,  $\\phi = \\rho(R/2)$", fontsize=11.5, color=INK2)
ax.set_ylabel("coordenação  (vizinhos ocupados / 4)", fontsize=11.5, color=INK2)
ax.set_title("Empacotamento local contra densidade",
             fontsize=12.5, color=INK, pad=12, loc="left")
cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=CMAP), ax=ax,
                  fraction=0.045, pad=0.02)
cb.set_label("$T_s$", fontsize=11, color=INK2)
cb.outline.set_visible(False)
cb.ax.tick_params(colors=MUTED, labelsize=9, length=0)

# ---------- (b) g(1) against T_s ----------
bx.set_facecolor(SURFACE)
bx.axhline(1.0, color=MUTED, lw=1.2, ls=(0, (4, 3)), zorder=2)
bx.axvspan(100, 30000, color=WASH, alpha=.18, lw=0, zorder=1)
bx.errorbar(TS, g1, yerr=g1_e, lw=2, marker="o", ms=8, color=ACCENT,
            mec=SURFACE, mew=1.8, capsize=3, zorder=3)
bx.set_xscale("log", base=2); bx.set_xlim(1.6, 22000)
bx.set_xticks([2, 16, 128, 1024, 8192]); bx.set_xticklabels(["2","16","128","1024","8192"])
bx.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
bx.set_xticks(TS, minor=True); bx.tick_params(axis="x", which="minor", length=0)
bx.set_ylim(0.97, 2.03)
plateau = g1[TS.index(128):].mean()
bx.annotate(f"platô  $g(1)\\approx${plateau:.2f}\na partir de $T_s$=128",
            (1400, 1.30), ha="center", fontsize=9.5, color=INK2, zorder=5)
bx.annotate(f"{g1[0]:.2f}", (TS[0], g1[0]), textcoords="offset points",
            xytext=(11, -2), fontsize=10, color=INK2)
bx.annotate("empacotamento aleatório", (2.4, 1.0), textcoords="offset points",
            xytext=(0, 7), fontsize=9.5, color=MUTED)
bx.set_xlabel("difusão superficial,  $T_s$", fontsize=11.5, color=INK2)
bx.set_ylabel("$g(1) = $ coordenação $/\\ \\phi$", fontsize=12, color=INK2)
bx.set_title("Correlação de pares à distância 1",
             fontsize=12.5, color=INK, pad=12, loc="left")

for a in (ax, bx):
    a.grid(True, color=GRID, lw=.8, zorder=0); a.set_axisbelow(True)
    for s in ("top", "right"): a.spines[s].set_visible(False)
    for s in ("left", "bottom"): a.spines[s].set_color(GRID)
    a.tick_params(colors=MUTED, labelsize=10, length=0)

fig.text(0.006, 0.017,
         "25 fibrilas por condição, 11 seções por fibrila.  $g(1)$ é formado por fibrila antes de "
         "promediado, de modo que a barra de erro carrega a correlação entre numerador e denominador.",
         fontsize=8.5, color=MUTED)
fig.subplots_adjust(left=0.068, right=0.985, top=0.90, bottom=0.155)
fig.savefig(OUT, dpi=175, facecolor=SURFACE)
print("wrote", OUT)
for t, p, c, g, e in zip(TS, phi, co, g1, g1_e):
    print(f"  ts={t:>5} phi={p:.3f} coord={c:.3f} g1={g:.3f}±{e:.3f}")

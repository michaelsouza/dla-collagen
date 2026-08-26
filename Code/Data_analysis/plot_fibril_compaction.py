#!/usr/bin/env python3
"""Figure: compaction of the cross-section with T_s, no fitted exponent."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = "/petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign"
SRC = f"{ROOT}/analysis/compaction/compaction.json"
OUT = f"{ROOT}/analysis/compaction/compaction.png"

SURFACE = "#fcfcfb"
INK, INK2, MUTED, GRID = "#10151c", "#3d4654", "#6d7787", "#e6e4e0"
ACCENT, WASH = "#1c5cab", "#86b6ef"
RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]
TS = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]
SHOWN = [2, 16, 64, 512, 8192]

res = json.load(open(SRC))

fig, (ax, bx, cx) = plt.subplots(
    1, 3, figsize=(15.0, 4.7),
    gridspec_kw=dict(width_ratios=[1.35, 1, 1], wspace=0.30))
fig.patch.set_facecolor(SURFACE)

# ---------- (a) local density profile ----------
ax.set_facecolor(SURFACE)
for ts, color in zip(SHOWN, RAMP):
    d = res[str(ts)]
    R = d["R"][0]
    r = np.array(d["profile_x"]) * R
    rho = np.array(d["profile"])
    keep = (r >= 2.6) & (r <= R / 2)          # lattice cutoff to half the section
    ax.plot(r[keep], rho[keep], lw=2.2, color=color, solid_capstyle="round", zorder=3)
    ax.plot([r[keep][-1]], [rho[keep][-1]], "o", ms=7, color=color,
            mec=SURFACE, mew=1.6, zorder=4)
    lab = "$T_s\\geq$512" if ts == 8192 else f"$T_s$={ts}"
    if ts != 512:
        ax.annotate(lab, (r[keep][-1], rho[keep][-1]), textcoords="offset points",
                    xytext=(9, 0), va="center", fontsize=10, color=color, zorder=5)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(2.4, 30); ax.set_ylim(0.06, 1.05)
ax.set_xticks([3, 5, 10, 20]); ax.set_xticklabels(["3", "5", "10", "20"])
ax.set_yticks([0.1, 0.2, 0.4, 0.8]); ax.set_yticklabels(["0,1", "0,2", "0,4", "0,8"])
ax.set_xlabel("raio  $r$  (sítios)", fontsize=11.5, color=INK2)
ax.set_ylabel("densidade local  $\\rho(r)=N(r)/\\pi r^2$", fontsize=11.5, color=INK2)
ax.set_title("Densidade: plana é compacto, inclinada é fractal",
             fontsize=12.5, color=INK, pad=12, loc="left")
ax.annotate("cada curva termina em $R/2$,\no raio útil da sua condição",
            (0.035, 0.06), xycoords="axes fraction", fontsize=9.5, color=MUTED)

# ---------- (b) coordination ----------
bx.set_facecolor(SURFACE)
v = [res[str(t)]["coord"][0] for t in TS]
e = [res[str(t)]["coord"][1] for t in TS]
bx.errorbar(TS, v, yerr=e, color=ACCENT, lw=2, marker="o", ms=7.5,
            mec=SURFACE, mew=1.8, capsize=3, zorder=3)
bx.set_xscale("log", base=2); bx.set_xlim(1.6, 11000)
bx.set_xticks([2, 16, 128, 1024, 8192])
bx.set_xticklabels(["2", "16", "128", "1024", "8192"])
bx.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
bx.set_xticks(TS, minor=True); bx.tick_params(axis="x", which="minor", length=0)
bx.set_ylim(0.28, 0.84)
bx.set_xlabel("difusão superficial,  $T_s$", fontsize=11.5, color=INK2)
bx.set_ylabel("coordenação  (vizinhos ocupados / 4)", fontsize=11.5, color=INK2)
bx.set_title("Empacotamento local", fontsize=12.5, color=INK, pad=12, loc="left")
bx.annotate(f"{v[0]:.2f}", (TS[0], v[0]), textcoords="offset points",
            xytext=(11, -2), fontsize=10, color=INK2)
bx.annotate(f"{v[-1]:.2f}", (TS[-1], v[-1]), textcoords="offset points",
            xytext=(-6, -14), ha="right", fontsize=10, color=INK2)
bx.annotate("nenhuma escolha livre:\nsó vizinhos de rede",
            (0.05, 0.88), xycoords="axes fraction", fontsize=9.5, color=MUTED)

# ---------- (c) density ratio ----------
cx.set_facecolor(SURFACE)
v = [res[str(t)]["ratio"][0] for t in TS]
e = [res[str(t)]["ratio"][1] for t in TS]
cx.axhline(1.0, color=MUTED, lw=1, ls=(0, (4, 3)), zorder=2)
cx.axvspan(100, 11000, color=WASH, alpha=.18, lw=0, zorder=1)
cx.errorbar(TS, v, yerr=e, color=ACCENT, lw=2, marker="o", ms=7.5,
            mec=SURFACE, mew=1.8, capsize=3, zorder=3)
cx.set_xscale("log", base=2); cx.set_xlim(1.6, 11000)
cx.set_xticks([2, 16, 128, 1024, 8192])
cx.set_xticklabels(["2", "16", "128", "1024", "8192"])
cx.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
cx.set_xticks(TS, minor=True); cx.tick_params(axis="x", which="minor", length=0)
cx.set_ylim(0.96, 1.78)
cx.set_xlabel("difusão superficial,  $T_s$", fontsize=11.5, color=INK2)
cx.set_ylabel("$\\rho(3)\\,/\\,\\rho(R/2)$", fontsize=12, color=INK2)
cx.set_title("Quanto ainda resta de fractal", fontsize=12.5, color=INK, pad=12, loc="left")
cx.annotate("densidade uniforme\n(compacto)", (2.6, 1.0), textcoords="offset points",
            xytext=(0, 9), fontsize=9.5, color=MUTED)
cx.annotate("indistinguível de\ncompacto a partir\nde $T_s=128$", (900, 1.30),
            ha="center", fontsize=9.5, color=INK2)

for a in (ax, bx, cx):
    a.grid(True, color=GRID, lw=.8, zorder=0)
    a.set_axisbelow(True)
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        a.spines[s].set_color(GRID)
    a.tick_params(colors=MUTED, labelsize=10, length=0)

fig.text(0.006, 0.018,
         "25 fibrilas por condição, 11 seções por fibrila, nb=30000.  Barras de erro: erro padrão "
         "entre fibrilas.  Nenhuma grandeza aqui envolve ajuste de reta ou janela de escala.",
         fontsize=8.5, color=MUTED)
fig.subplots_adjust(left=0.052, right=0.988, top=0.90, bottom=0.165)
fig.savefig(OUT, dpi=175, facecolor=SURFACE)
print("wrote", OUT)

#!/usr/bin/env python3
"""Fractal dimension vs T_s, and the fit-window sensitivity behind it.

Panel (a) is the manuscript's Figure 3 recomputed from the quenched-campaign
fibrils under two window rules, against the published points.  Panel (b) is the
diagnostic that explains the disagreement: the local slope of the mass-radius
curve is not constant, so D_f is whatever the fit window says it is.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = "/petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign"
SRC = f"{ROOT}/analysis/df/df_windows.json"
OUT = f"{ROOT}/analysis/df/df_vs_ts.png"

SURFACE = "#fcfcfb"
INK, INK2, MUTED, GRID = "#10151c", "#3d4654", "#6d7787", "#e6e4e0"
C_PUB, C_ABS, C_REL = "#eb6834", "#2a78d6", "#1baf7a"
RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]

TS = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]
# Endpoints from the published caption; the intermediate points are read off
# the published figure, so they carry a transcription uncertainty of ~0.005.
PUB = {2: 1.708, 8: 1.731, 16: 1.735, 32: 1.739, 64: 1.761,
       128: 1.790, 512: 1.901, 1024: 1.934, 4096: 1.962, 8192: 1.965}
PUB_ERR = {2: 0.005, 8192: 0.001}

res = json.load(open(SRC))
rad = np.array(res["radii"])
lt = np.log10(TS)

fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.8, 5.0),
                             gridspec_kw=dict(width_ratios=[1.12, 1], wspace=0.24))
fig.patch.set_facecolor(SURFACE)

# ---------- (a) D_f vs log10 T_s ----------
ax.set_facecolor(SURFACE)
series = [
    ("publicado", C_PUB, [PUB[t] for t in TS], [PUB_ERR.get(t, 0.005) for t in TS], "s"),
    ("janela fixa  $4\\leq r\\leq 8$", C_ABS,
     [res[str(t)]["abs_4_8"][0] for t in TS], [res[str(t)]["abs_4_8"][1] for t in TS], "o"),
    ("janela relativa  $0{,}15R\\leq r\\leq 0{,}5R$", C_REL,
     [res[str(t)]["rel"][0] for t in TS], [res[str(t)]["rel"][1] for t in TS], "^"),
]
for label, color, v, e, mk in series:
    ax.errorbar(lt, v, yerr=e, color=color, lw=1.8, marker=mk, ms=7,
                mec=SURFACE, mew=1.4, capsize=3, elinewidth=1.4, zorder=3, label=label)

ax.annotate("publicado", (lt[6], PUB[512]), textcoords="offset points",
            xytext=(6, -20), fontsize=10.5, color=C_PUB, zorder=5)
ax.annotate("janela fixa", (lt[4], res["64"]["abs_4_8"][0]), textcoords="offset points",
            xytext=(-8, 11), ha="right", fontsize=10.5, color=C_ABS, zorder=5)
ax.annotate("janela relativa", (lt[3], res["32"]["rel"][0]), textcoords="offset points",
            xytext=(4, -22), fontsize=10.5, color=C_REL, zorder=5)

ax.set_xlabel("$\\log_{10} T_s$", fontsize=12, color=INK2)
ax.set_ylabel("$D_f$", fontsize=13, color=INK2)
ax.set_title("A dimensão fractal e a janela que a define",
             fontsize=12.5, color=INK, pad=12, loc="left")
ax.set_ylim(1.62, 2.01)
ax.legend(frameon=False, fontsize=9.5, loc="lower right", labelcolor=INK2)

# ---------- (b) local slope ----------
bx.set_facecolor(SURFACE)
SHOWN = [2, 16, 64, 512, 8192]

# The fixed window of panel (a), drawn where it actually samples the curves.
bx.axvspan(4, 8, color=C_ABS, alpha=.10, lw=0, zorder=1)
bx.annotate("janela fixa\n$4\\leq r\\leq 8$", (5.66, 0.30), ha="center",
            fontsize=9.5, color=C_ABS, zorder=5)

bx.axhspan(1.70, 1.72, color=C_PUB, alpha=.16, lw=0, zorder=1)
bx.axhline(2.0, color=MUTED, lw=1, ls=(0, (4, 3)), zorder=2)

for ts, color in zip(SHOWN, RAMP):
    m = np.array(res[str(ts)]["mean_curve"])
    ok = m > 0
    lr, lm = np.log10(rad[ok]), np.log10(m[ok])
    sl = np.gradient(lm, lr)
    k = 7
    sl = np.convolve(sl, np.ones(k) / k, mode="same")[k:-k]
    r = rad[ok][k:-k]
    bx.plot(r, sl, lw=2, color=color, zorder=3, solid_capstyle="round")
    # Label on the rollover, where curves separate.  512 and 8192 roll over at
    # the same radius -- they have the same R -- so they share one label.
    if ts != 512:
        text = "$T_s\\geq$512" if ts == 8192 else f"$T_s$={ts}"
        j = int(np.argmin(np.abs(sl - 1.0)))
        bx.annotate(text, (r[j], sl[j]), textcoords="offset points",
                    xytext=(-9, 0), ha="right", va="center", fontsize=9.5,
                    color=color, zorder=5)

# Reference labels on the right, clear of every curve.
bx.annotate("compacto,  $D_f=2$", (41, 2.0), fontsize=9.5, color=MUTED,
            ha="right", va="bottom", zorder=5)
bx.annotate("DLA 2D,  $D_f\\approx1{,}71$", (41, 1.71), fontsize=9.5,
            color="#b04a1f", ha="right", va="bottom", zorder=5)

bx.set_xscale("log")
bx.set_xlim(1.6, 46)
bx.set_ylim(0.0, 2.25)
bx.set_xticks([2, 5, 10, 20, 40])
bx.set_xticklabels(["2", "5", "10", "20", "40"])
bx.set_xlabel("raio  $r$  (sítios)", fontsize=11.5, color=INK2)
bx.set_ylabel("inclinação local  $d\\log N / d\\log r$", fontsize=11.5, color=INK2)
bx.set_title("Não há um $D_f$ único: a inclinação depende de $r$",
             fontsize=12.5, color=INK, pad=12, loc="left")

for a in (ax, bx):
    a.grid(True, color=GRID, lw=.8, zorder=0)
    a.set_axisbelow(True)
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        a.spines[s].set_color(GRID)
    a.tick_params(colors=MUTED, labelsize=10, length=0)

fig.text(0.008, 0.017,
         "25 fibrilas por condição, 11 seções por fibrila, nb=30000.  Barras de erro: "
         "erro padrão entre fibrilas.  Pontos publicados lidos da Figura 3 do manuscrito "
         "(extremos, da legenda: 1,708±0,005 e 1,963±0,001).",
         fontsize=8.5, color=MUTED)
fig.subplots_adjust(left=0.065, right=0.985, top=0.90, bottom=0.16)
fig.savefig(OUT, dpi=175, facecolor=SURFACE)
print("wrote", OUT)

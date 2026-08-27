#!/usr/bin/env python3
"""Figure: is the Araujo et al. (2003) ansatz an adequate model for the cascades?"""
import csv, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import sparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avalanche_statistics import (fit_cutoff_power_law, fit_discrete_lognormal,
                                  fit_discrete_power_law, fit_generalized_cutoff,
                                  distribution_cdf)

ROOT = "/petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign"
CASC = f"{ROOT}/analysis/cascades"
OUT = f"{CASC}/araujo_adequacy.png"

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#10151c", "#3d4654", "#6d7787", "#e6e4e0"
C_ARA, C_EXP, C_LOG, C_POW = "#eb6834", "#2a78d6", "#1baf7a", "#6d7787"
RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]
TS = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]
MS = [1, 2, 3, 5, 10]

rows = {(int(r["ts"]), int(r["m"])): r
        for r in csv.DictReader(open(f"{CASC}/araujo_fits.csv"))}

fig, axes = plt.subplots(2, 2, figsize=(12.6, 9.0))
(ax, bx), (cx, dx) = axes
fig.patch.set_facecolor(SURFACE)

def style(a):
    a.set_facecolor(SURFACE)
    a.grid(True, color=GRID, lw=.8, zorder=0); a.set_axisbelow(True)
    for s in ("top", "right"): a.spines[s].set_visible(False)
    for s in ("left", "bottom"): a.spines[s].set_color(GRID)
    a.tick_params(colors=MUTED, labelsize=9.5, length=0)

def log_ticks(a):
    a.set_xscale("log", base=2); a.set_xlim(1.6, 30000)
    a.set_xticks([2, 16, 128, 1024, 8192]); a.set_xticklabels(["2","16","128","1024","8192"])
    a.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    a.set_xticks(TS, minor=True); a.tick_params(axis="x", which="minor", length=0)

# ---------- (a) compensated survival: flat = the model is right -------------
SHOW = (128, 10)
r = rows[SHOW]
xmin = int(r["xmin"])
counts = np.asarray(sparse.load_npz(f"{CASC}/casc_ts{SHOW[0]}_m{SHOW[1]}_pre.npz")
                    .sum(axis=0)).ravel()
sizes = np.arange(len(counts)); tail = sizes >= xmin
emp = 1.0 - np.cumsum(counts[tail]) / counts[tail].sum()
obs = sizes[tail]; keep = emp > 5e-7
fits = [("Araújo", fit_generalized_cutoff(counts, xmin=xmin), C_ARA),
        ("corte exponencial", fit_cutoff_power_law(counts, xmin=xmin), C_EXP),
        ("log-normal", fit_discrete_lognormal(counts, xmin=xmin), C_LOG),
        ("lei de potência", fit_discrete_power_law(counts, xmin=xmin), C_POW)]
for label, fit, color in fits:
    model = 1.0 - distribution_cdf(fit, obs[keep])
    ax.plot(obs[keep], np.where(model > 0, emp[keep] / np.maximum(model, 1e-300), np.nan),
            lw=2, color=color, label=label, zorder=3, solid_capstyle="round")
ax.axhline(1.0, color=INK2, lw=1.2, ls=(0, (4, 3)), zorder=4)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_ylim(0.2, 60)
ax.set_yticks([0.3, 1, 3, 10, 30]); ax.set_yticklabels(["0,3","1","3","10","30"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlabel("tamanho da cascata,  $s$", fontsize=11, color=INK2)
ax.set_ylabel("dados / modelo   (sobrevivência)", fontsize=11, color=INK2)
ax.set_title(f"(a)  $T_s$={SHOW[0]}, $m$={SHOW[1]}: razão com cada modelo",
             fontsize=12, color=INK, pad=10, loc="left")
ax.legend(frameon=False, fontsize=9, loc="upper left", labelcolor=INK2, ncols=2)
ax.annotate("1 = modelo exato", (obs[keep].max(), 1.0), textcoords="offset points",
            xytext=(-4, 6), ha="right", fontsize=9, color=INK2)
ax.annotate("acima: o modelo\nsubestima a cauda", (0.985, 0.965), xycoords="axes fraction",
            ha="right", va="top", fontsize=9, color=MUTED)

# ---------- (b) KS of every family, all 50 conditions ----------------------
series = [("Araújo", "ks_araujo", C_ARA, "o"),
          ("corte exponencial", "ks_exponential", C_EXP, "s"),
          ("log-normal", "ks_lognormal", C_LOG, "^")]
for label, key, color, mk in series:
    for m, alpha in zip(MS, (0.35, 0.5, 0.65, 0.8, 1.0)):
        v = [float(rows[(t, m)][key]) for t in TS]
        bx.plot(TS, v, lw=0, marker=mk, ms=5.5, color=color, alpha=alpha,
                mec="none", zorder=3, label=label if m == 10 else None)
bx.set_yscale("log"); log_ticks(bx)
bx.set_xlabel("difusão superficial,  $T_s$", fontsize=11, color=INK2)
bx.set_ylabel("distância KS  (menor é melhor)", fontsize=11, color=INK2)
bx.set_title("(b)  Adequação: Araújo tem o menor KS em 34 de 50",
             fontsize=12, color=INK, pad=10, loc="left")
bx.legend(frameon=False, fontsize=9, loc="lower left", labelcolor=INK2)
bx.annotate("cada modelo aparece 5×,\num por valor de $m$", (0.97, 0.93),
            xycoords="axes fraction", ha="right", va="top", fontsize=9, color=MUTED)

# ---------- (c) gamma ------------------------------------------------------
for m, color in zip(MS, RAMP):
    v = [float(rows[(t, m)]["gamma"]) for t in TS]
    e = [float(rows[(t, m)]["se_gamma"]) for t in TS]
    cx.errorbar(TS, v, yerr=e, lw=2, marker="o", ms=5.5, color=color,
                mec=SURFACE, mew=1.2, capsize=2, zorder=3)
    cx.annotate(f"$m$={m}", (TS[-1], v[-1]), textcoords="offset points",
                xytext=(7, 0), va="center", fontsize=9, color=color, zorder=5)
cx.axhline(2.5, color=MUTED, lw=1, ls=(0, (4, 3)), zorder=2)
cx.annotate("5/2", (2.2, 2.5), textcoords="offset points", xytext=(0, 5),
            fontsize=9, color=MUTED)
log_ticks(cx)
cx.set_xlabel("difusão superficial,  $T_s$", fontsize=11, color=INK2)
cx.set_ylabel("$\\gamma$", fontsize=12, color=INK2)
cx.set_title("(c)  Expoente do ansatz de Araújo", fontsize=12, color=INK, pad=10, loc="left")

# ---------- (d) eta --------------------------------------------------------
for m, color in zip(MS, RAMP):
    v = [float(rows[(t, m)]["eta"]) for t in TS]
    e = [float(rows[(t, m)]["se_eta"]) for t in TS]
    dx.errorbar(TS, v, yerr=e, lw=2, marker="o", ms=5.5, color=color,
                mec=SURFACE, mew=1.2, capsize=2, zorder=3)
    # m = 2/10 and m = 3/5 end within 0.1 of each other; nudge them apart.
    dy = {2: 9, 10: -9, 3: 7, 5: -7}.get(m, 0)
    dx.annotate(f"$m$={m}", (TS[-1], v[-1]), textcoords="offset points",
                xytext=(7, dy), va="center", fontsize=9, color=color, zorder=5)
dx.axhline(1.0, color=C_EXP, lw=1.4, ls=(0, (4, 3)), zorder=2)
dx.annotate("$\\eta$=1: corte exponencial", (2.2, 1.0), textcoords="offset points",
            xytext=(0, 6), fontsize=9, color=C_EXP)
dx.axhspan(1.5, 2.0, color=C_ARA, alpha=.14, lw=0, zorder=1)
# The band sits under every curve, so its label goes to the empty top-left
# corner with a swatch rather than on top of the data.
dx.plot([2.6], [5.95], marker="s", ms=8, color=C_ARA, alpha=.45, mec="none", zorder=5)
dx.annotate("faixa de Araújo para percolação  ($\\eta$ = 1,5 a 2,0)", (3.2, 5.95),
            ha="left", va="center", fontsize=9, color="#b04a1f", zorder=5)
log_ticks(dx)
dx.set_ylim(0.7, 6.3)
dx.set_xlabel("difusão superficial,  $T_s$", fontsize=11, color=INK2)
dx.set_ylabel("$\\eta$  (nitidez do corte)", fontsize=12, color=INK2)
dx.set_title("(d)  O corte é mais abrupto que exponencial em 50 de 50",
             fontsize=12, color=INK, pad=10, loc="left")

for a in (ax, bx, cx, dx):
    style(a)

fig.text(0.006, 0.012,
         "$p(s) \\propto s^{-\\gamma}\\exp[-(s/s_c)^{\\eta}]$, o ansatz de Araújo et al. (2003) como função de massa.  "
         "61 000 717 cascatas preterminais.  Barras: bootstrap de blocos por fibrila, 120 réplicas.",
         fontsize=8.5, color=MUTED)
fig.subplots_adjust(left=0.075, right=0.975, top=0.955, bottom=0.075, hspace=0.30, wspace=0.24)
fig.savefig(OUT, dpi=170, facecolor=SURFACE)
print("wrote", OUT)

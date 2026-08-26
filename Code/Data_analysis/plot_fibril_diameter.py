#!/usr/bin/env python3
"""Figure: cross-sectional diameter along the fibril axis, by T_s."""
import csv, collections, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = "/petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign"
CSV = f"{ROOT}/analysis/diameter/profile.csv"
OUT = f"{ROOT}/analysis/diameter/diameter_profile.png"

SURFACE = "#fcfcfb"
INK, INK2, MUTED = "#1a1a19", "#43423e", "#83827d"
GRID = "#e6e4e0"
# Ordinal ramp, single hue, validated (adjacent dL >= 0.06, light end 2.06:1).
RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]
SHOWN = [2, 16, 64, 512, 8192]
MIN_FIB = 20            # layers supported by fewer fibrils are tip noise

data = collections.defaultdict(dict)
for r in csv.DictReader(open(CSV)):
    data[int(r["ts"])][int(r["y"])] = (int(r["n_fibrils"]), float(r["mean_count"]),
                                       float(r["mean_d_gyr"]), float(r["mean_d_max"]))

def profile(ts, col=2):
    rows = data[ts]
    ys = sorted(y for y, v in rows.items() if v[0] >= MIN_FIB)
    return np.array(ys), np.array([rows[y][col] for y in ys])

fig, (ax, bx) = plt.subplots(
    1, 2, figsize=(12.4, 4.9), gridspec_kw=dict(width_ratios=[1.65, 1], wspace=0.26))
fig.patch.set_facecolor(SURFACE)

# ---- (a) profiles -------------------------------------------------------
ax.set_facecolor(SURFACE)
# T_s = 512 and 8192 lie on top of each other -- that IS the result -- so they
# get ONE shared label instead of two colliding ones.
LABELS = {2: "$T_s$=2", 16: "$T_s$=16", 64: "$T_s$=64", 8192: "$T_s\\geq$512"}
for ts, color in zip(SHOWN, RAMP):
    ys, d = profile(ts)
    k = 25                                    # light smoothing; layers are 1 site
    if len(d) > k:
        d = np.convolve(d, np.ones(k) / k, mode="same")
        ys, d = ys[k:-k], d[k:-k]
    ax.plot(ys, d, lw=2, color=color, solid_capstyle="round", zorder=3)
    if ts in LABELS:
        j = np.argmax(d)
        ax.annotate(LABELS[ts], (ys[j], d[j]), textcoords="offset points",
                    xytext=(0, 7), ha="center", fontsize=9.5, color=color,
                    zorder=4)
ax.set_ylim(3, 40)

ax.set_xlabel("posição ao longo do eixo,  $y$  (sítios)", fontsize=10.5, color=INK2)
ax.set_ylabel("diâmetro de giração,  $d_{gyr}$  (sítios)", fontsize=10.5, color=INK2)
ax.set_title("Perfil de diâmetro ao longo da fibrila",
             fontsize=12, color=INK, pad=12, loc="left")

# ---- (b) saturation -----------------------------------------------------
bx.set_facecolor(SURFACE)
allts = sorted(data)
core = []
for ts in allts:
    rows = data[ts]
    vals = [v[2] for y, v in rows.items() if v[0] >= MIN_FIB and abs(y) <= 100]
    core.append(np.mean(vals))
bx.plot(allts, core, lw=2, color=RAMP[3], zorder=3, solid_capstyle="round")
bx.plot(allts, core, "o", ms=8, color=RAMP[3], mec=SURFACE, mew=2, zorder=4)
bx.set_xscale("log", base=2)
bx.set_xlim(1.6, 11000)
# Ten ticks collide at the right end of a log axis; label a readable subset and
# let the markers carry the rest.
bx.set_xticks([2, 16, 128, 1024, 8192])
bx.set_xticklabels(["2", "16", "128", "1024", "8192"], fontsize=9.5)
bx.set_xticks(allts, minor=True)
bx.tick_params(axis="x", which="minor", length=0)
# A log axis auto-labels its minor ticks as powers of the base (2^9, 2^12...),
# which is exactly the crowding the subset above was meant to avoid.
bx.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

bx.axvspan(430, 11000, color=RAMP[0], alpha=0.16, lw=0, zorder=1)
plateau = np.mean([c for t, c in zip(allts, core) if t >= 512])
spread = (max(c for t, c in zip(allts, core) if t >= 512)
          - min(c for t, c in zip(allts, core) if t >= 512)) / plateau
bx.annotate(f"platô  $d_{{gyr}}\\approx${plateau:.1f}\n(variação {spread*100:.1f}%)",
            (1500, plateau), textcoords="offset points", xytext=(0, 44),
            ha="center", fontsize=9.5, color=INK2, zorder=5)
bx.annotate(f"{core[0]:.1f}", (allts[0], core[0]), textcoords="offset points",
            xytext=(11, -1), fontsize=9.5, color=INK2)
bx.set_ylim(14.5, 37)

bx.set_xlabel("difusão superficial,  $T_s$", fontsize=10.5, color=INK2)
bx.set_ylabel("$d_{gyr}$ no miolo ($|y|\\leq100$)", fontsize=10.5, color=INK2)
bx.set_title("O diâmetro satura em $T_s\\approx512$",
             fontsize=12, color=INK, pad=12, loc="left")

for a in (ax, bx):
    a.grid(True, color=GRID, lw=0.8, zorder=0)
    a.set_axisbelow(True)
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        a.spines[s].set_color(GRID)
    a.tick_params(colors=MUTED, labelsize=9.5, length=0)

fig.text(0.008, 0.018,
         "25 fibrilas por condição, nb=30000.  $d_{gyr}=2\\sqrt{\\langle|r-r_c|^2\\rangle}$ "
         "por seção transversal em $y$; camadas com <20 fibrilas (pontas) omitidas.",
         fontsize=8.5, color=MUTED)
fig.subplots_adjust(left=0.075, right=0.985, top=0.90, bottom=0.19, wspace=0.28)
fig.savefig(OUT, dpi=170, facecolor=SURFACE)
print("wrote", OUT)
for ts, c in zip(allts, core):
    print(f"  ts={ts:>5}  d_gyr_miolo={c:.2f}")

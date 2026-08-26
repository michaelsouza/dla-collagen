#!/usr/bin/env python3
"""Projected central segments in the x-z plane, coloured by attachment order.

Reproduces Figure 2 of the manuscript from the quenched-campaign fibrils.  Each
occupied (x, z) column of a thin central slab is painted with the uid of the
FIRST molecule to occupy it, so the colour reads as "when this column was
built" -- early attachments near the seed, late ones at the tips.

Unlike the published figure, every panel shares one spatial scale, so the
compaction with T_s is visible as size and not only as texture.
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from fibril_diameter_profile import read_compact

ROOT = "/petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign"
COMPACT = f"{ROOT}/fibrils/compact"
OUT = f"{ROOT}/analysis/diameter/central_sections.png"

TS = (2, 64, 512, 8192)
HALF = 25                    # slab |y| <= HALF; thicker slabs wash out the arms
NB = 30000
SURFACE = "#fcfcfb"
INK, INK2, MUTED = "#10151c", "#3d4654", "#6d7787"


def slab_map(ts, half=HALF):
    name = next(f for f in sorted(os.listdir(COMPACT))
                if f.startswith(f"dla_mode_s_ts_{ts}_nb_"))
    x, yb, z = read_compact(os.path.join(COMPACT, name))
    uid = np.arange(x.size)
    keep = np.abs(yb) <= half
    return x[keep], z[keep], uid[keep], name


panels = [slab_map(ts) for ts in TS]
half_span = max(max(np.abs(p[0]).max(), np.abs(p[1]).max()) for p in panels) + 2

fig, axes = plt.subplots(1, 4, figsize=(13.2, 4.75))
fig.patch.set_facecolor(SURFACE)
norm = Normalize(0, NB)
cmap = plt.get_cmap("turbo")

for ax, ts, (x, z, uid, name) in zip(axes, TS, panels):
    n = int(2 * half_span + 1)
    grid = np.full((n, n), np.nan)
    ix = (x + half_span).astype(int)
    iz = (z + half_span).astype(int)
    # First occupant wins: walk in reverse uid order so the smallest lands last.
    order = np.argsort(-uid)
    grid[iz[order], ix[order]] = uid[order]

    ax.imshow(np.ma.masked_invalid(grid), cmap=cmap, norm=norm, origin="lower",
              interpolation="nearest")
    ax.set_facecolor(SURFACE)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#d7dde6"); s.set_linewidth(0.8)
    occ = np.isfinite(grid).sum()
    bx = x.max() - x.min() + 1; bz = z.max() - z.min() + 1
    ax.set_xlabel(f"$T_s$ = {ts}", fontsize=13, color=INK, labelpad=10)
    ax.set_title(f"{occ} sítios · preenchimento {occ / (bx * bz):.2f}",
                 fontsize=10, color=MUTED, pad=8)

# escala comum: barra de 20 sítios no primeiro painel
ax0 = axes[0]
ax0.plot([3, 23], [4, 4], lw=3, color=INK, solid_capstyle="butt")
ax0.text(13, 7, "20 sítios", ha="center", fontsize=9.5, color=INK)

cax = fig.add_axes([0.30, 0.115, 0.40, 0.024])
cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax,
                  orientation="horizontal")
cb.set_label("ordem de incorporação da molécula  (0 = semente, 30000 = última)",
             fontsize=10, color=INK2, labelpad=7)
cb.outline.set_visible(False)
cb.ax.tick_params(colors=MUTED, labelsize=9, length=0)

fig.subplots_adjust(left=0.02, right=0.98, top=0.91, bottom=0.26, wspace=0.06)
fig.savefig(OUT, dpi=175, facecolor=SURFACE)
print("wrote", OUT)
for ts, (x, z, uid, name) in zip(TS, panels):
    print(f"  ts={ts:>5}  {name}  moleculas={x.size}")

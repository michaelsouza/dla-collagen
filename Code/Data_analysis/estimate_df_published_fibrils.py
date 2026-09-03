#!/usr/bin/env python3
"""D_f das fibrilas publicadas sob regras de janela uniformes, para a Fig. 3 nova.

Lê:      Data_fibrils/fibrilas_publicadas_artigo_10Ts_nb30000.zip
Escreve: Reviews/N7_fractal_proxy/df_published_fibrils_by_window.csv
         Reviews/N7_fractal_proxy/df_published_mass_radius_curves.csv
Chamado: à mão, para N7 (Estado_revisao_ER12738.md); a Fig. 3 do manuscrito
         revisado é desenhada a partir destes CSVs

Por que existe: o relatório da campanha (§4) mostrou, sobre as fibrilas da
campanha, que o D_f publicado depende da janela de ajuste. A Fig. 3 do
manuscrito foi feita com as fibrilas *publicadas*; este script mede as mesmas
fibrilas sob as mesmas regras uniformes do relatório, para que a figura nova
seja comparável ponto a ponto com a antiga.

Regras de janela (raio em unidades de rede):
  manuscript  -- 5 <= r <= R_max do ensemble, sobre a curva média das 11xN
                 seções (a regra do manuscrito, reproduzida sobre os mesmos dados)
  abs_4_8     -- 4 <= r <= 8, janela fixa curta (miolo)
  abs_2_16    -- 2 <= r <= 16, janela fixa longa
  rel         -- 0,15 R <= r <= 0,50 R, com R o raio médio da fibrila

Dois níveis de estimativa para cada regra:
  ensemble -- ajuste sobre a curva média de todas as seções do T_s (como o
              manuscrito); incerteza = erro-padrão da reta
  fibril   -- ajuste por fibrila (11 seções), média ± erro-padrão entre fibrilas
"""
from __future__ import annotations

import csv
import io
import re
import sys
import zipfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "Code" / "Data_analysis"))
from validate_fractal_proxy import (  # noqa: E402
    iter_compact_rows,
    section_index_for_rod,
    SECTION_Y,
)

ZIP = ROOT / "Data_fibrils" / "fibrilas_publicadas_artigo_10Ts_nb30000.zip"
OUT_DIR = ROOT / "Reviews" / "N7_fractal_proxy"
OUT_FITS = OUT_DIR / "df_published_fibrils_by_window.csv"
OUT_CURVES = OUT_DIR / "df_published_mass_radius_curves.csv"

NAME = re.compile(r"dla_mode_s_ts_(\d+)_nb_30000_seed_(\d+)_\.dat$")
RADII = np.arange(1, 65, dtype=float)  # inteiros, como no manuscrito


def sections_from_handle(handle) -> list[np.ndarray]:
    """As 11 seções amostradas de uma fibrila compacta, como parse_grown_sections."""
    sections: list[list[tuple[int, int]]] = [[] for _ in SECTION_Y]
    for _rid, x, y0, z in iter_compact_rows(handle, "zip"):
        idx = section_index_for_rod(y0)
        if idx is not None:
            sections[idx].append((x, z))
    empty = [int(y) for y, s in zip(SECTION_Y, sections) if not s]
    if empty:
        raise ValueError(f"seções vazias em y={empty}")
    return [np.asarray(s, dtype=float) for s in sections]


def mass_curves(sections: list[np.ndarray]) -> tuple[np.ndarray, float]:
    """Massa média m(r) sobre as seções e o raio máximo médio."""
    masses, rmax = [], []
    for xy in sections:
        d = np.sqrt(((xy - xy.mean(axis=0)) ** 2).sum(axis=1))
        d.sort()
        masses.append(np.searchsorted(d, RADII, side="right").astype(float))
        rmax.append(float(d[-1]))
    return np.vstack(masses), float(np.mean(rmax))


def fit_slope(mean_mass: np.ndarray, lo: float, hi: float) -> tuple[float, float, int]:
    """Inclinação log-log e seu erro-padrão sobre lo <= r <= hi."""
    w = (RADII >= lo) & (RADII <= hi) & (mean_mass > 0)
    n = int(w.sum())
    if n < 3:
        return float("nan"), float("nan"), n
    x, y = np.log10(RADII[w]), np.log10(mean_mass[w])
    coef, cov = np.polyfit(x, y, 1, cov=True)
    return float(coef[0]), float(np.sqrt(cov[0, 0])), n


def main() -> int:
    per_ts: dict[int, list[tuple[int, np.ndarray, float]]] = {}
    with zipfile.ZipFile(ZIP) as zf:
        for info in zf.infolist():
            m = NAME.search(info.filename)
            if not m:
                continue
            ts, seed = int(m.group(1)), int(m.group(2))
            with io.TextIOWrapper(zf.open(info), encoding="utf-8") as handle:
                sections = sections_from_handle(handle)
            masses, r_fib = mass_curves(sections)
            per_ts.setdefault(ts, []).append((seed, masses, r_fib))

    fits_rows, curve_rows = [], []
    for ts in sorted(per_ts):
        fibrils = per_ts[ts]
        all_masses = np.vstack([mm for _s, mm, _r in fibrils])
        ens_mean = all_masses.mean(axis=0)
        r_max_ens = max(r for _s, _mm, r in fibrils)
        r_mean_ens = float(np.mean([r for _s, _mm, r in fibrils]))
        n_sec = all_masses.shape[0]

        for r, mval in zip(RADII, ens_mean):
            curve_rows.append(dict(ts=ts, r=int(r), mean_mass=f"{mval:.4f}",
                                   n_sections=n_sec))

        rules = {
            "manuscript": (5.0, np.floor(r_max_ens)),
            "abs_4_8": (4.0, 8.0),
            "abs_2_16": (2.0, 16.0),
            "rel": (0.15 * r_mean_ens, 0.50 * r_mean_ens),
        }
        for rule, (lo, hi) in rules.items():
            slope, se, npts = fit_slope(ens_mean, lo, hi)
            fits_rows.append(dict(ts=ts, rule=rule, level="ensemble",
                                  r_lo=f"{lo:.2f}", r_hi=f"{hi:.2f}", n_points=npts,
                                  n_fibrils=len(fibrils), n_sections=n_sec,
                                  df=f"{slope:.4f}", df_err=f"{se:.4f}",
                                  decades=f"{np.log10(hi / lo):.2f}"))
            # por fibrila: a regra relativa usa o raio da própria fibrila
            vals = []
            for _seed, mm, r_fib in fibrils:
                lo_f, hi_f = ((0.15 * r_fib, 0.50 * r_fib) if rule == "rel"
                              else (lo, hi))
                s, _e, _n = fit_slope(mm.mean(axis=0), lo_f, hi_f)
                if np.isfinite(s):
                    vals.append(s)
            v = np.asarray(vals)
            fits_rows.append(dict(ts=ts, rule=rule, level="fibril",
                                  r_lo=f"{lo:.2f}", r_hi=f"{hi:.2f}", n_points="",
                                  n_fibrils=len(v), n_sections=n_sec,
                                  df=f"{v.mean():.4f}",
                                  df_err=f"{v.std(ddof=1) / np.sqrt(len(v)):.4f}",
                                  decades=f"{np.log10(hi / lo):.2f}"))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_FITS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fits_rows[0]))
        w.writeheader()
        w.writerows(fits_rows)
    with OUT_CURVES.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(curve_rows[0]))
        w.writeheader()
        w.writerows(curve_rows)

    print(f"{'Ts':>5} {'fibr':>4} {'R_ens':>6} {'manuscript':>18} {'abs[4,8]':>18} "
          f"{'abs[2,16]':>18} {'rel':>18}")
    for ts in sorted(per_ts):
        ens = {r["rule"]: r for r in fits_rows if r["ts"] == ts and r["level"] == "ensemble"}
        r_ens = max(r for _s, _mm, r in per_ts[ts])
        cells = "".join(f"{float(ens[k]['df']):>11.3f}±{float(ens[k]['df_err']):<6.3f}"
                        for k in ("manuscript", "abs_4_8", "abs_2_16", "rel"))
        print(f"{ts:>5} {len(per_ts[ts]):>4} {r_ens:>6.1f} {cells}")
    print(f"\nescrito: {OUT_FITS.relative_to(ROOT)}\n         {OUT_CURVES.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

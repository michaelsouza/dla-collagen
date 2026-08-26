"""D_f per condition under three fit-window rules, with SE across fibrils."""
import os, sys, json, numpy as np
from pathlib import Path
sys.path.insert(0, "Code/Data_analysis")
from validate_fractal_proxy import parse_grown_sections, mass_radius_for_sections

D = "/petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign/fibrils/compact"
OUT = "/petrobr/parceirosbr/solverbrict/michael.souza/dla-collagen/campaign/analysis/df"
TS = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]
NFIB = int(sys.argv[1]) if len(sys.argv) > 1 else 25
RAD = np.power(10.0, np.linspace(np.log10(1.0), np.log10(64.0), 96))

def fit(m, lo, hi):
    w = (RAD >= lo) & (RAD <= hi) & (m > 0)
    if w.sum() < 4:
        return np.nan
    return float(np.polyfit(np.log10(RAD[w]), np.log10(m[w]), 1)[0])

os.makedirs(OUT, exist_ok=True)
res = {}
for ts in TS:
    fs = [f for f in sorted(os.listdir(D)) if f.startswith(f"dla_mode_s_ts_{ts}_nb_")][:NFIB]
    rows = []
    for f in fs:
        sec = parse_grown_sections(Path(os.path.join(D, f)))
        m, desc = mass_radius_for_sections(sec, RAD)
        R = desc["full_mean_radius_11"]
        rows.append(dict(R=R,
                         abs_4_8=fit(m, 4, 8),
                         abs_2_16=fit(m, 2, 16),
                         rel=fit(m, 0.15 * R, 0.50 * R),
                         curve=m.tolist()))
    a = {k: np.array([r[k] for r in rows]) for k in ("R", "abs_4_8", "abs_2_16", "rel")}
    n = len(rows)
    res[ts] = {k: [float(v.mean()), float(v.std(ddof=1) / np.sqrt(n))] for k, v in a.items()}
    res[ts]["n"] = n
    res[ts]["mean_curve"] = np.mean([r["curve"] for r in rows], axis=0).tolist()
res["radii"] = RAD.tolist()
json.dump(res, open(f"{OUT}/df_windows.json", "w"))

pub = {2:1.708, 8:1.731, 16:1.735, 32:1.739, 64:1.761,
       128:1.790, 512:1.901, 1024:1.934, 4096:1.962, 8192:1.965}
print(f"{'Ts':>5} {'R':>6} {'abs[4,8]':>16} {'abs[2,16]':>16} {'rel[.15R,.5R]':>16} {'publicado':>10}")
for ts in TS:
    r = res[ts]
    print(f"{ts:>5} {r['R'][0]:>6.1f} "
          f"{r['abs_4_8'][0]:>9.3f}±{r['abs_4_8'][1]:<6.3f}"
          f"{r['abs_2_16'][0]:>9.3f}±{r['abs_2_16'][1]:<6.3f}"
          f"{r['rel'][0]:>9.3f}±{r['rel'][1]:<6.3f}"
          f"{pub[ts]:>10.3f}")

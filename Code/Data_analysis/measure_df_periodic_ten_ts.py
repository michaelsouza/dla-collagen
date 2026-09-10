#!/usr/bin/env python3
"""D_f dos cilindros periodicos nos dez T_s: raio de giracao e massa-raio, por semente.

Lê:      <cylinders>/dla_per216_mode_s_ts_<TS>_nb_60000_seed_<SEED>_.dat
         (sementes descobertas por glob; exige >= 5 por T_s; 125 desde 2026-09-10)
         Reviews/PhaseC_periodic_cylinder/df_wide_cylinders.csv        (conferencia)
         Reviews/PhaseC_periodic_cylinder/df_gyration_wide_cylinders.csv (conferencia)
Escreve: Reviews/N18_df_ten_ts/df_periodic_by_seed.csv
         Reviews/N18_df_ten_ts/df_periodic_summary.csv
         Reviews/N18_df_ten_ts/df_periodic_local_slopes.csv
         Reviews/N18_df_ten_ts/curves_corr_by_ts.csv
         Reviews/N18_df_ten_ts/identity_check_15_cylinders.csv
         Reviews/N18_df_ten_ts/xmgrace/df_by_ts_xydy.dat
Chamado: à mão, depois de Code/Data_analysis/run_periodic_cylinder_grid.sh

Secao transversal: a do artigo (paper_PRE.tex:141) e de measure_df_periodic.py.
Na camada L entram as moleculas cujo bastao cruza o plano y = L, um ponto (x, z)
por molecula; camadas L = 0, 18, ..., 198 no anel de periodo 216 (12 secoes);
cada molecula cai em exatamente uma secao. Media sobre secoes e, depois, sobre
as sementes do T_s (5; 15 em T_s = 2, 8, 4096, 8192; 40 em T_s = 16, desde 2026-09-10);
o erro e o erro-padrao entre sementes (n_seeds no summary).

Raio de giracao (regra principal): uid e a ordem de adesao; R_g(N) dos N
primeiros pontos da secao; N ~ R_g^{D_f}; ajuste de log10 N contra log10 R_g
em 40 <= N <= N_max/2, com N_max a media de moleculas por secao da semente.
Peso do ajuste (corrigido em 2026-09-10, segunda rodada): a reta e ajustada
sobre PONTOS_POR_OITAVA valores de N igualmente espacados em log N, nao sobre
todos os N inteiros -- com todos os inteiros, 90% do peso caia na decada de
cima e o "principal" media a periferia (diferenca ate 0,07 em T_s = 128).
Janelas de sensibilidade: 40-320, 320-5000, 40-5000, com o mesmo peso; as
versoes com todos os inteiros (*_allpts) so servem a conferencia contra
2026-09-09. Inclinacao local por oitava: sobre a curva media da semente
(slope_mean) e por secao (12 x n_seeds por T_s; slope_section_*).

Dimensao de correlacao (geometria da secao final, sem centro nem ordem):
C(r) = fracao dos pares de pontos da secao a distancia <= r, em grade de
RAIOS_CORR (log-uniforme, 20 por decada, 2 <= r <= 256); D_2 = inclinacao
de log C contra log r. Janelas: corr_primary 4 <= r <= R_bar/3 (~1 decada),
corr_4_32 fixa; inclinacao local por meia decada, por secao.
Controle de borda: C(r) de um disco uniforme com o mesmo numero de pontos e o
mesmo R_bar da secao (12 por cilindro, semente = seed) da inclinacao < 2 so
por efeito de tamanho finito; corr_*_disc e o valor no controle e
corr_*_corrected = medido - controle + 2.

Massa-raio: m(R) = pontos a distancia <= R do centro de massa da secao, R
inteiro de 1 a 200, media sobre secoes; janelas fixa 4-8, relativa
0,15 R <= r <= 0,5 R (R = media das distancias maximas por secao), faixa cheia
5 <= r <= R_max; inclinacao local por faixa de r.

Conferencia dura: os 15 cilindros de 2026-09-01 (T_s = 2, 128, 8192, sementes
SEEDS_REF) devem
reproduzir fixa_4_8 e relativa_0p15R_0p5R de df_wide_cylinders.csv e as tres
janelas de df_gyration_wide_cylinders.csv a 1e-3, senao nada e escrito. A
logica de conferencia repete a de export_periodic_cylinder_*_xmgrace.py, que
nao esta versionado.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import re
import sys
from multiprocessing import Pool

import numpy as np
from scipy.spatial import cKDTree

RAIZ = pathlib.Path(__file__).resolve().parents[2]
FASE_C = RAIZ / "Reviews" / "PhaseC_periodic_cylinder"
OUT = RAIZ / "Reviews" / "N18_df_ten_ts"
sys.path.insert(0, str(FASE_C))
from measure_df_periodic import carregar  # noqa: E402

NOME = re.compile(r"dla_per(\d+)_mode_s_ts_(\d+)_nb_(\d+)_seed_(\d+)_\.dat$")
TS = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]
SEEDS_REF = [900001, 900002, 900003, 900004, 900005]   # sementes de 2026-09-01 (conferencia)
MIN_SEEDS = 5
H = 18
RAIOS = np.arange(1.0, 200.0)
PONTOS_POR_OITAVA = 30
RAIOS_CORR = np.logspace(np.log10(2.0), np.log10(256.0), 43)   # 20 por decada
MEIAS_DECADAS = [2, 4, 8, 16, 32, 64, 128, 256]
JANELAS_N = {"gyr_N40_320": (40, 320), "gyr_N320_5000": (320, 5000), "gyr_N40_5000": (40, 5000)}
OITAVAS = [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5000]
FAIXAS_R = [5, 8, 12, 18, 27, 40, 60, 90, 135]


def secoes_em_ordem(caminho: pathlib.Path, periodo: int) -> list[np.ndarray]:
    """Pontos (x, z) de cada secao, na ordem de adesao (uid crescente)."""
    mols = carregar(str(caminho))                       # (x, y, z) na ordem do arquivo
    uids = []
    with open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            p = linha.split()
            if len(p) >= 5 and p[0].startswith("uid"):
                uids.append(int(p[1]))
    assert len(uids) == len(mols) and all(b > a for a, b in zip(uids, uids[1:])), \
        "uid nao cresce estritamente na ordem do arquivo"
    xyz = np.asarray(mols, dtype=np.int64)
    out = []
    for L in range(0, periodo, H):
        pertence = (L - xyz[:, 1]) % periodo < H
        out.append(xyz[pertence][:, [0, 2]].astype(float))
    return out


def inclinacao(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> float:
    if w.sum() < 3:
        return float("nan")
    return float(np.polyfit(np.log10(x[w]), np.log10(y[w]), 1)[0])


def inclinacao_log_uniforme(x: np.ndarray, y: np.ndarray, ok: np.ndarray,
                            lo: float, hi: float) -> float:
    """Reta de log10 y contra log10 x com pontos igualmente espacados em log x.

    x e a grade inteira de N (indice = N - 1). Escolhe PONTOS_POR_OITAVA valores
    de N por oitava entre lo e hi, sem repeticao, e ajusta so sobre eles.
    """
    if hi <= lo:
        return float("nan")
    n_pts = max(3, int(round(PONTOS_POR_OITAVA * np.log2(hi / lo))))
    grade = np.unique(np.rint(np.logspace(np.log10(lo), np.log10(hi), n_pts)).astype(int))
    grade = grade[(grade >= 1) & (grade <= len(x))]
    idx = grade - 1
    idx = idx[ok[idx]]
    if len(idx) < 3:
        return float("nan")
    return float(np.polyfit(np.log10(x[idx]), np.log10(y[idx]), 1)[0])


def disco_uniforme(n: int, R: float, rng: np.random.Generator) -> np.ndarray:
    rad = R * np.sqrt(rng.random(n))
    ang = 2.0 * np.pi * rng.random(n)
    return np.c_[rad * np.cos(ang), rad * np.sin(ang)]


def correlacao(s: np.ndarray) -> np.ndarray:
    """C(r): fracao dos pares distintos da secao a distancia <= r, r em RAIOS_CORR."""
    n = len(s)
    arvore = cKDTree(s)
    pares = arvore.count_neighbors(arvore, RAIOS_CORR).astype(float)   # ordenados, com i == j
    return (pares - n) / (n * (n - 1.0))


def medir(caminho: pathlib.Path) -> dict:
    periodo, ts, _nb, seed = (int(g) for g in NOME.match(caminho.name).groups())
    secoes = secoes_em_ordem(caminho, periodo)
    r = dict(ts=ts, seed=seed, n_sections=len(secoes),
             n_per_section=float(np.mean([len(s) for s in secoes])))

    # --- raio de giracao na ordem de crescimento
    curvas = []
    for s in secoes:
        n = np.arange(1, len(s) + 1)
        media = np.cumsum(s, axis=0) / n[:, None]
        rg2 = np.cumsum(s ** 2, axis=0).sum(axis=1) / n - (media ** 2).sum(axis=1)
        curvas.append(np.sqrt(np.maximum(rg2, 0.0)))
    n_max = max(len(c) for c in curvas)
    soma, cont = np.zeros(n_max), np.zeros(n_max)
    for c in curvas:
        soma[: len(c)] += c
        cont[: len(c)] += 1
    rg = soma / cont
    N = np.arange(1, n_max + 1)
    ok = rg > 0
    meio = int(r["n_per_section"] // 2)
    r["gyr_N_hi_primary"] = meio
    r["gyr_primary"] = inclinacao_log_uniforme(rg, N, ok, 40, meio)
    r["gyr_primary_allpts"] = inclinacao(rg, N, ok & (N >= 40) & (N <= meio))
    for nome, (lo, hi) in JANELAS_N.items():
        r[nome] = inclinacao_log_uniforme(rg, N, ok, lo, min(hi, n_max))
        r[nome + "_allpts"] = inclinacao(rg, N, ok & (N >= lo) & (N <= hi))
    r["gyr_local"] = {f"N{lo}_{hi}": inclinacao(rg, N, ok & (N >= lo) & (N <= hi))
                      for lo, hi in zip(OITAVAS[:-1], OITAVAS[1:])}
    # por secao: dentro de uma oitava o peso e uniforme a menos de um fator 2
    r["gyr_local_sections"] = {}
    for lo, hi in zip(OITAVAS[:-1], OITAVAS[1:]):
        vals = []
        for c in curvas:
            Nc = np.arange(1, len(c) + 1)
            vals.append(inclinacao(c, Nc, (c > 0) & (Nc >= lo) & (Nc <= hi)))
        r["gyr_local_sections"][f"N{lo}_{hi}"] = vals

    # --- dimensao de correlacao da secao final
    C = np.array([correlacao(s) for s in secoes])          # (12, len(RAIOS_CORR))
    r["corr_curve"] = C.mean(axis=0)
    okc = r["corr_curve"] > 0

    # --- massa-raio
    massas, rmax = [], []
    for s in secoes:
        d = np.sort(np.sqrt(((s - s.mean(axis=0)) ** 2).sum(axis=1)))
        massas.append(np.searchsorted(d, RAIOS, side="right").astype(float))
        rmax.append(float(d[-1]))
    m = np.mean(massas, axis=0)
    R_bar, R_max = float(np.mean(rmax)), float(max(rmax))
    r["R_bar"], r["R_max"] = R_bar, R_max
    okm = m > 0
    r["mr_fixed_4_8"] = inclinacao(RAIOS, m, okm & (RAIOS >= 4) & (RAIOS <= 8))
    r["mr_rel_0p15R_0p5R"] = inclinacao(RAIOS, m, okm & (RAIOS >= 0.15 * R_bar) & (RAIOS <= 0.5 * R_bar))
    r["mr_full_5_Rmax"] = inclinacao(RAIOS, m, okm & (RAIOS >= 5) & (RAIOS <= R_max))
    r["mr_local"] = {f"r{lo}_{hi}": inclinacao(RAIOS, m, okm & (RAIOS >= lo) & (RAIOS <= hi))
                     for lo, hi in zip(FAIXAS_R[:-1], FAIXAS_R[1:])}
    r["corr_r_hi_primary"] = R_bar / 3.0
    rng = np.random.default_rng(seed)
    Cd = np.array([correlacao(disco_uniforme(len(s_), R_bar, rng)) for s_ in secoes])
    r["corr_disc_curve"] = Cd.mean(axis=0)
    okd = r["corr_disc_curve"] > 0
    for nome, lo, hi in [("corr_primary", 4, R_bar / 3.0), ("corr_4_32", 4, 32)]:
        w = (RAIOS_CORR >= lo) & (RAIOS_CORR <= hi)
        r[nome] = inclinacao(RAIOS_CORR, r["corr_curve"], okc & w)
        r[nome + "_disc"] = inclinacao(RAIOS_CORR, r["corr_disc_curve"], okd & w)
        r[nome + "_corrected"] = r[nome] - r[nome + "_disc"] + 2.0
    r["corr_local"], r["corr_local_sections"] = {}, {}
    r["corr_disc_local"], r["corr_disc_local_sections"] = {}, {}
    for lo, hi in zip(MEIAS_DECADAS[:-1], MEIAS_DECADAS[1:]):
        w = (RAIOS_CORR >= lo) & (RAIOS_CORR <= hi)
        k = f"r{lo}_{hi}"
        r["corr_local"][k] = inclinacao(RAIOS_CORR, r["corr_curve"], okc & w)
        r["corr_local_sections"][k] = [inclinacao(RAIOS_CORR, c, (c > 0) & w) for c in C]
        r["corr_disc_local"][k] = inclinacao(RAIOS_CORR, r["corr_disc_curve"], okd & w)
        r["corr_disc_local_sections"][k] = [inclinacao(RAIOS_CORR, c, (c > 0) & w) for c in Cd]
    return r


def referencias() -> tuple[dict, dict]:
    ref_mr, ref_gyr = {}, {}
    with open(FASE_C / "df_wide_cylinders.csv", encoding="utf-8") as fh:
        for row in csv.DictReader(l for l in fh if not l.startswith("#")):
            if row["objeto"] == "cilindro_periodico":
                ref_mr[(int(row["Ts"]), int(row["seed"]))] = row
    with open(FASE_C / "df_gyration_wide_cylinders.csv", encoding="utf-8") as fh:
        for row in csv.DictReader(l for l in fh if not l.startswith("#")):
            for k, seed in enumerate(SEEDS_REF, start=1):
                ref_gyr[(int(row["Ts"]), seed, row["janela"])] = float(row[f"df_seed_{k}"])
    return ref_mr, ref_gyr


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cylinders", type=pathlib.Path, required=True)
    ap.add_argument("--out", type=pathlib.Path, default=OUT)
    ap.add_argument("--workers", type=int, default=10)
    a = ap.parse_args()

    arquivos = sorted(p for p in a.cylinders.glob("dla_per*_.dat") if NOME.match(p.name))
    por_ts = {ts: sorted(int(NOME.match(p.name).group(4)) for p in arquivos
                         if int(NOME.match(p.name).group(2)) == ts) for ts in TS}
    faltam = {ts: n for ts, n in ((ts, len(v)) for ts, v in por_ts.items()) if n < MIN_SEEDS}
    if faltam or len(arquivos) != sum(len(v) for v in por_ts.values()):
        sys.exit(f"esperava >= {MIN_SEEDS} sementes em cada T_s de {TS}; "
                 f"achei {len(arquivos)} cilindros, por T_s: { {ts: len(v) for ts, v in por_ts.items()} }")
    print("sementes por T_s:", {ts: len(v) for ts, v in por_ts.items()})
    with Pool(a.workers) as pool:
        res = pool.map(medir, arquivos)
    res.sort(key=lambda r: (r["ts"], r["seed"]))

    # --- conferencia contra 2026-09-01 e 2026-09-09
    ref_mr, ref_gyr = referencias()
    conf, falhas = [], 0
    for r in res:
        k = (r["ts"], r["seed"])
        if k not in ref_mr:
            continue
        pares = [("fixa_4_8", r["mr_fixed_4_8"], float(ref_mr[k]["fixa_4_8"])),
                 ("relativa_0p15R_0p5R", r["mr_rel_0p15R_0p5R"], float(ref_mr[k]["relativa_0p15R_0p5R"]))]
        for nome, (lo, hi) in JANELAS_N.items():
            pares.append((f"N_{lo}_{hi}", r[nome + "_allpts"], ref_gyr[(r["ts"], r["seed"], f"N_{lo}_{hi}")]))
        for nome, novo, ref in pares:
            ok = abs(novo - ref) < 1e-3
            falhas += not ok
            conf.append(dict(ts=r["ts"], seed=r["seed"], quantity=nome, new=f"{novo:.4f}",
                             recorded=f"{ref:.4f}", ok=int(ok)))
    print(f"conferencia: {len(conf)} valores, {falhas} fora de 1e-3")
    if falhas:
        for c in conf:
            if not c["ok"]:
                print("  DIFERE", c)
        sys.exit("cilindros nao reproduzem 2026-09-01; nada escrito")

    a.out.mkdir(exist_ok=True)
    (a.out / "xmgrace").mkdir(exist_ok=True)
    cab = ("# D_f dos cilindros periodicos (periodo 216, nb 60000), secoes a cada 18 camadas, "
           "12 por cilindro. gyr_* = raio de giracao na ordem de crescimento (log N x log R_g, "
           f"{PONTOS_POR_OITAVA} pontos por oitava; *_allpts = todos os N inteiros, so conferencia); "
           "corr_* = dimensao de correlacao C(r) da secao final; mr_* = massa-raio. "
           "Gerado por measure_df_periodic_ten_ts.py em 2026-09-10 (peso corrigido, segunda rodada).\n")
    with open(a.out / "identity_check_15_cylinders.csv", "w", newline="", encoding="utf-8") as fh:
        fh.write("# Conferencia dos 15 cilindros de 2026-09-01 contra df_wide_cylinders.csv e df_gyration_wide_cylinders.csv (tolerancia 1e-3).\n")
        w = csv.DictWriter(fh, fieldnames=list(conf[0]))
        w.writeheader(); w.writerows(conf)

    cols = ["gyr_primary", "gyr_N40_320", "gyr_N320_5000", "gyr_N40_5000",
            "gyr_primary_allpts", "gyr_N40_320_allpts", "gyr_N320_5000_allpts", "gyr_N40_5000_allpts",
            "corr_primary", "corr_primary_disc", "corr_primary_corrected",
            "corr_4_32", "corr_4_32_disc", "corr_4_32_corrected",
            "mr_rel_0p15R_0p5R", "mr_fixed_4_8", "mr_full_5_Rmax"]
    with open(a.out / "df_periodic_by_seed.csv", "w", newline="", encoding="utf-8") as fh:
        fh.write(cab)
        w = csv.writer(fh)
        w.writerow(["ts", "seed", "n_sections", "n_per_section", "R_bar", "R_max", "gyr_N_hi_primary", "corr_r_hi_primary"] + cols)
        for r in res:
            w.writerow([r["ts"], r["seed"], r["n_sections"], f"{r['n_per_section']:.1f}",
                        f"{r['R_bar']:.2f}", f"{r['R_max']:.2f}", r["gyr_N_hi_primary"], f"{r['corr_r_hi_primary']:.1f}"]
                       + [f"{r[c]:.4f}" for c in cols])

    def ep(v):
        v = np.asarray(v, float)
        return float(np.std(v, ddof=1) / np.sqrt(len(v)))

    linhas_sum, linhas_loc, dat = [], [], {}
    for ts in TS:
        grupo = [r for r in res if r["ts"] == ts]
        linha = dict(ts=ts, n_seeds=len(grupo),
                     n_per_section=f"{np.mean([r['n_per_section'] for r in grupo]):.1f}",
                     R_bar=f"{np.mean([r['R_bar'] for r in grupo]):.2f}",
                     R_max=f"{np.mean([r['R_max'] for r in grupo]):.2f}",
                     decades_gyr=f"{np.log10(np.mean([r['gyr_N_hi_primary'] for r in grupo]) / 40):.2f}",
                     decades_rel=f"{np.log10(0.5 / 0.15):.2f}")
        for c in cols:
            v = [r[c] for r in grupo]
            linha[f"{c}_mean"], linha[f"{c}_se"] = f"{np.mean(v):.4f}", f"{ep(v):.4f}"
            dat.setdefault(c, []).append((ts, np.mean(v), ep(v)))
        linhas_sum.append(linha)
        for chave in ("gyr_local", "corr_local", "corr_disc_local", "mr_local"):
            for nome in grupo[0][chave]:
                v = [r[chave][nome] for r in grupo]
                linha_loc = dict(ts=ts, method=chave.rsplit("_local", 1)[0], window=nome,
                                 slope_mean=f"{np.nanmean(v):.4f}", slope_se=f"{ep(v):.4f}")
                secs = [x for r in grupo for x in r.get(chave + "_sections", {}).get(nome, [])]
                secs = [x for x in secs if np.isfinite(x)]
                linha_loc["n_sections"] = len(secs)
                linha_loc["slope_section_mean"] = f"{np.mean(secs):.4f}" if secs else ""
                linha_loc["slope_section_se"] = f"{ep(secs):.4f}" if len(secs) > 1 else ""
                linhas_loc.append(linha_loc)
    for caminho, linhas in ((a.out / "df_periodic_summary.csv", linhas_sum),
                            (a.out / "df_periodic_local_slopes.csv", linhas_loc)):
        with open(caminho, "w", newline="", encoding="utf-8") as fh:
            fh.write(cab)
            w = csv.DictWriter(fh, fieldnames=list(linhas[0]))
            w.writeheader(); w.writerows(linhas)

    with open(a.out / "curves_corr_by_ts.csv", "w", newline="", encoding="utf-8") as fh:
        fh.write("# C(r) = fracao dos pares a distancia <= r, media sobre 12 secoes e todas as sementes "
                 "do T_s (n_seeds em df_periodic_summary.csv), por T_s. Gerado por measure_df_periodic_ten_ts.py.\n")
        w = csv.writer(fh)
        w.writerow(["ts", "r", "C", "C_se_seeds", "C_disc"])
        for ts in TS:
            curvas_ts = np.array([r["corr_curve"] for r in res if r["ts"] == ts])
            discos_ts = np.array([r["corr_disc_curve"] for r in res if r["ts"] == ts])
            for j, rr in enumerate(RAIOS_CORR):
                w.writerow([ts, f"{rr:.4f}", f"{curvas_ts[:, j].mean():.6e}", f"{ep(curvas_ts[:, j]):.2e}",
                            f"{discos_ts[:, j].mean():.6e}"])

    with open(a.out / "xmgrace" / "df_by_ts_xydy.dat", "w", encoding="utf-8") as fh:
        n_por_ts = ", ".join(f"{l['ts']}:{l['n_seeds']}" for l in linhas_sum)
        fh.write(f"# D_f versus T_s, periodic cylinders (period 216, nb = 60000); seeds per T_s: {n_por_ts}\n"
                 "# Columns: T_s   D_f   SE over seeds\n"
                 "# Sets: gyration N 40-N_max/2 (primary, 30 pts/octave); correlation 4 <= r <= R_bar/3, "
                 "boundary-corrected by a uniform-disc control; "
                 "mass-radius relative 0.15R-0.5R; mass-radius fixed 4-8\n"
                 "# Use a logarithmic x axis.\n@type xydy\n")
        for c in ["gyr_primary", "corr_primary_corrected", "mr_rel_0p15R_0p5R", "mr_fixed_4_8"]:
            fh.write(f"# {c}\n")
            for ts, v, e in dat[c]:
                fh.write(f"{ts} {v:.4f} {e:.4f}\n")
            fh.write("&\n")

    print(f"{'Ts':>5} {'N/sec':>6} {'R_bar':>6} | {'gir 40-N/2':>12} {'(allpts)':>8} {'gir 40-320':>11} {'gir 320-5k':>11} | {'corr 4-R/3':>12} {'disco':>6} {'corrig':>6} | {'mr rel':>11}")
    for l in linhas_sum:
        print(f"{l['ts']:>5} {l['n_per_section']:>6} {l['R_bar']:>6} | "
              f"{l['gyr_primary_mean']}±{l['gyr_primary_se']} {l['gyr_primary_allpts_mean']:>8} {l['gyr_N40_320_mean']}±{l['gyr_N40_320_se']} "
              f"{l['gyr_N320_5000_mean']}±{l['gyr_N320_5000_se']} | {l['corr_primary_mean']}±{l['corr_primary_se']} "
              f"{l['corr_primary_disc_mean']:>6} {l['corr_primary_corrected_mean']:>6} | {l['mr_rel_0p15R_0p5R_mean']}±{l['mr_rel_0p15R_0p5R_se']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Uma linha por condição (T_s, m): força de ruptura, dano preterminal e o teste da Eq. (5).

Lê:      Reviews/N9_damage_curves/damage_summary.csv
         Reviews/N9_damage_curves/damage_ts<TS>_m<M>_curve_norm.csv
         Reviews/N9_damage_curves/damage_ts<TS>_m<M>_curve_abs.csv
Escreve: Reviews/N9_damage_curves/damage_condition_table.csv
Chamado: à mão, para N9 (Estado_revisao_ER12738.md); a resposta R1-7 em
         Reviews/Respostas_ER12738.md cita esta tabela

O que se testa: se a forma fenomenológica do submetido,
    f(F) = 1e-3 [exp(beta F) - 1 + F^alpha],
ainda descreve a fração removida média sob o protocolo quenched. Ajusta-se
(i) sobre a curva média de todas as realizações (as rompidas contam como 1) e
(ii) sobre a curva condicionada às realizações ainda inteiras. Em (ii) também
se ajusta uma lei de potência pura, phi = c F^alpha, porque o termo exponencial
tende a desaparecer. As colunas rmse dizem qual forma sobra.
"""
from __future__ import annotations

import csv
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "Reviews" / "N9_damage_curves"
OUT = DIR / "damage_condition_table.csv"


def eq5(F, alpha, beta):
    return 1e-3 * (np.exp(beta * F) - 1.0 + F ** alpha)


def power(F, c, alpha):
    return c * F ** alpha


def fit(func, F, y, p0):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            p, _ = curve_fit(func, F, y, p0=p0, maxfev=50000)
        return p, float(np.sqrt(np.mean((func(F, *p) - y) ** 2)))
    except (RuntimeError, ValueError):
        return [np.nan] * len(p0), np.nan


def main() -> int:
    summary = pd.read_csv(DIR / "damage_summary.csv")
    rows = []
    for rec in summary.itertuples(index=False):
        ts, m = int(rec.ts), int(rec.m)
        norm = pd.read_csv(DIR / f"damage_ts{ts}_m{m}_curve_norm.csv")
        ab = pd.read_csv(DIR / f"damage_ts{ts}_m{m}_curve_abs.csv")

        def phi_at(u):
            return float(norm.loc[(norm.u - u).abs().idxmin(), "phi_mean"])

        F = ab.F.values
        y_all = ab.phi_mean_all.values
        ok = (F > 0) & (y_all < 0.999)
        p_all, rmse_all = fit(eq5, F[ok], y_all[ok], [1.0, 1.0 / F[ok].max()])

        y_int = ab.phi_mean_intact.values
        oki = (F > 0) & np.isfinite(y_int) & (ab.n_intact.values >= 100)
        p_int, rmse_int = fit(eq5, F[oki], y_int[oki], [1.0, 1.0 / F[oki].max()])
        p_pow, rmse_pow = fit(power, F[oki], y_int[oki], [1e-3, 1.0])

        rows.append(dict(
            ts=ts, m=m, n_realizations=int(rec.n_realizations),
            n_rods=float(rec.n_rods_mean),
            f_rup_mean=float(rec.f_rup_mean), f_rup_sd=float(rec.f_rup_sd),
            f_rup_cv=float(rec.f_rup_cv),
            f_rup_per_rod=float(rec.f_rup_mean) / float(rec.n_rods_mean),
            phi_preterminal=1.0 - float(rec.terminal_fraction_mean),
            phi_u050=phi_at(0.50), phi_u090=phi_at(0.90), phi_u099=phi_at(0.99),
            eq5_all_alpha=p_all[0], eq5_all_beta=p_all[1], eq5_all_rmse=rmse_all,
            eq5_intact_alpha=p_int[0], eq5_intact_beta=p_int[1], eq5_intact_rmse=rmse_int,
            power_intact_alpha=p_pow[1], power_intact_rmse=rmse_pow,
        ))

    df = pd.DataFrame(rows).sort_values(["m", "ts"])
    df.to_csv(OUT, index=False, float_format="%.6g")
    show = ["ts", "m", "f_rup_mean", "f_rup_cv", "f_rup_per_rod", "phi_preterminal",
            "phi_u090", "eq5_all_beta", "eq5_all_rmse", "power_intact_alpha",
            "power_intact_rmse"]
    print(df[show].to_string(index=False, float_format=lambda v: f"{v:.3g}"))
    print(f"\nescrito: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

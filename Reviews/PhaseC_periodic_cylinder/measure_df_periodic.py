#!/usr/bin/env python3
"""Mede D_f de um cilindro periódico pelo mesmo método do manuscrito.

Lê:      um .dat compacto de cilindro periódico (dla_per<P>_...)
Escreve: relatório em stdout (D_f, alcance em décadas, R_max)
Chamado: à mão, passo 2 da Fase C

Método idêntico ao de validate_fractal_proxy.py / paper_PRE.tex:162:
  1. seções transversais a cada 18 camadas (no anel de período P há P/18);
  2. em cada seção, massa m(R) = nº de partículas a distância <= R do centro
     de massa da seção;
  3. média de m(R) sobre as seções;
  4. ajuste linear de log10 m contra log10 R, de R_min=5 até R_max.
A diferença para o manuscrito é só a quantidade de seções (12 em vez de 11) e
a ausência de janela por condição: aqui o alcance é o que a fibrila dá.
"""
from __future__ import annotations

import math
import sys

import numpy as np
from scipy.stats import linregress

H = 18
R_MIN = 5.0


def carregar(caminho):
    mols = []
    with open(caminho) as fh:
        for linha in fh:
            p = linha.split()
            if len(p) >= 5 and p[0].startswith("uid"):
                mols.append((int(p[2]), int(p[3]), int(p[4])))
    return mols


def particulas_por_camada(mols, periodo):
    """Expande cada haste em H partículas; devolve {camada: array (x,z)}."""
    cam = {}
    for x, y, z in mols:
        for k in range(H):
            yy = (y + k) % periodo
            cam.setdefault(yy, []).append((x, z))
    return {y: np.asarray(v, float) for y, v in cam.items()}


def df_do_cilindro(caminho, periodo=216, passo=18, r_max_override=None):
    mols = carregar(caminho)
    cam = particulas_por_camada(mols, periodo)
    secoes = [cam[y] for y in range(0, periodo, passo) if y in cam]
    rmax_global = 0.0
    for s in secoes:
        c = s.mean(axis=0)
        rmax_global = max(rmax_global, float(np.sqrt(((s - c) ** 2).sum(axis=1)).max()))
    r_top = r_max_override or rmax_global
    radii = np.arange(R_MIN, r_top + 1.0, 1.0)
    massas = []
    for s in secoes:
        c = s.mean(axis=0)
        d = np.sort(np.sqrt(((s - c) ** 2).sum(axis=1)))
        massas.append(np.searchsorted(d, radii, side="right").astype(float))
    m = np.mean(np.vstack(massas), axis=0)
    ok = m > 0
    fit = linregress(np.log10(radii[ok]), np.log10(m[ok]))
    return {
        "n_mol": len(mols), "n_secoes": len(secoes),
        "R_max": rmax_global, "decadas": math.log10(r_top / R_MIN),
        "df": fit.slope, "df_err": fit.stderr, "r2": fit.rvalue ** 2,
        "mol_por_secao": float(np.mean([len(s) for s in secoes])),
    }


if __name__ == "__main__":
    for caminho in sys.argv[1:]:
        r = df_do_cilindro(caminho)
        print(f"{caminho.split('/')[-1]}")
        print(f"  moléculas={r['n_mol']}  partículas/seção={r['mol_por_secao']:.0f}  "
              f"R_max={r['R_max']:.1f}  alcance={r['decadas']:.2f} décadas")
        print(f"  D_f = {r['df']:.3f} ± {r['df_err']:.3f}   (R² = {r['r2']:.4f})")

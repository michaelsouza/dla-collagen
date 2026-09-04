#!/usr/bin/env python3
"""Exporta as tabelas da Figura 8 do manuscrito revisado no formato do xmgrace.

Funcao de sobrevivencia P(S > s) dos tamanhos de cascata preterminal, sem
ajuste: o manuscrito revisado nao reporta expoente (menos de uma decada acima
do menor tamanho ajustavel).

Painel (a): uma serie por T_s, com m = 2.
Painel (b): uma serie por m, com T_s = 128.

Le:      $DLA_PROJECT/campaign/analysis/cascades/casc_ts<TS>_m<M>_pre.npz
         (matriz esparsa; a soma no eixo 0 da a contagem por tamanho, o indice
         e o tamanho da cascata; mesmo esquema lido por plot_survival_by_ts.py)
Escreve: Reviews/N10_cascade_survival/xmgrace/figure_8a_survival_by_ts_xy.dat
         Reviews/N10_cascade_survival/xmgrace/figure_8b_survival_by_m_xy.dat
Chamado: à mão, para a Fig. 8 de N13 (Estado_revisao_ER12738.md), no cluster
         ou depois de copiar os .npz para cá:
         python3 Code/Data_analysis/export_figure_8_xmgrace.py --cascades <dir>
"""
import argparse
import os
import pathlib
import sys

import numpy as np
from scipy import sparse

RAIZ = pathlib.Path(__file__).resolve().parents[2]
SAIDA = RAIZ / "Reviews" / "N10_cascade_survival" / "xmgrace"

TS_PAINEL_A = [2, 16, 128, 1024, 8192]   # como na legenda do manuscrito (Fig. 8)
M_PAINEL_A = 2
MODULOS_PAINEL_B = [1, 2, 3, 5, 10]
TS_PAINEL_B = 128

PISO = 3e-7   # abaixo disso a cauda e um evento unico; o mesmo piso da Fig. 5.2


def sobrevivencia(casc: pathlib.Path, ts: int, m: int):
    """P(S > s) para s >= 1, a partir das contagens por tamanho."""
    arq = casc / f"casc_ts{ts}_m{m}_pre.npz"
    if not arq.exists():
        sys.exit(f"ausente: {arq}\n(os .npz ficam no Lustre; veja o cabecalho)")
    contagens = np.asarray(sparse.load_npz(arq).sum(axis=0)).ravel()
    total = contagens.sum()
    if total == 0:
        sys.exit(f"vazio: {arq}")
    acumulado = np.cumsum(contagens)
    tamanhos = np.arange(len(contagens))
    surv = 1.0 - acumulado / total
    manter = (tamanhos >= 1) & (surv > PISO)
    return tamanhos[manter], surv[manter], int(total)


def bloco(casc, pares, rotulo):
    corpo = []
    for ts, m, nome in pares:
        s, surv, total = sobrevivencia(casc, ts, m)
        corpo += ["@type xy", f"# {nome}; {total} cascatas preterminais"]
        corpo += [f"{int(x):d} {y:.8e}" for x, y in zip(s, surv)]
        corpo.append("&")
        print(f"  {nome}: {len(s)} pontos, {total} cascatas")
    return "\n".join([
        f"# Figure 8({rotulo}): survival function of the preterminal cascade size",
        "# Columns: s   P(S > s)",
        "# Set order: " + ", ".join(n for _, _, n in pares),
        f"# The terminal cascade of each realization is excluded. Points with",
        f"# P(S > s) <= {PISO:g} are dropped: there the tail is a single event.",
        "# Use logarithmic axes on both.",
        "",
    ] + corpo) + "\n"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--cascades", default=os.environ.get("DLA_PROJECT", "") + "/campaign/analysis/cascades")
    a = p.parse_args()
    casc = pathlib.Path(a.cascades)
    if not casc.is_dir():
        sys.exit(f"diretorio de cascatas nao encontrado: {casc}\n"
                 "passe --cascades, ou rode no cluster com $DLA_PROJECT definido")
    SAIDA.mkdir(parents=True, exist_ok=True)

    print("painel (a): sobrevivencia por T_s, m = 2")
    pa = [(ts, M_PAINEL_A, f"T_s = {ts}") for ts in TS_PAINEL_A]
    (SAIDA / "figure_8a_survival_by_ts_xy.dat").write_text(bloco(casc, pa, "a"), encoding="utf-8")

    print(f"painel (b): sobrevivencia por m, T_s = {TS_PAINEL_B}")
    pb = [(TS_PAINEL_B, m, f"m = {m}") for m in MODULOS_PAINEL_B]
    (SAIDA / "figure_8b_survival_by_m_xy.dat").write_text(bloco(casc, pb, "b"), encoding="utf-8")


if __name__ == "__main__":
    main()

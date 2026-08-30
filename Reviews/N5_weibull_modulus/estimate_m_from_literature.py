#!/usr/bin/env python3
"""Estima o módulo de Weibull de fibrilas de colágeno a partir de dados publicados.

Lê:      Reviews/N5_weibull_modulus/quigley2018_tensile_data.xlsx
         (dados brutos de Quigley et al. 2018, Sci Data 5:180229,
          https://doi.org/10.6084/m9.figshare.c.4126559)
         valores de média±DP dos demais estudos, embutidos abaixo com a fonte
Escreve: nada — relatório em stdout
Chamado: à mão, para reproduzir os números de
         Reviews/decision_log/2026-08-30_N5_modulo_de_weibull.md

Dois estimadores: máxima verossimilhança de Weibull (quando há valores
individuais) e a aproximação CV ~ 1.2/m (quando só há média e desvio).

ATENÇÃO: todo valor aqui foi conferido no PDF primário em Bibliography/.
Números tomados da discussão de outro artigo levaram a erro uma vez
(ver a §"Correção" da entrada do decision_log) e não devem ser usados.
"""
from __future__ import annotations

import os
import warnings

import numpy as np

warnings.filterwarnings("ignore")
from scipy import stats  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(AQUI, "quigley2018_tensile_data.xlsx")

# média, DP, n, procedência — todos conferidos no PDF primário
REPORTADOS = [
    ("Svensson2013 HPT patelar humano",   540, 140, None, "Tabela 3"),
    ("Svensson2013 RTT cauda nativo",     200, 110, None, "Tabela 3"),
    ("Svensson2013 RTT grupo 3",          290,  80, None, "Tabela 3"),
    ("Svensson2013 RTT grupo 4",          270,  60, None, "Tabela 3"),
    ("Svensson2013 RTT grupo 5",          250, 100, None, "Tabela 3"),
    ("Yang2012 Aquiles bovino isolada",    60,  10,   11, "texto, seção 3.2"),
]


def m_por_cv(media: float, dp: float) -> float:
    """CV ~ 1.2/m: aproximação válida para m entre ~1.5 e ~10."""
    return 1.2 / (dp / media)


def m_por_mle(x: np.ndarray) -> float:
    """Parâmetro de forma de Weibull por máxima verossimilhança, loc fixo em 0."""
    return stats.weibull_min.fit(x, floc=0)[0]


def main() -> None:
    print("A · média±DP reportados (aproximação CV)\n")
    for nome, mu, dp, n, onde in REPORTADOS:
        ntxt = f"n={n}" if n else "n=?"
        print(f"  {nome:34s} {mu:3d}±{dp:3d}  {ntxt:5s} "
              f"CV={dp/mu:.3f}  m~{m_por_cv(mu, dp):4.1f}   ({onde})")

    if not os.path.exists(XLSX):
        print(f"\n  ausente: {XLSX}")
        return

    import openpyxl
    ws = openpyxl.load_workbook(XLSX, data_only=True).worksheets[0]
    linhas = [r for r in ws.iter_rows(min_row=2, values_only=True)
              if r[7] is not None and r[4] is not None]
    # 'f' = flexor digital superficial (armazenamento de energia, mais reticulado)
    # 'e' = extensor digital comum (posicional)
    sigma = np.array([float(r[7]) for r in linhas])
    tendao = [str(r[1]) for r in linhas]

    print("\nB · Quigley2018, valores individuais (máxima verossimilhança)\n")
    for rot, sel in (("flexor (energético)", "f"), ("extensor (posicional)", "e"),
                     ("todos", None)):
        x = sigma if sel is None else sigma[[t == sel for t in tendao]]
        print(f"  {rot:24s} n={len(x):3d}  média={x.mean():6.1f}  "
              f"CV={x.std(ddof=1)/x.mean():.3f}  m(MLE)={m_por_mle(x):4.1f}")

    print("\n  Faixa consolidada no nível da FIBRILA: m entre 2 e 7, "
          "concentrado em 4–5.")
    print("  Ela NÃO fixa o m molecular do modelo — ver a entrada do decision_log.")


if __name__ == "__main__":
    main()

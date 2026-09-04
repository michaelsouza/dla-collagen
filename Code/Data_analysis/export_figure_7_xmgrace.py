#!/usr/bin/env python3
"""Exporta as tabelas da Figura 7 do manuscrito revisado no formato do xmgrace.

Painel (a): forca media de ruptura por T_s, uma serie por modulo de Weibull m.
Painel (b): dano preterminal contra forca normalizada, uma serie por T_s (m=2).

Le:      Reviews/N9_damage_curves/damage_summary.csv
         Reviews/N9_damage_curves/damage_ts<TS>_m2_curve_norm.csv
Escreve: Reviews/N9_damage_curves/xmgrace/figure_7a_f_rup_vs_ts_xydy.dat
         Reviews/N9_damage_curves/xmgrace/figure_7b_phi_vs_u_xydy.dat
Chamado: à mão, para a Fig. 7 de N13 (Estado_revisao_ER12738.md); refazer se
         damage_summary.csv mudar
"""
import csv
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]
DADOS = RAIZ / "Reviews" / "N9_damage_curves"
SAIDA = DADOS / "xmgrace"

MODULOS = [1, 2, 3, 5, 10]          # a grade completa de m da campanha
TS_PAINEL_B = [2, 32, 128, 8192]    # as quatro do painel (b), como na legenda
M_PAINEL_B = 2                      # m ilustrativo do manuscrito


def painel_a() -> str:
    """F_rup(T_s) com desvio padrao, uma serie por m. Eixo x logaritmico base 2."""
    linhas = list(csv.DictReader(open(DADOS / "damage_summary.csv")))
    por_m = {}
    for r in linhas:
        por_m.setdefault(int(r["m"]), []).append(
            (int(r["ts"]), float(r["f_rup_mean"]), float(r["f_rup_sd"]))
        )

    out = [
        "# Figure 7(a): mean rupture force versus surface diffusion parameter",
        "# Columns: T_s  <F_rup>  SD(F_rup)",
        "# One set per Weibull modulus, in the order m = " + ", ".join(map(str, MODULOS)),
        "# Each point averages 10^4 realizations (200 fibrils x 50 draws).",
        "# Use a base-2 logarithmic x axis and a linear y axis.",
    ]
    for m in MODULOS:
        pontos = sorted(por_m[m])
        out += ["@type xydy", f"# m = {m}"]
        out += [f"{ts:d} {media:.4f} {sd:.4f}" for ts, media, sd in pontos]
        out.append("&")
    return "\n".join(out) + "\n"


def painel_b() -> str:
    """phi(F/F_rup) preterminal com desvio padrao, uma serie por T_s.

    O ultimo ponto de cada curva, em u = 1, vale phi = 1 por construcao: e a
    cascata terminal, que remove o que restou do esqueleto de uma vez. Ele fica
    fora, porque a curva do painel e a do dano *preterminal*.
    """
    out = [
        "# Figure 7(b): preterminal damage versus normalized force",
        "# Columns: u = F/F_rup   <phi>   SD(phi)",
        "# One set per T_s, in the order T_s = " + ", ".join(map(str, TS_PAINEL_B)),
        f"# Weibull modulus fixed at m = {M_PAINEL_B}; 10^4 realizations per set.",
        "# The point at u = 1 is omitted: there phi = 1 by construction, because",
        "# the terminal cascade removes the remaining backbone in a single event.",
        "# Use linear axes on both.",
    ]
    for ts in TS_PAINEL_B:
        arq = DADOS / f"damage_ts{ts}_m{M_PAINEL_B}_curve_norm.csv"
        pontos = [
            (float(r["u"]), float(r["phi_mean"]), float(r["phi_sd"]))
            for r in csv.DictReader(open(arq))
            if float(r["u"]) < 1.0
        ]
        out += ["@type xydy", f"# T_s = {ts}"]
        out += [f"{u:.4f} {media:.6f} {sd:.6f}" for u, media, sd in pontos]
        out.append("&")
    return "\n".join(out) + "\n"


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    for nome, conteudo in [
        ("figure_7a_f_rup_vs_ts_xydy.dat", painel_a()),
        ("figure_7b_phi_vs_u_xydy.dat", painel_b()),
    ]:
        (SAIDA / nome).write_text(conteudo, encoding="utf-8")
        n = sum(1 for l in conteudo.splitlines() if l and not l.startswith(("#", "@", "&")))
        print(f"{nome}: {conteudo.count('@type')} series, {n} pontos")


if __name__ == "__main__":
    main()

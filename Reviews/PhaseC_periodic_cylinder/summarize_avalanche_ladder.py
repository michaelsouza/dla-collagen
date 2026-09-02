#!/usr/bin/env python3
"""Resume a estatística de avalanches ao longo de uma escada de janelas de corte.

Lê:      diretórios de saída legada do fiber_bundle_ava.py (ts_<TS>/*.txt),
         um por largura de janela; cada arquivo tem várias realizações
         separadas por linhas de '-'
Escreve: tabela em stdout e, com --csv, um CSV
Chamado: à mão, passo 2b da Fase C (README.md §4c)

A pergunta que a escada responde: o corte das avalanches (~90 na campanha) se
move quando o corpo de prova cresce, à arquitetura fixa? Aqui o objeto é UM
cilindro periódico largo, fraturado por janelas 17, 41, 81 e 181; só a janela
muda. Coluna 4 do formato legado = moléculas removidas na cascata (a avalanche);
a linha com num_active_particles == 0 é o evento terminal, tratado à parte.
"""
from __future__ import annotations

import csv
import glob
import os
import sys

import numpy as np


def ler(caminho):
    """Devolve (lista de avalanches não-terminais, lista de terminais, n_real, part_iniciais)."""
    nt, term, nreal, p0 = [], [], 0, []
    with open(caminho) as fh:
        for linha in fh:
            if linha.startswith("-") or linha.startswith("f,"):
                continue
            c = linha.rstrip("\n").split(",")
            if len(c) < 4:
                continue
            if c[0] == "0":
                nreal += 1
                p0.append(int(c[1]))
                continue
            ativos, rods = int(c[1]), int(c[3])
            if ativos == 0:
                term.append(rods)
            elif rods > 0:
                nt.append(rods)
    return nt, term, nreal, p0


def resumo(rotulo, arquivos):
    nt, term, nreal, p0 = [], [], 0, []
    for a in arquivos:
        x, y, n, p = ler(a)
        nt += x; term += y; nreal += n; p0 += p
    if not nt:
        return None
    v = np.sort(np.asarray(nt))
    mol = np.mean(p0) / 16.6          # partículas/molécula medido na campanha
    return dict(janela=rotulo, n_real=nreal, particulas=int(np.mean(p0)), moleculas=int(mol),
                eventos=len(v), frac_1=float(np.mean(v == 1)),
                p90=int(v[int(0.9 * len(v))]), p99=int(v[int(0.99 * len(v))]),
                max_nt=int(v[-1]), terminal=float(np.mean(term)) if term else float("nan"),
                terminal_frac=float(np.mean(term) / mol) if term else float("nan"))


def main(pares, csv_out=None):
    linhas = []
    print(f"  {'janela':10s} {'n_real':>6s} {'moleculas':>9s} {'eventos':>7s} {'frac1':>6s} {'p90':>4s} {'p99':>4s} {'max_nt':>6s} {'terminal':>9s} {'term/N':>6s}")
    for rotulo, d in pares:
        arqs = glob.glob(os.path.join(d, "ts_*", "*.txt"))
        r = resumo(rotulo, arqs)
        if r is None:
            print(f"  {rotulo:10s} (sem dados ainda)")
            continue
        linhas.append(r)
        print(f"  {r['janela']:10s} {r['n_real']:6d} {r['moleculas']:9d} {r['eventos']:7d} {r['frac_1']:6.2f} "
              f"{r['p90']:4d} {r['p99']:4d} {r['max_nt']:6d} {r['terminal']:9.0f} {r['terminal_frac']:6.2f}")
    if csv_out and linhas:
        with open(csv_out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()))
            w.writeheader(); w.writerows(linhas)
        print(f"  -> {csv_out}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--csv=")]
    csv_out = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--csv=")), None)
    if len(args) % 2:
        sys.exit("uso: summarize_avalanche_ladder.py <rotulo> <dir> [<rotulo> <dir> ...] [--csv=arquivo]")
    main(list(zip(args[::2], args[1::2])), csv_out)

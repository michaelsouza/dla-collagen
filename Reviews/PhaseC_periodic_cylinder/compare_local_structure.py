#!/usr/bin/env python3
"""Compara a estrutura LOCAL de fibrilas livres e de cilindros periódicos.

Lê:      arquivos .dat no formato compacto (uid: <uid> <x> <y> <z>), livres em
         <dir>/free/ e periódicos em <dir>/per/
Escreve: relatório em stdout
Chamado: à mão, passo 1 da Fase C (README.md, §4)

Grandezas escolhidas de propósito: coordenação K e distribuição de encaixes
0D–4D são médias sobre milhares de moléculas DENTRO de uma fibrila, logo bem
determinadas mesmo num objeto pequeno. O D_f NÃO entra — usá-lo como critério
seria circular, já que é o número que a Fase C existe para tornar confiável.

Armadilha corrigida em 2026-09-01: na fibrila livre a janela |y|<=J era aplicada
antes de montar as vizinhanças, e hastes perto da borda perdiam vizinhos logo
fora dela (~20% das hastes, cada uma perdendo metade de um lado). Isso
subestimava K em ~4,5% e produzia uma diferença falsa de 4,5 desvios. A
vizinhança agora é montada com margem |y|<=J+H e só o miolo entra na média.
"""
from __future__ import annotations

import glob
import math
import sys
from collections import defaultdict

H = 18          # comprimento da haste em unidades de rede
STAGGER = 4     # passo de encaixe


def carregar(caminho):
    mols = []
    with open(caminho) as fh:
        for linha in fh:
            p = linha.split()
            if len(p) >= 5 and p[0].startswith("uid"):
                mols.append((int(p[2]), int(p[3]), int(p[4])))   # x, y, z
    return mols


def analisar(mols, periodo=None, janela=None):
    """periodo=None -> livre (média em |y|<=janela); senão anel de período dado."""
    alvo = mols
    if periodo is None and janela is not None:
        mols = [m for m in mols if -(janela + H) <= m[1] <= janela + H]
        alvo = [m for m in mols if -janela <= m[1] <= janela]
    col = defaultdict(list)
    for x, y, z in mols:
        col[(x, z)].append(y)

    def sobrepoe(ya, yb):
        if periodo is None:
            return abs(ya - yb) < H
        d = (ya - yb) % periodo
        return d < H or d > periodo - H

    def delta(ya, yb):
        if periodo is None:
            return ya - yb
        d = (ya - yb) % periodo
        return d - periodo if d > periodo // 2 else d

    Ks, staggers = [], defaultdict(int)
    for x, y, z in alvo:
        k = 0
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for yv in col.get((x + dx, z + dz), ()):
                if sobrepoe(y, yv):
                    k += 1
                    d = abs(delta(y, yv))
                    if d % STAGGER == 0:
                        staggers[min(d // STAGGER, 4)] += 1
        Ks.append(k)

    n = len(Ks)
    media = sum(Ks) / n if n else 0.0
    var = sum((k - media) ** 2 for k in Ks) / (n - 1) if n > 1 else 0.0
    tot = sum(staggers.values()) or 1
    return {"n": n, "K": media, "K_dp": math.sqrt(var),
            "stagger": {i: staggers.get(i, 0) / tot for i in range(5)}}


def resumo(rotulo, rs):
    v = [r["K"] for r in rs]
    mu = sum(v) / len(v)
    sd = math.sqrt(sum((x - mu) ** 2 for x in v) / (len(v) - 1)) if len(v) > 1 else 0.0
    st = [sum(r["stagger"][i] for r in rs) / len(rs) for i in range(5)]
    print(f"  {rotulo:26s} n={rs[0]['n']:6d}  K={mu:5.3f}±{sd:.3f}"
          "  encaixes 0D-4D: " + " ".join(f"{100*x:4.1f}" for x in st))
    return mu, sd, st


def main(base: str, periodo: int = 216, janela: int = 90):
    for ts in (2, 128, 8192):
        print(f"\n=== Ts = {ts} ===")
        livres = sorted(glob.glob(f"{base}/free/dla_mode_s_ts_{ts}_nb_*_seed_*.dat"))
        peris = sorted(glob.glob(f"{base}/per/dla_per{periodo}_mode_s_ts_{ts}_nb_*_seed_*.dat"))
        if not livres or not peris:
            print(f"  faltam arquivos (livres={len(livres)}, periódicas={len(peris)})")
            continue
        rl = [analisar(carregar(f), None, janela) for f in livres]
        rp = [analisar(carregar(f), periodo, None) for f in peris]
        kl, sl, stl = resumo(f"livre ({len(rl)} sementes)", rl)
        kp, sp, stp = resumo(f"periódica ({len(rp)} sementes)", rp)
        sig = math.sqrt(sl ** 2 + sp ** 2) or 1e-9
        print(f"  -> K difere {100*(kp-kl)/kl:+.1f}%  ({abs(kp-kl)/sig:.1f} desvios)")
        pior = max(range(5), key=lambda i: abs(stp[i] - stl[i]))
        print(f"  -> maior diferença de encaixe: {pior}D, "
              f"{100*(stp[pior]-stl[pior]):+.1f} pontos percentuais")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")

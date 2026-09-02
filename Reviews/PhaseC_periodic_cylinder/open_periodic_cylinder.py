#!/usr/bin/env python3
"""Abre um cilindro periódico num plano, devolvendo um segmento com dois extremos.

Lê:      .dat compacto periódico (y em [0, P))
Escreve: .dat compacto com y deslocado para [-P/2, P/2), nome com sufixo _open
Chamado: à mão, passo 2 da Fase C, antes de extend_fibrils_batch.py

Por que existe: o motor de fratura exige extremos livres (o backbone é extraído
de ponta a ponta em y) e corta em |y| <= half_length. Deslocando y por -P/2 o
plano de abertura cai em y = ±P/2; o extend expande cada haste sem envolver, e
o corte da fratura trunca o que atravessa o plano — exatamente o mesmo tipo de
borda dos corpos de prova da campanha (hastes partidas em y = ±100).

Onde abrir é indiferente: no cilindro periódico todo y é equivalente.
"""
from __future__ import annotations

import sys
from pathlib import Path


def abrir(origem: Path, periodo: int) -> Path:
    destino = origem.with_name(origem.stem + "_open" + origem.suffix)
    meio = periodo // 2
    n = 0
    with open(origem) as fin, open(destino, "w") as fout:
        for linha in fin:
            p = linha.split()
            if len(p) >= 5 and p[0].startswith("uid"):
                y = int(p[3])
                if not 0 <= y < periodo:
                    raise ValueError(f"y={y} fora de [0,{periodo}) em {origem}")
                fout.write(f"uid: {p[1]} {p[2]} {y - meio} {p[4]}\n")
                n += 1
            else:
                fout.write(linha)
    print(f"  {destino.name}: {n} moléculas, y em [{-meio}, {periodo - meio})")
    return destino


if __name__ == "__main__":
    periodo = int(sys.argv[1])
    for f in sys.argv[2:]:
        abrir(Path(f), periodo)

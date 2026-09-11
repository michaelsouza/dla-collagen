#!/usr/bin/env python3
"""Gera grade 2x3 de seções transversais dos cilindros periódicos em PDF.

Lê:      Data_fibrils/periodic_cylinders_216_nb60000_10Ts_5to40seeds.tar.gz
Escreve: Reviews/N18_df_ten_ts/figures/sections_by_ts_2x3.pdf
Chamado: à mão
"""
from __future__ import annotations

import io
import pathlib
import sys
import tarfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RAIZ = pathlib.Path(__file__).resolve().parents[2]
TAR_PADRAO = RAIZ / "Data_fibrils" / "periodic_cylinders_216_nb60000_10Ts_5to40seeds.tar.gz"
FIG_DIR = RAIZ / "Reviews" / "N18_df_ten_ts" / "figures"
ESTILO = RAIZ / "Code" / "Data_analysis" / "xmgrace_paper.mplstyle"

TS_LIST = [2, 16, 64, 128, 1024, 8192]
SEED = 900001
PERIODO = 216
H = 18
FG = "#23373B"


def extrair_secao0(linhas: io.TextIOBase) -> np.ndarray:
    """Extrai pontos (x, z) da seção L=0 na ordem de chegada."""
    mols = []
    uids = []
    for linha in linhas:
        p = linha.split()
        if len(p) >= 5 and p[0].startswith("uid"):
            uids.append(int(p[1]))
            mols.append((int(p[2]), int(p[3]), int(p[4])))
    assert len(uids) == len(mols) and all(b > a for a, b in zip(uids, uids[1:])), \
        "uid não cresce estritamente na ordem do arquivo"
    xyz = np.asarray(mols, dtype=np.int64)
    pertence = (0 - xyz[:, 1]) % PERIODO < H
    return xyz[pertence][:, [0, 2]].astype(float)


def carregar_secoes_do_tar(caminho_tar: pathlib.Path) -> dict[int, np.ndarray]:
    secoes = {}
    with tarfile.open(caminho_tar, "r:gz") as tar:
        for ts in TS_LIST:
            nome_membro = f"dla_per216_mode_s_ts_{ts}_nb_60000_seed_{SEED}_.dat"  # o tar da noite de 2026-09-10 nao tem prefixo de diretorio
            membro = tar.getmember(nome_membro)
            f = tar.extractfile(membro)
            assert f is not None, f"Falha ao extrair {nome_membro}"
            with io.TextIOWrapper(f, encoding="utf-8") as text_io:
                secoes[ts] = extrair_secao0(text_io)
    return secoes


def plotar_grade_2x3(secoes: dict[int, np.ndarray], caminho_pdf: pathlib.Path) -> None:
    caminho_pdf.parent.mkdir(parents=True, exist_ok=True)
    if ESTILO.exists():
        plt.style.use(ESTILO)

    fig, axs = plt.subplots(2, 3, figsize=(8.0, 5.5))
    for ax, ts in zip(axs.ravel(), TS_LIST):
        s = secoes[ts]
        ordem = np.arange(len(s)) / len(s)
        ax.scatter(
            s[:, 0],
            s[:, 1],
            c=ordem,
            cmap="viridis",
            s=1.2,
            linewidths=0,
            rasterized=True,
        )
        ax.set_aspect("equal")
        ax.set_xlim(-170, 170)
        ax.set_ylim(-170, 170)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"$T_s = {ts}$", fontsize=15, color=FG, pad=8)

    fig.tight_layout()
    fig.savefig(caminho_pdf, dpi=300)
    plt.close(fig)
    print(f"Salvo: {caminho_pdf}")


def main() -> None:
    caminho_tar = TAR_PADRAO
    if len(sys.argv) > 1:
        caminho_tar = pathlib.Path(sys.argv[1])
    if not caminho_tar.exists():
        sys.exit(f"Arquivo não encontrado: {caminho_tar}")

    secoes = carregar_secoes_do_tar(caminho_tar)
    destino_pdf = FIG_DIR / "sections_by_ts_2x3.pdf"
    plotar_grade_2x3(secoes, destino_pdf)


if __name__ == "__main__":
    main()

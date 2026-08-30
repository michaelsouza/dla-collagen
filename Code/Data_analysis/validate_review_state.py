#!/usr/bin/env python3
"""Confere se as afirmações de Reviews/Estado_revisao_ER12738.md ainda são verdade.

Lê:      Reviews/Estado_revisao_ER12738.md; Reviews/decision_log/;
         Code/**/*.py; $DLA_PROJECT no SDumont2 (opcional, via ssh)
Escreve: nada — só relatório em stdout; código de saída 1 se algo falhou
Chamado: à mão, antes de confiar no estado; idealmente semanal

Cada checagem existe porque um erro real passou por ela nesta semana:
  C1  §9 afirmava que as fibrilas brutas estavam ausentes; estavam num zip aqui
  C2  §2 dava a campanha como bloqueada quatro dias depois de ela terminar
  C3  entradas de registro devem ser append-only
  C4  o estado apontava para arquivos que podiam não existir
  C5  cabeçalhos dizendo "Chamado: X" com X inexistente
  C6  nove variantes de extend_fibrils com sufixos de versão
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ESTADO = os.path.join(RAIZ, "Reviews", "Estado_revisao_ER12738.md")
REGISTRO = os.path.join(RAIZ, "Reviews", "decision_log")
FIBRILAS = os.path.join(RAIZ, "Data_fibrils",
                        "fibrilas_publicadas_artigo_10Ts_nb30000.zip")

falhas: list[str] = []
avisos: list[str] = []


def ok(msg: str) -> None:
    print(f"  ok      {msg}")


def falhou(msg: str) -> None:
    print(f"  FALHOU  {msg}")
    falhas.append(msg)


def aviso(msg: str) -> None:
    print(f"  aviso   {msg}")
    avisos.append(msg)


def _sem_caminhos(diff: str, sinal: str) -> str:
    """Linhas do diff com o sinal dado, sem os tokens que parecem caminho.

    Serve para distinguir renomeação mecânica de edição de conteúdo: se o texto
    restante de adições e remoções coincide, só caminhos mudaram.
    """
    linhas = [l[1:] for l in diff.splitlines()
              if l.startswith(sinal) and not l.startswith(sinal * 3)]
    texto = "\n".join(linhas)
    return re.sub(r"[\w.\-]+/[\w./\-]*", "", texto)


def c1_fibrilas_publicadas() -> None:
    """As fibrilas do artigo existem localmente e cobrem as 10 condições."""
    print("\nC1 · fibrilas publicadas")
    if not os.path.exists(FIBRILAS):
        falhou(f"ausente: {os.path.relpath(FIBRILAS, RAIZ)}")
        return
    try:
        import zipfile
        with zipfile.ZipFile(FIBRILAS) as z:
            ts = {m.group(1) for n in z.namelist()
                  if (m := re.search(r"_ts_(\d+)_", n))}
    except Exception as e:  # noqa: BLE001
        falhou(f"zip ilegível: {e}")
        return
    if len(ts) == 10:
        ok(f"10 condições de $T_s$ presentes: {sorted(ts, key=int)}")
    else:
        falhou(f"esperava 10 condições, achei {len(ts)}: {sorted(ts, key=int)}")


def c2_campanha_no_cluster() -> None:
    """A campanha tem 10.000 arquivos de avalanche e 2.000 fibrilas."""
    print("\nC2 · campanha no SDumont2")
    cmd = ("P=$HOME/scratch/dla-collagen/campaign; "
           "find $P/avalanches -type f | wc -l; "
           "find $P/fibrils/extended -type f | wc -l")
    try:
        saida = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15",
             "sdumont2nd", cmd],
            capture_output=True, text=True, timeout=180)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        aviso("cluster inacessível — checagem pulada, NÃO conte como verificada")
        return
    if saida.returncode != 0:
        aviso("cluster inacessível — checagem pulada, NÃO conte como verificada")
        return
    nums = [int(x) for x in saida.stdout.split() if x.isdigit()]
    if len(nums) < 2:
        aviso(f"resposta inesperada do cluster: {saida.stdout!r}")
        return
    avalanches, fibrilas = nums[0], nums[1]
    (ok if avalanches == 10000 else falhou)(
        f"avalanches: {avalanches} (esperado 10000)")
    (ok if fibrilas == 2000 else falhou)(
        f"fibrilas estendidas: {fibrilas} (esperado 2000)")


def c3_registro_append_only() -> None:
    """Nenhuma entrada de registro teve o conteúdo alterado depois de criada.

    Renomeação de arquivo ou diretório não conta: `--diff-filter=M` pede ao git
    só os commits que de fato modificaram o conteúdo, deixando de fora criação
    (A) e renomeação pura (R). Entre os que sobram, ainda são aceitáveis os que
    só corrigiram caminhos — a exceção registrada na §2 do AGENTS.md.
    """
    print("\nC3 · registro append-only")
    if not os.path.isdir(REGISTRO):
        falhou("Reviews/decision_log/ não existe")
        return
    alterados, so_caminho = [], []
    entradas = [n for n in sorted(os.listdir(REGISTRO))
                if n.endswith(".md") and n != "README.md"]
    for nome in entradas:
        caminho = os.path.join("Reviews", "decision_log", nome)
        r = subprocess.run(
            ["git", "log", "--follow", "--diff-filter=M", "--format=%H",
             "--", caminho], cwd=RAIZ, capture_output=True, text=True)
        commits = [c for c in r.stdout.split() if c]
        if not commits:
            continue
        conteudo_mudou = False
        for commit in commits:
            d = subprocess.run(
                ["git", "show", "--format=", "--unified=0", commit,
                 "--", caminho], cwd=RAIZ, capture_output=True, text=True)
            if _sem_caminhos(d.stdout, "+") != _sem_caminhos(d.stdout, "-"):
                conteudo_mudou = True
                break
        (alterados if conteudo_mudou else so_caminho).append(
            f"{nome} ({len(commits)})")
    if alterados:
        falhou("entradas com conteúdo editado após criação: "
               + ", ".join(alterados))
    else:
        extra = (f"; {len(so_caminho)} com correção de caminho apenas, "
                 f"permitida pela §2 do AGENTS.md" if so_caminho else "")
        ok(f"{len(entradas)} entradas, nenhuma com conteúdo editado{extra}")


def c4_caminhos_do_estado() -> None:
    """Todo caminho citado no estado existe."""
    print("\nC4 · caminhos citados no estado")
    if not os.path.exists(ESTADO):
        falhou("Reviews/Estado_revisao_ER12738.md não existe")
        return
    texto = open(ESTADO).read()
    padrao = re.compile(r"`([A-Za-z_][\w/.\-]*\.(?:tex|py|md|zip|sh|cpp))")
    faltando = sorted({
        c for c in padrao.findall(texto)
        if "/" in c and not os.path.exists(os.path.join(RAIZ, c))
    })
    if faltando:
        falhou("citados e inexistentes: " + ", ".join(faltando))
    else:
        ok("todos os caminhos com diretório resolvem")


def c5_cabecalhos_chamado_por() -> None:
    """Cabeçalho que declara 'Chamado: X' precisa que X exista."""
    print("\nC5 · cabeçalhos 'Chamado:'")
    checados = quebrados = 0
    for base, _, arquivos in os.walk(os.path.join(RAIZ, "Code")):
        if "annealed_protocol" in base or "extracted_notebooks" in base:
            continue
        for nome in arquivos:
            if not nome.endswith(".py"):
                continue
            caminho = os.path.join(base, nome)
            cabeca = open(caminho, errors="replace").read(2000)
            m = re.search(r"^Chamado:\s*(.+)$", cabeca, re.M)
            if not m:
                continue
            checados += 1
            for alvo in re.split(r"[;,]", m.group(1)):
                alvo = alvo.strip()
                if not alvo or " " in alvo:
                    continue
                achou = os.path.exists(os.path.join(RAIZ, alvo)) or any(
                    alvo in fs for _, _, fs in os.walk(os.path.join(RAIZ, "Code")))
                if not achou:
                    quebrados += 1
                    falhou(f"{os.path.relpath(caminho, RAIZ)} declara "
                           f"'Chamado: {alvo}', que não existe")
    if checados == 0:
        aviso("nenhum arquivo declara 'Chamado:' ainda — ver §4 do AGENTS.md")
    elif quebrados == 0:
        ok(f"{checados} cabeçalhos declaram 'Chamado:', todos resolvem")


def c6_sufixos_de_versao() -> None:
    """Nenhum arquivo com sufixo de versão no nome."""
    print("\nC6 · sufixos de versão")
    proibidos = re.compile(r"(_v\d+|_fixed|_new|_old|_REBUILT|_clean(ed)?|\.bak)"
                           r"(\.\w+)?$")
    achados = []
    r = subprocess.run(["git", "ls-files"], cwd=RAIZ,
                       capture_output=True, text=True)
    for caminho in r.stdout.splitlines():
        if "annealed_protocol" in caminho or "extracted_notebooks" in caminho:
            continue
        if not os.path.exists(os.path.join(RAIZ, caminho)):
            continue  # apagado no working tree, ainda no índice
        if proibidos.search(caminho):
            achados.append(caminho)
    if achados:
        falhou("sufixo de versão no nome: " + ", ".join(achados))
    else:
        ok("nenhum sufixo de versão")


def main() -> int:
    print("Conferindo Reviews/Estado_revisao_ER12738.md\n" + "=" * 52)
    for checagem in (c1_fibrilas_publicadas, c2_campanha_no_cluster,
                     c3_registro_append_only, c4_caminhos_do_estado,
                     c5_cabecalhos_chamado_por, c6_sufixos_de_versao):
        try:
            checagem()
        except Exception as e:  # noqa: BLE001
            falhou(f"{checagem.__name__} lançou {type(e).__name__}: {e}")
    print("\n" + "=" * 52)
    if falhas:
        print(f"{len(falhas)} FALHA(S) — o estado não está confiável:")
        for f in falhas:
            print(f"  · {f}")
    else:
        print("Nenhuma falha.")
    if avisos:
        print(f"{len(avisos)} aviso(s) — checagem não executada:")
        for a in avisos:
            print(f"  · {a}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())

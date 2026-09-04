#!/usr/bin/env python3
"""Monta os projetos .agr das Figuras 7 e 8 do manuscrito revisado.

O xmgrace e o ambiente dos coautores e o .agr e o artefato versionado; este
script produz a primeira versao dele a partir dos .dat, de forma reproduzivel.
Dali em diante o .agr e editado no proprio xmgrace.

Le:      Reviews/N9_damage_curves/xmgrace/figure_7[ab]_*.dat
         Reviews/N10_cascade_survival/xmgrace/figure_8[ab]_*.dat
Escreve: Reviews/N9_damage_curves/xmgrace/figure_7.agr   e Paper/figure_7.pdf
         Reviews/N10_cascade_survival/xmgrace/figure_8.agr e Paper/figure_8.pdf
Chamado: à mão, depois de export_figure_7_xmgrace.py e export_figure_8_xmgrace.py
"""
import math
import pathlib
import shutil
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[2]
F7 = RAIZ / "Reviews" / "N9_damage_curves" / "xmgrace"
F8 = RAIZ / "Reviews" / "N10_cascade_survival" / "xmgrace"
FIGS = RAIZ / "Paper"

# rampa azul sequencial, a mesma do relatorio da campanha; as series se
# distinguem pelo simbolo, nao pela cor, porque os azuis sao proximos demais
# tamanhos de fonte e espessuras do estilo dos coautores, medidos em
# Reviews/N7_fractal_proxy/xmgrace/figure_7.agr: rotulo 3,0; tique 2,25;
# legenda 1,8; painel 2,25; barra e tique com espessura 2,0; fonte 3
# (Times-BoldItalic), que e o "\3" no inicio de cada rotulo de eixo
ROTULO, TIQUE, LEGENDA, PAINEL = 3.0, 2.25, 1.4, 2.25
GROSSURA_EIXO = 2.0

RAMPA = [(134, 182, 239), (85, 152, 231), (42, 120, 214), (28, 92, 171), (13, 54, 107)]
SIMBOLOS = [1, 2, 3, 4, 10]     # circulo, quadrado, diamante, triangulo, estrela
TS_GRADE = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192]


def cores() -> list[str]:
    return [f'MAP COLOR {20 + i} TO ({r}, {g}, {b}), "ramp{i}"'
            for i, (r, g, b) in enumerate(RAMPA)]


def simbolo(s: int, i: int) -> list[str]:
    cor = 20 + i
    return [f"S{s} SYMBOL {SIMBOLOS[i % len(SIMBOLOS)]}",
            "S{} SYMBOL SIZE 1.05".format(s),
            f"S{s} SYMBOL COLOR {cor}",
            f"S{s} SYMBOL FILL COLOR {cor}",
            f"S{s} SYMBOL FILL PATTERN 1",
            f"S{s} SYMBOL LINEWIDTH 2.0"]


def serie(g: int, i: int, legenda: str, com_simbolo: bool, barra: bool) -> list[str]:
    """Conjunto S{i} do grafico g: a curva, com todos os pontos do .dat."""
    cor = 20 + i
    c = [f"WITH G{g}",
         f"S{i} LINE COLOR {cor}",
         f"S{i} LINE LINEWIDTH 2.6",
         f'S{i} LEGEND "{legenda}"']
    c += simbolo(i, i) if com_simbolo else [f"S{i} SYMBOL 0"]
    if not barra:
        # o conjunto e do tipo xydy; sem isto o Grace desenha a barra em preto
        c.append(f"S{i} ERRORBAR OFF")
    if barra:
        c += [f"S{i} ERRORBAR COLOR {cor}",
              f"S{i} ERRORBAR SIZE 0.8",
              f"S{i} ERRORBAR LINEWIDTH 2.0",
              f"S{i} ERRORBAR RISER LINEWIDTH 2.0"]
    return c


def marcador(g: int, s: int, i: int, legenda: str) -> list[str]:
    """Conjunto S{s}: so simbolos, sobre um subconjunto esparso da serie i.

    Uma curva de 100 a 270 pontos nao aceita simbolo em cada ponto, e o
    SYMBOL SKIP do Grace conta indices, o que em eixo log amontoa os simbolos
    a direita. Entao a curva vai num conjunto sem simbolo e os simbolos vao
    noutro, com os pontos escolhidos aqui. A legenda fica com este conjunto
    e mostra so o simbolo, que e o que distingue as series.
    """
    return [f"WITH G{g}", f"S{s} LINE TYPE 0", f'S{s} LEGEND "{legenda}"'] + simbolo(s, i)


def blocos(dat: pathlib.Path) -> list[list[tuple[float, float]]]:
    """Le um .dat com blocos separados por '&'; devolve (x, y) de cada bloco."""
    out, atual = [], []
    for linha in dat.read_text(encoding="utf-8").splitlines():
        t = linha.strip()
        if t == "&":
            out.append(atual)
            atual = []
        elif t and t[0] not in "#@":
            x, y = t.split()[:2]
            atual.append((float(x), float(y)))
    if atual:
        out.append(atual)
    return out


def esparso_log(pontos: list[tuple[float, float]], i: int, n: int,
                por_decada: int = 5) -> list[tuple[float, float]]:
    """Pontos em x inteiro, ~por_decada por decada, deslocados de 1/n de passo
    por serie para que os simbolos de series sobrepostas se intercalem."""
    por_x = {int(round(x)): (x, y) for x, y in pontos}
    x_max = max(por_x)
    escolha, k = {}, 0
    while True:
        alvo = int(round(10 ** ((k + i / n) / por_decada)))
        if alvo > x_max:
            break
        if alvo in por_x:
            escolha[alvo] = por_x[alvo]
        k += 1
    return [escolha[x] for x in sorted(escolha)]


def esparso_linear(pontos: list[tuple[float, float]], i: int, n: int,
                   passo: int = 20) -> list[tuple[float, float]]:
    """Um ponto a cada `passo` indices, comecando em i*passo/n por serie."""
    inicio = (i * passo) // n
    return pontos[inicio::passo]


def escreve_marcadores(destino: pathlib.Path, series: list[list[tuple[float, float]]]) -> None:
    linhas = ["@type xy"]
    for pontos in series:
        linhas += [f"{x:g} {y:g}" for x, y in pontos] + ["&"]
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")


# pagina 900 x 400: a coordenada de vista vai de 0 a 2,25 em x e de 0 a 1 em y
VISTA = {0: (0.28, 0.30, 1.06, 0.86), 1: (1.40, 0.30, 2.18, 0.86)}


def moldura(g: int, xlab: str, ylab: str, painel: str, x: float, y: float,
            legenda: float = LEGENDA) -> list[str]:
    vx0, vy0, vx1, vy1 = VISTA[g]
    return [f"WITH G{g}", f"VIEW {vx0}, {vy0}, {vx1}, {vy1}",
            f"FRAME LINEWIDTH {GROSSURA_EIXO}",
            f'XAXIS LABEL "\\3{xlab}"',
            f"XAXIS LABEL CHAR SIZE {ROTULO}",
            f"XAXIS TICKLABEL CHAR SIZE {TIQUE}",
            f"XAXIS BAR LINEWIDTH {GROSSURA_EIXO}",
            f"XAXIS TICK MAJOR LINEWIDTH {GROSSURA_EIXO}",
            f"XAXIS TICK MINOR LINEWIDTH {GROSSURA_EIXO}",
            "XAXIS TICK MAJOR SIZE 1.4",
            "XAXIS TICK MINOR SIZE 0.8",
            f'YAXIS LABEL "\\3{ylab}"',
            f"YAXIS LABEL CHAR SIZE {ROTULO}",
            f"YAXIS TICKLABEL CHAR SIZE {TIQUE}",
            f"YAXIS BAR LINEWIDTH {GROSSURA_EIXO}",
            f"YAXIS TICK MAJOR LINEWIDTH {GROSSURA_EIXO}",
            f"YAXIS TICK MINOR LINEWIDTH {GROSSURA_EIXO}",
            "YAXIS TICK MAJOR SIZE 1.4",
            "YAXIS TICK MINOR SIZE 0.8",
            "LEGEND ON",
            "LEGEND BOX LINESTYLE 0",
            "LEGEND BOX FILL PATTERN 0",
            f"LEGEND CHAR SIZE {legenda}",
            "LEGEND LOCTYPE VIEW",
            f"LEGEND {x:.3f}, {y:.3f}",
            "WITH STRING", "STRING ON", "STRING LOCTYPE VIEW",
            f"STRING {vx0 + 0.02:.3f}, {vy1 + 0.04:.3f}",
            f"STRING CHAR SIZE {PAINEL}", "STRING FONT 2",
            f'STRING DEF "{painel}"']


def ticks_por_decada() -> list[str]:
    """Escala logaritmica com tique por decada.

    Um tique por valor da grade (dez rotulos) nao cabe no corpo 2,25 do estilo
    da casa. A Fig. 3 do artigo resolve o mesmo problema em log_10, e aqui a
    escala e a mesma; os dez pontos continuam desenhados onde estao.
    """
    return ["XAXES SCALE LOGARITHMIC",
            "XAXIS TICK MAJOR 10", "XAXIS TICK MINOR TICKS 8"]


def roda(batch: list[str], dats: list[list[pathlib.Path]], agr: pathlib.Path,
         pdf: pathlib.Path) -> None:
    """dats[g] e a lista de arquivos carregados no grafico g, na ordem."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        eps = tmp / "saida.eps"
        bat = tmp / "comandos.bat"
        bat.write_text("\n".join(batch + [f'SAVEALL "{agr}"']) + "\n", encoding="utf-8")
        cmd = ["gracebat", "-nosafe", "-noask"]
        for g, arquivos in enumerate(dats):
            for d in arquivos:
                cmd += ["-graph", str(g), str(d)]
        cmd += ["-batch", str(bat), "-hardcopy", "-hdevice", "EPS",
                "-printfile", str(eps)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not eps.exists():
            sys.exit(f"gracebat falhou:\n{r.stdout}\n{r.stderr}")
        if r.stderr.strip():
            print("  gracebat avisou:", r.stderr.strip()[:300])
        subprocess.run(["epstopdf", str(eps), f"--outfile={pdf}"], check=True)
        print(f"  {agr.relative_to(RAIZ)}  ->  {pdf.relative_to(RAIZ)}")


def figura_7(tmp: pathlib.Path) -> None:
    print("Figura 7: F_rup(T_s) por m; phi contra F/F_rup")
    b = ["PAGE SIZE 900, 400"] + cores()
    b += moldura(0, "T\\ss\\N", "F\\srup\\N", "(a)", 0.365, 0.825)
    b += ticks_por_decada()
    b += ["WORLD XMIN 1.4", "WORLD XMAX 13000", "WORLD YMIN 0", "WORLD YMAX 2950",
          "YAXIS TICK MAJOR 1000", "YAXIS TICK MINOR TICKS 1"]
    for i, m in enumerate([1, 2, 3, 5, 10]):
        b += serie(0, i, f"m = {m}", com_simbolo=True, barra=True)
    b += moldura(1, "F / F\\srup\\N", "\\xj\\f{}", "(b)", 1.48, 0.83)
    b += ["WORLD XMIN 0", "WORLD XMAX 1", "WORLD YMIN 0", "WORLD YMAX 0.26",
          "XAXIS TICK MAJOR 0.2", "XAXIS TICK MINOR TICKS 1",
          "YAXIS TICK MAJOR 0.1", "YAXIS TICK MINOR TICKS 1"]
    ts_b = [2, 32, 128, 8192]
    curvas = F7 / "figure_7b_phi_vs_u_xydy.dat"
    marcas = tmp / "figure_7b_marcadores.dat"
    escreve_marcadores(marcas, [esparso_linear(p, i, len(ts_b))
                                for i, p in enumerate(blocos(curvas))])
    for i, ts in enumerate(ts_b):
        b += serie(1, i, "", com_simbolo=False, barra=False)
        b += marcador(1, len(ts_b) + i, i, f"T\\ss\\N = {ts}")
    roda(b, [[F7 / "figure_7a_f_rup_vs_ts_xydy.dat"], [curvas, marcas]],
         F7 / "figure_7.agr", FIGS / "figure_7.pdf")


def figura_8(tmp: pathlib.Path) -> None:
    print("Figura 8: sobrevivencia das cascatas por T_s e por m")
    b = ["PAGE SIZE 900, 400"] + cores()
    for g, painel in enumerate(["(a)", "(b)"]):
        # a legenda de (a) tem subscrito, que engorda a linha: sobe mais
        lx, ly = (0.38, 0.63) if g == 0 else (1.50, 0.545)
        b += moldura(g, "s", "P(S > s)", painel, lx, ly)
        b += [f"WITH G{g}", "XAXES SCALE LOGARITHMIC", "YAXES SCALE LOGARITHMIC",
              "WORLD XMIN 0.9", "WORLD XMAX 400",
              "WORLD YMIN 2e-7", "WORLD YMAX 1.6",
              "XAXIS TICK MAJOR 10", "XAXIS TICK MINOR TICKS 8",
              "YAXIS TICK MAJOR 10", "YAXIS TICK MINOR TICKS 8",
              "YAXIS TICKLABEL FORMAT POWER", "YAXIS TICKLABEL PREC 0",
              # rotulo a cada duas decadas; o tique fica em todas
              "YAXIS TICKLABEL SKIP 1"]
    paineis = [(F8 / "figure_8a_survival_by_ts_xy.dat",
                [f"T\\ss\\N = {ts}" for ts in [2, 16, 128, 1024, 8192]]),
               (F8 / "figure_8b_survival_by_m_xy.dat",
                [f"m = {m}" for m in [1, 2, 3, 5, 10]])]
    dats = []
    for g, (curvas, legendas) in enumerate(paineis):
        marcas = tmp / f"figure_8{'ab'[g]}_marcadores.dat"
        n = len(legendas)
        escreve_marcadores(marcas, [esparso_log(p, i, n)
                                    for i, p in enumerate(blocos(curvas))])
        for i, legenda in enumerate(legendas):
            b += serie(g, i, "", com_simbolo=False, barra=False)
            b += marcador(g, n + i, i, legenda)
        dats.append([curvas, marcas])
    roda(b, dats, F8 / "figure_8.agr", FIGS / "figure_8.pdf")


if __name__ == "__main__":
    if not shutil.which("gracebat"):
        sys.exit("gracebat nao encontrado (pacote grace)")
    with tempfile.TemporaryDirectory() as tmp:
        figura_7(pathlib.Path(tmp))
        figura_8(pathlib.Path(tmp))

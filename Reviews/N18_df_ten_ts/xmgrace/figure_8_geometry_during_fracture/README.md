# Fig. 8 refeita: $\langle K\rangle/\langle K_0\rangle$ e $\langle N\rangle/\langle N_0\rangle$ contra $F$

Substitui o `figure_8.pdf` da versão dos coautores de 2026-10-01
(`Paper/authors_final_version_2026-10-01/`), que herdou dos nossos `.dat` as
letras $K$ e $N$ trocadas. A curva de $T_s = 128$ do painel (a) deles também
não correspondia ao dado. Registro: `../../../decision_log/2026-10-01_N18_notacao_K_N_trocada.md`.

| Arquivo | Conteúdo |
|:--|:--|
| `figure_8.agr` | projeto xmgrace, com os dados embutidos (abre sozinho) |
| `figure_8.pdf` | exportado do `.agr` por `gracebat` |
| `figure_8a_K_xy.dat` | painel (a): $F$, $\langle K(F)\rangle/\langle K_0\rangle$, coordenação média dos bastões ativos; um bloco `xy` por $T_s$ |
| `figure_8b_N_xy.dat` | painel (b): $F$, $\langle N(F)\rangle/\langle N_0\rangle$, segmentos por camada, o $N(i)$ de $\sigma(i) = F/N(i)$; idem |

Os blocos, nos dois `.dat` e nos conjuntos `s0`–`s7` do `.agr`, seguem a ordem
$T_s = 2, 8, 16, 32, 64, 128, 1024, 8192$. Os seis primeiros têm a cor e o
símbolo da figura dos coautores. 1024 (magenta) e 8192 (índigo) mostram a
saturação. Para voltar a seis $T_s$, basta apagar `s6` e `s7` no xmgrace, ou
rodar o script com `--ts 2 8 16 32 64 128`.

**Protocolo.** Recorte 17×17 dos cilindros periódicos, $|y| \le 100$, $m = 2$,
10 realizações × 5 sementes, semente de fratura 101. Média sobre as
realizações ainda vivas em cada $F$, desde que sejam pelo menos três. Cada
curva termina no **maior** $F_{rup}$ do $T_s$, não no médio. A legenda do
manuscrito precisa dizer isso, e também que a amostra não é o ensemble de 200
fibrilas das Figs. 6–7.

**Leitura.** $\langle N\rangle$ só cai, porque as moléculas saem: 20% em
$T_s = 2$ e 7–8% de 128 em diante. $\langle K\rangle$ dos sobreviventes sobe:
6% em $T_s = 2$, 3–4% em 8 e 16, cerca de 1% de 32 em diante. Rompem primeiro
os bastões de poucos vizinhos, cujo limiar $K\sigma_c X$ é menor. De 128 em
diante as curvas praticamente coincidem.

**Origem.** `Code/Data_analysis/build_figure8_geometry_xmgrace.py`, a partir de
`../../geometry_during_fracture_curves.csv`. Os mesmos dados em duas colunas,
um arquivo por $T_s$, estão em `../geometry_during_fracture_two_column/`.

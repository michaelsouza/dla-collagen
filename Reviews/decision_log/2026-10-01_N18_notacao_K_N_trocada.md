# N18: as letras $K$ e $N$ da geometria do tronco estavam trocadas em relação ao artigo

**Data:** 2026-10-01
**Afeta:** N18 (geometria inicial e durante a fratura); Fig. 8 da versão dos coautores de 2026-10-01 (`Paper/authors_final_version_2026-10-01/`)
**Dados:** `Reviews/N18_df_ten_ts/{trunk_geometry_by_seed,trunk_geometry_by_ts,geometry_during_fracture_curves,geometry_during_fracture_by_realization}.csv`, `Reviews/N18_df_ten_ts/xmgrace/`, `Reviews/N18_df_ten_ts/xmgrace/geometry_during_fracture_two_column/`
**Cita:** `Reviews/decision_log/2026-09-10_N18_df_dez_ts_e_escalas_mecanicas.md`

> Entrada de registro. **Append-only** — não editar.

## O erro

Em `measure_trunk_geometry_by_ts.py` e `trace_geometry_during_fracture.py`,
escritos em 2026-09-10, a coluna `K_*` guardava a ocupação média das camadas
(segmentos por camada) e `N_*` a coordenação média (partículas vizinhas por
bastão). No artigo, tanto no submetido quanto no revisado, é o contrário:
$N(i)$ é o número de segmentos na seção $i$, em $\sigma(i) = F/N(i)$, e $K$ é a
coordenação, em $\sigma^{th} = K\sigma_c X$ (no submetido, em $P_R =
(\sigma_M/K\sigma_c)^m$). O README do N18 ainda justificava o nome errado com
uma fórmula que o artigo não tem ("o $N$ de $p_i = (\sigma_i/N\sigma_c)^m$").
O motor de fratura usa as grandezas certas; o erro estava só nos nomes da
análise.

## Consequência

Os coautores receberam os `.dat` com esses nomes e montaram a Fig. 8 da versão
de 2026-10-01 lendo `K` como coordenação. O texto ficou com a física invertida.
Diz que a coordenação cai 20% em $T_s = 2$, mas o que cai é $\langle N\rangle$,
porque as moléculas saem. Diz que $\langle N\rangle$ sobe pela poda das seções
finas, mas o que sobe é $\langle K\rangle$ dos sobreviventes, porque rompem
primeiro os bastões de poucos vizinhos. Os quatro `.dat` de duas colunas
mandados no mesmo dia para a saturação ($T_s = 1024, 8192$) tinham o mesmo
erro.

## Correção

Nomes trocados para a notação do artigo nos cinco scripts de geometria
(`measure_trunk_geometry_by_ts.py`, `trace_geometry_during_fracture.py`,
`build_trunk_geometry_xmgrace.py`, `plot_trunk_geometry_figures_en.py`,
`plot_geometry_during_fracture_eight_ts.py`) e nos READMEs.

Os dois scripts de medida foram rodados de novo nesta máquina. Os troncos foram
reconstruídos do tar `periodic_cylinders_216_nb60000_10Ts_5to40seeds.tar.gz`
(sha256 conferidos) pelo estágio A de `run_local_width_fracture.sh`: 50 para a
geometria inicial e 40 para a dinâmica. Os quatro CSVs saíram **idênticos valor
a valor** aos anteriores, depois de aplicar o mapa `K_*` ↔ `N_*` (50, 10, 1573
e 400 linhas). Os `.dat` do xmgrace também saíram idênticos com as letras
permutadas: o antigo `*_K_xydy.dat` é o atual `*_N_xydy.dat`. Nenhum número
mudou.

Os `.dat` de duas colunas para os coautores estão em
`xmgrace/geometry_during_fracture_two_column/`
(`export_geometry_during_fracture_xy.py`), para os oito $T_s$.

**Não corrigido aqui:** na Fig. 8 dos coautores, a curva de $T_s = 128$ do
painel (a) sobe até 1,01, mas o dado ($N/N_0$) nunca passa de 1 e termina em
0,933. É um erro de montagem no `.agr` deles; os arquivos novos dão a curva
certa.

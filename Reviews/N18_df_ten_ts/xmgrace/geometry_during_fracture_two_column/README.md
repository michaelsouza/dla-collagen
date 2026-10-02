# Geometria durante a fratura, duas colunas, oito $T_s$ (Fig. 8 e saturação)

Pedido de coautor em 2026-10-01: os dados da Fig. 8 em duas colunas `x y`
separadas por espaço, **sem cabeçalho**, para o xmgrace ler direto, incluindo
$T_s = 1024$ e $8192$ para mostrar a saturação.

Notação do artigo:

| Arquivo | Coluna 1 | Coluna 2 |
|:--|:--|:--|
| `KxF_T_s_<TS>.dat` | $F$ | $\langle K(F)\rangle / \langle K_0\rangle$, coordenação média dos bastões ativos |
| `NxF_T_s_<TS>.dat` | $F$ | $\langle N(F)\rangle / \langle N_0\rangle$, segmentos por camada, o $N(i)$ de $\sigma(i) = F/N(i)$ |

$T_s \in \{2, 8, 16, 32, 64, 128, 1024, 8192\}$. Uma primeira versão de
1024 e 8192, mandada no mesmo dia, tinha $K$ e $N$ trocados: registro
`../../../decision_log/2026-10-01_N18_notacao_K_N_trocada.md`.

**Protocolo.** Recorte 17×17 dos cilindros periódicos, $|y| \le 100$, $m = 2$,
10 realizações × 5 sementes (900001–900005), semente de fratura 101. A amostra
é diferente do ensemble de 200 fibrilas das Figs. 6–7. A grade em $F$ vai até
o **maior** $F_{rup}$ de cada $T_s$, e cada ponto é a média sobre as realizações
ainda vivas, desde que sejam pelo menos três. Por isso a cauda é ruidosa.
Normalização: média em $F$ dividida pela média em $F = 0$, depois do filtro de
caminho de carga.

| $T_s$ | $F$ máximo | $N_0$ | $K_0$ | $N/N_0$ no fim | $K/K_0$ máximo |
|--:|--:|--:|--:|--:|--:|
| 2 | 225 | 55,4 | 27,2 | 0,798 | 1,064 |
| 8 | 517 | 78,5 | 33,3 | 0,861 | 1,034 |
| 16 | 897 | 110,6 | 37,7 | 0,904 | 1,045 |
| 32 | 1230 | 153,6 | 42,8 | 0,909 | 1,014 |
| 64 | 1634 | 182,4 | 46,1 | 0,924 | 1,014 |
| 128 | 1634 | 193,6 | 47,7 | 0,933 | 1,013 |
| 1024 | 1857 | 201,8 | 49,9 | 0,934 | 1,012 |
| 8192 | 1942 | 203,5 | 50,1 | 0,919 | 1,012 |

**Origem.** Os dados vêm de `../../geometry_during_fracture_curves.csv`
(`trace_geometry_during_fracture.py --ts 2 8 16 32 64 128 1024 8192`, nesta
máquina, 2026-10-01), por `Code/Data_analysis/export_geometry_during_fracture_xy.py`.
As linhas dos seis $T_s$ originais são idênticas às do CSV de 2026-09-10.

# Modelo com corte exponencial estendido em todos os valores de $T_s$

## Ajustes individuais e teste de uma forma conjunta

**Manuscrito:** ER12738, *Scaling behaviors in simulated collagen fibrils*  
**Spec de revisão:** GitHub issue #1  
**Ticket estatístico:** GitHub issue #5

## 1. Resultado principal

O modelo discreto com fator de potência e corte exponencial estendido,

$$
p(s\mid s\geq s_{min})=
\frac{s^{-\alpha}\exp[-(s/s_c)^\beta]}
{\sum_{k=s_{min}}^\infty k^{-\alpha}\exp[-(k/s_c)^\beta]},
$$

foi aplicado às dez condições $T_s=2,8,16,32,64,128,512,1024,4096,8192$.
O limite comum foi selecionado para esse próprio modelo, reajustando doze
parâmetros em cada candidato: $\alpha$, $\beta$ e dez escalas $s_c$. A
minimização do maior KS entre as condições forneceu

$$
s_{min}=31.
$$

Os dez ajustes individuais no suporte comum não são rejeitados pelo bootstrap
de fibrilas, com $p_{block}=0.275$--0.835. Portanto, a família com corte é uma
descrição plausível de cada condição quando $\alpha$, $\beta$ e $s_c$ podem
variar independentemente.

A hipótese mais forte de uma forma comum aos dez valores, entretanto, não é
apoiada de maneira robusta. O ajuste conjunto fornece

$$
\alpha=2.037\;[1.465,2.345],\qquad
\beta=1.085\;[0.743,1.586],
$$

e o teste simultâneo por fibrilas não rejeita o modelo
($p_{joint,block}=0.980$). Contudo, o diagnóstico condicionado a
$T_s=512$ produz $p_{block}=0.060$, com intervalo binomial de Monte Carlo
[0.028, 0.097], abaixo do limiar de 0.10. Além disso, o bootstrap paramétrico
iid rejeita decisivamente a forma conjunta, com zero excedências em 999
réplicas ($p_{joint,iid}=0.001$), e todos os dez diagnósticos iid condicionais
ficam abaixo de 0.10.

Assim, o resultado geral sustenta a **família** com corte como descrição
individual das caudas, mas não sustenta um único par $(\alpha,\beta)$ para
todo o intervalo de $T_s$. A forma comum anteriormente validada para
$T_s\geq512$ deve permanecer restrita àquele subconjunto.

## 2. Dados e inferência

A análise usa 50 geometrias independentes e 1.000 realizações de ruptura por
geometria em cada condição. Uma avalanche local é um componente espacialmente
conexo removido durante um passo de força fixa; componentes desconectados são
contados separadamente, eventos unitários são preservados no corpo da
distribuição e o passo terminal é excluído.

A fibrila é a unidade independente da inferência estrutural. Os testes
individuais e o teste conjunto usam 199 réplicas que reamostram fibrilas
inteiras. Essa resolução produz incrementos de 0.005 nos $p$-valores. O
diagnóstico iid usa 999 réplicas e é apresentado como sensibilidade, pois
eventos da mesma fibrila e da mesma trajetória de dano não são independentes.

## 3. Seleção do suporte comum

Foram avaliados todos os limites inteiros admissíveis com pelo menos 1.000
eventos em cada uma das dez caudas. Para cada candidato, o modelo conjunto foi
reajustado e a discrepância foi definida como o maior KS entre as condições,

$$
\widehat{s}_{min}=\underset{s_{min}}{\operatorname{argmin}}\;
\max_{T_s}D_{KS}(T_s,s_{min}).
$$

Os candidatos próximos ao mínimo foram:

| $s_{min}$ | maior KS |
|---:|---:|
| 29 | 0.024194 |
| 30 | 0.020050 |
| **31** | **0.017106** |
| 32 | 0.018043 |
| 33 | 0.019261 |

A seleção em 31 não é herdada da potência pura nem do ajuste de alto $T_s$.
Ela resulta da aplicação conjunta do modelo com corte às dez condições.

## 4. Ajuste conjunto

| $T_s$ | eventos $s\geq31$ | $s_c$ | KS | $p_{block}$ condicional | $p_{iid}$ condicional |
|---:|---:|---:|---:|---:|---:|
| 2 | 91.421 | 82.84 | 0.01518 | 0.520 | 0.001 |
| 8 | 79.736 | 91.20 | 0.01706 | 0.530 | 0.001 |
| 16 | 53.952 | 146.21 | 0.01228 | 0.725 | 0.001 |
| 32 | 30.687 | 160.42 | 0.01199 | 0.880 | 0.001 |
| 64 | 22.390 | 120.31 | 0.01299 | 0.550 | 0.001 |
| 128 | 16.654 | 118.81 | 0.00869 | 0.485 | 0.052 |
| 512 | 13.086 | 114.07 | 0.01711 | **0.060** | 0.001 |
| 1024 | 13.341 | 104.51 | 0.01109 | 0.325 | 0.018 |
| 4096 | 13.936 | 99.12 | 0.01002 | 0.385 | 0.019 |
| 8192 | 13.042 | 114.44 | 0.00946 | 0.515 | 0.065 |

![CCDFs e ajuste conjunto do modelo com corte para todos os valores de Ts.](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_all_ts/joint_ccdf.png)

*Figura 1 — CCDFs condicionais no suporte comum $s\geq31$. As linhas usam
$\alpha$ e $\beta$ comuns e uma escala $s_c$ específica para cada $T_s$.*

O valor conjunto alto do teste por fibrilas indica que o maior KS observado é
compatível com a variação entre geometrias. Ainda assim, o critério adotado no
projeto exige que o modelo conjunto e cada condição sejam compatíveis. O
resultado condicionado de $T_s=512$, aliado à rejeição iid, impede concluir
que os dez valores compartilham a mesma forma estatística.

## 5. Ajustes individuais

| $T_s$ | $\alpha$ | $\beta$ | $s_c$ | KS | $p_{block}$ |
|---:|---:|---:|---:|---:|---:|
| 2 | 1.597 | 0.752 | 31.00 | 0.01463 | 0.275 |
| 8 | 1.603 | 0.721 | 31.00 | 0.01595 | 0.275 |
| 16 | 2.379 | 2.623 | 263.85 | 0.00633 | 0.835 |
| 32 | 2.336 | 2.140 | 280.31 | 0.01496 | 0.485 |
| 64 | 2.413 | 2.219 | 226.04 | 0.00823 | 0.540 |
| 128 | 2.458 | 2.418 | 234.45 | 0.00418 | 0.605 |
| 512 | 2.587 | 3.211 | 255.43 | 0.00480 | 0.540 |
| 1024 | 2.456 | 2.290 | 203.59 | 0.00621 | 0.295 |
| 4096 | 2.564 | 2.485 | 216.24 | 0.00436 | 0.600 |
| 8192 | 2.468 | 2.306 | 228.70 | 0.00469 | 0.660 |

![CCDFs e ajustes individuais do modelo com corte para todos os valores de Ts.](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_all_ts/individual_ccdf.png)

*Figura 2 — Cada painel estima $\alpha$, $\beta$ e $s_c$ separadamente. Todos
os ajustes individuais são compatíveis com a variabilidade entre fibrilas.*

Os parâmetros individuais mudam substancialmente entre $T_s=8$ e 16. Nos
dois menores valores, $s_c$ atinge o limite inferior permitido, $s_c=31$, e
$\beta<1$; a partir de $T_s=16$, os ajustes apresentam $\beta>2$ e escalas
maiores. Essa mudança explica por que uma parametrização comum a todos os
valores perde adequação, embora a família flexível continue plausível.

## 6. Interpretação

O intervalo conjunto de $\beta$ inclui 1, portanto o ajuste agregado não
distingue com segurança um corte estendido de um corte exponencial simples.
Além disso, a ampla incerteza de $\alpha$ e as soluções de fronteira em baixo
$T_s$ desaconselham atribuir significado universal aos parâmetros comuns.

Os ajustes individuais mostram uma transição descritiva entre caudas de baixo
e alto $T_s$, mas não estabelecem uma relação causal com a morfologia da
fibrila. Em particular, nenhum valor de $\alpha$ deve ser identificado como
expoente crítico, evidência de SOC ou classe de compartilhamento de carga.

Para $T_s\geq512$, a análise específica permanece mais informativa: ela
seleciona $s_{min}=29$ e encontra $\alpha=2.534$, $\beta=2.547$ e
$s_c\simeq212$--243, sem rejeição por fibrilas ou iid. Misturar as seis
condições menores desloca os parâmetros para $\alpha\simeq2.04$ e
$\beta\simeq1.08$ e destrói essa compatibilidade robusta.

## 7. Formulação recomendada

> A discrete power-law factor with a stretched-exponential cutoff can
> describe each surface-relaxation condition separately above the common
> model-selected support $s_{min}=31$; none of the ten individual fits is
> rejected by fibril-block goodness-of-fit tests. A stronger joint model with
> common $\alpha=2.037$ and $\beta=1.085$ is not robust, however: the
> condition-specific block diagnostic rejects it at $T_s=512$
> ($p=0.060$), and the iid parametric sensitivity test rejects the joint form
> with zero exceedances in 999 replicates ($p=0.001$). We therefore use the
> cutoff family as a condition-wise empirical description and retain the
> common finite-scale model only for the separately validated high-$T_s$
> subset.

## 8. Evidência e reprodução

- [Varredura completa de $s_{min}$](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_all_ts/xmin_scan.csv);
- [Ajuste conjunto e bootstrap por fibrilas](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_all_ts/joint_fit.csv);
- [Réplicas do teste conjunto](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_all_ts/joint_block_bootstrap.csv);
- [Ajustes individuais](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_all_ts/individual_model_fits.csv);
- [Diagnóstico iid de 999 réplicas](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_all_ts/iid_B999/iid_joint_gof.csv).

A execução usa `run_stretched_cutoff_high_ts.py` com os dez argumentos `--ts`
e seleção automática do suporte. O diagnóstico iid usa
`run_stretched_cutoff_iid.py --xmin 31 --replicates 999 --workers 6`,
inicializado pelo `joint_fit.csv` observado para evitar um mínimo local
espúrio na otimização de doze parâmetros.

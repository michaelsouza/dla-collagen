# Registro de evidências para a resposta sobre avalanches

## Status deste documento

Este é o registro de trabalho para preparar as respostas aos comentários
R1-2, R1-3, R2-2, R2-3 e R2-4. Ele consolida decisões, resultados e caminhos
dos artefatos. A resposta unificada pronta para revisão autoral está em
`UNIFIED_REFEREE_RESPONSE_AVALANCHES.md`; este registro não substitui o texto
revisado do manuscrito.

## Decisões autorais congeladas

1. **Tamanho do ensemble.** A análise revisada usa 50 geometrias de fibrila
   por $T_s$, cinco vezes as 10 fibrilas mencionadas no relatório do Referee 1.
   Cada geometria possui 1000 realizações estocásticas de ruptura, totalizando
   50.000 realizações por $T_s$ e 500.000 realizações nas dez condições. Não
   será feita uma curva adicional de sensibilidade com subconjuntos de 10, 20,
   30 e 40 fibrilas. A ampliação do ensemble será apresentada como a melhor
   cobertura disponível, e não como prova formal de convergência no número de
   geometrias.
2. **Módulo de Weibull.** Não serão executadas novas simulações em outros
   módulos devido ao custo computacional. Todos os dados analisados possuem
   $m=2$. As conclusões serão explicitamente limitadas ao modelo com $m=2$ e
   não será reivindicada robustez em relação ao módulo de Weibull.
3. **Objeto estatístico.** O objeto principal é o tamanho inteiro dos clusters
   locais conectados. Os ajustes de distribuição usam eventos não triviais
   $s\geq2$. Os singletons são preservados e usados para descrever a composição
   da população completa.
4. **Binagem.** Estimação, KS, bootstrap e comparações usam os valores
   discretos não binados. Gráficos binados não serão usados como evidência de
   lei de potência nem para estimar expoentes.
5. **Interpretação.** SOC, comportamento *scale-free*, classe de universalidade
   e crossover LLS--ELS não serão atribuídos aos resultados.

## Auditoria dos dados

O manifesto de preparação registra, para cada um dos dez $T_s$:

- 50 arquivos correspondentes a 50 geometrias;
- 1000 realizações por geometria;
- 50.000 realizações de ruptura;
- módulo de Weibull exclusivamente $m=2$;
- hashes SHA-256 dos consolidados;
- contagens separadas de $s=1$ e $s\geq2$.

No total, a análise contém 301.039.035 avalanches locais com $s\geq1$, das
quais 28.785.331 possuem $s\geq2$. A fonte auditável dessas contagens é:

- `Data_fibrils/Avalanche_force_grouped/local_avalanche_sizes/manifest.json`.

## Decisão científica principal

### Lei de potência pura

A hipótese discreta

\[
p(s)\propto s^{-\alpha},\qquad s\geq s_{\min},
\]

foi ajustada por MLE discreta exata. $s_{\min}$ foi escolhido por minimização
do KS, com pelo menos 1000 eventos na cauda. O teste semiparamétrico de Clauset
usou 2500 réplicas por $T_s$, reestimando $s_{\min}$ e $\alpha$ em cada
réplica.

| $T_s$ | $s_{\min}$ | $\hat\alpha$ | eventos na cauda | fração da população $s\geq2$ | $p_{\rm PL}$ |
|---:|---:|---:|---:|---:|---:|
| 2 | 3 | 1.798 | 1.011.943 | 0.62894 | <0.0004 |
| 8 | 4 | 1.883 | 871.697 | 0.37262 | <0.0004 |
| 16 | 787 | 11.822 | 6.430 | 0.00245 | <0.0004 |
| 32 | 1177 | 37.282 | 1.256 | 0.00043 | <0.0004 |
| 64 | 1411 | 41.048 | 1.009 | 0.00031 | 0.0248 |
| 128 | 1490 | 38.502 | 1.684 | 0.00050 | <0.0004 |
| 512 | 1593 | 39.535 | 1.941 | 0.00061 | <0.0004 |
| 1024 | 1605 | 50.498 | 1.009 | 0.00032 | 0.0012 |
| 4096 | 1618 | 39.908 | 1.623 | 0.00051 | <0.0004 |
| 8192 | 1659 | 42.125 | 2.097 | 0.00067 | <0.0004 |

Pelo critério conservador $p\leq0.1$, a potência pura é rejeitada em todas as
condições. Para $T_s\geq16$, a cauda selecionada contém no máximo 0,245% dos
eventos e cobre no máximo 0,160 década. Os valores de $\hat\alpha$ são
parâmetros de modelos rejeitados e não podem ser usados como expoentes físicos.

Evidência:

- `observed_power_law_fits.csv`;
- `power_law_gof_B2500.csv`;
- `power_law_gof_B2500_replicates.csv`.

### Modelos concorrentes nas mesmas caudas

Potência com corte exponencial, lognormal discreta e exponencial discreta foram
comparadas usando exatamente os mesmos eventos $s\geq\hat s_{\min}$. A potência
com corte possui o menor BIC, mas a lognormal é praticamente indistinguível em
várias condições de alto $T_s$. O bootstrap absoluto mostra:

- potência com corte e lognormal plausíveis somente em algumas caudas estreitas
  ($T_s=32,128,512,1024,8192$);
- resultado limítrofe em $T_s=64$;
- rejeição das duas famílias em $T_s=2,16,4096$ e rejeição da potência com corte
  também em $T_s=8$;
- nenhuma alternativa validada em todos os $T_s$.

Para $T_s\geq16$, o parâmetro $\alpha$ da potência com corte é negativo. Nessa
parametrização, a distribuição cresce em direção a uma escala característica
antes do corte; ela não representa um trecho decrescente de scaling.

Evidência:

- `model_fits.csv`;
- `model_comparisons.csv`;
- `alternative_model_gof_B2500.csv`;
- `alternative_model_gof_B2500_replicates.csv`.

### Distribuição completa

As PMFs e CCDFs exatas de todos os tamanhos mostram que a evolução com $T_s$
não é uma simples translação da distribuição:

- $P(s=1)$ cresce de 0,7650 para 0,9218;
- entre os eventos $s\geq2$, q90 cai de 27 para 5;
- q99 cresce de 270 para aproximadamente 1300;
- os eventos intermediários perdem peso;
- eventos pequenos coexistem com uma população rara de eventos muito grandes;
- as distribuições agregadas tornam-se muito semelhantes para $T_s\geq512$.

Entre todos os pares com $T_s\geq512$, a distância de Jensen--Shannon é no
máximo 0,027 para a distribuição condicional $s\geq2$ e 0,008 para a população
incluindo singletons. Isso sustenta uma descrição empírica de mudança forte em
baixos/intermediários $T_s$ seguida de estabilização aproximada em altos $T_s$.

Evidência:

- `full_distribution_summary.csv`;
- `full_distribution_pmf.csv`;
- `full_distribution_pairwise_distances.csv`;
- `full_distribution_overview.png`;
- `full_distribution_js_heatmap.png`.

### Teste de mistura na distribuição completa $s\geq2$

Foi ajustada uma mistura de cinco parâmetros formada por um componente
decrescente $s^{-\alpha}e^{-\lambda s}$ e uma lognormal discreta para o grupo
extremo. A mistura melhora substancialmente o BIC em relação a uma única
lognormal e recupera visualmente as duas escalas, mas é rejeitada em todos os
$T_s$.

Foram geradas 100 réplicas por condição e todos os cinco parâmetros foram
reestimados. Houve zero excedências em cada $T_s$. O limite binomial unilateral
exato de 95% é $p<0.0296$, abaixo do critério 0,1. O KS observado foi de 50 a
108 vezes maior que o maior KS sintético.

Evidência:

- `complete_mixture_gof_B100.csv`;
- `complete_mixture_gof_B100_replicates.csv`;
- `complete_mixture_comparison.png`;
- `complete_mixture_parameters.png`.

## Matriz para a resposta aos referees

### R1-2 e R2-4: potência, scale-free e SOC

**Decisão:** concordar com os referees e substituir a afirmação original.

**Resposta sustentada pelos dados:** a análise não binada e discreta rejeita a
potência pura em todos os $T_s$. Nenhuma família alternativa fornece uma forma
universal. Como o sistema é externamente dirigido, irreversível e sem cura, as
estatísticas não são interpretadas como SOC. A terminologia permitida é
“estatísticas de clusters locais de avalanche em fratura desordenada dirigida”.

**Mudanças necessárias no manuscrito:** substituir a atual Fig. 10 e remover
os ajustes lineares binados e a curva de $\gamma$. Inserir CCDFs não binadas,
resultados de GOF e a descrição empírica de duas escalas.

### R1-3: $\gamma>5/2$, tamanho do ensemble e Weibull

**Decisão sobre o expoente:** não comparar nenhum dos $\hat\alpha$ ou slopes
binados com $5/2$. A potência foi rejeitada; portanto, não há expoente crítico
validado nem evidência de crossover de universalidade.

**Tamanho do ensemble:** informar que a reanálise usa 50 geometrias por $T_s$,
cinco vezes a amostra original, com 1000 realizações por geometria. Não alegar
que foi realizado um estudo formal de convergência em tamanho de ensemble.

**Weibull:** declarar que todas as simulações usam $m=2$, que novas simulações
seriam computacionalmente onerosas e que nenhuma robustez em $m$ é reivindicada.
As conclusões são condicionais ao modelo com $m=2$.

### R2-2: natureza do compartilhamento de carga

**Decisão:** o modelo não será classificado como ELS ou LLS convencional. A
carga é uniforme dentro de cada seção transversal afetada; $N(i)$ varia ao
longo do eixo; moléculas diferentes atravessam conjuntos distintos de seções;
e a resistência local depende da coordenação $K$. Não existe kernel elástico
de redistribuição dependente da distância. Como não há expoente validado, as
distribuições de avalanche não serão usadas para atribuir uma classe de load
sharing.

**Mudança necessária na carta:** criar uma resposta específica para R2-2, hoje
ausente no documento de resposta.

### R2-3: definição das avalanches

**Decisão:** usar consistentemente “avalanche local” ou “cluster local de
avalanche”. Cada evento é um componente conectado das moléculas removidas no
mesmo nível do drive; componentes desconectados são eventos locais distintos.
Essa classificação mede organização espacial do dano e não implica LLS.

### R1-5: relação entre estrutura e estatísticas de ruptura

**Decisão pendente de redação, não de nova distribuição:** a associação
$D_f$--$\gamma$ deve ser eliminada, porque $\gamma$ não foi validado. Se a
relação estrutura--avalanche for mantida, ela deve usar estatísticas empíricas
da distribuição, como $P(s=1)$, q90, q99 e frações de eventos extremos. A
evolução paralela dessas quantidades com $T_s$ é correlação sob um controle
comum, não relação causal.

## Análises adicionais executadas somente com tamanhos de avalanche

Todas as análises abaixo usam a distribuição empírica exata e não binada dos
eventos $s\geq2$. Elas não usam força, outra métrica mecânica ou novas
simulações.

### Polarização e concentração

Uma partição empírica em duas escalas foi obtida minimizando a soma dos
quadrados dentro de dois grupos contíguos em $\log s$, ponderada pelas
frequências exatas. O separador cresce de $9|10$ em $T_s=2$ para $51|52$ em
altos $T_s$. A fração de eventos na escala superior cai de 23,12% para cerca
de 1,77%, enquanto sua mediana cresce de 23 para aproximadamente 1345. A média
geométrica do grupo pequeno permanece próxima de 2,6--3,0. A partição explica
64--74% da variância de $\log s$, corroborando a separação visual sem impor
uma família de probabilidades.

A concentração da soma dos tamanhos também aumenta fortemente. Os maiores
10% dos eventos respondem por 69,63% da soma em $T_s=2$ e por 91,48% em
$T_s=8192$. Para os maiores 1%, a participação passa de 20,64% para 59,16%,
atingindo 61,17% em $T_s=128$. Os maiores 0,1% respondem por 2,63% em
$T_s=2$ e aproximadamente 6,6--7,0% para $T_s\geq64$. As curvas de Lorenz
registram a mesma concentração crescente.

### Escala característica e estabilização em alto $T_s$

A escala não paramétrica $\langle s^2\rangle/\langle s\rangle$ cresce de
140,6 em $T_s=2$ para 1063,8 em $T_s=128$ e varia somente entre 1178,2 e
1214,9 para $T_s\geq512$. A mediana do grupo superior passa de 23 para 1204
até $T_s=128$ e permanece entre 1322 e 1356 para $T_s\geq512$.

Após normalizar a escala superior por sua própria mediana, a distância média
absoluta entre log-quantis de todos os pares com $T_s\geq512$ fica entre
0,0115 e 0,0234. Isso sustenta um colapso empírico aproximado da forma do grupo
superior em alto $T_s$. É uma descrição de estabilização, não um teste de
universalidade, expoente crítico ou transição de fase.

### Cruzamentos e agrupamento descritivo

As CCDFs consecutivas apresentam um cruzamento principal que se desloca de
$s\simeq201$ ($T_s:2\to8$) para 285, 480, 685 e 829 até
$T_s:64\to128$. Isso formaliza a transferência de probabilidade dos tamanhos
intermediários para tamanhos superiores. Acima de $T_s=512$, as diferenças
entre CCDFs são pequenas e produzem vários cruzamentos locais; eles não devem
ser interpretados individualmente.

O agrupamento hierárquico médio da distância de Jensen--Shannon seleciona,
descritivamente, três grupos: $\{2\}$, $\{8,16,32\}$ e
$\{64,128,512,1024,4096,8192\}$. A evidência para três grupos é fraca em
relação a dois: a silhueta média é 0,484 para três e 0,476 para dois. Portanto,
o agrupamento serve apenas como resumo da evolução; o resultado mais robusto é
a grande semelhança das quatro distribuições com $T_s\geq512$.

Evidência:

- `avalanche_behavior_summary.csv`;
- `avalanche_lorenz.csv`;
- `avalanche_ccdf_crossings.csv`;
- `avalanche_large_scale_distances.csv`;
- `avalanche_regime_clustering.csv` e `avalanche_regime_linkage.csv`;
- `avalanche_behavior_metrics.png`;
- `avalanche_large_scale_collapse.png`;
- `avalanche_ccdf_crossings.png`;
- `avalanche_regime_dendrogram.png`.

### Interpretações não recomendadas

- testar sucessivamente distribuições mais flexíveis até alguma não ser
  rejeitada;
- recuperar slopes de gráficos binados;
- interpretar parâmetros de modelos rejeitados como expoentes físicos;
- alegar uma transição crítica apenas porque algumas métricas atingem plateau;
- alegar robustez ao tamanho do ensemble ou a $m$ sem executar esses testes.

## Redação-base da conclusão estatística

> We reanalyzed the raw integer sizes of local avalanche clusters without
> logarithmic binning, using exact discrete maximum likelihood, objective
> lower-cutoff selection, semiparametric goodness-of-fit tests, and comparisons
> with cutoff-power-law, lognormal, and exponential alternatives. The pure
> power-law hypothesis was rejected for every surface-relaxation condition.
> The complete distributions instead show a finite, two-scale structure: a
> dominant population of small local events coexists with a rare population of
> much larger clusters, while intermediate sizes lose weight as surface
> relaxation increases. No tested parametric family provides an adequate
> universal description across all conditions. We therefore do not report a
> critical avalanche exponent or interpret the results in terms of
> self-organized criticality, scale-free behavior, or a load-sharing
> universality class. These conclusions apply to the present model with
> Weibull modulus $m=2$.

## Estado e próximos passos de integração

As análises adicionais baseadas apenas nos tamanhos foram executadas, e a
resposta estatística unificada está em
`UNIFIED_REFEREE_RESPONSE_AVALANCHES.md`. Após a revisão e aprovação autoral
dessa interpretação, ainda será necessário:

1. substituir a Fig. 10 e sua legenda pelas figuras empíricas selecionadas;
2. substituir a seção de resultados que ainda apresenta $\gamma$ binado;
3. incorporar o texto aprovado na carta oficial e sincronizar os arquivos TeX
   e PDF;
4. registrar os resultados e a decisão final na Issue #5;
5. criar um checkpoint Git reproduzível para uso em outro computador.

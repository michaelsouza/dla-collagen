# Análise agregada de avalanches locais pelo protocolo de Clauset

O registro de trabalho que conecta esta análise aos comentários dos referees,
às decisões autorais e às mudanças ainda necessárias está em
`REFEREE_RESPONSE_EVIDENCE.md`.

## Escopo

Esta análise foi implementada do zero em
`Code/Data_analysis/clauset_pooled/`. Ela não importa os códigos estatísticos
anteriores do repositório.

A população analisada é formada por todas as avalanches locais agregadas em
cada valor de $T_s$, com as seguintes regras:

- eventos singleton são excluídos: $s \geq 2$;
- etapas terminais são incluídas, pois estão presentes nos arquivos preparados;
- todos os eventos do mesmo $T_s$ têm o mesmo peso;
- não foi feita análise individual, reponderação ou bootstrap por fibrila.

## Método

Para cada $T_s$:

1. α foi estimado pela máxima verossimilhança discreta exata com
   normalização pela zeta de Hurwitz;
2. $s_{\min}$ foi escolhido pela minimização do KS discreto, exigindo pelo
   menos 1000 eventos na cauda;
3. a plausibilidade da potência pura foi testada com 2500 réplicas Monte Carlo
   semiparamétricas, reestimando α e $s_{\min}$ em cada réplica;
4. potência pura, potência com corte exponencial, lognormal discreta e
   exponencial discreta foram ajustadas aos mesmos dados
   $s \geq \hat{s}_{\min}$;
5. potência versus lognormal e exponencial foi comparada por Vuong;
6. potência versus potência com corte foi comparada pelo limite qui-quadrado
   de Wilks com um grau de liberdade;
7. a qualidade absoluta das três alternativas foi testada por bootstrap
   paramétrico com 2500 réplicas, mantendo o suporte
   $s \geq \hat{s}_{\min}$ e reestimando todos os parâmetros em cada réplica.

## Resultado da potência pura

| $T_s$ | $s_{\min}$ | α | $n_{tail}$ | fração da cauda | KS | $p_{Clauset}$ |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 3 | 1.7982 | 1,011,943 | 0.62894 | 0.02418 | <0.0004 |
| 8 | 4 | 1.8830 | 871,697 | 0.37262 | 0.03096 | <0.0004 |
| 16 | 787 | 11.8224 | 6,430 | 0.00245 | 0.04965 | <0.0004 |
| 32 | 1177 | 37.2820 | 1,256 | 0.00043 | 0.04015 | <0.0004 |
| 64 | 1411 | 41.0475 | 1,009 | 0.00031 | 0.03195 | 0.0248 |
| 128 | 1490 | 38.5022 | 1,684 | 0.00050 | 0.05758 | <0.0004 |
| 512 | 1593 | 39.5351 | 1,941 | 0.00061 | 0.04857 | <0.0004 |
| 1024 | 1605 | 50.4984 | 1,009 | 0.00032 | 0.04473 | 0.0012 |
| 4096 | 1618 | 39.9076 | 1,623 | 0.00051 | 0.04464 | <0.0004 |
| 8192 | 1659 | 42.1248 | 2,097 | 0.00067 | 0.05452 | <0.0004 |

Quando nenhuma das 2500 réplicas excedeu o KS observado, a tabela registra o
limite de resolução $p<1/2500=0.0004$, em vez de interpretar o valor Monte
Carlo zero como uma probabilidade exata.

Pelo limiar conservador $p \leq 0.1$, a potência pura é rejeitada em todos os
valores de $T_s$. Para $T_s \geq 16$, além da rejeição, a cauda selecionada é
uma fração muito pequena dos dados e cobre no máximo 0.160 década. Os expoentes
altos dessas caudas estreitas não devem ser interpretados como um regime de
escala.

## Modelos concorrentes

A potência com corte possui o menor BIC em todos os valores de $T_s$. Para
$T_s=2,8,16$, sua vantagem é clara. Para $T_s \geq 32$, a diferença de BIC
entre potência com corte e lognormal é menor que 0.5; portanto, essas duas
famílias são praticamente indistinguíveis pelo BIC nessas condições.

Para $T_s \geq 16$, o expoente ajustado da família com corte é negativo. Nessa
parametrização, o modelo descreve uma distribuição concentrada em torno de uma
escala característica antes do corte exponencial, e não uma região decrescente
de lei de potência. O nome da família não deve ser confundido com evidência de
*scaling*.

O teste de Wilks favorece a potência com corte sobre a potência pura em todas
as condições. Vuong favorece a lognormal sobre a potência pura em todos os
valores de $T_s$. A exponencial simples é desfavorecida em $T_s=2,8$, mas
favorecida sobre a potência pura para $T_s \geq 16$.

## Qualidade absoluta dos modelos concorrentes

| $T_s$ | potência com corte | lognormal | exponencial |
|---:|---:|---:|---:|
| 2 | <0.0004 | <0.0004 | <0.0004 |
| 8 | <0.0004 | não testável¹ | <0.0004 |
| 16 | <0.0004 | <0.0004 | <0.0004 |
| 32 | 0.4540 | 0.4220 | 0.0056 |
| 64 | 0.1060 | 0.0992 | 0.1376 |
| 128 | 0.7832 | 0.6664 | <0.0004 |
| 512 | 0.3360 | 0.2276 | <0.0004 |
| 1024 | 0.9088 | 0.8508 | 0.0028 |
| 4096 | 0.0600 | 0.0260 | 0.0004 |
| 8192 | 0.2836 | 0.1324 | <0.0004 |

Os valores são os $p$-valores do bootstrap paramétrico. Pelo critério de
Clauset, $p \leq 0.1$ rejeita o modelo. Em $T_s=64$, os resultados ficam no
limiar: os erros-padrão Monte Carlo são aproximadamente 0.006, de modo que não
há separação robusta entre aceitação e rejeição nesse ponto.

¹ Em $T_s=8$, a verossimilhança lognormal tende ao limite
$\mu\to-\infty$, $\sigma\to\infty$; portanto, não existe uma MLE finita
identificável para parametrizar um bootstrap válido. O caso foi registrado
como não testável, sem fabricar um $p$-valor.

Os testes absolutos mudam a leitura das comparações relativas. Não há uma
única família candidata que descreva todas as condições. A potência com corte
e a lognormal são descrições plausíveis das caudas condicionais em
$T_s=32,128,512,1024,8192$; em $T_s=64$, o resultado é limítrofe. Ambas são
rejeitadas em $T_s=2,16,4096$, e a potência com corte também em $T_s=8$.
A exponencial simples só não é rejeitada em $T_s=64$.

Mesmo onde a potência com corte passa no teste, para $T_s\geq16$ seu expoente
é negativo e o suporte testado é uma cauda muito estreita selecionada pelo
ajuste da potência pura. Assim, o resultado indica uma distribuição com escala
característica e corte, não evidência de uma região de lei de potência.

## Distribuição completa dos tamanhos

A distribuição empírica completa foi calculada exatamente, sem amostragem, em
duas populações: todos os eventos locais ($s\geq1$) e os eventos não triviais
condicionados a $s\geq2$. Esta etapa usa somente os tamanhos de avalanche; não
condiciona por força e não utiliza outras métricas da fibrila.

| $T_s$ | eventos | $P(s=1)$ | média, $s\geq2$ | q90, $s\geq2$ | q99, $s\geq2$ | q99.9, $s\geq2$ |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 6,847,150 | 0.7650 | 15.48 | 27 | 270 | 376 |
| 8 | 12,940,682 | 0.8192 | 15.00 | 15 | 424 | 604 |
| 16 | 18,910,218 | 0.8610 | 17.14 | 10 | 625 | 864 |
| 32 | 26,985,855 | 0.8910 | 19.14 | 7 | 861 | 1135 |
| 64 | 35,512,519 | 0.9085 | 20.84 | 6 | 1077 | 1353 |
| 128 | 39,454,004 | 0.9149 | 21.51 | 5 | 1165 | 1450 |
| 512 | 39,910,756 | 0.9205 | 24.10 | 5 | 1284 | 1565 |
| 1024 | 40,352,406 | 0.9209 | 24.09 | 5 | 1298 | 1546 |
| 4096 | 40,342,638 | 0.9211 | 24.45 | 5 | 1321 | 1580 |
| 8192 | 39,782,807 | 0.9218 | 24.96 | 5 | 1311 | 1632 |

A evolução não é um simples deslocamento de toda a distribuição para tamanhos
maiores ou menores. O percentil 90 dos eventos não triviais cai de 27 para 5,
enquanto o percentil 99 cresce de 270 para aproximadamente 1300. Ao mesmo
tempo, $P(s=1)$ cresce de 0.765 para 0.922. Portanto, o aumento de $T_s$ produz
uma distribuição progressivamente mais polarizada: predominam avalanches
unitárias ou pequenas, coexistindo com uma população rara de eventos muito
grandes, e os tamanhos intermediários perdem peso.

Em termos da população completa, a classe $10\leq s<100$ cai de 4.63% em
$T_s=2$ para 0.21% em $T_s=8192$; a classe $100\leq s<1000$ cai de 0.80% para
0.008%. Em contraste, a fração $s\geq1000$, inexistente em $T_s=2$, estabiliza
em aproximadamente 0.12% a partir de $T_s=64$. A CCDF mostra essa separação
como um patamar entre o corpo de eventos pequenos e o grupo de eventos
extremos. Isso é evidência empírica de duas escalas, mas, sem usar informação
adicional, não identifica a origem dinâmica do segundo grupo.

As distâncias entre distribuições confirmam uma aproximação gradual a um
plateau. Para os eventos $s\geq2$, a distância de Jensen–Shannon entre pares
consecutivos cai de 0.153 em $T_s=2\rightarrow8$ para 0.017 em
$T_s=512\rightarrow1024$. Entre todos os pares com $T_s\geq512$, essa distância
é no máximo 0.027; incluindo os singletons, é no máximo 0.008. Assim, os dados
agregados sustentam uma mudança forte em baixos e intermediários $T_s$, seguida
por um regime empiricamente estável a partir de aproximadamente $T_s=512$.

O fracasso dos modelos de cauda em $T_s=4096$ não corresponde a uma anomalia
da distribuição completa: sua distância às distribuições vizinhas é pequena.
É uma inadequação paramétrica localizada na cauda estreita, e não uma mudança
global de comportamento.

## Teste de uma distribuição completa de dois componentes

A forma polarizada motivou um teste paramétrico adicional sobre **todos** os
eventos $s\geq2$. O modelo combina:

\[
p(s)=w\,C_1s^{-\alpha}e^{-\lambda(s-2)}
 +(1-w)\,p_{\mathrm{LN,disc}}(s;\mu,\sigma),
\]

onde o primeiro termo é obrigado a ser monotonicamente decrescente e representa
o corpo de eventos pequenos, enquanto a lognormal discreta representa o grupo
raro de eventos grandes. Os cinco parâmetros foram ajustados conjuntamente por
MLE discreta. Uma mistura de duas lognormais também foi examinada durante a
validação, mas o componente pequeno correu para uma MLE não finita; por isso
essa parametrização não foi promovida a teste final.

| $T_s$ | $\alpha$ pequeno | $\lambda$ | peso grande | mediana grande | KS | bootstrap |
|---:|---:|---:|---:|---:|---:|:---|
| 2 | 1.813 | 0.003971 | 0.0230 | 246 | 0.0341 | 0/100 |
| 8 | 2.171 | 0.000715 | 0.0190 | 420 | 0.0386 | 0/100 |
| 16 | 2.419 | 0 | 0.0184 | 631 | 0.0426 | 0/100 |
| 32 | 2.723 | 0 | 0.0168 | 882 | 0.0402 | 0/100 |
| 64 | 2.964 | 0 | 0.0153 | 1120 | 0.0375 | 0/100 |
| 128 | 3.102 | 0 | 0.0149 | 1219 | 0.0325 | 0/100 |
| 512 | 3.148 | 0 | 0.0157 | 1321 | 0.0325 | 0/100 |
| 1024 | 3.145 | 0 | 0.0156 | 1332 | 0.0320 | 0/100 |
| 4096 | 3.132 | 0 | 0.0157 | 1348 | 0.0328 | 0/100 |
| 8192 | 3.184 | 0 | 0.0161 | 1348 | 0.0311 | 0/100 |

A mistura tem BIC muito menor que uma lognormal única em todos os $T_s$ e
recupera descritivamente a separação entre as duas escalas. Isso não basta para
validá-la. No bootstrap paramétrico, os cinco parâmetros foram reajustados em
cada réplica. Nenhuma das 1000 réplicas, 100 por $T_s$, atingiu o KS observado.
Com zero excedências em 100 ensaios, o limite binomial unilateral exato de 95%
é $p<0.0296$, abaixo do critério $p=0.1$; portanto, a mistura é rejeitada em
todos os $T_s$. O KS observado foi de 50 a 108 vezes maior que o maior KS
sintético em cada condição, tornando a decisão distante do limiar.

Os valores de $\alpha$ da tabela são parâmetros **descritivos de um componente
de um modelo global rejeitado**. Eles não validam uma lei de potência, não são
expoentes universais de avalanche e não devem substituir os expoentes também
rejeitados do ajuste de Clauset. O teste reforça duas conclusões mais limitadas:

1. um modelo de componente único é inadequado para a distribuição completa;
2. a separação em um corpo pequeno e um grupo extremo é real, mas suas formas
   não são descritas exatamente por esta mistura paramétrica simples.

Assim, a descrição defensável permanece empírica: distribuição discreta de
duas escalas, com suporte finito e forte polarização, sem uma família
paramétrica universal validada para todos os $T_s$.

Nenhum desses resultados estabelece criticalidade auto-organizada,
comportamento *scale-free*, universalidade ou um mecanismo de compartilhamento
de carga.

## Comportamento empírico sem impor uma distribuição

Como nenhuma família paramétrica descreve a distribuição completa em todos os
$T_s$, foram calculados diagnósticos exatos e não paramétricos para $s\geq2$.
Uma partição ótima em dois intervalos contíguos de $\log s$ separa uma escala
pequena de uma escala superior. O limiar passa de $9|10$ em $T_s=2$ para
$51|52$ em altos $T_s$. A fração na escala superior cai de 23,12% para cerca
de 1,77%, enquanto sua mediana cresce de 23 para aproximadamente 1345.

A soma dos tamanhos fica progressivamente concentrada nos maiores eventos. A
participação dos maiores 10% cresce de 69,63% para 91,48%; para os maiores 1%,
de 20,64% para cerca de 59%. Em paralelo, a escala característica
$\langle s^2\rangle/\langle s\rangle$ cresce de 140,6 para aproximadamente
1200 e atinge um plateau empírico em altos $T_s$.

Para $T_s\geq512$, a mediana da escala superior fica entre 1322 e 1356. Após
normalização por essa mediana, a distância média absoluta entre log-quantis é
no máximo 0,0234 entre qualquer par dessas quatro condições. Esse colapso
aproximado e as pequenas distâncias de Jensen--Shannon sustentam estabilização
empírica da forma, não universalidade ou transição crítica.

Um agrupamento hierárquico descritivo prefere três grupos
$\{2\}$, $\{8,16,32\}$ e $\{64,128,512,1024,4096,8192\}$, mas a silhueta
para três grupos (0,484) é apenas ligeiramente maior que para dois (0,476).
Assim, os grupos não devem ser tratados como fases. A conclusão defensável é
uma evolução contínua para maior polarização, seguida de estabilização
aproximada em $T_s\geq512$.

## Artefatos

- `observed_power_law_fits.csv`: MLE, cutoff e metadados das caudas;
- `power_law_gof_B2500.csv`: resumo do teste semiparamétrico;
- `power_law_gof_B2500_replicates.csv`: KS e cutoff das 25.000 réplicas;
- `model_fits.csv`: parâmetros, log-verossimilhança, KS, AIC e BIC;
- `model_comparisons.csv`: testes de Vuong e Wilks;
- `alternative_model_gof_B2500.csv`: testes absolutos das alternativas;
- `alternative_model_gof_B2500_replicates.csv`: KS das 72.500 réplicas
  paramétricas válidas;
- `full_distribution_summary.csv`: estatísticas exatas das populações
  $s\geq1$ e $s\geq2$;
- `full_distribution_pmf.csv`: histograma, PMF e CCDF empíricos completos;
- `full_distribution_pairwise_distances.csv`: distâncias de variação total,
  Jensen–Shannon, KS e Wasserstein entre todos os pares de $T_s$;
- `full_distribution_overview.png` e `.pdf`: CCDFs, quantis e composição por
  tamanho;
- `full_distribution_js_heatmap.png` e `.pdf`: mapa de distâncias entre as
  distribuições não triviais;
- `complete_mixture_gof_B100.csv`: parâmetros e teste absoluto da mistura na
  distribuição completa $s\geq2$;
- `complete_mixture_gof_B100_replicates.csv`: KS das 1000 réplicas da mistura;
- `complete_mixture_comparison.png` e `.pdf`: CCDF empírica, mistura e seus
  dois componentes;
- `complete_mixture_parameters.png` e `.pdf`: evolução descritiva dos cinco
  parâmetros da mistura;
- `avalanche_behavior_summary.csv`: concentração, partição em duas escalas e
  escalas características não paramétricas;
- `avalanche_lorenz.csv`: curvas de Lorenz exatas;
- `avalanche_ccdf_crossings.csv`: cruzamentos entre CCDFs consecutivas;
- `avalanche_large_scale_distances.csv`: distâncias entre log-quantis da
  escala superior normalizada;
- `avalanche_regime_clustering.csv` e `avalanche_regime_linkage.csv`:
  agrupamento descritivo por distância de Jensen--Shannon;
- `avalanche_behavior_metrics.png`, `avalanche_large_scale_collapse.png`,
  `avalanche_ccdf_crossings.png` e `avalanche_regime_dendrogram.png`: figuras
  dos diagnósticos não paramétricos (também disponíveis em PDF);
- `pooled_model_ccdf_comparison.png` e `.pdf`: CCDF empírica completa com os
  modelos de cauda sobrepostos;
- arquivos `*_run.json`: escopo, sementes e caminhos de entrada.

## Reprodução

```bash
python -m Code.Data_analysis.clauset_pooled.run_observed \
  Data_fibrils/Avalanche_force_grouped/local_avalanche_sizes \
  Reviews/Issue5_clauset_pooled_from_scratch --minimum-tail 1000

python -m Code.Data_analysis.clauset_pooled.run_gof \
  Data_fibrils/Avalanche_force_grouped/local_avalanche_sizes \
  Reviews/Issue5_clauset_pooled_from_scratch \
  --minimum-tail 1000 --replicates 2500 --workers 4 \
  --tag power_law_gof_B2500

python -m Code.Data_analysis.clauset_pooled.run_models \
  Data_fibrils/Avalanche_force_grouped/local_avalanche_sizes \
  Reviews/Issue5_clauset_pooled_from_scratch --minimum-tail 1000

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python -m Code.Data_analysis.clauset_pooled.run_alternative_gof \
  Data_fibrils/Avalanche_force_grouped/local_avalanche_sizes \
  Reviews/Issue5_clauset_pooled_from_scratch \
  --minimum-tail 1000 --replicates 2500 --workers 2 \
  --tag alternative_model_gof_B2500 --resume

python -m Code.Data_analysis.clauset_pooled.run_full_distribution \
  Data_fibrils/Avalanche_force_grouped/local_avalanche_sizes \
  Reviews/Issue5_clauset_pooled_from_scratch

MPLBACKEND=Agg \
python -m Code.Data_analysis.clauset_pooled.plot_full_distribution \
  Reviews/Issue5_clauset_pooled_from_scratch

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python -m Code.Data_analysis.clauset_pooled.run_complete_mixture \
  Data_fibrils/Avalanche_force_grouped/local_avalanche_sizes \
  Reviews/Issue5_clauset_pooled_from_scratch \
  --replicates 100 --workers 2 --tag complete_mixture_gof_B100 --resume

MPLBACKEND=Agg \
python -m Code.Data_analysis.clauset_pooled.plot_complete_mixture \
  Reviews/Issue5_clauset_pooled_from_scratch

python -m Code.Data_analysis.clauset_pooled.run_distribution_behavior \
  Data_fibrils/Avalanche_force_grouped/local_avalanche_sizes \
  Reviews/Issue5_clauset_pooled_from_scratch

MPLBACKEND=Agg \
python -m Code.Data_analysis.clauset_pooled.plot_distribution_behavior \
  Reviews/Issue5_clauset_pooled_from_scratch
```

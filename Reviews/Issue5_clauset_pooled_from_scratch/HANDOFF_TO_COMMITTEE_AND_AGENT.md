# Pacote para o comitê e para outro agente

## 1. Arquivos para entregar ao comitê

Levar estes quatro documentos de decisão:

- `UNIFIED_REFEREE_RESPONSE_AVALANCHES.md` — resposta única aos pareceristas;
- `TWO_FIGURES_RECOMMENDATION.md` — escolha e interpretação das duas figuras;
- `REFEREE_RESPONSE_EVIDENCE.md` — matriz completa de evidências e limitações;
- `README.md` — método, resultados e comandos de reprodução.

Levar também estas duas figuras principais:

- `full_distribution_overview.pdf` — distribuição completa;
- `avalanche_behavior_metrics.pdf` — concentração e escalas características.

Se o comitê quiser consultar os números diretamente, acrescentar:

- `full_distribution_summary.csv`;
- `full_distribution_pmf.csv`;
- `observed_power_law_fits.csv`;
- `power_law_gof_B2500.csv`;
- `model_fits.csv`;
- `model_comparisons.csv`;
- `alternative_model_gof_B2500.csv`;
- `complete_mixture_gof_B100.csv`;
- `avalanche_behavior_summary.csv`;
- `avalanche_lorenz.csv`.

## 2. Arquivos para outro agente reproduzir a análise

Copiar a pasta inteira:

`Code/Data_analysis/clauset_pooled/`

Copiar também a pasta inteira de resultados:

`Reviews/Issue5_clauset_pooled_from_scratch/`

Para reproduzir a partir dos dados, é necessário copiar a pasta consolidada,
com aproximadamente 578 MB:

`Data_fibrils/Avalanche_force_grouped/local_avalanche_sizes/`

Ela contém `manifest.json` e os dez arquivos `ts_*.txt`. O manifesto registra
as contagens, o número de geometrias/realizações e os hashes SHA-256.

## 3. Contexto científico que deve acompanhar o pacote

- `Reviews/Referees.md` — comentários dos dois pareceristas;
- `Bibliograph/Clauset2009.md` — artigo metodológico de Clauset;
- `Reviews/Research_Clauset2009_method_summary.md` — resumo metodológico;
- `Reviews/Research_Issue5_avalanche_distribution_statistics.md` — protocolo
  e histórico da decisão estatística;
- `Data_fibrils/Avalanche_force_grouped/local_avalanche_sizes/manifest.json` —
  manifesto da preparação dos dados.

## 4. Mensagem científica a transmitir

A análise usa tamanhos locais discretos e não binados, com $s\geq2$ nos
ajustes. A lei de potência pura foi rejeitada em todos os $T_s$, e nenhuma
família paramétrica alternativa foi validada universalmente. O resultado
defensável é uma distribuição empírica polarizada em duas escalas, com
concentração crescente nos maiores eventos e estabilização aproximada para
$T_s\geq512$. Todas as conclusões são condicionais ao modelo com $m=2$.

Não levar como conclusão válida: SOC, comportamento *scale-free*, expoente
universal, comparação física com $5/2$ ou crossover de universalidade de
compartilhamento de carga.

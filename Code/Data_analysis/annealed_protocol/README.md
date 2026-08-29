# Scripts do protocolo recozido (superados)

Trinta e quatro scripts movidos para cá em 2026-08-29. Todos pertencem à análise
feita **antes** da troca para o protocolo fiber-bundle de desordem congelada
(§12 da DAG). Ficam como referência histórica; **não são o pipeline corrente**.

## Por que cada família saiu

| Família | Motivo |
|:--|:--|
| `run_clauset_*`, `consolidate_clauset_results` | a reanálise da cauda será refeita em N10 sobre a campanha quenched |
| `run_stretched_cutoff_*` | a família de corte esticado pertence ao protocolo antigo (I2, I5 da DAG) |
| `run_issue14_araujo` | validação do ansatz de Araújo sobre os dados recozidos |
| `local_avalanche_*`, `prepare_local_avalanche_sizes`, `fit_local_power_law`, `extract_local_fibril_frequencies`, `compare_local_discrete_models` | operavam sobre `Data_avalanches/`, removido |
| `reproduce_figure_7`, `reproduce_figure_8` | todas as figuras serão geradas de novo à luz dos dados novos |
| `analyze_avalanche_binning`, `compare_binned_avalanche_models` | binning do protocolo antigo |
| `analise_db` | script exploratório de janeiro/2026 |

## O que continua vivo em `Code/Data_analysis/`

Quatro módulos compartilhados, apesar da data antiga, porque scripts da era
quenched os importam ou o cluster os chama:

| Módulo | Quem depende |
|:--|:--|
| `read_avalanche_runs.py` | `campaign_convergence.py` |
| `validate_fractal_proxy.py` | `df_fit_windows.py`, `fibril_compaction.py`, `cluster/sdumont2nd/validate.sh` |
| `extend_fibrils_batch.py` | `slurm/worker_generate.sh` |
| `analyze_fractal_proxy_results.py` | pipeline de $D_f$ |

## Aviso sobre execução

Vários destes scripts não rodam mais como estão: a entrada (`Data_avalanches/`)
foi removida, e alguns importavam módulos que ficaram no diretório pai
(p. ex. `run_avalanche_statistics.py` → `avalanche_statistics.py`). Servem para
consultar como uma análise foi feita, não para reproduzir.

Estado anterior recuperável no commit `99813e7`.

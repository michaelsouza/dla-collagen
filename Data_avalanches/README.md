# Análise das distribuições de avalanches locais

> **Registro exploratório, supersedido para inferência pelo trabalho da issue
> #14.** Os ajustes `scaling_cutoff_*` abaixo usam `tau` no colchete onde a
> derivação de Araújo et al. exige `tau - 1`, além de uma normalização truncada
> em `4*s_max`. As PMFs `local_avalanches_*.dat` continuam sendo as entradas
> preservadas e válidas. A implementação auditada, os testes e as novas
> evidências ficam em `Code/Data_analysis/issue14_araujo/` e
> `Reviews/Issue14_araujo_validation/`.

Os arquivos `local_avalanches_*.dat` possuem duas colunas sem cabeçalho:

1. tamanho inteiro do cluster local, `s`;
2. probabilidade empírica exata, `P(s)`.

Os pontos ausentes no suporte inteiro têm frequência zero. Os scripts não
alteram os arquivos originais nem usam binagem logarítmica.

## Ambiente

A partir da raiz do repositório:

```bash
.venv/bin/pip install -r requirements.txt
```

## Tabelas descritivas

```bash
.venv/bin/python Data_avalanches/scripts/analyze_original_data.py
```

Saídas:

- `Data_avalanches/results/original_data_summary.csv`;
- `Data_avalanches/results/terminal_effect_summary.csv`.

A reconstrução das contagens usa o quantum de probabilidade `1/N` presente em
cada PMF e valida que todas as probabilidades correspondem a frequências
inteiras.

## Figuras log-log dos dados originais

```bash
.venv/bin/python Data_avalanches/scripts/plot_original_loglog.py
```

Saídas em PNG e PDF:

- `figures/original_pmf_com_terminal_loglog.*`;
- `figures/original_pmf_sem_terminal_loglog.*`;
- `figures/original_pmf_terminal_comparison_loglog.*`.

As figuras mostram diretamente as probabilidades não binadas. Não há ajuste,
regressão, suavização ou interpolação. Formatos e diretório podem ser alterados,
por exemplo:

```bash
.venv/bin/python Data_avalanches/scripts/plot_original_loglog.py \
  --formats png svg --dpi 200 --output-dir /tmp/avalanche_figures
```

## Ajuste do modelo de escala finita

O script abaixo usa os dados `com_terminal` e ajusta, por máxima
verossimilhança discreta,

```text
P(s) = C s^(-tau) [tau + eta (s/s0)^eta] exp[-(s/s0)^eta].
```

O ajuste principal é condicionado aos eventos coletivos `s >= 2`, mantendo a
ruptura terminal:

```bash
.venv/bin/python Data_avalanches/scripts/fit_scaling_cutoff.py
```

Saídas:

- `results/scaling_cutoff_fit_parameters.csv`;
- `figures/scaling_cutoff_fits_loglog.{png,pdf}`;
- `figures/scaling_cutoff_parameters_vs_ts.{png,pdf}`.

Para incluir também os singletons, use `--minimum-size 1`. O script normaliza o
modelo sobre todos os tamanhos inteiros, inclusive aqueles com frequência zero.

### Ajuste com escala fixa

Para fixar $s_0$ no maior cluster observado de cada $T_s$ e ajustar somente
$\tau$ e $\eta$:

```bash
.venv/bin/python Data_avalanches/scripts/fit_scaling_cutoff_fixed_s0.py
```

Saídas:

- `results/scaling_cutoff_fixed_s0_parameters.csv`;
- `figures/scaling_cutoff_fixed_s0_fits_loglog.{png,pdf}`;
- `figures/scaling_cutoff_fixed_s0_parameters_vs_ts.{png,pdf}`.

## PMFs com binagem logarítmica

```bash
.venv/bin/python Data_avalanches/scripts/plot_log_binned_pmf.py
```

Por padrão, o script usa 50 bins solicitados entre $s=2$ e o maior tamanho
global. Como as bordas são convertidas em inteiros e duplicatas são removidas,
o conjunto atual contém 46 bins representáveis. A massa de cada bin é dividida
pela largura $\Delta s$, preservando a interpretação de densidade da PMF e a
inclinação de uma eventual potência.

Saídas:

- `results/log_binned_pmf.csv`;
- `figures/log_binned_pmf_com_terminal.{png,pdf}`;
- `figures/log_binned_pmf_sem_terminal.{png,pdf}`;
- `figures/log_binned_pmf_terminal_comparison.{png,pdf}`.

O número de bins pode ser alterado com `--bins`, por exemplo `--bins 100`.

# Execução das simulações de fratura com Slurm

O lote contém 300 tarefas independentes: 50 fibrilas para cada valor de
`Ts`, na ordem `8192, 4096, 1024, 512, 128, 64`. O `Ts=32` não faz parte
do lote.

Cada tarefa usa um núcleo, 1 GB de RAM e executa 1000 realizações. O array
permite até 150 tarefas simultâneas. O benchmark local de `Ts=8192` mediu
aproximadamente 285 MB e 46 segundos por realização, o que estima cerca de
12,8 horas por tarefa; o limite solicitado é de 24 horas para acomodar nós
mais lentos e variação entre fibrilas.

## Estrutura transferida

```text
cluster_bundle/
├── code/
│   └── stress_strain_ava.py
├── inputs/
│   ├── ts_8192/       # 50 arquivos .dat
│   ├── ts_4096/       # 50 arquivos .dat
│   ├── ts_1024/       # 50 arquivos .dat
│   ├── ts_512/        # 50 arquivos .dat
│   ├── ts_128/        # 50 arquivos .dat
│   └── ts_64/         # 50 arquivos .dat
├── logs/
├── results/
├── manifest.tsv       # maior Ts primeiro
├── run_array.sbatch
└── submit.sh
```

Cada tarefa copia seu `.dat` para o armazenamento temporário do nó e cria ali
seu próprio `.db`. Os bancos não precisam ser preparados nem transferidos.

## 1. Preparar os dados localmente

Na raiz do repositório:

```bash
bash Code/Fracture_fibril/slurm/prepare_bundle.sh
```

Por padrão, isso cria a pasta `cluster_bundle/` e também o arquivo único
`cluster_bundle.tar.gz`. Para escolher outros caminhos:

```bash
bash Code/Fracture_fibril/slurm/prepare_bundle.sh \
  /caminho/cluster_bundle /caminho/collagen_cluster.tar.gz
```

## 2. Transferir pela interface do Teleport

Faça upload de apenas um arquivo:

```bash
cluster_bundle.tar.gz
```

No terminal web do Teleport, descompacte:

```bash
tar -xzf cluster_bundle.tar.gz
```

## 3. Preparar o Python no cluster

Somente Python e NumPy são necessários para esta etapa. Adapte o módulo à
instalação do cluster:

```bash
cd /scratch/usuario/collagen
module load python
python3 -m venv venv
source venv/bin/activate
python3 -m pip install numpy
```

## 4. Submeter

Execute a partir do diretório transferido:

```bash
cd /scratch/usuario/collagen
source venv/bin/activate
./submit.sh --account=SEU_PROJETO --partition=cpu
```

Se o cluster não exigir conta ou partição:

```bash
./submit.sh
```

O Slurm não garante formalmente a ordem de início dos elementos de um array,
mas o manifesto enumera primeiro os maiores valores de `Ts`, que normalmente
serão despachados primeiro. Até 150 núcleos serão usados simultaneamente.

## Acompanhar e retomar

```bash
squeue -u "$USER"
sacct -j ID_DO_JOB --format=JobID,State,Elapsed,MaxRSS,ExitCode
find results -type f -name '*_m_2.txt' | wc -l
```

Uma nova execução de `./submit.sh` ignora resultados completos e recalcula
somente tarefas ausentes. Cada resultado é produzido no armazenamento
temporário do nó e movido para `results/` apenas depois de concluído, evitando
publicar arquivos parciais.

Para alterar o número de realizações ou o expoente:

```bash
N_REPS=1000 M_VALUE=2 ./submit.sh --account=SEU_PROJETO --partition=cpu
```

Essas variáveis precisam ser exportadas para chegarem aos nós em clusters que
configuram `sbatch --export=NONE`:

```bash
export N_REPS=1000 M_VALUE=2
./submit.sh --export=ALL --account=SEU_PROJETO --partition=cpu
```

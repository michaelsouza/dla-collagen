# Campanha quenched no SDumont2

Substitui o caminho `prepare_bundle.sh` + `run_array.sbatch`, escrito para outro
cluster. Aqui o código chega por git, os resultados vão para a área de projeto,
e nada é transferido por tar.

## Ordem de operações

```bash
ssh sdumont2nd
cd ~/gitrepos/dla-collagen && git pull --ff-only
bash Code/cluster/sdumont2nd/bootstrap.sh        # uma vez por conta
source Code/cluster/sdumont2nd/env.sh
```

**Antes de qualquer job longo**, a bateria de validação, em nó de compute:

```bash
srun --account=solverbrict --partition=cpu_amd_dev \
     --ntasks=1 --cpus-per-task=8 --mem=16G --time=00:20:00 \
     bash Code/cluster/sdumont2nd/validate.sh
```

Ela roda V0–V8 e sai não-zero se algo falhar. **Não submeta a campanha com
falhas pendentes.**

Não canalize a saída (`| tail`, `| tee`) se quiser conferir o código de saída: o
pipe devolve o status do último comando, não o da bateria. Para guardar o log
sem perder o status, use `bash ... validate.sh > val.log 2>&1; echo $?`.

Depois:

```bash
Code/Fracture_fibril/slurm/make_manifest.sh generate
CAMPAIGN_KIND=generate Code/Fracture_fibril/slurm/submit_campaign.sh

# quando a geração terminar
Code/Fracture_fibril/slurm/make_manifest.sh fracture
CAMPAIGN_KIND=fracture Code/Fracture_fibril/slurm/submit_campaign.sh
```

## Duas restrições operacionais descobertas na prática

- **`cpu_amd_dev` aceita um job por vez.** Um segundo `srun` falha com
  `QOSMaxSubmitJobPerUserLimit`, mesmo com a fila aparentemente vazia.
- **Um `srun` sobrevive à queda do ssh.** Se a conexão cair, a alocação
  continua e bloqueia a partição de desenvolvimento. Confira com
  `squeue -u "$USER"` e libere com `scancel -u "$USER" -p cpu_amd_dev`.

## Forma do job, e por quê

O QOS limita a conta a **1920 CPUs** e a **100 jobs em execução**. Dez tarefas de
192 núcleos saturam o teto de CPU usando um décimo dos slots de job; cem tarefas
de um núcleo usariam todos os slots para 5% da CPU. Por isso `campaign.sbatch`
pede `--exclusive` e fatia o manifesto, rodando cada fatia com `xargs -P`
(GNU parallel não é assumido).

Aumentar `CAMPAIGN_TASKS` acima de 10 não ajuda: o teto de CPU vincula primeiro.

## Retomada

Reenvie o mesmo array. Ambos os workers são idempotentes:

- `worker_generate.sh` sai imediatamente se o arquivo estendido já existe;
- `worker_fracture.sh` conta os separadores de realização e continua de onde
  parou, com `-start`.

Uma tarefa que falha **não aborta a fatia**: `xargs` segue e o job termina com
aviso. Uma fibrila ruim não descarta o trabalho das outras 199.

## Onde as coisas ficam

```
$DLA_PROJECT/campaign/
  manifest_generate.tsv        TS SEED
  manifest_fracture.tsv        TS SEED M
  bin/fast_dla2                gerador de produção (-O3 -march=native)
  fibrils/compact/             dla_mode_s_ts_<TS>_nb_<NB>_seed_<SEED>_.dat
  fibrils/extended/            ts_<TS>_seed_<SEED>.dat
  avalanches/runs/ts_<TS>/     ts_<TS>_seed_<SEED>_m_<M>.txt
  logs/coverage/               estatística de cobertura por fibrila
  logs/failed/                 logs preservados de tarefas que falharam
```

`avalanches/runs` é exatamente a raiz que `read_avalanche_runs.py` espera:

```bash
python3 Code/Data_analysis/read_avalanche_runs.py summary \
    "$DLA_PROJECT/campaign/avalanches/runs"
```

`$HOME` tem 100 GB e guarda só o clone e o venv. Resultados vão para a área do
projeto (6 TB de quota **de grupo**, compartilhada):

```bash
lfs quota -h -g solverbrict /petrobr
```

## Sementes

`seed = 100000 + 1000*i + k`, com `i` o índice do $T_s$ em `CAMPAIGN_TS` e `k` o
índice da fibrila. O bloco por condição importa: a parada adaptativa da Fase B
encerra cada $T_s$ independentemente, então estender uma condição não pode
deslocar as sementes de outra. Nada histórico chega a 100000 (a campanha antiga
vai até ~10750).

Não há requisito de reproduzir as fibrilas publicadas. Com `-rng fast` a mesma
semente não dá a mesma fibrila, e isso é aceito: o requisito é que a geração siga
a mesma lógica de etapas, que é o que V3 verifica.

## Duas armadilhas herdadas

- **Modo padrão divergente.** `fast_dla` assume `-mode n`, `fast_dla2` assume
  `-mode s`. Os workers sempre passam `-mode s` explicitamente. Produção sempre
  foi `s` (registro axial em múltiplos de 4, o D-period).
- **`run_array.sbatch` antigo pede `%150`**, acima do teto de 100 do QOS, e
  `prepare_bundle.sh` aborta se um $T_s$ não tiver exatamente 50 fibrilas.
  Nenhum dos dois é usado por esta campanha; ficam para reproduzir o resultado
  antigo, se necessário.

## Variáveis de ajuste

| Variável | Padrão | Efeito |
|:--|:--|:--|
| `CAMPAIGN_FIBRILS` | 200 | teto de fibrilas por $T_s$ |
| `CAMPAIGN_REALIZATIONS` | 100 | realizações por fibrila |
| `CAMPAIGN_NUM_BIND` | 30000 | moléculas por fibrila |
| `CAMPAIGN_TASKS` | 10 | tarefas do array |
| `CAMPAIGN_WORKERS` | núcleos do nó | processos por tarefa |
| `CAMPAIGN_BIN` | `$DLA_PROJECT/campaign/bin/fast_dla2` | gerador |

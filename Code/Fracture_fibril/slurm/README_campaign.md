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

## Restrições operacionais, verificadas

**O limite de submissão é o que vincula.** `MaxSubmitPU=100` e **cada elemento
de array conta como um job submetido**, somado sobre todos os seus jobs, na fila
ou rodando. O acelerador `%N` não ajuda: ele limita quantas tarefas *rodam*, não
quantas são submetidas. O orçamento é 100 menos o que já está na fila — uma
única tarefa retida de uma tentativa anterior basta para derrubar um array de
100. `submit_campaign.sh` confere isso antes de submeter e faz um `--test-only`.

**As partições `*_dev` aceitam um job por vez**, por limite de **associação**
(`MaxJobs=1, MaxSubmit=1`), não da QOS — `cpu_amd` e `cpu_amd_dev` usam a mesma
QOS. Confira com:

```bash
sacctmgr -P show assoc user="$USER" format=Partition,QOS,MaxJobs,MaxSubmit
sacctmgr -P show qos ict_cpu-genoa format=Name,MaxTRESPU,MaxJobsPU,MaxSubmitJobsPU
```

Peça o cabeçalho (`-P` sem `-n`): `sacctmgr -nP` emite uma coluna vazia extra
que faz `MaxJobsPU` parecer o limite de submissão.

**Um `srun` sobrevive à queda do ssh.** A alocação continua e bloqueia a
partição de desenvolvimento, que só aceita um job. Confira com
`squeue -u "$USER"` e libere com `scancel -u "$USER" -p cpu_amd_dev`.

**Uma tarefa de array pode ficar retida.** `launch failed requeued held` não
produz log nenhum e não sai sozinha do estado. Libere com
`scontrol release <JOBID>_<TASK>`; se reincidir, deixe as outras terminarem e
use `check_campaign.sh` + reenvio, que é idempotente. Uma tarefa retida também
**consome uma vaga do orçamento de submissão**.

**Falhas de lançamento são aleatórias, ~1/3, e o fluxo já lida com isso.**
Medido num teste controlado (2026-08-25): 3 tarefas retidas em 8, e 5 em 16 nas
submissões anteriores. **Não dependem do índice** — num array de 2, a tarefa 0
falhou e a 1 rodou — nem do tamanho do array, nem do nó. Uma leitura inicial de
que "só os índices 0 e 1 rodam" era coincidência de amostra pequena: com 1/3 de
falha, um array de 2 sai limpo em 45% das vezes.

Use `run_until_complete.sh`, que submete, espera, verifica e reenvia até fechar.
Como os workers são idempotentes, cada rodada faz só o que falta; a fração
ainda pendente após *n* rodadas é ~(1/3)ⁿ — 67% pronto após uma, 89% após duas,
96% após três.

```bash
CAMPAIGN_KIND=fracture Code/Fracture_fibril/slurm/run_until_complete.sh
```

**A causa não foi estabelecida.** Numa medição de 2026-08-25 havia **12 jobs
retidos no cluster inteiro**, de vários usuários e projetos, com a partição
tendo 344 núcleos livres. Portanto não é falta de recurso nem algo específico
desta campanha.

Uma hipótese plausível e barata de eliminar: o Slurm abre os arquivos de
`--output` e `--error` **no momento do lançamento**; um caminho relativo resolve
contra o diretório de submissão como visto do nó de compute, e no Lustre esse
diretório pode ainda não ter propagado. Isso explicaria por que a tarefa retida
não deixa log nenhum — falha antes de abrir o arquivo. Por isso
`submit_campaign.sh` passa caminhos **absolutos**, num diretório criado e
confirmado antes de submeter.

Mas isso é mitigação, não diagnóstico: os jobs retidos de outros usuários podem
ter outra causa, e não temos como inspecioná-los. **Trate o ciclo
`check_campaign.sh` + reenvio como parte normal da operação**, não como
exceção — é ele que garante o resultado, independentemente da causa.

## Forma do job, e por quê

O QOS limita a conta a **1920 CPUs** e a **100 jobs em execução**, mas na prática
quem decide o tempo de início é outra coisa: a `cpu_amd` é compartilhada e vive
com **zero nós ociosos** e dezenas de jobs de outros usuários na fila (79 numa
medição de 2026-08-25, com 10 nós alocados, 9 mistos e 1 drenando).

Por isso a campanha **não** pede `--exclusive`. Um pedido de nó inteiro entra na
fila atrás de todo mundo; um pedido de fração de nó entra nos núcleos livres de
um nó parcialmente usado e começa quase imediatamente. O padrão é **40 tarefas
de 48 núcleos** — chega ao teto de 1920 CPUs, cabe no limite de 100 jobs, e cada
tarefa faz backfill.

Cada tarefa pega uma fatia contígua do manifesto e a roda com `xargs -P`
(GNU parallel não é assumido presente).

Ajuste com `CAMPAIGN_TASKS` e `CAMPAIGN_CPUS`. Para um lote pequeno, poucas
tarefas pequenas começam antes e consomem menos da alocação do grupo.

## Exclusividade e memória

A campanha **não** pede `--exclusive`, e não precisa. Cada item de trabalho — uma
fibrila, ou a fratura de uma fibrila num dado $m$ — é de núcleo único e
independente: não há MPI, nem memória compartilhada entre itens, nem
comunicação. A escrita vai para `$DLA_TMP` node-local, então nem a I/O é
disputada. Nada se ganha em ter o nó só para si, e numa partição sem nós
ociosos a exclusividade só serve para ficar na fila.

Como consequência, é preciso **pedir memória explicitamente**: sem
`--exclusive`, o job recebe só o que pede. O `DefMemPerCPU` da `cpu_amd` é
7800 MB, então uma tarefa de 48 núcleos reservaria 374 GB por omissão. O uso
medido é bem menor:

| Medição | Valor |
|:--|:--|
| MaxRSS, tarefa de 24 processos de geração | 0,56 GB |
| Por processo | ~23 MB |
| Reservado por omissão (24 núcleos) | 187 GB |

Reservar 334× o necessário não é gratuito num cluster compartilhado: um nó de
1,5 TB comportaria só quatro tarefas de memória padrão, de modo que a **memória,
e não os núcleos**, vira o limite de empacotamento, e outros usuários ficam sem
núcleos que estão ociosos. O padrão é `--mem-per-cpu=2G`, ajustável por
`CAMPAIGN_MEM_PER_CPU`, com margem larga sobre as poucas centenas de MB por
processo do protocolo de fratura.

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

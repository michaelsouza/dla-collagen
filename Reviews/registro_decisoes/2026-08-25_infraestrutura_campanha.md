# Infraestrutura da campanha

**Data:** 2026-08-25  
**Origem:** §15 de `DAG_dependencias_revisao.md`, dividida em 2026-08-29.

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

Escrita e **validada localmente** antes de subir. Documentação de operação em
`Code/Fracture_fibril/slurm/README_campaign.md`.

#### Peças

| Arquivo | Papel |
|:--|:--|
| `slurm/campaign_common.sh` | grade, esquema de sementes, layout — definidos uma vez |
| `slurm/worker_generate.sh` | gera + estende UMA fibrila; idempotente |
| `slurm/worker_fracture.sh` | fratura quenched de UM (fibrila, m); retoma por separadores |
| `slurm/make_manifest.sh` | lista de trabalho: 2000 itens de geração, 10000 de fratura |
| `slurm/campaign.sbatch` | fatia o manifesto e roda a fatia com `xargs -P` |
| `slurm/submit_campaign.sh` | submete respeitando o QOS |
| `cluster/sdumont2nd/validate.sh` | bateria V0–V8 |

#### Decisões de desenho

- **Workers separados do sbatch.** Foi o que permitiu validar toda a lógica sem
  Slurm; sem isso, o primeiro teste real seria no cluster.
- **Poucos jobs largos.** O QOS limita a 1920 CPUs *e* 100 jobs. Dez tarefas de
  192 núcleos saturam a CPU usando um décimo dos slots. `xargs -P` em vez de GNU
  parallel, que não se pode assumir presente.
- **Idempotência em vez de estado.** Reenviar o mesmo array retoma; não há
  arquivo de progresso para corromper.
- **Falha isolada.** Uma fibrila ruim não aborta a fatia; o job termina com aviso
  e o reenvio recolhe o que falta.

#### Bugs encontrados e corrigidos na validação local

1. **`set -e` engolia os erros.** O `python3` que falha abortava o worker antes
   do tratamento de erro, e o `trap` apagava o log — no cluster não se veria
   nada. Agora o status é capturado explicitamente, o log é ecoado e uma cópia
   é preservada em `logs/failed/`.
2. **Scripts não eram testáveis fora do cluster**, porque `env.sh` sai com erro
   sem `module`/venv. Passaram a respeitar um ambiente já configurado.

#### Verificações locais

| Teste | Resultado |
|:--|:--|
| Fatiamento de array (4 tarefas × 20 itens) | sem lacuna nem sobreposição |
| Geração ponta a ponta | 20/20 fibrilas |
| Fratura ponta a ponta | 100/100 resultados, 10/10 condições |
| Parser sobre a saída da campanha | 50 condições, 300 realizações, 12772 eventos |
| Retomada (2 apagados + 1 truncado) | restaurados em 4,2 s, só o faltante |
| Idempotência | segunda execução é no-op |

#### Pendente no cluster

V0–V8 em `cpu_amd_dev`, com atenção especial a **V3**: a identidade bit a bit foi
verificada com `-O2`; a produção usa `-O3 -march=native`, que habilita contração
FMA em `launch_on_sphere` — o único passo de ponto flutuante do gerador, onde
1 ULP pode mover uma coordenada inteira. Por isso `validate.sh` compila dois
binários e usa o `-O2` para o teste de identidade.

# Política de trabalho — dla-collagen

**Este arquivo não contém objetivos, prioridades nem estado de tickets.** Só
regras que sobrevivem à troca de assunto. O que está sendo feito agora está em
`Reviews/Estado_revisao_ER12738.md`, cuja tabela de nós é a lista de tickets.

## 1. Como conversar comigo

- **Linguagem simples por padrão.** Mecanismo concreto primeiro, analogia física quando ajudar, um argumento por parágrafo, números medidos em tabela curta. Michael avisa quando faltar rigor — não antecipe subindo o nível técnico.
- **Matemática:** `\( \)` e `\[ \]` nas respostas do chat; `$ $` nos `.md` do repositório.
- **Meça antes de afirmar.** Este repositório tem dados; estimativa de cabeça quando a medição é possível é erro, não atalho.

## 2. Onde mora o conhecimento

Três lugares, com papéis **que** não se misturam:

| Onde | Papel | Por que é verdadeiro |
|:--|:--|:--|
| `AGENTS.md` (= `CLAUDE.md`) | política de trabalho | porque Michael o edita; durável, sem objetivos, sem estado |
| `Reviews/Estado_revisao_ER12738.md` | nós, arestas e estado da revisão; a tabela de nós **é** a lista de tickets | porque `validate_review_state.py` confere; cabe numa tela; editado, nunca acrescido |
| `Reviews/decision_log/AAAA-MM-DD_assunto.md` | por que cada decisão foi tomada | porque **nunca muda**; append-only |

**Única exceção ao append-only:** correção mecânica de caminho, quando um arquivo
ou diretório citado é renomeado. Proibir isso obrigaria o registro a apodrecer,
que é o oposto do objetivo. Nenhum fato, número ou raciocínio pode mudar — só a
referência. Registre a renomeação no commit.
| `.claude/memory/` (fora do git) | memória automática do Claude: preferências e correções de Michael | escrita pelo Claude, visível e editável por Michael; **não versionada** |

**Sem GitHub Issues.** Foram abandonadas em 2026-08-29: para um projeto de um
autor só, não compravam nada que a tabela de nós não dê, e eram mais um lugar
para o estado apodrecer. Nada científico mora fora do repositório.

**Fronteira com `.claude/memory/`.** Regra do próprio Claude Code: a memória
automática deve pular o que o `CLAUDE.md` já diz. Então o que é específico deste
projeto mora **aqui**, onde Michael vê e corrige; a memória guarda só o que
segue Michael para outros repositórios. Se um fato aparecer nos dois, o
`AGENTS.md` vence e a memória aponta para ele em vez de repetir.

Ela fica em `.claude/memory/` por causa de `autoMemoryDirectory` em
`.claude/settings.local.json` — o mecanismo suportado, sem link simbólico. Não é
versionada: o Claude a reescreve sozinho (conflitaria entre sessões paralelas),
o caminho absoluto não vale no clone do cluster, e ela é local à máquina por
desenho.

**`CLAUDE.md` é link para `AGENTS.md`.** O Claude Code lê `CLAUDE.md`, **não**
`AGENTS.md` — o link é necessário, não conveniência.

**Por que separado.** Entre 25 e 29 de agosto de 2026 o documento único afirmou que a campanha estava bloqueada enquanto ela rodava até o fim, e que as fibrilas brutas estavam ausentes quando estavam num zip do próprio repositório. Um arquivo que é 85% arquivo morto não é atualizado no lugar certo.

**Toda afirmação de estado deve ser verificável por script.** "N16 bloqueado" é checável contando arquivos no cluster. `Code/Data_analysis/validate_review_state.py` confere as afirmações; rode-o antes de confiar no estado.

## 3. Convenção de nomes

Nome genérico é o começo do problema — foi assim que nasceram nove versões de `extend_fibrils` e um `compact.zip` que ninguém sabia conter as fibrilas do artigo.

- **Nomeie pelo conteúdo específico, não pela categoria.**
  `fibrilas_publicadas_artigo_10Ts_nb30000.zip`, não `compact.zip`.
  `validate_review_state.py`, não `status.py`.
- **Diretórios sempre em en-US**, mesmo os que guardam documentos em português:
  `decision_log/`, não `registro_decisoes/`; `annealed_protocol/`, não
  `protocolo_recozido/`.
- **Código em inglês, conteúdo dos documentos em português**, seguindo o que já
  existe. O nome do arquivo datado pode ser em português; o diretório, não.
- **Verbo primeiro nos executáveis:** `validate_`, `run_`, `plot_`, `extract_`,
  `compare_`. Módulos importáveis levam substantivo: `avalanche_statistics.py`.
- **Documento datado:** `AAAA-MM-DD_assunto.md`.
- **Sem sufixos de versão.** Nada de `_fixed`, `_v2`, `_new`, `_REBUILT`, `.bak`.
  O histórico do git é a versão anterior.

## 4. Cabeçalho de arquivo de código

Todo arquivo deve abrir com um cabeçalho que carregue **fatos verificáveis**, não
descrição. Descrição nunca fica errada e por isso nunca ajuda:

```python
"""Estima D_f por T_s a partir das seções transversais.

Lê:      Data_fibrils/.../extended/ts_<TS>_seed_<SEED>.dat
Escreve: Reviews/N7_fractal_proxy/df_por_ts.csv
Chamado: Code/cluster/sdumont2nd/validate.sh; df_fit_windows.py
"""
```

As três últimas linhas podem ser conferidas por script. Um cabeçalho que diz
"chamado por X" e X não existe mais é um erro detectável.

## 5. Regras de conteúdo científico

- **Nunca** trate criticalidade auto-organizada, comportamento livre de escala ou
  universalidade de load sharing como conclusão estabelecida sem suporte
  estatístico e mecanístico explícito e concluído.
- **Distinga correlação empírica de relação causal**, em especial entre dimensão
  fractal da seção e estatística de ruptura (é o objeto de R1-5 / N12).
- **Não ajuste lei de potência sobre menos de duas décadas.** A campanha atual dá
  ~1 década; `Clauset2009` é a autoridade para **não** afirmar.
- **Rastreabilidade:** todo resultado que entra no manuscrito nomeia o CSV de
  origem, e todo ticket nomeia todos os comentários de revisor que atende.
- **Ao citar uma fonte, abra a fonte.** Já houve caso de citar `Parkinson1995` e
  `Kadler1987` para o oposto do que dizem.
- **Preserve alterações locais não relacionadas.** Michael trabalha em várias
  sessões ao mesmo tempo; confira `git status` e o estado remoto antes de editar
  ou commitar, e não commite sem pedirem.

## 6. Cluster SDumont2 (LNCC)

Conta `solverbrict`, partição `cpu_amd` (`cpu_amd_dev` para teste). Alias
`ssh sdumont2nd`. Ambiente: `source Code/cluster/sdumont2nd/env.sh`.

- **Código vai por git**, nunca cópia de working tree.
- **Nunca** rode simulação, benchmark ou suíte completa no nó de login.
- **Resultados em `$DLA_PROJECT`** (`~/scratch/dla-collagen`, área de 6 TB), nunca
  em `$HOME`, cuja cota de 100 GB só cabe o clone e o venv. `$SCRATCH` é apelido
  de `$HOME` e não dá espaço extra.
- **Escreva primeiro no disco local do nó** (`$DLA_TMP`), depois copie para o
  Lustre e `mv` no lugar, para que job interrompido nunca publique parcial.
  `SLURM_TMPDIR` não existe aqui: use `${SLURM_TMPDIR:-${TMPDIR:-/tmp}}`.
- **Teto de 100 tarefas de array submetidas por usuário**, contando cada
  elemento; `%N` não levanta isso. Confirme com `sbatch --test-only`.
- Registre cluster, partição e job ID de todo resultado que entra no manuscrito.
- A rede para o cluster cai de forma intermitente. Se cair, siga com o que houver
  e diga explicitamente o que não deu para verificar.

## 7. Ambiente local e ferramentas

- **Instale pacotes livremente** quando ajudarem. Ferramenta pronta é melhor que
  reimplementar.
- Não há `pip` nem `conda` nesta máquina. Use:
  `uv pip install --python .venv/bin/python <pacote>` (venv do projeto, Python 3.12).
- `ls` está aliasado para um formato com permissões — não faça parsing da saída
  dele; use glob do shell.
- O shell é **zsh**: variável não citada **não** é dividida em palavras. Use
  `while read` em vez de `for x in $lista`.

## 8. Higiene do repositório

- `Code/` é código. Dado vai em `Data_fibrils/`, documento em `Reviews/`.
- Notebook não é entregável: converta com `nbconvert` e versione o `.py`.
  Notebook com saída embutida chegou a 49 MB para 168 KB de código.
- Análise superada vai para uma subpasta com README explicando **por que** saiu,
  não é apagada em silêncio.
- Apagar do working tree **não** encolhe o `.git` (702 MB de 1,5 GB). O objetivo
  da limpeza é clareza, não espaço.
- Ao remover um conjunto, registre o commit onde ele ainda existe.
- **Figuras do manuscrito são feitas no xmgrace**, porque é o ambiente dos
  coautores. Python só exporta as tabelas: um diretório por figura, arquivos
  `.dat` já no formato que o xmgrace lê (`xy`, `xydy`, `xydxdy`; um bloco por
  série), e um README que nomeia o CSV de origem e o script que os gerou. O
  projeto `.agr` é versionado ao lado dos dados. Figura em Python fica só nos
  relatórios internos de `Reviews/`. Exemplo: `Reviews/N7_fractal_proxy/xmgrace/`.
- **Michael trabalha em várias sessões ao mesmo tempo neste repositório.**
  Rode `git fetch` e confira divergência antes de editar em lote ou commitar;
  nunca faça rebase ou force-push sobre trabalho que pode não ser seu.

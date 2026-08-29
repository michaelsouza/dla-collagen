# Limpeza do repositório

**Data:** 2026-08-29  
**Origem:** §18 de `DAG_dependencias_revisao.md`, dividida em 2026-08-29.

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

`Code/` foi de 140 MB para 1,8 MB; `Reviews/` de 18 MB para 4,0 MB. O `.git`
continua com 702 MB — apagar do working tree não toca no histórico.

| Removido | Motivo |
|:--|:--|
| 9 variantes de `extend_fibrils` | a viva é `extend_fibrils_batch.py` (`worker_generate.sh:83`) |
| 7 notebooks (49 MB) | convertidos com `nbconvert` para 168 KB em `Code/Data_analysis/notebooks_extraidos/` |
| `Reviews/Issue5_*`, `Issue14_*`, `Issue3_*`, `Report_stretched_cutoff_*` | protocolo recozido; entrada (`Data_avalanches/`) já removida |
| 34 scripts → `Code/Data_analysis/protocolo_recozido/` | mesma razão; os 26 vivos ficaram no topo |

`Code/Fracture_fibril/compact.zip` →
`Data_fibrils/fibrilas_publicadas_artigo_10Ts_nb30000.zip`. **Não é redundante
com o cluster**: o SDumont só tem fibrilas da campanha (sementes 100000+) e do
piloto. É a única cópia das fibrilas do artigo. Foi essa verificação que expôs o
erro corrigido na §9.

Estado anterior recuperável em `99813e7`.

#### O que a limpeza ensinou sobre este documento

Duas heurísticas mecânicas falharam ao classificar o que era código morto: a
contagem de referências (drivers de linha de comando não são importados por
ninguém) e a data de modificação (`validate_fractal_proxy.py` é de 20/08 e é
infraestrutura viva, importada por três scripts novos). O que decidiu foi
combinar as duas com o conhecimento de qual protocolo cada família servia.

O mesmo vale um nível acima: **este documento afirmou por quatro dias que N16
estava bloqueado enquanto a campanha rodava até o fim, e que as fibrilas brutas
estavam ausentes quando estavam num zip do próprio repositório.** Prosa datada
não detecta a própria defasagem. Ver a discussão de ferramenta na §17 da
sessão.

# Limpeza depois do manuscrito e da carta escritos

**Data:** 2026-09-03
**Afeta:** `Carta_Resposta/`, `Reviews/`, `.gitignore`
**Motivo:** com o manuscrito revisado e a carta commitados (`ad86b41`–`f1f4518`),
sobraram no repositório artefatos de versões anteriores que nada mais cita.

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## O que saiu, e onde ainda existe

| conjunto | por que saiu | último commit em que existe |
|:--|:--|:--|
| `Carta_Resposta/figure_1.png`, `figure_2.png`, `figure_3.png`, `figure_4.pdf` | figuras da carta de 2026-08-15; a carta escrita em 2026-09-03 cita o manuscrito e não tem `\includegraphics` | `f1f4518` (usadas pela última vez em `6d0e874`) |
| `Reviews/Response_to_Referees.tex`, `.md`, `.pdf` | checkpoint da carta de 2026-08-06; a carta viva é `Carta_Resposta/Response_to_Referees.tex`, e nada apontava para estas cópias | `f1f4518` |

## O que se moveu

`Reviews/xmgrace_export/` → `Reviews/annealed_protocol/xmgrace_export/`. São os
ajustes de corte esticado do protocolo recozido, gerados por
`Code/Data_analysis/annealed_protocol/run_stretched_cutoff_individual.py`, que já
estava arquivado como superado desde 2026-08-29; os dados tinham ficado na raiz
de `Reviews/`, ao lado dos atuais. README novo em `Reviews/annealed_protocol/`.

## `.gitignore`

Reescrito. Saíram os padrões que apontavam para caminhos inexistentes (sete
diretórios `Reviews/Issue*` e `Figure7_*`, `Data/`, `tmp/`, dois `.zip` já
cobertos por `*.zip`, `ai-tools`, `.env`) e as duas linhas que ignoravam arquivos
versionados (`Paper/apssamp.bib`, `Reviews/Research_Clauset2009_method_summary.md`),
que não faziam nada. Nenhuma regra com efeito real mudou: conferido com
`git status --ignored` antes e depois.

## Também

- `export_figure_8_xmgrace.py:18` dizia `export_figure_9_xmgrace.py` no exemplo
  de uso — resto da renomeação 9→8.
- A linha 233–238 da @tbl-plano em `Respostas_ER12738.qmd` dizia que `fig_9`
  ficaria com o nome; registra agora que foi renomeado para 8.
- `Paper/figure_10.pdf` (figura da revisão descartada, 2026-08-24, em `521a284`)
  e `Paper/texput.log` estavam no working tree, ignorados; apagados.

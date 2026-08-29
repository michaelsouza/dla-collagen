# Código extraído dos notebooks legados

Os sete notebooks de `Code/Data_analysis/` foram convertidos com
`nbconvert --to script` e removidos em 2026-08-29. Eles somavam 49 MB — quase
tudo saída embutida (figuras em base64) — contra 168 KB de código.

**Origem:** todos com última alteração em 2026-01-08, nenhum citado por script,
`.md` ou `.tex`. Pertencem ao protocolo recozido, anterior à troca para a
dinâmica quenched (§12 da DAG).

**Status:** referência histórica. Nenhum destes arquivos é executável como está
— vários apontam para caminhos de outra máquina (p. ex. `graph_fibrils.py`
lê `/home/robert/Datas/...`). Servem para consultar como uma análise foi feita,
não para rodar.

Os notebooks originais continuam recuperáveis no commit `99813e7`:

```bash
git show 99813e7:Code/Data_analysis/dla_fractal.ipynb > /tmp/dla_fractal.ipynb
```

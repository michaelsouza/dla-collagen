# Saída bruta da escada de janelas (Fase C, passo 2b)

Arquivos no esquema legado do `fiber_bundle_ava.py` (uma linha por cascata;
realizações separadas por `----`), um por (condição, janela). São a fonte dos
CSVs `../avalanche_ladder_ts128.csv` e `../avalanche_ladder_ts8192.csv`, via
`../summarize_avalanche_ladder.py`.

Objeto: cilindro periódico `-period 216`, `nb`=60.000, semente 900001, gerado
pelo `fast_dla2.cpp` do commit `17cfc1f`, aberto em $y=\pm108$ por
`open_periodic_cylinder.py`, estendido por `extend_fibrils_batch.py` e
fraturado com `-m 2 -seed 1` e `-half-width` 8 / 20 / 40 / 90 (128) e 8 / 70
(8192). Guardados aqui porque as fraturas largas custam ~2 h cada e o
scratchpad da sessão não é permanente.

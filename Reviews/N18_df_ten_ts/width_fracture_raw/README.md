# Fraturas locais por largura de recorte — arquivos brutos

Saída legada de `Code/Fracture_fibril/fiber_bundle_ava.py` (mesmo esquema de
`../../PhaseC_periodic_cylinder/avalanche_ladder_raw/`): uma linha por evento,
`f, num_active_particles, num_deleted_particles, total_deleted_rods, avalanche_sizes`;
realizações separadas por `----…<k>`; a linha com `num_active_particles == 0` é a
cascata terminal e sua coluna `f` é $F_{rup}$.

| pasta | recorte | `-half-width` | conteúdo |
|:--|:--|--:|:--|
| `w17/ts_<T>/ts_<T>_seed_<S>_m_2.txt` | 17×17 | 8 | 10 realizações por cilindro |
| `w41/ts_<T>/ts_<T>_seed_<S>_m_2.txt` | 41×41 | 20 | 10 realizações por cilindro |

Objeto: cilindros periódicos `dla_per216_mode_s_ts_<T>_nb_60000_seed_<S>_.dat`
($T \in \{2, 32, 128, 8192\}$, $S \in$ 900001–900005; receita em `../README.md`),
abertos em $y = \pm 108$ por `open_periodic_cylinder.py`, estendidos por
`extend_fibrils_batch.py`, fraturados com `-m 2 -seed 101 -half-length 100`.
Gerados por `Code/Data_analysis/run_local_width_fracture.sh` em 2026-09-10 nesta
máquina (1 h 10 para os 41×41). Resumidos por `summarize_width_fracture.py` em
`../width_fracture_{by_realization,summary}.csv`.

Ficam versionados (~8 MB) pelo mesmo motivo da escada: cada 41×41 custa de 12 a
47 min por cilindro, e a semente de fratura 101 não repete as realizações da
escada de 02/09 (semente 1).

# N7 — dimensão fractal: o que está aqui

| arquivo | objeto | o que traz |
|:--|:--|:--|
| `ensemble_curve_validation.csv` | 499 fibrilas publicadas (`Data_fibrils/…zip`) | os 10 $D_f$ do artigo reproduzidos com as janelas por condição do projeto Grace original (que **não** está no repositório) |
| `condition_descriptor_summary.csv` | idem | $D_f$ por fibrila sob as mesmas janelas, com $\langle N\rangle$, $\langle K\rangle$ e CV |
| `df_published_fibrils_by_window.csv` | idem | $D_f$ sob quatro regras de janela uniformes, ensemble e por fibrila (`estimate_df_published_fibrils.py`) |
| `df_published_mass_radius_curves.csv` | idem | a curva $\langle m(R)\rangle$ do ensemble, $R = 1$–64 |
| `df_campaign_fibrils_by_window.json` | 250 fibrilas da campanha quenched (25 por $T_s$), no cluster | $D_f$ sob três regras (fixa 4–8, fixa 2–16, relativa $0{,}15R$–$0{,}5R$), erro-padrão entre fibrilas, raio médio e curva média por $T_s$. É a fonte da tabela da §4 do relatório da campanha. Escrito por `df_fit_windows.py` como `analysis/df/df_windows.json` (2026-08-26); copiado para cá em 2026-09-10 |
| `proxy_correlations.csv`, `xmgrace/` | figura de correlação cortada da revisão (§13.2 das respostas) | |

Os cilindros periódicos largos estão em `../PhaseC_periodic_cylinder/`.

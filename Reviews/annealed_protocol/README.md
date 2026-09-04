# Resultados do protocolo recozido (superados)

Dados da análise feita **antes** da troca para o protocolo fiber-bundle de
desordem congelada (quenched), decidida em 2026-08 e registrada em
`decision_log/`. Nenhum número daqui entra no manuscrito revisado nem na carta.
Ficam como referência histórica, ao lado dos scripts que os produziram, que
estão em `Code/Data_analysis/annealed_protocol/` (README lá explica por que
cada família saiu).

| subpasta | o que é | gerado por | movido de |
|:--|:--|:--|:--|
| `xmgrace_export/` | ajustes de corte esticado $p(s)\propto s^{-\alpha}e^{-(s/s_0)^{\beta}}$ por $T_s$, com CCDF, bootstrap e GOF em `.dat` do Grace | `run_stretched_cutoff_individual.py` | `Reviews/xmgrace_export/` em 2026-09-03 (existia lá até `f1f4518`) |

Por que saiu: a família de corte esticado pertence ao protocolo antigo, e a
Fig. 8 revisada mostra $P(S>s)$ sem ajuste algum (teste de Clauset rejeita a lei
de potência em 48 das 50 condições; menos de uma década acima de $s_{\min}$).
Os dados atuais da figura estão em `Reviews/N10_cascade_survival/xmgrace/`.

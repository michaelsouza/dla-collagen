# Evidência do protocolo de carregamento (N2 / R2-1) e da correção de σ (N0)

**Aviso de proveniência.** Todos os `p_*.json.gz`, `exact_*.json` e
`stale_ts128.json` deste diretório foram gerados com o código **anterior** à
correção de σ (commit `a834c53`). Eles documentam *por que* a correção foi
feita e não devem ser usados como linha de base atual. As medições do
protocolo (Q_quieto, sensibilidade a ΔF e ao critério de parada) precisam ser
refeitas com o código corrigido.

## Scripts

| arquivo | o que mede |
|:--|:--|
| `probe.py` | por passo de força: nº de varreduras, removidos, `sum_p` e `q_quiet` na configuração de parada |
| `stale.py` | desvio entre o σ em cache e o exato `F/N(i)` ao longo de uma simulação |
| `exact.py` | comparação pareada cache vs. recomputação forçada (força de ruptura e avalanches) |
| `summarize.py` | tabela consolidada de `protocol_sensitivity.txt` |

## Resultados principais

`protocol_sensitivity.txt` traz a tabela completa. Os dois achados:

1. **A parada não é um estado absorvente.** Q_quieto ≈ 0,55–0,60: há ~43% de
   chance de que outra varredura idêntica removesse algo.
2. **Não há convergência.** Exigir k varreduras quietas consecutivas derruba
   F_rup monotonicamente (178 → 141 → 120 → 101 para k = 1, 2, 3, 5) sem
   platô; F_rup também cresce monotonicamente com ΔF.

Ambos motivaram a adoção do protocolo fiber-bundle de desordem congelada
(`Code/Fracture_fibril/fiber_bundle_ava.py`), em que a cascata termina
deterministicamente e não há ΔF nem critério de parada.

## Reprodução

Os `p_*.json.gz` exigem o código pré-correção (`git show a834c53^:Code/Fracture_fibril/stress_strain_ava.py`).
Os scripts rodam contra a versão corrente sem alteração.

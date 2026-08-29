# Registro de decisões

Uma entrada por decisão, datada, **append-only**. Se um fato de uma entrada
deixar de valer, escreva uma entrada nova com a correção e cite a antiga —
nunca edite a original. `validate_review_state.py` confere isso pelo histórico
do git (checagem C3).

O estado corrente **não** mora aqui: está em `../Estado_revisao_ER12738.md`.

## Origem

As dez primeiras entradas foram extraídas de `Reviews/DAG_dependencias_revisao.md`
em 2026-08-29, quando o documento único foi dividido. Ele tinha 769 linhas e
misturava estado com histórico, o que fez o estado apodrecer: afirmava que a
campanha estava bloqueada quatro dias depois de ela terminar, e que as fibrilas
brutas estavam ausentes quando estavam num zip do próprio repositório.

Referências internas do tipo "§12 da DAG" apontam para o documento anterior.
A correspondência:

| Seção antiga | Entrada |
|:--|:--|
| §9 | `2026-08-24_N1_auditoria_citacoes.md` |
| §10 | `2026-08-24_N0_correcao_atualizacao_sigma.md` |
| §11 | `2026-08-24_N5_parkinson_varre_m.md` |
| §12 | `2026-08-24_adocao_protocolo_quenched.md` |
| §13 | `2026-08-25_consolidacao_da_dag.md` |
| §14 | `2026-08-25_faseA_saturacao_ts.md` |
| §15 | `2026-08-25_infraestrutura_campanha.md` |
| §16 | `2026-08-25_faseB_tamanhos_campanha.md` |
| §17 | `2026-08-29_faixa_dinamica_avalanches.md` |
| §18 | `2026-08-29_limpeza_repositorio.md` |

As §1–§8 (estado, grafo, arestas) foram reescritas em `../Estado_revisao_ER12738.md`.
O documento original está em `git show 99813e7:Reviews/DAG_dependencias_revisao.md`.

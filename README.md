# dla-collagen

Modelo de agregação limitada por difusão (DLA) para fibrilas de colágeno tipo I,
e a mecânica de ruptura dessas fibrilas sob um protocolo de fiber bundle com
desordem congelada.

O repositório está organizado em torno da revisão do manuscrito **ER12738**,
*Scaling behaviors in simulated collagen fibrils*, submetido ao Physical Review E.

## Por onde começar

| Quero… | Vá para |
|:--|:--|
| entender o estado da revisão | [`Reviews/Estado_revisao_ER12738.md`](Reviews/Estado_revisao_ER12738.md) |
| saber por que uma decisão foi tomada | [`Reviews/decision_log/`](Reviews/decision_log/) |
| trabalhar no repositório (política) | [`AGENTS.md`](AGENTS.md) |
| ler as críticas dos revisores | [`Reviews/Referees.md`](Reviews/Referees.md) |

O estado da revisão é verificável:

```bash
.venv/bin/python Code/Data_analysis/validate_review_state.py
```

## Estrutura

| Diretório | Conteúdo |
|:--|:--|
| `Paper/` | manuscrito LaTeX |
| `Carta_Resposta/` | carta ponto a ponto aos revisores |
| `Reviews/` | estado da revisão, registro de decisões, relatórios |
| `Code/Dla/` | gerador DLA (`fast_dla2.cpp`) |
| `Code/Fracture_fibril/` | protocolo de fratura e infraestrutura da campanha |
| `Code/Data_analysis/` | análise; `annealed_protocol/` guarda o que foi superado |
| `Code/cluster/sdumont2nd/` | ambiente e validação no SDumont2 (LNCC) |
| `Bibliography/` | fontes citadas, em PDF e em markdown |
| `Data_fibrils/` | fibrilas publicadas do artigo (zip) |

Os dados da campanha corrente **não** ficam aqui: vivem em `$DLA_PROJECT`
(`~/scratch/dla-collagen`) no SDumont2. O que está versionado são as fibrilas
publicadas, que são a referência de validação do gerador.

## Modelo, em uma frase

Moléculas de colágeno são bastões rígidos numa rede cúbica que se agregam por
difusão; um parâmetro adimensional $T_s$ controla quantas tentativas de difusão
superficial cada molécula tem após aderir, e portanto o quanto a fibrila fica
compacta. A fibrila resultante é depois carregada até a ruptura, e a estatística
das avalanches de quebra é comparada com sua arquitetura.

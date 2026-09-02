# N15 — o gerador da campanha reproduz as fibrilas publicadas (pela estrutura, não pelo $D_f$)

**Data:** 2026-09-02
**Fecha:** N15

> Entrada de registro. **Append-only** — não editar.

## O que N15 pedia, e por que o alvo mudou

A campanha foi gerada por um gerador otimizado (`fast_dla2` com `-rng fast
-jumps 1 -coverstop 1`), estatisticamente equivalente ao original mas não
bit-idêntico. N15 exigia provar que as fibrilas da campanha são "as do artigo",
e o critério previsto era o $D_f$ publicado. Esse critério caiu: o relatório da
campanha (§4) e a Fase C (§4c) mostraram que o $D_f$ publicado depende da
janela de ajuste — comparar com ele seria comparar com uma escolha.

O critério que se sustenta é a **estrutura local**: quantos vizinhos cada
molécula tem (coordenação $K$) e como as moléculas se sobrepõem (encaixes
0D–4D). São médias sobre milhares de moléculas em cada fibrila, não dependem de
janela, e já haviam validado o cilindro periódico (Fase C §4b) com tolerância
pré-registrada de 5% em $K$.

## O teste

Três fibrilas **publicadas** por condição, tiradas do zip em `Data_fibrils/`
(sementes 130/145/160 em $T_s=2$; 3130/3145/3160 em 128; 6130/6145/6160 em
8192), contra três fibrilas geradas agora com o gerador da campanha e seus flags
(sementes 100002/101002/102002, 100128/101128/102128, 108192/109192/110192;
`nb`=30.000). Mesma análise, mesma janela $|y|\le 90$ com margem de borda.
Script: `PhaseC_periodic_cylinder/compare_published_vs_campaign.py`.

## O resultado

| $T_s$ | $K$ publicadas | $K$ campanha | diferença | encaixes 0D–4D |
|---:|---:|---:|---:|:--|
| 2 | 2,777 ± 0,019 | 2,762 ± 0,016 | −0,5% (0,6σ) | dentro de 0,4 ponto |
| 128 | 4,716 ± 0,038 | 4,708 ± 0,038 | −0,2% (0,1σ) | dentro de 0,5 ponto |
| 8192 | 4,792 ± 0,115 | 4,857 ± 0,038 | +1,4% (0,5σ) | dentro de 0,5 ponto |

Tudo dentro da tolerância, por margem larga. **As fibrilas da campanha têm a
mesma estrutura local das publicadas.** A dispersão maior das publicadas em
8192 (±0,115) vem de uma das três fibrilas do artigo ser um pouco diferente das
outras duas; não afeta a conclusão.

## O que decorre

N15 fecha, e com ele o "risco aberto mais caro" que o estado carregava desde
25/08: a campanha inteira não passou por uma porta que faltava — passou por uma
porta que estava mal definida, e passa pela definição certa.

Não foi preciso o cluster: as publicadas estão no repositório e as da campanha
se regeneram em minutos com o mesmo binário.

# Teste de escala em $n_b$ — o crescimento livre não engorda a fibrila o bastante

**Data:** 2026-08-30
**Job:** SDumont2 584509, partição `cpu_amd`, 6 gerações em paralelo, 1h09.
**Dados:** `$DLA_PROJECT/nb_scaling_test/`

## Pergunta

A Fase C propõe gerar cilindros periódicos, o que exige alterar o
`fast_dla2.cpp`. Antes de pagar esse custo: bastaria **lançar mais moléculas**
no gerador atual para obter fibrilas mais grossas?

O alvo é $R_{\max} = 158$ l.u., que dá 1,5 décadas de ajuste massa-raio
(contra 0,57–0,90 hoje) e coincide com a contagem de moléculas por seção de uma
fibrila real de 200 nm (~15.000).

## Desenho

Uma fibrila por célula, **mesma semente (900001)** nos dois $n_b$, mesmo
binário, mesma execução. A única diferença entre as colunas é o número de
moléculas. Os controles em $n_b=30.000$ foram regerados em vez de reaproveitados
da campanha, para eliminar diferença de semente ou de data.

## Resultado

| $T_s$ | $R_{\max}$ (30k) | $R_{\max}$ (120k) | razão | massa/camada | comprimento |
|---:|---:|---:|---:|---:|---:|
| 2 | 37,4 | 52,3 | **1,40×** | 2,01× | 1,99× |
| 128 | 18,4 | 24,2 | **1,32×** | 2,02× | 2,01× |
| 8192 | 17,8 | 22,0 | **1,24×** | 1,94× | 1,96× |

Quadruplicar a massa **dobra o comprimento e dobra a massa por camada**. O raio
cresce pouco, e cada vez menos conforme a fibrila fica compacta.

$$R \propto n_b^{\alpha}, \qquad \alpha = 0{,}24 \;(T_s{=}2) \;\to\; 0{,}20 \;(128) \;\to\; 0{,}15 \;(8192)$$

## Consequência

Extrapolando cada expoente até $R_{\max}=158$:

| $T_s$ | $n_b$ necessário |
|---:|---:|
| 2 | $1{,}2\times10^7$ |
| 128 | $1{,}6\times10^9$ |
| 8192 | $4{,}8\times10^{10}$ |

E o custo cresce perto de $n_b^{1,5}$ (4× em $n_b$ custou mais de 4× em tempo:
~10 min para os controles, ~69 min para os de 120k).

**O crescimento livre está descartado** — não por impossibilidade de princípio,
já que a fibrila de fato engorda, mas por seis a nove ordens de grandeza de
custo. E a condição mais penalizada, $T_s=8192$, é justamente onde o ajuste de
$D_f$ é mais curto (0,57 décadas).

O cilindro periódico precisa de **180.000 moléculas em qualquer condição**,
porque o comprimento é fixo e nenhuma molécula é gasta nele. Fator $10^4$ a
$10^5$ contra o crescimento livre.

## O que este teste acrescenta ao artigo

O expoente $\alpha$ é uma propriedade estrutural do modelo que o manuscrito
nunca reportou, e ela diz que a fibrila simulada **alonga muito mais do que
engorda**. Isso dá conteúdo quantitativo à observação de Parkinson1995
(`Bibliography/Parkinson1995.md:168`): *"there must be some additional mechanism,
not included in our model, which acts to limit the maximum diameter."* Antes era
citação; agora é medida, e toca diretamente R1-4.

## Reprodução

`$DLA_PROJECT/nb_scaling_test/run.sbatch`. Saída bruta preservada em
`nb_scaling_584509.out` no mesmo diretório.
```text
=== RESULTADO: R_max na regiao central |y|<=90 ===
ts      nb        R_max      part/camada  comprimento
2       30000     37.4       70           3477      
2       120000    52.3       141          6917      
128     30000     18.4       64           3737      
128     120000    24.2       129          7521      
8192    30000     17.8       64           4069      
8192    120000    22.0       124          7981
```

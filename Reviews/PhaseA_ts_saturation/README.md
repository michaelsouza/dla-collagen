# Fase A — saturação de $T_s$: quantas condições existem de fato?

Medições de 2026-08-25 com `Code/Dla/fast_dla2.cpp` (commit `201abfe`),
`nb=30000`, uma semente (7011) por condição, aceleradores ligados.

## Pergunta

Se a difusão superficial cobre todo o componente acessível, mais $T_s$ não muda
nada. Com `-coverstop`, o gerador **para de consumir aleatoriedade** nesse ponto,
então duas condições acima da cobertura dariam fibrilas bit-idênticas para a
mesma semente. Isso permitiria eliminar condições da campanha.

## Resultado

| $T_s$ | cobriu | esgotou | passos até cobrir (média) | maior componente |
|---:|---:|---:|---:|---:|
| 2 | 0,00% | 100,00% | — | — |
| 8 | 0,35% | 99,65% | 6,1 | 509 |
| 16 | 0,94% | 99,06% | 11,1 | 432 |
| 32 | 1,49% | 98,51% | 17,9 | 229 |
| 64 | 1,70% | 98,30% | 33,0 | 173 |
| 128 | 2,66% | 97,34% | 62,3 | 118 |
| 256 | 5,27% | 94,73% | 128,9 | 117 |
| 512 | 9,81% | 90,19% | 248,9 | 123 |
| 1024 | 18,33% | 81,67% | 481,0 | 116 |
| 2048 | 34,04% | 65,96% | 946,9 | 109 |
| 4096 | 57,99% | 42,01% | 1812,4 | 105 |
| 8192 | **82,90%** | 17,10% | 3007,8 | 104 |

Nenhuma condição atinge cobertura completa. O teto `COMPONENT_CAP` nunca foi
alcançado (maior componente 509 contra teto de 4096), então o limite não é
artefato de implementação.

## Conclusões

1. **Nenhuma condição pode ser eliminada.** Com 17% das moléculas ainda
   esgotando o orçamento em $T_s=8192$, os fluxos aleatórios divergem e nenhum
   par de condições é idêntico. A grade de $T_s$ permanece como está.
2. **A cobertura depende do tamanho da fibrila.** Em `nb=2000` a cobertura em
   $T_s=8192$ é 99,8%; em `nb=30000` cai para 82,9%. O componente acessível
   cresce com o perímetro e o tempo de cobertura de um passeio aleatório vai com
   $O(n^2)$. Qualquer argumento de saturação por cobertura é, portanto,
   dependente do tamanho — relevante para a discussão de efeitos de tamanho
   finito no manuscrito.
3. **A cobertura não explica o platô de $D_f$ na região onde o artigo o situa.**
   Em $T_s=512$, onde o manuscrito afirma saturação, apenas 9,8% das moléculas
   cobriram.

## O que NÃO foi estabelecido

Tentou-se testar se $D_f$ realmente satura, usando `df_common.py` — um cálculo
de $D_f$ com **janela de raio comum** a todas as condições. O script foi
validado contra as fibrilas publicadas e **falhou**: dá 1,83 / 1,93 / 1,93 para
$T_s$ = 2 / 128 / 8192, contra 1,708 / 1,790 / 1,965 publicados.

A causa é a janela. O raio da fibrila cai de ~33 (em $T_s=2$) para ~14 (em
$T_s=8192$); uma janela fixa amostra só o núcleo denso das fibrilas abertas e
ultrapassa o objeto nas compactas. É por isso que o pipeline publicado
(`validate_fractal_proxy.py`) toma a janela de ajuste de um projeto xmgrace
**por $T_s$**.

Consequência a registrar: os valores publicados de $D_f$ dependem de uma janela
de ajuste escolhida condição a condição, e a afirmação de saturação de $D_f$ não
pode ser separada dessa escolha sem uma reanálise. Isso pertence a N7, não à
Fase A. `df_common.py` fica arquivado como registro do que foi tentado e por que
não serve.

## Reprodução

```bash
g++ -std=c++17 -O2 -o fast_dla2 Code/Dla/fast_dla2.cpp
fast_dla2 -ts <TS> -mode s -num_bind 30000 -seed 7011 \
  -rng fast -jumps 1 -coverstop 1 -output_dir <DIR>
```

A estatística de cobertura é impressa ao final quando `-coverstop 1`.

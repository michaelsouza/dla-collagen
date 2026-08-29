# Adoção do protocolo quenched e otimização do gerador

**Data:** 2026-08-24  
**Origem:** §12 de `DAG_dependencias_revisao.md`, dividida em 2026-08-29.

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

#### Decisão: adoção do protocolo fiber-bundle de desordem congelada

A varredura em $\Delta F$ com o código corrigido provou que a regra recozida
não tem limite quase-estático: $F_{rup}$ é essencialmente linear em
$\log\Delta F$ (92,6 → 188,0 para $\Delta F$ de 0,0625 a 2,0), sem platô em
cinco oitavas; o dano total por realização é conservado (~506–574), e o p99
das avalanches vai de 8 a 89 — a cauda era fixada pelo protocolo, não pela
fibrila. Decisão do autor: adotar o protocolo padrão de fiber-bundle.

**Implementação:** `Code/Fracture_fibril/fiber_bundle_ava.py`.

- Desordem congelada com correspondência exata à Eq. (4): $X_i$ com CDF
  $P(X\le x)=x^m$ em $[0,1]$, limiar $\sigma^{th}_i=K_i(t)\sigma_c X_i$
  ⇒ $P(\sigma^{th}\le\sigma)=(\sigma/(K\sigma_c))^m$ truncado em 1 — a mesma
  expressão, reinterpretada como distribuição de resistência. O canal de
  enfraquecimento por coordenação ($K_i$ corrente) é preservado.
- Carregamento quase-estático extremal: $F$ sobe até o menor
  $F^*_i=K_i\sigma_c X_i/a_i$ (com $a_i=\langle 1/N\rangle$ das seções da
  haste); cascata determinística a $F$ fixo; avalanche = total removido na
  cascata (limiar + estrutural) — exatamente a definição do Revisor 2.
- **Sem $\Delta F$, sem varredura, sem critério de parada** — R2-1 dissolve-se
  estruturalmente; R2-3 vira canônica; a comparação com 5/2 (R1-3) passa a
  ser legítima por protocolo.

**Validações:**
- Motor de cascata contra a distribuição exata de Hemmer & Hansen (ELS,
  limiares uniformes): desvio <2% até $s=8$ na rodada 150×4000.
- Testes unitários: fórmula de $F^*$ conferida à mão, monotonicidade das
  forças, esvaziamento, contagem. Suíte conjunta: 8/8.
- Piloto (1 fibrila/Ts, 15 realizações): ordenação de $F_{rup}$ e a tendência
  das avalanches com $T_s$ preservadas em relação ao protocolo antigo;
  0,2–4,3 s por realização.

#### Otimização do gerador DLA

`Code/Dla/fast_dla2.cpp`, mesma CLI e formato de saída.

- **Modo padrão bit-idêntico** ao original (store de colunas $(x,z)\to$ lista
  ordenada em $y$ no lugar da k-d tree, mesma ordem de consumo de `rand()`).
  Verificado: saídas idênticas byte a byte em ts∈{2,100} nb=300 e em
  ts∈{2,64} nb=1200 — cobrindo os dois regimes de custo (volume dominante em
  $T_s$ baixo, superfície dominante em $T_s$ alto).
- **Aceleradores** (`-rng fast -jumps 1 -coverstop 1`), estatisticamente
  equivalentes:
  - `-jumps`: saltos longos gaussianos com a covariância exata por passo
    diag(0,6; 0,2; 0,6) e comprimento $n=\text{gap}-1$ limitado pelo suporte
    ($|\delta|\le n$), de modo que o caminhante provadamente não toca o
    agregado no meio do salto;
  - `-coverstop`: encerra a difusão superficial quando o componente acessível
    de posições ligadas foi todo visitado (lei de colocação exatamente igual);
  - `-rng fast`: xoshiro256++; corrige também o bug `irand(0, 2*PI)` que
    truncava o ângulo de lançamento a $[0,6)$.
- **Medições:** nb=1200: 540 s → 3,2 s (ts=2, 171×) e 300 s → 2,7 s (ts=64,
  111×). Produção nb=30000: 279 s (ts=2) e 381 s (ts=8192) por fibrila —
  campanha de 500 fibrilas ≈ 1,5 h em 32 núcleos.
- **Validação estatística preliminar:** 1 fibrila v2-opt vs ensemble de
  produção (n=8) em nº de moléculas na janela, $\langle N\rangle$ e raio rms:
  todos $|z|\le1{,}45$, em ts=2 e ts=8192. Validação de $D_f$ em escala de
  campanha pendente.

#### Consequências na DAG

- N2, N8, N10, N11, N12 passam a depender da **recomputação sob o protocolo
  quenched** (não mais da reanálise do recozido). A Issue #5 será refeita
  sobre os novos dados.
- As respostas de R2-1/R2-3 mudam de defensivas para estruturais.
- Pendências: campanha de geração + fratura quenched; validação de $D_f$ do
  gerador otimizado em escala; texto novo das Eqs. (4)–(5) no manuscrito.

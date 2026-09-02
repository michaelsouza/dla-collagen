# Fase C — cilindro periódico: o corte das avalanches é física ou é tamanho de caixa?

Plano de validação escrito em 2026-08-27. As medições da §1 foram feitas sobre a
campanha quenched em `$DLA_PROJECT/campaign` (SDumont2), já completa: 10 $T_s$ ×
200 fibrilas × 5 valores de $m$ = 10.000 arquivos de avalanche, 2.000 fibrilas.

## 1. Por que esta fase existe

Quatro medições feitas sobre a campanha, nesta ordem. Cada uma responde à
anterior.

### 1.1 O corpo de prova é 2% a 8% do que se gera

O corte para a fratura (`stress_strain_ava.py:408`: $|x|\le8$, $|y|\le100$,
$|z|\le8$) seguido da extração do backbone deixa muito menos material do que se
imagina. Média sobre 20 fibrilas × 50 realizações, $m=2$:

| $T_s$ | partículas | moléculas | % das 30.000 | partículas/molécula |
|---:|---:|---:|---:|---:|
| 2 | 10.051 | 600 | 2,0% | 16,7 |
| 8 | 15.264 | 920 | 3,1% | 16,6 |
| 16 | 20.105 | 1.212 | 4,0% | 16,6 |
| 32 | 27.311 | 1.647 | 5,5% | 16,6 |
| 64 | 33.073 | 1.995 | 6,7% | 16,6 |
| 128 | 35.960 | 2.166 | 7,2% | 16,6 |
| 512 | 37.492 | 2.265 | 7,5% | 16,6 |
| 1024 | 38.058 | 2.297 | 7,7% | 16,6 |
| 4096 | 38.494 | 2.326 | 7,8% | 16,6 |
| 8192 | 37.663 | 2.283 | 7,6% | 16,5 |

A razão partículas/molécula fica em 16,5–16,7 nas dez condições — coerente com
bastões de 18 l.u. truncados nas bordas $y=\pm100$. Serve de teste de sanidade
da contagem.

Consequência imediata: **o número 30.000 não pode ser usado para descrever o
objeto mecânico.** Ele descreve a fibrila (objeto sobre o qual $D_f$ é medido);
o objeto fraturado tem $10^3$ moléculas e, na calibração lateral
(1 l.u. = 1,5 nm), é um prisma de $25{,}5\times25{,}5\times300$ nm.

### 1.2 A faixa dinâmica das avalanches é de uma década

Avalanches excluindo o evento terminal, $m=2$:

| $T_s$ | $N$ moléculas | frac. tam. 1 | p90 | p99 | maior não-terminal | evento terminal |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 600 | 72% | 4 | 32 | 147 | 462 (77% do sistema) |
| 32 | 1.647 | 72% | 3 | 12 | 89 | 1.436 (87%) |
| 128 | 2.166 | 72% | 3 | 12 | 91 | 1.905 (88%) |
| 1024 | 2.297 | 72% | 3 | 12 | 97 | 2.011 (88%) |
| 8192 | 2.283 | 71% | 3 | 13 | 72 | 1.988 (87%) |

Com a janela de ajuste do manuscrito ($s_{\min}\approx20$), a faixa vai de 20 a
~90: **0,56 a 0,87 décadas**. Abrindo para $s_{\min}=1$, o nominal chega a ~2
décadas, mas 72% da massa está em $s=1$ e o p99 é 12.

A distribuição é **bimodal**: chuvisco de eventos unitários, e então um único
evento terminal que leva 77% a 88% do sistema. É ruptura frágil localizada.

**Quantidade de dados não é o gargalo.** São 148 mil eventos em 20 fibrilas, e a
campanha completa tem dez vezes isso. A precisão é excelente; o que falta é
faixa de tamanhos. São coisas diferentes, e a Fase B dimensionou a campanha para
a primeira.

### 1.3 Não é escolha de $m$

Varredura completa em $T_s=128$:

| $m$ | frac. tam. 1 | p99 | maior não-terminal | evento terminal |
|---:|---:|---:|---:|---:|
| 1 | 78% | 8 | 89 | 79% do sistema |
| 2 | 72% | 12 | 91 | 88% |
| 3 | 66% | 14 | 68 | 90% |
| 5 | 61% | 17 | 69 | 91% |
| 10 | 57% | 20 | 62 | 91% |

O p99 anda de 8 a 20 — meia década — enquanto o maior evento *diminui*. A faixa
de uma década vale nas 50 combinações de $(T_s, m)$ medidas.

### 1.4 Não é o corte lateral, e não há teto para subir

Moléculas por seção transversal, por fibrila, com cortes de larguras diferentes
(média de 5 fibrilas, $|y|\le90$):

| $T_s$ | **±8 (atual)** | ±12 | ±16 | ±24 | fibrila inteira | teto de ganho |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | **61** | 118 | 185 | 279 | 308 | 5,1× |
| 32 | **134** | 219 | 271 | 295 | 295 | 2,2× |
| 128 | **176** | 269 | 290 | 295 | 295 | 1,7× |
| 8192 | **192** | 283 | 289 | 289 | 289 | 1,5× |

A coluna "fibrila inteira" é praticamente constante — 308, 295, 295, 289. Faz
sentido: são sempre 30.000 moléculas distribuídas num comprimento parecido, de
modo que o material disponível por seção é fixo em ~300. O $T_s$ decide apenas
se ele fica espalhado num anel ralo ou apertado num cilindro denso.

**Alargar o corte tem teto de 1,5× a 5×.** E o 5,1× de $T_s=2$ é otimista: o que
está fora do tronco naquela condição são galhos ramificados que a extração do
backbone removeria de qualquer forma.

O corte também não está limitando as avalanches hoje: em $T_s=128$ o sistema tem
2.166 moléculas e a maior avalanche é 91 — 4% do sistema. E ao longo da grade
$N$ cresce 3,9× enquanto a maior avalanche **cai** (147 → 72).

## 2. As duas explicações concorrentes

**(A) Seção transversal pequena demais.** Com poucos elementos por seção, a
queda de $N(i)$ ao remover algumas moléculas eleva a tensão nas restantes o
bastante para disparar o colapso da seção. Seções mais gordas permitiriam
cascatas maiores antes da ruptura, e mais décadas.

**(B) Elo mais fraco em série.** O tronco é uma pilha de ~200 camadas, ou ~12
seções independentes dado que os bastões têm 18 l.u. A ruptura ocorre na seção
mais fraca. Aumentar $N$ por seção faz cada seção convergir para a média
(flutuação cai com $1/\sqrt{N}$), o que torna as seções mais parecidas entre si
e o colapso mais simultâneo — menos décadas, não mais.

Os dados da §1.4 favorecem (B): a seção já triplicou ao longo da grade (61 →
192) e a ruptura ficou mais abrupta (terminal de 77% → 87%). A seção mais fraca
passou de 23% abaixo da média em $T_s=2$ para 19% abaixo em $T_s=8192$.

**Mas $T_s$ muda arquitetura e seção ao mesmo tempo.** O teste é confundido. Só
um experimento que varie a seção com a arquitetura fixa decide.

## 2b. O crescimento livre foi testado e descartado (2026-08-30)

Antes de escrever o modo periódico, testamos a rota barata: bastaria lançar mais
moléculas no gerador atual? **Não basta.** Job 584509, uma fibrila por célula,
mesma semente nos dois $n_b$ — detalhes em `nb_scaling_test.md`.

| $T_s$ | $R_{\max}$ (30k) | $R_{\max}$ (120k) | razão | comprimento |
|---:|---:|---:|---:|---:|
| 2 | 37,4 | 52,3 | 1,40× | 1,99× |
| 128 | 18,4 | 24,2 | 1,32× | 2,01× |
| 8192 | 17,8 | 22,0 | 1,24× | 1,96× |

Quadruplicar a massa dobra o comprimento e a massa por camada; o raio quase não
anda. $R \propto n_b^{\alpha}$ com $\alpha$ caindo de 0,24 (aberta) a 0,15
(compacta) — e a compacta é onde o ajuste de $D_f$ é mais curto.

Chegar a $R_{\max}=158$ exigiria de $1{,}2\times10^{7}$ a $4{,}8\times10^{10}$
moléculas conforme a condição, contra **180.000** no cilindro periódico. O
crescimento livre não é impossível: é seis a nove ordens de grandeza caro demais.

**O cilindro periódico deixa de ser otimização e passa a ser a única rota.**

## 3. Desenho proposto

Gerar um **cilindro periódico em $y$** com lançamento externo, e **abrir o
cilindro** antes da fratura.

- **Periodicidade em $y$** elimina pontas e afunilamento — que o corte já
  descartava — e permite gastar todas as moléculas na seção transversal em vez
  de no comprimento.
- **Lançamento externo preservado** (sorteio de $y$ uniforme no período e ângulo,
  a raio fixo) mantém o bloqueio lateral, que é o mecanismo que faz o DLA ser
  DLA. É o que o tubo fechado destruiria.
- **Abertura antes da fratura** devolve dois extremos livres, de modo que o
  motor de fratura roda **sem nenhuma alteração**: o corte em $|y|\le100$ e a
  extração do backbone de ponta a ponta continuam válidos como estão.

Ganho de escala: cada molécula ocupa 18 camadas, então 30.000 moléculas dão
540.000 fatias. Espalhadas nas ~3.800 camadas de hoje, dão ~300 por seção; num
período de 216, dão **~2.500 por seção** — 13× mais, ao mesmo custo. Em
diâmetro, a seção passa de 17 para ~65 l.u.

Notas de desenho:

- **Período 216** (= 12×18 = 54×4) ou 180. Não 201: o período precisa fechar com
  o comprimento do bastão (18) e com a regra de fixação em múltiplos de 4, senão
  a emenda quebra o padrão de encaixe.
- **Onde abrir é indiferente** — no cilindro periódico todo $y$ é equivalente.
  Isso é melhor que hoje, onde o tronco fica na região central, a mais velha e
  mais engrossada, portanto não típica.
- **Os bastões truncados voltam** no plano de abertura. É desejável: reproduz o
  mesmo tipo de borda dos corpos de prova da campanha, preservando
  comparabilidade.

## 4. Plano de validação

### 4.1 Densidade é variável de controle, não resultado

Hoje a densidade do tronco **emerge** de $n_b=30.000$ com um dado $T_s$: 61
moléculas por seção em $T_s=2$, 192 em $T_s=8192$. Num cilindro de 216 camadas,
lançar 30.000 moléculas produziria densidade muito maior, e a comparação com o
tronco atual não significaria nada — tudo diferiria já pela densidade.

**Procedimento:** ajustar $n_b$ até a densidade por camada bater com a da
campanha (tolerância 2%), na mesma condição de $T_s$; só então comparar as
demais grandezas.

### 4.2 Grandezas e tolerâncias, fixadas antes de olhar

| Grandeza | Fonte de comparação | Tolerância para "bate" |
|:--|:--|:--|
| moléculas por seção | §1.4 desta nota | 2% (é a variável de controle) |
| coordenação $\langle K\rangle$ | campanha, mesma $T_s$ | 5% |
| área de seção $\langle N\rangle$ | campanha, mesma $T_s$ | 5% |
| $D_f$ em seção transversal | `validate_fractal_proxy.py` | 0,02 em valor absoluto |
| $F_{rup}$ | campanha, mesma $T_s$ | dentro da barra de erro da Fase B |
| p99 e maior avalanche não-terminal | §1.2 desta nota | dentro da barra de erro da Fase B |
| fração do evento terminal | §1.2 desta nota | 3 pontos percentuais |

O motivo de fixar a lista antes é evitar o resultado sempre favorável: comparar
dez grandezas, ver nove baterem e declarar validado.

### 4.3 Tamanhos de amostra

As grandezas não têm todas a mesma variabilidade entre fibrilas, e isso decide
quantas fibrilas são necessárias.

- **Estruturais** ($K$, $N$, densidade, $D_f$): são médias sobre milhares de
  moléculas dentro de cada fibrila. **5 fibrilas por condição bastam** para
  enxergar diferenças de poucos por cento.
- **Mecânicas** ($F_{rup}$, cauda das avalanches): a Fase B mediu a dispersão —
  com 20 fibrilas, SE($\gamma$) fica entre 0,027 e 0,060. **20 fibrilas × 50
  realizações por condição**, que é exatamente o desenho do piloto da Fase B,
  de modo que o poder estatístico já é conhecido e a comparação é direta.

Com menos que isso, a conclusão "não afetou" seria indistinguível de "não
consegui ver". É o principal risco deste plano.

### 4.4 Condições e previsão registrada

Três condições: $T_s = 2$, $128$, $8192$ — as duas pontas e o meio.

**Previsão, registrada antes de rodar:** as pontas da fibrila bloqueiam
moléculas que iriam para o meio, e esse bloqueio pesa mais onde a estrutura é
aberta e ramificada. Portanto **espera-se concordância em $T_s=8192$ e é em
$T_s=2$ que pode falhar**. Se o resultado for o oposto, alguma suposição deste
plano está errada e cabe investigar antes de prosseguir.

Depois da validação no tamanho atual, dois passos:

1. **Auto-correlação pela volta.** Gerar com período 216 e 432 e comparar
   densidade e coordenação. Se o período curto for insuficiente, o cilindro
   enxerga a si mesmo pela imagem periódica.
2. **Engordar** a seção até ~65 l.u. e medir se o corte das avalanches se move.

## 4b. Passo 1 executado — o cilindro reproduz a estrutura local (2026-09-01)

Gerador com `-period 216` (commit `17cfc1f`). Modo livre verificado
**byte-idêntico** ao anterior nos dois caminhos (libc sem aceleradores; RNG
rápido com `-jumps -coverstop`). Sem artefato na emenda: 12 faixas de 18
camadas com média 299 moléculas, desvio 32, a faixa da costura a +1,06 desvio.

Cinco sementes por célula, `nb`=3.600 no cilindro (300 moléculas/seção, a
densidade da fibrila livre). Análise em `compare_local_structure.py`.

| $T_s$ | $K$ livre | $K$ periódica | diferença | tolerância |
|---:|---:|---:|---:|---:|
| 2 | 2,770 ± 0,024 | 2,790 ± 0,017 | +0,7% (0,7σ) | 5% ✓ |
| 128 | 4,716 ± 0,054 | 4,825 ± 0,022 | +2,3% (1,9σ) | 5% ✓ |
| 8192 | 4,870 ± 0,060 | 4,940 ± 0,034 | +1,4% (1,0σ) | 5% ✓ |

Encaixes 0D–4D coincidem dentro de 2,4 pontos percentuais e reproduzem a
migração para 0D/1D em $T_s$ alto que Parkinson1995 descreve (11/23/22/22/22
em $T_s=2$; 22/28/19/16/15 em $T_s=8192$).

**Viés pequeno e consistente:** $K$ periódico é maior nas três condições e o
0D é sempre menor. Nenhum passa de 2σ isolado, mas o sinal repetido sugere
efeito real — provavelmente a ausência da franja externa mal-conectada que a
fibrila livre carrega. Dentro da tolerância; registrado como primeira hipótese
caso o $D_f$ do cilindro largo divirja do publicado.

**Um erro de análise pego no caminho:** a primeira comparação deu $K$ 5,5%
maior e 4,5σ, e quase virou "as pontas importam". Era a janela da fibrila
livre sem margem — hastes na borda perdiam vizinhos logo fora, subestimando o
$K$ livre. Documentado no cabeçalho do script.

**Escala do cilindro, medida:** $R \propto n_b^{0{,}55}$ (35,2 → 111,2 de
`nb`=3.600 a 28.800). Para $R_{\max}=158$ bastam **~56.000 moléculas**, não as
180.000 estimadas a partir da fibrila livre.

**Perda operacional:** os 30 arquivos da comparação e o analisador original
estavam em `/tmp` e foram apagados pelo sistema. Os números acima sobreviveram
na conversa; o script foi reescrito no repositório. Tudo passou a ir para o
scratchpad da sessão, como o `AGENTS.md` já mandava.

## 4c. Passo 2a executado — o $D_f$ (2026-09-01)

**Antes de tudo:** `Reviews/quenched_campaign_report/README.md` §4, da outra
sessão, já havia estabelecido — sobre as fibrilas livres da campanha — que o
$D_f$ publicado depende da janela de ajuste, que qualquer regra uniforme dá
~1,95 em $T_s=64$–$128$ onde o artigo publicou 1,76–1,79, e que os valores
intermediários são *crossover* entre DLA puro (~1,7) e sólido compacto (2,0),
não uma dimensão variando. Aquele relatório **fecha N7**. O que segue é
corroboração por um objeto independente, com o *ensemble* que a ressalva final
daquela §4 pedia.

Cinco cilindros periódicos por condição, `nb`=60.000 (5.000 partículas por
seção, 17× a fibrila livre), $R_{\max}$ de 68 a 161. Dados e receita de
regeneração em `df_wide_cylinders.csv`; inclinações locais em
`df_local_slopes_wide.csv`; método em `measure_df_periodic.py`.

| $T_s$ | $R_{\max}$ | décadas | fixa $4$–$8$ | relativa $0{,}15R$–$0{,}5R$ | faixa cheia $5$–$R_{\max}$ | publicado | relatório (fixa / rel.) |
|---:|---:|---:|---:|---:|---:|---:|:--|
| 2 | 161 ± 11 | 1,51 | 1,96 ± 0,23 | **1,675 ± 0,023** | 1,617 ± 0,020 | 1,708 | 1,722 / 1,676 |
| 128 | 86 ± 5 | 1,24 | **1,964 ± 0,041** | 1,691 ± 0,047 | 1,577 ± 0,045 | 1,790 | 1,959 / 1,953 |
| 8192 | 68 ± 3 | 1,13 | 1,946 ± 0,031 | **1,955 ± 0,012** | 1,753 ± 0,042 | 1,963 | 1,964 / 1,981 |

**O que confirma.** Nos extremos, cilindro e relatório coincidem à terceira
casa (1,675 vs 1,676 em $T_s=2$; 1,955 vs 1,981 e 1,946 vs 1,964 em 8192) e
batem com o publicado. Em $T_s=128$ a janela fixa também coincide (1,964 vs
1,959) — e **nenhuma regra reproduz o 1,790 publicado**.

**O que acrescenta.** Três coisas que a fibrila livre não podia dar:

1. *Alcance.* Em $T_s=2$ o ajuste cobre 1,5 década e o $D_f$ relativo fica em
   1,675 ± 0,023 — o valor de DLA bidimensional, agora sobre um intervalo de
   escala real, com barra de erro entre sementes.
2. *A anomalia de $T_s=128$ é evidência, não ruído.* A janela relativa dá 1,69
   no cilindro e 1,95 na fibrila livre porque $0{,}15R$–$0{,}5R$ cai em
   $r=13$–$43$ num objeto de $R=86$ e em $r=3$–$10$ num de $R=20$. Uma regra
   "invariante de escala" devolve valores diferentes conforme o tamanho —
   **porque em $T_s=128$ não há invariância de escala**. As inclinações locais
   com 5 sementes descem sem patamar: 1,93 → 1,87 → 1,78 → 1,67 → 1,73 → 1,41 →
   0,48 de $r=5$ a $90$.
3. *Controle de objeto.* Uma fibrila livre gerada pelo mesmo binário e medida
   pelo mesmo script, em $T_s=128$: faixa cheia 1,582 (cilindro 1,577), fixa
   1,944 (cilindro 1,964). Periódico e livre dão o mesmo número sob cada regra.
   A distância ao publicado é a janela, não a geometria.

**Ressalva.** A janela fixa $4$–$8$ em $T_s=2$ tem desvio 0,23 entre sementes:
oito unidades de raio numa seção aberta e fractal contêm poucas dezenas de
partículas, e o eixo carrega a coluna-semente. É a regra errada para a
estrutura aberta; a relativa é a que se sustenta ali.

**Para o manuscrito.** O que o relatório propõe fica reforçado: não "$D_f$ cresce
de 1,71 a 1,96", e sim "em $T_s$ baixo a seção é um agregado DLA com
$D_f \approx 1{,}68$ sobre 1,5 década; conforme $T_s$ cresce o regime fractal
encolhe até desaparecer e a seção passa a ser compacta ($D=2$)". Isso resolve o
lado estrutural da I9 sem ampliar nada — substituindo um número ajustado onde
não há lei de potência por uma descrição do que há.

**O que a Fase C ainda deve.** O lado das avalanches (passo 2b): o cilindro
largo de $T_s=128$ fraturado pela janela padrão 17×17 reproduz a campanha
(frac. tam. 1 = 0,75; p99 = 9; terminal = 2.077 moléculas); a fratura pela
seção inteira (181×181, 1,08 milhão de partículas) está em execução.

## 4d. Passo 2b em curso — a escada de janelas e o que cada hipótese prevê (2026-09-01)

**Desenho.** Um único cilindro periódico largo de $T_s=128$ (`nb`=60.000, semente
900001), aberto e fraturado com o motor de produção sem alteração, por quatro
janelas de corte. Só a janela muda; a arquitetura é a mesma. Script:
`summarize_avalanche_ladder.py`.

| janela | moléculas | fator sobre a base |
|:--|---:|---:|
| 17×17 (padrão da campanha) | 2.372 | 1× |
| 41×41 | 12.023 | 5,1× |
| 81×81 | 36.812 | 15,5× |
| 181×181 (seção inteira) | 58.783 | 24,8× |

**Previsões, registradas antes dos degraus grandes saírem.** Com uma ou duas
realizações por janela, o *maior* evento não serve de estatística — os 91 da
campanha são o máximo sobre 1.000 realizações. O que compara entre tamanhos é a
forma da distribuição e a fração do sistema que vai no evento terminal:

| | corte **dinâmico** (hipótese B, §2) | corte de **tamanho finito** (hipótese A) |
|:--|:--|:--|
| p99 das avalanches pré-terminais | fica em ~10 em todas as janelas | cresce com $N$ (com $s_c \propto N^{\alpha}$, $\alpha>0$) |
| fração do sistema no evento terminal | fica em ~0,88 | cai, porque as cascatas pré-terminais absorvem mais |
| fração de eventos de tamanho 1 | fica em ~0,75 | cai |

**Observado até agora:**

| janela | realizações | frac. tam. 1 | p90 | p99 | maior pré-terminal | terminal / $N$ |
|:--|---:|---:|---:|---:|---:|---:|
| campanha (referência) | 1000 | 0,72 | 3 | 12 | 91 | 0,88 |
| 17×17 | 5 | 0,75 | 2 | 10 | 39 | 0,88 |
| 41×41 | 3 | 0,75 | 3 | 11 | 127 | 0,87 |
| 81×81 | em execução | | | | | |
| 181×181 | em execução | | | | | |
| *$T_s=8192$, mesmo desenho:* | | | | | | |
| campanha 8192 (referência) | 1000 | 0,71 | 3 | 13 | 72 | 0,87 |
| 17×17 no cilindro 8192 | 5 | 0,73 | 3 | 14 | 40 | 0,88 |
| 141×141 (seção inteira, 58.322 mol.) | em execução | | | | | |

O primeiro degrau (5,1× em $N$) não move nenhuma das três colunas de forma
(frac. 1, p90, p99, terminal/$N$). Mas a terceira realização produziu **uma**
cascata pré-terminal de 127 moléculas — maior que qualquer uma das 1.000
realizações da campanha em 17×17 (máximo 91). Uma ocorrência em três não decide
nada, e o máximo foi excluído do critério por isso mesmo; fica registrado porque,
se os degraus grandes mostrarem p99 parado e o máximo crescendo, a leitura
correta será: **o corte da distribuição é dinâmico, mas a maior cascata
alcançável cresce com o sistema** — duas afirmações compatíveis, e a segunda
importa para como N10 será escrito. Os dois degraus seguintes cobrem mais de uma
década em $N$ e decidem.

**Nota operacional.** O carregador original construía vizinhanças por
todos-os-pares por camada ($2{,}3\times10^8$ pares numa janela 41×41, horas
numa seção inteira); foi trocado por *hash* espacial com resultado idêntico
(commit `ab128dc`). O custo restante é a re-extração do backbone a cada passo de
cascata (`filter_rids`, 93% do tempo no *profile*), que escala como $N^{2}$:
5 s por realização em 17×17, 202 s em 41×41, ~1,5 h previstos na seção inteira.

## 5. Decisão conforme o resultado

O teste de tamanho finito compara cilindro fino com cilindro gordo, **dentro da
família periódica**. Ele não depende da validação contra a campanha:

| Validação | Teste de tamanho | O que se pode afirmar |
|:--|:--|:--|
| passa | corte se move com a seção | explicação (A); os números do artigo são de tamanho finito e precisam ser requalificados |
| passa | corte fica parado | explicação (B); o corte é dinâmico, e isso vira resultado positivo contra R1-2 / R2-4 |
| falha | qualquer | a pergunta é respondida dentro de um modelo aparentado; a diferença em relação à campanha vira achado sobre o papel das pontas |

Nos três casos sai resultado. É o que justifica rodar.

## 6. Custo

Geração: 10,6 min-núcleo por fibrila em $n_b=30.000$ (Fase B). Vinte fibrilas em
três condições ≈ **11 CPU-h**. Fratura: 9,2 s por realização × 50 × 60 fibrilas
≈ **8 CPU-h**. O cilindro gordo custa 2–3× por fibrila.

Total da validação abaixo de **20 CPU-h** — meia hora em 24 núcleos. Não há
motivo para economizar em número de fibrilas.

Comparação: obter a mesma seção transversal por fibrilas maiores exigiria
$n_b=300.000$, ~10× o custo atual por fibrila, 1 a 3 h cada.

## 7. Pendências de implementação

1. Modo periódico em `fast_dla2.cpp`: fronteira em $y$, lançamento cilíndrico,
   raio de morte radial. A CLI e o formato de saída devem permanecer.
2. Escritor que abre o cilindro num plano e emite no esquema `extended`, para
   que `worker_fracture.sh` consuma sem alteração.
3. Verificação de que o padrão de encaixe (staggers 0D–4D) não quebra na emenda
   com período 216.

## 8. Relação com a DAG

Esta fase é a montante de **N10** (reanálise estatística), **N11** (expoente
frente a $5/2$) e **N12** (estatuto da relação $D_f \leftrightarrow$ ruptura).

A §1.2 já basta para questionar N11: um expoente ajustado sobre 0,7 décadas não
sustenta comparação com um valor de campo médio. E a §1.1 expõe um
confundimento novo para N12 — ao correr a grade de $T_s$, o número de moléculas
do corpo de prova varia 3,9× junto com $D_f$, de modo que as duas quantidades
não são descritores independentes. Alargar o corte até a fibrila inteira
tornaria a seção ~300 em todas as condições e isolaria arquitetura de tamanho;
é barato, e independente desta fase.

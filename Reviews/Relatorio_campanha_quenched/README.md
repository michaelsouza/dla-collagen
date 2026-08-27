# Relatório — campanha quenched (ER12738)

Resultados do conjunto de dados gerado sob o protocolo de fibra em feixe com desordem congelada, depois da correção do cálculo de $\sigma$ (`a834c53`) e da troca do protocolo de carga (§12 da DAG).

| | |
|:--|:--|
| Fibrilas | 2 000 (10 $T_s$ × 200) |
| Realizações | 500 000 (10 $T_s$ × 200 fibrilas × 5 valores de $m$ × 50) |
| Eventos | 79 719 965, dos quais 19 508 453 selecionados |
| Geração | job 576131 no SDumont2, 1 h 43 min, 384 núcleos |
| Verificação | 10 000/10 000 por conteúdo; 0 falhas; 0 claims órfãos |
| Dados | `$DLA_PROJECT/campaign/` (1,7 GB de fratura, 21 GB de fibrilas) |

Este documento cresce por figura. Cada seção traz a imagem, os números, o código que a produziu, o algoritmo em resumo e as ressalvas.

---

## Figura 1 — o diâmetro da fibrila ao longo do seu eixo

![Perfil de diâmetro de seção transversal](fig01_perfil_diametro.png)

*Painel esquerdo: diâmetro de giração em função da posição ao longo do eixo, para $T_s$ = 2, 16, 64 e $\geq$ 512. Painel direito: diâmetro na região central em função de $T_s$. 25 fibrilas por condição; camadas sustentadas por menos de 20 fibrilas (as pontas) foram omitidas. As curvas de $T_s$ = 512 a 8192 se sobrepõem e por isso recebem um rótulo único.*

### O que o gráfico mostra

**A fibrila não é um cilindro — é um fuso.** Mais grossa na semente ($y = 0$) e afinando monotonicamente até as pontas, ao longo de ~3 900 sítios de rede. O perfil é simétrico em torno da semente, o que é esperado para agregação por difusão a partir de um germe central: a semente teve todo o tempo de deposição para engrossar, as pontas são recentes.

**A difusão superficial compacta a fibrila.** Do menor ao maior $T_s$ o diâmetro no miolo cai por um fator de 2,15, enquanto o comprimento cresce apenas 9%. Como o número de moléculas é fixo em 30 000, o volume ocupado cai por um fator de $\approx 4{,}2$ — a mesma massa num envelope quatro vezes menor.

**A queda para.** De $T_s = 512$ a 8192, um fator 16 na difusão superficial, o diâmetro varia 1,2%. As quatro condições do platô são estatisticamente indistinguíveis entre si, separadas por menos de um erro padrão.

### Valores medidos

Média sobre 25 fibrilas por condição, na região central $|y| \leq 100$. O erro é o erro padrão **entre fibrilas** — a incerteza correta para comparar condições. Todas as grandezas em sítios de rede.

| $T_s$ | $d_{gyr}$ | $d_{max}$ | $d_{max}/d_{gyr}$ | comprimento |
|---:|---:|---:|---:|---:|
| 2 | 35,33 ± 0,35 | 66,29 ± 0,92 | 1,876 | 3 571 |
| 8 | 30,75 ± 0,37 | 57,83 ± 0,84 | 1,881 | 3 668 |
| 16 | 26,78 ± 0,38 | 50,90 ± 0,73 | 1,901 | 3 742 |
| 32 | 22,15 ± 0,23 | 43,21 ± 0,76 | 1,951 | 3 768 |
| 64 | 18,95 ± 0,19 | 37,56 ± 0,69 | 1,982 | 3 839 |
| 128 | 17,63 ± 0,18 | 32,90 ± 0,85 | 1,866 | 3 849 |
| **512** | **16,34 ± 0,08** | **28,02 ± 0,29** | **1,714** | 3 922 |
| **1024** | **16,42 ± 0,09** | **28,01 ± 0,21** | **1,706** | 3 892 |
| **4096** | **16,54 ± 0,18** | **29,36 ± 0,72** | **1,774** | 3 864 |
| **8192** | **16,46 ± 0,05** | **28,59 ± 0,22** | **1,737** | 3 894 |

O comprimento é a extensão total em $y$, incluindo as pontas omitidas do gráfico.

**A razão $d_{max}/d_{gyr}$ não é monotônica.** Ela é um índice de irregularidade da seção: quanto maior, mais a envolvente é ditada por protuberâncias isoladas em vez do corpo da seção. Sobe até 1,98 em $T_s = 64$ e **cai** para $\approx 1{,}72$ no platô. A superfície fica relativamente mais lisa exatamente onde o tamanho para de mudar — dois indícios independentes apontando para a mesma transição.

### Código utilizado

| arquivo | papel |
|:--|:--|
| `Code/Data_analysis/fibril_diameter_profile.py` | percorre os compactos e escreve um CSV com uma linha por ($T_s$, camada $y$) |
| `Code/Data_analysis/plot_fibril_diameter.py` | lê o CSV e desenha os dois painéis |
| `Code/Data_analysis/test_fibril_diameter_profile.py` | quatro verificações de geometria com resposta conhecida |

```bash
python3 Code/Data_analysis/fibril_diameter_profile.py \
    --compact-dir $DLA_PROJECT/campaign/fibrils/compact \
    --out-csv     $DLA_PROJECT/campaign/analysis/diameter/profile.csv \
    --fibrils 25

python3 Code/Data_analysis/plot_fibril_diameter.py
```

Commit `2b1ad4c`. A execução completa sobre as dez condições leva **5 segundos**
no nó de login do SDumont2.

### Algoritmo

**Entrada.** A saída *compacta* do gerador, uma linha por molécula (`uid: id x y z`, com $y$ = base da haste). Cada molécula ocupa 18 camadas consecutivas, de $y$ a $y+17$, sempre no mesmo par $(x, z)$. Os arquivos estendidos têm a mesma informação com 18× o tamanho — 1,2 GB contra 20 GB — então não há motivo para lê-los.

**Acumulação.** Para cada camada é preciso o centroide e a dispersão das partículas que a ocupam. Materializar as 540 000 partículas de cada fibrila é desnecessário, porque a variância só depende de somas. O algoritmo faz **18 passagens** — uma por deslocamento dentro da haste — acumulando por camada a contagem e as somas de $x$, $z$, $x^2$ e $z^2$. Daí saem, em forma fechada:

$$
c = (\langle x\rangle,\ \langle z\rangle), \qquad
\langle |r-c|^2 \rangle = \langle x^2\rangle - \langle x\rangle^2
                        + \langle z^2\rangle - \langle z\rangle^2
$$

$$
d_{gyr} = 2\sqrt{\langle |r-c|^2 \rangle}, \qquad
d_{max} = 2\max|r-c|
$$

O $d_{max}$ exige os extremos e não sai de somas, então custa mais 18 passagens de máximo. Toda a acumulação usa indexação dispersa do NumPy (`np.add.at`, `np.maximum.at`), sem laço em Python sobre moléculas.

**Duas definições, de propósito.** O $d_{gyr}$ é um segundo momento: pesa o corpo
da seção e é insensível a uma partícula distante. O $d_{max}$ é fixado pela
partícula mais distante e é a grandeza que os ajustes massa–raio publicados usam.
Para um agregado fractal as duas discordam, e a razão entre elas é informativa
por si — como se vê na coluna $d_{max}/d_{gyr}$.

**Agregação entre fibrilas.** Por coordenada $y$ absoluta. A semente ocupa
$y \in [-9, 8]$ em toda fibrila, então $y = 0$ é uma origem comum genuína, não um
alinhamento imposto.

### Ressalvas

1. **São 25 fibrilas por condição, não as 200 disponíveis.** Suficiente para o
   gráfico e para o erro padrão da tabela, mas o platô merece o ensemble completo
   antes de virar afirmação no manuscrito. O custo é trivial: 5 s viram ~40 s.
2. **Saturação do diâmetro não implica saturação de $D_f$.** São grandezas
   diferentes — uma é tamanho, a outra é dimensão fractal. A coincidência do
   ponto de saturação é sugestiva, não demonstrativa.

### Por que isto importa para a revisão

O manuscrito situa o platô de $D_f$ em $T_s \approx 512$. A Fase A mediu a
cobertura de difusão superficial e mostrou que ela **não** satura ali: apenas 9,8%
das moléculas cobrem o componente acessível em $T_s = 512$, contra 82,9% em 8192
(ver `Reviews/PhaseA_ts_saturation/README.md`). O mecanismo de cobertura,
portanto, não explica o platô — o que enfraquecia a resposta a R1-5 / N12.

Aqui está um observável estrutural independente que satura exatamente onde o
artigo diz, e que **não depende de janela de ajuste por condição** — justamente a
fragilidade identificada nos $D_f$ publicados (§14 da DAG).

---

## Figura 2 — morfologia da seção central e ordem de incorporação

![Segmentos centrais projetados no plano x-z](fig02_secoes_centrais.png)

*Segmentos centrais ($|y| \leq 25$) projetados no plano $x$–$z$, para $T_s$ = 2, 64, 512 e 8192. Cada sítio ocupado é pintado com o índice da primeira molécula que o ocupou, de modo que a cor lê "quando esta coluna foi construída". **Os quatro painéis compartilham a mesma escala espacial**; a barra no primeiro painel mede 20 sítios de rede. Sementes 100000, 104000, 106000 e 109000.*

Reproduz a Figura 2 do manuscrito a partir das fibrilas da campanha nova.

### O que o gráfico mostra

A transição descrita no artigo aparece igual: morfologia **esparsa e irregular** em $T_s$ baixo, passando por densa com protuberâncias, até **empacotamento denso e radialmente simétrico** em $T_s$ alto. A fração de preenchimento da caixa envolvente quantifica isso.

| $T_s$ | sítios ocupados | preenchimento |
|---:|---:|---:|
| 2 | 858 | 0,21 |
| 64 | 526 | 0,51 |
| 512 | 436 | 0,82 |
| 8192 | 454 | 0,94 |

O gradiente de cor mostra o mecanismo. Em $T_s = 2$ as moléculas antigas (azul) formam um esqueleto ramificado e as recentes (vermelho) se depositam nas pontas dos braços, sem preencher os vãos — é blindagem difusiva clássica. Em $T_s = 8192$ o núcleo antigo é compacto e as moléculas recentes formam uma **casca externa contínua**: a difusão superficial permite que a molécula desça para os vãos antes de fixar, então o crescimento é camada a camada em vez de dendrítico.

### Diferença deliberada em relação à figura publicada

Na figura do artigo cada painel parece normalizado ao próprio tamanho, o que faz os quatro aparentarem largura semelhante e **esconde a compactação**. Aqui a escala é comum: $T_s = 2$ preenche o quadro e $T_s = 8192$ ocupa cerca de um terço dele.

Isso mantém a Figura 2 consistente com a Figura 1, que mede a mesma compactação como número. Com escala independente por painel, as duas figuras diriam coisas diferentes sobre o mesmo fenômeno.

### Código utilizado

| arquivo | papel |
|:--|:--|
| `Code/Data_analysis/plot_central_sections.py` | lê os compactos, recorta a fatia central e desenha os quatro painéis |

```bash
python3 Code/Data_analysis/plot_central_sections.py
```

Reusa `read_compact` de `fibril_diameter_profile.py`.

### Algoritmo

**Recorte.** Molécula entra no painel se a base da haste satisfaz $|y| \leq 25$. Cada molécula guarda o seu índice de chegada — a ordem em que o gerador a ligou ao agregado, de 0 (semente) a 30 000.

**Projeção.** Uma coluna $(x, z)$ pode ser ocupada por várias moléculas em alturas diferentes. O sítio recebe o índice da **primeira** a ocupá-lo. Na implementação, os índices são ordenados de forma decrescente antes da escrita na grade, de modo que o menor é o último a ser gravado e vence.

**Preenchimento.** Razão entre sítios ocupados e a área da caixa envolvente da fatia, $(\Delta x + 1)(\Delta z + 1)$.

### Escolhas que precisam ser declaradas se a figura for para o manuscrito

1. **A espessura da fatia não é neutra.** A legenda original diz "segmento central" sem quantificar. Em $|y| \leq 25$ o preenchimento vai de 0,21 a 0,94; em $|y| \leq 400$ vai de 0,52 a 0,90 e os braços dendríticos desaparecem — uma fatia grossa empasta a projeção e destrói justamente o contraste que a figura existe para mostrar. Foi por isso que se escolheu 25. 
2. **As sementes são as primeiras de cada condição, não escolhidas.** Convém verificar se são representativas do ensemble antes da publicação; se forem selecionadas, a seleção precisa ser declarada.
3. **Mapa de cores.** Usa-se `turbo` em vez de `jet` — mesma aparência azul→vermelho, sem as bandas falsas que o `jet` introduz.

---

## Figura 3 — compactação da seção transversal

![Densidade local, coordenação e razão de densidade em função de T_s](fig03_compactacao.png)

*Painel (a): densidade local $\rho(r)=N(r)/\pi r^2$ das seções transversais; cada curva termina em $R/2$, o maior raio ainda dentro do corpo da sua condição. Painel (b): coordenação — fração dos 4 vizinhos de rede ocupados. Painel (c): razão $\rho(3)/\rho(R/2)$, que vale 1 para densidade uniforme. 25 fibrilas por condição, 11 seções por fibrila. Barras de erro: erro padrão entre fibrilas.*

**Nenhuma grandeza desta figura envolve ajuste de reta ou janela de escala.** Essa é a razão de ela existir — ver a subseção final.

### O que o gráfico mostra

**Painel (a) é o mecanismo.** Um objeto compacto tem densidade uniforme: $\rho(r)$ é uma reta horizontal. Um fractal de dimensão $D$ tem $\rho \sim r^{D-2}$, isto é, densidade que **cai** conforme se olha mais longe, porque há buracos em toda escala. Em $T_s = 2$ a curva desce de 0,31 a 0,18; em $T_s \geq 512$ ela é plana. A transição de fractal para compacto se lê direto, sem ajustar nada.

**Painel (b) é o empacotamento local.** A coordenação não usa centroide, raio nem janela — só conta quantos dos 4 vizinhos de rede estão ocupados. Vai de 0,34 a 0,76: em $T_s$ baixo uma molécula tem em média 1,4 vizinhos, em $T_s$ alto tem 3,0.

**Painel (c) mede quanto ainda resta de fractal.** A razão $\rho(3)/\rho(R/2)$ vale 1 se a densidade for uniforme e cresce conforme a estrutura fica rarefeita para fora. Cai de 1,68 para 1,02 e fica **indistinguível de compacto a partir de $T_s = 128$**.

### Valores medidos

| $T_s$ | $R$ | coordenação | $\rho(3)/\rho(R/2)$ | $D$ implícito |
|---:|---:|---:|---:|---:|
| 2 | 33,1 | 0,342 ± 0,001 | 1,683 ± 0,034 | 1,695 |
| 8 | 29,0 | 0,439 ± 0,001 | 1,679 ± 0,047 | 1,671 |
| 16 | 25,5 | 0,514 ± 0,002 | 1,527 ± 0,045 | 1,707 |
| 32 | 21,6 | 0,591 ± 0,002 | 1,311 ± 0,035 | 1,789 |
| 64 | 18,8 | 0,656 ± 0,001 | 1,130 ± 0,016 | 1,893 |
| 128 | 16,5 | 0,693 ± 0,001 | 1,065 ± 0,016 | 1,938 |
| 512 | 14,0 | 0,736 ± 0,001 | 1,034 ± 0,008 | 1,961 |
| 1024 | 14,0 | 0,750 ± 0,001 | 1,041 ± 0,005 | 1,952 |
| 4096 | 14,7 | 0,757 ± 0,001 | 1,033 ± 0,013 | 1,964 |
| 8192 | 14,3 | 0,760 ± 0,001 | 1,018 ± 0,007 | 1,979 |

A coluna final não é um ajuste. Como $\rho \sim r^{D-2}$, a razão de duas densidades medidas implica

$$ D = 2 + \frac{\ln\left[\rho(3)/\rho(R/2)\right]}{\ln\left(6/R\right)} $$

**E o resultado bate com o ajuste.** O $D$ implícito dá 1,695 em $T_s = 2$ e 1,979 em 8192, contra 1,722 e 1,964 obtidos por regressão sobre a janela fixa. Ou seja: ao trocar $D_f$ por compactação **não se está abandonando a física, e sim medindo-a sem a escolha livre**. É um argumento bem mais forte perante um revisor do que mudar de assunto.

Note também que os dois observáveis não saturam no mesmo ponto. A razão de densidade estabiliza em $T_s = 128$; a coordenação continua subindo devagar até o topo da grade (0,736 → 0,760 de 512 a 8192, uma variação de 3,3%). São coisas diferentes: a primeira diz que acabou o regime fractal, a segunda que o empacotamento local ainda melhora um pouco depois disso.

### Código utilizado

| arquivo | papel |
|:--|:--|
| `Code/Data_analysis/fibril_compaction.py` | calcula coordenação, perfil de densidade e razão por fibrila |
| `Code/Data_analysis/plot_fibril_compaction.py` | desenha os três painéis |

```bash
python3 Code/Data_analysis/fibril_compaction.py 25
python3 Code/Data_analysis/plot_fibril_compaction.py
```

Reusa `parse_grown_sections` e `mass_radius_for_sections` de `validate_fractal_proxy.py`, então a amostragem de seções é idêntica à do pipeline publicado. A execução leva 12 s.

### Algoritmo

**Coordenação.** Para cada seção, monta-se o conjunto de sítios $(x,z)$ ocupados e conta-se, para cada sítio, quantos dos 4 vizinhos de rede estão no conjunto. O valor é a soma dividida por $4N$. Uma partícula isolada dá 0; uma no interior de um sólido dá 1. Não há parâmetro algum.

**Densidade local.** A partir da curva massa–raio $N(r)$ de cada seção, $\rho(r) = N(r)/\pi r^2$. Os perfis são interpolados em $r/R$ antes de serem promediados, para que condições de tamanhos diferentes sejam comparáveis.

**Razão.** Avaliada entre $r = 3$ — o corte de rede, abaixo do qual se contam pixels e não estrutura — e $r = R/2$, o maior raio cujo círculo ainda está dentro do corpo da seção. Acima de $R/2$ o círculo começa a sair do objeto e $\rho$ cai por motivo geométrico trivial, não por fractalidade.

### Ressalvas

1. **A razão não é totalmente livre de escolhas.** Ela usa $r=3$ e $r=R/2$. A diferença em relação ao ajuste de $D_f$ é que ambas são principiadas (corte de rede; metade do objeto), aplicadas uniformemente, e o resultado é uma razão entre duas densidades **medidas** — não a inclinação de uma reta ajustada onde não há lei de potência. A coordenação, essa sim, não tem escolha nenhuma.
2. **A coordenação é sensível à rede.** Ela é natural aqui porque o modelo é de rede, mas não tem análogo direto em dados experimentais.

### Por que não uma figura de $D_f$

![Diagnóstico: D_f e a janela que o define](fig03b_df_janelas.png)

*Material de apoio, mantido como evidência da pendência N7.*

A dimensão fractal só existe se a inclinação de $\log N$ contra $\log r$ for constante ao longo de um intervalo de $r$. Essa constância **é** a definição. Toda medida tem dois cortes: embaixo a rede ($r \gtrsim 3$), em cima o próprio objeto ($r \lesssim R/2$). O que sobra nas nossas fibrilas:

| $T_s$ | $R$ | intervalo utilizável | décadas |
|---:|---:|:--|---:|
| 2 | 33 | 3 → 17 | 0,74 |
| 64 | 19 | 3 → 9 | 0,50 |
| 8192 | 14 | 3 → 7 | 0,38 |

Ajustar um expoente de lei de potência sobre um fator 2,4 não é medir. O padrão da área pede ao menos uma década.

A consequência é mensurável. Recalculando $D_f$ sobre as fibrilas da campanha, os extremos reproduzem o publicado (1,722 contra 1,708; 1,964 contra 1,965) mas o meio não: em $T_s = 64$ e 128 a diferença chega a **0,16, dezesseis vezes a barra de erro**, e duas regras de janela uniformes concordam entre si enquanto discordam da publicada no mesmo lugar.

| $T_s$ | publicado | janela fixa $4\leq r\leq 8$ | janela relativa $0{,}15R\leq r\leq 0{,}5R$ |
|---:|---:|---:|---:|
| 2 | 1,708 | 1,722 ± 0,018 | 1,676 ± 0,014 |
| 32 | 1,739 | 1,834 ± 0,018 | 1,797 ± 0,021 |
| 64 | 1,761 | **1,920 ± 0,011** | **1,913 ± 0,011** |
| 128 | 1,790 | **1,959 ± 0,010** | **1,953 ± 0,011** |
| 512 | 1,901 | 1,968 ± 0,007 | 1,961 ± 0,008 |
| 8192 | 1,965 | 1,964 ± 0,007 | 1,981 ± 0,008 |

Isso desloca o **ponto de saturação**: sob janela uniforme $D_f$ satura perto de $T_s = 128$, contra ~4096 nos pontos publicados. Fecha a pendência **N7** com medição em vez de suspeita.

Os pontos publicados intermediários foram lidos da imagem da Figura 3, com incerteza de transcrição de ~0,005; apenas os extremos (1,708 ± 0,005 e 1,963 ± 0,001) vêm da legenda. A discrepância de 0,16 é grande demais para ser transcrição, mas os valores merecem conferência contra a fonte antes de entrarem na carta-resposta.

**O que fica no lugar da afirmação atual.** Não "$D_f$ cresce de 1,71 a 1,96", que sugere um expoente variando continuamente, e sim: em $T_s$ baixo a seção é um agregado DLA bidimensional com $D_f \approx 1{,}71$ sobre um intervalo de escala real — o valor que a geometria de crescimento prevê, sem ajuste de nada; conforme $T_s$ cresce, **o intervalo de escala encolhe até desaparecer** e a seção passa a ser compacta. A transição é a perda do regime fractal, e é isso que a Figura 3 mede.

### Por que isto importa para a revisão

As três figuras passam a contar a mesma história por caminhos independentes e sem parâmetro livre: o diâmetro cai e satura (Figura 1), a fração de preenchimento sobe de 0,21 a 0,94 (Figura 2), a densidade deixa de decair e a coordenação dobra (Figura 3). A região de transição é 128–512 nas três.

Um teste que resolveria a questão de $D_f$ em definitivo, se for desejado: gerar fibrilas maiores. Se o problema é o intervalo de escala curto, aumentar $R$ de 33 para ~100 — cerca de 7× mais moléculas, viável com o `fast_dla2` — deve alargar o platô. Se $D_f$ convergir, ótimo; se o platô continuar ausente em $T_s$ alto, confirma-se que não há fractal ali e a releitura acima vira conclusão, não alternativa.

---

## Figura 4 — estatística das cascatas e o ansatz de Araújo

![Razão dados/modelo, KS das quatro famílias, expoente e nitidez do corte](fig04_cascatas.png)

*Painel (a): razão entre a sobrevivência observada e a de cada modelo em $T_s$=128, $m$=10; o valor 1 significa modelo exato. Painel (b): distância KS das três famílias competitivas nas 50 condições, cinco pontos por modelo (um por $m$), com opacidade crescente em $m$. Painéis (c) e (d): expoente e nitidez do corte do ansatz de Araújo, com bootstrap de blocos por fibrila (120 réplicas). 61 000 717 cascatas preterminais.*

### A definição adotada

**A cascata é o observável primário**: tudo que é removido numa mesma elevação quase-estática de carga, até o sistema reestabilizar, incluindo as hastes que perdem o caminho de carga por consequência. É `total_deleted_rods` no esquema legado.

Ela é **livre de parâmetro** — determinada pelo modelo, não por escolha do operador, ao contrário do protocolo recozido, em que a avalanche era definida por $\Delta F$ e a estatística era propriedade do $\Delta F$ e não da fibrila (§12 da DAG). É a **unidade causal**: partes espacialmente separadas de uma mesma cascata foram causalmente ligadas, e particioná-las por geometria descarta esse vínculo. E é o que **"avalanche" significa na literatura de fiber bundle**.

A decomposição em aglomerados conexos permanece nos dados como diagnóstico de localização do dano — 12% a 25% das cascatas se partem em mais de um aglomerado — mas não é o estimando primário. **A cascata terminal é excluída**: é a ruptura catastrófica final, uma por realização, com tamanho de centenas contra a média de ~11 das preterminais.

### A lei de potência pura é rejeitada

Pelo procedimento de `Bibliograph/Clauset2009.md` (Box 1), com 2500 réplicas semiparamétricas e o limiar $p > 0{,}1$:

| | de 50 condições |
|:--|--:|
| Lei de potência pura **rejeitada** | **48** |
| Plausível | 2 (no fio: $p$ = 0,106 e 0,123) |

Em 47 das 48, $p = 0{,}000$: **nenhuma** das 2500 amostras sintéticas alcançou o KS observado. Comparada às quatro alternativas da Tabela 1 de Clauset pela razão normalizada de Vuong, a lei pura perde para log-normal e esticada em 49 de 50, e só vence a exponencial simples.

### O ansatz de Araújo é o melhor dos quatro

Araújo, Moreira, Costa Filho e Andrade (Phys. Rev. E **67**, 027102) descrevem a massa do esqueleto de percolação por

$$ F(M) \sim M^{-\alpha} \exp\left[-\left(\frac{M}{M_0}\right)^{\eta}\right] $$

uma lei de potência cujo corte tem **nitidez livre** em vez de fixada em exponencial. Escrito como função de massa, $p(s) \propto s^{-\gamma}\exp[-(s/s_c)^{\eta}]$. Esta família **contém** o corte exponencial em $\eta = 1$, então o parâmetro extra é testável por razão de verossimilhança com um grau de liberdade.

**O corte é mais abrupto que exponencial em 50 de 50 condições.** Mediana $\eta$ = 2,30, faixa 1,13 a 5,19; em 46 das 50, $\eta - 2\,\mathrm{SE} > 1$. Contra $\eta = 1$, $p < 0{,}001$ em 49 das 50.

| menor KS | condições |
|:--|--:|
| **Araújo** | **34** |
| corte exponencial | 9 |
| log-normal | 7 |
| esticada pura | 0 |

Isto **desfaz a degenerescência** que a análise anterior encontrara. Log-normal, esticada e corte exponencial pareciam equivalentes porque nenhuma delas tem a forma certa de corte; com $\eta$ livre, a diferença aparece. Em $T_s$=128, $m$=10 o KS cai de 0,0109 (exponencial) e 0,0148 (log-normal) para **0,0039**.

### Onde o ansatz falha

O painel (a) mostra o limite. Até $s \approx 30$ a razão dados/modelo é 1 para Araújo — descrição exata. Além disso ela **sobe até 30**: o modelo **subestima os maiores eventos**. O corte exponencial erra na direção oposta, superestimando-os por um fator 3.

Ou seja: nenhuma das famílias acerta a cauda extrema. Araújo vence porque acerta o corpo e a região de corte, que é onde está a massa de probabilidade e o que o KS mede. **Não se trata de um modelo exato, e sim do melhor entre os disponíveis.**

### Parâmetros medidos

Expoente $\gamma$:

| $T_s$ | $m$=1 | $m$=2 | $m$=3 | $m$=5 | $m$=10 |
|---:|---:|---:|---:|---:|---:|
| 2 | 1.874 ± 0.008 | 1.995 ± 0.013 | 2.037 ± 0.018 | 2.055 ± 0.019 | 2.022 ± 0.021 |
| 8 | 2.229 ± 0.007 | 2.322 ± 0.011 | 2.356 ± 0.013 | 2.335 ± 0.018 | 2.110 ± 0.058 |
| 16 | 2.503 ± 0.008 | 2.519 ± 0.010 | 2.479 ± 0.013 | 2.387 ± 0.016 | 2.169 ± 0.034 |
| 32 | 2.719 ± 0.008 | 2.605 ± 0.009 | 2.547 ± 0.019 | 2.306 ± 0.028 | 2.075 ± 0.032 |
| 64 | 2.842 ± 0.006 | 2.605 ± 0.009 | 2.396 ± 0.021 | 2.201 ± 0.028 | 2.011 ± 0.023 |
| 128 | 2.865 ± 0.007 | 2.552 ± 0.008 | 2.343 ± 0.015 | 2.119 ± 0.021 | 1.982 ± 0.012 |
| 512 | 2.846 ± 0.009 | 2.485 ± 0.011 | 2.238 ± 0.020 | 2.033 ± 0.022 | 1.933 ± 0.015 |
| 1024 | 2.851 ± 0.005 | 2.493 ± 0.009 | 2.449 ± 0.021 | 1.993 ± 0.035 | 1.921 ± 0.021 |
| 4096 | 2.845 ± 0.006 | 2.482 ± 0.012 | 2.202 ± 0.025 | 1.990 ± 0.031 | 1.904 ± 0.017 |
| 8192 | 2.830 ± 0.005 | 2.452 ± 0.013 | 2.188 ± 0.022 | 1.975 ± 0.028 | 1.912 ± 0.013 |

Nitidez do corte $\eta$ ($\eta = 1$ seria corte exponencial):

| $T_s$ | $m$=1 | $m$=2 | $m$=3 | $m$=5 | $m$=10 |
|---:|---:|---:|---:|---:|---:|
| 2 | 2.57 ± 0.11 | 3.54 ± 0.27 | 3.99 ± 0.66 | 4.03 ± 0.46 | 4.18 ± 0.69 |
| 8 | 3.12 ± 0.18 | 3.71 ± 0.43 | 3.63 ± 0.79 | 3.01 ± 1.92 | 1.18 ± 0.31 |
| 16 | 3.20 ± 0.24 | 3.14 ± 0.46 | 2.90 ± 0.45 | 2.44 ± 0.49 | 1.63 ± 0.29 |
| 32 | 2.81 ± 0.29 | 3.30 ± 0.34 | 2.90 ± 0.33 | 1.71 ± 0.29 | 1.73 ± 0.26 |
| 64 | 3.58 ± 0.36 | 3.19 ± 0.32 | 1.62 ± 0.15 | 1.39 ± 0.13 | 1.68 ± 0.15 |
| 128 | 4.25 ± 0.33 | 2.72 ± 0.21 | 1.86 ± 0.13 | 1.48 ± 0.10 | 2.01 ± 0.12 |
| 512 | 4.81 ± 0.47 | 2.23 ± 0.18 | 1.47 ± 0.12 | 1.34 ± 0.08 | 1.93 ± 0.14 |
| 1024 | 4.54 ± 0.45 | 2.22 ± 0.18 | 2.30 ± 0.22 | 1.13 ± 0.10 | 1.70 ± 0.14 |
| 4096 | 5.19 ± 0.50 | 2.20 ± 0.21 | 1.27 ± 0.11 | 1.20 ± 0.10 | 1.75 ± 0.13 |
| 8192 | 4.30 ± 0.37 | 1.87 ± 0.16 | 1.29 ± 0.09 | 1.19 ± 0.09 | 1.77 ± 0.13 |

Escala de corte $s_c$:

| $T_s$ | $m$=1 | $m$=2 | $m$=3 | $m$=5 | $m$=10 |
|---:|---:|---:|---:|---:|---:|
| 2 | 135.8 ± 4.3 | 124.8 ± 5.7 | 118.1 ± 6.1 | 116.2 ± 7.3 | 105.0 ± 7.6 |
| 8 | 128.0 ± 4.3 | 108.0 ± 6.7 | 103.7 ± 7.8 | 91.7 ± 10.2 | 52.6 ± 12.3 |
| 16 | 111.5 ± 5.6 | 84.6 ± 5.2 | 75.4 ± 5.5 | 62.3 ± 5.6 | 44.2 ± 4.7 |
| 32 | 82.6 ± 4.7 | 61.6 ± 3.3 | 56.5 ± 3.1 | 38.0 ± 3.1 | 30.0 ± 2.2 |
| 64 | 65.3 ± 1.9 | 53.5 ± 1.6 | 38.9 ± 2.3 | 29.4 ± 2.1 | 27.9 ± 1.3 |
| 128 | 67.1 ± 1.6 | 51.6 ± 1.5 | 38.3 ± 1.7 | 28.4 ± 1.6 | 31.1 ± 0.9 |
| 512 | 70.0 ± 1.7 | 49.4 ± 1.5 | 34.6 ± 2.2 | 26.9 ± 1.8 | 32.6 ± 1.1 |
| 1024 | 73.4 ± 2.0 | 52.4 ± 1.8 | 49.9 ± 2.1 | 23.9 ± 2.6 | 31.4 ± 1.5 |
| 4096 | 73.9 ± 1.7 | 52.7 ± 2.3 | 33.7 ± 2.9 | 25.9 ± 2.4 | 32.5 ± 1.3 |
| 8192 | 72.8 ± 1.9 | 51.2 ± 2.3 | 32.8 ± 2.4 | 25.1 ± 2.1 | 33.5 ± 1.1 |

### Leitura

**$\gamma$ satura em $T_s \approx 128$** para todo $m$ — a mesma região das três figuras estruturais, e a primeira medida a vir da mecânica e não da geometria.

**$\gamma$ decresce com $m$** em $T_s$ alto, de 2,83 ($m$=1) a 1,91 ($m$=10): desordem mais estreita dá cauda mais pesada, o que é o esperado, pois limiares próximos rompem juntos.

**O 5/2 de campo médio cai entre $m$=1 e $m$=2.** Isso **não** autoriza dizer que se encontrou campo médio: $m$ é parâmetro livre da desordem, e escolher o $m$ que cruza 5/2 seria ajuste a posteriori. Além disso o modelo não é ELS puro — o limiar $F^*_i = K_i \sigma_c X_i / a_i$ tem canal global (ocupação de camada, via $a_i$) **e** canal local (vizinhos ativos, via $K_i$).

**$\eta$ não é universal.** Varia por um fator 4,6 na grade e depende sistematicamente de $m$ e $T_s$: cresce com $T_s$ em $m$=1, decresce em $m$=5. Araújo tem dois valores fixos, um por grau de correlação. Apenas 11 das nossas 50 condições caem na faixa 1,5–2,0 dele. Um $\eta$ que varia assim é parâmetro de ajuste, não assinatura de classe de universalidade.

### O que NÃO transfere: a leitura do expoente

Araújo liga $\alpha$ à dimensão fractal do esqueleto por $\alpha = d/d_B - 1$, o que dá o expoente da função de massa $\tau = d/d_B$, e para eles fecha: $\tau = 1{,}26$ implica $d_B = 1{,}59$, contra a estimativa independente de 1,64.

Para nós **não fecha**:

| | Araújo | esta campanha |
|:--|--:|--:|
| expoente da função de massa | 1,26 | 1,87 a 2,87 |
| $d_B$ implícito ($d=2$) | **1,59** ✓ | **0,70 a 1,07** ✗ |
| condições com $d_B < 1$ | — | **40 de 50** |

Um $d_B$ menor que 1 é impossível para um aglomerado conexo, e incompatível com o $D_f$ estrutural que a Figura 3 mede (1,7 a 2,0). A razão é física: o $M_B$ de Araújo é um **objeto geométrico estático** — o esqueleto de percolação — e a relação vem da estatística de *blobs*; a nossa cascata é um **evento dinâmico** num processo de carga.

**A forma funcional transfere; a interpretação do expoente não.** Isso importa para N12: seria tentador usar Araújo para ligar o expoente de avalanche a $D_f$ e responder R1-5 — os números não permitem.

### Código utilizado

| arquivo | papel |
|:--|:--|
| `Code/Data_analysis/extract_cascades.py` | reduz os 10 000 arquivos a histogramas de tamanho de cascata por realização, separando a terminal |
| `Code/Data_analysis/run_cascade_statistics.py` | procedimento de Clauset por condição, com bootstrap de blocos |
| `Code/Data_analysis/run_araujo_fits.py` | ajusta o ansatz de Araújo, testa $\eta=1$ e compara o KS das quatro famílias |
| `Code/Data_analysis/plot_araujo_adequacy.py` | desenha os quatro painéis |
| `Code/Data_analysis/avalanche_statistics.py` | núcleo de ajuste; recebeu `fit_generalized_cutoff`, `fit_stretched_exponential` e `vuong_likelihood_ratio` |
| `Code/Data_analysis/test_generalized_cutoff.py` | cinco verificações do ansatz de Araújo |
| `Code/Data_analysis/test_stretched_exponential.py` | cinco verificações da esticada e da razão de Vuong |

```bash
python3 Code/Data_analysis/extract_cascades.py \
    --runs-dir $DLA_PROJECT/campaign/avalanches/runs \
    --out      $DLA_PROJECT/campaign/analysis/cascades --workers 48

python3 Code/Data_analysis/run_cascade_statistics.py \
    --cascades $DLA_PROJECT/campaign/analysis/cascades \
    --out      $DLA_PROJECT/campaign/analysis/cascades/cascade_stats_clauset.csv \
    --replicates 400 --gof-replicates 2500 --lr-replicates 500 --workers 48

python3 Code/Data_analysis/run_araujo_fits.py \
    --cascades $DLA_PROJECT/campaign/analysis/cascades \
    --stats    $DLA_PROJECT/campaign/analysis/cascades/cascade_stats_clauset.csv \
    --out      $DLA_PROJECT/campaign/analysis/cascades/araujo_fits.csv --replicates 120

python3 Code/Data_analysis/plot_araujo_adequacy.py
```

Extração 12 s; Clauset 11 min; ajustes de Araújo 4 min. A tabela completa dos ajustes de Araújo está aqui, em `fig04_araujo_ajustes.csv`; a dos testes de Clauset — aderência, razões de Vuong e as colunas sem piso de cauda — fica em `$DLA_PROJECT/campaign/analysis/cascades/cascade_stats_clauset.csv`, junto dos dados.

### Algoritmo

**Redução.** Cada arquivo vira uma matriz esparsa com uma linha por realização e uma coluna por tamanho de cascata, mais o índice da fibrila de cada linha — que é o que o bootstrap reamostra. Verificado contra o parser: 61 000 717 preterminais + 500 000 terminais + 500 000 linhas de abertura $f=0$ = 62 000 717 passos de força.

**Seleção de $x_{\min}$.** Minimização da distância KS discreta, **com piso de 5% dos eventos na cauda** — ver ressalva 2.

**Estimativa.** MLE discreto exato via zeta de Hurwitz, não a aproximação contínua: Clauset avisa que a aproximação só é boa para $x_{\min} \gtrsim 6$, e os nossos são quase todos 2. Para o ansatz de Araújo a normalização é uma soma explícita sobre o suporte inteiro, truncada onde o corte já matou a massa, e a otimização parte de três pontos distintos.

**Aderência.** Bootstrap semiparamétrico com **2500 réplicas**, seguindo $n \geq \frac{1}{4}\epsilon^{-2}$ para $\epsilon = 0{,}01$; cada réplica sintética resseleciona o próprio $x_{\min}$, como o §4 exige.

**Comparação de modelos.** Para as três alternativas não aninhadas, a razão normalizada da equação (C.6). Para o corte exponencial e para o ansatz de Araújo, que são aninhados, razão de verossimilhança — bootstrap paramétrico no primeiro caso, $\chi^2$ com um grau de liberdade no segundo.

**Incerteza.** Bootstrap de blocos, **bloco = fibrila**: realizações da mesma fibrila compartilham topologia e não são independentes.

### Ressalvas

1. **Araújo é o melhor dos quatro, não um modelo exato.** Ele subestima a cauda extrema por até um fator 30 (painel a). Vence porque acerta o corpo e a zona de corte, que é o que o KS pesa.
2. **O piso de 5% na cauda é uma escolha.** Sem ele, a minimização de KS cai numa cauda distante em 4 de 50 condições (todas $m$=10), devolvendo $x_{\min} \approx 30$ e $\gamma \approx 5$ sobre 0,15% dos eventos, com condições vizinhas discordando por um fator 2,3. O piso é uniforme e as colunas sem piso ficam no CSV. A instabilidade é sintoma do mesmo fato que o teste de aderência estabelece.
3. **`fit_generalized_cutoff` foi implementado agora**, com cinco testes — inclusive o caso $\eta=1$, em que deve reproduzir o corte exponencial, e o caso $\eta=2$, que deve ser detectado com $2\Delta\ell > 100$.

### Por que isto importa para a revisão

A Issue #5 e as Figuras 8–10 do manuscrito assumem cauda de lei de potência. Com 61 milhões de cascatas sob o protocolo corrigido essa descrição é **rejeitada em 48 de 50 condições**, e o que a substitui é uma lei de potência com **corte mais abrupto que exponencial** — a mesma forma que descreve o esqueleto de percolação e a fragmentação por impacto.

Isso dá conteúdo a N11: $\gamma$ existe e é bem determinado dentro do ansatz, mas citá-lo sem o corte seria enviesado. E fecha uma porta em N12: a ponte de Araújo entre expoente de avalanche e dimensão fractal não é utilizável aqui.

---

*Próximas figuras entram abaixo.*

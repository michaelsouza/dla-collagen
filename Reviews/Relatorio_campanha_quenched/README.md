# Relatório — campanha quenched (ER12738)

Resultados do conjunto de dados gerado sob o protocolo de fibra em feixe com
desordem congelada, depois da correção do cálculo de $\sigma$ (`a834c53`) e da
troca do protocolo de carga (§12 da DAG).

| | |
|:--|:--|
| Fibrilas | 2 000 (10 $T_s$ × 200) |
| Realizações | 500 000 (10 $T_s$ × 200 fibrilas × 5 valores de $m$ × 50) |
| Eventos | 79 719 965, dos quais 19 508 453 selecionados |
| Geração | job 576131 no SDumont2, 1 h 43 min, 384 núcleos |
| Verificação | 10 000/10 000 por conteúdo; 0 falhas; 0 claims órfãos |
| Dados | `$DLA_PROJECT/campaign/` (1,7 GB de fratura, 21 GB de fibrilas) |

Este documento cresce por figura. Cada seção traz a imagem, os números, o código
que a produziu, o algoritmo em resumo e as ressalvas.

---

## Figura 1 — o diâmetro da fibrila ao longo do seu eixo

![Perfil de diâmetro de seção transversal](fig01_perfil_diametro.png)

*Painel esquerdo: diâmetro de giração em função da posição ao longo do eixo,
para $T_s$ = 2, 16, 64 e $\geq$ 512. Painel direito: diâmetro na região central
em função de $T_s$. 25 fibrilas por condição; camadas sustentadas por menos de 20
fibrilas (as pontas) foram omitidas. As curvas de $T_s$ = 512 a 8192 se sobrepõem
e por isso recebem um rótulo único.*

### O que o gráfico mostra

**A fibrila não é um cilindro — é um fuso.** Mais grossa na semente ($y = 0$) e
afinando monotonicamente até as pontas, ao longo de ~3 900 sítios de rede. O
perfil é simétrico em torno da semente, o que é esperado para agregação por
difusão a partir de um germe central: a semente teve todo o tempo de deposição
para engrossar, as pontas são recentes.

**A difusão superficial compacta a fibrila.** Do menor ao maior $T_s$ o diâmetro
no miolo cai por um fator de 2,15, enquanto o comprimento cresce apenas 9%. Como
o número de moléculas é fixo em 30 000, o volume ocupado cai por um fator de
$\approx 4{,}2$ — a mesma massa num envelope quatro vezes menor.

**A queda para.** De $T_s = 512$ a 8192, um fator 16 na difusão superficial, o
diâmetro varia 1,2%. As quatro condições do platô são estatisticamente
indistinguíveis entre si, separadas por menos de um erro padrão.

### Valores medidos

Média sobre 25 fibrilas por condição, na região central $|y| \leq 100$. O erro é
o erro padrão **entre fibrilas** — a incerteza correta para comparar condições.
Todas as grandezas em sítios de rede.

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

**A razão $d_{max}/d_{gyr}$ não é monotônica.** Ela é um índice de irregularidade
da seção: quanto maior, mais a envolvente é ditada por protuberâncias isoladas em
vez do corpo da seção. Sobe até 1,98 em $T_s = 64$ e **cai** para $\approx 1{,}72$
no platô. A superfície fica relativamente mais lisa exatamente onde o tamanho
para de mudar — dois indícios independentes apontando para a mesma transição.

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

**Entrada.** A saída *compacta* do gerador, uma linha por molécula
(`uid: id x y z`, com $y$ = base da haste). Cada molécula ocupa 18 camadas
consecutivas, de $y$ a $y+17$, sempre no mesmo par $(x, z)$. Os arquivos
estendidos têm a mesma informação com 18× o tamanho — 1,2 GB contra 20 GB — então
não há motivo para lê-los.

**Acumulação.** Para cada camada é preciso o centroide e a dispersão das
partículas que a ocupam. Materializar as 540 000 partículas de cada fibrila é
desnecessário, porque a variância só depende de somas. O algoritmo faz **18
passagens** — uma por deslocamento dentro da haste — acumulando por camada a
contagem e as somas de $x$, $z$, $x^2$ e $z^2$. Daí saem, em forma fechada:

$$
c = (\langle x\rangle,\ \langle z\rangle), \qquad
\langle |r-c|^2 \rangle = \langle x^2\rangle - \langle x\rangle^2
                        + \langle z^2\rangle - \langle z\rangle^2
$$

$$
d_{gyr} = 2\sqrt{\langle |r-c|^2 \rangle}, \qquad
d_{max} = 2\max|r-c|
$$

O $d_{max}$ exige os extremos e não sai de somas, então custa mais 18 passagens de
máximo. Toda a acumulação usa indexação dispersa do NumPy (`np.add.at`,
`np.maximum.at`), sem laço em Python sobre moléculas.

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

*Segmentos centrais ($|y| \leq 25$) projetados no plano $x$–$z$, para
$T_s$ = 2, 64, 512 e 8192. Cada sítio ocupado é pintado com o índice da primeira
molécula que o ocupou, de modo que a cor lê "quando esta coluna foi construída".
**Os quatro painéis compartilham a mesma escala espacial**; a barra no primeiro
painel mede 20 sítios de rede. Sementes 100000, 104000, 106000 e 109000.*

Reproduz a Figura 2 do manuscrito a partir das fibrilas da campanha nova.

### O que o gráfico mostra

A transição descrita no artigo aparece igual: morfologia **esparsa e irregular**
em $T_s$ baixo, passando por densa com protuberâncias, até **empacotamento denso
e radialmente simétrico** em $T_s$ alto. A fração de preenchimento da caixa
envolvente quantifica isso.

| $T_s$ | sítios ocupados | preenchimento |
|---:|---:|---:|
| 2 | 858 | 0,21 |
| 64 | 526 | 0,51 |
| 512 | 436 | 0,82 |
| 8192 | 454 | 0,94 |

O gradiente de cor mostra o mecanismo. Em $T_s = 2$ as moléculas antigas (azul)
formam um esqueleto ramificado e as recentes (vermelho) se depositam nas pontas
dos braços, sem preencher os vãos — é blindagem difusiva clássica. Em
$T_s = 8192$ o núcleo antigo é compacto e as moléculas recentes formam uma
**casca externa contínua**: a difusão superficial permite que a molécula desça
para os vãos antes de fixar, então o crescimento é camada a camada em vez de
dendrítico.

### Diferença deliberada em relação à figura publicada

Na figura do artigo cada painel parece normalizado ao próprio tamanho, o que faz
os quatro aparentarem largura semelhante e **esconde a compactação**. Aqui a
escala é comum: $T_s = 2$ preenche o quadro e $T_s = 8192$ ocupa cerca de um
terço dele.

Isso mantém a Figura 2 consistente com a Figura 1, que mede a mesma compactação
como número. Com escala independente por painel, as duas figuras diriam coisas
diferentes sobre o mesmo fenômeno.

### Código utilizado

| arquivo | papel |
|:--|:--|
| `Code/Data_analysis/plot_central_sections.py` | lê os compactos, recorta a fatia central e desenha os quatro painéis |

```bash
python3 Code/Data_analysis/plot_central_sections.py
```

Reusa `read_compact` de `fibril_diameter_profile.py`.

### Algoritmo

**Recorte.** Molécula entra no painel se a base da haste satisfaz
$|y| \leq 25$. Cada molécula guarda o seu índice de chegada — a ordem em que o
gerador a ligou ao agregado, de 0 (semente) a 30 000.

**Projeção.** Uma coluna $(x, z)$ pode ser ocupada por várias moléculas em
alturas diferentes. O sítio recebe o índice da **primeira** a ocupá-lo. Na
implementação, os índices são ordenados de forma decrescente antes da escrita na
grade, de modo que o menor é o último a ser gravado e vence.

**Preenchimento.** Razão entre sítios ocupados e a área da caixa envolvente da
fatia, $(\Delta x + 1)(\Delta z + 1)$.

### Escolhas que precisam ser declaradas se a figura for para o manuscrito

1. **A espessura da fatia não é neutra.** A legenda original diz "segmento
   central" sem quantificar. Em $|y| \leq 25$ o preenchimento vai de 0,21 a 0,94;
   em $|y| \leq 400$ vai de 0,52 a 0,90 e os braços dendríticos desaparecem —
   uma fatia grossa empasta a projeção e destrói justamente o contraste que a
   figura existe para mostrar. Foi por isso que se escolheu 25.
2. **As sementes são as primeiras de cada condição, não escolhidas.** Convém
   verificar se são representativas do ensemble antes da publicação; se forem
   selecionadas, a seleção precisa ser declarada.
3. **Mapa de cores.** Usa-se `turbo` em vez de `jet` — mesma aparência azul→
   vermelho, sem as bandas falsas que o `jet` introduz.

---

*Próximas figuras entram abaixo.*

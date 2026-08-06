# Issue #5, protocolo estatístico para as distribuições de avalanche

> **Decisão autoral posterior, 2026-08-06.** O protocolo abaixo registra a
> recomendação metodológica original. A execução final foi ampliada para os dez
> valores de $T_s$ e usa 50 geometrias por condição. Os autores decidiram não
> executar a curva adicional de sensibilidade ao número de geometrias nem novas
> simulações para outros módulos de Weibull, devido ao custo computacional. A
> resposta apresentará a ampliação de 10 para 50 geometrias como a melhor
> cobertura disponível, sem alegar convergência formal, e limitará explicitamente
> as conclusões a $m=2$. Os resultados e a matriz de evidências estão em
> [`Issue5_clauset_pooled_from_scratch/REFEREE_RESPONSE_EVIDENCE.md`](Issue5_clauset_pooled_from_scratch/REFEREE_RESPONSE_EVIDENCE.md).
> A resposta unificada pronta para revisão autoral está em
> [`Issue5_clauset_pooled_from_scratch/UNIFIED_REFEREE_RESPONSE_AVALANCHES.md`](Issue5_clauset_pooled_from_scratch/UNIFIED_REFEREE_RESPONSE_AVALANCHES.md).

## Escopo e conclusão

Esta nota transforma os pedidos do primeiro Referee e as recomendações do
professor Suki em um protocolo reproduzível para testar as distribuições dos
tamanhos de avalanche. Nesta primeira etapa, o escopo é restrito a
\(T_s=2,8,32\), para os quais os novos lotes de fratura estão completos.

**Conclusão curta:** os dados disponíveis permitem executar um teste rigoroso,
mas os ajustes antigos sobre probabilidades agrupadas em bins não devem ser
reutilizados. O objeto básico deve ser cada tamanho inteiro de cluster extraído
dos arquivos brutos, mantendo a identificação da fibrila e da realização de
ruptura. A inferência é condicionada a \(s\geq2\), com a busca de
\(s_{\min}\) começando em 2; os eventos \(s=1\) permanecem preservados para
auditoria e descrição, mas não entram como candidatos no ajuste. Para cada
\(T_s\), deve-se estimar \(s_{\min}\) e os parâmetros por máxima
verossimilhança discreta, testar a qualidade absoluta do ajuste por bootstrap e
comparar a potência pura com potência com corte exponencial, lognormal e
exponencial. A incerteza deve ser obtida por reamostragem hierárquica, porque
milhões de clusters provenientes da mesma fibrila não são milhões de
geometrias independentes.

Os três valores de \(T_s\) são suficientes para validar o pipeline e testar a
parte inicial da variação das distribuições, mas não permitem decidir se existe
o plateau alegado para \(T_s\geq512\). Portanto, esta etapa não encerra sozinha
a [Issue #5](https://github.com/michaelsouza/dla-collagen/issues/5), cuja
aceitação exige a análise de todos os valores reportados e a sensibilidade ao
módulo de Weibull.

## Fontes primárias examinadas

- Clauset, Shalizi e Newman, “Power-Law Distributions in Empirical Data”,
  *SIAM Review* **51**, 661–703 (2009),
  [doi:10.1137/070710111](https://doi.org/10.1137/070710111), transcrito
  integralmente em
  [`Bibliograph/Clauset2009.md`](../Bibliograph/Clauset2009.md).
- Zapperi et al., “First-Order Transition in the Breakdown of Disordered
  Media”, *Physical Review Letters* **78**, 1408–1411 (1997),
  [doi:10.1103/PhysRevLett.78.1408](https://doi.org/10.1103/PhysRevLett.78.1408),
  transcrito em
  [`Bibliograph/Zapperi1997a.md`](../Bibliograph/Zapperi1997a.md).
- Zapperi et al., “Avalanches in Breakdown and Fracture Processes”,
  *Physical Review E* **59**, 5049–5057 (1999),
  [doi:10.1103/PhysRevE.59.5049](https://doi.org/10.1103/PhysRevE.59.5049),
  transcrito em
  [`Bibliograph/Zapperi1999.md`](../Bibliograph/Zapperi1999.md).
- Laurson, Santucci e Zapperi, “Avalanches and Clusters in Planar Crack Front
  Propagation”, *Physical Review E* **81**, 046116 (2010),
  [doi:10.1103/PhysRevE.81.046116](https://doi.org/10.1103/PhysRevE.81.046116),
  consultado também na
  [versão integral dos autores](https://arxiv.org/abs/0911.2380).
- Parkinson et al., “The Mechanical Properties of Simulated Collagen Fibrils”,
  *Journal of Biomechanics* **30**, 549–554 (1997), transcrito em
  [`Bibliograph/Parkinson1997.md`](../Bibliograph/Parkinson1997.md).
- Relatórios e comentários internos em
  [`Reviews/Referees.md`](Referees.md) e
  [`Reviews/Referees-comment-Suki.md`](Referees-comment-Suki.md).
- Estrutura e semântica dos dados verificadas no programa
  [`Code/Fracture_fibril/stress_strain_ava.py`](../Code/Fracture_fibril/stress_strain_ava.py#L441-L576)
  e no
  [`README` das simulações de fratura](../Code/Fracture_fibril/README.md#L65-L115).

Clauset et al. é a referência metodológica explicitamente solicitada pelo
primeiro Referee. Os artigos de Zapperi e Laurson foram examinados porque o
Referee os usa para definir o contexto correto de fratura dirigida e porque
eles separam explicitamente avalanches globais de clusters geométricos locais.
Parkinson foi consultado para o papel de \(m\), pois o próprio artigo afirma
que uma faixa de valores deve ser investigada quando o módulo de Weibull não é
conhecido experimentalmente
([Parkinson, Methods, linhas 74–84](../Bibliograph/Parkinson1997.md#L74-L84)).

## 1. O que foi solicitado

O primeiro Referee identifica três falhas no tratamento atual:

1. a faixa aparentemente linear cobre no máximo cerca de duas ordens de
   grandeza;
2. o expoente foi obtido sem máxima verossimilhança nem teste de qualidade de
   ajuste;
3. nenhuma distribuição concorrente foi testada
   ([R1-2, linhas 21–27](Referees-comment-Suki.md#L21-L27)).

O professor Suki recomenda usar os eventos individuais sem bins arbitrários e
comparar a potência pura com uma potência com corte exponencial e uma
lognormal. Dentro da definição coletiva fixada na Issue #4, isso corresponde a
usar todos os eventos \(s\geq2\), enquanto \(s=1\) é preservado e descrito
separadamente. Ele também alerta que, em outro estudo, a forma com corte foi
melhor que a potência pura
([comentário de Suki, linha 31](Referees-comment-Suki.md#L29-L31)). O Referee
acrescenta que tamanho finito, número de fibrilas, definição de avalanche e
módulo de Weibull podem alterar os expoentes
([R1-3, linhas 33–45](Referees-comment-Suki.md#L33-L45)).

A Issue #5 incorpora esses pedidos e acrescenta uma condição essencial: a
reamostragem não pode tratar as realizações repetidas na mesma fibrila como
geometrias independentes. Seus bloqueadores, Issues #2 e #4, estavam fechados
quando esta nota foi preparada.

## 2. O que Clauset et al. realmente permite concluir

Clauset et al. propõe três etapas:

1. estimar o limite inferior e o expoente por máxima verossimilhança;
2. calcular um valor \(p\) de qualidade de ajuste por Monte Carlo com a
   estatística de Kolmogorov–Smirnov;
3. comparar a potência com alternativas por razões de verossimilhança
   ([Box 1](../Bibliograph/Clauset2009.md#L65-L78)).

O tamanho de avalanche é inteiro. Portanto, a potência correta acima de
\(s_{\min}\) é

\[
p(s\mid\gamma,s_{\min})=
\frac{s^{-\gamma}}{\zeta(\gamma,s_{\min})},
\qquad s=s_{\min},s_{\min}+1,\ldots,
\]

e não a densidade contínua
([Clauset et al., Eq. 2.4](../Bibliograph/Clauset2009.md#L92-L125)). O expoente
deve maximizar

\[
\ell(\gamma)=
-n_{\mathrm{tail}}\ln\zeta(\gamma,s_{\min})
-\gamma\sum_{i=1}^{n_{\mathrm{tail}}}\ln s_i.
\]

Como \(s_{\min}\) pode ser pequeno, deve-se usar a normalização discreta exata.
A aproximação contínua corrigida de Clauset só alcança erro próximo de 1% para
\(s_{\min}\gtrsim6\), e usar diretamente o estimador contínuo em dados inteiros
é explicitamente desaconselhado
([seção 3.1](../Bibliograph/Clauset2009.md#L183-L224)).

O limite \(s_{\min}\) não deve ser escolhido visualmente. Para cada candidato,
ajusta-se \(\gamma\) e calcula-se

\[
D=\max_{s\geq s_{\min}}
\left|S(s)-P_{\mathrm{PL}}(s)\right|,
\]

onde \(S\) é a distribuição acumulada complementar empírica e
\(P_{\mathrm{PL}}\) a do modelo. Escolhe-se o \(s_{\min}\) que minimiza \(D\)
([seção 3.3](../Bibliograph/Clauset2009.md#L321-L350)).

O valor \(p\) de qualidade de ajuste não é o valor assintótico usual do teste
KS, pois os parâmetros foram estimados nos próprios dados. É necessário gerar
amostras sintéticas, reestimar \(s_{\min}\) e \(\gamma\) em cada amostra e
comparar seu \(D\) ao observado
([seção 4.1](../Bibliograph/Clauset2009.md#L410-L450)). Clauset et al. usa o
critério conservador \(p\leq0.1\) para rejeitar a potência. Um valor
\(p>0.1\) significa apenas que a hipótese não foi rejeitada; não demonstra que
ela é verdadeira, nem que supera uma lognormal ou outra alternativa
([seção 4.1](../Bibliograph/Clauset2009.md#L451-L469)).

Para erro Monte Carlo máximo aproximado de 0.01, Clauset recomenda pelo menos
2500 amostras sintéticas, segundo \(B\geq1/(4\epsilon^2)\). Esse número deve ser
usado para o resultado final; execuções menores servem apenas para desenvolver
e testar o pipeline.

## 3. Inventário dos dados disponíveis

Os dados que preservam a hierarquia estão em:

```text
Data_fibrils/Avalanche_force_grouped/runs/ts_2/
Data_fibrils/Avalanche_force_grouped/runs/ts_8/
Data_fibrils/Avalanche_force_grouped/runs/ts_32/
```

Cada condição contém 50 arquivos de fibrila e cada arquivo contém 1000
realizações completas, separadas por uma linha numerada. O programa grava, para
cada força, a lista exata dos tamanhos dos componentes conectados na coluna
`avalanche_sizes`
([logger, linhas 452–471](../Code/Fracture_fibril/stress_strain_ava.py#L452-L471)).
Assim, a hierarquia observada é:

\[
T_s \longrightarrow \text{fibrila} \longrightarrow
\text{realização de ruptura} \longrightarrow
\text{nível de força} \longrightarrow \text{cluster local}.
\]

Um inventário somente de leitura, antes de qualquer ajuste, produziu:

| \(T_s\) | fibrilas | realizações | clusters | \(s=1\) | fração \(s=1\) | clusters na linha terminal | maior \(s\) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2  | 50 | 50 000 | 6 847 150  | 5 238 180  | 76.50% | 50 221 | 546  |
| 8  | 50 | 50 000 | 12 940 682 | 10 601 287 | 81.92% | 50 017 | 795  |
| 32 | 50 | 50 000 | 26 985 855 | 24 043 453 | 89.10% | 50 000 | 1353 |

Essas contagens incluem os clusters unitários e os clusters registrados no
nível de força que produz ruptura completa. Em todas as condições, cada uma das
50 000 realizações possui exatamente uma linha terminal, embora essa linha
possa conter mais de um componente desconectado.

Os arquivos antigos `Data_fibrils/ava_sizes/ava_*.txt` não devem ser a entrada
principal. Eles perderam a identidade da fibrila, da realização e do nível de
força, e por isso não permitem bootstrap hierárquico, exclusão verificável do
evento terminal ou auditoria de duplicações.

## 4. Definição prévia do objeto estatístico

Antes de olhar os ajustes, devem ser congeladas quatro decisões. Recomenda-se a
seguinte especificação.

### 4.1 Evento

Um evento é um componente espacialmente conectado de moléculas removidas em um
mesmo nível de força. Se uma lista contém `5-2-1`, ela fornece três observações,
\(s=5,2,1\). Não se deve substituir essa lista por sua soma, pois isso voltaria
à definição global rejeitada na Issue #4.

Essa escolha precisa ser nomeada com precisão. Laurson et al. definem a
**avalanche global** como toda a resposta entre dois incrementos do drive e
mostram que, sob interações de longo alcance, ela pode conter vários
**clusters locais** espacialmente desconectados. As distribuições dessas duas
grandezas têm expoentes diferentes no modelo estudado por eles
([Laurson et al., seções II.1–II.2 e III.3](https://arxiv.org/abs/0911.2380)).
Zapperi et al. fazem a mesma separação operacional: a avalanche conta todas as
falhas produzidas pelo incremento de carga, enquanto o cluster geométrico conta
ligações rompidas conectadas
([Zapperi et al. 1999, seções IV–VI](../Bibliograph/Zapperi1999.md#L166-L232)).
Portanto, os dados deste trabalho medem uma **distribuição de tamanhos de
clusters locais de avalanche**, e não a distribuição global por incremento de
força. A referência de Laurson sustenta a separação dos componentes, mas não
prova que dois componentes desconectados sejam cascatas causalmente
independentes; essa interpretação mais forte deve ser evitada.

### 4.2 Eventos unitários

Os eventos \(s=1\) devem permanecer no conjunto bruto e sua fração deve ser
reportada, pois representam entre 76.5% e 89.1% dos clusters e variam
sistematicamente com \(T_s\). Eles não pertencem à população inferencial
definida na Issue #4 e não entram como observações candidatas no ajuste.

Para manter a interpretação de “evento coletivo”, recomenda-se apresentar a
distribuição em duas partes:

\[
P(s=1)=\pi_1,
\qquad
P(s\mid s\geq2).
\]

O ajuste principal é explicitamente condicional a \(s\geq2\), e a busca
objetiva de \(s_{\min}\) começa em 2. Não se deve repetir o ajuste reinserindo
\(s=1\) como sensibilidade, pois isso mudaria a definição do evento coletivo já
fixada. O painel da distribuição ajustada começa em \(s=2\); a legenda e a
tabela devem dizer explicitamente que a massa unitária foi preservada,
auditada e reportada separadamente.

### 4.3 Ruptura terminal

A linha em que `num_active_particles=0` representa a descontinuidade final da
realização, não apenas mais um precursor. Recomenda-se definir como análise
principal a distribuição de **clusters precursores**, excluindo todos os
clusters dessa linha, e repetir o ajuste incluindo-os como sensibilidade.

Essa escolha tem fundamento físico. Zapperi et al. integra avalanches globais
até o limiar de ruptura, mas distingue a falha macroscópica final dos
precursores. Além disso, eles mostram que a distribuição de avalanches globais
tem corte que cresce com o sistema, enquanto os clusters geométricos locais
podem ter corte exponencial que não cresce com o tamanho
([Zapperi et al. 1999, seções IV–VI](../Bibliograph/Zapperi1999.md#L166-L232)).
Como nossos eventos são clusters locais, a inclusão da linha terminal pode
misturar dois mecanismos e controlar artificialmente a cauda.

Quando \(s=1\) é incluído apenas para o inventário de todos os clusters, os
terminais representam menos de 1% das observações: aproximadamente 0.73%,
0.39% e 0.19% para \(T_s=2,8,32\), respectivamente. No conjunto efetivamente
analisado, condicionado a \(s\geq2\), sua participação é maior:
aproximadamente 3.12%, 2.14% e 1.70%, na mesma ordem. Apesar dessa fração
pequena, sua posição na extremidade superior pode alterar de forma
desproporcional \(s_{\min}\), o expoente, a escala de corte e a seleção do
modelo. A tabela final deve mostrar, lado a lado, essas quatro quantidades com e
sem a linha terminal, além da fração de observações removida calculada sobre
\(s\geq2\).

Se os autores decidirem que o objeto publicado deve incluir toda a trajetória,
a ordem pode ser invertida, mas ambos os resultados precisam ser mostrados. A
decisão não pode ser tomada depois de conhecer qual versão favorece a potência.

### 4.4 Ponderação entre fibrilas

O ajuste agrupado responde: “qual é a distribuição de um evento escolhido ao
acaso entre todos os eventos gerados nesta condição?”. Fibrilas que produzem
mais clusters recebem mais peso. Essa é uma quantidade válida, mas não equivale
a escolher primeiro uma fibrila ao acaso e depois um evento nela.

Recomenda-se:

- usar a distribuição agrupada de eventos como estimando principal;
- obter toda a incerteza por blocos de fibrila e realização;
- repetir o ajuste com cada fibrila recebendo peso total igual como análise de
  sensibilidade.

Se as conclusões mudarem, deve-se reportar a heterogeneidade entre fibrilas e
evitar uma única distribuição “universal” por \(T_s\).

## 5. Protocolo recomendado

### Etapa 0, congelar entradas e opções

Registrar em um manifesto:

- caminho, tamanho e hash de cada arquivo;
- \(T_s\), seed da fibrila, \(m\), número de realizações e versão do código;
- regra para \(s=1\), regra para a linha terminal e estimando de ponderação;
- seed mestre do bootstrap e número de réplicas.

O resultado deve ser regenerável sem editar arquivos brutos.

### Etapa 1, extrair uma tabela longa auditável

Cada linha derivada deve conter pelo menos:

```text
ts, fibril_seed, run_id, force, force_index, cluster_index,
avalanche_size, terminal, initial_backbone_size, weibull_m
```

O parser deve verificar automaticamente:

1. 50 arquivos e 1000 realizações por arquivo;
2. identificadores de realização sem lacunas;
3. tamanhos inteiros e positivos, ignorando somente o marcador textual `0`;
4. soma da lista igual a `total_deleted_rods` em cada linha;
5. força não decrescente dentro de cada realização;
6. exatamente uma linha com zero partículas ativas por realização;
7. ausência de linhas incompletas ou cabeçalhos repetidos inesperados.

Para acelerar os ajustes, cada realização pode ser convertida em um vetor de
frequências exatas para cada tamanho inteiro. Isso não é binning: nenhuma
categoria é combinada e a verossimilhança é matematicamente idêntica à dos
eventos individuais. A identidade dos blocos deve continuar armazenada.

### Etapa 2, visualização descritiva sem ajuste por regressão

Para cada \(T_s\), produzir:

- CCDF empírica não agrupada;
- massa em \(s=1\);
- número de eventos, número de valores distintos e maior tamanho;
- distribuição das contagens por fibrila e por realização;
- CCDFs por fibrila, ou uma faixa contendo as 50 CCDFs.

Uma PDF com bins logarítmicos pode ser usada apenas para visualização. Sua
inclinação, \(R^2\) e erro de regressão não entram na inferência. Clauset et al.
mostra que regressões em histogramas log-log podem produzir expoentes
sistematicamente errados e erros formais que não revelam o viés
([Tabela 2 e Apêndice A](../Bibliograph/Clauset2009.md#L235-L260)).

### Etapa 3, ajuste da potência discreta

O conjunto de entrada desta etapa contém apenas eventos \(s\geq2\). Para cada
candidato inteiro a \(s_{\min}\), começando obrigatoriamente em 2:

1. selecionar todos os eventos com \(s\geq s_{\min}\);
2. maximizar a verossimilhança discreta exata para \(\gamma>1\);
3. calcular o KS entre as CCDFs empírica e ajustada;
4. selecionar o candidato de menor KS.

Além de \(\hat s_{\min}\) e \(\hat\gamma\), reportar:

- \(n_{\mathrm{tail}}\) e \(n_{\mathrm{tail}}/n\);
- número de fibrilas e de realizações que contribuem para a cauda;
- número de valores distintos na cauda;
- amplitude \(s_{\max}/s_{\min}\) e seu logaritmo em décadas;
- KS observado.

Clauset et al. observa que a estimação de \(s_{\min}\) é muito mais confiável
com cerca de 1000 ou mais observações na cauda
([seção 3.4](../Bibliograph/Clauset2009.md#L351-L379)). Aqui a contagem bruta
deve ser acompanhada da representação independente. Um candidato não deve ser
aceito se a cauda estiver concentrada em poucas fibrilas. Recomenda-se exigir,
como controle de estabilidade, pelo menos 1000 eventos e contribuição de pelo
menos metade das 50 fibrilas, e mostrar sensibilidade a esse limite.

### Etapa 4, incerteza hierárquica

A unidade independente de geometria é a fibrila. Dentro dela, 1000 realizações
compartilham a mesma estrutura, e vários clusters da mesma realização
compartilham toda a história de carregamento. O bootstrap recomendado é:

1. sortear 50 fibrilas com reposição;
2. para cada fibrila sorteada, sortear 1000 realizações completas com
   reposição;
3. conservar juntos todos os níveis de força e clusters da realização;
4. refazer a seleção de \(s_{\min}\) e todos os ajustes;
5. repetir pelo menos 2000 vezes para intervalos de confiança finais.

Os intervalos percentis, ou preferencialmente BCa quando estáveis, devem ser
reportados para \(s_{\min}\), \(\gamma\), parâmetros das alternativas,
fração da cauda e diferenças entre condições. O erro analítico da MLE e um
bootstrap que sorteia eventos individualmente podem ser fornecidos somente
como comparação; eles não são a incerteza principal.

### Etapa 5, qualidade absoluta do ajuste

Executar o teste semiparamétrico de Clauset com pelo menos 2500 réplicas:

1. acima de \(\hat s_{\min}\), gerar tamanhos da potência discreta ajustada;
2. abaixo de \(\hat s_{\min}\), reamostrar a distribuição empírica;
3. manter em cada conjunto sintético o mesmo número total de observações;
4. reestimar \(s_{\min}\) e \(\gamma\);
5. calcular a fração dos KS sintéticos maiores ou iguais ao observado.

Esse é o teste diretamente solicitado pelo Referee. Contudo, a derivação de
Clauset pressupõe observações independentes e identicamente distribuídas
([Apêndice B](../Bibliograph/Clauset2009.md#L770-L805)), o que não vale
literalmente para clusters da mesma trajetória. Por isso, ele não deve ser o
único diagnóstico.

Como verificação principal de robustez, realizar também um bootstrap KS
hierárquico. Reamostram-se fibrilas e realizações completas, reajusta-se o
modelo e usa-se a distribuição do processo empírico centrado,

\[
\left[S^*(s)-P_{\hat\theta^*}(s)\right]
-\left[S(s)-P_{\hat\theta}(s)\right],
\]

para calibrar a distância suprema. Esse procedimento mantém a variação entre
geometrias e as dependências internas de cada realização. Devem ser reportados
o valor \(p\) de Clauset e o diagnóstico hierárquico. Se eles discordarem, a
conclusão deve ser a mais cautelosa, “resultado sensível à dependência”, e não
uma confirmação de lei de potência.

### Etapa 6, modelos concorrentes

Todos os concorrentes devem ser ajustados por MLE aos mesmos eventos
\(s\geq\hat s_{\min}\) selecionados para a potência. Usar cutoffs diferentes
em uma razão de verossimilhança compara conjuntos de dados diferentes e torna
o resultado inválido.

Os modelos mínimos são:

1. potência pura,

   \[
   p(s)\propto s^{-\gamma};
   \]

2. potência com corte exponencial,

   \[
   p(s)\propto s^{-\gamma}e^{-\lambda s};
   \]

3. lognormal discreta, definida por probabilidades em intervalos inteiros e
   renormalizada acima de \(s_{\min}\);
4. exponencial discreta,

   \[
   p(s)\propto e^{-\lambda s}.
   \]

Uma exponencial estirada discreta é uma quinta alternativa útil, mas não
substitui as três comparações explicitamente pedidas. Toda normalização deve
ser discreta e calculada sobre \(s\geq s_{\min}\).

A potência com corte não é apenas uma alternativa estatisticamente mais
flexível. Há uma motivação física concreta para testá-la. O tamanho finito do
backbone limita \(s\), e uma grandeza local não precisa herdar a divergência da
avalanche global. Na rede de molas de Zapperi et al., a distribuição dos
clusters conectados tem corte exponencial que não cresce com o tamanho do
sistema, ao contrário do corte das avalanches globais
([Zapperi et al. 1999, seções IV e VI](../Bibliograph/Zapperi1999.md#L166-L232)).
Laurson et al. também descrevem as distribuições global e local por funções de
corte controladas pelo parâmetro de restauração do drive
([Laurson et al., Eqs. 4 e 5](https://arxiv.org/abs/0911.2380)). Esses resultados
em modelos análogos não demonstram qual forma vale para a fibrila, mas tornam
uma escala de corte finita uma hipótese física que deve ser comparada à
potência pura, e não um termo acrescentado somente para melhorar o ajuste.

Para potência versus lognormal, exponencial e exponencial estirada, calcular a
razão de log-verossimilhanças com sinal e sua incerteza. Clauset usa o teste de
Vuong para famílias não aninhadas e exige um valor \(p\) para decidir se o
sinal é confiável
([seção 5.1](../Bibliograph/Clauset2009.md#L470-L488)). No presente conjunto,
o valor \(p\) ingênuo por evento deve ser acompanhado de uma comparação por
blocos:

- somar as diferenças de log-verossimilhança dentro de cada fibrila;
- reamostrar fibrilas e realizações hierarquicamente;
- obter um intervalo para a diferença total e para a diferença média por
  fibrila;
- executar, como confirmação, validação cruzada deixando uma fibrila inteira
  de fora por vez.

A potência pura está aninhada na potência com corte quando \(\lambda=0\).
Portanto, o teste de Vuong comum não se aplica. Usar uma razão de
verossimilhança aninhada calibrada por bootstrap paramétrico, reajustando os
dois modelos em cada réplica. Clauset também alerta que hipóteses aninhadas
exigem uma versão modificada do teste
([seção 5.2](../Bibliograph/Clauset2009.md#L489-L490)).

Além da comparação relativa, calcular a qualidade absoluta do ajuste de cada
modelo candidato. Um modelo pode ser “melhor que a potência” e ainda assim ser
inadequado.

### Etapa 7, comparação entre \(T_s=2,8,32\)

Há dois problemas diferentes:

1. verificar se a distribuição muda com \(T_s\);
2. verificar se um parâmetro específico, como \(\gamma\), muda com \(T_s\).

O segundo só faz sentido se a mesma família for defensável nas três condições.
Se a potência com corte for preferida, \(\gamma\) é apenas um parâmetro de
forma acompanhado por \(\lambda\), não um expoente crítico independente.

Para contrastes de expoente, fazer dois ajustes:

- ajuste ótimo em cada condição, com \(s_{\min}\) próprio, usado para testar
  adequação;
- ajuste comparável usando
  \(s_{\min}^{\mathrm{comum}}=\max(\hat s_{\min,2},
  \hat s_{\min,8},\hat s_{\min,32})\), usado para os contrastes
  \(\gamma_8-\gamma_2\) e \(\gamma_{32}-\gamma_8\).

Os intervalos dos contrastes devem vir do bootstrap hierárquico conjunto. Não
se deve concluir que duas condições diferem apenas porque um valor central é
maior, nem porque intervalos individuais parecem separados.

Com apenas esses três valores, a conclusão máxima permitida é sobre a tendência
inicial. Crescimento e plateau ao longo de todos os \(T_s\) só podem ser
avaliados quando os demais lotes forem processados pelo mesmo pipeline.

### Etapa 8, análises de robustez requeridas

#### Tamanho e geometria da fibrila

Embora todas as fibrilas tenham 30 000 moléculas antes da extração do backbone,
o número inicial de moléculas resistentes varia com \(T_s\) e entre seeds. O
maior cluster permitido é, portanto, condicionado ao tamanho efetivo do
backbone.

Usar, para cada fibrila, o tamanho inicial \(N_0\) e verificar se o maior
evento, um quantil alto e o corte ajustado variam com \(N_0\). Mostrar também
a CCDF em \(s/N_0\) como diagnóstico, sem substituir o ajuste discreto de
\(s\). Uma dependência forte do corte com \(N_0\) deve ser descrita como efeito
de tamanho finito.

Essa análise é especialmente importante porque Zapperi et al. encontrou corte
crescente com o tamanho para avalanches globais, mas corte aproximadamente
independente do tamanho para clusters geométricos locais
([Zapperi et al. 1997](../Bibliograph/Zapperi1997a.md#L139-L165);
[Zapperi et al. 1999](../Bibliograph/Zapperi1999.md#L216-L232)).

#### Tamanho do ensemble

Construir curvas de estabilidade usando subconjuntos aleatórios de 10, 20, 30,
40 e 50 fibrilas. Para cada tamanho, repetir a seleção muitas vezes e refazer
\(s_{\min}\), parâmetros, teste de ajuste e escolha do modelo. Isso responde
diretamente à crítica sobre as dez fibrilas originais e mostra se 50 geometrias
estabilizam a conclusão.

#### Posição ao longo da trajetória de força

A distribuição integrada mistura dano inicial, dano próximo da ruptura e a
mudança sistemática da força. Como sensibilidade, repetir o diagnóstico em
faixas pré-especificadas de \(F/F_{\mathrm{rup}}\), sempre excluindo a linha
terminal. Se uma potência aparecer apenas após misturar faixas com
distribuições diferentes, não se deve descrevê-la como uma única lei de escala.

#### Módulo de Weibull

Os dados atuais contêm somente \(m=2\). Eles não podem responder ao pedido de
sensibilidade a \(m\). Parkinson afirma explicitamente que, sem um módulo
experimental conhecido, deve-se investigar uma faixa de valores
([Methods](../Bibliograph/Parkinson1997.md#L74-L84)).

Depois de validar o pipeline em \(m=2\), selecionar valores menores e maiores
que 2, definidos antes das novas simulações, e repetir um subconjunto
balanceado de fibrilas em cada \(T_s\). O número mínimo de fibrilas e
realizações deve ser escolhido por uma curva de estabilidade, não pela
contagem nominal de milhões de eventos. Até isso ser feito, a conclusão deve
ser explicitamente limitada a \(m=2\).

## 6. Regra de decisão e linguagem permitida

Para cada \(T_s\), usar a seguinte árvore:

1. Se \(p_{\mathrm{PL}}\leq0.1\), rejeitar a potência pura.
2. Se \(p_{\mathrm{PL}}>0.1\), dizer “a potência não foi rejeitada acima de
   \(s_{\min}\)”, nunca “a potência foi provada”.
3. Se a potência com corte for significativamente melhor no teste aninhado,
   concluir que os dados favorecem uma potência com escala de corte finita.
4. Se lognormal, exponencial ou exponencial estirada tiver vantagem robusta,
   nomear essa alternativa; se a comparação for inconclusiva, dizer que os
   dados não distinguem os modelos.
5. Se todos os modelos forem rejeitados ou a escolha depender da regra de
   terminal, ponderação ou bootstrap, concluir que não há forma paramétrica
   defensável com os dados atuais.

Mesmo que a potência pura não seja rejeitada, isso não restabelece SOC,
universalidade de load sharing ou comportamento scale-free. Zapperi et al.
mostra que leis de potência podem surgir quando um controle externo varre o
sistema até uma instabilidade, sem estado estacionário auto-organizado
([Zapperi et al. 1997](../Bibliograph/Zapperi1997a.md#L151-L165)). A linguagem
do manuscrito deve continuar sendo “avalanche statistics in driven disordered
fracture”, seguindo o Referee.

## 7. Resultados que o pipeline deve produzir

### Tabela principal

Uma linha por \(T_s\), contendo:

- número de fibrilas, realizações e eventos;
- fração de \(s=1\);
- regra para o terminal;
- \(\hat s_{\min}\), intervalo hierárquico, \(n_{\mathrm{tail}}\) e fração da
  cauda;
- número de fibrilas e realizações representadas na cauda;
- \(\hat\gamma\) e intervalo hierárquico;
- KS e valores \(p\) de Clauset e do diagnóstico hierárquico;
- parâmetros e qualidade absoluta das alternativas;
- razões de verossimilhança, intervalos por blocos e decisão final.

### Figuras

1. CCDF empírica não agrupada com ajustes, \(s_{\min}\) e faixa de bootstrap;
2. resíduos da CCDF ou gráfico quantil-quantil para cada modelo;
3. distribuição das estimativas por fibrila e leave-one-fibril-out;
4. estabilidade com 10, 20, 30, 40 e 50 fibrilas;
5. diagnóstico do corte em função de \(N_0\);
6. contrastes entre os três \(T_s\), somente para parâmetros de modelos não
   rejeitados.

### Arquivos reproduzíveis

- tabela longa ou formato colunar derivado, sem substituir os brutos;
- manifesto de entradas e opções;
- CSV com todos os ajustes e contrastes;
- JSON com decisões, valores \(p\), seeds e número de réplicas;
- log de validação dos dados e testes unitários com dados sintéticos.

Antes de analisar os resultados reais, a implementação deve recuperar, dentro
da incerteza, parâmetros conhecidos de amostras sintéticas de potência
discreta, potência com corte, lognormal e exponencial. Também deve rejeitar uma
potência quando os dados sintéticos forem gerados por uma alternativa bem
separada. Isso verifica o código sem usar a resposta desejada como teste.

## 8. Principais riscos

- **Pseudorreplicação:** usar milhões de eventos como independentes produzirá
  intervalos artificialmente estreitos e valores \(p\) excessivamente
  extremos.
- **Seleção posterior de regras:** reinserir \(s=1\), alterar a regra dos
  terminais ou excluir fibrilas depois de ver qual decisão favorece a potência
  invalida a interpretação dos testes.
- **Mistura de regimes de força:** uma cauda aparente pode resultar da mistura
  de distribuições condicionais diferentes ao longo da ruptura.
- **Cauda dominada por poucas geometrias:** \(n_{\mathrm{tail}}\) grande não é
  suficiente se quase todos os grandes eventos vierem de poucas fibrilas.
- **Comparação com suportes diferentes:** todos os modelos de uma razão de
  verossimilhança precisam usar os mesmos eventos e o mesmo \(s_{\min}\).
- **Normalização contínua:** usar a fórmula contínua em tamanhos inteiros pode
  deslocar o expoente, especialmente quando \(s_{\min}\) é pequeno.
- **Evento terminal:** a falha completa é limitada pelo sistema e pode criar
  uma população distinta na extremidade da cauda.
- **Definição local:** resultados teóricos para o número global de falhas em um
  incremento de carga não se transferem automaticamente aos componentes
  conectados locais usados neste trabalho.
- **Comparação entre expoentes de modelos rejeitados:** um número ajustado
  continua existindo matematicamente mesmo quando a família é inadequada, mas
  não deve ser interpretado como expoente físico.
- **Escopo incompleto:** \(T_s=2,8,32\) testa o pipeline e a tendência inicial,
  não o plateau, e \(m=2\) não resolve a sensibilidade ao módulo de Weibull.

## Decisão recomendada para a próxima etapa

Implementar primeiro o parser auditável e o ajuste da potência discreta em
\(T_s=2\), com dados sintéticos e bootstrap curto de desenvolvimento. Depois de
validar todas as invariantes, executar exatamente o mesmo pipeline congelado em
\(T_s=8\) e \(T_s=32\). Somente então aumentar para 2500 réplicas, comparar as
alternativas e interpretar os resultados. Essa ordem reduz o custo de detectar
erros e impede que decisões metodológicas sejam adaptadas ao resultado de uma
condição específica.

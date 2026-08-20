# Modelo com corte estendido ajustado separadamente em cada $T_s$

## Análise individual, incerteza por fibrilas e teste de parcimônia

**Manuscrito:** ER12738, *Scaling behaviors in simulated collagen fibrils*  
**Spec de revisão:** GitHub issue #1  
**Ticket estatístico:** GitHub issue #5  
**Condições:** $T_s=2,8,16,32,64,128,512,1024,4096,8192$

## 1. Pergunta e resposta

Esta análise abandona qualquer hipótese de uma distribuição conjunta. Para
cada valor de $T_s$, ela estima separadamente o início da cauda e os três
parâmetros da distribuição discreta

$$
p(s\mid s\geq s_{min})=
\frac{s^{-\alpha}\exp[-(s/s_c)^\beta]}
{\sum_{k=s_{min}}^\infty k^{-\alpha}\exp[-(k/s_c)^\beta]}.
$$

Portanto, estamos ajustando dez modelos estatísticos independentes da mesma
família funcional, e não um único modelo com parâmetros compartilhados. Essa
distinção é essencial: a análise testa se a família com corte descreve a cauda
de cada condição, mas não testa se duas condições possuem o mesmo $\alpha$,
$\beta$ ou $s_c$.

O modelo com corte estendido não é rejeitado em nenhuma condição pelo teste
por blocos de fibrilas, com $p_{bloco}=0{,}242$--$0{,}915$. Ele é, assim, a
única das cinco famílias avaliadas que fornece uma descrição uniforme das dez
caudas selecionadas. Entretanto, isso não significa que seja o modelo mínimo
em cada $T_s$: formas mais simples também são adequadas em $T_s=2,8,16$ e 64.
Entre os candidatos considerados, os três parâmetros do corte estendido são
necessários para descrever as caudas comparadas em $T_s=32$ e em todas as
condições $T_s\geq128$.

## 2. O que foi estimado e testado

Os dados são os tamanhos inteiros, sem binning, dos componentes locais conexos
removidos antes do passo terminal. As 1.000 realizações de ruptura executadas
sobre uma mesma geometria não são tratadas como observações estruturais
independentes; a unidade de reamostragem é cada uma das 50 fibrilas.

Em cada condição, todos os valores inteiros admissíveis de $s_{min}$ foram
avaliados, desde 1 até o maior limite que ainda retinha pelo menos 1.000
eventos. O modelo com corte estendido recebeu um ajuste de máxima
verossimilhança discreta em cada candidato, e o valor com menor distância KS
foi selecionado. Essa seleção foi feita separadamente, razão pela qual os dez
valores de $s_{min}$ não precisam coincidir.

Depois da seleção, 999 réplicas reamostraram fibrilas inteiras e reajustaram os
parâmetros no $s_{min}$ observado. O teste absoluto usa o processo empírico
centrado e calcula $p=(b+1)/(999+1)$, em que $b$ é o número de réplicas cuja
discrepância excede o KS observado. Os intervalos percentis de 95% também vêm
dessas réplicas. Como o suporte permanece fixo nessa etapa, os intervalos
quantificam a variação entre fibrilas condicionada ao $s_{min}$ escolhido;
eles não incorporam a incerteza adicional da seleção do suporte.

Esse procedimento segue a lógica de Clauset, Shalizi e Newman — máxima
verossimilhança discreta, seleção objetiva por KS, teste absoluto e comparação
com alternativas —, mas não é uma aplicação literal do bootstrap
semiparamétrico iid do artigo. A modificação é necessária porque os eventos
de uma mesma fibrila são dependentes. Consequentemente, os resultados abaixo
devem ser descritos como testes de Clauset adaptados à hierarquia da simulação.

## 3. Ajustes individuais do corte estendido

| $T_s$ | $s_{min}$ | eventos na cauda | fração | $\alpha$ (IC 95%) | $\beta$ (IC 95%) | $s_c$ (IC 95%) | KS | $p_{bloco}$ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 34 | 78.888 | 1,161% | 1,815 [1,384; 3,082] | 0,730 [0,685; 4,690] | 34,0 [34,0; 295,0] | 0,00907 | 0,728 |
| 8 | 88 | 9.097 | 0,071% | 2,646 [1,697; 4,254] | 0,834 [0,393; 5,000] | 88,0 [88,0; 727,2] | 0,00812 | 0,827 |
| 16 | 7 | 360.639 | 1,912% | 2,000 [1,576; 2,130] | 1,310 [0,563; 2,682] | 157,0 [23,5; 248,6] | 0,00460 | 0,678 |
| 32 | 5 | 466.517 | 1,732% | 2,378 [2,301; 2,436] | 2,374 [1,323; 4,057] | 293,9 [225,3; 341,7] | 0,00545 | 0,242 |
| 64 | 13 | 86.001 | 0,243% | 2,386 [1,817; 2,507] | 2,092 [0,651; 3,295] | 218,3 [36,3; 258,0] | 0,00295 | 0,915 |
| 128 | 22 | 29.047 | 0,074% | 2,470 [2,323; 2,574] | 2,461 [1,812; 3,279] | 236,8 [194,3; 262,3] | 0,00259 | 0,828 |
| 512 | 8 | 140.741 | 0,353% | 2,674 [2,630; 2,718] | 4,005 [2,792; 5,000] | 272,9 [245,6; 295,1] | 0,00192 | 0,735 |
| 1024 | 13 | 59.811 | 0,148% | 2,607 [2,517; 2,698] | 2,821 [2,193; 3,521] | 230,3 [203,9; 257,6] | 0,00233 | 0,809 |
| 4096 | 18 | 34.734 | 0,086% | 2,532 [2,350; 2,658] | 2,378 [1,615; 3,317] | 210,9 [156,0; 250,4] | 0,00271 | 0,750 |
| 8192 | 21 | 24.653 | 0,062% | 2,484 [2,322; 2,623] | 2,377 [1,743; 3,129] | 232,4 [185,5; 269,4] | 0,00263 | 0,901 |

![CCDFs dos dez ajustes individuais.](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/individual_ccdf.png)

*Figura 1 — CCDF empírica e modelo ajustado acima do suporte selecionado
separadamente em cada condição. O $p$-valor de cada painel usa 999 réplicas de
fibrilas.*

Os dez $p$-valores estão acima do limiar conservador de 0,10. Essa não
rejeição estabelece adequação estatística no suporte indicado, mas não prova
que a forma funcional seja verdadeira ou única. Em particular, o KS pondera
a maior diferença vertical entre CDFs e pode ser pouco sensível às últimas
observações da cauda, onde as frequências são muito pequenas.

## 4. Parâmetros em função de $T_s$

![Parâmetro alpha em função de Ts.](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/ts_vs_alpha.png)

*Figura 2 — Estimativas individuais de $\alpha$ e intervalos percentis de 95%
por fibrilas, condicionados ao suporte selecionado.*

![Parâmetro beta em função de Ts.](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/ts_vs_beta.png)

*Figura 3 — Estimativas individuais de $\beta$ e intervalos percentis de 95%.
O limite superior do ajuste é $\beta=5$.*

![Escala de corte em função de Ts.](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/ts_vs_sc.png)

*Figura 4 — Estimativas individuais de $s_c$ e intervalos percentis de 95%.
O limite inferior permitido é $s_c=s_{min}$.*

Os gráficos sugerem que, a partir de $T_s=128$, $\alpha$ permanece próximo de
2,5 e $s_c$ fica aproximadamente entre 211 e 273. Essa semelhança é apenas
descritiva: como cada ponto condiciona a distribuição a um suporte diferente,
os intervalos não constituem um teste de igualdade nem demonstram um platô
paramétrico comum.

As condições $T_s=2$ e 8 exigem cautela adicional. Seus ajustes observados
atingem $s_c=s_{min}$; no bootstrap, isso ocorre em 660 de 999 réplicas para
$T_s=2$ e em 354 de 999 para $T_s=8$. Além disso, 210 réplicas de $T_s=8$
atingem $\beta=5$. Esses limites e os intervalos largos mostram que os três
parâmetros não são identificados separadamente com precisão nessas caudas.
Em $T_s=512$, 92 réplicas também atingem $\beta=5$, de modo que a estimativa
alta de $\beta$ não deve ser interpretada como um máximo físico.

## 5. O corte estendido é o modelo mais simples adequado?

Para responder a essa pergunta sem alterar o objeto comparado, potência pura,
exponencial discreta, potência com corte exponencial simples e lognormal foram
ajustadas no mesmo $s_{min}$ selecionado pelo corte estendido. Cada alternativa
recebeu o mesmo teste por fibrilas com 999 réplicas.

| $T_s$ | exponencial | potência pura | corte simples | lognormal | corte estendido | menor complexidade não rejeitada |
|---:|---:|---:|---:|---:|---:|:---|
| 2 | 0,001 | 0,005 | 0,685 | 0,864 | 0,728 | corte simples ou lognormal |
| 8 | 0,006 | 0,195 | 0,858 | 0,727 | 0,827 | potência pura |
| 16 | 0,001 | 0,001 | 0,909 | 0,055 | 0,678 | corte simples |
| 32 | 0,001 | 0,048 | 0,027 | 0,006 | 0,242 | corte estendido |
| 64 | 0,001 | 0,006 | 0,555 | 0,144 | 0,915 | corte simples ou lognormal |
| 128 | 0,001 | 0,001 | 0,016 | 0,001 | 0,828 | corte estendido |
| 512 | 0,001 | 0,048 | 0,060 | 0,023 | 0,735 | corte estendido |
| 1024 | 0,001 | 0,001 | 0,028 | 0,003 | 0,809 | corte estendido |
| 4096 | 0,001 | 0,001 | 0,010 | 0,001 | 0,750 | corte estendido |
| 8192 | 0,001 | 0,001 | 0,048 | 0,002 | 0,901 | corte estendido |

![Testes absolutos dos modelos concorrentes.](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/model_gof.png)

*Figura 5 — $p$-valores dos testes absolutos por fibrilas. A linha tracejada
marca o limiar de 0,10; modelos abaixo dela são rejeitados no suporte
comparado.*

Em $T_s=2$, corte simples e lognormal têm dois parâmetros e nenhum é rejeitado.
Uma comparação de Vuong baseada nas contribuições das 50 fibrilas não os
distingue ($p=0{,}822$), portanto os dados não identificam um vencedor. Em
$T_s=64$, as duas formas também passam o teste absoluto, mas a comparação
relativa favorece o corte simples ($p=0{,}023$).

O caso $T_s=8$ requer uma formulação especialmente cuidadosa. A potência pura
é a família adequada com menos parâmetros, mas o suporte começa em 88, retém
apenas 9.097 eventos, ou 0,071% do total, e cobre 0,86 década até o maior valor
observado. Assim, a não rejeição não sustenta uma alegação de comportamento
livre de escala; ela apenas diz que o teste não detecta incompatibilidade
naquela cauda curta.

Consequentemente, a resposta depende do nível da pergunta. Se quisermos uma
única família funcional que seja adequada para todas as caudas selecionadas,
o corte estendido é o modelo mais simples entre os candidatos testados que
satisfaz esse requisito. Essa conclusão é condicionada aos suportes escolhidos
pelo próprio corte estendido; permitir que cada alternativa descarte uma
fração diferente dos dados responderia a outra pergunta. Se escolhermos um
modelo separadamente em cada condição, o corte estendido é mais complexo do
que o necessário em $T_s=2,8,16$ e 64.

## 6. Interpretação permitida

Os resultados apoiam o uso do corte estendido como descrição empírica uniforme
das caudas, sem impor parâmetros comuns. Eles não apoiam uma lei universal
para $\alpha$, $\beta$ ou $s_c$, nem transformam a semelhança observada em uma
relação causal com a morfologia das fibrilas. Da mesma forma, nenhuma das
potências ajustadas deve ser apresentada como evidência de criticalidade
auto-organizada, comportamento livre de escala ou classe universal de
compartilhamento de carga.

## 7. Reprodução e evidência

A análise foi executada no ambiente virtual do repositório com:

```bash
.venv/bin/python Code/Data_analysis/run_stretched_cutoff_individual.py \
  --replicates 999 --workers 6 \
  --output /tmp/stretched_cutoff_individual_all_ts
```

O diretório indicado em `--output` deve estar vazio, pois o programa se recusa
a sobrescrever uma execução anterior.

Os artefatos completos são:

- [ajustes, intervalos e testes absolutos](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/model_fits.csv);
- [varreduras individuais de $s_{min}$](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/xmin_scan.csv);
- [49.950 reajustes por blocos](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/block_bootstrap.csv);
- [comparações relativas entre corte simples e lognormal](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/model_comparisons.csv);
- [metadados da execução](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/analysis.json).

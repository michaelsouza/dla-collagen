# Recomendação: duas figuras principais para as avalanches

## Decisão

Para apresentar a análise de distribuição de avalanches usando apenas duas
figuras, recomendamos:

1. a distribuição completa dos tamanhos;
2. a figura de concentração e escalas características.

Essa combinação mostra tanto a forma empírica das distribuições quanto as
medidas quantitativas que resumem sua evolução com $T_s$.

## Figura 1 — Distribuição completa dos tamanhos

Arquivo: `full_distribution_overview.pdf`.

Essa deve ser a figura principal da distribuição. Ela deve apresentar as
CCDFs/PMFs empíricas não binadas, os quantis e a composição da população de
eventos. Sua função é mostrar que:

- não ocorre uma translação simples da distribuição com $T_s$;
- o percentil 90 dos eventos $s\geq2$ cai de 27 para 5;
- o percentil 99 cresce de 270 para aproximadamente 1300;
- a probabilidade de eventos unitários aumenta de 0,765 para 0,922;
- avalanches pequenas coexistem com uma população rara de avalanches muito
  grandes.

Essa figura deve substituir a apresentação baseada em retas ajustadas a
histogramas log-log. Os dados mostrados são discretos e não binados.

## Figura 2 — Concentração e escalas características

Arquivo: `avalanche_behavior_metrics.pdf`.

Essa figura reúne quatro diagnósticos não paramétricos:

- fração da soma dos tamanhos carregada pelos maiores 10%, 1%, 0,1% e 0,01%
  dos eventos;
- escala característica $\langle s^2\rangle/\langle s\rangle$ e mediana da
  escala superior;
- partição empírica entre a escala pequena e a escala superior;
- curvas de Lorenz dos tamanhos.

Ela quantifica a polarização observada na Figura 1. Os principais valores a
reportar são:

- os maiores 10% dos eventos carregam 69,63% da soma em $T_s=2$ e 91,48% em
  $T_s=8192$;
- os maiores 1% carregam 20,64% e 59,16%, respectivamente;
- $\langle s^2\rangle/\langle s\rangle$ cresce de 140,6 para aproximadamente
  1200;
- a fração de eventos na escala superior cai de 23,12% para aproximadamente
  1,77%;
- a mediana da escala superior cresce de 23 para aproximadamente 1345.

## Mensagem conjunta das duas figuras

As figuras sustentam a seguinte interpretação:

> A distribuição de tamanhos de avalanche não é descrita por uma lei de
> potência universal. À medida que $T_s$ aumenta, a população torna-se mais
> polarizada: predominam eventos pequenos, enquanto uma fração rara de eventos
> muito grandes concentra uma parte crescente do tamanho acumulado. Para
> $T_s\geq512$, as escalas superiores e a forma normalizada das distribuições
> apresentam estabilização empírica aproximada.

Essa estabilização não deve ser chamada de ponto crítico, comportamento
*scale-free*, universalidade ou transição de fase. Também não deve ser
convertida em um novo expoente de avalanche.

## Figuras que ficam fora do corpo principal

As figuras de cruzamentos das CCDFs, agrupamento hierárquico e colapso da escala
superior são úteis como material suplementar e como evidência detalhada na
resposta aos pareceristas, mas não são necessárias no corpo principal se o
limite for de apenas duas figuras.

## Escopo estatístico

Os ajustes e testes de distribuição usam os tamanhos locais discretos e não
binados com $s\geq2$. Os singletons são preservados e aparecem apenas na
descrição da composição da população completa. Todas as conclusões são
condicionais ao modelo com módulo de Weibull $m=2$ e ao ensemble revisado de
50 geometrias por $T_s$.

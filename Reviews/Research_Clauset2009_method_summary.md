# Resumo metodológico de Clauset, Shalizi e Newman (2009)

## Registro e escopo

Este documento registra uma leitura metodológica do artigo *Power-Law
Distributions in Empirical Data*, de Aaron Clauset, Cosma Rohilla Shalizi e
M. E. J. Newman, publicado em 2009.

Fonte primária local:
[`Bibliograph/Clauset2009.md`](../Bibliograph/Clauset2009.md).

O objetivo deste resumo é estabelecer a interpretação do artigo que servirá de
base para análises posteriores. Ele não registra resultados específicos das
simulações de fibrilas e não substitui a nota da Issue #5,
[`Research_Issue5_avalanche_distribution_statistics.md`](Research_Issue5_avalanche_distribution_statistics.md).

## Ideia central

Clauset, Shalizi e Newman não propõem uma maneira de “provar” que os dados
seguem uma lei de potência. Eles propõem um protocolo para responder duas
perguntas mais cuidadosas:

1. Uma lei de potência é uma descrição estatisticamente plausível da cauda?
2. Ela é preferível a outras distribuições plausíveis?

Isso exige três etapas independentes:

1. estimar o expoente \(\alpha\) e o limite inferior \(x_{\min}\);
2. testar a qualidade absoluta do ajuste;
3. comparar a lei de potência com modelos concorrentes.

Um gráfico aproximadamente reto em escala log–log não responde nenhuma dessas
perguntas.

## 1. O que é ajustado

A lei de potência tem a forma

\[
p(x)\propto x^{-\alpha}.
\]

Em dados reais, ela normalmente só é proposta acima de um limite inferior
\(x_{\min}\):

\[
p(x)\propto x^{-\alpha}, \qquad x\ge x_{\min}.
\]

Portanto, o artigo não afirma que a distribuição inteira precisa ser uma lei de
potência. O objeto do teste é a cauda acima de \(x_{\min}\).

Para dados contínuos,

\[
p(x)=\frac{\alpha-1}{x_{\min}}
\left(\frac{x}{x_{\min}}\right)^{-\alpha}.
\]

Para dados inteiros,

\[
p(x)=\frac{x^{-\alpha}}{\zeta(\alpha,x_{\min})},
\]

onde \(\zeta\) é a função zeta de Hurwitz. Essa distinção é crucial para
tamanhos de avalanche, que são variáveis discretas.

## 2. Estimação do expoente

O expoente deve ser estimado por máxima verossimilhança, e não pela inclinação
de histogramas.

Para dados contínuos,

\[
\hat{\alpha}
=
1+n\left[
\sum_{i=1}^{n}
\ln\left(\frac{x_i}{x_{\min}}\right)
\right]^{-1}.
\]

Para dados discretos, o estimador exato é obtido numericamente maximizando

\[
\ell(\alpha)
=
-n\ln\zeta(\alpha,x_{\min})
-\alpha\sum_i\ln x_i.
\]

O artigo também apresenta a aproximação

\[
\hat{\alpha}\simeq
1+n\left[
\sum_i
\ln\left(
\frac{x_i}{x_{\min}-1/2}
\right)
\right]^{-1},
\]

mas ela só fica razoavelmente precisa quando \(x_{\min}\gtrsim6\). Para
avalanche pequenas, deve-se preferir a maximização discreta exata.

Outro detalhe importante é a relação entre o expoente da densidade e a
inclinação da distribuição acumulada complementar. Se a CCDF contínua aparece
como

\[
P(X\ge x)\propto x^{-\beta},
\]

então

\[
\alpha=\beta+1.
\]

A inclinação da CCDF não é diretamente \(-\alpha\).

## 3. Escolha de \(x_{\min}\)

Escolher \(x_{\min}\) visualmente é inadequado:

- um valor muito baixo inclui dados que não seguem a lei de potência e gera
  viés;
- um valor muito alto descarta informação, reduz \(n_{\mathrm{tail}}\) e
  aumenta a incerteza.

O procedimento recomendado é testar cada candidato a \(x_{\min}\):

1. ajustar \(\alpha\) usando somente \(x_i\ge x_{\min}\);
2. calcular a distância de Kolmogorov–Smirnov,

   \[
   D=\max_{x\ge x_{\min}}|S(x)-P(x)|;
   \]

3. escolher o \(x_{\min}\) que minimiza \(D\).

Devem sempre ser reportados juntos:

\[
\hat{\alpha},\quad \hat{x}_{\min},\quad n_{\mathrm{tail}}.
\]

Nos testes sintéticos difíceis do artigo, uma boa estimação de \(x_{\min}\)
exigiu aproximadamente mil observações na cauda. Isso é uma referência
empírica, não um limiar universal.

## 4. Teste de qualidade do ajuste

Encontrar o melhor \(\alpha\) não significa que a lei de potência seja um bom
modelo. Qualquer conjunto de dados admite algum “melhor ajuste” dentro dessa
família.

O artigo usa um teste Monte Carlo semiparamétrico:

1. ajustar \(\hat{x}_{\min}\) e \(\hat{\alpha}\) aos dados;
2. calcular o KS observado;
3. gerar muitas amostras sintéticas:
   - abaixo de \(x_{\min}\), reamostrar a distribuição empírica;
   - acima de \(x_{\min}\), gerar dados da lei de potência ajustada;
4. reajustar \(x_{\min}\) e \(\alpha\) separadamente em cada amostra sintética;
5. calcular o KS de cada réplica;
6. definir \(p\) como a fração das réplicas cujo KS é maior que o observado.

Reajustar os parâmetros em cada réplica é indispensável. Não se deve usar
diretamente a distribuição assintótica usual do KS porque os parâmetros foram
estimados dos próprios dados.

A regra conservadora adotada no artigo é:

- \(p\le0.1\): rejeitar a lei de potência;
- \(p>0.1\): a lei de potência é plausível, isto é, não foi rejeitada.

Um \(p\) alto não confirma a lei de potência e não representa a probabilidade de
ela ser verdadeira. Amostras pequenas frequentemente produzem \(p\) alto
simplesmente porque o teste tem pouco poder.

Para precisão Monte Carlo de aproximadamente \(0.01\), o artigo recomenda cerca
de 2500 réplicas.

## 5. Comparação com alternativas

Mesmo que a lei de potência não seja rejeitada, uma lognormal, exponencial ou
lei de potência com corte pode ajustar tão bem quanto ou melhor.

Para modelos não aninhados, o artigo usa a razão de log-verossimilhanças:

\[
\mathcal R
=
\sum_i
\left[
\ln p_1(x_i)-\ln p_2(x_i)
\right].
\]

Quando \(p_1\) é a lei de potência:

- \(\mathcal R>0\): favorece a lei de potência;
- \(\mathcal R<0\): favorece a alternativa.

O sinal só é interpretável quando o valor \(p\) do teste de Vuong é pequeno. Se
esse \(p\) for grande, o resultado é inconclusivo.

Há, portanto, dois valores \(p\) com sentidos diferentes:

- no teste KS, \(p\) pequeno rejeita o modelo;
- na comparação de verossimilhanças, \(p\) pequeno torna confiável o sinal de
  \(\mathcal R\).

Lei de potência pura e lei de potência com corte são modelos aninhados. Nesse
caso, o teste de Vuong comum não vale; é necessário o teste próprio baseado no
limite qui-quadrado de Wilks.

## 6. Por que regressão log–log não serve para inferência

O artigo rejeita o procedimento tradicional de ajustar uma reta a um
histograma log–log porque:

- os resultados dependem do binning;
- o logaritmo altera a distribuição dos erros;
- pontos sucessivos da CCDF são correlacionados;
- os erros fornecidos pela regressão ficam incorretos;
- um \(R^2\) alto também aparece para distribuições que não são leis de
  potência;
- a reta ajustada pode nem representar uma distribuição normalizada.

Gráficos PDF e CCDF continuam úteis para visualização, mas não para inferência
do expoente nem validação do modelo.

## 7. Resultado empírico do artigo

Ao aplicar o protocolo a 24 conjuntos de dados previamente associados a leis de
potência:

- 17 não rejeitaram a lei de potência;
- sete a rejeitaram;
- apenas a frequência de palavras apresentou suporte realmente forte à lei de
  potência contra todas as alternativas testadas;
- lognormal e lei de potência foram frequentemente indistinguíveis;
- em vários casos, uma lei de potência com corte foi preferida.

A mensagem é que não rejeitar uma lei de potência é relativamente comum;
demonstrar que ela é a melhor explicação é raro.

## 8. Consequências para a análise de avalanches

Para o trabalho com fibrilas, a leitura de Clauset et al. implica:

1. tratar tamanhos de avalanche como dados discretos;
2. estimar \(s_{\min}\) objetivamente por KS;
3. ajustar o expoente por máxima verossimilhança discreta;
4. reportar \(n_{\mathrm{tail}}\);
5. executar o teste semiparamétrico com reajuste completo em cada réplica;
6. comparar potência pura, potência com corte, lognormal discreta e exponencial
   discreta;
7. considerar explicitamente o tamanho finito da fibrila;
8. não interpretar um expoente ou um bom ajuste como evidência automática de
   criticalidade auto-organizada, comportamento *scale-free* ou universalidade
   de compartilhamento de carga;
9. tratar separadamente a possível dependência entre avalanches da mesma
   fibrila, pois a teoria do artigo pressupõe observações independentes e
   identicamente distribuídas.

## 9. Limites das conclusões

Mesmo uma aplicação correta do protocolo permite concluir apenas que uma lei de
potência é ou não uma descrição plausível da cauda observada e, eventualmente,
que ela é favorecida em relação a um conjunto explícito de alternativas.

O protocolo não estabelece:

- que a lei de potência é a distribuição verdadeira;
- que não existe outra distribuição igualmente plausível;
- que o sistema é *scale-free* em todos os tamanhos;
- que há criticalidade auto-organizada;
- que um mecanismo físico específico gerou o expoente;
- que o expoente pertence a uma classe universal de compartilhamento de carga.

Identificação estatística da forma da cauda e explicação mecanística são etapas
científicas diferentes.

## Nota sobre a transcrição Markdown

A versão local em Markdown apresenta alguns sinais de conversão ou OCR,
incluindo sinais ausentes ou fórmulas mal transcritas em tabelas e apêndices.
Para reprodução literal de uma expressão, a versão publicada em PDF deve
prevalecer. Isso não altera as conclusões metodológicas registradas acima.

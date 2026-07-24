# Issue #3 — protocolo de ruptura em Parkinson et al. (1997)

## Pergunta e conclusão

Esta nota verifica se Parkinson et al. (1997) permite defender, sem alterar as
simulações existentes, o encerramento de um nível de força após um sweep sem
novas quebras.

**Conclusão curta:** Parkinson et al. fornece precedente direto para o
**critério operacional** usado no código: após uma quebra, reavaliar a estrutura
no mesmo \(F\) e aumentar \(F\) em \(0.5\) somente quando uma passagem não
produzir novas quebras. A referência, porém, não demonstra que esse primeiro
sweep vazio seja um equilíbrio mecânico ou uma estabilidade estocástica sob
tempo de espera ilimitado. A defesa fiel à fonte é, portanto, preservar o
protocolo e as simulações, mas substituir a alegação de “mechanically stable
equilibrium” por “operational stopping criterion of the prescribed discrete
loading protocol”.

## Fontes primárias examinadas

- Parkinson et al., “The Mechanical Properties of Simulated Collagen Fibrils”,
  *Journal of Biomechanics* 30, 549–554 (1997), integralmente transcrito em
  [`Bibliograph/Parkinson1997.md`](../Bibliograph/Parkinson1997.md).
- Equações e descrição atuais do manuscrito em
  [`Paper/paper_PRE.tex`, Eqs. 2–4 e protocolo](../Paper/paper_PRE.tex#L173-L204).
- Implementação atual em
  [`Code/Fracture_fibril/stress_strain_ava.py`](../Code/Fracture_fibril/stress_strain_ava.py#L159-L245)
  e seu loop de ruptura
  ([linhas 427–514](../Code/Fracture_fibril/stress_strain_ava.py#L427-L514)).
- Comentário R2-1, que distingue corretamente um sweep sem evento de
  estabilidade sob novos sorteios no mesmo \(F\), em
  [`Reviews/Referees-comment-Suki.md`, linhas 85–91](Referees-comment-Suki.md#L85-L91).

As referências que Parkinson cita para modelos gerais de fratura não são
necessárias para decidir o que o algoritmo específico de Parkinson faz. Por
isso, não foram usadas fontes secundárias para preencher detalhes que o artigo
de 1997 não documenta.

## 1. O procedimento de Parkinson

Na seção Methods, Parkinson divide o núcleo em seções e assume equipartição da
carga em cada seção:

\[
\sigma(i)=\frac{F}{N(i)}.
\]

O artigo justifica essa expressão dizendo que equilíbrio mecânico requer carga
constante ao longo da amostra. Nesse trecho, “mechanical equilibrium” descreve
o balanço axial que fundamenta a distribuição de tensão, não um critério
estocástico de parada
([Parkinson, Methods, p. 551, linhas 68–72](../Bibliograph/Parkinson1997.md#L68-L72)).

Para uma haste, Parkinson usa a média de \(\sigma(i)\) nas seções atravessadas
e define a probabilidade de remoção

\[
P_b=\left(\frac{\sigma}{n\sigma_c}\right)^m,
\]

onde \(n\) representa coordenação, \(\sigma_c\) a resistência típica da ligação
e \(m\) a dispersão das resistências, relacionada ao módulo de Weibull
([Parkinson, Methods, p. 551, linhas 74–82](../Bibliograph/Parkinson1997.md#L74-L82)).
Logo, a escolha atual da **tensão média** nas Eqs. 3–4 do manuscrito tem
precedente explícito nessa fonte. Esse precedente documenta a origem da escolha,
mas, por si só, não substitui uma justificativa física ou uma análise de
sensibilidade entre média e máximo solicitada no Issue #3.

O passo decisivo está no fim da seção Methods. As hastes são avaliadas em um
valor de \(F\), as selecionadas probabilisticamente são removidas, o esqueleto é
reavaliado e a tensão é recalculada. O procedimento se repete, e \(F\) só
aumenta, em incrementos de \(0.5\), quando não ocorrem novos eventos de quebra
([Parkinson, Methods, p. 551, linha 84](../Bibliograph/Parkinson1997.md#L84)).

Assim, Parkinson sustenta diretamente que:

1. há nova avaliação no mesmo \(F\) após uma passagem que produz dano;
2. a geometria resistente e a tensão são reavaliadas depois do dano;
3. o primeiro passo sem nova quebra autoriza o incremento de carga;
4. o incremento adotado é \(\Delta F=0.5\).

## 2. Resorteio ou limiares *quenched*?

Parkinson chama \(P_b\) de probabilidade de remoção e manda repetir a avaliação,
mas não documenta como os números aleatórios são gerados ou conservados. Em
particular, o artigo não diz se:

- cada haste recebe uma única variável aleatória persistente, equivalente a um
  limiar *quenched*; ou
- uma nova variável aleatória é sorteada a cada avaliação.

A associação de \(m\) à dispersão de resistências e o uso da expressão
“fracture thresholds” não bastam para concluir que um limiar persistente foi
armazenado; o procedimento computacional correspondente não é descrito
([Parkinson, Methods, p. 551, linhas 80–84](../Bibliograph/Parkinson1997.md#L80-L84)).
Portanto, não é fiel à fonte afirmar que Parkinson usou thresholds *quenched*,
nem é possível provar, somente pelo artigo, a identidade dos sorteios entre
passagens.

O código atual, ao contrário, é inequívoco: a cada chamada de
`random_deleted_rids`, `np.random.random(len(ssd.rods))` cria um novo conjunto
de valores
([`stress_strain_ava.py`, linhas 427–437](../Code/Fracture_fibril/stress_strain_ava.py#L427-L437)).
Essa função é chamada novamente em cada iteração, inclusive quando \(F\)
permanece constante após uma passagem com falhas
([linhas 480–491](../Code/Fracture_fibril/stress_strain_ava.py#L480-L491)).
A classe `Rod` não armazena um limiar aleatório persistente
([linhas 159–186](../Code/Fracture_fibril/stress_strain_ava.py#L159-L186)).

Essa distinção é material:

- com limiar *quenched*, sobreviver a uma avaliação em uma configuração
  inalterada implica sobreviver a outra avaliação idêntica;
- com resorteio independente, sobreviver a uma passagem não elimina a
  probabilidade de falhar na seguinte.

## 3. Um sweep vazio é estabilidade?

Não no sentido estocástico ou temporal levantado pelo Referee. Para uma
configuração inalterada com probabilidades \(p_j>0\), a probabilidade de nenhum
evento em uma passagem é

\[
q=\prod_j(1-p_j)>0.
\]

Se o algoritmo executasse outra passagem independente na mesma configuração, a
probabilidade de ao menos uma quebra seria \(1-q>0\). Repetidas passagens
indefinidamente levariam a novas quebras mesmo sem aumentar \(F\). O Referee
está correto sob essa interpretação.

Parkinson não chama a passagem sem quebra de equilíbrio ou estabilidade. O
artigo somente diz que a ausência de um novo evento aciona o próximo incremento
de força ([Methods, p. 551, linha 84](../Bibliograph/Parkinson1997.md#L84)).
Há duas menções próximas que não devem ser confundidas com esse critério:

- a introdução descreve genericamente outros modelos, com nós indeformáveis e
  ligações elásticas, nos quais a rede relaxa após a quebra até um novo
  equilíbrio
  ([Introduction, p. 550, linha 41](../Bibliograph/Parkinson1997.md#L41));
- o modelo específico de Parkinson é declarado frágil, sem deformação e sem
  reassociação das hastes removidas
  ([Methods, p. 551, linha 84](../Bibliograph/Parkinson1997.md#L84)).

Além disso, como observado acima, a expressão “mechanical equilibrium” na
formulação específica justifica carga axial constante e equipartição em uma
seção, não transforma uma realização sem falha em estado absorvente
([Methods, p. 551, linhas 68–72](../Bibliograph/Parkinson1997.md#L68-L72)).

Logo, o primeiro sweep vazio deve ser apresentado como uma **regra de parada e
avanço da carga**, não como prova de que \(P_R\) se anulou ou de que nenhuma
quebra poderia ocorrer sob permanência indefinida no mesmo \(F\).

## 4. Interpretação de tempo, passo de carga e probabilidade

Parkinson não atribui duração física a uma passagem do algoritmo, não define
tempo de permanência em cada \(F\) e não trata \(P_b\) como taxa de risco por
unidade de tempo. A grandeza que o procedimento controla é a força aplicada:
\(F\) é aumentada em passos de \(0.5\), enquanto a tensão em uma seção é
\(F/N(i)\)
([Methods, p. 551, linhas 68–84](../Bibliograph/Parkinson1997.md#L68-L84)).

Assim, a interpretação mais estrita e defensável é:

- um sweep é uma tentativa discreta de atualização de dano;
- \(P_R\) é uma probabilidade adimensional **por avaliação**, não um hazard
  térmico ou uma probabilidade por segundo;
- um nível de força contém tantas avaliações quantas forem necessárias enquanto
  cada avaliação precedente produz novas quebras;
- a primeira avaliação sem quebra encerra operacionalmente esse nível de força;
- creep, fadiga e vida útil sob força mantida durante um tempo físico estão fora
  do modelo.

“Discrete progressively stepped loading protocol” é uma descrição diretamente
amparada pelo algoritmo. “Quasistatic” pode ser usado como caracterização do
regime de passos de carga e atualizações de dano, desde que não seja definido
como relaxamento estocástico completo nem como limite de tempo infinito.

## 5. Até onde o código equivale a Parkinson

### Equivalência sustentada

| Elemento | Parkinson (1997) | Manuscrito/código atual |
|---|---|---|
| Tensão na seção | \(\sigma(i)=F/N(i)\) | Eq. 2 e `Rod.update_sigma` |
| Tensão da haste | média nas seções atravessadas | Eq. 3 e `np.mean(...)` |
| Remoção | probabilidade potência com \(m\) | Eq. 4 e `Rod.prob_break` |
| Passagem com dano | reavaliar no mesmo \(F\) | `F` não muda no ramo com remoção |
| Passagem sem dano | incrementar \(F\) | linhas 488–491 |
| Incremento | \(\Delta F=0.5\) | linha 490 |
| Dano | irreversível, sem reassociação | hastes removidas não retornam |

Fontes: [Parkinson, Methods, p. 551, linhas
68–84](../Bibliograph/Parkinson1997.md#L68-L84);
[manuscrito, linhas 173–204](../Paper/paper_PRE.tex#L173-L204);
[código, linhas 214–245](../Code/Fracture_fibril/stress_strain_ava.py#L214-L245)
e [473–514](../Code/Fracture_fibril/stress_strain_ava.py#L473-L514).

Esse paralelismo permite dizer que o **fluxo algorítmico e o stopping rule**
seguem Parkinson. Não permite dizer que todos os detalhes estocásticos ou de
atualização são “exactly the same”, pois o artigo não os especifica.

### Ressalvas necessárias

1. **Sorteios.** Parkinson não informa se reutiliza ou resorteia a variável
   aleatória; o código atual resorteia.

2. **Coordenação.** Parkinson introduz \(n\) como o número de vizinhos de uma
   partícula antes de escrever a probabilidade para a haste
   ([p. 551, linha 74](../Bibliograph/Parkinson1997.md#L74)). O manuscrito atual
   usa \(K\), soma de contatos ao longo da molécula
   ([`paper_PRE.tex`, linhas 187–195](../Paper/paper_PRE.tex#L187-L195)), e o
   código usa `len(self.neigh_pids)`
   ([`stress_strain_ava.py`, linhas 214–223](../Code/Fracture_fibril/stress_strain_ava.py#L214-L223)).
   Há continuidade conceitual, mas a agregação da coordenação ao nível da haste
   não está completamente especificada por Parkinson.

3. **Reavaliação de tensão.** Parkinson diz que, após remover as hastes, o
   esqueleto é reavaliado e a tensão recalculada. No código atual, remover uma
   haste invalida o cache (`updated=False`) das hastes que eram suas vizinhas
   espaciais
   ([linhas 192–212](../Code/Fracture_fibril/stress_strain_ava.py#L192-L212)).
   Porém, a remoção também reduz \(N(i)\) para todas as hastes que atravessam a
   mesma seção. Uma haste não vizinha nessa seção pode permanecer com
   `updated=True`; nesse caso, `prob_break` chama somente `update_force`, que,
   para o mesmo \(F\), conserva a tensão média em cache
   ([linhas 214–245](../Code/Fracture_fibril/stress_strain_ava.py#L214-L245)).
   Portanto, as frases atuais “immediately updated across the remaining
   backbone” e “exact iterative relaxation procedure” são mais fortes do que a
   implementação demonstra.

4. **Probabilidade acima de um.** Nem Parkinson nem a Eq. 4 atual especificam
   explicitamente um truncamento. No código, como \(u\in[0,1)\), qualquer
   `p >= 1` implica remoção certa, equivalente operacionalmente a
   \(\min(1,p)\)
   ([linhas 427–437](../Code/Fracture_fibril/stress_strain_ava.py#L427-L437)).
   Isso pode ser documentado sem mudar os resultados.

5. **Avalanches.** Parkinson não define avalanches. A referência sustenta o
   protocolo de carregamento, não a definição espacial ou temporal de evento. A
   decisão sobre avalanche pertence ao ticket subsequente e não deve ser
   apresentada como consequência de Parkinson.

## 6. Formulação fiel para a resposta ao Referee

> We thank the Referee for pointing out that the meaning of a no-event sweep was
> insufficiently explained. Our rupture model does not introduce physical time,
> a dwell time at fixed load, or a thermally activated failure rate.
> Accordingly, \(P_R\) is a dimensionless removal probability evaluated during
> a discrete damage-update sweep, not a hazard per unit physical time.
>
> The loading and stopping rule follows the procedure introduced by Parkinson
> et al. (1997). At a prescribed force \(F\), all currently load-bearing
> molecules are assessed. If removals occur, the active skeleton is reassessed
> and another damage sweep is performed at the same external force. The force
> is increased by \(\Delta F=0.5\) only after a complete sweep produces no new
> breaking event, as specified in the original model.
>
> We agree, however, that a no-event sweep should not be described as an
> absorbing stochastic equilibrium: because \(P_R\) can remain nonzero, another
> independent trial at the same unchanged configuration could produce further
> removal. It is instead the operational stopping criterion of this discrete,
> progressively stepped damage protocol. The model therefore characterizes
> failure under stepped loading and is not intended to describe creep, fatigue,
> or lifetime under a force held constant for a physical duration. We have
> revised the manuscript to make this distinction explicit.

Essa formulação não tenta provar que a estabilidade foi “alcançada”. Ela aceita
a observação matemática do Referee, delimita o modelo e mostra que a regra
questionada não é uma escolha criada *ad hoc* no presente trabalho. É a
estratégia mais forte que Parkinson permite sem alegar além da evidência.

### Frase sugerida para Methods

> After any sweep that produces removals, the active skeleton is reassessed and
> the damage sweep is repeated at the same \(F\). Following Parkinson et al.
> (1997), \(F\) is increased by \(\Delta F=0.5\) after the first complete sweep
> with no new breaking event. This no-event sweep is the operational stopping
> criterion of the discrete loading protocol; it is not interpreted as
> vanishing failure probability or as stability under an indefinitely held
> load.

## Decisão recomendada para o Issue #3

É possível preservar o stopping rule e as simulações existentes com uma
resposta cientificamente defensável, desde que:

1. o texto não chame um sweep vazio de equilíbrio mecânico, estabilidade
   estocástica ou “full relaxation”;
2. \(P_R\) seja definido como probabilidade adimensional por avaliação;
3. o escopo exclua explicitamente creep, fadiga e vida útil sob carga constante;
4. Parkinson seja citado como precedente do algoritmo, não como prova de
   estabilidade em tempo infinito;
5. a equivalência seja limitada ao fluxo do protocolo, sem afirmar identidade
   total na atualização de tensão ou no tratamento dos sorteios;
6. a definição de avalanche seja retirada desta defesa e resolvida no ticket
   próprio.

Essa decisão resolve a interpretação do stopping rule sem exigir uma nova
simulação. Ela não resolve, por si só, os demais critérios do Issue #3, em
especial a atualização global da tensão após remoção e a sensibilidade entre
tensão média e máxima.

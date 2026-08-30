# A fibrila simulada é fina demais — e isso atinge o diâmetro e a dimensão fractal

**Data:** 2026-08-30
**Afeta:** N7, N12, N15, I8; fundamenta a Fase C

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## O que esta entrada estabelece

Duas medidas centrais do artigo — o diâmetro da fibrila e a dimensão fractal
$D_f$ — têm o mesmo problema de fundo: **a fibrila que o modelo produz é fina
demais**. Aqui ficam os números, medidos, e o que decorre deles.

## 1. O modelo não sabe quantos nanômetros tem uma unidade de rede

O bastão que representa a molécula tem 18 de comprimento por 1 de largura. A
molécula real tem 300 nm por 1,5 nm — ou seja, 200 por 1. O bastão é atarracado
demais, e por isso a conversão para nanômetros só consegue acertar **uma** das
duas dimensões:

| Se acertamos… | 1 unidade de rede vale | a fibrila fica com |
|:--|---:|---:|
| a **largura** do bastão | 1,5 nm | 54–118 nm de diâmetro |
| o **comprimento** do bastão | 16,7 nm | 600–1.320 nm |

São respostas que diferem por um fator 11. Parkinson1995 usou a primeira e
publicou "0,1 µm".

Fibrilas reais, medidas nas fontes que temos em `Bibliography/`: 101–313 nm
(Quigley2018), 140–490 nm (Yamamoto2017), cerca de 200 nm (Yang2012).

**Nenhuma das duas conversões cai nessa faixa.** Uma fica abaixo, a outra acima.

## 2. Contando moléculas, a diferença é bem maior que em nanômetros

Nanômetro engana, porque o que governa estatística é quantas moléculas existem
numa seção transversal, e área cresce com o quadrado do raio:

| | moléculas por seção transversal |
|:--|---:|
| modelo, fibrila inteira, região central | **~300** |
| modelo, depois do corte $17\times17$ usado na fratura | 59 a 202 |
| **fibrila real de 200 nm** | **~15.000** |

**Fator 50**, e ele já existe na fibrila gerada, antes de qualquer recorte.

Um detalhe que chama atenção: as ~300 moléculas por seção são praticamente as
mesmas em todas as dez condições de $T_s$ (295, 297, 333 nas três medidas). O
$T_s$ decide se essa massa fica espalhada num anel ralo ou apertada num cilindro
denso — mas **não muda quanta massa existe por unidade de comprimento**.

## 3. Lançar mais moléculas não engorda a fibrila o bastante

A saída óbvia seria gerar fibrilas com mais moléculas. Testamos (job 584509,
detalhes em `Reviews/PhaseC_periodic_cylinder/nb_scaling_test.md`), com a mesma
semente nos dois tamanhos para que a única diferença fosse a quantidade:

| $T_s$ | raio com 4× mais moléculas | comprimento |
|---:|---:|---:|
| 2 | 1,40× | 1,99× |
| 128 | 1,32× | 2,01× |
| 8192 | 1,24× | 1,96× |

Quadruplicar a massa **dobra o comprimento e dobra a massa por camada**. O raio
quase não anda — e anda cada vez menos conforme a fibrila fica compacta.

Em outras palavras: **a fibrila simulada cresce em comprimento, não em
grossura.** Para chegar à grossura necessária seriam de 10 milhões a 48 bilhões
de moléculas, conforme a condição. Inviável.

Isso dá conteúdo numérico ao que Parkinson1995 já dizia
(`Bibliography/Parkinson1995.md:168`): falta ao modelo um mecanismo que limite o
diâmetro. Antes era citação; agora é medida nossa.

## 4. A dimensão fractal é ajustada sobre pouco espaço

O $D_f$ sai de um ajuste: mede-se quanta massa cabe dentro de um raio $R$, para
vários $R$, e a inclinação da reta em escala log-log é o $D_f$.

Para essa reta ser confiável, é preciso variar $R$ bastante. A convenção é medir
esse alcance em **décadas** — cada fator de 10 é uma década.

O manuscrito ajusta de $R=5$ unidades de rede (o mínimo que a rede permite) até
o raio máximo da fibrila. Como o raio máximo é pequeno, o alcance é curto:

| $T_s$ | raio máximo | **décadas de ajuste** |
|---:|---:|---:|
| 2 | 39,3 | **0,90** |
| 8 | 36,4 | 0,86 |
| 32 | 32,1 | 0,81 |
| 128 | 22,6 | 0,65 |
| 1024 | 18,9 | 0,58 |
| 8192 | 18,6 | **0,57** |

**Menos de uma década em todas as dez condições.** E o alcance é pior justamente
onde o artigo afirma o platô de $D_f$: em $T_s \geq 512$ são 0,57.

Some-se o que a Fase A já havia registrado
(`2026-08-25_faseA_saturacao_ts.md`): os $D_f$ publicados dependem de uma janela
de ajuste escolhida condição a condição, e usar uma janela comum não reproduz os
valores publicados (dá 1,83/1,93/1,93 contra 1,708/1,790/1,965).

## 5. O problema de consistência — o ponto mais desconfortável

Estamos preparando uma resposta que diz, sobre as avalanches: *0,7 décadas não
sustentam a estimativa de um expoente*.

O $D_f$ é ajustado sobre **0,57 a 0,90 décadas**.

**As duas medidas centrais do artigo repousam em menos de uma década, pela mesma
razão física.** Não é possível aplicar o critério a uma e não à outra: um revisor
que aceite o argumento sobre as avalanches vai aplicá-lo ao $D_f$ três páginas
antes.

## 6. O que decorre

**Para o diâmetro (I8): não declarar escala física.** Reportar em unidades de
rede e em grandezas normalizadas. Um modelo com 300 moléculas por seção contra
15.000 da fibrila real não sustenta comparação em nanômetros, e declará-la só
cria superfície de ataque. Isso é coerente com a ressalva que já está no
manuscrito (`paper_PRE.tex:347`), de que o modelo captura tendências
qualitativas e não predições quantitativas.

**Para N15:** validar o gerador novo contra o $D_f$ publicado é validar contra um
número frágil. Faz mais sentido validar no regime largo, depois da Fase C.

**Para N7 e N12:** o lado estrutural é o mais fraco dos dois. Em N12 soma-se o
confundimento já registrado — o tamanho do corpo de prova varia 3,9× junto com
o $D_f$ ao longo da grade de $T_s$.

**A Fase C resolve os dois de uma vez.** O cilindro periódico dá seção ~13× maior
ao mesmo custo, o que amplia o alcance do ajuste de $D_f$ e ao mesmo tempo testa
se o corte das avalanches é efeito de tamanho. O teste de escala da §3 mostrou
que não existe caminho mais barato.

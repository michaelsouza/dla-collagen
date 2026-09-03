# Auditoria: as onze críticas contra o submetido, o atual e os dados

**Data:** 2026-09-03
**Afeta:** N2, N5, N7, N9, N10, N11, N12, N13, N14; I6, I8; abre I10
**Insumos:** `Paper/submitted_ER12738/paper_PRE.tex` (arquivado hoje do commit
`5d2d272`, 363 linhas), `Paper/paper_PRE.tex` (452 linhas),
`Carta_Resposta/Response_to_Referees.tex`, `Reviews/Referees.md`,
`Reviews/quenched_campaign_report/README.md`, registros de 2026-08-24 a
2026-09-02.

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

## Por que esta auditoria

A tabela de nós acompanha decisões, mas ninguém tinha voltado ao texto dos
revisores e conferido, crítica a crítica, o que o submetido dizia, o que o
manuscrito e a carta dizem hoje, e o que os dados sustentam agora. Com o
submetido arquivado, a comparação ficou verificável. O resultado é que
**manuscrito e carta estão congelados no estado do commit `521a284`** — a
reanálise sobre o protocolo recozido — e descrevem, e defendem, um protocolo
que o projeto abandonou em 2026-08-24.

## Achados que a tabela de nós não registrava

1. **Manuscrito e carta ainda descrevem e defendem o protocolo recozido.**
   `paper_PRE.tex:240-242` (varreduras, $\Delta F = 0{,}5$, "$P_R$ por
   avaliação"), `:312` (avalanche = removidos em varreduras sucessivas) e a
   Eq. (4) com $\min\{1,\cdot\}$. Na carta, R2-1 defende a "primeira varredura
   sem remoção" como critério de parada e R2-3 diz ter adotado a definição do
   revisor mas a descreve por varreduras. Desde 2026-08-24 o protocolo é
   carga extremal com cascata determinística: R2-1 **dissolve-se**, não se
   defende. N2 é maior do que "falta o texto" — é o vocabulário de toda a
   seção de fratura.

2. **A carta em R1-3 contradiz N5.** Diz "all simulations use $m=2$ … we do
   not claim robustness with respect to $m$". A campanha varreu
   $m \in \{1,2,3,5,10\}$, e o resultado — em geometria fixa ($T_s = 8192$),
   $\gamma$ vai de $2{,}830 \pm 0{,}005$ ($m=1$) a $1{,}912 \pm 0{,}013$
   ($m=10$) — é o argumento mais forte para **não** comparar com $5/2$.

3. **Todo número da seção de fratura é do recozido.** $\gamma$ de 1,019 a
   2,253; platô $2{,}204 \pm 0{,}034$; $s_c = 101{,}0 \pm 5{,}6$; 50 fibrilas
   × $10^3$ realizações. A campanha tem 200 fibrilas × 50 realizações × 5 $m$
   por $T_s$; lei de potência pura rejeitada em 48 de 50 condições; corte de
   Araújo vence em 34 de 50; $\eta$ mediano 2,30, não universal; corte
   invariante a $m$, a $T_s \geq 16$ e a 25× em $N$.

4. **A Fig. 3 também muda, não só a Fig. 7.** O estado listava "N7/I6:
   regenerar a Fig. 7 com leitura de *crossover*". Mas a frase "$D_f$ sobe
   de 1,708 a 1,963" está nos resultados (`:170-176`) e na conclusão (`:354`), o resumo
   (`:86`) fala em "evolução sistemática" de $D_f$, e os pontos intermediários
   publicados (1,76 em $T_s=64$; 1,79 em 128) não saem de nenhuma janela objetiva (1,92 / 1,95 na
   fibrila comum; 1,96 no cilindro largo). A Fig. 3 precisa ser regenerada
   sob regra uniforme, ou trocada pela inclinação local; o platô sai de 512
   para $\approx 128$.

5. **A resposta a R1-4 inverte de sinal.** Carta e manuscrito (`:287`) dizem
   "direct numerical validation that $D_f$ … provides a quantitatively
   supported proxy". N7 concluiu o contrário: $D_f$ depende da janela, e as
   grandezas mecanicamente relevantes ($\langle N\rangle$, $\langle K\rangle$,
   fração de preenchimento) devem ser reportadas diretamente. Agrava: a
   Fig. 7(a) correlaciona $D_f$ com $\langle N\rangle$ dentro de uma janela
   fixa de 17×17, onde $N \sim R^{D_f}$ por construção (registro de
   2026-08-29) — é quase tautologia.

6. **I8 resolve-se.** A decisão (2026-08-30, §6) foi não declarar escala
   física. Conferido hoje: os únicos "nm" do manuscrito (`:101`, `:133`) são
   fatos da literatura sobre colágeno real; nenhuma frase converte unidade de
   rede. Não há o que mudar — só manter.

7. **I10, nova.** O manuscrito diz 50 fibrilas por $T_s$ (550 seções). O zip
   das fibrilas publicadas tem **49** em $T_s = 16$ (`unzip -l`). Ou falta um
   arquivo no zip, ou a contagem está errada por um. Conferir antes de N13
   afirmar "50".

8. **O que está feito e conferido no `.tex`:** R1-1 (`:137` "arrive in
   isolation"; conclusão sem enfisema/aneurisma), R1-6 (`:347-349`), R2-2
   (parágrafo de `:230` vale na substância; só troca "probabilidade de
   remoção" por "limiar"). SOC: zero ocorrências de "SOC", "Self-Organized",
   `Bak1987`, `Zapperi1997b`, "5/2" no atual; "universality" aparece uma vez,
   negada (`:336`).

## Crítica a crítica

| Crítica | O submetido dizia | O atual diz | Os dados dizem | Falta | Nó |
|:--|:--|:--|:--|:--|:--|
| **R1-1** $T_s$ sem base física | "$T_s$ não mapeia em pH"; especula enfisema e aneurisma | razão deposição/salto (`:137`); limitação explícita; especulação removida | — | nada; N14 confere as citações da carta contra o `.tex` final | N1 ✔ |
| **R1-2** SOC + estatística | SOC no resumo e no texto; reta em log-log sobre 2 décadas | SOC removido; Eq. (6) corte exponencial por MLE, $\gamma$ 1,019→2,253 (**recozido**) | lei pura rejeitada 48/50; corte de Araújo, $\eta$ não universal; corte invariante a $m$, $T_s$ e tamanho | reescrever `:312-342` e Fig. 9 com a campanha; carta R1-2 (tirar `% TODO`, decidir o controle de percolação) | N4 ✔, **N10**, I7 |
| **R1-3** $\gamma > 5/2$; $m$; 10 fibrilas | de 2,31 a 2,80 "cruzando 5/2", transição LLS→GLS | comparação removida; carta diz "$m=2$ só, sem robustez" | $\gamma$ depende de $m$ tanto quanto de $T_s$; uma década não sustenta expoente | texto da não-afirmação; **carta R1-3 inteira**; `:289` 50×$10^3$ → 200×50×5 | **N11**, N5 ✔ |
| **R1-4** $D_f$ 2D vs 3D | usa $D_f$ como proxy sem justificar | Fig. 7 + "validação numérica direta" (`:255-287`) | $D_f$ depende da janela; *crossover* DLA(1,68)→sólido(2,0) em $T_s\approx128$ | Fig. 3 **e** Fig. 7; resumo, `:170-176`, `:354`; **carta R1-4 inteira**; I6 | N7 ✔ (texto), **I6** |
| **R1-5** ponte empírica | "quantitative bridge"; $D_f$ e $\gamma$ saturam juntos em 512 | "associação empírica, não causal" (`:336`), números do recozido | não existe $\gamma(D_f)$; assinatura comum em $T_s\approx128$; confundimento de $N$ desfeito | texto de `:336` e conclusão; carta R1-5; decidir teste por fibrila | **N12** |
| **R1-6** 18:1 | ausente | `:347` | — | nada | N6 ✔ |
| **R1-7** Eq. (5) | $\alpha,\beta$ qualitativos | interpretação em vocabulário recozido (`:293-309`) | $F_{rup}$ ~10× maior no quenched; forma de $\varphi(F)$ não refeita | refit no cluster; então Eq. (5), Fig. 8, carta R1-7 | **N9** |
| **R2-1** protocolo | varreduras + $\Delta F$ | **ainda varreduras** (`:240-242`); carta defende | protocolo trocado em 2026-08-24; objeção sem objeto | Eq. (4) como limiar $X_i \sim x^m$, $F^*_i$, cascata; Fig. 6; **carta R2-1 inteira** | **N2** |
| **R2-2** LLS vs ELS | crossover LLS→GLS | dois canais, nenhuma classe (`:230`) | idem, sob quenched | só vocabulário, junto com N2 | N3 ✔ |
| **R2-3** definição de avalanche | aglomerado conexo por passo de força | por passo de força, via varreduras (`:312`) | cascata determinística a $F$ fixo, inclusive os que perdem caminho de carga | frase de `:312`; carta R2-3 | N8 ∅, **N2** |
| **R2-4** cautela com SOC | SOC | removido; carta diz "cauda com corte exponencial" | três invariâncias medidas | últimas frases da carta R2-4, junto com N10 | N4 ✔ |

## O que decorre

**Ordem.** N2 passa à frente de N10/N11: as definições de limiar, cascata e
avalanche são o vocabulário de tudo o que vem depois (`:230`, `:312`, Eq. (6),
carta R2-1/R2-3/R1-2). Escrever N10 antes obrigaria a reescrevê-lo. N7 (Fig. 3,
Fig. 7, I6) não depende de N2 e pode correr em paralelo. N12 depende de N10/N11
e de N7. N9 espera o cluster. N13 e N14 por último, como sempre.

**A carta precisa de mais do que retoque.** Sete das onze respostas mudam de
conteúdo: R1-2 (metade estatística), R1-3, R1-4, R1-5, R1-7, R2-1, R2-3 —
mais as frases finais de R2-4. Só R1-1, R1-6 e R2-2 ficam.

**Sobre N12 e o teste por fibrila.** A campanha tem 200 fibrilas por condição
com arquivos de avalanche por fibrila, mas eles estão em `$DLA_PROJECT` no
SDumont2 e não há cópia local. O teste que a issue #8 pede — se o descritor
estrutural de **cada** fibrila prevê a forma da **sua** distribuição de
avalanches, dentro de uma condição — depende do cluster tanto quanto N9.
Registrar isso corrige a linha "análise local" do estado.

**Sobre I6.** O 0,997 do manuscrito e da carta entrou no commit `521a284` sem
script que o produza; o CSV de `Reviews/N7_fractal_proxy/proxy_correlations.csv`
é o reprodutível, e carrega um artefato: $\rho = 1{,}0000$ com $p \approx
6{,}6\times10^{-64}$, impossível para $n=10$ (o menor $p$ por permutação é
$5{,}5\times10^{-7}$; é a aproximação-$t$ do `spearmanr` degenerando). Se a
leitura de *crossover* dispensar a tabela de Spearman, I6 fecha por remoção; se
alguma correlação ficar, usa-se o CSV com $p$ por permutação.

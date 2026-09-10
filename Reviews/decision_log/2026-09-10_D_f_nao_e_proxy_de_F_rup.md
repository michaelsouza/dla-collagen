# $D_f$ não serve de proxy para $F_{rup}$: teste dentro de $T_s$ nos 20 cilindros fraturados

**Data:** 2026-09-10 (noite)
**Afeta:** N12 (confirma o fechamento: associação empírica, não proxy); R1-5
**Dados:** `Reviews/N18_df_ten_ts/trunk_predictors_{by_seed,correlations}.csv`; README §4
**Cita:** `Reviews/decision_log/2026-09-10_N18_quarenta_sementes_em_ts_16.md`

> Entrada de registro. **Append-only** — não editar.

## Pergunta

Michael: "analisar a relação entre $D_f$ e os termos calculados na ruptura,
para tentar justificar o uso de $D_f$ como proxy das propriedades mecânicas".

## O que se mediu antes de opinar

1. Através dos dez $T_s$, $D_f$ e $F_{rup}$ dão Spearman 0,88–0,95 — mas $\bar R$
   da seção dá −0,88 e qualquer monótona de $T_s$ passa. Um só botão.
2. Contraexemplo dentro da grade: de $T_s = 2$ a 32, $D_f$ (correlação) vai de
   1,703 a 1,684 enquanto $F_{rup}$ vai ×5,5 e $F_{rup}/N$ ×2.
3. Dentro de $T_s$ (5 sementes × 4 $T_s$ × 2 recortes), $D_f$ da semente
   contra $F_{rup}/R$ da mesma semente: Pearson dos z agrupados +0,26 / +0,13
   (correlação), +0,04 / +0,01 (giração). Nada.
4. Candidatas na escala do bastão (coordenação, ocupação de camada, $F^*$ do
   modelo): a melhor, coordenação média, dá +0,51 ($p = 0{,}02$) em 17×17 e
   +0,09 em 41×41. Com 32 testes, é acaso.

## Decisão

$D_f$ **não** entra no manuscrito como proxy de propriedade mecânica. A frase
de N12 ("associação empírica") fica como está. Se um dia houver proxy, ele
terá de mostrar sinal dentro de $T_s$ em mais sementes do que estas cinco; a
infraestrutura (script e `.db`) está pronta para isso.

## Fatos laterais registrados

- $F^*$ do modelo ($m = 2$) supera $F_{rup}/R$ por 2,2–2,8, quase constante.
- No tronco DLA ($T_s = 2$) 19% (17×17) e 37% (41×41) dos bastões nunca rompem;
  em $T_s \ge 32$, menos de 2%. A força "por bastão" no regime aberto conta
  bastões que não portam carga.

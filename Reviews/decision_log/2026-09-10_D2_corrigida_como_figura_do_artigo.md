# A dimensão de correlação corrigida contra $T_s$ vai para o artigo

**Data:** 2026-09-10 (noite)
**Afeta:** N7 (reabre em parte: uma figura nova de $D_f$ entra no manuscrito), a regra de intervenção mínima de 2026-09-03
**Dados:** `Reviews/N18_df_ten_ts/xmgrace/df_corr_vs_ts.{agr,pdf}`, `df_corr_vs_ts_xydy.dat` (renomeados de `d2_corrected_vs_ts.*` em 2026-09-10 à noite, quando a curva passou a ser a bruta; ver registro `2026-09-10_N18_dez_sementes_extras_em_cinco_ts.md`)
**Cita:** `Reviews/decision_log/2026-09-10_N18_peso_do_ajuste_e_dimensao_de_correlacao.md`

> Entrada de registro. **Append-only** — não editar.

## Decisão de Michael

Das figuras de $D_f$ do N18, **só uma** vai para o artigo: $D_2$ corrigida contra
$T_s$ (a curva vermelha de `figures/corr_df_vs_ts.png`), uma série só, em azul,
rótulos em en-US. Nem a giração nem o massa–raio entram como figura.

## Por que esta e não a giração

- $D_2$ não depende de centro nem da ordem de adesão: é a geometria da seção
  final, que é o que a mecânica sente. A giração mede a história do crescimento.
- Tem um controle de borda explícito (disco uniforme de mesmo $n$ e $\bar R$),
  então a correção é declarada, não escondida numa janela.
- É o estimador mais reprodutível entre cilindros (erro-padrão 0,002–0,007).
- Limitação a declarar no texto: uma década ($4 \le r \le \bar R/3$), abaixo da
  regra de duas; e no regime compacto dá 1,92, não 2, porque pesa a periferia
  DLA junto com o miolo. O artigo deve chamar de "correlation dimension of the
  cross-section" e não afirmar lei de potência além do que a janela cobre.

## O que ainda não foi decidido

Onde a figura entra no manuscrito (qual figura substitui ou a que painel se
junta) e o texto que a acompanha. Isso muda `paper_PRE.tex` e a carta, e fica
para uma entrada própria quando Michael decidir.

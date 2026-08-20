# Modelo com corte estendido ajustado separadamente em cada $T_s$

**Manuscrito:** ER12738, *Scaling behaviors in simulated collagen fibrils*  
**Spec de revisão:** GitHub issue #1  
**Ticket estatístico:** GitHub issue #5  
**Condições:** $T_s=2,8,16,32,64,128,512,1024,4096,8192$

## 1. Resultado principal

Para cada $T_s$, o início da cauda e os três parâmetros foram estimados
separadamente no modelo discreto

$$
p(s\mid s\geq s_{min})=
\frac{s^{-\alpha}\exp[-(s/s_c)^\beta]}
{\sum_{k=s_{min}}^\infty k^{-\alpha}\exp[-(k/s_c)^\beta]}.
$$

Não há parâmetros compartilhados nem ajuste conjunto. O corte estendido não é
rejeitado em nenhuma das dez condições pelo teste por blocos de fibrilas, com
$p_{bloco}=0{,}242$--$0{,}915$. Contudo, ele não é o modelo mínimo em todos os
casos: formas mais simples também descrevem as caudas selecionadas em
$T_s=2,8,16$ e 64.

## 2. Método

Os ajustes usam tamanhos inteiros e não agrupados de avalanches locais
pré-terminais. Em cada $T_s$, $s_{min}$ minimiza o KS do próprio corte
estendido entre os candidatos com pelo menos 1.000 eventos. A incerteza e os
testes absolutos usam 999 réplicas de fibrilas inteiras, mantendo o suporte
selecionado fixo. Portanto, os intervalos de 95% são condicionais a esse
$s_{min}$. Trata-se da metodologia de Clauset adaptada à dependência entre
eventos de uma mesma fibrila, e não do bootstrap iid literal do artigo.

## 3. Ajustes individuais

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

*Figura 1 — CCDF empírica e corte estendido acima do suporte selecionado em
cada $T_s$.*

## 4. Parâmetros em função de $T_s$

![Parâmetro alpha em função de Ts.](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/ts_vs_alpha.png)

*Figura 2 — $\alpha$ e IC 95% por fibrilas.*

![Parâmetro beta em função de Ts.](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/ts_vs_beta.png)

*Figura 3 — $\beta$ e IC 95% por fibrilas.*

![Escala de corte em função de Ts.](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/ts_vs_sc.png)

*Figura 4 — $s_c$ e IC 95% por fibrilas.*

Para $T_s\geq128$, $\alpha$ fica próximo de 2,5 e $s_c$ entre 211 e 273, mas
os suportes diferentes impedem interpretar essa semelhança como um teste de
igualdade. Além disso, os parâmetros são pouco identificados em $T_s=2$ e 8,
onde $s_c=s_{min}$, enquanto parte das réplicas de $T_s=8$ e 512 atinge o
limite $\beta=5$.

## 5. Modelos mais simples no mesmo suporte

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

*Figura 5 — $p$-valores por fibrilas; a linha tracejada marca $p=0{,}10$.*

O corte estendido é a única família não rejeitada em todas as caudas
selecionadas. Condição por condição, porém, o corte simples ou a lognormal
bastam em $T_s=2$, a potência pura passa em $T_s=8$, e o corte simples basta
em $T_s=16$ e 64. Em $T_s=8$, a cauda cobre somente 0,86 década e 0,071% dos
eventos, de modo que a não rejeição da potência pura não sustenta uma
conclusão de comportamento livre de escala.

## 6. Conclusão e reprodução

O corte estendido fornece uma descrição empírica uniforme quando cada $T_s$ é
ajustado separadamente, mas não estabelece parâmetros universais, criticalidade
auto-organizada ou uma classe de compartilhamento de carga. A conclusão sobre
parcimônia é condicionada aos suportes escolhidos pelo próprio corte estendido.

```bash
.venv/bin/python Code/Data_analysis/run_stretched_cutoff_individual.py \
  --replicates 999 --workers 6 \
  --output /tmp/stretched_cutoff_individual_all_ts
```

- [ajustes e testes](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/model_fits.csv);
- [varreduras de $s_{min}$](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/xmin_scan.csv);
- [réplicas por blocos](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/block_bootstrap.csv);
- [comparações relativas](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/model_comparisons.csv);
- [metadados](../Data_avalanches_all_fibrils/reproduction/stretched_cutoff_individual_all_ts/analysis.json).


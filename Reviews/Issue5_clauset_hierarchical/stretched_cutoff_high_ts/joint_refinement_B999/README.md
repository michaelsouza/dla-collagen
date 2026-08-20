# High-Ts stretched-cutoff analysis

The exploratory candidate is the exact discrete model $p(s)\propto s^{-\alpha}\exp[-(s/s_c)^\beta]$ on the fixed common support $s\geq8$.

| Ts | alpha | beta | scale | KS | individual block p | decision |
|---:|---:|---:|---:|---:|---:|:---|
| 512 | 2.6741 | 4.0055 | 272.90 | 0.00192 | 1.000 | not rejected |
| 1024 | 2.6491 | 3.1660 | 241.72 | 0.00503 | 1.000 | not rejected |
| 4096 | 2.6488 | 3.2545 | 238.16 | 0.00329 | 1.000 | not rejected |
| 8192 | 2.6445 | 3.6794 | 277.19 | 0.01126 | 0.500 | not rejected |

The joint common-shape fit gives alpha=2.6543, beta=3.4401, and joint block p=0.381. 
The family is considered a common high-Ts description only if the joint test and every condition-specific absolute-fit test exceed 0.10.

Because this family was proposed after inspecting the observed curvature, the analysis is exploratory even if a goodness-of-fit test does not reject it.

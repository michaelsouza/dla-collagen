# High-Ts stretched-cutoff analysis

The exploratory candidate is the exact discrete model $p(s)\propto s^{-\alpha}\exp[-(s/s_c)^\beta]$ on the fixed common support $s\geq29$.

| Ts | alpha | beta | scale | KS | individual block p | decision |
|---:|---:|---:|---:|---:|---:|:---|
| 512 | 2.5913 | 3.2343 | 256.13 | 0.00445 | 0.645 | not rejected |
| 1024 | 2.5065 | 2.4283 | 211.87 | 0.00645 | 0.205 | not rejected |
| 4096 | 2.5590 | 2.4650 | 215.31 | 0.00411 | 0.655 | not rejected |
| 8192 | 2.4839 | 2.3585 | 231.81 | 0.00378 | 0.810 | not rejected |

The joint common-shape fit gives alpha=2.5341, beta=2.5472, and joint block p=0.981. 
The family is considered a common high-Ts description only if the joint test and every condition-specific absolute-fit test exceed 0.10.

Because this family was proposed after inspecting the observed curvature, the analysis is exploratory even if a goodness-of-fit test does not reject it.

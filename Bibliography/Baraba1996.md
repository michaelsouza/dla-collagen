VOLUME 76, NUMBER 12

PHYSICAL REVIEW LETTERS

18 MARCH 1996

# Avalanches in the Lung: A Statistical Mechanical Model

Albert-László Barabási, $^{1,2}$  Sergey V. Buldyrev, $^{1}$  H. Eugene Stanley, $^{1}$  and Béla Suki $^{3}$

$^{1}$ Center for Polymer Studies and Department of Physics, Boston University, Boston, Massachusetts 02215

$^{2}$ Department of Physics, University of Notre Dame, Notre Dame, Indiana 46556

$^{3}$ Respiratory Research Laboratory, Department of Biomedical Engineering, Boston University, Boston, Massachusetts 02215

(Received 10 March 1995)

We study a statistical mechanical model for the dynamics of lung inflation which incorporates recent experimental observations on the opening of individual airways by a cascade or avalanche mechanism. Using an exact mapping of the avalanche problem onto percolation on a Cayley tree, we analytically derive the exponents describing the size distribution of the first avalanches and test the analytical solution by numerical simulations. We find that the treelike structure of the airways, together with the simplest assumptions concerning opening threshold pressures of each airway, is sufficient to explain the existence of power-law distributions observed experimentally.

PACS numbers: 87.45.Bp, 05.40.+j, 05.45.+b

Recent interactions between physics and physiology have resulted in advances in understanding some "simpler" physiological systems [1]. In particular, considerable progress has occurred in the general area of statistical mechanics and pulmonary physiology [2,3] due most likely to the unique treelike connectivity of the airways [4].

During a forced exhalation, lungs deflate to very low volumes, and many peripheral airways close up [5]. In lung disease, closure occurs even during normal breathing; the closed airways do not reopen for a significant portion of the following inhalation [6]. As a consequence, a large portion of the alveolar space can remain closed during the entire breathing cycle leading to severe hypoventilation and an imbalance between ventilation and perfusion. The process of opening a single airway is a local and isolated phenomenon. However, the dynamics of consecutive airway openings in the lung is a highly cooperative process. There is recent evidence suggesting that during inflation the resistance to airflow of the small airways decreases in discrete jumps [7,8]. Thus airways do not open individually, but in a sequence of bursts or "avalanches" [9] involving many airways; both the size of these jumps and the time intervals between jumps follow power-law distributions [8]. In this paper, we argue that the existence of power laws in lung inflation can arise directly from the treelike connectivity of the airways. We observe that the dynamics of lung inflation can be usefully described by a percolation problem on a Cayley tree, with the inflated lung volume corresponding to a percolation cluster. Using this exact mapping, we analytically derive the exponents describing the size distribution of the first avalanches, and test our results using simulations.

Morphological data [4] show that human (as well as other mammalian) lungs constitute an asymmetric branching airway structure with  $\approx 35$  generations. Complete airway closure appears to occur only in the last  $\approx 10 - 14$  generations [8], where the branching structure is largely symmetric [4]. Accordingly, we model this part of the airway tree as a binary Cayley tree with airway segments

that can be either closed or opened (Fig. 1). At time  $t = 0$ , all airways are assumed to be closed. Lung inflation is simulated by applying an external pressure  $P_{E}$  at the root of the tree, and gradually increasing  $P_{E}$  at a uniform and slow rate. Airways are labeled  $(i,j)$  with a generation number  $i$  ( $i = 0,\dots,N$ ), where  $N$  is the order of the tree ( $i = 0$  denotes the tree root), and a column number  $j$  ( $j = 0,\dots,2^{i} - 1$ ). An opening threshold pressure  $P_{ij}$  is also assigned to each airway  $(i,j)$ . Experiments on flexible tube airway models [10] confirm that the opening of a single airway is a dynamic process, with each airway characterized by a critical pressure threshold such that if  $P_{E}$  exceeds this threshold, then the airway opens in a short time, which is considered to be instantaneous [11]. Opening of airway  $(i,j)$  occurs whenever  $P_{ij}$  is smaller than the pressure in its parent.

![img-0.jpeg](img-0.jpeg)
FIG. 1. Schematic diagram of the airways represented by a branching tree. The airways are labeled by a generation number  $(i = 0, \dots, N)$  and a column number  $(j = 0, \dots, 2^i - 1)$ . An opening threshold pressure  $0 &lt; P_{ij} &lt; 1$  chosen from a uniform distribution is also assigned to each airway.

0031-9007/96/76(12)/2192(4)$10.00

© 1996 The American Physical Society

---

VOLUME 76, NUMBER 12
PHYSICAL REVIEW LETTERS
18 MARCH 1996

We assume that $P_{ij}$ is uniformly distributed between 0 and 1 [12], and allow $P_{\mathrm{E}}$ to increase from 0 to 1 in small increments. When $P_{\mathrm{E}}$ first exceeds $P_{00}$, the airway (0,0) opens and its pressure is set equal to $P_{\mathrm{E}}$. Next, the two airways (1,0) and (1,1) are tested to see if they can be opened with this value of $P_{\mathrm{E}}$—i.e., if $P_{\mathrm{E}} &gt; P_{10}$ and/or $P_{E} &gt; P_{11}$. If one or both conditions are met, then the airways (1,0) and/or (1,1) are also opened. This opening is then continued sequentially down the tree until no airway is found with its $P_{ij} &lt; P_{\mathrm{E}}$.

Of particular interest is the fact that a small increase in $P_{E}$ can lead to an "avalanche" in which many airways open simultaneously. When the first avalanche stops, $P_{E}$ is further incremented and pressures in the open airways are updated. We iterate this process until all airways open. The location and size of the next avalanche depends on the distribution of $P_{ij}$ in the accessible region.

We do not treat the full problem analytically, but we can obtain exact results for the distribution of the first avalanche. At $t = 0$, we increase $P_{E}$ until the first avalanche occurs and we calculate its size $s$. Then we restart the simulation with a new set of thresholds $\{P_{ij}\}$.

Before we consider two possible definitions of $s$, we note that gas exchange in the lung occurs only in the "opened" alveoli (the terminal units of the bronchial tree) which are in communication with the trachea. For this reason, in definition A, $s$ denotes the number of alveoli, defined as the number of elements in the last generation, $N$, that become open. Motivated by percolation theory [13,14], in definition B, $s$ is the number of airways that open following an increase of $P_{E}$ that opens at least one airway. The physiological rationale for definition B is that when the lung is deflated to low volumes, most airways close. However, often there remains trapped air in the alveoli. Thus, concerning gas exchange, it may not be necessary that an avalanche reach the bottom of the tree for it to connect alveoli with the trachea.

We study $\Pi(s)$, the size distribution of first avalanches. For definition A, $\Pi^A(s)$ shows a single power law behavior with an exponent $\gamma^A = 0.9$ ($\approx 1.0$) (Fig. 2). For definition B the function $\Pi^B(s)$ has two regions (Fig. 2): a first region with a steep power-law decay and a second region with a moderate power-law decay, with a crossover at a scale $N$,

$$
\Pi^ {B} (s) \sim \left\{ \begin{array}{l l} s ^ {- \gamma_ {1} ^ {B}} &amp; [ s \leq N ] \\ s ^ {- \gamma_ {2} ^ {B}} &amp; [ s \gg N ] \end{array} . \right. \tag {1}
$$

The exponent $\gamma_1^B = 1.9$ ($\approx 2.0$) for the first regime, while $\gamma_2^B = 0.9$ ($\approx 1.0$) for the second regime which extends to sizes including all branches, i.e., almost to a size of $2^{N + 1} - 1$.

We argue that for definition B, this problem can be mapped onto the percolation problem for the Cayley tree [14]. In the percolation problem, we occupy randomly every branch of the tree with a probability $p$. Then, starting from the root, we connect all occupied branches

![img-1.jpeg](img-1.jpeg)
FIG. 2. Double logarithmic plot of the avalanche size distributions $\Pi(s)$ obtained by computer simulation on a Cayley tree of 12 generations. Shown are data obtained for $10^{8}$ realizations for each of the two avalanche size definitions discussed in the text, definition A (closed circles) and definition B (open circles). Also shown, for comparison, are the exact results obtained using the generating function approach described in the text. Again, both definitions are shown: definition A (solid line) and definition B (dotted line).

that are neighbors of each other. Definition B concerns the cluster of connected bonds that starts from the root. The size of this cluster depends on the fraction $p$ of occupied bonds. As we approach a critical probability $p_c$, the typical size of a cluster can be characterized by the $s_{\mathrm{typ}} \sim |p - p_c|^{-1 / \sigma}$. Both $\sigma$ and $p_c$ can be calculated exactly due to the branching nature of the tree: $\sigma = \frac{1}{2}$ and $p_c = \frac{1}{2}$ [14]. In general, the size distribution of the finite clusters in the infinite system obeys the scaling form [14]

$$
\Pi (s) = s ^ {- \tau} f \left(s ^ {\sigma} | p - p _ {c} |\right), \tag {2}
$$

where $\tau = 3 / 2$, and $f(u) = \text{const}$ for $u \ll 1$ and $f(u \gg 1) \rightarrow 0$. To connect percolation theory to the lung model, instead of occupying the branches randomly with probability $p$, we assign a random number or pressure threshold value to each airway. We then define a cluster to be the set of airways that have a threshold smaller than a predefined value $p$ and are connected to the root. When $P_{E}$ exceeds $P_{00}$, we open all airways below the root which have a threshold value smaller than $P_{00}$.

If $P_{00}$ is fixed and set equal to $p$, then this is exactly the percolation problem on the Cayley tree, and the distribution of the cluster sizes or avalanches is given by (2). However, in our case, $P_{00}$ is also a random variable. Thus, in order to obtain the size distribution of the first avalanche, we must integrate the cluster distribution over the probability $p$ from 0 to 1 with the result that

$$
\gamma_ {1} ^ {B} = \tau + \sigma , \tag {3}
$$

which predicts $\gamma_1^B = 2$, in agreement with the scaling observed for $s \leq N$ in Fig. 2.

2193

---

VOLUME 76, NUMBER 12
PHYSICAL REVIEW LETTERS
18 MARCH 1996

These calculations assume that the system size is infinite. No avalanche with $s &lt; N$ can reach the bottom of the tree, so the scaling behavior for $s &lt; N$ is that of the infinite tree with an exponent $\gamma_1^B = 2$. On the other hand, avalanches of size $s &gt; N$ are affected by finite-size effects, and indeed the data for $s \gg N$ indicate a different exponent. Moreover, finite-size effects will always affect the scaling behavior of $\Pi^A(s)$, since every avalanche that leads to the opening of one or more alveoli must open at least $N$ airways.

We next calculate the effect of finite $N$ on the cluster size distribution. Following the general theory of branching processes [15], we consider the generating function of order $N$

$$
g _ {N} ^ {A, B} (p, x) \equiv \sum_ {s = 0} ^ {\infty} P _ {N} ^ {A, B} (p, s) x ^ {s}, \tag {4}
$$

where $P_N^{A,B}(p,s)$ give, for definitions A and B, the probability that in a tree with $N$ generations we have an avalanche of size $s$ for a given $P_{00} = p$. Therefore,

$$
\Pi_ {N} ^ {A, B} (s) = \int_ {0} ^ {1} P _ {N} ^ {A, B} (p, s) d p. \tag {5}
$$

These generating functions satisfy the recursion relations

$$
\begin{array}{l} g _ {N + 1} ^ {A, B} (p, x) = x ^ {\theta} \left[ (1 - p) + p g _ {N} ^ {A, B} (p, x) \right] ^ {2}, \\ g _ {0} ^ {A, B} (p, x) = x, \tag {6} \\ \end{array}
$$

where $\theta = 0$ for definition A and $\theta = 1$ for definition B, $g_N^A$ is a polynomial in $x$ of degree $2^{N}$, and $g_N^B$ is a polynomial of degree $2^{N + 1} - 1$. We obtain the distribution functions $\Pi^A (s)$ and $\Pi^B (s)$ by numerical integration of the coefficients of these polynomials with respect to $p = P_{00}$. The results for $\Pi^A (s)$ and $\Pi^B (s)$ are shown in Fig. 2; note the good agreement between simulations and theory, despite the fact that there are no adjustable parameters in the calculation (the theoretical line being determined solely by the value of $N$).

For $N \to \infty$, for any $x &lt; 1$, the generating function $g_N^B(p, x)$ approaches the limit $g_\infty^B(p, x) \equiv [1 - 2p(1 - p)x - \sqrt{1 - 4p(1 - p)x}] / 2p^2x$, which can be expanded in powers of $x$. On integrating the coefficients of this expansion with respect to $p$, we obtain $\Pi^B(s) = 1 / s(2s + 1)$ for $s \leq N$, which implies an asymptotic exponent $\gamma_1^B = 2$.

Next we consider definition A, and show that $\Pi^A(s) \sim 1 / s$ for large $s$, so that $\gamma^A = 1$. For large $N$ and large $s$, it follows from general theorems [15] that for $p &gt; 1 / 2$,

$$
\begin{array}{l} P _ {N} ^ {A} (p, s) \sim s _ {0} ^ {- 1} \exp \left[ - C \left(s / s _ {0}\right) ^ {\gamma (p)} \right], \\ s _ {0} = (2 p) ^ {N}. \tag {7} \\ \end{array}
$$

Here $s_0$ is the average avalanche size (number of open alveoli) in the generation $N$, $\gamma(p)$ is a continuous function of $p$ for $p &lt; 1$, and $C$ is a positive number with a weak dependence on $s / s_0$. For $p \leq \frac{1}{2}$, $s_0$ decays exponentially with $N$. Thus, for $p \leq \frac{1}{2}$, the coefficients $P_N^A(p, s)$ for

large $s$ become negligibly small and do not contribute to the integral (5). In contrast, for $p &gt; \frac{1}{2}$ the probability of a nonzero avalanche in definition A—which is equal to the sum of all the $P_N^A(p,s)$ with $s \geq 1$—is finite when $N \to \infty$ and equal to $(2p - 1)/p^2$. This quantity should be used as a normalizing constant in the equation (7). Integrating equation (7) with respect to $p$ from $\frac{1}{2}$ to 1 with the help of the saddle point approximation, we find

$$
\begin{array}{l} \Pi^ {A} (s) \sim \frac {1}{s N} \left(1 - s ^ {- 1 / N}\right), \\ N \ll s \ll 2 ^ {N}, \tag {8} \\ \end{array}
$$

so $\gamma^A = 1$. If we expand Eq. (8) for small $s$, we find $\Pi^A(s) \sim \ln s / (sN^2)$; hence we expect to find an effective exponent that is smaller than the asymptotic value $\gamma_2^A = 1$, and indeed our simulations give $\gamma^A = 0.9$ (Fig. 2). For very large $s$, comparable with $2^N$, the saddle point approximation is no longer valid, and we observe (Fig. 2) the "kink" near the end of the distribution [16]; Eq. (8) also holds for definition B, so $\gamma_2^B = 1$. Note that Eq. (8) is valid for trees with any coordination number.

Having derived the above exponents analytically, we next examine their "universality" by discussing how deviations from the assumptions made in the model may affect the scaling exponents. (i) The first assumption (which matters only for definition B) is that we neglect the fact that in the lung the length $\ell$ and the radius $r$, and hence the volume of the airways, depend on the generation number $i$ [4]. Previously, we modeled this generational dependence such that $\ell_{i+1} = \ell_i / 0.9$ and $r_{i+1} = r_i / 0.86$ [8], where the scaling factors (0.9 and 0.86) arise from morphological data [4]. This exponential dependence should not affect the scaling behavior, an expectation we verified by simulations. (ii) The second assumption, that the distribution of $P_{ij}$ is uniform, matters for both definitions. Unfortunately, direct experimental data on the distribution of $P_{ij}$ in the lung are not available. However, even if the distribution is not uniform, but normal or exponential, the scaling exponents will not be influenced as long as the values of $P_{ij}$ are not correlated. Correlations among $P_{ij}$ have not been reported. (iii) While the assumption of a uniform distribution is physiologically reasonable, it is also possible that there is a weak generational dependence of $P_{ij}$ [12] which can reduce the scaling region and/or change the value of the exponents. A stronger generational dependence of $P_{ij}$ in which the mean of $P_{ij}$ as a function of $i$ increases from the root to the bottom by at least a factor of 10 will, however, break down the scaling behavior [17]. As a consequence, the very existence of scaling exponents found in experimental data [8] provides indirect evidence that the distribution of $P_{ij}$ does not have any significant generational dependence.

In summary, we have studied a statistical mechanical model of the distribution of the first avalanches during lung inflation. Our main result is an analytically soluble model which, compared to the more realistic model

---

VOLUME 76, NUMBER 12
PHYSICAL REVIEW LETTERS
18 MARCH 1996

of Ref. [8], permits exact calculation of the scaling exponents with the avalanche size defined either as the number of alveoli (definition A) or number of opened airways (definition B). We have found that the treelike structure of the airways with the simplest assumptions concerning opening threshold pressures is sufficient to explain the existence of power-law distributions observed experimentally [8]. Finally, the fact that the size distribution of the first avalanches follows a power law suggests that in disease high pressures for at least short periods of inspiration might be necessary to open up larger alveolar volumes. Thus, our results may also find important applications in the design of appropriate wave forms for artificial ventilation of patients who suffer from substantial airway closure and alveolar collapse.

We thank P. Ch. Ivanov, R. Sadr, A. Shehter, K. Sneppen, and especially M. Wortis for very helpful comments, and NSF Grant No. BES-9503008 and OTKA 2675 for financial support.

[1] J.B. Bassingthwaight, L.S. Liebovitch, and B.J. West, Fractal Physiology (Oxford University Press, New York, 1994); Fractals in Natural Sciences, edited by T. Vicsek, M. Shlesinger, and M. Matsushita (World Scientific, Singapore, 1994); B.J. West and W. Deering, Phys. Rep. 246, 1 (1994); Growth Patterns in Physical Sciences and Biology, J.M. Garcia-Ruiz et al. (Plenum, New York, 1993); B.J. West, Fractal Physiology and Chaos in Medicine (World Scientific, Singapore, 1990).
[2] M.F. Shlesinger and B.J. West, Phys. Rev. Lett. 67, 2106 (1991).
[3] B.J. West and M.F. Shlesinger, Int. J. Mod. Phys. B 3, 795 (1989).
[4] K.G. Horsfield, G. Dart, D.E. Olson, and G. Cumming, J. Appl. Phys. 31, 207-217 (1971).
[5] L. A. Engel, A. Grassino, and N. R. Anthonisen, J. Appl. Phys. 38, 1117 (1975).
[6] A.B.H. Crawford, D.J. Cotton, M. Paiva, and L.A. Engel, J. Appl. Phys. 66, 2511 (1989).
[7] F. Peták, Z. Hantos, A. Adamicza, D.R. Otis, and B. Daróczy, Eur. Respir. J. 6, 403S (1993); D.R. Otis, Ph.D. thesis, MIT, 1994.
[8] B. Suki, A.-L. Barabási, Z. Hantos, F. Peták, and H.E. Stanley, Nature (London) 368, 615 (1994).
[9] Note that although we use the term "avalanche," our avalanches are different from those observed in self-organized criticality (SOC); for a review, see G. Grinstein, in Scale Invariance, Interfaces, and Non-Equilibrium Dynamics, edited by A.J. McKane, M. Droz, J. Vannimenus, and D. Wolf (Plenum, New York, 1995). The most important difference is in the actual mechanisms that lead to the avalanches: Here we show that the avalanches in the lung are related to the distribution of percolation clusters on a Cayley tree.
[10] D.P. Gaver, R.W. Samsel, and J. Solway, J. Appl. Phys. 69, 74 (1990).
[11] The time required to open an airway is well under 0.05 s for the smaller airways [10]. Since the inflation time in the experiments was 80 s [7], the process of opening an airway can be considered to be instantaneous.
[12] A recent study of physical tube models [10] finds that viscous and surface tension forces increase with decreasing radius, so there may exist a generational dependence of $P_{ij}$ on airway radius $r_i$. It was predicted [10] that $P_{ij}$ is inversely proportional to $r_i$. There are many additional factors that can balance this generational dependence, such as local variations in $r$, length, surface tension, airway wall thickness, local elastic moduli, smooth muscle tone, etc. Additionally, there are two important systematic factors that compensate this generational dependence. First, the airway wall volumetric elastic modulus is inversely proportional to the cube of $r$ [B. Suki et al., J. Appl. Phys. 75, 2755 (1993)]. Thus, airway wall modulus increases rapidly with decreasing diameter. Since the $P_{ij}$ is smaller in stiffer tubes, this mechanism alone may balance the generational dependence of $P_{ij}$. Second, it was found that at any given generation $i$ the distribution of $r_i$ is not normal, but it has a longer tail toward the larger radii [H. Kitaoka and B. Suki (unpublished)]. The fact that this tail increases with increasing $i$ will again reduce the effect of the inverse dependence of $P_{ij}$ on $r_i$.
[13] J. Essam, Rep. Prog. Phys. 43, 833 (1980).
[14] A. Bunde and S. Havlin, in Fractals and Disordered Systems, edited by A. Bunde and S. Havlin (Springer-Verlag, Berlin, 1996), 2nd ed..
[15] T. E. Harris, The Theory of Branching Processes (Dover Publication Inc., New York, 1989); S. Asmussen and H. Hering, Branching Processes (Birkhäuser, Boston, 1983); N. H. Bingham, J. Appl. Prob. 25A, 215 (1988).
[16] For very small $s \ll N$ approximation (7) is also incorrect. For example, one can show that $\Pi^A(1) \sim 1/N^3$.
[17] If $r_{i+1} = r_i / 0.86$ as in Ref. [8], then in a 14-generation tree, $P_{ij}$ will increase by no more than a factor of 10. Since it was suggested that $P_{ij} \sim 1 / r_i$ [10], we modeled the generational dependence of $P_{ij}$ so that the mean of $P_{ij}$ depended on $i$ according to $P_{i+1,j} = P_{ij} / 0.86$. Simulations in a 12-generation tree showed that using definition A, the scaling completely breaks down, and with definition B, the scaling region is significantly reduced to about one decade.

2195
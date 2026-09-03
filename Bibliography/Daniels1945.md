# THE ROYAL SOCIETY PUBLISHING

The Statistical Theory of the Strength of Bundles of Threads. I

Author(s): H. E. Daniels

Source: Proceedings of the Royal Society of London. Series A, Mathematical and Physical Sciences, Jun. 18, 1945, Vol. 183, No. 995 (Jun. 18, 1945), pp. 405-435

Published by: Royal Society

Stable URL: https://www.jstor.org/stable/97823

JSTOR is a not-for-profit service that helps scholars, researchers, and students discover, use, and build upon a wide range of content in a trusted digital archive. We use information technology and tools to increase productivity and facilitate new forms of scholarship. For more information about JSTOR, please contact support@jstor.org.

Your use of the JSTOR archive indicates your acceptance of the Terms & Conditions of Use, available at https://about.jstor.org/terms

JSTOR

Royal Society is collaborating with JSTOR to digitize, preserve and extend access to Proceedings of the Royal Society of London. Series A, Mathematical and Physical Sciences

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

# The statistical theory of the strength of bundles of threads. I

BY H. E. DANIELS, PH.D., *Wool Industries Research Association*

*(Communicated by H. Jeffreys, F.R.S.—Received 31 May 1944)*

A group of parallel threads of equal length, clamped at each end so that all threads extend equally under tension, is called a bundle, and the maximum load which the bundle can support is called its strength. The object of the work is to study the probability distribution of the strength of bundles whose constituent threads are sampled randomly from an infinite population of threads in which the probability distribution of strength is known.

The relation between the strength of a bundle and the strengths of its constituent threads is first discussed, and results are stated for bundles so large that the proportions of threads of different strengths approach their expectations. The properties of the probability distribution of bundle strength are next developed in detail, attention being confined in the present paper to the case where all threads have the same load-extension curve up to breaking point. Finally, the asymptotic behaviour of the distribution for large numbers of threads is studied, and it is shown that in the commonest cases the distribution tends to assume the normal form.

## INTRODUCTION

1. Consider an infinite population of threads of equal length whose probability distribution of strength is known. A number of threads are sampled randomly from this population, laid side by side and clamped at each end to form what we term a *bundle*. When a free load is applied to the bundle all threads extend by an equal amount, and the minimum load beyond which all the threads of the bundle break is called its *strength*. The present work is an investigation into the probability distribution of the strength of such bundles.

The problem presents itself naturally in the theory of strength testing of textile materials. For example, a test widely used in practice for estimating the strength of yarns is known as the 'hank' test for wool yarns, and the 'lea' test for cotton yarns. The method employed is to reel a hank of yarn containing a stated number of turns of specified circumference and to apply the breaking load to the hank by stretching it between two hooks. The word 'bundle' has been used here in preference to 'hank' or 'lea', since there is usually a small amount of slip at the hooks which makes the conditions of this test indeterminate. The testing of cloth samples for warp and weft strength is another instance of a practical test in which the specimens approximate to bundles, though in closely woven fabrics the cross-threads afford a measure of support which introduces complications. Other examples outside the field of textile testing could no doubt also be quoted.

2. The subject was first considered, as far as the author is aware, by F. T. Peirce (1926), relevant experimental work being published in previous papers in the same series. He deals exhaustively with the underlying physical considerations and derives useful formulae for the strength of large bundles.

Vol. 183. A.

[ 405 ]

27

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

406

H. E. Daniels

The wider significance of the problem was also recognized by Peirce. He points out that a study of the strength properties of certain materials must involve considerations fundamentally similar to those arising in the theory of bundles (called by Peirce 'composite specimens'), since each element of the material may be thought of as made up of subelements arranged both in series and parallel along a particular direction of stress. Recently a notable attempt has been made by W. Weibull (1939) to evolve a statistical theory of strength of materials, in the course of which consideration is given to the behaviour under a free load of materials composed of independent parallel elements (the case of so-called 'incoherent irregularity')*.

The present paper opens with a preliminary section on the relation between the strength of a bundle and the strengths of its constituent threads, in which the work overlaps that of Peirce to some extent. The distribution which forms the main topic of the paper was not, however, discussed by Peirce. Apart from its practical application, it is of considerable inherent interest and appears hitherto to have received little attention from mathematicians.

# THE RELATION BETWEEN A BUNDLE AND ITS CONSTITUENT THREADS

3. It is assumed that for each thread there is a definite extension and load at which it breaks, so that threads which yield rather than snap are excluded from the discussion. Whatever assumptions are made about the elastic properties of the threads, the following sequence of events occurs when a given load is applied. Suppose the load is increased gradually from zero to its final value. At first it is distributed in some way between the $n$ threads, and equilibrium may be reached without any thread giving way. If the load is great enough, however, one of the threads breaks at some stage and the load is redistributed among the remaining $n-1$ threads, each bearing a somewhat larger share of the load than before and so being more likely to give way. Similarly, a number of threads may break successively until either a point is reached where the remaining threads have sufficient strength to maintain between them the final load, or no such point is reached and all the threads ultimately give way, in which case, of course, the bundle is broken.

To formulate the problem more precisely, it is necessary to know how the load distributes itself between the individual threads of the bundle, and this depends on the elastic properties of the threads. It should be observed that if they are assumed to be inextensible the problem has no definite solution. A familiar example of the same state of affairs is that of a rigid beam supported horizontally at more than two points, in which case the pressures on the supports cannot be deduced.

* Unfortunately there appears to be a flaw in his discussion of probabilities, and formulae are obtained which are open to question. I suggest that his equations (136) and (137) should read

$$dS'_{2/2} = 2[S(2\sigma) - S(\sigma)] dS(\sigma)$$

and $$dS''_{2/2} = 2S(\sigma) dS(2\sigma)$$

respectively. The final expression for $S_{2/2} = S'_{2/2} + S''_{2/2}$ then agrees with the present formula (9.1) for $n = 2$.

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

The statistical theory of the strength of bundles of threads

407

Denoting load by S and extension by ε, the load-extension relation for a given thread can be written

$$S = f(\epsilon, \alpha),$$

where α represents, for simplicity, one parameter defining the curve specific to a particular thread. The value of α is in the general case correlated with the breaking extension ε, or the breaking load σ = f(ε, α).

### Large bundles

4. It is convenient first to consider very large bundles within which the actual numbers of threads with given properties can be treated as equal to their expectations. (See, however, the remark at the end of § 7.)

The probability of ε and α lying in specified small intervals is denoted by

$$\phi(\epsilon, \alpha) d\alpha d\epsilon \tag{4·1}$$

and the probability density for ε for each thread is

$$\psi(\epsilon) = \int_{0}^{\infty} \phi(\epsilon, \alpha) d\alpha. \tag{4·2}$$

Let a load S be applied to the bundle, and let the corresponding extension be ε. If the bundle does not break, a state of equilibrium is set up in which there are r surviving threads out of the original n, where r satisfies the relation

$$\frac{r}{n} = \int_{\epsilon}^{\infty} \psi(\epsilon) d\epsilon = \int_{\epsilon}^{\infty} d\epsilon \int_{0}^{\infty} \phi(\epsilon, \alpha) d\alpha. \tag{4·3}$$

At extension ε the load on a particular thread is f(ε, α), and when equilibrium is established, the total load is distributed over the surviving threads so as to make

$$S = r \frac{\int_{\epsilon}^{\infty} d\epsilon \int_{0}^{\infty} f(\epsilon, \alpha) \phi(\epsilon, \alpha) d\alpha}{\int_{\epsilon}^{\infty} d\epsilon \int_{0}^{\infty} \phi(\epsilon, \alpha) d\alpha}. \tag{4·4}$$

Hence from (4·3) and (4·4) the load-extension relation for the bundle is

$$S = n \int_{\epsilon}^{\infty} d\epsilon \int_{0}^{\infty} f(\epsilon, \alpha) \phi(\epsilon, \alpha) d\alpha. \tag{4·5}$$

Breaking extension ε_r is attained when S has its greatest possible value S_r, and ε_r is therefore the root of the equation

$$\frac{d}{d\epsilon_r} \int_{\epsilon_r}^{\infty} d\epsilon \int_{0}^{\infty} f(\epsilon_r, \alpha) \phi(\epsilon, \alpha) d\alpha = 0, \tag{4·6}$$

which gives S its greatest value.

It is worth noting from (4·5) that the load-extension curve is similar for all large bundles, the load for a given extension being directly proportional to the original number of constituent threads.

27·2

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

408

H. E. Daniels

5. We now introduce certain restrictions on the behaviour of the threads which lead to simplifications in the theory.

(i) In many practical cases the load-extension curves for all threads are similar in form, differing only in a scale factor. This might be expected, for example, when the parameter $\alpha$ is the thickness of the thread. Then

$$f(e, \alpha) = \alpha f(e) \tag{5·1}$$

and (4·5) becomes $$S = nf(e) \int_{e}^{\infty} \alpha(e) \phi(e, \alpha) d\epsilon, \tag{5·2}$$

where $\alpha(e)$ is the expectation of $\alpha$ given that the thread has breaking extension $e$.

The function $f(e)$ may reasonably be taken to increase steadily with $e$, and no generality is then sacrificed if Hooke's law is assumed, since otherwise we may always transform to a new 'extension' $f(e)$. The load-extension curve is therefore taken to be

$$f(e, \alpha) = \alpha e \tag{5·3}$$

and (5·2) becomes $$S = ne \int_{e}^{\infty} \alpha(e) \phi(e, \alpha) d\epsilon. \tag{5·4}$$

(ii) It is found experimentally (cf. Peirce 1926) that the probabilities of $\alpha$ and $e$ are often distributed independently, in which case $\phi(e, \alpha) = \psi(e)\phi(\alpha)$ and $\alpha(e) = \overline{\alpha}$, independent of $e$. Then (5·4) becomes

$$S = n\overline{\alpha}e \int_{e}^{\infty} \psi(e) d\epsilon \tag{5·5}$$

and the breaking extension of the bundle satisfies

$$\frac{d}{de_r} \left\{ e_r \int_{e_r}^{\infty} \psi(e) d\epsilon \right\} = 0. \tag{5·6}$$

(iii) Finally, the dispersion of $\alpha$ may be negligibly small compared with that of breaking extension $e$. That this is a reasonable assumption in certain circumstances is evident on considering a thread composed of a large number $N$ of independent consecutive elements, such as, for example, a long chain, the $r$th element obeying Hooke's law with $\alpha = \alpha_r$. Under a load $s$ each element extends by $e_r = s/\alpha_r$ and the total extension is

$$e = \frac{1}{N} \sum_{r=1}^{N} e_r = \frac{s}{N} \sum_{r=1}^{N} \frac{1}{\alpha_r}.$$

The load-extension ratio for the whole thread is thus $\alpha$, where

$$\frac{1}{\alpha} = \frac{1}{N} \sum_{r=1}^{N} \frac{1}{\alpha_r},$$

and it follows that as the number $N$ of elements is increased the standard deviation of $\alpha$ decreases as $N^{-\frac{1}{2}}$.

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

The statistical theory of the strength of bundles of threads

409

But if $\beta(s)$ is the chance of an element succumbing under load $s$, the chance of the whole thread giving way is

$$b(s) = 1 - [1 - \beta(s)]^N.$$

When $N$ is large, and $\beta(s) \sim \kappa s^\gamma$ ($\gamma > 0$) near $s = 0$, the limiting form of $b(s)$ is

$$b(s) \sim 1 - e^{-N\kappa s^\gamma}. \tag{5·7}$$

Hence the expectation of $s$ and the standard deviation of $s$ are both proportional to $(N\kappa)^{1/\gamma}$ and so have a ratio independent of $N$.

We have reduced the problem to the simplest case when all threads have the same load-extension ratio and each thread bears an equal share of the load. Writing $\theta(\sigma)$ for the probability density of breaking load $\sigma$, where

$$\theta(\sigma) = \frac{1}{\alpha} \psi \left( \frac{\sigma}{\alpha} \right),$$

the relation between the total load $S$ and the load $s$ on each surviving thread at equilibrium is

$$S = ns \int_s^\infty \theta(\sigma) d\sigma, \tag{5·8}$$

and the breaking load $S_r$ of the bundle occurs when $s = s_r$ satisfies

$$\frac{d}{ds_r} \left\{ s_r \int_{s_r}^\infty \theta(\sigma) d\sigma \right\} = 0, \tag{5·9}$$

and gives $S$ its greatest value $S_r$.

6. A very useful way of representing these results graphically is now introduced. The notation

$$\int_0^s \theta(\sigma) d\sigma = b(s) = a \left( \frac{1}{s} \right) = a(w) \tag{6·1}$$

is used for the chance of a thread not exceeding $s$ in strength, where $w$ may be called the 'weakness' of the thread. Then (5·8) and (5·9) become

$$S = \frac{n[1 - a(w)]}{w} \tag{6·2}$$

and $$\frac{d}{dw_r} \frac{[1 - a(w_r)]}{w_r} = 0. \tag{6·3}$$

The function $a(w)$ decreases steadily from 1 to 0 as $w$ increases from 0 to $\infty$, and a typical curve is shown in figure 1. The line $PQ$ joining the points $(0, 1)$ and $(n/S, 0)$ cuts the curve at $R_1$, $R_2$ whose values of $w = w_1$, $w_2$ satisfy (6·2). Both points therefore give possible states of equilibrium under load $S$, the ordinate at each point being the fraction of the total number $n$ of threads which have broken at equilibrium. It is possible to give a physical interpretation to the region between $w_1$ and $w_2$. When the load $S$ is applied to the bundle, threads break until a fraction

This content downloaded from 179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC All use subject to https://about.jstor.org/terms

---

410

H. E. Daniels

$a(w_2)$ have given way, at which point equilibrium is established. If now additional threads are *cut*, equilibrium is still maintained until the total fraction removed is $a(w_1)$; beyond this point the cutting of an extra thread causes the whole bundle to collapse. In fact the region between $w_1$ and $w_2$ gives all possible states of equilibrium under a load $S$. Perhaps the argument is more clearly seen if it is noted that the ordinate of the *line PQ* gives the fraction of threads actually broken when the load on each thread is $1/w$, while the ordinate of the *curve* represents the fraction which must break under this load. Equilibrium is only possible when the former exceeds the latter.

The condition (6·3) which holds at breaking load is satisfied when $PQ$ is tangent to the curve at $w_r$. When $PQ$ is steeper than this, it does not intersect the curve at any point and there are no values of $w$ at which equilibrium can be established.

FIGURE 1

# *Small bundles*

7. When the bundle is small, the sample of $n$ threads may still be considered as a finite population in its own right and many of the results proved are directly applicable, but care has to be exercised in certain cases. For example, in (5·5), $\bar{\alpha}$ is the average value of $\alpha$ over those threads which survive at the point of rupture of the bundle.

In the simplest case when all threads have the same value of $\alpha$, let the strengths of the $n$ threads be arranged in descending order of magnitude as $\sigma_1, \sigma_2, \dots, \sigma_n$. Then the condition for equilibrium with $r$ survivors under a load $S$ is

$$S \leqslant r\sigma_r \quad (7\cdot1)$$

and the breaking load of the bundle is given by

$$S_r = \max(r\sigma_r). \quad (7\cdot2)$$

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

*The statistical theory of the strength of bundles of threads*

411

This rather curious rule may be illustrated by an example. Suppose that six threads when tested singly snapped at loads given in the first line of table 1. Their descending order is written out in the second line and finally the product of load × order is given. Then the rule states that if all six threads had been tested as a bundle, its breaking load would have been given by the greatest of these products, that is, by 22·0.

TABLE 1

|  load σ | 3·2 | 5·2 | 4·4 | 8·2 | 6·1 | 5·7  |
| --- | --- | --- | --- | --- | --- | --- |
|  order r | 6 | 4 | 5 | 1 | 2 | 3  |
|  σ × r | 19·2 | 20·8 | 22·0* | 8·2 | 12·2 | 17·1  |

A graphical representation analogous to figure 1 is also available for small bundles, the curve for a(w) being replaced by the survivor diagram of w_r for the sample, which descends from 1 to 0 in steps of 1/n. The example of table 1 is shown diagrammatically in figure 2.

FIGURE 2

The formulae for very large bundles were obtained on the hypothesis that they all tend to have the same breaking load. It emerges later (§ 23) that while in the majority of cases this assumption is true, for certain populations of threads the breaking loads of large bundles do not tend to a limiting value with negligible dispersion. But even in such a case, the formulae may still be validly applied to the bundle considered as a finite population.

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

412

H. E. Daniels

# THE PROBABILITY DISTRIBUTION OF BUNDLE STRENGTH

8. From now on the discussion is confined to threads having a constant value of $\alpha$. It is assumed that the bundle is randomly sampled from a population of such threads and we proceed to derive an expression for the chance that a bundle of $n$ threads is of strength less than $S$.

It is evident on considering the breakage of successive threads that if the bundle succumbs under load $S$ the conditions to be satisfied are

$$\left. \begin{array}{l} 0 \leqslant \sigma_n \leqslant \frac{S}{n}, \\ \sigma_n \leqslant \sigma_{n-1} \leqslant \frac{S}{n-1}, \\ \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \\ \sigma_3 \leqslant \sigma_2 \leqslant \frac{S}{2}, \\ \sigma_2 \leqslant \sigma_1 \leqslant S, \end{array} \right\} \tag{8·1}$$

where $\sigma_n, \sigma_{n-1}, \dots, \sigma_2, \sigma_1$ are the strengths of threads breaking in order $1, 2, \dots, n-1, n$ and the chance of the event (8·1) occurring is

$$B_n = n! \int_0^{S/n} \theta(\sigma_n) d\sigma_n \int_{\sigma_n}^{S/(n-1)} \theta(\sigma_{n-1}) d\sigma_{n-1} \dots \int_{\sigma_2}^{1/S} \theta(\sigma_2) d\sigma_2 \int_{\sigma_2}^{S} \theta(\sigma_1) d\sigma_1$$

the factor $n!$ allowing for all possible ways of arranging the threads. Setting

$$b(\sigma) = \int_0^\sigma \theta(u) du, \quad b_r = b\left(\frac{S}{r}\right), \quad x_r = b(\sigma_{r+1})$$

the formula is more simply written as

$$B_n = n! \int_0^{b_n} dx_{n-1} \int_{x_{n-1}}^{b_{n-1}} dx_{n-2} \dots \int_{x_2}^{b_2} dx_1 \int_{x_1}^{b_1} dx_0. \tag{8·2}$$

The chance (8·2) may be expressed in a variety of ways, some of which are now given.

9. The slightly more general function

$$B_n(x) = n! \int_x^{b_n} dx_{n-1} \int_{x_{n-1}}^{b_{n-1}} dx_{n-2} \dots \int_{x_2}^{b_2} dx_1 \int_{x_1}^{b_1} dx_0 \tag{9·1}$$

satisfies the equation $$\frac{\partial B_n(x)}{\partial x} = -n B_{n-1}(x)$$

with $B_0(x) = 1$ and has the property that $B_n(b_n) = 0$, consequently a Taylor expansion leads to

$$0 = B_n(x) - n(b_n - x) \bar{B}_{n-1}(x) + \frac{n(n-1)}{2!} (b_n - x)^2 B_{n-2}(x) - \dots + (-)^{n-1} (b_n - x)^{n-1} B_1(x) + (-)^n (b_n - x)^n. \tag{9·2}$$

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

The statistical theory of the strength of bundles of threads

413

Solving the set of equations with $n = n, n - 1, n - 2, \dots$ and $x = 0$ we obtain

$$B_n = n! \begin{vmatrix} b_n & \frac{b_n^2}{2!} & \frac{b_n^3}{3!} & \dots & \frac{b_n^{n-1}}{(n-1)!} & \frac{b_n^n}{n!} \\ 1 & b_{n-1} & \frac{b_{n-1}^2}{2!} & \dots & \frac{b_{n-1}^{n-2}}{(n-2)!} & \frac{b_{n-1}^{n-1}}{(n-1)!} \\ 0 & 1 & b_{n-2} & \dots & \frac{b_{n-2}^{n-3}}{(n-3)!} & \frac{b_{n-2}^{n-2}}{(n-2)!} \\ \dots & \dots & \dots & \dots & \dots & \dots \\ 0 & 0 & 0 & \dots & 1 & b_1 \end{vmatrix}$$

The corresponding formula for $B_n(x)$ is given on writing $b_r - x$ for $b_r$ in this expression.

10. There are two useful ways in which $B_n$ can be expanded in series.

(i) The first is most directly arrived at from first principles. Consider the whole range of strength from 0 to $\infty$ to be divided into intervals bounded by $S/n, S/n-1, \dots, S/2, S$. The chance of a thread having strength between $S/r-1$ and $S/r$ is $b_{r-1} - b_r$. If a bundle of $n$ threads breaks under load $S$, it must at least satisfy the condition that none of its threads exceeds $S$ in strength, otherwise the last survivor would not break. The chance that the bundle contains $p_1$ threads between $S/2$ and $S$, $p_2$ between $S/3$ and $S/2, \dots, p_{n-1}$ between $S/n-1$ and $S/n$ and $p_n$ less than $S/n$, where $p_1 + p_2 + \dots + p_n = n$ is

$$\frac{n!(b_1 - b_2)^{p_1}(b_2 - b_3)^{p_2} \dots (b_{n-1} - b_n)^{p_{n-1}} b_n^{p_n}}{p_1! p_2! \dots p_{n-1}! p_n!}.$$

But further conditions have to be satisfied if the bundle is to break under load $S$. For equilibrium never to be possible, the number of threads in the bundle which are less than $S/r$ in strength must be at least equal to $r$, in which case the $p$'s have to satisfy conditions (10-11) or their equivalent form (10-12), viz.

$$\left. \begin{array}{l} p_n \geqslant 1 \\ p_n + p_{n-1} \geqslant 2 \\ p_n + p_{n-1} + p_{n-2} \geqslant 3 \\ \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \\ p_n + p_{n-1} + \dots + p_2 \geqslant n - 1 \\ p_n + p_{n-1} + \dots + p_2 + p_1 = n \end{array} \right\}, \quad (10\cdot11) \quad \left. \begin{array}{l} p_1 \leqslant 1 \\ p_1 + p_2 \leqslant 2 \\ p_1 + p_2 + p_3 \leqslant 3 \\ \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \dots \end{array} \right\} \quad (10\cdot12)$$

The chance of the bundle breaking under load $S$ is therefore given by

$$B_n = \sum_p \frac{n!(b_1 - b_2)^{p_1}(b_2 - b_3)^{p_2} \dots (b_{n-1} - b_n)^{p_{n-1}} b_n^{p_n}}{p_1! p_2! \dots p_{n-1}! p_n!}, \quad (10\cdot2)$$

where the $p$'s are summed over all values consistent with (10-11) or (10-12). The corresponding formula for $B_n(x)$ is obtained on writing $b_r - x$ for $b_r$.

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

414

H. E. Daniels

(ii) The second series expansion is the multiple Taylor expansion of the determinant in powers of the $b_r$'s. We have

$$B_n = (B_n)_0 + \sum_r b_r \left(\frac{\partial B_n}{\partial b_r}\right)_0 + \frac{1}{2!} \sum_{r>s} \sum_{s} b_r b_s \left(\frac{\partial^2 B_n}{\partial b_r \partial b_s}\right)_0 + \dots$$

where $(\ )_0$ means that all the $b_r$'s are replaced by 0 in the bracketed expression. Many of the terms of this expansion vanish on account of two rows of the determinant becoming identical after differentiation when the $b_r$'s are made zero, and in fact the only non-vanishing terms are obtained as follows. Numbering the rows from the bottom upwards, first the $r_1$th row is differentiated $r_1$ times, then the $(r_1+r_2)$th row $r_2$ times, the $(r_1+r_2+r_3)$th row $r_3$ times and so on, till finally the $n$th (top) row is differentiated $r_m$ times where $r_1+r_2+\dots+r_m=n$, it being essential to differentiate the top row at least once. If the resulting determinant is then rearranged with the $r_1$th row at the bottom, the $(r_1+r_2)$th row in place of the $r_1$th, the $(r_1+r_2+r_3)$th in place of the $(r_1+r_2)$th and so on, the sign of the determinant is changed by

$$(-)^{r_1-1+r_2-1+\dots+r_n-1} = (-)^{n-m}$$

and its value becomes unity. The expansion is therefore

$$B_n = \sum_{m=1}^n \sum_r (-)^{n-m} \frac{n! b_{r_1}^{r_1} b_{r_1+r_2}^{r_2} \dots b_{r_1+r_2+\dots+r_{m-1}}^{r_{m-1}} b_n^{r_m}}{r_1! r_2! \dots r_{m-1}! r_m!} \tag{10·3}$$

summed over all values of the $r$'s such that $r_l \geqslant 1$, all $t$, and $r_1+r_2+\dots+r_m=n$.

Using this expansion, the following formulae are obtained

$$B_0 = 1, \quad B_1 = b_1, \quad B_2 = 2b_1b_2 - b_1^2,$$

$$B_3 = 6b_1b_2b_3 - 3b_1^2b_3 - 3b_1b_3^2 - b_3^2,$$

$$B_4 = 24b_1b_2b_3b_4 - 12b_1^2b_3b_4 - 12b_1b_3^2b_4 - 12b_1b_2b_4^2 - 4b_3^2b_4 + 6b_1^2b_4^2 - 4b_1b_4^2 - b_4^4$$

though in practice it is perhaps simpler to build them up by means of the recurrence formula (9·2) with $x=0$. For higher values of $n$ the formulae rapidly become unmanageable, and it is necessary to seek an asymptotic expression for $B_n$. Before considering this question, however, mention must be made of two forms of $b(s)$ which, though not common ones in practice, give rise to specially simple $B_n$ expressions for all values of $n$.

11. Consider the case where the threads have only two possible strengths $\rho$ and $\nu\rho$, that is

$$\left. \begin{array}{ll} b(s) = 0 & (0 \leqslant s < \rho), \\ b(s) = b & (\rho \leqslant s < \nu\rho), \\ b(s) = 1 & (\nu\rho \leqslant s), \end{array} \right\} \tag{11·1}$$

and let a load $S$ be applied to a bundle of $n$ of such threads.

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

The statistical theory of the strength of bundles of threads

415

We observe first that $b_n = 0$ and hence $B_n = 0$ whenever $S < n\rho$. Divide up the range of $S$ into the intervals $r\nu\rho \leqslant S < (r+1)\nu\rho$. Then for values of $S \geqslant n\rho$ we have, when $S$ is in the $r$th interval,

$$b_m = b\left(\frac{S}{m}\right) = 1 \quad (m \leqslant r),$$

$$b_m = b \quad (m > r).$$

This holds for all intervals having $r > \left[\frac{n}{\nu}\right]$ and also for that part of the interval $r = \left[\frac{n}{\nu}\right]$ in which $S \geqslant n\rho$.

Consider now the series expansion (10·2). When $S \geqslant n\rho$ and $S$ is in the $r$th interval the only non-vanishing terms are those in which $p_m = 0$ except for $m = r$ and $m = n$. Writing $p_r = p$, $p_n = n - p$ conditions (11·12) imply that $p \leqslant r$ and the expression for $B_n$ becomes, with this special form for $b(s)$,

$$\left. \begin{array}{l} B_n = 0 \\ B_n = \sum_{p=0}^{r} \frac{n!(1-b)^p b^{n-p}}{p!(n-p)!} \end{array} \right\} \quad \text{when} \quad S < n\rho, \quad \text{when} \quad r\nu\rho \leqslant S < (r+1)\nu\rho \quad \text{and} \quad S \geqslant n\rho. \tag{11·2}$$

The strength of the bundle can therefore only have values $r\nu\rho$ ($r > \left[\frac{n}{\nu}\right]$) or $n\rho$, the probability of the value $r\nu\rho$ being the coefficient of $t^r$ in $[b+t(1-b)]^n$ and the probability of $n\rho$ the sum of the coefficients of $t^p$ for values of $p \leqslant \left[\frac{n}{\nu}\right]$. The approximate form of $B_n$ when $n$ is large is in this case easily deduced from the normal approximation to the binomial distribution. For very large $n$ there are two distinct limiting forms according to whether the 'collapsed' part contains the greater or lesser number of binomial terms, the appropriate conditions being $\nu(1-b) < 1$ or $> 1$ respectively. In the first case all values concentrate at $S = n\rho$; in the second they concentrate at $n\nu\rho(1-b)$. These ultimate limiting forms are immediately obvious on applying the method of § 6 for very large bundles.

12. The second form of $b(s)$ is that in which the weakness $w = 1/s$ of a thread has an equal chance of lying anywhere in the interval $0 \leqslant w \leqslant 1/s_0$ but cannot exceed $1/s_0$, that is

$$\left. \begin{array}{l} b(s) = 0 \quad (0 \leqslant s < s_0) \\ b(s) = 1 - \frac{s_0}{s} \quad (s_0 \leqslant s). \end{array} \right\} \tag{12·1}$$

We now show that the chance that a bundle of $n$ threads sampled from such a population has strength less than $S$ is

$$\left. \begin{array}{l} B_n = 0 \quad (0 \leqslant S < n s_0) \\ B_n = 1 - \frac{n s_0}{S} \quad (n s_0 \leqslant S) \end{array} \right\} \tag{12·2}$$

so that for all values of $n$ the probability distribution of $S/n$ is simply $b(S/n)$.

This content downloaded from

179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC

All use subject to https://about.jstor.org/terms

---

416

H. E. Daniels

The proof is as follows. Evidently $b_n = 0$ when $0 \leqslant S < ns_0$ and hence $B_n$ vanishes for values of $S$ in this interval. Let $S \geqslant ns_0$ and insert $b_r = 1 - \frac{rs_0}{S}$ in (9·1). The function

$$B_n(x) = (1 - x)^n - \frac{ns_0}{S}(1 - x)^{n-1}$$

is such that $B_0(x) = 1$, $B_n\left(1 - \frac{ns_0}{S}\right) = 0$ and it satisfies

$$\frac{\partial B_n(x)}{\partial x} = -nB_{n-1}(x).$$

It must therefore be identical with (9·1) for the particular form of $b_r$ chosen, and putting $x = 0$ the result follows.

The method already given for large bundles breaks down in this case since

$$s[1 - b(s)] = s_0$$

for $s_0 \leqslant s$ and there is no unique value of $s_r$ which maximizes it. It will be of interest later to recall (12·2) in connexion with the asymptotic form of $B_n$ when $b(s)$ behaves like $1 - s_0/s$ for large $s$ (§ 23).

# THE ASYMPTOTIC BEHAVIOUR OF $B_n$ FOR LARGE $n$

13. It has been shown that as $n$ becomes very large the bundle strength is likely to concentrate near a value $S_r = n \max s[1 - b(s)]$. No indication has so far been given, however, except in two special cases of the form assumed by $B_n$ in the vicinity of $S_r$, and the remainder of the paper is devoted to a study of the asymptotic behaviour of $B_n$ for general forms of the parent distribution $b(s)$. The mode of attack adopted here provides the dominant term of the asymptotic expansion together with the order of magnitude of the approximation involved.

It is first necessary to derive an important identity upon which the subsequent theory depends. Let us introduce the notation

$$\begin{aligned} (n, m) &= \int_0^{b_n} dx_{n-1} \int_{x_{n-1}}^{b_{n-1}} dx_{n-2} \dots \int_{x_{m+1}}^{b_{m+1}} dx_m \\ &= \left| \begin{array}{cccc} b_n & \frac{b_n^2}{2!} & \dots & \frac{b_n^{n-m-1}}{(n-m-1)!} & \frac{b_n^{n-m}}{(n-m)!} \\ 1 & b_{n-1} & \dots & \frac{b_{n-1}^{n-m-2}}{(n-m-2)!} & \frac{b_{n-1}^{n-m-1}}{(n-m-1)!} \\ \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots \\ 0 & 0 & \dots & 1 & b_{m+1} \end{array} \right| \tag{13·1}$$

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

The statistical theory of the strength of bundles of threads

417

and $$(n, n) = 1$$, so that, for example, $$B_n = n!(n, 0)$$. Now in the determinant $$(n, 0)$$ multiply the $$(n-1)$$th column by $$-x$$, the $$(n-2)$$th column by $$\frac{x^2}{2!}$$, ..., the 1st column by $$(-)^{n-1} \frac{x^{n-1}}{(n-1)!}$$ and add them to the last column, thus obtaining

$$(n, 0) = \left| \begin{array}{cccccc} b_n & \frac{b_n^2}{2!} & \frac{b_n^3}{3!} & \dots & \frac{b_n^{n-1}}{(n-1)!} & \frac{(b_n - x)^n}{n!} - (-)^n \frac{x^n}{n!} \\ 1 & b_{n-1} & \frac{b_{n-1}^2}{2!} & \dots & \frac{b_{n-1}^{n-2}}{(n-2)!} & \frac{(b_{n-1} - x)^{n-1}}{(n-1)!} \\ 0 & 1 & b_{n-2} & \dots & \frac{b_{n-2}^{n-3}}{(n-3)!} & \frac{(b_{n-2} - x)^{n-2}}{(n-2)!} \\ \dots & \dots & \dots & \dots & \dots & \dots \\ 0 & 0 & 0 & \dots & 1 & b_1 - x \end{array} \right|$$

The expansion of the determinant in terms of the last column may then be rearranged to give

$$\frac{x^n}{n!} \equiv \sum_{m=0}^n (n, m) \frac{(x - b_m)^m}{m!} \quad \text{for all } x, \tag{13·21}$$

or, more generally, after differentiating $$r$$ times,

$$\frac{x^{n-r}}{(n-r)!} \equiv \sum_{m=r}^n (n, m) \frac{(x - b_m)^{m-r}}{(m-r)!} \quad \text{for all } x \text{ and } r \geqslant 0. \tag{13·22}$$

One observes in passing that $$(n, m)$$ is related to the chance $$B_{n,m}$$ that $$m$$ threads will survive under a load $$S$$ by the formula

$$B_{n,m} = \frac{n!}{m!} (n, m) (1 - b_m)^m.$$

Substituting in (13·21) leads to

$$x^n = \sum_{m=0}^n B_{n,m} \left( \frac{x - b_m}{1 - b_m} \right)^m, \quad \text{all } x.$$

For example, when $$x = 1$$ the result $$1 = \sum_{m=0}^n B_{n,m}$$ simply expresses the fact that values of $$m$$ from 0 to $$n$$ exhaust all possible contingencies.

The identities (13·21) and (13·22) are not in the form most convenient for our purpose. Writing $$x = 1/\lambda$$, (13·21) becomes

$$1 \equiv \sum_{m=0}^n \frac{n!(n, m)}{m!} \lambda^{n-m} (1 - \lambda b_m)^m, \quad \text{all } \lambda,$$

and by analogy with the binomial distribution, one is led to consider the expression

$$Q_{n,m} = \frac{(n-m)!(n, m)}{b_m^{n-m}} = (n-m)! \int_0^{b_n/b_m} dx_{n-1} \int_{x_{n-1}}^{b_{n-1}/b_m} dx_{n-2} \dots \int_{x_{m+1}}^{b_{m+1}/b_m} dx_m, \tag{13·3}$$

This content downloaded from

179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC

All use subject to https://about.jstor.org/terms

---

418

H. E. Daniels

which satisfies, and is in fact uniquely determined by,

$$1 = \sum_{m=0}^{n} Q_{n,m} \frac{n! (\lambda b_m)^{n-m} (1 - \lambda b_m)^m}{m! (n-m)!}, \quad \text{all } \lambda, \tag{13·4}$$

or the more general identity

$$1 = \sum_{m=r}^{n} Q_{n,m} \frac{(n-r)! (\kappa b_m)^{n-m} (1 - \kappa b_m)^{m-r}}{(m-r)! (n-m)!}, \quad \text{all } \kappa, \text{ all } r \geqslant 0, \tag{13·5}$$

where $\kappa$ is written in place of $\lambda$ for a reason that will be apparent later. Note that $Q_{n,0}$ is simply $B_n$.

### The function $T_{n,m,r}$

14. When $n$ is large, (13·4) and (13·5) approximate to integral equations and the behaviour of $Q_{n,m}$ for large $n$ is evidently related to that of

$$T_{n,m,r} = \frac{(n-r)! (\kappa b_m)^{n-m} (1 - \kappa b_m)^{m-r}}{(m-r)! (n-m)!}.$$

A substantial digression is therefore made at this stage to investigate the asymptotic behaviour of $T_{n,m,r}$.

It will be found simplest first to discuss the special case

$$T_{n,m} = \frac{n! (\lambda b_m)^{n-m} (1 - \lambda b_m)^{m-r}}{m! (n-m)!},$$

and to extend the results afterwards to the more general function. The important range of $\lambda$ is $0 \leqslant \lambda \leqslant 1$ in which $T_{n,m}$ is never negative. In the case of the ordinary binomial distribution $\frac{n! p^{n-m} (1-p)^m}{m! (n-m)!}$ there are two distinct limiting forms for large $n$.

When neither $p$ nor $1-p$ is small the binomial is approximated to by a continuous normal distribution having the same first and second moments $np$ and $np(1-p)$ respectively. On the other hand, when $p$ is small the appropriate limiting form is the discrete Poisson distribution with parameter $np$, and similarly for small $1-p$. In the present more general case it is useful to preserve the distinction, and we first discuss various continuous limiting forms corresponding to the normal approximation.

### Continuous limiting forms of $T_{n,m}$

15. Assuming that both $m$ and $n-m$ are $O(n)$ so that neither $m/n$ nor $1-m/n$ is small, Stirling's formula gives

$$T_{n,m} = \frac{n^{n+\frac{1}{2}} (\lambda b_m)^{n-m} (1 - \lambda b_n)^m}{\sqrt{2\pi} m^{m+\frac{1}{2}} (n-m)^{n-m+\frac{1}{2}}} [1 + O(n^{-1})].$$

Writing $m/n = z$, $1/n = dz$, $S = n\zeta$, $T_{n,m} = T_n(z) dz$ and $a(1/s) = b(s)$ as defined in §7, the approximation is

$$T_n(z) dz = \sqrt{\left(\frac{n}{2\pi}\right)} \frac{dz}{\sqrt{[z(1-z)]}} \left[\frac{\lambda a(z/\zeta)}{1-z}\right]^{n(1-z)} \left[\frac{1 - \lambda a(z/\zeta)}{z}\right]^{nz} [1 + O(n^{-1})]. \tag{15·1}$$

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

The statistical theory of the strength of bundles of threads

419

Clearly the important regions for $T_n(z)$ are near the maxima of

$$\begin{aligned} F(z) &= \left[ \frac{\lambda a(z/\zeta)}{1-z} \right]^{(1-z)} \left[ \frac{1-\lambda a(z/\zeta)}{z} \right]^z \\ &= \left[ 1 - \frac{(1-z-\lambda a)}{1-z} \right]^{(1-z)} \left[ 1 + \frac{(1-z-\lambda a)}{z} \right]^z \\ &= \exp \left\{ -\frac{1}{2}(1-z-\lambda a)^2 \left( \frac{1}{1-z} + \frac{1}{z} \right) - \frac{1}{3}(1-z-\lambda a)^3 \left( \frac{1}{(1-z)^2} - \frac{1}{z^2} \right) - \dots \right\}. \end{aligned} \tag{15·2}$$

Differentiating, $\frac{F'}{F} = \frac{(1-z\lambda a)}{z(1-z)} \left( 1 + \frac{\lambda}{\zeta} a' \right) + \text{higher powers of } (1-z-\lambda a)$,

$$\frac{F''}{F} - \left( \frac{F'}{F} \right)^2 = - \frac{\left( 1 + \frac{\lambda}{\zeta} a' \right)}{z(1-z)} + \text{terms containing } (1-z-\lambda a).$$

The condition $F'(z) = 0$ is thus at least satisfied when

$$1-z-\lambda a(z/\zeta) = 0 \tag{15·3}$$

and at the roots $z = z_r$ of this equation it is found that

$$F(z_r) = 1, \quad F''(z_r) = - \left[ 1 + \frac{\lambda}{\zeta} a'(z_r/\zeta) \right]^2 / z_r(1-z_r). \tag{15·4}$$

It follows that the roots $z_r$ are all maxima of $F(z)$.

Moreover, at all other points in $0 < z < 1$ one must necessarily have $F(z) < 1$. For consider $F = e^G$ as a function of $\lambda$. Turning points occur when $G_\lambda = 0$, where

$$G_\lambda = a \left\{ \frac{1-z}{\lambda a} - \frac{z}{1-\lambda a} \right\} = \frac{(1-z-\lambda a)}{\lambda(1-\lambda a)}$$

and for given $z$ there is only one value of $\lambda$ satisfying $G_\lambda = 0$, namely, that making $1-z-\lambda a = 0$. Furthermore

$$G_{\lambda\lambda} = -a^2 \left\{ \frac{1-z}{(\lambda a)^2} + \frac{z}{(1-\lambda a)^2} \right\},$$

showing that $G_{\lambda\lambda} < 0$ for all $z$ and $\lambda$ lying between 0 and 1. Hence $G$ has a unique maximum at the point $\lambda = (1-z)/a$ and so has $F$ for the same $\lambda$, taking the value $F = 1$ there, and decreasing steadily on either side of it. No values of $z$ and $\lambda$ between 0 and 1 can therefore be found at which $F \geqslant 1$ and $1-z-\lambda a \neq 0$, for if such a value existed, then at $\lambda = (1-z)/a$ one should also have $F = 1$, $1-z-\lambda a = 0$ which would imply $G_{\lambda\lambda} \geqslant 0$ at some point of the range.

Considering $F$ once more as a function of $z$ for fixed $\lambda$, we conclude that when $n$ is large, $F^n$ is negligible except near the roots $z = z_r$ of (15·3) at which it approximates to 1, and consequently $T_n(z)$ consists of a series of isolated peaks situated at these roots.

The positions of the roots are conveniently examined by means of a diagram (figure 3) similar to that introduced in §7. A typical curve for $a(w)$ is shown. The line joining the point $(0, 1/\lambda)$ to the point $(1/\zeta, 0)$ intersects the curve at points

This content downloaded from

179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC

All use subject to https://about.jstor.org/terms

---

420

H. E. Daniels

$z_1/\zeta, z_2/\zeta, z_3/\zeta$, and it is evident that $z_1, z_2, z_3$ so found are the only positive roots of $1-z-\lambda a(z/\zeta) = 0$. With an $a(w)$ curve of the form shown a maximum of 3 positive real roots is possible with suitable values of $\zeta$ and $\lambda$, and in general the maximum number of roots is odd.

FIGURE 3

16. Consider first the behaviour of $T_n(z)$ near a simple real root $z_r$ such that neither $z_r$ nor $1-z_r$ is small. On substituting

$$1-z-\lambda a(z/\zeta) = -\left[1+\frac{\lambda}{\zeta}a'(z_r/\zeta)\right]^2(z-z_r)^2 + O(z-z_r)^3$$

in (15·2) the appropriate expansion of (15·1) is found to be

$$T_n(z) = \sqrt{\left(\frac{n}{2\pi z_r(1-z_r)}\right) \exp\left[-\frac{n\left[1+\frac{\lambda}{\zeta}a'(z_r/\zeta)\right]^2(z-z_r)^2}{2z_r(1-z_r)}\right] \{1+O(n(z-z_r)^3) + O(z-z_r)\}}.$$

Since the exponential is negligibly small except when $n(z-z_r)^2 = O(1)$, only the range $z-z_r = O(n^{-1})$ need be considered and the approximation factor is $1+O(n^{-1})$. It will be found more useful, however, to write the result in the form

$$T_n(z) = \sqrt{\left(\frac{n}{2\pi z_r(1-z_r)}\right) \exp\left[-\frac{n\left[1+\frac{\lambda}{\zeta}a'(z_r/\zeta)\right]^2(z-z_r)^2}{2z_r(1-z_r)}\right]} \times \{1+A(z-z_r) + Bn(z-z_r)^3 + O(n^{-1})\}, \quad (16\cdot1)$$

where the constants $A$ and $B$ are $O(1)$.

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

The statistical theory of the strength of bundles of threads

421

17. Suppose next that the two roots $z_2$ and $z_3$, which may be real or complex, are such that $|z_2 - z_3|$ is small. It is assumed that neither $|z_r|$ nor $|1 - z_r|$ is small ($r = 2, 3$).

Write

$$\epsilon = \frac{1}{2}(z_3 - z_2)$$

and

$$f(z) = 1 - z - \lambda a(z/\zeta).$$

Let $\bar{z}$ be that value of $z$ near $z_2, z_3$ which makes $f'(z) = 0$; then since

$$f(z) = f(\bar{z}) + \frac{1}{2}(z - \bar{z})^2 f''(\bar{z}) + O(z - \bar{z})^3$$

and $$f(z_2) = f(z_3) = 0, \quad f''(\bar{z}) = -\frac{\lambda}{\zeta^2} a''(\bar{z}/\zeta)$$

it follows, if $f''(\bar{z})$ is not small and $z - \bar{z} = O(\epsilon)$, that

$$f(z) = -\frac{\lambda a''(\bar{z}/\zeta)}{2\zeta^2} [(z - \bar{z})^2 - \epsilon^2] + O(\epsilon^3) \tag{17·1}$$

and $$\bar{z} = \frac{1}{2}(z_2 + z_3) + O(\epsilon^2).$$

The sign of $\epsilon^2$ may be either positive or negative according as the roots are real or complex.

If the parameters $\lambda$ and $\zeta$ are altered until $z_2 = z_3$, we shall call the coincident value of the roots a critical point of $z$. In particular, two critical points $z_r, z_c$ are obtained by (i) keeping $\lambda$ fixed and changing $\zeta$ or (ii) keeping $\zeta$ fixed and changing $\lambda$, respectively, the corresponding critical values of $\zeta$ and $\lambda$ being $\zeta_r$ and $\lambda_c$. It will be shown that both $z_r$ and $z_c$ differ from $\bar{z}$ by $O(\epsilon^2)$. They are illustrated graphically in figure 4.

Expressions for $T_n(z)$ are now obtained in terms of $z_r$ and $z_c$ respectively.

(i) Put $w = z/\zeta$, $w_r = z_r/\zeta_r$, and let

$$\zeta(w) = \frac{1 - \lambda a(w)}{w} = \zeta_r + (w - w_r)\zeta_r' + \frac{1}{2}(w - w_r)^2 \zeta_r'' + O(w - w_r)^3,$$

where the suffix $\tau$ denotes evaluation at $w_r$. By (15·3),

$$\zeta(w_2) = \zeta(w_3) = \zeta, \quad \zeta_r' = 0, \quad \zeta_r'' = -\frac{\lambda a_r''}{w_r}.$$

In general $\zeta_r''$ is not small, so that

$$w_r = \frac{1}{2}(w_2 + w_3) + O(\epsilon^2), \quad \epsilon^2 = \frac{1}{4}\zeta_r^2(w_2 - w_3)^2 + O(\epsilon^3)$$

or, to the same order

$$z_r = \bar{z} + O(\epsilon^2), \quad \epsilon^2 = -\frac{2z_r \zeta_r}{\lambda a_r''} (\zeta - \zeta_r) + O(\epsilon^2),$$

and inserting these results in (16·1) and (15·2) the form of $F(z)$ in the range $z - z_r = O(\epsilon)$ is found to be

$$F(z) = \exp \left\{ -\frac{1}{2z_r(1 - z_r)} \left[ \frac{\lambda a_r''}{2\zeta_r^2} (z - z_r)^2 + \frac{z_r}{\zeta_r} (\zeta - \zeta_r) \right]^2 + O(\epsilon^5) \right\}.$$

Vol. 183. A.

28

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

422

H. E. Daniels

Now $\epsilon$ has to be at most $O(n^{-\frac{1}{2}})$ for otherwise $T_n(z)$ in (15·1) becomes small at $z - z_r$ and $z_2, z_3$ may then be considered as isolated simple roots. Also, in the vicinity of $z_r$, $T_n(z)$ is negligible outside a range $z - z_r = O(n^{-\frac{1}{2}})$ and its approximate form is therefore

$$T_n(z) = \sqrt{\left(\frac{n}{2\pi z_r(1-z_r)}\right) \exp\left\{-\frac{n}{2z_r(1-z_r)}\left[\frac{\lambda a_r''}{2\zeta_r^2}(z-z_r)^2 + \frac{z_r}{\zeta_r}(\zeta-\zeta_r)\right]^2\right\}\{1+O(n^{-\frac{1}{2}})\} \tag{17·2}$$

provided $z_r = O(1), \quad 1 - z_r = O(1).$

FIGURE 4

(ii) Let $\lambda(z) = \frac{1-z}{a(z/\zeta)} = \lambda_c + (z-z_c)\lambda_c' + \frac{1}{2}(z-z_c)^2\lambda_c'' + O(z-z_c)^3.$

By definition $\lambda(z_2) = \lambda(z_3) = 0$, and $\lambda_c' = 0$, $\lambda_c'' = -\lambda_c a_c'' / \zeta^2 a_c$, the suffix $c$ denoting evaluation at $z_c$. Since $\lambda_c''$ is not usually small, it follows that

$$z_c = \bar{z} + O(\epsilon^2), \quad \epsilon^2 = -\frac{2\zeta^2 a_c}{\lambda_c a_c''}(\lambda - \lambda_c) + O(\epsilon^3)$$

and, as before, the approximate form of $T_n(z)$ is

$$T_n(z) = \sqrt{\left(\frac{n}{2\pi z_c(1-z_c)}\right) \exp\left\{-\frac{n}{2z_c(1-z_c)}\left[\frac{\lambda_c a_c''}{2\zeta^2}(z-z_c)^2 + \frac{a_c}{\zeta}(\lambda - \lambda_c)\right]^2\right\}\{1+O(n^{-\frac{1}{2}})\}. \tag{17·3}$$

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

The statistical theory of the strength of bundles of threads

423

There is one other continuous limiting form of $T_n(z)$ which has to be considered. When the first root $z_1$ is isolated and small the approximation to $T_n(z)$ in its vicinity is no longer given by (16·1), the discrete limiting form discussed below (§ 20) taking its place. But when $z_1$ and $z_2$ are close together and both small, a continuous approximation to $T_n(z)$ is still appropriate. It is best to discuss this case later (§ 19) in its more general form, after the results so far obtained have been extended to $T_{n,m,r}$.

### Continuous limiting forms of $T_{n,m,r}$

18. The asymptotic behaviour of the function

$$T_{n,m,r} = \frac{(n-r)! (\kappa b_m)^{n-m} (1-\kappa b_m)^m}{(n-m)! (m-r)!}$$

is discussed on similar lines and the proofs will be only briefly sketched. For $T_{n,m,r}$ to be never negative in the range $r \leqslant m \leqslant n$, $\kappa$ has to satisfy the condition

$$0 \leqslant \kappa \leqslant 1/b_r. \tag{18·1}$$

The continuous approximations hold when neither $(m-r)/n$ nor $1-m/n$ is small, and Stirling's formula then gives

$$T_{n,m,r} = \frac{(n-r)^{n-r+\frac{1}{2}} (\kappa b_m)^{n-m} (1-\kappa b_m)^{m-r}}{\sqrt{2\pi} (m-r)^{m-r+\frac{1}{2}} (n-m)^{n-m+\frac{1}{2}}} [1+O(n^{-1})].$$

Adopting the previous notation and putting in addition

$$r = nx, \quad T_{n,m,r} = T_n(z, x) dz$$

this becomes

$$T_n(z, x) = \sqrt{\left(\frac{n(1-x)}{2\pi(z-x)(1-z)}\right) (1-x)^{n(1-x)} \left[\frac{\kappa a(z/\zeta)}{1-z}\right]^{n(1-x)}} \times \left[\frac{1-\kappa a(z/\zeta)}{z-x}\right]^{n(z-x)} [1+O(n^{-1})], \tag{18·2}$$

where $x < z < 1$, and we may write

$$F(z, x) = (1-x)^{(1-x)} \left[\frac{\kappa a(z/\zeta)}{1-z}\right]^{(1-x)} \left[\frac{1-\kappa a(z/\zeta)}{z-x}\right]^{(z-x)} = \exp \left\{ -\frac{1}{2}(1-z-\lambda a)^2 \left(\frac{1}{1-z} + \frac{1}{z-x}\right) - \frac{1}{3}(1-z-\lambda a)^2 \left(\frac{1}{(1-z)^2} - \frac{1}{(z-x)^2}\right) - \cdots \right\}, \tag{18·3}$$

where $\lambda = (1-x)\kappa$. (18·4)

By (18·1), $\lambda$ must satisfy the condition

$$0 \leqslant \lambda \leqslant \lambda_x = (1-x)/a(x/\zeta). \tag{18·5}$$

28·2

This content downloaded from 179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC All use subject to https://about.jstor.org/terms

---

424

H. E. Daniels

$F(z, x)$ then takes its maximum value $F = 1$ at the roots $z_r$ of $1 - z - \lambda a(z/\zeta) = 0$, and the argument proceeds as before. Near an isolated simple root $z_r$ such that $x < z_r < 1$, $z_r - x = O(1)$, $1 - z_r = O(1)$ the limiting form of $T_n(z, x)$ is

$$T_n(z, x) = \sqrt{\left(\frac{n(1-x)}{2\pi(z_r-x)(1-z_r)}\right)} \times \exp\left(-\frac{n(1-x)\left[1+\frac{\lambda}{\zeta}a'(z_r/\zeta)\right]^2(z-z_r)^2}{2(z_r-x)(1-z_r)}\right)[1+A(z-z_r)+Bn(z-z_r)^3+O(n^{-1})], \tag{18·6}$$

and near a critical point the formulae corresponding to (17·2) and (17·3) are

$$T_n(z, x) = \sqrt{\left(\frac{n(1-x)}{2\pi(z_r-x)(1-z_r)}\right)} \times \exp\left\{-\frac{n(1-x)}{2(z_r-x)(1-z_r)}\left[\frac{\lambda a_r''}{2\zeta_r^2}(z-z_r)^2+\frac{z_r}{\zeta_r}(\zeta-\zeta_r)\right]^2\right\}[1+O(n^{-1})] \tag{18·7}$$

$$T_n(z, x) = \sqrt{\left(\frac{n(1-x)}{2\pi(z_c-x)(1-z_c)}\right)} \times \exp\left\{-\frac{n(1-x)}{2(z_c-x)(1-z_c)}\left[\frac{\lambda_c a_c''}{2\zeta^2}(z-z_c)^2+\frac{a_c}{\zeta}(\lambda-\lambda_c)\right]^2\right\}[1+O(n^{-1})]. \tag{18·8}$$

19. Suppose now that $x$ is in the neighbourhood of the critical point. Let $z_c - x = O(\epsilon)$; then, on substituting (17·1) in (18·3), $F(z, x)$ assumes the form

$$F(z, x) = \exp\left\{-\frac{1}{2(z-x)}\left[\frac{\lambda_c a_c''}{2\zeta^2}(z-z_c)^2+\frac{a_c}{\zeta}(\lambda-\lambda_c)\right]^2+O(\epsilon^4)\right\}$$

since $1 - z_c' = 1 - x + O(\epsilon)$, and (18·2) becomes

$$T_n(z, x) = \sqrt{\left(\frac{n}{2\pi(z-x)}\right)} \times \exp\left\{-\frac{n}{2(z-x)}\left[\frac{\lambda_c a_c''}{2\zeta^2}(z-z_c)^2+\frac{a_c}{\zeta}(\lambda-\lambda_c)\right]^2\right\}[1+O(\epsilon)+O(n\epsilon^4)]. \tag{19·1}$$

For the exponent to be $O(1)$ at $z = z_c$ we must have $\epsilon = O(n^{-1})$ and so, over a range $z - z_c = O(n^{-1})$, (19·1) holds to $O(n^{-1})$.

In the discussion of the limiting form of $Q_{n,m}$, however, it will be necessary to assume $\epsilon = O(n^{-1})$ in this case. At $z = z_c$ the exponent is then $O(n^1)$ and $T_n(z, x)$ splits into two isolated peaks at $z_2, z_3$. The behaviour of $T_n(z, x)$ near $z_3$ is of interest, and one would expect the approximation (18·6) to hold there, but to a lower order of accuracy. To study $T_n(z, x)$ near $z_3$, write (17·1) as

$$f(z) = -\frac{\lambda_c a_c''}{2\zeta_c^2}(z-z_2)(z-z_3) + O(\epsilon^3).$$

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

The statistical theory of the strength of bundles of threads

425

$T_n(z, x)$ is not negligible in a range of $z - z_3$ satisfying

$$\frac{n \lambda_c^2 a_c^{n2}}{8 \zeta_c^2} \frac{(z - z_3)^2 (z - z_3)^2}{(z - x)} = O(1)$$

and since $z - z_3$ and $z - x$ are $O(n^{-\frac{1}{2}})$, this implies

$$z - z_3 = O(n^{-\frac{1}{2}}).$$

The approximation near $z_3$ when $\epsilon = O(n^{-\frac{1}{2}})$ is then found to be

$$T_n(z, x) = \sqrt{\left(\frac{n}{2\pi(z_3 - x)}\right)} \times \exp\left[-\frac{n \lambda_c^2 a_c^{n2}}{2 \zeta^4} \frac{(z_3 - z_c)^2 (z - z_3)^2}{(z_3 - x)}\right] [1 + A n^2 (z - z_3) + B n (z - z_3)^2 + O(n^{-\frac{1}{2}})], \quad (19\cdot2)$$

where $A$, $B$ are $O(1)$ and independent of $z$. The formula agrees to $O(n^{-\frac{1}{2}})$ with (18·6).

# Discrete limiting forms of $T_{n,m}$

20. Reverting once more to

$$T_{n,m} = \frac{n!}{m!(n-m)!} (\lambda b_m)^{n-m} (1 - \lambda b_m)^m$$

the analogue of the Poisson binomial limit, when $n$ is large but $m$ is $O(1)$ is next discussed. It is assumed that $a(z/\zeta)$ admits of an expansion in integral powers of $z$ near $z = 0$. The possibility of an expansion in non-integral powers is realized, and, in fact, such an expansion is to be expected in some cases in view of the limiting form (5·7). But the more general analysis is not essentially different, and for simplicity only integral powers are considered. The expansion of $a(z/\zeta)$ is then

$$a(z/\zeta) = 1 + a'(0) \frac{z}{\zeta} + O(z^2),$$

i.e. $$b_m = 1 - \frac{\zeta_0 m}{\zeta n} + O(n^{-2}) \quad (20\cdot1)$$

where $1/\zeta_0$ is the intercept on the horizontal axis of the tangent to the $a(w)$ curve at the origin. Two types of $a(w)$ curve are shown in figures 5 and 6. Since the important values of $\lambda$ turn out to be near $\lambda = 1$, we put

$$\lambda = 1 - \frac{\mu}{n}$$

where $\mu$ is $O(1)$. Then

$$(n - m) \log \lambda b_m = -(\mu + m \zeta_0 / \zeta) + O(n^{-1})$$

and $$(1 - \lambda b_m) = \frac{1}{n} (\mu + m \zeta_0 / \zeta) + O(n^{-2}).$$

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

426

H. E. Daniels

FIGURE 5

FIGURE 6

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

The statistical theory of the strength of bundles of threads

427

Hence $$T_{n,m} = \frac{n^{n+\frac{1}{2}}e^{-m}(\mu + m\zeta_0/\zeta)^m}{m!(n-m)^{n-m+\frac{1}{2}}n^m} e^{-(\mu + m\zeta_0/\zeta)}[1 + O(n^{-1})]$$

and since $$\left(1 - \frac{m}{n}\right)^{n-m+\frac{1}{2}} = e^{-m}[1 + O(n^{-1})],$$

the appropriate limiting form of $T_{n,m}$ is

$$T_{n,m} = \frac{(\mu + m\zeta_0/\zeta)^m}{m!} e^{-(\mu + m\zeta_0/\zeta)}[1 + O(n^{-1})]. \tag{20-2}$$

The majority of distributions encountered in practice are such that $\zeta_0 = 0$ for this condition implies that the chance that a thread exceeds $S$ in strength tends to zero more rapidly than $1/S$ as $S$ increases. In that case (20-2) degenerates to the Poisson formula

$$T_{n,m} = \frac{\mu^m}{m!} e^{-\mu}[1 + O(n^{-1})]. \tag{20-3}$$

It is a useful confirmation of a later result to prove that when $\zeta > \zeta_0$ and $\zeta - \zeta_0$ is not small

$$\sum_{m=0}^{\infty} \frac{(\mu + m\zeta_0/\zeta)^m}{m!} e^{-(\mu + m\zeta_0/\zeta)} = \frac{1}{1 - \zeta_0/\zeta}. \tag{20-4}$$

which is independent of $\mu$.

The series converges since the ratio of the $(m+1)$th to the $m$th term tends to $\zeta_0/\zeta \cdot \exp 1 - \zeta_0/\zeta$ which is less than 1 except when $\zeta = \zeta_0$. It may be written in the form

$$- \sum_{m=0}^{\infty} \frac{1}{2\pi i} \int_C \frac{e^{-(\mu + m\zeta_0/\zeta)u} du}{(1-u)^{m+1}}$$

where the contour $C$ encloses $u = 1$ and is such that $|\exp - u\zeta_0/\zeta| < |1-u|$ at every point on it. The curve $|1-u| = \nu |\exp - u\zeta_0/\zeta|$ satisfies this condition and has as one of its branches a closed loop containing $u = 1$, and also $u = 0$, provided that

$$1 < \nu < \zeta/\zeta_0 \cdot \exp (\zeta_0/\zeta - 1)$$

so $C$ is chosen to be this loop. The series therefore has the sum

$$\frac{1}{2\pi i} \int_C \frac{e^{-\mu u} du}{u - 1 + e^{-u\zeta_0/\zeta}}.$$

The integrand has a simple pole inside the contour at which the residue is $1/(1 - \zeta_0/\zeta)$ and some consideration will show that there are no other singularities within $C$. Consequently the sum of the series is $1/(1 - \zeta_0/\zeta)$ when $\zeta > \zeta_0$, which is the required result.

# Discrete limiting form of $T_{n,m,r}$

21. The corresponding discrete limiting form of

$$T_{n,m,r} = \frac{(n-r)!}{(m-r)!(n-m)!} (\kappa b_m)^{n-m} (1 - \kappa b_m)^{m-r} \quad (0 \leqslant \kappa < 1/b_r),$$

This content downloaded from 179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC All use subject to https://about.jstor.org/terms

---

428

H. E. Daniels

is appropriate when $n$, $m$ and $r$ are all large, but $m - r$ is $O(1)$. Retaining the notation of the previous sections, we expand $a(z/\zeta)$ near $x$ as

$$a(z/\zeta) = a(x/\zeta) + \frac{(z-x)}{\zeta}a'(x/\zeta) + O(z-x)^2$$

i.e. $$b_m = b_r \left[ 1 - \frac{(m-r)}{n} \frac{\zeta_x}{\zeta} \right] + O(n^{-2}) \tag{21·1}$$

where $\zeta_x = -\frac{a'(x/\zeta)}{a(x/\zeta)}$, and $1/\zeta_x$ is the subtangent to the $a(w)$ curve at $w = x/\zeta$. The important values of $\kappa$ are near its maximum $1/b_r$ and accordingly we write

$$\kappa = \frac{1}{b_r} \left( 1 - \frac{\mu}{n} \right)$$

or in terms of $\lambda = \kappa(1'-x)$, $$\lambda = \lambda_x \left( 1 - \frac{\mu}{n} \right). \tag{21·2}$$

Then $$(n-m) \log \kappa b_m = -\frac{(n-m)}{n} [\mu + (m-r)\zeta_x/\zeta] + O(n^{-1})$$

$$= -(1-x)[\mu + (m-r)\zeta_x/\zeta] + O(n^{-1}),$$

$$1 - \kappa b_m = \frac{1}{n} [\mu + (m-r)\zeta_x/\zeta] + O(n^{-2})$$

and $T_{n,m,r}$ reduces to

$$T_{n,m,r} = \frac{(1-x)^{m-r} [\mu + (m-r)\zeta_x/\zeta]^{m-r}}{(m-r)!} e^{-(1-x)(\mu + (m-r)\zeta_x/\zeta)} [1 + O(n^{-1})]. \tag{21·3}$$

It follows immediately from (20·4) that, to $O(n^{-1})$,

$$\sum_{m=r}^{\infty} T_{n,m,r} = \frac{1}{1 - \frac{(1-x)\zeta_x}{\zeta}} = \frac{1}{1 + \frac{(1-x)a'(x/\zeta)}{\zeta} \frac{a(x/\zeta)}{a(x/\zeta)}}, \tag{21·4}$$

provided that the denominator is not small, or in other words, that $x$ is not near a critical point.

Limiting form of $Q_{n,m}$ for large $n$

22. One can now examine the asymptotic behaviour of $Q_{n,m}$ and ultimately that of $B_n = Q_{n,0}$ by means of the identity (13·5), viz.

$$\sum_{m=r}^{n} Q_{n,m} \frac{(n-r)! (\kappa b_m)^{n-m} (1 - \kappa b_m)^{m-r}}{(m-r)! (n-m)!} \equiv 1 \tag{13·5}$$

$$0 \leqslant r \leqslant n, \quad 0 \leqslant \kappa \leqslant \frac{1}{b_n}.$$

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

*The statistical theory of the strength of bundles of threads*

429

The limiting form of (13·5) depends on the situation of the roots of

$$1 - z - \lambda a(z/\zeta) = 0$$

which lie in the range $x \leqslant z \leqslant 1$, where, as defined above,

$$\lambda = \kappa(1 - x), \quad 0 \leqslant \lambda \leqslant \lambda_x = (1 - x)/a(x/\zeta).$$

The discussion is first confined to what we call the 'non-critical' regions where $z$ is not near a critical point. Suppose, for simplicity, that the $a(w)$ curve is of the type shown in figure 7 having at most 3 positive real roots. As before, $\lambda_c$ denotes the critical value of $\lambda$ at which the two largest roots $z_2, z_3$ coincide at $z_c$ for fixed $\zeta$, the smallest root then being $z_c$.

FIGURE 7

Consider what happens as $x$ changes from 1 to 0, $\zeta$ being fixed, confining attention to the non-critical regions.

(i) $z_c < x < 1$. When $x$ is in this range there is only one root $z_3$ in $x \leqslant z \leqslant 1$ and if neither $z_3 - x$ nor $1 - z_3$ are small, (16·1) may be substituted in (13·5) to give

$$\int_{-\infty}^{\infty} Q_n(z) \, dz \sqrt{\left( \frac{n(1-x)}{2\pi(z_3-x)(1-z_3)} \right)} \times \exp \left[ -\frac{n(1-x)\left[1 + \frac{\lambda}{\zeta} a'(z_3/\zeta)\right]^2 (z-z_3)^2}{2(z_3-x)(1-z_3)} \right] [1 + A(z-z_3) + Bn(z-z_3)^3] = 1 + O(n^{-1}) \quad (22\cdot1)$$

where $Q_n(z)$ is written for $Q_{n,m}$.

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

430

H. E. Daniels

On the other hand, when $z_3 - x$ is small so that $m - r = O(1)$ and $\lambda = \lambda_x\left(1 - \frac{\mu}{n}\right)$ with $\mu = O(1)$ the appropriate limiting form is, from (21·3),

$$\sum_{m=r}^{\infty} Q_{n,m} \frac{[(1-x)(\mu+(m-r)\zeta_x/\zeta)]^{m-n}}{(m-r)!} e^{-(1-x)(\mu+(m-r)\zeta_x/\zeta)} = 1 + O(n^{-1}) \tag{22·2}$$

where $\zeta_x = -a'(x/\zeta)/a(x/\zeta)$.

It is now proved that when $z_c < z < 1$ and $z - z_c = O(1)$,

$$Q_n(z) = \left\{1 + \frac{(1-z)a'(z/\zeta)}{\zeta a(z/\zeta)}\right\} (1 + O(n^{-1})). \tag{22·3}$$

The values $\mu = 0$ and $\mu = \zeta_x/\zeta$ in (22·2) give respectively

$$\sum_{m=r}^{\infty} Q_{n,m} \frac{[(1-x)(m-r)\zeta_x/\zeta]^{m-r}}{(m-r)!} e^{-(1-x)(m-r)\zeta_x/\zeta} = 1 + O(n^{-1}),$$

$$\sum_{m=r}^{\infty} Q_{n,m} \frac{[(1-x)(m-r+1)\zeta_x/\zeta]^{m-r}}{(m-r)!} e^{-(1-x)(m-r+1)\zeta_x/\zeta} = 1 + O(n^{-1}).$$

Writing $r + 1$ for $r$ and multiplying through by $(1-x)\zeta_x/\zeta$ the latter becomes

$$\sum_{m=r+1}^{\infty} Q_{n,m} \frac{[(1-x)(m-r)\zeta_x/\zeta]^{m-r}}{(m-r)!} e^{-(1-x)(m-r)\zeta_x/\zeta} = (1-x)\zeta_x/\zeta(1 + O(n^{-1}))$$

whence, on subtraction,

$$Q_{n,r} = Q_n(x) = \{1 - (1-x)\zeta_x/\zeta\}(1 + O(n^{-1}))$$

which is equivalent to (22·3). The proof can be made rigorous by inserting the approximation factor $\exp A(m-r)^2/n$ in place of $1 + O(n^{-1})$ and confining the summation to the range in which this factor does not begin to dominate, the remainder being demonstrably negligible.

The same expression for $Q_n(z)$ is seen to satisfy (22·1), as it should, for then, to $O(n^{-1})$,

$$Q_n(z_3) = 1 + \frac{(1-z_3)}{\zeta} \frac{a'(z_3/\zeta)}{a(z_3/\zeta)} = 1 + \frac{\lambda}{\zeta} a'(z_3/\zeta)$$

and expanding $Q_n(z)$ in (22·1) as $Q_n(z_3) + Q_n'(z_3)(z - z_3) + O(z - z_3)^2$, the first term integrates to 1, the odd powers of $z - z_3$ vanish on integration, and $O(z - z_3)^2 = O(n^{-1})$ in the effective range of $z - z_3$.

It also follows that over the important range of $m$ in (22·2), $Q_{n,m}$ differs from $Q_n(x)$ only by $O(n^{-1})$ and on substituting this value for $Q_{n,m}$ the result (21·4) is verified.

(ii) $z_c' < x < z_c$. Avoiding for the present the critical region near $z_c$, we next discuss the range between $z_c'$ and $z_c$. There are two cases typified by the values $x'$ and $x''$ in figure 7, both corresponding to $\lambda = \lambda_x$ as shown.

This content downloaded from

179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC

All use subject to https://about.jstor.org/terms

---

The statistical theory of the strength of bundles of threads

431

Consider first the case of $x'$. When $\lambda < \lambda_x$ the only root greater than $x'$ is $z_3$, which is also greater than $x$, and (22·1) holds with $x'$ for $x$. On making $\lambda = \lambda_x$, however, the roots are $x'$ and $x$, and (13·5) becomes

$$\begin{array}{l} Q_{n,r'} T_{n,r',r'} + Q_{n,r'+1} T_{n,r'+1,r'} + \dots + \int_{-\infty}^{\infty} Q_n(z) \, dz \sqrt{\left(\frac{n(1-x')}{2\pi(x-x')(1-x)}\right)} \\ \quad \times \exp\left[-\frac{n(1-x')\left[1+\frac{\lambda_x}{\zeta}a'(x/\zeta)\right]^2(z-x)^2}{2(x-x')(1-x)}\right] [1+A(z-x)+Bn(z-x)^3] \\ = 1+O(n^{-1}), \end{array} \tag{22·4}$$

where $\frac{r'}{n} = x'$, and it is sufficient to note that $T_{n,r',r'} = 1+O(n^{-1})$.

The integral reduces to $1+O(n^{-1})$ by virtue of (22·3), and so

$$Q_{n,r'} = Q_n(x') = O(n^{-1}). \tag{22·5}$$

In the case of $x''$, when we make $\lambda = \lambda_x$ there are three roots at $x''$, $x'$ and $x$; then (13·5) takes a form similar to (22·4) but with $r''$ for $r'$, and two integrals in the neighbourhoods of $x'$ and $x$ respectively. The first integral vanishes by (22·5), the second is $1+O(n^{-1})$, and as before $Q_{n,r'} = Q_n(x'') = O(n^{-1})$.

When $x''-x'$ is small the discussion is a little more elaborate but the same result is true. Hence for any value of $z$ in the non-critical region between $z_{c'}$ and $z_c$,

$$Q_n(z) = O(n^{-1}). \tag{22·6}$$

(iii) $0 \leqslant x < z_{c'}$. As $x''$ passes through the value $z_{c'}$ into the range $0 \leqslant x'' < z_{c'}$, the other roots $x'$, $x$ for $\lambda = \lambda_x$ coalesce and become complex, so by the previous argument $Q_n(z)$ again satisfies (22·3).

The conclusions are therefore summarized as follows. Let $a(w)$ be such that $1-z-\lambda a(z/\zeta) = 0$ has at most 3 positive real roots, and let $\zeta$ be chosen so that when $z_2$ and $z_3$ are made to coalesce at $z_c$ for suitable $\lambda = \lambda_c$ the smallest root $z_1$ has a value $z_{c'} > 0$. Then the approximate form of $Q_n(z)$ in the non-critical regions of $z$ is

$$\begin{array}{l} Q_n(z) = \left\{1 + \frac{(1-z)a'(z/\zeta)}{\zeta a(z/\zeta)}\right\}(1+O(n^{-1})) \quad \text{in } z_c < z < 1, \\ = O(n^{-1}) \quad \text{in } z_{c'} < z < z_c, \\ = \left\{1 + \frac{(1-z)a'(z/\zeta)}{\zeta a(z/\zeta)}\right\}(1+O(n^{-1})) \quad \text{in } 0 \leqslant z < z_{c'}. \end{array} \tag{22·7}$$

By varying $\zeta$ the range $z_{c'} < z < z_c$ may be made to vanish or to include $z = 0$ but in all cases (22·6) holds throughout any part of this range, and (22·3) otherwise (excluding values of $z$ near $z_c$ or $z_{c'}$). The argument can evidently be extended to forms of $a(w)$ where the maximum number of roots is greater than 3.

23. The result just obtained has an immediate application to $B_n = Q_{n,0}$. Let $\lambda = 1$ so that the lowest root $z_1 = 0$ and allow $\zeta$ to vary, the critical value $\zeta_r$ corresponding to the double root $z_r$. Suppose $a(w)$ to have the form shown in figure 8.

This content downloaded from

179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC

All use subject to https://about.jstor.org/terms

---

432

H. E. Daniels

The remaining non-zero roots $z_2$, $z_3$ are real or complex according as $\zeta < \zeta_r$ or $\zeta > \zeta_r$. Putting $z = 0$, $a(0) = 1$, $a'(0) = -\zeta_0$ in (22·7), it can therefore be stated that

$$\begin{array}{l} B_n = Q_{n,0} = O(n^{-1}) \quad \text{when} \quad \zeta < \zeta_r, \\ B_n = (1 - \zeta_0/\zeta)(1 + O(n^{-1})) \quad \text{when} \quad \zeta > \zeta_r, \end{array} \tag{23·1}$$

provided

$$|\zeta - \zeta_r| = O(1).$$

Figure 9 illustrates the special case when $\zeta_r = \zeta_0$ and there is only one non-zero root.

The fact that $B_n \sim 1 - \zeta_0/\zeta$ when $\zeta > \zeta_r$ is perhaps not unexpected in view of the similar exact expression for $B_n$ (12·2) which holds for a form of $a(w)$ to which the present more general case approximates near $w = 0$. But the result (23·1) sheds an interesting light on the argument and conclusions reached about large bundles in the early part of the paper (§§ 4, 5, 6). It was deduced there that all very large bundles of a given size $n$ would break at loads approximating to $n\zeta_r$ in the present notation, provided that a unique value of $\zeta_r$ exists. Evidently this is not the whole truth of the matter. If the chance $1 - b(s)$ of a thread exceeding $s$ in strength tends to zero at a rate proportional to $1/s$, then, however large the bundle may be, its strength $S = n\zeta$ can take values ranging from $n\zeta_r$ to $\infty$ with probabilities according to (23·1). In such cases (23·1) provides all the information necessary about $B_n$ for large $n$, since the small excluded region near $\zeta_r$ is negligible compared with the wide range over which $B_n$ varies slowly with $\zeta$. In practice, however, it is generally found that $1 - b(s)$ tends to zero more rapidly than $1/s$ so that $\zeta_0 = 0$, and (23·1) then gives no information about $B_n$ in the region where it differs appreciably from 0 or 1.

24. Finally the behaviour of $Q_{n,m}$ in the critical region is discussed. Keeping $\lambda = 1$, $z_1 = 0$, let $\zeta$ now approach $\zeta_r$. The two largest roots $z_2$, $z_3$ come into the vicinity of $z_r$, and on substituting (18·7) and (20·2) the appropriate limiting form of (13·5) is found to be

$$\sum_{m=0}^{\infty} Q_{n,m} \frac{(m\zeta_0/\zeta)^m}{m!} e^{-m\zeta_0/\zeta} + \int_{-\infty}^{\infty} Q_n(z) \, dz \sqrt{\left(\frac{n}{2\pi z_r(1 - z_r)}\right)} \times \exp\left\{-\frac{n}{2z_r(1 - z_r)}\left[\frac{a''}{2\zeta_r^2}(z - z_r)^2 + \frac{z_r}{\zeta_r}(\zeta - \zeta_r)\right]^2\right\} = 1 + O(n^{-\frac{1}{2}}) \tag{24·1}$$

where

$$\zeta - \zeta_r = O(n^{-\frac{1}{2}}).$$

The most commonly occurring type of thread population has $\zeta_0 = 0$ and (24·1) then reduces to

$$\begin{array}{l} B_n = Q_{n,0} = 1 - \int_{-\infty}^{\infty} Q_n(z) \, dz \sqrt{\left(\frac{n}{2\pi z_r(1 - z_r)}\right)} \\ \quad \times \exp\left\{-\frac{n}{2z_r(1 - z_r)}\left[\frac{a''}{2\zeta_r^2}(z - z_r)^2 + \frac{z_r}{\zeta_r}(\zeta - \zeta_r)\right]^2\right\} = 1 + O(n^{-\frac{1}{2}}). \tag{24·2} \end{array}$$

When $\zeta_0 \neq 0$ it can be shown by an argument similar to that used to prove (22·3) that the effect is to multiply the right-hand side of this equation by a factor $1 - \zeta_0/\zeta$.

This content downloaded from

179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC

All use subject to https://about.jstor.org/terms

---

*The statistical theory of the strength of bundles of threads*

433

The behaviour of $B_n$ for values of $\zeta$ satisfying $\zeta - \zeta_r = O(n^{-\frac{1}{2}})$ is thus seen to depend on that of $Q_n(z)$ over a range of $z$ such that $z - z_r = O(n^{-\frac{1}{2}})$. Therefore consider

FIGURE 8

FIGURE 9

the limiting form of (13·5) when $x$ is in the critical region and $z_3 - z_2 = O(n^{-\frac{1}{2}})$. It is more convenient for the moment to work in terms of $z_e$. Suppose first that $z_e < x$, and now make use of the result (19·2) that near $z_3$, $T_n(z, x)$ take the form appropriate

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

434

H. E. Daniels

to an isolated simple root, but to the order $O(n^{-1})$ only. Since $z_3$ is the only root in $x < z < 1$, (13·5) becomes

$$\int_{-\infty}^{\infty} Q_n(z) \, dz \sqrt{\left(\frac{n}{2\pi(z_3 - x)}\right)} \exp\left[-\frac{n\lambda_c^2 a_c''^2}{2\zeta^4} \frac{(z_3 - z_c)^2}{(z_3 - x)} (z - z_3)^2\right] \times [1 + A n^1 (z - z_3) + B n (z - z_3)^3] = 1 + O(n^{-1}) \quad (24\cdot3)$$

and this is satisfied by $Q_n(z) = \frac{\lambda_c a_c''}{\zeta^2} (z - z_c) [1 + O(n^{-1})]$ (24·4)

which is the same as (22·3) to $O(n^{-1})$. Such an argument does not establish (24·4) as the unique solution of (24·3), but it is possible to construct a direct rigorous proof on the lines of § 22 (i), though the details are tedious.

By taking $x < z_c$, $z_c - x = O(n^{-1})$, the behaviour of $Q_n(z)$ when $z < z_c$, $z_c - z = O(n^{-1})$ may be studied by a similar extension of § 22 (ii), and it is found that

$$Q_n(z) = O(n^{-1}) \tag{24\cdot5}$$

where $z < z_c$, $z_c - z = O(n^{-1})$.

The asymptotic form of $B_n$

25. Applying these formulae to (24·2) one writes to $O(n^{-1})$

$$\lambda_c = 1, \quad z_c = z_\tau, \quad \lambda_c a_c'' / \zeta^2 = a_\tau'' / \zeta_\tau^2.$$

The contribution to the integral in (24·2) from points in a range of $z - z_\tau$ smaller than $O(n^{-1})$ can be shown to be negligible to $O(n^{-1})$ and it is concluded that

$$B_n = 1 - \int_0^\infty \frac{a_\tau''}{\zeta_\tau^2} (z - z_\tau) \, dz \sqrt{\left(\frac{n}{2\pi z_\tau (1 - z_\tau)}\right)} \times \exp\left\{-\frac{n}{2z_\tau (1 - z_\tau)} \left[\frac{a_\tau''}{2\zeta_\tau^2} (z - z_\tau)^2 + \frac{z_\tau}{\zeta_\tau} (\zeta - \zeta_\tau)\right]^2 + O(n^{-1})\right\}$$

which reduces on setting

$$\frac{z_\tau}{\zeta_\tau} y = \frac{a_\tau''}{2\zeta_\tau^2} (z - z_\tau)^2 + \frac{z_\tau}{\zeta_\tau} (\zeta - \zeta_\tau)$$

to $B_n = \int_{-\infty}^{\zeta - \zeta_\tau} \frac{dy}{\zeta_\tau} \sqrt{\left(\frac{nz_\tau}{2\pi(1 - z_\tau)}\right)} \exp\left[-\frac{nz_\tau y^2}{2\zeta_\tau^2(1 - z_\tau)}\right] + O(n^{-1}). \quad (25\cdot1)$

That is, the probability distribution of $\zeta$ tends to the normal form for large $n$ with expectation $\zeta_\tau$ and standard deviation

$$\sigma = \zeta_\tau \sqrt{\left(\frac{1 - z_\tau}{n z_\tau}\right)} = \zeta_\tau \sqrt{\left(\frac{a_\tau}{n(1 - a_\tau)}\right)}.$$

When $\zeta_0$ is not zero the formula for $B_n$ is simply multiplied by $1 - \zeta/\zeta_0$.

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms

---

*The statistical theory of the strength of bundles of threads* 435

The final result restated in terms of the earlier notation is therefore as follows. If all threads have the same load-extension curve, and the chance $b(s)$ of a thread breaking under load $s$ is such that $1 - b(s)$ tends to zero faster than $1/s$, then the strength $S$ of a bundle of $n$ threads has a probability distribution which tends for large $n$ to the normal form with expectation

$$S_{\tau} = n s_{\tau} [1 - b(s_{\tau})]$$

and standard deviation $\sigma = s_{\tau} \sqrt{\{n b(s_{\tau}) [1 - b(s_{\tau})]\}}$,

where $s_{\tau}$ gives $s[1 - b(s)]$ its greatest value.

It is worth remarking that the same result would follow at once if one could assume that for sufficiently large $n$ the probability distribution of breaking extension is independent of that of the number of threads surviving up to the point of rupture, the probability of this number being then distributed according to a simple binomial law. Subsequent work on breaking extension suggests that the assumption is in fact true, but there seems to be no *a priori* justification for it.

Note also that I have assumed the dispersion of $\alpha$ to be negligible compared to that of $\zeta$, but when $n$ is large it may become of comparable order, in which case the formulae are not strictly valid.

Part II of this paper will contain a generalization to threads having varying load-extension curves, a discussion of the probability distribution of extension at break, and a further investigation into the asymptotic form of $B_n$ by a more powerful saddle-point method based on the special properties of $B_n$ when $b(s) = e^{-s/s}$.

My thanks are due to the Director and Council of the Wool Industries Research Association for permission to publish this work.

# REFERENCES

Peirce, F. T. 1926 *J. Textile Inst.* **17**, T. 355. (See also preceding papers of the series, with O. Midgley.)
Weibull, W. 1939 *IngenVetenskAkad. Handl.* no. 153 (in English.)

This content downloaded from
179.160.38.86 on Thu, 03 Sep 2026 14:48:32 UTC
All use subject to https://about.jstor.org/terms
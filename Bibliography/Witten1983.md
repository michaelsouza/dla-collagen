PHYSICAL REVIEW B
VOLUME 27, NUMBER 9
1 MAY 1983

# Diffusion-limited aggregation

T. A. Witten
Exxon Research and Engineering Company, Linden, New Jersey 07036

L. M. Sander
Physics Department, University of Michigan, Ann Arbor, Michigan 48109
(Received 19 November 1982)

Diffusion-limited aggregation (DLA) is an idealization of the process by which matter irreversibly combines to form dust, soot, dendrites, and other random objects in the case where the rate-limiting step is diffusion of matter to the aggregate. We study the process from several points of view stressing the fact that it apparently gives rise to scale-invariant objects whose Hausdorff dimension is independent of short-range details. We show that DLA has no upper critical dimension. We apply scale invariance to study growth, gelation, and the structure factor of aggregates.

# I. INTRODUCTION

The irreversible aggregation of small particles to form clusters is a central problem in many fields of applied science; examples are colloids¹ and coagulated aerosols.² The rate-limiting step in aggregation is often the diffusion of the particles to the surface of the aggregate. Similar growth processes occur when a chemical species precipitates from a supersaturated matrix or when crystals grow from a supercooled melt.³ In these cases diffusion of the species toward the surface (or heat away from it) can be the rate-limiting process. The aggregates formed in all of these cases have extremely complicated multibranched forms familiar in the case of dust balls, agglomerated soot, and dendrites. The complicated shapes have been associated with the proliferation of instabilities induced by the diffusion-limited process³ (cf. Sec. II).

In a previous publication⁴ the authors considered a lattice model which simulates such diffusion-limited aggregation (DLA). This paper contains a further exploration of the consequences of the model. The rules of the model are quite simple: We start with a seed particle at the origin of a lattice. Another particle is allowed to walk at random (i.e., diffuse) from far away until it arrives at one of the lattice sites adjacent to the occupied site. Then it is stopped; another particle is launched and halted when adjacent to the two occupied sites, and so forth. An indefinitely large cluster may be formed in this way. A typical structure produced on a two-dimensional lattice is shown in Fig. 1. The model does, thus, produce complicated shapes qualitatively similar to real dendrites or dust.

A new, unexpected result was found⁴,⁵ by direct measurement of an ensemble of such two-dimensional aggregates: The correlations that arose between particle positions seem to be those typical of a scale-invariant (or dilation-symmetric) object. That is, when viewed with a resolution coarser than the size of the aggregating particles the object has no natural length scale. The density-density correlation function for such an object obeys the following:

$$
\left\langle \rho \left(r ^ {\prime} + r\right) \rho \left(r ^ {\prime}\right) \right\rangle \sim r ^ {- A}. \tag {1}
$$

The exponent $A$ is related to the Hausdorff dimension $^6$ $D$ which characterizes the object by $D = d - A$. (See Sec. II below.) In two dimensions, $D$ was found to be 1.7. Since our original work the results have been confirmed and extended to higher dimensions by Meakin⁷; he also finds evidence for scale invariance.

Scale invariance is most familiar in the context of critical phenomena⁸ where the divergence of the correlation length leads to universality (independence of microscopic length scales and interactions) and correlation functions which have the form of Eq. (1). This symmetry is understood in terms of the "renormalizability" of the Hamiltonian governing the statistical mechanics. In this context renormalization⁸ is the process of multiplying certain fields in the theory by the scale factors necessary to render the correlation functions finite when microscopic length scales go to zero. The scale factors contain the information about the Hausdorff dimension of the object in question. A powerful technique in such studies is the investigation of the dependence

©1983 The American Physical Society

---

DIFFUSION-LIMITED AGGREGATION

![img-0.jpeg](img-0.jpeg)

![img-1.jpeg](img-1.jpeg)

![img-2.jpeg](img-2.jpeg)
FIG. 1. (a) Aggregate of 3000 particles on a square lattice. (b) Screening effect: The first 1500 particles to attach to the aggregate are open circles, the rest are dots. (c) Fragments of the same aggregate chosen at random.

of  $D$  on spatial dimensionality  $d$ ; in commonly studied systems  $D$  is simply derivable by dimensional analysis above a certain upper critical dimension  $d_{c}$ . For dimensions lower than  $d_{c}$  expansions about  $d_{c}$

are often used.

The concepts of upper critical dimension and renormalizability apply to the best-known random density profiles: self-avoiding random walks and random lattice animals. These are qualitatively similar to DLA clusters and percolation clusters. However, there is a fundamental difference, which we discuss in Sec. III. The random walks and lattice animals form an equilibrium ensemble; DLA is defined kinetically.

Kinetic models have been much less thoroughly studied than equilibrium ones. A model similar to ours (that of Eden, $^{12}$  see Sec. II below) has been proposed in the context of biology. However, the Eden clusters appear $^{13}$  to lack the anomalous scale invariance of DLA. Other kinetic processes have been proposed which are similar to DLA (Ref. 14) though the spatial structure of the objects produced has not been the focus of the studies.

In this paper we study the DLA model and its dilation symmetry and illustrate certain aspects which make it possibly important both theoretically and practically. We have been guided in our research by the successes of the equilibrium theories mentioned above. The paper is organized as follows: In the next section we review the origin of the randomness of the aggregates as it arises from the proliferation of instabilities of the Mullins-Sekerka type. The numerical evidence for scale invariance for  $d = 2$  aggregates is discussed; some elements of universality are demonstrated by relaxing the constraint that the aggregate absorb perfectly.

In Sec. III we give equations for the time development of the density  $\rho(r)$ . We find that DLA has no upper critical dimension in the ordinary sense. (The same line of reasoning shows that Eden clusters have  $D = d$  for any  $d$ .) These findings show that DLA is qualitatively different from known critical phenomena. We have been unable to show why DLA is dilation symmetric. To show this will require a generalization of renormalization theory yet to be developed.

In Sec. IV we turn to a discussion of some consequences of the dilation symmetry. We study the growth rate of aggregates, the gelation of a collection of aggregates, the dependence of the scattering structure factor on  $D$ , and the relation of the density profile, its projection, and its cross section to  $D$ . Section V contains a summary of our conclusions.

# II. SCALE INVARIANCE IN DLA

# A. Stability analysis

Diffusion is essential in producing the dilation symmetry observed in DLA. To see this, we consid-

---

T. A. WITTEN AND L. M. SANDER
27

er the analogous growth model without diffusion: the "growing animals" of Eden.¹² Here every perimeter site is equally likely to grow at each step. Eden clusters appear to fill a finite, nonzero fraction of space, i.e., $D = d$ (cf. Sec. III); they lack the multibranched structure of DLA. In DLA the exposed ends of the clusters grow more rapidly than the interior, because the random walkers are captured before they reach the interior.

To show in detail the origin of the complex structures such as those in Fig. 1, we first point out that in a certain limit an electrostatic analogy can be used. Consider a random walk which eventually adds to the aggregate. Let $u(\vec{x}, k)$ be the probability that the walk reaches site $\vec{x}$ at the $k$th step. As in any random walk $u$ obeys the following:

$$
u (\vec {x}, k + 1) = \frac {1}{c} \sum_ {\vec {1}} u (\vec {x} + \vec {1}, k), \tag {2a}
$$

where $\vec{1}$ runs over the $c$ neighbors of $\vec{x}$. This, of course, is a discrete version of the continuum diffusion equation

$$
\frac {\partial u}{\partial t} = \eta \nabla^ {2} u, \tag {2b}
$$

where $\eta$ is the diffusion constant. Also, since walks visiting perimeter sites terminate there we must set $u = 0$ on the right-hand side of (2a) for these sites and for cluster sites. The probability that a perimeter site gains a particle at $k + 1$ is, as above,

$$
v (\vec {x}, k + 1) = \frac {1}{c} \sum_ {\vec {1}} u (\vec {x} + \vec {1}, k). \tag {3a}
$$

In the limit of a smooth surface with unit normal $\hat{n}$ the normal growth velocity $V_{n}$ can be expressed as a gradient:

$$
V _ {n} = \eta \hat {n} \cdot \vec {\nabla} u \mid_ {s}. \tag {3b}
$$

Equations (2b) and (3b) are, of course, standard in studies of dendritic growth.³ In DLA the field $u$ far from the aggregate is such as to provide a steady total flux to the surface; this is another boundary condition on $u$.

Now consider the time dependence of $u$: With a steady flux from far away the only source of time dependence is in the boundary condition (3b) via the growth of the aggregate. In our simulations the growth is sufficiently slow that it is adequate to neglect $\partial u / \partial t$ in Eq. (2b), as we discuss in Sec. III.

We are faced, then, with solving Laplace's equation for $u$ in the presence of a boundary where $u = 0$ (effectively, a "conducting" surface). The growth rate $V_{n}$ of any region on the surface is proportional to the "electric field" (i.e., $\nabla u$) there. Now it is well known that electric fields are large near sharp points

on a conductor; thus sharp points grown unstably. In fact, our aggregates look qualitatively like structures (e.g., lightning) which occur due to electrical breakdown.¹⁵

A graphical illustration of this idea may be seen by considering the growth of a tower of spheres (see Fig. 2). If a small amount of material is added uniformly (as in the Eden model), then the conical envelope of the tower is unaffected (except near the tip). However, in diffusive aggregation the growth rate of each sphere is proportional to $1 / R$; thus the tower becomes steeper since the smaller spheres grow more rapidly.

Mullins and Sekerka³ treat this problem using a stability analysis for a slightly deformed sphere. We can do a similar analysis for $d = 2$; consider a disc whose radius is given by

$$
r = R + \delta_ {m} \cos (m \theta), \tag {4}
$$

where $\delta_{m}$ is small. Outside the disc $u$ is a solution to Laplace's equation:

$$
u = A \ln (r) + B + C _ {m} \cos (m \theta) / r ^ {m}. \tag {5}
$$

Using $u(r) = 0$ and Eq. (3b) gives at once

$$
d R / d t = A / R, \tag {6a}
$$

$$
d \delta_ {m} / d t = (m - 1) \delta_ {m} A / R ^ {2}, \tag {6b}
$$

$$
(\dot {\delta} / \delta) / (\dot {R} / R) = m - 1. \tag {6c}
$$

That is, all deformations for $m &gt; 1$ grow unstably and, from Eq. (6c), those for $m &gt; 2$ grow faster than the radius itself. Thus tiny amounts of noise will perturb a smooth surface irretrievably. A similar treatment works for three dimensions and higher. This wrinkling instability shows why DLA produces irregular, noncompact shapes.

![img-3.jpeg](img-3.jpeg)
(a)
FIG. 2. Growth of a tower of spheres according to (a) the Eden model and (b) DLA.

![img-4.jpeg](img-4.jpeg)
(b)

---

DIFFUSION-LIMITED AGGREGATION
5689

## B. Simulations of the model

Numerical simulations of the DLA process were first carried out in two dimensions and reported in Ref. 4. A plot of a typical aggregate is in Fig. 1(a). A few more details of the technique may be useful to mention here. At each stage of the computation it is necessary to launch particles at random, let them walk randomly, stop them when they arrive at a perimeter site, or to start them over when they wander away. For launching it is sufficient to start walkers on a small circle circumscribing the existing cluster. To catch errant particles we chose another circle twice the radius of the cluster.

The motivation for the location of the circles is as follows: We are trying to simulate the situation of isotropic flux very far from the aggregate. We expect that the field $u$ will be distorted from isotropy on scales of the order of the size of the aggregate. The inner circle can be close to the object because the first passage of particles from far away toward the object is isotropic$^{16}$; thereafter, to represent the situation without bias we must not stop particles until they are far away compared to the radius. We have performed simulations with the outer circle at $3\times$ the aggregate size. The results were the same except that they took more computer time.

A number of interesting features become evident in the course of examining the simulations. These are shown in Figs. 1(b) and 1(c). In Fig. 1(b) we distinguish the first half and second half of the particles added. The significant feature is that particles do not penetrate to the interior as they are added, but stick to the protruding "arms" even though the interior appears readily accessible to the exterior. The cluster effectively screens the flux of diffusing particles.

In Fig. 1(c) we show several small sections of the large figure positioned at random to illustrate that the clusters appear locally homogeneous and isotropic. The appearance of these pictures leads us to the hypothesis that the density correlations within a bounded region attain a well-defined limiting form for indefinitely large clusters, and that this form is invariant under translations and rotations. In this respect the density would be similar to the order parameter or energy field at a critical phase transition.

To test for scale invariance we use the techniques originally used by Forrest and Witten$^{5}$ to study the scale invariance of metallic smoke aggregates which seem to be a physical realization of DLA. The criterion for scale invariance that we use is that in a scale-invariant object all correlation functions are unchanged up to a constant under rescaling of lengths by an arbitrary factor $b$:

$$
\begin{array}{l}
\left\langle \rho \left(br_{1}\right) \rho \left(br_{2}\right) \cdots \rho \left(br_{k}\right) \right\rangle \\
\simeq b^{-A_{k}} \left\langle \rho \left(r_{1}\right) \rho \left(r_{2}\right) \cdots \rho \left(r_{k}\right) \right\rangle . \tag{7}
\end{array}
$$

In practice, we calculated only the two-point function $\langle \rho (r_1)\rho (r_2)\rangle$, whose exponent we call $A$ for short. Equation (7) leads at once to Eq. (1).

As a cross check we also measured the radius of gyration $R(N)$ as a function of the number of particles $N$. It is clear from Eq. (1) that

$$
N \sim \int^{R} \left\langle \rho (0) \rho (r) \right\rangle d^{d} r \sim R^{d - A} \sim R^{D}. \tag{8}
$$

Thus the Hausdorff dimension$^{6}$ is $d - A$.

To measure the density-density correlations within the aggregates, we computed the $c(r)$ defined by

$$
c(r) = \frac{1}{N} \sum_{\vec{r}^{\prime}} \rho (\vec{r} + \vec{r}^{\prime}) \rho (\vec{r}^{\prime}). \tag{9}
$$

The average of $c(r)$ over many clusters positioned at random is the correlation function of Eq. (1). We computed $c(r)$ is such a way as to maximize the information sampled from each image. We Fourier transformed the density profile of the cluster using a fast-Fourier-transform technique, found the power spectrum, inverted the transform, and averaged over directions and over narrow ranges (up to about 15% spread) of $r$. Often we used a matrix of densities which was not identical to the original cluster lattice: We overlaid the lattice with a coarser grid oriented at random and summed the cluster points within each cell of the coarse grid to form $\rho(r)$. This allowed us to treat larger clusters with a given sized matrix at the cost of some short-distance information. This method was calibrated by applying it to a Koch curve$^{6}$ with $D$ constructed to be $\ln 3 / \ln 2$. The $D$ value obtained from the measured correlation function was correct to within 0.01.

The average $c(r)$ of six aggregates on a square lattice is shown in Fig. 3. We note that the measured $c(r)$ falls below the power-law line when $r$ becomes comparable to the size of the aggregates; note the arrow which marks the average radius of gyration. The values of $D$ deduced for two-dimensional aggregates are displayed in Table I.

Our estimates of $D$ are in good agreement with those of Meakin$^{7}$ who used larger aggregates. The $D$ values are significantly different from those characteristic of equilibrium profiles, also displayed in Table I.

## C. Universality

One of the most striking features of the power-law behavior observed in critical phenomena is its

---

5690
T. A. WITTEN AND L. M. SANDER
27

![img-5.jpeg](img-5.jpeg)
FIG. 3. Density correlation function averaged over six aggregates as a function of distance measured in lattice constants. The arrow marks the average radius of gyration. The solid line is a least-squares fit over the range $r = 3 - 27$. The error bars represent the spread of values among the six aggregates.

universality, i.e., its independence of microscopic details of the Hamiltonian. Such behavior is not unexpected in a situation where statistical properties lead to the buildup of correlations on scales much larger than those of the microscopic interactions. This behavior should also occur in our case. In this section we will present evidence that $D$ is universal for DLA in several respects.

First, the long-range properties of our aggregates should be independent of the lattice on which we did the simulation. To check this we produced clusters on a triangular as well as a square lattice. An example is given in Fig. 4; the Hausdorff dimension for the aggregates on the triangular lattice, given in Table I, is not significantly different from those on a square lattice. Meakin$^7$ did very interesting simulations with no lattice at all; and again found the same $D$.

We were motivated to investigate a second aspect of universality by comparison with treatments of dendritic growth.$^{3,17}$ Our Eqs. (2b) and (3b) are the same as in those treatments, but our boundary condition $u|_{z} = 0$ is not, except in the case of vanishing surface tension. The radius of a real dendrite tip is determined by the capillary length $\Gamma$ via the Gibbs-Thomson boundary condition

$$
u \mid_ {z} = \Gamma K, \tag {10}
$$

TABLE I. Values of correlation exponent $A$ and Hausdorff dimension $D$ for particles in two dimensions. Errors are statistical.

|   | A | D  |
| --- | --- | --- |
|  DLA: correlation functions of aggregates on a square lattice; average of six clusters of 2079–3609 particles | 0.343±0.004 | 1.66  |
|  DLA: correlation functions on a triangular lattice; average of three clusters of 1500–2997 particles | 0.327±0.01 | 1.67  |
|  DLA: radius of gyration of six clusters of 999–3000 particles | 0.299 | 1.70±0.02  |
|  Self-avoiding walk in two dimensions from correlations in step density$^a$ | 0.667 | 1.33  |
|  Random animals, radius of gyration$^b$ |  | 1.54  |
|  Percolation$^c$ |  | 1.89  |

$^a$D. S. McKenzie, Phys. Rep. 27C, 37 (1976).
$^b$Reference 13.
$^c$D. Stauffer, Phys. Rep. 54, 1 (1979).

---

DIFFUSION-LIMITED AGGREGATION

5691

![img-6.jpeg](img-6.jpeg)
FIG. 4. Aggregate of 2500 particles on a triangular lattice.

where $K$ is the local curvature of the surface. Our perfectly absorbing clusters correspond to zero surface tension, and hence to a diffusing field which is constant over the surface. We first relaxed the condition of perfect absorption by allowing the randomly walking particle to stick to the aggregate only during a fraction $s$ of its encounters; previously, $s = 1$. This partial sticking introduces a length parameter into the diffusion equation.

To see this we work in one dimension, and write

$$
u (l, k + 1) = (1 - s) u (O, k) + \frac {1}{s} u (2 l, k), \tag {11a}
$$

$$
u (O, k + 1) = \frac {1}{s} u (l, k). \tag {11b}
$$

Here $O$ labels the perimeter site and $l,2l$, the free space. In steady state we may drop the $k$ label and manipulate Eqs. (11a) and (11b) to find

$$
s u (l) = u (2 l) - u (l), \tag {12a}
$$

or, in a continuum limit, as above,

$$
s u \mid_ {s} = l \hat {n} \cdot \vec {\nabla} u \mid_ {s}. \tag {12b}
$$

The fixed logarithmic derivative of $u$ at the surface introduces a new length scale,

$$
\lambda = l / s, \tag {13}
$$

which we may adjust at will. This new length plays the role of the capillary length in conventional treatments. Indeed, we can use our electrostatic analogy to reinterpret Eq. (12b). Consider a spherical surface; then if $\lambda \ll R$, $\nabla u|_s \sim u_\infty / R$ and to first order in $\lambda$ we may put

$$
u \mid_ {s} = u _ {\infty} \lambda / R, \tag {14}
$$

i.e., a condition of the form of Eq. (10).

To gain some appreciation of what Eq. (12b) implies we repeated the stability analysis with the new

![img-7.jpeg](img-7.jpeg)
FIG. 5. Aggregate of 3000 particles with $s = 0.5$. Note the thickening of the "branches."

boundary condition. We find, for $d = 2$ [compare Eq. (6)],

$$
d \delta_ {m} / d t = (m - 1) \delta_ {m} A / R (R + m \lambda), \tag {15a}
$$

$$
(\hat {\delta} / \delta) / (\dot {R} / R) = (m - 1) R / (R + m \lambda). \tag {15b}
$$

Note that for $\lambda &gt;&gt; R / m$, $d\delta / dt$ is suppressed compared to its value in Eq. (6). It does not change sign as in the usual dendritic growth case, but if $R &lt; \lambda$, for any $m$ the distortions will become smaller relative to $R$ as time proceeds instead of larger. Since the instability leading to DLA is quenched for $R &lt; \lambda$, we expect the DLA density profiles to be uniform over distances $R \leq \lambda$. For larger $R$, the instabilities are again present, and we expect the density profiles on this scale to be multibranched, like those of the simple DLA. The same conclusion holds in three dimensions.

Using these insights we created a number of aggregates with $s &lt; 1$. Plots of a cluster of this type are shown in Fig. 5, and its correlation functions are given in Fig. 6. The correlation function does have the form we hoped for: At small distances $c(r)$ is roughly constant and represents the thickening of the "branches" of the object; at large distances (but still smaller than the total size of the object) the power law is unchanged. The change in behavior from constant to power law occurs at a distance which increases as $s$ decreases, in accord with our prediction of crossover for $R \approx \lambda \sim 1 / s$.

We also did simulations with a more ad hoc type of boundary condition. We take a sticking probabil

---

5692
T. A. WITTEN AND L. M. SANDER
27

![img-8.jpeg](img-8.jpeg)
FIG. 6. Correlation function for the aggregate of Fig. 5.

ity which depends on the number of bonds to filled neighbor sites $B$; for a square lattice we put

$$
s = t ^ {3 - B}, \tag {16}
$$

where $t$ is an adjustable parameter less than 1. Thus a hole (with $B = 3$) is far more likely to fill than a point (with $B = 1$).

A simulation for $t = 0.5$ is shown in Fig. 7, and correlation functions for several values of $t$ in Fig. 8. Once more, small $t$ introduces a minimum length scale for the object, but the long-range properties seem to be unaltered.

The simulations of Meakin$^{7}$ in higher dimensions seem to bear out our hypothesis of scale invariance. For $d = 3$ he finds $D = 2.51 \pm 0.06$ by examining only the radius of gyration. We have presented$^{18}$ data for $c(r)$ in $d = 3$, which is in agreement with Ref. 7.

## III. GENERAL FORMULATION

The computer simulations described above, if repeated for all possible random walks, would generate a statistical ensemble of clusters. In this section we formulate equations for the time development of this ensemble. We argue that these equations may be simplified considerably without affecting the

![img-9.jpeg](img-9.jpeg)
FIG. 7. Aggregate of 3000 particles with $t = 0.5$.

large-scale properties of large aggregates.

We may describe any given cluster $\underline{i}$ on a lattice by a density field $[\rho(x)]$ which is 1 at an occupied site and zero elsewhere. Aggregation processes generate a large class of clusters $\underline{i}$, each with a relative probability $f_{\underline{i}}$. Thus, e.g., in the ensemble of "random animals," any connected pattern of 1's has $f_{\underline{i}} = 1$; any disconnected pattern has $f_{\underline{i}} = 0$. In the DLA model the $f_{\underline{i}}$ for a given cluster cannot be expressed directly in terms of the $\rho$ field. One must

![img-10.jpeg](img-10.jpeg)
FIG. 8. Correlation functions for three aggregates with $t &lt; 1$.

---

DIFFUSION-LIMITED AGGREGATION
5693

also know the $f_{\underline{i}}$ for other clusters; it does not belong to an equilibrium ensemble like that of the random animals. The $f_{\underline{i}}$ are determined instead by a time-development equation.

We consider the time derivative $\frac{\partial f_{\underline{i}}}{\partial t}$ for a particular cluster $\underline{i}$. In a given instance the cluster $\underline{i}$ is produced by the growth of some other cluster, $\underline{i} - x$, equal to $\underline{i}$ but for the absence of the site at $\vec{x}$. The growth of $\underline{i}$ from $\underline{i} - x$ occurs with an average rate which we denote $v_{\underline{i} - x}(\vec{x})$. The (positive) contribution to $f_{\underline{i}}$ from these growth processes is

$$
\sum_{x \in \underline{i}} v_{\underline{i} - x}(\vec{x}) f_{\underline{i} - x}. \tag{17}
$$

The cluster $\underline{i}$ also disappears from the ensemble at a certain rate, as larger clusters grow from it. The clusters thus produced have one particle added at some site $\vec{x}$, and we denote them as $\underline{i} + x$. Combining the processes which increase and which reduce $f_{\underline{i}}$, we have

$$
\frac{\partial f_{i}}{\partial t} = \sum_{x \in \underline{i}} v_{\underline{i} - x}(\vec{x}) f_{\underline{i} - x} - \left\{ \sum_{x \in \partial \underline{i}} v_{\underline{i}}(\vec{x}) \right\} f_{\underline{i}}, \tag{18}
$$

where we have used $\partial \underline{i}$ to denote the sites on the perimeter of $\underline{i}$. By contrast, a thermal equilibrium ensemble with temperature $\beta^{-1}$ and energy $E_{i}$ has $\partial f_{i} / \partial \beta = E_{i}f_{i}$; there is no coupling of different $f_{i}$.

Other growth models are governed by time-development equations of the form of Eq. (18). For the Eden model, $^{12}$ the $v$ factor is taken independent of $\underline{i}$ and $x$, so that all perimeter sites grow at the same rate.

The distinctive feature of diffusive growth is that the growth rate $v$ is the flux of a diffusing field $u$, as discussed in Sec. II above: the effect of the absorbing cluster on the diffusing field $u$ may be expressed by a boundary condition at the cluster surface. Instead, we allow the field $u$ to occupy any site, but introduce a strong absorption at perimeter sites. Such a site $x$ is indicated by the function

$$
P(\vec{x}) = \left[ 1 - \rho(\vec{x}) \right] \left[ 1 - \prod_{\vec{1}} \left[ 1 - \rho(\vec{x} + \vec{1}) \right] \right], \tag{19}
$$

which is 1 for perimeter sites and 0 elsewhere. Thus the diffusion equation for $u$ may be written

$$
\frac{\partial u}{\partial t} = \eta \nabla^{2} u - \mathcal{Z} u(\vec{x}) P(\vec{x}). \tag{20}
$$

Evidently, in the limit of large $Z$ the perimeter sites become an absorbing boundary, where $u \to 0$. For any $Z$ the local rate of absorption $Zu(\vec{x})$ is also the average rate $v(\vec{x})$ of cluster growth there.

The equations for $u$ and $f_{i}$ determine the probability of a given cluster as a function of time given suitable boundary conditions. The equation for $f_{i}$ requires an initial condition, e.g., $f_{i} = 0$ at $t = 0$, except for $f_{i} = 1$ for the single particle at the origin. The equation for $u$ requires a boundary condition such as $u = 1$ for $R = R_{m}$ where $R_{m}$ is a large radius.

The equation for $u$ may be simplified by recalling that $\partial u / \partial t$ does not play a crucial role. The field $u$ changes most rapidly with time near a point $x$ where a site has just grown. The effect of the new absorbers is appreciable over distances $r$ of the order of the lattice spacing—an arbitrarily small fraction of the growing sites. Thus the $u$ field relaxes everywhere to its new steady-state value in a time independent of the cluster size. Within this time, only a small amount of new growth occurs and only a negligible part of this lies in the region around $x$ where the time dependence is appreciable. $^{3,4}$ When the growth rate per surface site is negligible compared to the diffusive relaxation time, the time dependence of the relaxation may be neglected. This amounts to neglecting the $\partial u / \partial t$ term. Without this term, the $u$ field relaxes instantly to the cluster which exists at that time. We shall adopt this "adiabatic" approximation in the sequel so that $v$ and $u$ depend on the cluster, but not otherwise on time.

We may also formulate DLA to derive an equation for the random variable $\rho(\vec{x})$ itself. The density $\rho(x)$ grows in discrete units at an average rate proportional to $v(x)$. We let $q(z)$ be a random noise variable equal to 1 with probability $z$ and zero with probability $1 - z$. Then in an elementary time step $\Delta t$,

$$
\rho(\vec{x}, t + \Delta t) = \rho(\vec{x}, t) + q(v \Delta t) P(\vec{x}), \tag{21}
$$

so that

$$
\frac{\Delta \rho}{\Delta t} = \frac{q(v(x) \Delta t)}{\Delta t} P(\vec{x}, t). \tag{22}
$$

Our interest here is to understand the correlations of the $\rho$ field on length scales much larger than the lattice spacing. Accordingly, we may use a continuum description for a smoothed field

$$
\rho_{a}(\vec{x}) \equiv \sum_{y} w(\vec{x} - \vec{y}) \rho(\vec{y}),
$$

where the resolution function $w$ sums to unity and has a spatial extent of order $a$. This smoothing will not alter correlations at distances much larger than $a$, yet it gives a smooth density which is easier to treat. Further, any field $\rho$ with inverse power correlations will decrease upon averaging. We expect then, that sufficiently high powers of the field may be neglected after averaging, as in field theories of phase transitions. We are thus led to expand out the expression (19) for $P$:

---

5694
T. A. WITTEN AND L. M. SANDER
27

$$
\begin{aligned}
P(\vec{\mathbf{x}}) &amp;= [1 - \rho_a(\vec{\mathbf{x}})] \left[ 1 - \prod_{n=1}^{r} [1 - \rho_a(\vec{\mathbf{x}} + \vec{1})] \right] = [1 - \rho_a(\vec{\mathbf{x}})] \left[ \sum \rho_a + O(\rho_a^2) \right] \\
&amp;= \sum \rho_a - \rho_a \sum \rho_a + O(\rho_a^2) \\
&amp;\approx c^2 \nabla^2 \rho_a + c \rho_a + c(c - 3) \rho_a^2 / 2 + O(\rho_a \nabla^2 \rho_a) + O(\rho_a^3).
\end{aligned}
$$

In addition the averaging runs over many values of the random variables $q$, so it seems plausible to replace this variable by its average $v$. To perform this averaging systematically would require a full-fledged renormalization treatment. We defer such a detailed treatment for a planned future paper. Our present aim is to formulate an equation for the averaged fields which incorporates the above expectations. Replacing $n$ by its average $v$, and using the expanded form of the $P(x)$ term, we postulate that

$$
\begin{aligned}
\frac{d\rho_a}{dt} &amp;= Z u_a \left( \nabla^2 \rho_a + r_a \rho_a + g_a \rho_a^2 + \cdots \right), \\
\nabla^2 u_a &amp;= \frac{d\rho_a}{dt},
\end{aligned}
\tag{24}
$$

where $r_a$ and $g_a$ are renormalized parameters depending on the averaging scale. We may anticipate several qualitative features of these equations. We first investigate the transparency of the density profile to the diffusing field $u$. To this end, we average $\rho_a$ on a scale comparable to the cluster radius $R$, and treat it as a simple absorber of the field $u$:

$$
\nabla^2 u = Z u \rho_a(r).
\tag{25}
$$

This extreme averaging would be justifiable as long as the cluster is transparent to the diffusing field. Within the radius $R$, $\rho_a$ is roughly constant and $u$ falls off exponentially in a characteristic skin depth given by $1/h^2 = Z \rho_a(r)$. In a large cluster, $\rho_a$ is expected to become arbitrarily small, so that the skin depth goes to infinity. But if the cluster is to be transparent, we require that $h/R \to \infty$, so that $R^2 \rho_a(r)$ must go to zero. For clusters with a Hausdorff dimension $D$, $\rho_a(r) \sim N/R^d \sim R^{D-d}$. Thus $(R/h)^2 \sim R^{(2+D)-d}$. This result is natural since the path of our random walker has Hausdorff dimension 2. The $R^{(2+D)-d}$ counts the number of intersections¹⁹ of the cluster and the random walker, within radius $R$, assuming these are independent. For $2 + D &lt; d$, the number does not diverge with $R$, the number of contacts for potential absorption remains finite, and the cluster remains transparent to the diffusing field. But in the reverse case we expect the cluster to be opaque, with new growth occurring

only on the periphery. This opacity is observed to be the case in our simulations where indeed $2 + D &gt; d$.

Since growth occurs only within a thin layer, we may average the fields only over distances smaller than this layer. In the growing layer the gradient of $\rho$ is large and it is not clear that the $\nabla^2\rho$ can be neglected in the growth equation. No correct simplification of this equation is apparent to us.

To shed light on our growth process, we have studied its behavior in high-dimensional space with the aim of deriving its asymptotic $D$. The motivation for this approach is the simple behavior of known aggregates and other dilation-symmetric profiles above a certain upper critical dimension. The case of random animals illustrates this point. Random animals or randomly branched chains²⁰ may be readily treated under the assumption that there is only a single path on the object connecting any pair of points; such objects have $D = 4$. One may investigate the validity of the assumption by estimating the number of contacts between two parts of the object which meet at the origin, assuming the two are independent. The density of points in each of the two parts falls off as $r^{D - d}$; thus the density of crossings goes as $r^{2(D - d)}$. The number $N(R)$ of crossings within radius $R$ goes as

$$
R^{2(D - d) + d} = R^{2D - d}.
$$

The number grows indefinitely with $R$ if $2D &gt; d$. Thus the argument giving $D = 4$ requires $2D &lt; d$, or $d &gt; 8$. This criterion gives an upper critical dimension of 8. A more standard field theoretic argument²¹ gives the same result. Random linear chains have $D = 2$ if intersections of links are allowed. By the same reasoning these intersections are negligible when $d &gt; 2D = 4$. Thus 4 is the upper critical dimension in agreement with polymer field theory.

For the DLA problem, there is no upper critical dimension in this sense. We show this by assuming the reverse and arriving at a contradiction. Suppose that $D$ attains an asymptotic value for large $d$. Since $2D &lt; d$ the cluster may be treated as a treelike structure, where self-crossings are not appreciable. Since $2 + D &lt; d$, the aggregate is, in addition, transparent

---

DIFFUSION-LIMITED AGGREGATION

to the diffusing field from which it grows, by the argument above. We may thus simplify the growth model considerably. Since the field $u$ is essentially uniform within the cluster, we allow all sites adjacent to cluster sites to grow with the same probability. Since cluster intersections are assumed negligible, we may allow multiple occupancy of any lattice site. These simplifications give a model which can be explicitly solved. We will see that the radius grows only logarithmically with particle number, violating the hypothesis.

To show this, we consider the ensemble of $n$-site clusters grown from the origin. The $n$ clusters are grown by adding each successive particle indifferently to the $(n - 1)c$ sites adjacent to the existing ones. The number $G(n)$ of $n$-site clusters is thus

$$
(n - 1) c \quad G (n - 1) = c ^ {n - 1} (n - 1)!
$$

The number $G(x, n)$, with the $n$th site at $\vec{x}$ is given by

$$
G (x, n) = \sum_ {\vec {1}} S (\vec {x} + \vec {1}, n - 1), \tag {26}
$$

where $S(\vec{y}, m)$ is the number of $m$-particle clusters with an arbitrary particle at $\vec{y}$. The particle at $\vec{y}$ must be the $i$th particle for some $i \leq m$. There are $G(\vec{y}, i)$ ways to arrange the first $i$ particles, and

$$
i c (i + 1) c \dots (m - 1) c = G (m) / G (i)
$$

ways to arrange the rest. Thus

$$
S (\vec {y}, m) = \sum_ {i = 1} ^ {m} \frac {G (m)}{G (i)} G (\vec {y}, i). \tag {27}
$$

Inserting this into Eq. (26) for $G(x, n)$, we find

$$
\frac {G (x , n)}{G (n)} = \frac {G (n - 1)}{G (n)} \sum_ {\vec {1}} \sum_ {i = 1} ^ {m - 1} \frac {G (\vec {x} + \vec {1} , i)}{G (i)}. \tag {28}
$$

The left-hand side is the probability that the $n$th site is at $\vec{x}$; we denote it by $g(\vec{x}, n)$; thus

$$
g (\vec {x}, n + 1) = \frac {1}{c n} \sum_ {\vec {1}} \sum_ {i = 1} ^ {n} g (\vec {x} + \vec {1}, i). \tag {29}
$$

This may readily be transformed into a differential equation by multiplying by $n$ and taking an $n$ difference:

$$
n \frac {\partial g}{\partial n} (x, n) = \nabla^ {2} g. \tag {30}
$$

In this diffusion equation, $\ln n$ plays the role of time. Thus, e.g., the second moment $R^2$ of the distribution increases as $\ln n$.

The radius grows more slowly with $n$ than for any finite $D$: The $D$ of this model is $\infty$, contradicting

![img-11.jpeg](img-11.jpeg)
FIG. 9. Hausdorff dimension $D$ of the density in various random aggregates as a function of spatial dimension $d$. The values for DLA are from Ref. 4 ($d = 2$) and Ref. 7 ($d = 3$). The two solid lines indicate the approximate behavior of $D(d)$ for random animals and self-avoiding walks. The boundaries of the finite density domain ($D &lt; d$), the transparent domain ($D &lt; d - 2$), and the non-self-intersection domain ($D &lt; d / 2$) are indicated by dashed lines.

the hypothesis that it attains a finite asymptotic value. We conclude that there is no asymptotic $D$ in diffusion-limited aggregation (or in the Eden model). The same argument shows that $D &gt; d / 2$ for large $d$.

Given this, there are two possibilities for the asymptotic behavior of $D$ (see Fig. 9). One is that $D &lt; d - 2$, so that the clusters are transparent. In this case the high-$d$ behavior is that of the Eden model. Assuming this, we are led again to a contradiction.

Our supposedly transparent clusters have $D &lt; d$, and hence the perimeter of the cluster has the same $D$ as the cluster itself. The number of perimeter sites is proportional to the number of cluster sites, with some proportionality factor less than the coordination number $c$. Thus we may repeat the derivation of $G(n)$, $S(\vec{y}, m)$, and $G(\vec{x}, n)$ above for the Eden model, replacing $c$ by an effective coordination number $\tilde{c}$. The sum over neighbors in the equation for $G(x, n)$ must be multiplied by $\tilde{c} / c$, since only this fraction of sites adjacent to a cluster site consists of perimeter sites. These modifications do not change the qualitative behavior of the growth of these clusters as compared to the multiple occupancy clusters of our original model. We thus arrive

---

T. A. WITTEN AND L. M. SANDER
27

again at the contradictory result that $D \to \infty$, indicating that the original hypothesis of $D &lt; d$ was false. This shows that diffusion-limited aggregates cannot be transparent to the diffusing field, so that $d - 2 \leq D \leq d$. It also shows that Eden-model aggregates must be compact, as has been previously shown numerically$^{12,13}$ for $d = 2$ and 3.

It appears from this study that our Monte Carlo simulations of DLA correspond to a well-defined stochastic model which is amenable to treatment in a continuum language. It appears further that the model has no upper critical dimension in the usual sense. Instead, $d - D$ may attain an asymptotic limit between 0 and 2, so that the aggregates are always opaque to the diffusing field.

## IV. CONSEQUENCES OF SCALE INVARIANCE IN DLA

A number of observable properties of objects growing via DLA can be deduced simply from the (assumed) scale invariance of process. We describe here how aggregates should appear in projection and cross section, and how they should scatter $\mathbf{x}$ rays or neutrons. We also discuss the gelation expected when many aggregates grow together.$^{22}$

Projected onto a plane, a diffusion-limited aggregate with $D &gt; 2$ should appear opaque. The projected density

$$
\sigma(x, y) = \int_{-R}^{R} \rho(\vec{r}) \, dz \sim R^{D-2} \tag{31}
$$

goes to infinity with the size of the objects, and the local density correlations do not survive in the projected density. On the other hand, the cross section of a diffusion-limited aggregate evidently has $\langle \rho(r') \rho(r' + r) \rangle$ equal to that of the full aggregate, so that the exponent $A$ is unchanged in the cross section.

A direct way to observe these correlations is by diffracting a wave from the aggregates. This method has been successful in detecting power-law correlations in random-coil polymers.$^{23}$ The diffracted intensity as a function of wave vector $q$ measures the structure function

$$
S(q) \equiv \int d^3 r \langle \rho(r' + r) \rho(r') \rangle e^{i \vec{q} \cdot \vec{r}}. \tag{32}
$$

The power-law correlations of $\rho$ in some range of $r$ give rise to a conjugate power behavior in $S(q)$ in the range $q \sim r^{-1}$. Here $S(q)$ is proportional to the number of scatterers within a distance $q^{-1}$ of an arbitrary scatterer. Thus $S(q) \sim q^{-D}$ in this range, as one may check by direct substitution into the definition of $S(q)$. Since the aggregates are asymptotically opaque to a scattering wave, a weakly scattered wave is needed to probe the whole volume of the aggregate.

The growth rate of an aggregate in three dimensions can also be readily deduced. We consider the regime where the number of free particles is much greater than the number of aggregated particles, so that $u(\infty)$ is constant in time. Then at large distances $r$, the diffusing field $u$ obeys

$$
u(r) \approx u(\infty)[1 - R(N)/r], \tag{33}
$$

$$
\eta \vec{\nabla} u \mid_r \approx \eta u(\infty)R/r^2. \tag{34}
$$

The capture "radius" $R(N)$ must be proportional to the radius of gyration since the aggregates are opaque to the diffusing field; the quantity in Eq. (34) is the flux density incident on the object. The total rate of aggregation is given by

$$
\begin{aligned}
dN/dt &amp;= R \eta u(\infty) \int d^2 r / r^2 \\
&amp;\sim R(N) \sim N^{1/D}, \tag{35}
\end{aligned}
$$

Solving the equation gives $N \sim t^{D/(D-1)}$. This law gives the asymptotic growth rate of an aggregate.

In a similar way one may predict gelation (i.e., intersection) of a collection of growing aggregates. Suppose that $c_0$ is the concentration of nucleated aggregates. They will start to intersect and form a gel when $c_0 R^d \approx 1$. The concentration of monomers (the "particles") is

$$
c \approx N(R)/R^d = R^{D-d} = c_0^{1-D/d}. \tag{36}
$$

In three dimensions this gives $c \sim c_0^{1/6}$. Thus the mass of the gel may be made indefinitely small by reducing the concentration of seeds. This effect is augmented by the percolation effects present in ordinary gels.

## V. SUMMARY

The DLA model which we have discussed in this paper seems to be applicable to a wide variety of phenomena which at first sight are unrelated. As such, its general properties are worth examining in detail; it is to this task that we have addressed ourselves.

The most striking features that we have discussed are the long-range, universal properties associated with scale invariance. It is worth repeating explicitly that these long-range properties do not arise from long-range forces: Whatever occurs in real dust, smoke, etc., our simulations show that short-range forces can build up long-range correlations, just as in the case of critical phenomena.

The remaining theoretical problems associated with our model seem formidable. We believe it would be very interesting and useful to understand

---

DIFFUSION-LIMITED AGGREGATION
5697

on a deeper level the apparent scale invariance that we observe; such understanding has been arrived at in other apparently similar problems (such as that of the self-avoiding random walk). We have shown that DLA is much too different from critical phenomena to be treated by a direct translation of the methods used there. The lack of an upper critical dimension for the theory is one signal of our difficulty.

Some promising approaches have appeared and should be pursued. Rikvold²⁴ has reduced DLA to a simpler problem by schematically representing the "screening" effect by a reduction of the flux onto a point according to a formula involving the number of neighbors in shells surrounding the site. This is a further simplification of the mean-field treatment of Sec. III which may be useful if it indeed contains all the relevant physics (which is not clear to us at the moment). Gould, Family, and Stanley²⁵ are using the methods of real-space renormalization for DLA (and other similar problems). Of course, this approach assumes the existence of scaling symmetry; it should allow an approximate calculation of  $D$ .

## ACKNOWLEDGMENTS

We would like to thank L. Auvray, Z. M. Cheng, P. G. de Gennes, H. Gould, R. Richter, H. Muller-Krumbhaar, T. M. Sanders, R. Savit, and L. S. Schaefer for useful discussions. One of us (T.W.) is grateful to the Collège de France for hospitality. This work was supported in part by the Centre National de la Recherche Scientifique and by the National Science Foundation Grants Nos. DMR-78-25012, DMR-82-03698, and DMR-80-12867 (polymer program).

¹A. I. Medalia, Surf. Colloid Sci. 4, 1 (1971).
²S. K. Friedlander, Smoke, Dust, and Haze (Wiley, New York, 1977).
³W. W. Mullins and R. F. Sekerka, J. Appl. Phys. 34, 323 (1963).
⁴T. A. Witten, Jr. and L. M. Sander, Phys. Rev. Lett. 47, 1400 (1981).
⁵S. R. Forrest and T. A. Witten, Jr., J. Phys. A 12, L109 (1979).
⁶B. Mandelbrot, Fractals, Form, Chance, and Dimension (Freeman, San Francisco, 1977).
⁷P. Meakin, Phys. Rev. A 27, 1495 (1983).
⁸D. Amit, Field Theory, the Renormalization Group, and Critical Phenomena (McGraw-Hill, New York, 1978).
⁹P. G. de Gennes, Phys. Lett. 38A, 339 (1972).
¹⁰C. Domb, J. Phys. A 9, L141 (1976); see also Ref. 11 and references therein.
¹¹D. Stauffer, Phys. Rep. 54, 1 (1979).
¹²M. Eden, in Proceedings of the Fourth Berkeley Symposium on Mathematical Statistics and Probability, edited by J. Neyman (University of California Press, Berkeley, 1961), Vol. IV, p. 223.
¹³See Ref. 12 and H. P. Peters, D. Stauffer, H. P. Holters, and K. Loewenich, Z. Phys. B 34, 399 (1979).
¹⁴P. Mandeville and L. de Seze, in Numerical Methods in the Study of Critical Phenomena, edited by I. Della Dora, J. Demongeot, and B. Lacolle (Springer, Berlin, 1981); G. K. Shultheiss, G. B. Benedeck, and R. W. du Bois, Macromolecules 13, 939 (1980); H. J. Hermann, D. P. Landau, and D. Stauffer, Phys. Rev. Lett. 49, 412 (1982).
¹⁵We are grateful to Loic Auvray for pointing this out. See E. D. Forster, J. Electrostatics 12, 1 (1982).
¹⁶M. E. Sander (private communication).
¹⁷J. S. Langer and H. Muller-Krumbhaar, Acta Metall. 26, 1081 (1979); 26, 1689 (1979); H. Muller-Krumbhaar and J. S. Langer, ibid. 26, 1697 (1978).
¹⁸Z.-M. Cheng, R. Richter, L. M. Sander, and T. A. Witten, Jr., Bull. Am. Phys. Soc. 28, 261 (1983).
¹⁹J. des Cloizeaux (private communication).
²⁰M. Daoud and J. F. Joanny, J. Phys. (Paris) 42, 1359 (1981).
²¹T. C. Lubensky and J. Isaacson, Phys. Rev. A 20, 2130 (1979).
²²T. A. Witten, Jr., in International Union of Pure and Applied Chemistry 28th Macromolecular Symposium, University of Massachusetts, Amherst, Massachusetts, 1982, edited by J. Chien, R. Lenz, and O. Vogl (IUPAC, New York, 1982).
²³J. P. Cotton, D. Decker, B. Farnoux, G. Jannik, R. Oker, and C. Picot, Phys. Rev. Lett. 32, 1170 (1974).
²⁴P. A. Rikvold, Phys. Rev. A 26, 647 (1982).
²⁵H. Gould (private communication); H. Gould, F. Family, and H. E. Stanley, Phys. Rev. Lett. 50, 261 (1983).
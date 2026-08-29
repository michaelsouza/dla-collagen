PRL 109, 255701 (2012)

PHYSICAL REVIEW LETTERS

week ending 21 DECEMBER 2012

# Fracturing Highly Disordered Materials

A. A. Moreira,¹ C. L. N. Oliveira,¹ A. Hansen,² N. A. M. Araújo,³ H. J. Herrmann,¹,³ and J. S. Andrade, Jr.¹,*

¹Departamento de Física, Universidade Federal do Ceará, 60451-970 Fortaleza, Ceará, Brazil
²Department of Physics, Norwegian University of Science and Technology, N-7491 Trondheim, Norway
³Computational Physics for Engineering Materials, IfB, ETH Zürich, 8093 Zürich, Switzerland

(Received 6 June 2012; published 21 December 2012)

We investigate the role of disorder on the fracturing process of heterogeneous materials by means of a two-dimensional fuse network model. Our results in the extreme disorder limit reveal that the backbone of the fracture at collapse, namely, the subset of the largest fracture that effectively halts the global current, has a fractal dimension of $1.22 \pm 0.01$. This exponent value is compatible with the universality class of several other physical models, including optimal paths under strong disorder, disordered polymers, watersheds and optimal path cracks on uncorrelated substrates, hulls of explosive percolation clusters, and strands of invasion percolation fronts. Moreover, we find that the fractal dimension of the largest fracture under extreme disorder, $d_{f} = 1.86 \pm 0.01$, is outside the statistical error bar of standard percolation. This discrepancy is due to the appearance of trapped regions or cavities of all sizes that remain intact till the entire collapse of the fuse network, but are always accessible in the case of standard percolation. Finally, we quantify the role of disorder on the structure of the largest cluster, as well as on the backbone of the fracture, in terms of a distinctive transition from weak to strong disorder characterized by a new crossover exponent.

DOI: 10.1103/PhysRevLett.109.255701

PACS numbers: 64.60.ah, 64.60.al, 89.75.Da

The brittle fracture of heterogeneous systems still represents a major challenge from both scientific and technological points of view. It has been the subject of intense scientific research in physics, material science, and mechanical and metallurgical engineering [1–4]. The amount of small cracks and the shape of the largest fracture potentially determine whether or not the system still supports external loads and how catastrophic the rupture will be. Previous studies have shown that the degree of disorder in the material rules the transition between abrupt and gradual ruptures; i.e., the more heterogeneous the material is, the more warning one gets before the system collapses [5]. However, the nature of this transition, as well as the behavior of the fracturing system in the limit of strong disorder [6–8], remain as important open questions. Evidently, to model fracturing formation, it is fundamental to determine how stress is redistributed over the system while cracks appear, grow, and merge. Although conceptually simple, the fuse network model is a good candidate for dealing with such a problem, since it can clearly capture the essential features of the involved physical phenomena. In this model, resistors are used to mimic springs, in an approximate description for elasticity, where vector and tensor fields describing fracture mechanics are replaced by a scalar field representing the local strain [9–12].

In this Letter we investigate the role of disorder on the scaling properties of the fuse network model at the critical collapse condition. We first study in detail the limiting case of extreme disorder. This is performed by measuring, through a purely geometrical technique, the fractal dimension of three different structures, namely, the backbone of

the fracture of broken bonds that halts current through the lattice, the largest fracture formed by the broken bonds (backbone plus dangling ends attached to it), and the total network of all broken bonds (largest cluster plus smaller clusters not attached to it). We then show how the self-similar behavior of the resulting fracture topology crosses over from one regime to another as we move from weak to strong disorder.

Let us start by describing the fuse network model [5,13]. In this model, the electric potential in a resistor network should provide a simplified description of the local strain in a fracturing system. A crack forms when the stress or, correspondingly, the electric current over a given resistor surpasses a certain threshold. Here, our system is a two-dimensional lattice where each bond is a resistor with a given conductance and fusing threshold value. Fracture formation in 2D systems represents an important technological problem with many practical applications [14–16]. For simplicity, we consider here the case in which the conductance is the same for all bonds; however, we expect similar results with a varying conductance [17]. We model the heterogeneity by assigning to each bond $i$ a threshold given by $\tau_{i} = 10^{\beta R_{i}}$, where $R_{i}$ is a random number uniformly distributed in the interval $-1 &lt; R_{i} &lt; 1$. Therefore, the distribution of thresholds is hyperbolic, $P_{\tau}(\tau) \sim \tau^{-1}$, with upper and lower bounds given by $10^{\beta}$ and $10^{-\beta}$, respectively.

Generally speaking, we consider that a potential difference is applied between two opposite sides of a resistor network, and solve Kirchhoff’s law to determine the current passing through each bond [18]. Below the threshold

0031-9007/12/109(25)/255701(5)

255701-1

© 2012 American Physical Society

---

PRL 109, 255701 (2012)

PHYSICAL REVIEW LETTERS

week ending 21 DECEMBER 2012

value, each bond conducts according to Ohm's law, but once the current $I_{i}$ at a given bond $i$ reaches the threshold $\tau_{i}$, the bond burns (or breaks, in the mechanical terminology) and becomes an insulator. In this way, the largest current-threshold ratio, $\max(I_{i} / \tau_{i})$, determines the next bond to be burned. Here we assume that the potential starts from zero and raises slowly, allowing only one bond to burn at each step. Pathological defects are avoided by using a tilted square lattice; therefore, in the first step all currents are the same, and the bond with the smaller threshold is the first to burn. In the following steps, inhomogeneities are gradually introduced due to the burnt bonds, so that local threshold and current values should determine which one burns next.

We initially focus on the case of a fuse network under extreme disorder, $\beta \rightarrow \infty$, where thresholds are distributed over many orders of magnitude. In this limit, for all practical purposes, one can assume that the smaller (larger than one) ratio between the thresholds of any two bonds is larger than the largest ratio of the currents of any two bonds in the conducting part of the network. In this regime, any variability in the currents becomes irrelevant so that the next bond to burn should be the one with the smaller threshold among those that participate in transport. Since the thresholds are randomly distributed, this is entirely equivalent to a process in which a random bond with finite current, $I &gt; 0$, is chosen to burn at each step. As the bonds burn, however, they may form a cavity that is connected to the rest at a single node (see Fig. 1). Because all nodes inside a

![img-0.jpeg](img-0.jpeg)
FIG. 1 (color online). The fuse network under extreme disorder. In each step, a random bond belonging to the conducting part of the network is chosen to burn. Here the burnt bonds were removed and the red lines (dark gray thick) placed in the complementary lattice, representing cracks. The green line (gray) in the center corresponds to a bond that will merge two large cracks, forming two cavities in the lattice (light blue and light yellow dots). The dark blue and dark brown dots depict the limiting boundaries of each cavity. The purple dots (top center) correspond to sites connected to only one of the poles; therefore, they do not participate in the transport, and the (purple) bonds connecting them do not burn.

cavity are equipotential, their connecting bonds are current free and cannot burn.

In this way, the extreme disorder limit of the fuse network model can be viewed as a modified percolation problem. In the standard percolation, bonds are randomly and sequentially occupied, while in the fuse network under extreme disorder, one only burns (occupies) bonds that belong to the conducting backbone. As shown in Fig. 1, once a cavity is formed, the bonds inside remain unoccupied and, as a consequence, the clusters of occupied bonds in the complementary lattice do not form loops. Under this reasoning, the extreme disorder limit of the fuse network model becomes a purely geometrical problem. Simulations performed with fuse networks at $\beta = 10^{8}$ confirm that these two models are identical. Such a geometrical approach for the extreme disorder case greatly reduces the computational demand, enabling us to simulate the fracturing process for networks with linear size $L$ going from 16 to 2048, and using at least 1000 samples. As shown in Fig. 2, we stop each realization when the two sides, where the potential difference is applied, become disconnected; i.e., no current can pass through the system.

In Fig. 3 we show that the mass of the largest fracture, $M_{f}$, its backbone mass $M_{b}$, as well as the set of all broken bonds, $M_{t}$, grow with the system size as power laws. First, the total mass of burnt bonds scales with the linear size as $M_{t} \sim L^{d_{t}}$, with $d_{t} = 2.00 \pm 0.01$, suggesting that the bonds burn homogeneously through the lattice. The backbone grows as $M_{b} \sim L^{d_{b}}$, with $d_{b} = 1.22 \pm 0.01$, which is statistically identical to the exponent obtained for optimal paths under strong disorder [19], disordered polymers [20], watersheds [21] and optimal path cracks on uncorrelated substrates [22], the hulls of explosive percolation clusters [23], and the strands of invasion percolation fronts [24]. For the largest fracture, however, we obtain $M_{f} \sim L^{d_{f}}$, with $d_{f} = 1.86 \pm 0.01$, which is different from the fractal dimension of the largest cluster in 2D percolation, $d_{p} = 1.8958$ [25,26]. For 3D lattices under strong disorder, a continuous chain can no longer split the system in two. We therefore expect a cutting surface that is similar to a watershed in 3D with fractal dimension, $d_{b} \approx 2.48$ [27].

In the limit of extreme disorder, the fracture backbone in the fuse model is identical to the one of loopless percolation [28]. This can be seen by considering that the burning of fuses of a specific configuration of thresholds due to the extreme disorder just follows the sequence of their inverse rank, except if the fuse would close a loop or lie inside a nearly closed loop. In parallel, one can construct a configuration of loopless percolation by assigning an occupation rank to each site, identical to the ranking given by the thresholds (not occupying sites closing loops). The spanning cluster of this percolation configuration then consists of the fracture of the fuse model and sites inside nearly closed loops that do not contribute to the backbone. This shows that the bonds forming the backbone should be

255701-2

---

PRL 109, 255701 (2012)

PHYSICAL REVIEW LETTERS

week ending 21 DECEMBER 2012

![img-1.jpeg](img-1.jpeg)

![img-2.jpeg](img-2.jpeg)
FIG. 3 (color online). Size dependence for the total number of burnt bonds  $M_{t}$ , the mass of the largest fracture  $M_{f}$ , and the mass of the backbone  $M_{b}$ . The inset shows the size dependence of the ratio between the masses of largest clusters in the fuse and in the percolation model,  $M_{f} / M_{p}$ .

![img-3.jpeg](img-3.jpeg)
FIG. 2 (color online). Typical realizations of the fuse network at the point of disconnection  $(L = 32)$ . In (a)  $\beta = 0.01$  (weak disorder), in (b)  $\beta = 1$  (intermediate disorder), and in (c)  $\beta = 100$  (strong disorder, for this lattice size). The black lines show the backbone, the (dark gray) red lines the dangling ends, and the light gray (light blue) lines all the other cracks.

exactly the same in both models. It was previously observed that the backbone of loopless percolation has the same fractal dimension as the optimum path in strong disorder [29], therefore giving support to this argument.

The cavities cannot change the fractal dimension of the backbone but may very well change the dimension of the largest fracture. The largest fracture comprises the backbone and the dangling ends attached to it. Once a cavity is formed in the largest fracture, it precludes the growing and attaching of other dangling ends inside it. Note that in three dimensions, since we need an almost closed surface to form a cavity, this effect would be less important. As a consequence, the largest fracture in the 2D fuse model under extreme disorder is certainly smaller than the largest cluster in standard percolation. Since we obtain, for the former case, a fractal dimension smaller than the one

![img-4.jpeg](img-4.jpeg)

expected for standard percolation, we conclude that cavities form at every scale, and the difference between the two models becomes increasingly relevant as the system size grows.

To further test our hypothesis, we performed simulations with a pinpoint algorithm that simultaneously builds percolation clusters and fuse network fractures under extreme disorder. Precisely, at each step, we randomly choose a bond in the lattice and, if this bond is part of the conducting backbone, it is occupied in the percolation lattice as well as burned in the fuse network. If this bond is inside one of the cavities, however, it is occupied only in the percolation lattice. Once a cluster forms that crosses the system, the percolation condition is achieved in both models simultaneously. If the fractal dimensions are in fact different, the ratio between the masses of the largest clusters,  $M_{f} / M_{p}$ , where  $M_{p}$  is the mass of the spanning cluster in percolation, should vary with the system size as a power law, with an exponent given by  $d_{f} - d_{p} \approx -0.03$ . The obtained results shown in the inset of Fig. 3 support our conjecture that the largest fracture of the fuse network under extreme disorder corresponds to a subset of the spanning cluster in percolation. Moreover, this new object is also self-similar, but with a slightly smaller fractal dimension.

It is important to mention that some variants of the percolation model previously investigated also depart from the universality class of standard percolation. For example, in invasion percolation with trapping [30], when a loop is formed in the growing cluster, no site or bond inside this loop can be occupied, constituting a trapped region. These trapped regions are somehow similar to our cavities, only that cavities are sections of the lattice outside the conducting backbone of unoccupied bonds, while trapped regions

255701-3

---

PRL 109, 255701 (2012)

PHYSICAL REVIEW LETTERS

week ending 21 DECEMBER 2012

![img-5.jpeg](img-5.jpeg)

![img-6.jpeg](img-6.jpeg)
FIG. 4 (color online). The transition from weak to strong disorder. We show the mass of the largest fracture (a) and backbone (b) as function of the disorder parameter  $\beta$ . The exponents  $d_{f}$  and  $d_{b}$ , controlling the scaling in the strong disorder regime, are the same as in Fig. 3.

are sections outside the infinite cluster of unoccupied bonds. In this case, statistically relevant deviations have also been detected from the fractal dimension of the spanning cluster in standard percolation [31,32].

Next we investigate how the behavior of the fuse network model crosses over from weak to strong disorder by gradually increasing the value of the parameter  $\beta$ . Local currents are computed by applying Kirchhoff's law to each site of the network at each burning step and solving the resulting system of linear algebraic equations. In weak disorder, most of the burnt bonds belong to the backbone of the fracture that grows linearly with the system size,  $d_{b} = d_{f} = 1$ . As  $\beta$  increases, the fractal dimensions obtained in the extreme disorder limit should eventually be recovered. Figure 4 shows how the masses  $M_{f}$  and  $M_{b}$  vary with the disorder parameter  $\beta$ . For small values,  $\beta &lt; 0.1$ , both masses are proportional to the system size and depend weakly on  $\beta$ . For intermediate values,  $0.1 &lt; \beta &lt; \beta^{*}(L)$ , the masses depend on  $\beta$  but still grow linearly with  $L$ , therefore indicating the persistence of the weak disorder regime. However, as one goes to larger values,  $\beta &gt; \beta^{*}(L)$ , the curves cross over to the strong disorder

regime, where the masses show superlinear growth with system size,  $M_{t} \sim L^{d_{t}}$ ,  $M_{f} \sim L^{d_{f}}$ , and  $M_{b} \sim L^{d_{b}}$ , but are again not dependent on  $\beta$ . The value  $\beta^{*}$  marks the transition from weak to strong disorder. One should expect that, above a characteristic length  $\xi$ , the system scales as in the weak disorder limit. Certainly, the length  $\xi$  should depend on the strength of the disorder, diverging in the extreme disorder as  $\xi \sim \beta^{1 / \eta}$ . The onset of the strong disorder regime takes place when  $\xi &gt; L$ , resulting in  $\beta^{*} \sim L^{\eta}$ . The insets of Figs. 4(a) and 4(b) show the data scaled by the fractal dimensions and  $\beta^{*}$ , with the controlling exponent  $\eta = 0.9 \pm 0.1$ . The collapse of the curves in the transition region corroborates our analysis and reveals the presence of a crossover between the two regimes.

The scaling in Fig. 4 provides important information to evaluate the strength of a sample and the current state of a fracture. Based on the sample size and disorder strength, one can determine how far a fracture is from complete rupture and if it can still resist external load. In addition, the identification of a crossover length can be useful to elucidate the dynamical nature of the rupture process [33].

In conclusion, our results show that the threshold disorder introduces a characteristic scale  $\xi$ . Above this scale, the fracture backbone grows linearly with system size, consistent with the weak disorder regime. However, for scales smaller than  $\xi$ , the main fracture displays a tortuous self-similar shape, with the same fractal dimension of the optimum path under strong disorder [24] and other previously investigated models [19,21-23]. In the limit of extreme disorder,  $\xi \rightarrow \infty$ , the largest fracture has a fractal dimension of  $d_{f} = 1.86 \pm 0.01$ , close to, but different from, the fractal dimension of percolation clusters [26]. Establishing that the fractures are fractal within a certain range has several practical implications. For example, Rayleigh waves, which dissipate elastic energy, can be severely damped when traveling along fractal surfaces. Also, when cracks age or cement under a load, they do this much faster being fractal.

We thank the Brazilian Agencies CNPq, CAPES, FUNCAP and FINEP, the FUNCAP/CNPq Pronex grant, and the National Institute of Science and Technology for Complex Systems in Brazil for financial support.

*soares@fisica.ufc.br
[1] M.P. Marder, Condensed Matter Physics (Wiley, Hoboken, 2010), 2nd ed.
[2] M.F. Kanninen and C.H. Popelar, Advanced Fracture Mechanics, The Oxford Engineering Science Series (Oxford University, New York, 1985).
[3] M. Sahimi, Phys. Rep. 306, 213 (1998).
[4] M.J. Alava, P.K. V. V. Nukala, and S. Zapperi, Adv. Phys. 55, 349 (2006).
[5] B. Kahng, G.G. Batrouni, S. Redner, L. de Arcangelis, and H.J. Herrmann, Phys. Rev. B 37, 7625 (1988).

255701-4

---

PRL 109, 255701 (2012)

PHYSICAL REVIEW LETTERS

week ending 21 DECEMBER 2012

[6] P.K.V.V. Nukala, S. Simunovic, and S. Zapperi, J. Stat. Mech. Theory Exp. (2004) P08001.

[7] I. Malakhovsky and M.A.J. Michels, Phys. Rev. B 76, 144201 (2007).

[8] D.-P. Hao, G. Tang, H. Xia, K. Han, and Z.-P. Xun, J. Stat. Phys. 146, 1203 (2012).

[9] A. Hansen, E. L. Hinrichsen, and S. Roux, Phys. Rev. Lett. 66, 2476 (1991); Phys. Rev. B 43, 665 (1991).

[10] L. de Arcangelis, A. Hansen, H. J. Herrmann, and S. Roux, Phys. Rev. B 40, 877 (1989).

[11] A. Gilabert, C. Vanneste, D. Sornette, and E. Guyon, J. Phys. (Paris) 48, 763 (1987).

[12] M.J. Alava, P.K.V.V. Nukala, and S. Zapperi, Int. J. Fract. 154, 51 (2008); P.K.V.V. Nukala, S. Zapperi, M.J. Alava, and S. Šimunović, Int. J. Fract. 154, 119 (2008); C. Manzato, A. Shekhawat, P.K.V.V. Nukala, M.J. Alava, J.P. Sethna, and S. Zapperi, Phys. Rev. Lett. 108, 065504 (2012).

[13] L. de Arcangelis, S. Redner, and H.J. Herrmann, J. Phys. (Paris), Lett. 46, 585 (1985).

[14] F. Wittel, F. Kun, H. J. Herrmann, and B. H. Kroplin, Phys. Rev. Lett. 93, 035504 (2004).

[15] T. Pardoen, F. Hachez, B. Marchioni, P.H. Blyth, and A.G. Atkins, J. Mech. Phys. Solids 52, 423 (2004).

[16] E. W. Wong, P. E. Sheehan, and C. M. Lieber, Science 277, 1971 (1997).

[17] In the case where all the conductances are the same, some symmetric conditions may happen, where a fraction of the backbone lies on a Wheatstone bridge connecting sites with the same potential. Our geometrical model does not account for this possibility. However, we performed tests introducing disorder in the conductance, apart from the disorder in the thresholds, avoiding this effect, and obtained similar results. In fact, no qualitative difference is expected, as long as the distribution of conductance is bounded, not ranging over many orders of magnitude.

[18] The linear equation system was solved through the HSL library, a collection of FORTRAN codes for large-scale scientific computation. See http://www.hsl.rl.ac.uk/.

[19] J.S. Andrade, E.A. Oliveira, A.A. Moreira, and H.J. Herrmann, Phys. Rev. Lett. 103, 225503 (2009).

[20] M. Cieplak, A. Maritan, and J.R. Banavar, Phys. Rev. Lett. 72, 2320 (1994).

[21] E. Fehr, J. S. Andrade, S. D. da Cunha, L. R. da Silva, H. J. Herrmann, D. Kadau, C. F. Moukarzel, and E. A. Oliveira, J. Stat. Mech. (2009) P09007; E. Daryaei, N. A. M. Araújo, K. J. Schrenk, S. Rouhani, and H. J. Herrmann, Phys. Rev. Lett. 109, 218701 (2012).

[22] E.A. Oliveira, K.J. Schrenk, N.A.M. Araújo, H.J. Herrmann, and J.S. Andrade, Phys. Rev. E 83, 046113 (2011).

[23] N. A. M. Araújo and H. J. Herrmann, Phys. Rev. Lett. 105, 035701 (2010).

[24] M. Cieplak, A. Maritan, and J.R. Banavar, Phys. Rev. Lett. 76, 3754 (1996).

[25] D. Stauffer and A. Aharony, Introduction to Percolation Theory (Taylor &amp; Francis, London, 1992).

[26] S. Roux, A. Hansen, H. Herrmann, and E. Guyon, J. Stat. Phys. 52, 237 (1988).

[27] E. Fehr, D. Kadau, N.A.M. Araújo, J.S. Andrade, and H.J. Herrmann, Phys. Rev. E 84, 036116 (2011).

[28] M. Porto, S. Havlin, S. Schwarzer, and A. Bunde, Phys. Rev. Lett. 79, 4060 (1997); M. Porto, N. Schwartz, S. Havlin, and A. Bunde, Phys. Rev. E 60, R2448 (1999).

[29] K.J. Schrenk, N.A.M. Araújo, J.S. Andrade, and H.J. Herrmann, Sci. Rep. 2, 348 (2012).

[30] D. Wilkinson and J.F. Willemsen, J. Phys. A 16, 3365 (1983).

[31] S. Roux and E. Guyon, J. Phys. A 22, 3693 (1989).

[32] A.P. Sheppard, M.A. Knackstedt, W.V. Pinczewski, and M. Sahimi, J. Phys. A 32, L521 (1999).

[33] A. Shekhawat, S. Zapperi, and J. P. Sethna, arXiv:1210.0989.

255701-5
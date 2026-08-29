Physica A 178 (1991) 415-420
North-Holland

# Diffusion limited aggregation. The role of surface diffusion

Juan M. García-Ruiz and Fermín Otálora

Instituto Andaluz de Geología Mediterranea, C.S.I.C. – Universidad de Granada, c/Fuentenueva s/n, Granada 18002, Spain

Received 3 April 1991

We present a growth model in which the hitting particles are able to diffuse to more stable growth sites in the perimeter of a cluster growing by diffusion limited aggregation. By tuning the diffusion path $L_{s}$, the morphological output – from disordered fractal to perfect single crystals – can be controlled. Instabilities appear when the mean length of the crystal faces $L_{t}$ are greater than $2L_{s}$.

Over the last years, several modifications to the diffusion limited aggregation (DLA) model have been proposed in order to explain the morphological behaviour at conditions closer to equilibrium. For instance Meakin [1] reports the emergence of anisotropy in very large DLA simulations and suggest that this anisotropic shape should be the asymptotic one when dealing with on-lattice simulations. A mathematical procedure called "noise reduction" [2] has been developed allowing the apparition of this asymptotic anisotropic shape for reasonable CPU times. The importance of anisotropy is accepted as inherent to crystal growth simulations using DLA modifications [3]. Adding ideas from the crystal growth theory to DLA-like simulations, Vicsek [4], Banavar et al. [5] and Xiao et al. [6] find patterns that are reminiscent of those formed in dendritic solidification. In this paper we test the influence of just one process (surface diffusion) on the morphological pattern arising from a DLA computer simulation.

In the present simulation a single particle (seed) is placed in the centre of a 350 by 350 pixels matrix and particles will be added to the seed in order to form a cluster. We consider a set of 1000 independently diffusing particles released in a circumference of radius $r = 50$, in order to simulate a finite concentration of diffusing particles. The particles move following a random walk trajectory until either (a) they reach a growth site, i.e., a site that is any of the eight nearest neighbours of a site forming the cluster, or alternatively,

0378-4371/91/$03.50 © 1991 – Elsevier Science Publishers B.V. (North-Holland)

---

416
J.M. García-Ruiz, F. Otálora / DLA, surface diffusion

(b) they reach a position that is 60 pixels far from the maximum cluster radius $r_{\mathrm{max}}$. In both cases, a new particle is released in a point belonging to a circumference with radius $r_{\mathrm{g}} = r_{\mathrm{max}} + 50$. So, we have (1) a circle of “generation” of diffusing particles at least 50 pixels far from any particle in the cluster, (2) a perfect circular sink for particles placed at least 60 pixels far from any particle in the cluster and (3) a growth cell with a constant number of 1000 diffusing particles (note that because $r_{\mathrm{max}}$ increases as the cluster grows, particle concentration in the bulk is decreasing with time). The main difference between our model and the original Witten and Sander model [7, 8] and their subsequent modifications lie in the behaviour of a particle when it reaches a growth site. In previous simulations, a particle reaching growth site may (a) be added to the cluster (original Witten and Sander model [7]), (b) increment a counter that represents the number of times this site has been visited and once the counter reaches a predefined number $m$, the particle is attached to it (noise reduction approach) [9, 10], or (c) have the possibility of desorption (dielectric breakdown model) [11, 12]. In the present case, the particle landing on a growth site undergoes a further diffusion on the cluster perimeter following a random walk over the set of growing sites during a diffusion time $T_{\mathrm{s}}$. We will consider the square particles to have a bonding distribution of eight bonds oriented normally to their edges and corners. As the system is supported on a two-dimensional square lattice with P4mm symmetry and the bonds are assumed to have the same energy, there is a number of different positions on the perimeter of a cluster with P4mm symmetry, which are displayed in fig. 1c. The most energetically favourable positions are those sharing the larger number of bonds with the cluster. After $T_{\mathrm{s}}$ units of time, the particle is added to the cluster on a visited site of higher attachment energy. If more than one site is found with that local property, the first reached one is selected and filled. If during its walk of $T_{\mathrm{s}}$ time units, the particle does not find any site with higher attachment energy than the one corresponding to the touching point, it stays in the landing position as a new cluster particle.

We have tested the effect of diffusion time $T_{\mathrm{s}}$, which correlates with the mean diffusion path $L_{\mathrm{s}}$ on the cluster perimeter ($L_{\mathrm{s}} \propto T_{\mathrm{s}}^{D / 2}$, where $D$ is the fractal dimension of the cluster perimeter). Six different $T_{\mathrm{s}}$ values were tested. The morphological output for $T_{\mathrm{s}} = 0$ (fig. 2a) is the well-known fractal pattern of a typical DLA with $D \approx 1.70$ [7]. For $T_{\mathrm{s}} = 10$, we obtained a cluster which also displayed a random fractal pattern. Fig. 2b show overlapped shapes taken every 1000 aggregated particles. In this pattern, tip splitting creates a disordered ramified structure with wider branches. For $T_{\mathrm{s}} = 50$ (fig. 2c), the number of branches, which are created from an initial isometric single pixel square nucleus, are clearly reduced to some preferred orientations.

For $T_{\mathrm{s}} = 100$, the situation is dramatically different. Under this condition, a clear anisotropic pattern was obtained (fig. 2d). The P4mm symmetry appears

---

J.M. García-Ruiz, F. Otálora / DLA, surface diffusion

![img-0.jpeg](img-0.jpeg)
(a)

![img-1.jpeg](img-1.jpeg)
(b)

![img-2.jpeg](img-2.jpeg)
(c)
Fig. 1. Basic definitions concerned with the computer simulation. (a) A random walking particle approaches a growing crystal face. The four different states of any given lattice site are outlined. (b) Bond distribution of every random walker or cluster site. B1 and B2 strengths are equal. (c) A selected set of growing sites on the surface of a P4mm cluster made up with squares particles with the bonding distribution shown in (b). The label of the sites corresponds to its total bond strength.

in the initial stages of the experiment under the shape of an octagonal crystal  $(D = 2)$ , bounded by  $\{10\}$  (box) and  $\{11\}$  (diamond) faces, but once 3000 particles were attached to the seed, the corners start to have a preferred growth rate and four protrusions become later well defined branches. Note that because all the bonds have the same energy, the emergency of anisotropy along [11] comes from diffusion geometry and from the fact that the hitting of

---

J.M. García-Ruiz, F. Otálora / DLA, surface diffusion

![img-3.jpeg](img-3.jpeg)

![img-4.jpeg](img-4.jpeg)

![img-5.jpeg](img-5.jpeg)

![img-6.jpeg](img-6.jpeg)

![img-7.jpeg](img-7.jpeg)

Fig. 2. Morphological output of the simulation for different diffusion times showing the influence of the mean diffusion path on a cluster made by diffusion limited aggregation. Shape contours were drawn after deposition of 1000 particles. (a) $T_{\mathrm{c}} = 0$, 3600 particles. (b) $T_{\mathrm{c}} = 10$, 11 000 particles. (c) $T_{\mathrm{c}} = 50$, 19 000 particles. (d) $T_{\mathrm{c}} = 100$, 23 000 particles. (e) $T_{\mathrm{c}} = 1000$, 23 000 particles. (f) $T_{\mathrm{c}} = 10000$, 27 000 particles.

![img-8.jpeg](img-8.jpeg)

---

J.M. García-Ruiz, F. Otálora / DLA, surface diffusion

particles provokes a growth rate along $\langle 11\rangle$ directions $2^{1/2}$ times that along $\langle 10\rangle$ directions. The branches again develop some protrusions and secondary $\langle 11\rangle$ sidebranches appear. The rate of advance of the protruding tips decrease with time. Secondary arms appearing in the opposite sides are uncorrelated and they have a non-periodical distribution along $\langle 11\rangle$ in accordance with laboratory experiments [13]. In fact, the pattern is strongly reminiscent of the $\mathrm{NH}_4\mathrm{Cl}$ crystalline pattern obtained by Honjo et al. [14].

For $T_{\mathrm{s}} = 1000$ (fig. 2e), the cluster starts with the shape of an octagonal 2D single crystal limited by $\{10\}$ box-type and $\{11\}$ diamond-type faces. As expected from the Wulf law [15] and the growth ratio above defined, the $\{11\}$ faces disappear as growth proceeds and the shape is composed by box faces with concave perimeter topography. Finally, for $T_{\mathrm{s}} = 10000$, the cluster takes the form of an isometric octagonal crystal bounded by equally developed $\{10\}$ and $\{11\}$ faces, in agreement with the theoretical morphology obtained from the periodical bond chains of the structure [16]*.

The mean path $L_{\mathrm{s}}$ on the cluster perimeter is a function of the number of time steps $T_{\mathrm{s}}$. In fact, the particle walk is a fractal walk on the perimeter of the cluster ($L_{\mathrm{s}} \propto T_{\mathrm{s}}^{D / 2}$). A new "nucleation" (type-1 position) occurs on a face when all the other growth sites are farther than $L_{\mathrm{s}}$ from the touching point. This nucleation creates two type-4 positions, i.e., a growing step with two (+ and -) preferred growing sites [17]. Later, new "nucleation" is forbidden on this face until either the growing instability (new step) reaches a $2L_{\mathrm{s}}$ size or it fills completely the face. The speed at which a face grows is proportional to the nucleation rate on this face and to the number of particles needed to fill a face [18]. This growth behaviour implies an anisotropy in the probability of touching. Because the diffusion field is homogeneous, the growth sites closer to the corner of the box shape can be reached by diffusing particles with a probability slightly greater than particles in the centre of box faces. Thus, instabilities leading to ordered dendritic growth appear in these areas when the mean length of the faces $L_{\mathrm{f}}$ are greater than $2L_{\mathrm{s}}$. This assertion can be easily tested in fig. 2. Assuming a square cluster with a perimeter of topological dimension $D_{\mathrm{T}} = 1$, the length of the cluster perimeter is $P = 4(n^{1 / 2} + 1)$, where $n$ is the number of particles conforming the cluster. Thus, for the $n$-particle cluster at which instabilities start to be formed, the values for $L_{\mathrm{s}}$ and $P$ (and hence $L_{\mathrm{f}}$) can be obtained. Comparing them with the morphological output in figs. 2c, d, a good agreement is obtained.

These results support the view that DLA is an appropriate model to describe the morphological behaviour of aggregation patterns grown under diffusional control of mass transport. We think that our work yields interesting results to

*Nevertheless, we have noted that \{11\} faces tend to disappear in clusters of larger sizes.

---

420
J.M. García-Ruiz, F. Otálora / DLA, surface diffusion

be used in the task to understand complex morphological behaviour in terms of simple elementary processes. In particular, we show how the introduction of surface relaxation in a DLA simulation reveals quickly the symmetry properties of the cluster that depends on the bonding distribution in the growth units.

## Acknowledgements

This work was performed under financial support from the Autonomous Government of Andalucía and CICYT Project number PB89-0059.

## References

[1] P. Meakin, R.C. Ball, P. Ramanlal and L.M. Sander, Phys. Rev. A 35 (1987) 5233.
[2] J. Nittmann and H.E. Stanley, Nature 321 (1986) 663.
J. Kertész and T. Vicsek, J. Phys. A 19 (1986) L257.
R.C. Ball, Physica A 104 (1986) 62.
J. Kertész, T. Vicsek and P. Meakin, Phys. Rev. Lett. 57 (1986) 3303.
J. Eckmann, P. Meakin, I. Procaccia and R. Zeitak, Phys. Rev. A 39 (1989) 3185.
[3] E. Ben-Jacob, R. Godbey, N.D. Goldenfeld, J. Koplik, H. Levine, T. Muller and L.M. Sander, Phys. Rev. Lett. 55 (1985) 1315.
J.D. Chen and D. Wilkinson, Phys. Rev. Lett. 55 (1985) 1892.
[4] T. Vicsek. Phys. Rev. Lett. 53 (1984) 2281; Rev. A 32 (1985) 3084.
[5] J.R. Banavar, M. Kohmoto and J. Roberts, Phys. Rev. A 33 (1986) 2065.
[6] R. Xiao, J.I.D. Alexander and F. Rosemberg, Phys. Rev. A 38 (1988) 2447; 39 (1989) 6397.
[7] T.A. Witten and L.M. Sander, Phys. Rev. Lett. 47 (1981) 1400; Phys. Rev. B 27 (1983) 5686.
[8] P. Meakin, in: On Growth and Form, H.E. Stanley and N. Ostrowsky, eds. (Kluwer, Boston, 1986), pp. 111–135.
[9] J. Nittmann and E.H. Stanley, Nature 321 (1986) 663.
J. Kertész and T. Vicsek, J. Phys. A 19 (1986) L257.
[10] H.E. Stanley, in: The Physics of the Structure Formation, W. Güttinger and G. Dangelmayr, eds. (Springer, Heidelberg, 1987) p. 210.
[11] L. Niemeyer, L. Pietronero and H.J. Wiesmann, Phys. Rev. Lett. 52 (1984) 1033.
[12] E. Arian, P. Alstrom, A. Aharony and E. Stanley, Phys. Rev. Lett. 63 (1989) 2005.
[13] A. Dougherty, P.D. Kaplan and J.P. Gollub, Phys. Rev. Lett. 58 (1987) 1652.
[14] H. Honjo, S. Ohta and M. Matsushita, J. Phys. Soc. Jpn. 55 (1986) 2487.
[15] G. Wulff, Z. Kristallogr. Mineral. 34 (1901) 449.
[16] P. Hartman and G.W. Perdock, Acta Crystall. 8 (1956) 49.
[17] W.K. Burton and N. Cabrera, Disc. Faraday Soc. 5 (1949) 33.
[18] A.A. Chernov, J. Cryst. Growth 24/25 (1974) 11.
Journal of Physics A: Mathematical and General

# Backbone and elastic backbone of percolation clusters obtained by the new method of 'burning'

To cite this article: H J Herrmann et al 1984 J. Phys. A: Math. Gen. 17 L261

View the article online for updates and enhancements.

# You may also like

- The Effects of Perfluoroalkyl and Alkyl Backbone Chains, Spacers, and Anchor Groups on the Performance of Organic Compounds as Corrosion Inhibitors for Aluminum Investigated Using an Integrative Experimental-Modeling Approach
I. Milosev, A. Kokalj, M. Poberznik et al.
- A Particle-Based Model for Effective Properties in Infiltrated Solid Oxide Fuel Cell Electrodes
A. Bertel, J. G. Pharoah, D. A. W. Gawel et al.
- Multi-level aggregation of conjugated small molecules and polymers: from morphology control to physical insights
Qi-Yi Li, Ze-Fan Yao, Jie-Yu Wang et al.

This content was downloaded from IP address 200.17.35.102 on 09/01/2026 at 19:22

---

J. Phys. A: Math. Gen. 17 (1984) L261-L266. Printed in Great Britain

# LETTER TO THE EDITOR

# Backbone and elastic backbone of percolation clusters obtained by the new method of 'burning'

H J Herrmann†‡, D C Hong† and H E Stanley†

† Center for Polymer Studies§ and Department of Physics, Boston University, Boston MA 02215, USA

‡ Laboratoire Léon Brillouin, CEN Saclay, 91191 Gif-sur-Yvette Cedex, France

Received 6 January 1984

Abstract. We introduce a method of obtaining information about percolation clusters in which the clusters are 'burned' in different ways. This method yields the backbone and the elastic backbone, their number of loops, shortest path and other quantities. It works in any dimension and can be applied also to other clusters. We obtain accurate estimates for the backbone exponents in two and three dimensions.

Suppose we choose two points  $\mathbf{P}_1$  and  $\mathbf{P}_2$  separated by a distance comparable to the correlation length  $\xi$ . If we pass a current from  $\mathbf{P}_1$  to  $\mathbf{P}_2$  then the set of current carrying bonds is called the backbone and the remaining bonds are called dangling ends. One can also define the backbone as the intersection of all the self-avoiding walks between  $\mathbf{P}_1$  and  $\mathbf{P}_2$  (Shlifer et al 1979, Hong and Stanley 1983a, b).

The investigation of the backbone of clusters—especially in the case of percolation clusters—has been of interest for a long time. Possible applications are the conductivity of random systems (Skal and Shklovski 1975, de Gennes 1976, Daoud 1983) and the flow of fluids in porous media (Stanley and Coniglio 1984). From the theoretical point of view, the backbone has provided an understanding of the general structure of percolation structures within the framework of links, nodes and blobs (Coniglio 1981, 1982, Pike and Stanley 1981, Stanley 1977, Hong and Stanley 1983a, Stanley and Coniglio 1984). The exponents of the backbone such as the exponent  $\beta_{\mathrm{B}}$ :

$$
\rho_ {S} ^ {B} (p) \sim \left(p - p _ {c}\right) ^ {\beta_ {B}}, \tag {1}
$$

where  $\rho_{\mathrm{S}}^{\mathrm{B}}(p)$  is the mean density of sites of the backbone of the fractal dimension  $D_{\mathrm{B}} = d - \beta_{\mathrm{B}} / \nu$ , have been calculated numerically by different methods: large-cell renormalisation (Shlifer et al 1979), Monte Carlo (Kirkpatrick 1978, Pike and Stanley 1981),  $\varepsilon$ -expansion (Harris 1983, Harris and Lubensky 1983), position-space renormalisation group (Hong and Stanley 1983b), and series expansions (Hong and Stanley 1983a). The error bars are quite big, however, and it is important to find effective algorithms for obtaining backbones in order to improve the error estimates for these exponents. The availability of backbones is also important in testing the argument of Stanley and Coniglio (1984) stating the non-validity for backbones of the conjecture of Alexander and Orbach (1982). (See Hong et al (1984) for the case of ants on backbones.)

0305-4470/84/050261+06$02.25 © 1984 The Institute of Physics

---

Letter to the Editor

We now introduce a new fractal object, which we call the elastic backbone. It has been proposed that the elasticity of disordered structures—a gel at the sol-gel transition point, for instance—can be described by the electrical conductivity (de Gennes 1976) and thus related to the normal backbone. However, elasticity can be described by small springs in the bonds of a cluster. It is difficult to imagine that more than just the shortest paths connecting the two points at which a force is applied should contribute to this elasticity. This can be seen by considering figure 1, where a piece of the backbone is shown before and after the elongation due to the force  $F$ . We thus introduce as a new object the 'elastic backbone' of a cluster as being the sites that lie on the union of all the shortest paths between two points  $\mathbf{P}_1$  and  $\mathbf{P}_2$  on the cluster. If the distance between  $\mathbf{P}_1$  and  $\mathbf{P}_2$  goes to infinity, we expect that the densities  $\rho_{\mathrm{S}}^{\mathrm{E}}$  of sites or  $\rho_{\mathrm{L}}^{\mathrm{E}}$  of loops or  $\rho_{\mathrm{C}}^{\mathrm{E}}$  of cutting sites of the elastic backbone should become independent of  $\mathbf{P}_1$  and  $\mathbf{P}_2$ . The question of critical behaviour of  $\rho_{\mathrm{S}}^{\mathrm{E}}, \rho_{\mathrm{L}}^{\mathrm{E}}$  and  $\rho_{\mathrm{C}}^{\mathrm{E}}$  will be studied in this paper.

![img-0.jpeg](img-0.jpeg)
(a)

![img-1.jpeg](img-1.jpeg)
(b)
Figure 1. Supposing that the angles of the object of springs shown in (a) can change freely, we show in (b) the elongation of the object due to the application of the force  $F$  at A and B.

To construct the elastic backbone (and also the full backbone), we propose a new method which we call 'burning'. We first select two endpoints  $\mathbf{P}_1$  and  $\mathbf{P}_2$ , which we choose to be as close as possible to diagonally opposite corners of a surrounding hypercube. The first step is to burn the cluster from  $\mathbf{P}_1$ : at time  $t_1$  site  $\mathbf{P}_1$  burns and gets the value 1; at the next time unit  $t_2$ , all the neighbours of  $\mathbf{P}_1$  burn and get the value 2; at time  $t_{i+1}$ , all the neighbours of sites burning at time  $t_i$  that have not yet burned are burned and get the value  $i+1$ . This procedure was first presented by Stauffer (1984) as a means of describing forest fires (of fractal shape). The first burning of the cluster imposes an ordering to the sites of the cluster. One obtains the burning time  $T_{\mathrm{P}}$ , which is the number of time units needed to burn all the sites, the length of the shortest path  $l_{\mathrm{p}}$  (Middlemiss et al 1980), which is the number of time units needed to burn  $\mathbf{P}_2$ , and the number of loops  $L_{\mathrm{P}}$  of the cluster, which is the number of times that one tries to burn a site  $\mathbf{P}_i$  that is already burned in the same time unit. The ordering of the cluster obtained in this first burning will be used in the next steps and is thus kept in mind. The second step is a burning starting at  $\mathbf{P}_2$  and with the additional condition that only those sites can be burned at time  $t_{i+1}$  which, in the ordering of the previous step, have a smaller value than those burned at time  $t_i$ . Due to this condition, only sites on the elastic backbone are now burned. Simultaneously one obtains the

---

Letter to the Editor

number of sites $S_{\mathrm{E}}$, of loops $L_{\mathrm{E}}$, and of cutting sites $C_{\mathrm{E}}$ of the elastic backbone; $C_{\mathrm{E}}$ is the number of time steps that only one site is burning. Also the maximal number $M_{\mathrm{E}}$ of sites that burn simultaneously can be obtained, and it is in some sense a measure of the broadness of the elastic backbone. Finally, the backbone is obtained by growing it from the elastic backbone. So before starting the third step the 'growing' backbone is equal to the elastic backbone. In the third step one burns from the sites $\mathbf{P}_i$, which were the sites at which loops were closed in the first burning. In this third burning again a site can only be burned at $t_{i+1}$ if its value (in the ordering from the first burning) is smaller than the value of the sites burned at $t_i$ but additionally the growing backbone cannot burn. Now the question is asked if starting at a given $\mathbf{P}_i$ the elastic backbone is reached at only one site or at several sites. In the case of several sites all the sites that have been burned from $\mathbf{P}_i$ are added to the growing backbone. This is done over and over again until no more parts can be attached to the growing backbone by burning from the $\mathbf{P}_i$. Then the backbone is complete. One can finally obtain the number of sites $S_{\mathrm{B}}$ or loops $L_{\mathrm{B}}$ of the backbone, for instance, by burning the backbone in the same way as in the first step. We note that the backbone constructed in this way depends on $\mathbf{P}_1$ and $\mathbf{P}_2$ in the same fashion as described above for the elastic backbone and also for the backbone the distance between $\mathbf{P}_1$ and $\mathbf{P}_2$ should ideally go to infinity.

We applied the above method to the largest (or incipient infinite) cluster of site percolation at $p_{\mathrm{c}}$ on a square lattice and a simple cubic lattice in finite boxes of edge length $L$. The endpoints $\mathbf{P}_1$ and $\mathbf{P}_2$ were determined to be as close as possible to diagonally opposing corners, but if their Euclidean distance was smaller than a number $\alpha$ the cluster was not considered and a new percolation configuration was chosen. This procedure prevents, due to statistical fluctuations, too small or deformed clusters being taken as prototypes for a spanning or 'infinite' clusters in a finite box. The parameter $\alpha$ can be changed and the results should not depend on $\alpha$ in the limit of large $L$. If $\alpha$ is too close to the length of the diagonal of the box, however, too many rejections of clusters will slow down the algorithm. The number of realisations (different samples taken) varies in two dimensions from 450 000 for $L = 10$ to 100 for $L = 500$ and in three dimensions from 500 for $L = 6$ to 100 for $L = 40$.

In two dimensions we use $p_{\mathrm{c}} = 0.59277$ (Gebele 1983). Our results are shown in figure 2. We also tested for $\alpha$ dependence; within error bars the results are the same for all values of $\alpha$. We find very straight lines for the sites of the backbone and the slope gives, because of finite size scaling and

$$
S _ {\mathrm {B}} \left(p _ {\mathrm {c}}\right) = L ^ {d} \rho_ {\mathrm {S}} ^ {\mathrm {B}} \left(p _ {\mathrm {c}}\right) \sim L ^ {d - \beta_ {\mathrm {B}} / \nu} = L ^ {D _ {\mathrm {B}}}, \tag {2}
$$

the fractal dimension of the backbone $D_{\mathrm{B}} = 1.60 \pm 0.05$. Note that the question of whether $\nu_{\mathrm{B}} = \frac{4}{3} = \nu$ (percolation) does not arise in equation (2). The points for the sites of the elastic backbone, of the shortest path and the cutting sites of the elastic backbone also lie on straight lines although with larger statistical deviations. They all have more or less the same slope of about 1.1. In the large $L$ limit it cannot be excluded that the slope(s) might go to unity, as may occur for the shortest path, but without extrapolating possible curvatures hidden in the error bars our data yield $D_{\mathrm{E}} = 1.10 \pm 0.05$ for the fractal dimension of the elastic backbone.

In three dimensions we work at $p_{\mathrm{c}} = 0.3117$ (Heermann and Stauffer 1981). Our results are shown in figure 3 for $\alpha = L$. The statistical errors are indicated for $L = 10$, where two independent runs are shown. All quantities seem to be critical as they show straight lines over a wide range with a slope different from one (compare with the broken line) and a curvature that would give a slope one for large values of $L$ seems

---

Letter to the Editor

![img-2.jpeg](img-2.jpeg)
Figure 2. Log-log plot showing dependence on  $L$  of the number of sites in the backbone  $S_{\mathrm{B}}(\times)$ , the elastic backbone  $S_{\mathrm{E}}(\triangle)$ , the shortest path  $l_{p}(\nabla)$  and red bonds in the elastic backbone  $S_{\mathrm{red}}(\square)$  for  $p_{\mathrm{c}} = 0.59277$ .

![img-3.jpeg](img-3.jpeg)
Figure 3. Log-log plot of the number of sites in the backbone  $S_{\mathrm{B}}(\times)$ , the number of sites in the elastic backbone  $S_{\mathrm{E}}(\triangle)$ , and the number of sites on one shortest path  $l_{p}(\nabla)$  against the system length  $L$  for three dimensions at  $p_{\mathrm{c}} = 0.3117$ . The broken line has slope 1.

extremely unlikely. The fractal dimension of the backbone is estimated to be  $D_{\mathrm{B}} = 1.77 \pm 0.07$  and the fractal dimension of the elastic backbone is, as in the two-dimensional case, equal to the fractal dimension of the shortest path and has a value of  $D_{\mathrm{E}} = 1.35 \pm 0.05$ . In figure 4 we show the number of loops of the largest cluster,

---

Letter to the Editor

![img-4.jpeg](img-4.jpeg)
Figure 4. Log-log plot of the number of loops of the largest cluster  $L_{p}(\square)$  backbone  $L_{\mathrm{B}}(\times)$  and elastic backbone  $L_{\mathrm{E}}(\bigcirc)$  against the system length in three dimensions at  $p_{c} = 0.3117$ .

the backbone and the elastic backbone. Within their statistical error bars, the three slopes agree with the corresponding fractal dimensions. This shows that for all the three objects the site and bond problems yield the same fractal dimension because of Euler's relation.

The values that we find for the fractal dimension of the backbone of percolation, in two dimensions: 1.60 and in three dimensions 1.77, are in fair agreement with the results of series expansion  $(1.80 \pm 0.05$  in  $d = 2$ ,  $1.83 \pm 0.08$  in  $d = 3$ , Hong and Stanley 1983a), Monte Carlo simulation (1.55-1.62 in 2D and 1.8-2.1 in 3D, Kirkpatrick 1978; 1.72 in 2D, Li and Strieder 1982), and PSRG (1.55 for  $d = 2$ , Hong and Stanley 1983b) and large-cell renormalisation ( $\sim$ 1.62 in 2D).

In summary, we have introduced a new critical object in percolation: the elastic backbone which, at least in three dimensions, has a non-trivial fractal dimension of about 1.35. It seems to be equivalent to the shortest path in the cluster. However, the elastic backbone does not explain the experimental discrepancy by nearly a factor of two between the conductivity and elasticity exponents (Adam et al 1981) because in addition to the effect shown in figure 1 a real gel will also have retrieving forces in the angles and volumes enclosing nearly incompressible fluids so that any deformation will contribute to the elasticity. We proposed a fast algorithm which obtains for any cluster not only the elastic backbone but also the usual backbone. The fractal dimension that we get for the usual backbone agrees with numerical work of other authors.

We thank E Guyon for useful discussions.

---

Letter to the Editor

Note added in proof. In two dimensions our result agrees well with recent calculations by Puech and Rammal (1983).

## References

Adam M, Delsanti M, Durand D, Hild G and Munch J P 1981 Pure Appl. Chem. 53 1489
Alexander S and Orbach R 1982 J. Physique Lett. 43 L625
Coniglio A 1981 Phys. Rev. Lett. 46 250
— 1982 J. Phys. A: Math. Gen. 15 3829
Daoud M 1983 J. Physique Lett to appear
de Gennes P G 1976 J. Physique Lett. 37 L1
Gebele T 1984 J. Phys. A: Math. Gen. 17 L51
Harris A B 1983 J. Phys. A: Math. Gen. 16 L365
Harris A B and Lubensky T C 1983 Preprint
Heermann D W and Stauffer D 1981 Z. Phys. B 44 339
Hong D C, Havlin S, Herrmann H J and Stanley H E 1984 Preprint
Hong D C and Stanley H E 1983a J. Phys. A: Math. Gen. 16 L475
— 1983b J. Phys. A: Math. Gen. 16 L525
Kirkpatrick S 1978 AIP Conf. Proc. 40 99
Li P S and Strieder W 1982 J. Phys. C: Solid State Phys. 15 L1235
Middlemiss K M, Whittington S G and Gaunt D S 1980 J. Phys. A: Math. Gen. 13 1835
Puech L and Rammal R 1983 J. Phys. C: Solid State Phys. 16 L1197
Pike R and Stanley H E 1981 J. Phys. A: Math: Gen. 14 L169
Shlifer G, Klein W, Reynolds P J and Stanley H E 1979 J. Phys. A: Math. Gen. 12 L169
Skal A and Shlovski B I 1975 Sov. Phys.-Semicond. 8 1029
Stanley H E 1977 J. Phys. A: Math. Gen. 10 L211
Stanley H E and Coniglio A 1984 Phys. Rev. B 29 522
Stauffer D 1984 Introduction to Percolation Theory ch 1 (London: Taylor and Francis) to be published
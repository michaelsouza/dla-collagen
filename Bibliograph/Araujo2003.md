PHYSICAL REVIEW E 67, 027102 (2003)

# Statistics of the critical percolation backbone with spatial long-range correlations

A. D. Araújo,¹,² A. A. Moreira,¹ R. N. Costa Filho,¹ and J. S. Andrade, Jr.¹

¹Departamento de Física, Universidade Federal do Ceará, 60451-970 Fortaleza, Ceará, Brazil

²Departamento de Física, Universidade Estadual Vale do Acaraú, 62040-370 Sobral, Ceará, Brazil

(Received 25 October 2002; published 24 February 2003)

We study the statistics of the backbone cluster between two sites separated by distance r in two-dimensional percolation networks subjected to spatial long-range correlations. We find that the distribution of backbone mass follows the scaling ansatz, P(M_B) ~ M_B^(α+1)f(M_B/M_0), where f(x) = (α + ηx^η)exp(-x^η) is a cutoff function and M_0 and η are cutoff parameters. Our results from extensive computational simulations indicate that this scaling form is applicable to both correlated and uncorrelated cases. We show that the exponent α can be directly related to the fractal dimension of the backbone d_B, and should therefore depend on the imposed degree of long-range correlations.

DOI: 10.1103/PhysRevE.67.027102

PACS number(s): 64.60.-i, 74.25.Qt, 47.55.Mh

# I. INTRODUCTION

Percolation is a useful model to study a variety of systems in many fields of science displaying structural disorder and statistical self-similarity. In particular, the percolation geometry has been frequently used as a simple paradigm to investigate fluid flow in porous media [1-3]. In this type of problem, the geometry underlying the system can be very complex and display heterogeneous features over a very wide range of length scales, going from centimeters to kilometers [4]. For example, an open question in the modeling process of oil recovery is the effect of the connectedness of the porous medium on the dynamical process of fluid displacement. If the pore space is so poorly connected as to be considered macroscopically heterogeneous, one expects the overall behavior of the flowing system to display significant anomalies. In this way, it is important to investigate the physics of disordered media at a marginal state of connectivity, for example, in terms of the geometry of the spanning cluster at the percolation threshold [5,6].

The most relevant subset of the percolation cluster for transport is the conducting backbone. It can be defined as the cluster that carries the current when a voltage difference is applied between two sites. Thus the backbone structure alone determines the conductivity of the whole percolation network. Recently, Barthélémy et al. [7] have shown that the average mass of the backbone ⟨M_B⟩ connecting two sites in a two-dimensional system of size L obeys the scaling form ⟨M_B⟩ ~ L^{d_B}G(r/L), where the function G(r/L) can be approximated by a power law for any value of r/L. Their results from numerical simulations with uncorrelated structures indicate that, for the case where r ≈ L, the distribution of backbone mass is peaked around L^{d_B}. When r ≪ L, the distribution follows a power-law behavior.

The fact that the geometry of real rocks is generally random does not necessarily imply that their disordered morphology is spatially uncorrelated. In other words, the probability for a small region in the system to have a given porosity (or permeability) may not be independent of the probability associated with other locations. This is certainly true for some types of rocks and geological fields where geometrical and/or transport properties can be adequately

characterized in terms of their spatial correlations [3]. It is under this framework that the correlated percolation model [8-11] represents a more realistic description for the pore space in terms of structure and transport. In a previous work [12], the hydrodynamic dispersion behavior of percolation porous media with spatial correlations has been investigated. More recently, we studied the displacement dynamics between two fluids flowing through correlated percolation clusters [13]. It was found that the presence of correlations can substantially modify the scaling behavior of the distributions of relevant transport properties and, therefore, their universality class. In the present paper we extend the previous work of Barthélémy et al. [7] to investigate the effect of spatial long-range correlations on the statistics of the backbone mass connecting two "wells" in a two-dimensional percolation geometry. In Sec. II, we present the mathematical model to simulate long-range spatial correlations. The results and analysis of the numerical simulations are shown in Sec. III, while the conclusions are presented in Sec. IV.

# II. MODEL

Our model for the porous medium is based on a two-dimensional site percolation cluster of size L at criticality [5] where correlations among the elementary units of the lattice are systematically introduced [10,11]. For a given realization of the correlated network, we extract the percolation backbone between two sites A and B separated by an Euclidean distance r ≪ L that belong to the infinite cluster and are sufficiently far from the edges of the system to prevent boundary effects. The correlations are induced by means of the Fourier filtering method, where a set of random variables u(r) is introduced following a power-law correlation function of the form

$$\langle u(\mathbf{r})u(\mathbf{r}+\mathbf{R})\rangle\propto R^{-\gamma}\quad[0<\gamma\leqslant2].\tag{1}$$

Here γ = 2 is the uncorrelated case and γ ≈ 0 corresponds to the maximum correlation. The correlated variables u(r) are used to define the occupancy ζ(r) of the sites

$$\zeta(\mathbf{r})=\Theta[\phi-u(\mathbf{r})],\tag{2}$$

1063-651X/2003/67(2)/027102(4)/$20.00

67 027102-1

©2003 The American Physical Society

---

BRIEF REPORTS

PHYSICAL REVIEW E 67, 027102 (2003)

![img-0.jpeg](img-0.jpeg)

![img-1.jpeg](img-1.jpeg)

FIG. 1. Log-log plot of the cumulative distribution of backbone mass for uncorrelated ($\gamma=2$, $r=8$, circles) and correlated networks ($\gamma=0.5$, $r=16$, squares). The solid lines correspond to the scaling function, Eq. (4), with the same values of the parameters obtained from the best fit to the data of Eq. (5).

where $\Theta$ is the Heaviside step function and the parameter $\phi$ is chosen to produce a network at the percolation threshold. Due to computational limitations, we restricted our simulations to two values of $\gamma=2$ and 0.5, corresponding to uncorrelated and correlated percolation structures, respectively. For each value of $\gamma$, we performed simulations for 100 000 network realizations of size $L \times L$, where $L=1024$, and different values of the "well" distance $r$ to compute the distribution $P(M_B)$ and the cumulative distribution $F(M_B)$ of backbone mass

$$F(M_B) = \int_{M_B}^{\infty} P(M) dM. \tag{3}$$

### III. RESULTS

In Fig. 1 we show the log-log plot of typical cumulative distributions of backbone mass $F(M_B)$ for uncorrelated as well as correlated morphologies. It is clear from this figure that $F(M_B)$ displays power-law behavior for intermediate mass values in both cases. In addition, the scaling region is followed by a sudden cutoff that decays faster than exponential. A similar behavior has been observed experimentally [14] and through numerical simulations [15–18] for the phenomenon of impact fragmentation. Based on these features, we argue that $F(M_B)$ should obey the following scaling ansatz:

$$F(M_B) \sim M_B^{-\alpha} \exp\left[-\left(\frac{M_B}{M_0}\right)^\eta\right], \tag{4}$$

where $\alpha$ is a scaling exponent and $M_0$ and $\eta$ are cutoff parameters. For comparison with the approach presented in Ref. [7], here we determine these parameters from the simu-

FIG. 2. Log-log plot of the distribution of backbone mass of uncorrelated percolation networks for $L=1024$ and $r=8$ (circles), 16 (triangles up), 32 (squares), 64 (triangles down), and 128 (diamonds). The solid line is the best fit of Eq. (5) to the data for the scaling region and lower cutoff, with parameters $\alpha=0.255$, $\eta=1.5$, and $M_0=3.32 \times 10^4$.

lation results in terms of their corresponding distributions of backbone mass $P(M_B)$. From Eq. (4), it follows that

$$P(M_B) \sim M_B^{-(\alpha+1)} f(M_B/M_0), \tag{5}$$

where the function $f(M_B/M_0)$ has the form

$$f(M_B/M_0) = \left[\alpha + \eta\left(\frac{M_B}{M_0}\right)^\eta\right] \exp\left[-\left(\frac{M_B}{M_0}\right)^\eta\right]. \tag{6}$$

Figure 2 shows the distributions $P(M_B)$ generated for the uncorrelated case ($\gamma=2$) and different values of $r$. They all display a lower cutoff of order $r$ (the smallest backbone possible is a straight line connecting points $A$ and $B$) and an upper cutoff of order $L^{D_B}$, where a "bump" can also be observed [7]. For comparison, each of these distributions has been rescaled by its corresponding value at the position of this bump. The smaller the distance $r$ is between the wells, larger is the range over which the scaling term of Eq. (5) holds, $P(M_B) \sim M_B^{-(\alpha+1)}$. The solid line in Fig. 2 corresponds to the best nonlinear fit we found for the $r=8$ data in both the scaling and cutoff zones with $\alpha=0.255$, $M_0=3.32 \times 10^4$, and $\eta=1.5$. Because the sampling of the backbone mass should be equivalent to the sampling of blobs in the percolation cluster [19], it is possible to draw a direct relation between the scaling exponent $\alpha$ and the fractal dimension of the backbone [20]. Accordingly, the exponent $\tau$ governing the blob size distribution can be calculated as $\tau = d/d_B + 1$. Since the exponent $\tau_B = \alpha + 1$ governs the statistics of the entire backbone, we obtain by integration that $\alpha = d/d_B - 1$, which gives a fractal dimension of $d_B \approx 1.6$. This is in good agreement with the current numerical estimate of $d_B = 1.6432 \pm 0.0008$ [21].

027102-2

---

BRIEF REPORTS

PHYSICAL REVIEW E 67, 027102 (2003)

![img-2.jpeg](img-2.jpeg)

![img-3.jpeg](img-3.jpeg)

FIG. 3. Log-log plot of the distribution of backbone mass of correlated percolation networks for $L=1024$ and $r=16$ (circles), 32 (triangles up), 64 (squares), and 128 (triangles down). The solid line is the best fit of Eq. (5) to the data for the scaling region and lower cutoff, with parameters $\alpha=0.075$, $\eta=2.0$, and $M_0=5.4\times10^5$. The degree of correlation is $\gamma=0.5$.

We now turn to the case with spatial long-range correlations. As shown in Fig. 3, Eq. (5) (solid line) also fits very well the simulation data for $P(M_B)$ with $\gamma=0.5$ and $r=16$, both in the scaling region and in the cutoff zone. The parameter set obtained with a nonlinear estimation algorithm includes $\alpha=0.075$, $M_0=5.4\times10^5$, and $\eta=2$. Compared to the uncorrelated geometry, the results shown in Fig. 3 for large masses clearly indicate the presence of a narrow plateau followed by a much more pronounced bump and a sharper cutoff profile. These features are consistent with the exponent $\alpha\approx0$ and also reflect the fact that $\eta$ is significantly larger for the correlated case. The resulting fractal dimension of the backbone $d_B\approx1.86$ is in good agreement with previous estimates for correlated structures generated with $\gamma=0.5$ [10,13].

![img-4.jpeg](img-4.jpeg)

For completeness, we show that the scaling ansatz used to fit the simulation results for $P(M_B)$ is consistent with the observed behavior for $F(M_B)$ over the whole range of relevant backbone masses. Precisely, the solid lines in Fig. 1 correspond to Eq. (3) with the same set of parameters used to fit the simulation data for $\gamma=0.5$ and 2 in terms of Eq. (5). Although close to zero, the value of $\alpha=0.075$ for the correlated geometry is sufficiently large to characterize the power-law signature of the cumulative mass distribution $F(M_B)$. The differences in the exponent $\alpha$ obtained for correlated and uncorrelated cases can be explained in terms of the morphology of the conducting backbone. As $\gamma$ decreases, the backbone becomes gradually more compact [10]. This distinctive aspect of the correlated geometry tends to increase the value of $d_B$, and therefore reduce the value of $\alpha$ as the strength of the long-range correlations increases (i.e., $\gamma$ decreases). As in Ref. [7], here we also investigate the scaling behavior of the average backbone mass $\langle M_B \rangle$, but for a correlated geometry. In Fig. 4 we show the log-log plot of $\langle M_B \rangle$

FIG. 4. Log-log plot of the average backbone mass $\langle M_B \rangle$ for correlated structures ($\gamma=0.5$) against the distance $r$ for $L=1024$ (circles), 512 (triangles), and 256 (squares). The inset shows the best data collapse obtained by rescaling $M_B$ and $r$ to $L^{1.85}$ and $L$, respectively. The least-squares fit to the data gives the scaling exponent $\psi=0.17\pm0.03$.

against $r$ for $\gamma=0.5$ and three different values of $L$. The approximation proposed in Ref. [7] for uncorrelated networks when $r \ll L$ reveals that $\langle M_B \rangle$ should scale as

$$\langle M_B \rangle \sim L^{d_B - \psi} r^\psi, \tag{7}$$

where the exponent $\psi$ is the codimension of the fractal backbone, i.e., $\psi=d-d_B$. Using Eq. (7) and $d_B=1.85$, the inset of Fig. 4 shows the data collapse obtained by rescaling $M_B$ and $r$ to the corresponding values of $L^{d_B}$ and $L$, respectively. From the least-squares fit to the data in the scaling region,

FIG. 5. Data collapse of the distribution of backbone mass for correlated networks ($\gamma=0.5$) and three values of $r\approx L$. For each value of $L$, 100 000 realizations have been generated to produce the statistics. Equation (8) with $d_B=1.86$ has been used to collapse the results.

027102-3

---

BRIEF REPORTS

PHYSICAL REVIEW E 67, 027102 (2003)

we obtain the exponent $\psi=0.17\pm0.03$. This result is in good agreement with the estimated value 0.15 for the fractal codimension.

Finally, it is also interesting to investigate the case where $r\approx L$. As for uncorrelated clusters [7], we expect the distribution $P(M_B)$ for correlated geometries to obey the simple scaling form

$$P(M_B) \sim \frac{1}{L^{d_B}} g \left( \frac{M_B}{L^{d_B}} \right), \tag{8}$$

where $g$ is a scaling function. In Fig. 5 we show results from simulations with correlated networks generated with $\gamma=0.5$ for $r\approx L$ and three different values of $L$. It can be seen that the probability distribution is peaked around an average value $\langle M_B \rangle$ of the order of $L^{d_B}$. As depicted, Eq. (8) can indeed be used to collapse the data. The value adopted for the fractal dimension of the backbone, $d_B=1.86$, is compatible with the corresponding degree of correlation imposed.

## IV. SUMMARY

We have studied the scaling characteristics of the backbone mass distribution between two sites in two-dimensional percolation lattices subjected to long-range correlations. A scaling ansatz that is capable of describing the power-law region as well as the complex details of the cutoff profile is proposed, and it is shown to be applicable for both correlated and uncorrelated structures. Based on the results of extensive simulations, we find that the presence of long-range correlations can substantially modify the scaling exponents of these distributions and, therefore, their universality class. We explain this change of behavior in terms of the morphological differences among uncorrelated and correlated pore spaces generated at criticality. Compared to the uncorrelated case, the backbone clusters with spatial long-range correlations have a more compact geometry. The level of compactness depends, of course, on the degree of correlations $\gamma$ introduced during the generation process.

## ACKNOWLEDGMENTS

This work was supported by CNPq, CAPES, and FUNCAP.

[1] J. Bear, Dynamics of Fluids in Porous Materials (Elsevier, New York, 1972).

[2] F. A. Dullien, Porous Media - Fluid Transport and Pore Structure (Academic, New York, 1979).

[3] M. Sahimi, Flow and Transport in Porous Media and Fractured Rock (VCH, Boston, 1995), and the extensive references therein.

[4] P. R. King, in North Sea Oil and Gas Reservoirs III, edited by A. T. Buller et al. (Graham and Trotman, London, 1990).

[5] D. Stauffer and A. Aharony, Introduction to Percolation Theory (Taylor Francis, Philadelphia, 1994).

[6] Fractals and Disordered Systems, 2nd ed., edited by A. Bunde and S. Havlin (Springer-Verlag, New York, 1996).

[7] M. Barthélémy, S.V. Buldyrev, S. Havlin, and H.E. Stanley, Phys. Rev. E 60, R1123 (1999).

[8] S. Havlin, R.B. Selinger, M. Schwartz, H.E. Stanley, and A. Bunde, Phys. Rev. Lett. 61, 1438 (1988).

[9] S. Havlin, M. Schwartz, R.B. Selinger, A. Bunde, and H.E. Stanley, Phys. Rev. A 40, 1717 (1989).

[10] S. Prakash, S. Havlin, M. Schwartz, and H.E. Stanley, Phys.

Rev. A 46, R1724 (1992).

[11] H.A. Makse, S. Havlin, M. Schwartz, and H.E. Stanley, Phys. Rev. E 53, 5445 (1996).

[12] H.A. Makse, J.S. Andrade, Jr., and H.E. Stanley, Phys. Rev. E 61, 583 (2000).

[13] A.D. Araújo, A.A. Moreira, H.A. Makse, H.E. Stanley, and J.S. Andrade, Jr., Phys. Rev. E 66, 046304 (2002).

[14] A. Meibom and I. Balslev, Phys. Rev. Lett. 76, 2492 (1996).

[15] H. Inaoka, E. Toyosawa, and H. Takayasu, Phys. Rev. Lett. 78, 3455 (1997).

[16] A. Diehl, H.A. Carmona, L.E. Araripe, J.S. Andrade, Jr., and G.A. Farias, Phys. Rev. E 62, 4742 (2000).

[17] J.A. Aström, R.P. Linna, and J. Timonen, Phys. Rev. E 65, 048101 (2002).

[18] A. Diehl, J.S. Andrade, Jr., and G.A. Farias, Phys. Rev. E 65, 048102 (2002).

[19] H.E. Stanley, J. Phys. A 10, L211 (1977).

[20] H.J. Herrman and H.E. Stanley, Phys. Rev. Lett. 53, 1121 (1984).

[21] P. Grassberger, Physica A 262, 251 (1999).

027102-4
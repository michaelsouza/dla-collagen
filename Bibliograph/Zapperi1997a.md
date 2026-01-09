VOLUME 78, NUMBER 8

PHYSICAL REVIEW LETTERS

24 FEBRUARY 1997

# First-Order Transition in the Breakdown of Disordered Media

Stefano Zapperi,¹ Purusattam Ray,² H. Eugene Stanley,¹ and Alessandro Vespignani³

¹Center for Polymer Studies and Department of Physics, Boston University, Boston, Massachusetts 02215

²The Institute of Mathematical Sciences, CIT Campus, Madras 600 113, India

³Instituut-Lorentz, University of Leiden, P.O. Box 9506, 2300 RA, Leiden, The Netherlands

(Received 3 December 1996)

We study the approach to global breakdown in disordered media driven by increasing external forces. We first analyze the problem by mean-field theory, showing that the failure process can be described as a first-order phase transition, similarly to the case of thermally activated fracture in homogeneous media. Then we quantitatively confirm the predictions of the mean-field theory using numerical simulations of discrete models. Widely distributed avalanches and the corresponding mean-field scaling are explained by the long-range nature of elastic interactions. We discuss the analogy of our results to driven disordered first-order transitions and spinodal nucleation in magnetic systems. [S0031-9007(97)02501-5]

PACS numbers: 05.70.Ln, 62.20.Mk, 64.60.Fr

The breakdown of solids under external forces is a longstanding problem that has both theoretical and practical relevance [1]. The first theoretical approach to fracture mechanics, proposed by Griffith [2] more than 75 years ago, is similar to the classical theory of nucleation in first-order phase transitions [3]. An elastic solid under stress is in a "metastable state" and will decay to the "stable fractured state" by the formation of cracks. Recently it has been shown [4] that the point of zero external stress has the same mathematical properties as the condensation point in gas-liquid first-order transitions. In the language of phase transitions, the stress imposed on the solid plays the role of an external field and cracks are the analog of droplets of a new phase. The classical theory of nucleation is expected to fail close to the limit of stability, the spinodal point [5], and it has been suggested [6-9] that a similar behavior should occur for fracture, for large values of the external stress. Thus, the failure threshold corresponds to the spinodal point of first-order phase transitions.

The Griffith theory and related calculations deal with the situation in which fracture is thermally activated and quenched disorder is absent or weak. In many realistic situations, however, the solid is not homogeneous, and disorder, in the form of vacancies or microcracks, strongly affects the nucleation process [8,9]. There are situations, encountered, for example, in material testing, in which the system is driven by an increasing external stress [11] and the time scale of thermal fluctuations is much larger than the time scale induced by the driving. In those cases, the system can be effectively considered as being at zero temperature, so only quenched disorder is relevant. It has been experimentally observed [10-14] that the response (acoustic emission) of stressed disordered media takes place in bursts of widely distributed intensity, indicative of an internal avalanche dynamics.

The understanding of the breakdown of disordered systems has considerably progressed due to the use of large scale simulations of lattice models [15]. These models

have provided a good description of geometrical and topological properties of cracks, leading to the introduction in this field of scaling concepts. Recently, these models have also been used to study the dynamic response of the system before breakdown [16-20]. Scaling and power-law avalanche distributions were observed, in agreement with experiments, but a clear theoretical interpretation of the results is still lacking. Here, we address the problem by mean-field calculations and numerical simulations. The picture that emerges from our analysis is that the breakdown in disordered media can be described by a first-order transition, similarly to the case of thermally activated homogeneous fracture. Since elastic interactions are long range, scaling behavior may be present also in low dimensions, in analogy with spinodal nucleation [5].

The models we will consider are defined for a two-dimensional lattice of linear size $L$. Each bond of the lattice represents an elastic spring that breaks when it is stretched beyond a threshold chosen from a given probability distribution. An external stress is imposed on the system by suitably chosen boundary conditions. A simple example, because of the scalar nature of the interactions, is the random fuse model [21] for electric breakdown. With each bond $i$ is associated a resistor of unit conductivity $(\sigma_{i} = 1)$. When the current in the bond exceeds a threshold $D_{i}$ the bond becomes an insulator $(\sigma_{i} = 0)$. A slowly increasing external current [22] is imposed on the lattice and the voltage drops $(\Delta V)_i$ for each bond are computed by minimizing the total dissipated energy

$$
E (\{\sigma \}) \equiv \frac {1}{2} \sum_ {i} \sigma_ {i} \left(\left(\Delta V\right) _ {i} ^ {2} - D _ {i} ^ {2}\right). \tag {1}
$$

The dynamics of the model results from a double minimization process. The voltage drops $(\Delta V)_i$ are obtained by a global minimization of the energy at fixed $\sigma_{i}$, while the $\sigma_{i}$ are then chosen to minimize the local bond energy. This last step corresponds to breaking the bonds for which

0031-9007/97/78(8)/1408(4)$10.00

© 1997 The American Physical Society

---

VOLUME 78, NUMBER 8
PHYSICAL REVIEW LETTERS
24 FEBRUARY 1997

the current overcomes the threshold. The external current is increased slowly until the lattice is no longer conducting. We note that this dynamics is very similar in spirit to that of a field-driven random-field Ising model (RFIM), studied by Sethna et al. [23,24] in the context of magnetic hysteresis. In that model, each spin chooses the sign of the local field.

To derive a mean-field theory, it is useful to recast the dynamics of the model in terms of the externally applied current $I$. In full generality, we can rewrite the energy of Eq. (1) as

$$
E(I, \{\sigma\}) = \frac{1}{2} \left(\frac{I^2}{G(\{\sigma\})}, -\sum_i \sigma_i D_i^2\right), \tag{2}
$$

where $G(\{\sigma\})$ is the total conductivity of the lattice and is a complicated function of the local conductivities. We can estimate $G(\{\sigma\})$ using the effective medium theory [25], which in our case gives

$$
G(\{\sigma\}) = 2\phi - 1, \tag{3}
$$

where $\phi \equiv \sum_i \sigma_i / L^2$. We can express the energy as a sum over "spins" interacting with effective random fields $h_i$

$$
\begin{aligned}
E_{MF}(I, \{\sigma\}) &amp;= \sum_i \sigma_i h_i \\
&amp;= \frac{1}{2} \sum_i \sigma_i \left(\frac{I^2}{L^2 \phi (2\phi - 1)} - D_i^2\right). \tag{4}
\end{aligned}
$$

the value of $\phi$ can be computed self-consistently as

$$
\phi = P(h_i &gt; 0) = 1 - \int_0^{I/L \phi \sqrt{(2\phi - 1)}} \rho(D) \, dD, \tag{5}
$$

where $\rho(D)$ is the distribution of failure thresholds. The solution of this equation can be expressed in terms of the current per unit length $f \equiv I / L$. We can identify $f$ with the external field and $\phi$ with the order parameter.

From considerations similar to those presented in Ref. [24], we can show that for any analytic [26] normalizable distribution function $\rho$ Eq. (5) has a solution for $f &lt; f_c$ and, close to $f_c$, $\phi$ scales as

$$
\phi - \phi_c \sim (f_c - f)^{1/2}. \tag{6}
$$

The mean-field theory we have presented can be exactly mapped to the democratic fiber-bundle model (DFBM), an exactly solvable model for fracture which has been studied extensively [27]. We can, therefore, obtain the mean-field avalanche size distribution from the exact results derived for the DFBM [27]

$$
P(m) \sim m^{-\tau} f\left(m(f_c - f)^\kappa\right); \quad \tau = \frac{3}{2}, \quad \kappa = 1, \tag{7}
$$

where $m$ is the number of bonds that break as a function of the current. The average avalanche size $\langle m \rangle$ is proportional

to the "susceptibility" $d\phi / df$ [17], and therefore diverges at the breakdown as

$$
\langle m \rangle \sim (f_c - f)^{-\gamma}, \quad \gamma = 1/2. \tag{8}
$$

The exponents we have introduced satisfy the scaling relation $\kappa(2 - \tau) = \gamma$, which is consistent with the values reported in Eqs. (7) and (8). The mean-field analysis indicates that the system is undergoing a first-order transition since the order parameter has a discontinuity and the conductivity at $f_c$ has a finite jump from $G(\phi_c) &gt; 0$ to zero. The approach to this transition is characterized by avalanches of increasing size, diverging at the transition.

A similar behavior with the same scaling exponents is observed in the mean-field theory of the driven RFIM [23,24] for small disorder. In the RFIM, one observes also a second-order transition as the width of the disorder is increased. A similar transition does not seem to be present in our system, at least not in the mean-field treatment. It is also interesting to note that the same scaling laws describe metastable systems close to a spinodal point. The quasistatic susceptibility diverges as in Eq. (8) and droplets are distributed according to Eq. (7).

An important issue to address at this point is the validity of mean-field results in the case of real low-dimensional systems. It is known that scaling does not hold close to the first-order transition for short-ranged RFIM in dimensions $d = 2,3$ [23,24]. Similarly, spinodal singularities are observed when interactions are long range [28]. Elastic interactions are intrinsically long range, which leads to mean-field behavior even for low dimensions, as we will next show numerically. We simulate the random fuse model [21] on a tilted square lattice, with periodic boundary conditions in the transverse direction. The current in each bond is computed numerically by solving the Kirchhoff equations with a precision $\epsilon = 10^{-10}$. The distribution of thresholds is chosen to be uniform in the interval $[1 - \Delta, 1 + \Delta]$. We made the choice $\Delta = 1$ in order to avoid the "ductile-brittle" crossover at a finite value of the lattice size [21]. Other broad analytic distributions give rise to similar results. We impose an external current $I$ through the lattice, and we increase it at an infinitesimal rate. When a bond fails, we recompute the currents to see if other failures occur. The system responds to the increase of the current with avalanches whose size $m$ diverges at the breakdown $f_c$. In Fig. 1 we plot the average avalanche size $\langle m \rangle$ versus $I / L$, and we see that the mean-field exponent $\gamma = 1/2$ fits the data quite well. The data collapse is not perfect because logarithmic corrections are expected in $d = 2$ [21]. The avalanche size distribution, integrated over the entire range of the current, is plotted in Fig. 2. We see that the scaling is consistent with an exponent $\tau' = \tau + 1/\kappa = 5/2$, which results from the mean-field calculations [Eq. (7)]. As expected the cutoff of the distribution increases with $L$.

We have studied the behavior of the average crack size $\langle s \rangle$ as a function of the current. Although the crack size

---

VOLUME 78, NUMBER 8

PHYSICAL REVIEW LETTERS

24 FEBRUARY 1997

![img-0.jpeg](img-0.jpeg)
FIG. 1. The average avalanche size $\langle m\rangle^{-1 / \gamma}$ is plotted as a function of $I / L$, using the mean-field value $\gamma = 1 / 2$. The curves are averaged over several realizations of the disorder ($N = 500$ for $L = 32$, $N = 100$ for $L = 64, 128$). The critical current of the random fuse model $I_{c} / L$ has logarithmic corrections, so the curves do not superpose.

grows with the current, it does not appear to diverge at the breakdown when the system size is increased. This implies that the final macroscopic crack is formed by the coalescence of several microcracks, rather than by the growth of a single crack. In fact, by monitoring the dynamics, we observe that avalanches are not spatially connected since interactions are long range; this may be the reason why mean field works so well for these systems. Finally, we have checked that the conductivity of the lattice displays a finite jump at the first-order transition.

![img-1.jpeg](img-1.jpeg)
FIG. 2. The avalanche size distribution for a random fuse model of size $L = 32$ and $L = 128$ is plotted in log-log scale. A line with the mean-field value $\tau' = 5/2$ of the exponent is plotted for reference. The cutoff of the distribution increases with the system size.

The mean-field theory was derived for the case of a scalar model, but the results do not only apply to scalar models. We have numerically simulated a more complex vectorial model, defined in Ref. [18]. The model is a spring network with central and bond bending forces, with random failure thresholds associated with each bond. The system is driven by an increasing external stress $f$, and the dynamics is obtained by numerically integrating the equations of motion of the springs. The model gives a more reliable description of the fracture process, taking into account the tensorial nature of the elastic interactions and a realistic relaxation dynamics. In this case we also find power-law distributed avalanches and mean-field exponents (see Fig. 3). A detailed account of the results of this model, as well as a complete discussion of the random fuse model, will be reported elsewhere [29].

The results we have discussed clarify the nature of the breakdown process in the presence of quenched disorder. We have shown that the breakdown corresponds to a first-order transition, with avalanche precursors characterized by power laws. The scaling exponents are in quantitative agreement with the prediction of mean-field calculations. In mean-field theory, driven disordered systems behave similarly to their homogeneous, thermally driven, counterparts, if we compare the scaling of avalanches with that of the droplets. This applies to the RFIM [23,24], which shows features similar to those of spinodal nucleation [5], and to the fracture models we have studied. However, one should be careful not to interpret these analogies too strictly, since in driven disordered systems the notions of metastability, spinodal point, and nucleation are not well defined.

Finally, we comment on the applicability of self-organized criticality (SOC) [30] to fracture problems. In fact, first-order transitions and SOC are becoming the principal competing theoretical frameworks for the interpretation of avalanche phenomena in disordered systems.

![img-2.jpeg](img-2.jpeg)
FIG. 3. The susceptibility $d\phi / df$ for the spring network of size $L = 50$, averaged over $N = 100$ configurations, is plotted as function of the applied stress $f$. Mean-field scaling ($\gamma = 1/2$) appears to be very good also in this case.

---

VOLUME 78, NUMBER 8

PHYSICAL REVIEW LETTERS

24 FEBRUARY 1997

A striking example of this controversy is represented by earthquake phenomena [31]. The definition of SOC implies a slowly driven system with a critical stationary state [32]. The only possibility to observe SOC behavior in fracture phenomena is in the presence of a long lived plastic state before rupture. Recently proposed scalar models [33] of microfractures and molecular dynamics simulations of granular solids under shear [34] have shown that the plastic stationary state is characterized by power-law avalanche distributions suggestive of SOC. On the other hand, the model studied in Ref. [19] that was claimed to display SOC has no stationary state, like the models discussed here. Power laws without cutoff in this case arise not due to self-organization, but because the control parameter is externally "swept" towards the instability (as pointed out by Sornette [35]). We believe that different experimental conditions can all give rise to similar scaling behavior, but the underlying physical mechanisms could be quite different.

The Center for Polymer Studies is supported by the NSF. We thank P. Cizeau, W. Klein, and F. Sciortino for interesting discussions and remarks.

[1] Non-linearity and Breakdown in Soft Condensed Matter, edited by K.K. Bardhan, B.K. Chakrabarti, and A. Hansen (Springer-Verlag, Berlin/New York, 1994).
[2] A.A. Griffith, Phil. Trans. R. Soc. London A 221, 163 (1920).
[3] J.D. Gunton, M. San Miguel, and P.S. Sahini, in Phase Transitions and Critical Phenomena, edited by C. Domb and J.L. Lebowitz (Academic, London, 1983), Vol. 8.
[4] A. Buchel and J.P. Sethna, Phys. Rev. Lett. 77, 1520 (1996); cond-mat/9610008.
[5] C. Unger and W. Klein, Phys. Rev. B 29, 2698 (1984); 31, 6127 (1985); for a review, see L. Monette, Int. J. Mod. Phys. B 8, 1417 (1994).
[6] J.B. Rundle and W. Klein, Phys. Rev. Lett. 63, 171 (1989).
[7] R. L. B. Selinger, Z.-G. Wang, W. M. Gelbart, and A. Ben-Saul, Phys. Rev. A 43, 4396 (1991).
[8] R. L. B. Selinger, Z.-G. Wang, and W. M. Gelbart, J. Chem. Phys. 95, 9128 (1991).
[9] L. Golubovic and A. Pedrera, Phys. Rev. E 51, 2799 (1995); L. Golubovic and S. Feng, Phys. Rev. A 43, 5223 (1991).
[10] H. Strauven, G. Claes, G. Heylen, G. Crevecoer, and C. Maes (to be published).
[11] J.-C. Anifrani, C. Le Floc'h, D. Sornette, and B. Souillard, J. Phys. I 5, 631 (1995).
[12] A. Petri, G. Paparo, A. Vespignani, A. Alippi, and M. Costantini, Phys. Rev. Lett. 73, 3423 (1994).
[13] G. Cannelli, R. Cantelli, and F. Cordero, Phys. Rev. Lett. 70, 3923 (1993).

[14] P. Diodati, F. Marchesoni, and S. Piazza, Phys. Rev. Lett. 67, 2239 (1991).
[15] Statistical Models for the Fracture of Disordered Media, edited by H.J. Herrmann and S. Roux (North-Holland, Amsterdam, 1990).
[16] F. Tzschichholz and H.J. Herrmann, Phys. Rev. E 51, 1961 (1995).
[17] M. Acharaya and B.K. Chakrabarti, Phys. Rev. E 53, 140 (1996); M. Acharaya, P. Ray, and B.K. Chakrabarti, Physica (Amsterdam) 224A, 287 (1996).
[18] P. Ray and G. Date, Physica (Amsterdam) 229A, 26 (1996).
[19] G. Caldarelli, F. Di Tolla, and A. Petri, Phys. Rev. Lett. 77, 2503 (1996).
[20] M. Sahimi and S. Arbabi, Phys. Rev. Lett. 77, 3689 (1996).
[21] L. de Arcangelis, S. Redner, and H.J. Herrmann, J. Phys. Lett. (Paris) 46, L585 (1985); P. Duxbury, P.D. Beale, and P.L. Leath, Phys. Rev. Lett. 57, 1052 (1986); B. Kahng, G.G. Batrouni, S. Redner, L. de Arcangelis, and H.J. Herrmann, Phys. Rev. B 37, 7625 (1988); L. de Arcangelis and H.J. Herrmann, Phys. Rev. B 39, 2678 (1989).
[22] The total current represents the electric analog of the applied load, while the voltage drop corresponds to the strain.
[23] J.P. Sethna, K. Dahmen, S. Karta, J.A. Krumhansl, and J.D. Shore, Phys. Rev. Lett. 70, 3347 (1993).
[24] K. Dahmen and J.P. Sethna, Phys. Rev. B 53, 14872 (1996).
[25] S. Kirkpatrick, Rev. Mod. Phys. 45, 574 (1973).
[26] The results are also valid in the case of the uniform distribution we use in simulations, as can be shown by a direct calculation.
[27] H.E. Daniels, Proc. R. Soc. London A 183, 405 (1945); S.L. Phoenix and H.M. Taylor, Adv. Appl. Prob. 5, 200 (1973); P.C. Hemmer and A. Hansen, J. Appl. Mech. 59, 909 (1992); D. Sornette, J. Phys. A 22, L243 (1989); J. Phys. I (France) 2, 2089 (1992).
[28] D. Heermann, W. Klein, and D. Stauffer, Phys. Rev. Lett. 49, 1262 (1982); T. Ray and W. Klein, J. Stat. Phys. 61, 891 (1990).
[29] S. Zapperi, P. Ray, H.E. Stanley, and A. Vespignani (to be published).
[30] P. Bak, C. Tang, and K. Wiesenfeld, Phys. Rev. Lett. 59, 381 (1987).
[31] A SOC model for earthquakes is presented in Z. Olami, H.J.S. Feder, and K. Christensen, Phys. Rev. Lett. 68, 1244 (1992). An interpretation of the phenomenon in terms of spinodals and first-order transitions is discussed in J.B. Rundle, W. Klein, and S. Gross, Phys. Rev. Lett. 76, 4285 (1996).
[32] A. Vespignani, S. Zapperi, and V. Loreto, Phys. Rev. Lett. 77, 4560 (1996).
[33] S. Zapperi, A. Vespignani, and H.E. Stanley, Mater. Res. Soc. Symp. Proc. 409, 355 (1996).
[34] H.J. Tillemans and H.J. Herrmann, Physica (Amsterdam) 217A, 261 (1995).
[35] D. Sornette, J. Phys. I (France) 4, 209 (1994).
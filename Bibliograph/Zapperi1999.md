PHYSICAL REVIEW E
VOLUME 59, NUMBER 5
MAY 1999

# Avalanches in breakdown and fracture processes

Stefano Zapperi,¹ Purusattam Ray,² H. Eugene Stanley,³ and Alessandro Vespignani⁴
¹PMMH-ESPCI, 10 Rue Vauquelin, 75231 Paris Cedex 05, France
²The Institute of Mathematical Sciences, CIT Campus, Chennai 600 113, India
³Center for Polymer Studies and Department of Physics, Boston University, Boston, Massachusetts 02215
⁴The Abdus Salam International Centre for Theoretical Physics (ICTP), P.O. Box 586, 34100 Trieste, Italy
(Received 6 November 1998)

We investigate the breakdown of disordered networks under the action of an increasing external—mechanical or electrical—force. We perform a mean-field analysis and estimate scaling exponents for the approach to the instability. By simulating two-dimensional models of electric breakdown and fracture we observe that the breakdown is preceded by avalanche events. The avalanches can be described by scaling laws, and the estimated values of the exponents are consistent with those found in mean-field theory. The breakdown point is characterized by a discontinuity in the macroscopic properties of the material, such as conductivity or elasticity, indicative of a first-order transition. The scaling laws suggest an analogy with the behavior expected in spinodal nucleation. [S1063-651X(99)09205-3]

PACS number(s): 05.65.+b, 62.20.Fe, 62.20.Mk

# I. INTRODUCTION

The breakdown of solids under external forces is a longstanding problem that has practical and theoretical relevance [1]. The first theoretical approach to fracture mechanics dates back to the 1920s with Griffith's theory [2] which says that cracks grow or heal, depending on whether the external stress prevails over the resistance at the surface of the crack. Since the work of Griffith, a great effort has been devoted to experimentally test the validity of the theory and to extend it to various crack geometries and boundary conditions [4]. The Griffith theory, in spirit, is very similar to the classical theory of nucleation in first-order phase transitions [3]. In bubble nucleation, a critical droplet will form when the change in free energy due to the bulk forces exceeds that of the surface terms.

The analogy between first-order transitions and fracture has been investigated further by numerical model and theoretical calculations. Several authors suggested that the breakdown point in a thermally activated fracture is analogous to a spinodal point. Spinodal nucleation [5], contrary to classical nucleation, is characterized by scaling properties and fractal droplets. Rundle and Klein [6], analyzing a Landau-Ginzburg equation for the growth of a single crack, showed that the system obeys scaling laws expected for spinodal nucleation. Selinger et al. [7,8] have studied the problem in mean-field theory and by numerical simulation. They conclude that a solid under stress is in a metastable state and when the external stress is raised beyond a critical value, corresponding to the spinodal point, the system becomes unstable. The nature of the nucleation process in a stressed solid was studied by Golubovic and co-workers [9] using Monte Carlo simulations. Recently, in the framework of elastic theory, it was shown [10] that the point of zero external stress corresponds to the condensation point in gas-liquid first-order transitions. One of the ambitious goals of these and other studies is to formulate a statistical thermodynamics of fracture processes.

Most of the theoretical studies we have discussed deal

with the situation in which fracture is thermally activated and quenched disorder is irrelevant. In most realistic situations, however, the solid is not homogeneous and disorder, in the form of vacancies or microcracks, strongly affects the nucleation process [8,9]. For example, cracks may start from different defects and coalesce [11], in contrast with the assumptions of Griffith-like theories. There are situations, encountered, for example, in material testing, in which the system is driven by an increasing external stress and the time scale of thermal fluctuations is larger than the time scale induced by the driving. In those cases, the system can effectively be considered as being at zero temperature and only quenched disorder is relevant. This is the situation we investigate in this paper. It is also worth emphasizing that the breaking process is in most cases irreversible, so opening and closing a crack is not like flipping back and forth a spin.

The understanding of the breakdown of disordered systems has progressed to a large extent with the use of large-scale simulations of lattice models [12]. In these models a conductor is represented by a resistor network and an elastic medium by a spring network or other more complex discretizations. The disorder is modeled by random failure thresholds or by bond dilution. In this way the model retains the long-range nature and the tensorial structure of the interactions, which are computed solving coupled linear equations. These models have provided a good description of geometrical and topological properties of fracture, leading to the injection in this field of scaling concepts [13]. Recently, quasistatic lattice models have also been used to study dynamical properties of fracture [14-17].

The breakdown of a disordered solid is preceded by intense precursors in the form of avalanches. It has been experimentally observed that the response (acoustic emission) to an increasing external stress takes place in bursts distributed over a wide range of scales. Examples are found in the fracturing of wood [18], cellular glass [19], and concrete [20], in hydrogen precipitation [21], in dislocation motion in ice crystals [22], and in volcanic activity [23]. These phenomena are reminiscent of the Gutenberg-Richter law for

1063-651X/99/59(5)/5049(9)/$15.00
©1999 The American Physical Society

---

ZAPPERI, RAY, STANLEY, AND VESPIGNANI
PRE 59

earthquake statistics [24]. It is becoming apparent that avalanche response is the rule rather than the exception in driven disordered systems. Other examples range from the motion of domain walls in magnets (the Barkhausen effect) [25] and flux lines in superconductors [26], frictional sliding [27], to fluid flow in porous media [28] and the inflation of degassed lungs [29]. Therefore, understanding the general physical mechanisms of avalanche dynamics goes well beyond the study of breakdown and fracture.

In this paper, we numerically study the random fuse model [30–33] and a spring network [34]. The investigation of these two models allows us to compare the behavior of a quasistatic scalar model with a more complex vectorial dynamical model. We analyze the scaling close to the breakdown and we find that it is consistent with a mean-field analysis. We show that avalanche behavior near the breakdown in disordered systems is analogous to the formation of droplets observed close to a spinodal instability in first-order phase transitions. The system is driven by a slowly increasing external force through a complex energy landscape; it is not allowed to jump over energy barriers by thermal activation. This situation should correspond to the experiment reported in Ref. [18]. The intriguing consequence of this analysis is that the behavior of a disordered driven system at zero temperature is similar to what is expected from a thermally driven homogeneous system close to a spinodal point. It is tempting to conclude that quenched disorder has an effect similar to thermal fluctuations, although a discussion in terms of metastability and nucleation is not possible in the first case. We will briefly discuss these analogies in the magnetic context. Finally, it is interesting to remark that spinodal nucleation and first-order transitions have also been suggested to play an important role in the physics of frictional sliding and earthquakes [35]. Also for these systems thermal disorder is expected to be irrelevant with respect to quenched inhomogeneities.

The paper is organized as follows. In Sec. II, we briefly review spinodal nucleation and we discuss the role of quenched disorder. In Sec. III, we present a mean-field analysis of fracture. Section IV discusses the simulations for the random fuse model and Sec. V is devoted to molecular dynamics simulations of a spring network. In Sec. VI, we discuss the cluster structure of our models and draw analogies with percolation and in Sec. VII, we compare the results of our model with experiments and discuss some open questions.

A short account of a subset of these results has been presented in Ref. [15].

## II. SPINODAL NUCLEATION, THERMAL FLUCTUATIONS, AND QUENCHED DISORDER

Nucleation near a spinodal appears to be very different than classical nucleation and the classical theory is expected to fail. Droplets appear to be fractal objects and the process of nucleation is due to the coalescence of these droplets, rather than the growth of a single one [36]. The theoretical description of homogeneous spinodal nucleation is based on the Landau-Ginzburg free energy of a spin system in the presence of an external magnetic field [5]. When the temperature is below the critical value, the free energy has the

typical two-well structure. In the presence of an external magnetic field, one of the wells is depressed with respect to the other, which therefore represents the metastable state. The system must cross a free energy barrier to relax into the stable phase. When the external field is increased, this nucleation barrier decreases, eventually vanishing at the spinodal. Using this formalism, it has been shown that the approach to the spinodal is characterized by scaling laws, analogous to critical phenomena. The magnetization or the order parameter $\phi$ scales with the external field $H$ as

$$
\phi - \phi_{s} \sim \left(H_{s} - H\right)^{1/2}, \tag{1}
$$

where $\phi_s$ and $H_s$ are, respectively, the order parameter and the field at the spinodal. This law implies a divergence of the quasistatic susceptibility

$$
\chi \equiv \frac{d\phi}{dH} \sim \left(H_{s} - H\right)^{-\gamma}, \quad \gamma = 1/2. \tag{2}
$$

The fluctuations in the order parameter can be related to suitably defined clusters, whose sizes turn out to be power law distributed with an exponent $\tau = 3/2$, in mean-field theory. For finite-dimensional short-range models, this mean-field picture is expected to fail, since the system will nucleate before reaching the limit of metastability. On the other hand, mean-field behavior is expected to be valid in the presence of the long-range interactions, and it has been numerically verified in Monte Carlo simulations of the long-range Ising model [37]. The limit of stability in a thermally activated homogeneous fracture is believed to correspond to a spinodal point. One should then be able to observe scaling laws consistent with those found in spinodal nucleation. To our knowledge, such a scaling behavior has not yet been observed in numerical simulations.

In this paper we will not deal with a thermally activated fracture but rather with a disordered driven system. In this regard, an interesting analogy can be made with a model recently proposed by Sethna and co-workers [38,39] in the context of magnetic hysteresis. The model in question is a random-field Ising model (RFIM), driven at zero temperature by an increasing uniform magnetic field $H$. Each spin $s_i$ takes the sign of the local force

$$
f_{i} \equiv - \frac{\delta E}{\delta s_{i}} = J \sum_{j} s_{j} + h_{i} + H, \tag{3}
$$

where the sum runs over the neighboring sites, and $h_i$ is the random field at site $i$, which has a Gaussian distribution with variance $R$. When the external field is increased, some local forces change sign and the spins flip along the direction of $H$ in avalanches. For low values of the strength of the disorder $R &lt; R_c$, there is a critical value of the field $H_c$ for which the system undergoes a discrete (first-order) transition involving a finite change in the order parameter (the magnetization).

In mean-field theory, the approach to the instability $H_{c}$ is characterized by the same scaling laws and exponents of spinodal nucleation, as reported in Eqs. (1) and (2). Close to the first-order transition, the avalanche size distribution is described by a scaling form

$$
P(m) \sim s^{-\tau} f\left(m \left(H_{c} - H\right)^{n}\right), \tag{4}
$$

---

PRE 59
AVALANCHES IN BREAKDOWN AND FRACTURE PROCESSES
5051

with $\tau = 3/2$ and $\kappa = 1$. It is worth noting that these scaling exponents coincide with the mean-field exponents for the distribution of droplets in homogeneous spinodal nucleation. From these studies it appears that the behavior of thermally activated homogeneous spinodal nucleation is similar to the approach to the instability in disordered systems driven at zero temperature. However, one should bear in mind that for a given realization of the disorder the dynamics is completely deterministic in the second case. Concepts such as metastability and nucleating droplets are formally not defined in this context.

## III. MEAN-FIELD THEORY

In this section we generalize the analysis of Ref. [7] to derive a simple mean-field theory for fracture. The models we will analyze are defined on a two-dimensional lattice. Each bond of the lattice is supposed to obey the equations of linear elasticity, until it is stretched beyond a randomly chosen threshold, after which it breaks. In the electric case the equations are scalar, each bond satisfies the Ohm law, and the currents are computed numerically by solving the Kirchhoff equations with the appropriate boundary condition.

To illustrate the mean-field theory we will consider for simplicity the random fuse model. To every bond $i$ of the lattice we associate a fuse of unit conductivity $\sigma_{i} = 1$. An external current $I$ or voltage $V$ is then applied to the system by imposing an external voltage $V$ to two opposite edges of the lattice. When the current in the bond exceeds a randomly distributed threshold $D_{i}$ the bond becomes an insulator $(\sigma_{i} = 0)$. The voltage drops $(\Delta V)_{i}$ for each bond are computed by minimizing the total dissipated energy

$$
E (\{\sigma \}) \equiv \frac {1}{2} \sum_ {i} \sigma_ {i} \left[ \left(\Delta V\right) _ {i} ^ {2} - D _ {i} ^ {2} \right]. \tag {5}
$$

The dynamics of the model results from a double minimization process. The voltage drops $(\Delta V)_i$ are obtained by a global minimization of the energy at fixed $\sigma_{i}$, while the $\sigma_{i}$ are then chosen to minimize the local bond energy. The first step is equivalent to solving the Kirchhoff equations for the network, while the second step corresponds to breaking the bonds for which the current overcomes the threshold. The external current is increased slowly until the lattice is no longer conducting. This means that each time a bond is broken, the voltage and the currents are recomputed with the new values of the conductivities.

To derive a mean-field theory, it is useful to recast the dynamics of the model in terms of the externally applied current $I$. We can rewrite the energy of Eq. (5), in full generality, as

$$
E (I, \{\sigma \}) = \frac {1}{2} \left(\frac {I ^ {2}}{G (\{\sigma \})} - \sum_ {i} \sigma_ {i} D _ {i} ^ {2}\right), \tag {6}
$$

where $G(\{\sigma\})$ is the total conductivity of the lattice and is a complicated function of the local conductivities. We can estimate $G(\{\sigma\})$ using the effective medium theory [40], which in our case gives

$$
G (\{\sigma \}) = 2 \phi - 1, \tag {7}
$$

where $\phi \equiv \sum_{i} \sigma_{i} / L^{2}$. We can express the energy as a sum over "spins" interacting with effective random fields $h_{i}$,

$$
E _ {\mathrm {M F}} (I, \{\sigma \}) = \sum_ {i} \sigma_ {i} h _ {i} = \frac {1}{2} \sum_ {i} \sigma_ {i} \left(\frac {I ^ {2}}{L ^ {2} \phi (2 \phi - 1)} - D _ {i} ^ {2}\right). \tag {8}
$$

The value of $\phi$ can be computed self-consistently as

$$
\phi = P \left(h _ {i} &lt; 0\right) = 1 - \int_ {0} ^ {I / \{L \sqrt {\phi (2 \phi - 1)} \}} \rho (D) d D, \tag {9}
$$

where $\rho(D)$ is the distribution of failure thresholds. The solution of this equation can be expressed in terms of the current per unit length $f \equiv I / L$. We can identify $f$ with the external field and $\phi$ with the order parameter.

We can show (see Appendix) that under general conditions $\rho$ in Eq. (9) has a solution for $f &lt; f_{c}$ and, close to $f_{c}$, $\phi$ scales as

$$
\phi - \phi_ {c} \sim \left(f _ {c} - f\right) ^ {1 / 2}. \tag {10}
$$

The mean-field theory we have presented is very similar to the fiber-bundle model (FBM) with global load sharing, an exactly solvable model for fracture which has been studied extensively [41,42]. In the FBM an external load $F$, is applied to $N$ parallel fibers, and equally shared among the unbroken ones. This means that the force on each fiber is

$$
f _ {i} = F / n, \tag {11}
$$

where $n = N\phi$ is the number of unbroken fibers. A fiber breaks when its force exceeds a quenched random threshold $D$. One can write an equation for the density of unbroken fibers that has the form of Eq. (9), with the upper limit of integration replaced by $F / (N\phi)$. The FBM can be obtained as a mean-field theory in the case of site damage, since in this case the effective medium conductivity is given by $G(\phi) = \phi$.

We can obtain the mean-field avalanche size distribution from the exact results derived for the FBM [42],

$$
P (m) \sim m ^ {- \tau} f \left(m \left(f _ {c} - f\right) ^ {\kappa}\right), \quad \tau = \frac {3}{2}, \quad \kappa = 1 \tag {12}
$$

where $m$ is the number of bonds that break as a function of the current. Equation (12) can also be obtained in the case of bond damage using similar arguments.

The average avalanche size $\langle m\rangle$ is proportional to the "susceptibility" $d\phi /df$ [43], and therefore diverges at the breakdown as

$$
\langle m \rangle \sim \left(f _ {c} - f\right) ^ {- \gamma}, \quad \gamma = 1 / 2. \tag {13}
$$

The exponents we have introduced satisfy the scaling relation $\kappa (2 - \tau) = \gamma$, which is consistent with the values reported in Eq. (12) and Eq. (13). The mean-field analysis indicates that the system is undergoing a first-order transition since the order parameter has a discontinuity and the conductivity at $f_{c}$ has a jump from $G(\phi_c) &gt; 0$ to zero. The approach to this transition is characterized by avalanches of increasing size, diverging at the transition.

---

ZAPPERI, RAY, STANLEY, AND VESPIGNANI
PRE 59

![img-0.jpeg](img-0.jpeg)
FIG. 1. Avalanches in the fuse model. As the current is increased the bonds break in avalanches of increasing size until the final breakdown occurs.

A similar behavior with the same scaling exponents is observed in the mean-field theory of the driven RFIM [38,39] for small disorder. In the RFIM, one observes also a second-order transition as the width of the disorder is increased. A similar transition does not seem to be present in our system, at least not in the mean-field treatment. It is also interesting to note that the same scaling laws describe metastable systems close to a spinodal point. The quasistatic susceptibility diverges as in Eq. (13) and droplets are distributed according to Eq. (12).

# IV. SCALING BEFORE BREAKDOWN IN THE RANDOM FUSE MODEL

An important issue to address at this point is the validity of mean-field results in the case of real low-dimensional systems. It is known that scaling does not hold close to the first-order transition for short-ranged RFIM in dimensions $d = 2,3$ [38,39]. Similarly, spinodal singularities are observed when interactions are long range [37]. Elastic interactions are intrinsically long range, which could lead to mean-field behavior even for low dimensions, as we will next show numerically.

![img-1.jpeg](img-1.jpeg)
FIG. 2. The average avalanche size in the fuse model scaled with the mean-field exponent $(\gamma = 1 / 2)$ as a function of $I / I_{c}$, for different values of the system size $L$. The linearity of the plot supports the validity of the mean-field calculations.

![img-2.jpeg](img-2.jpeg)
FIG. 3. The avalanche size distribution in the fuse model for two values of system size plotted in log-log scale. A line with the mean-field value $\tau' = 5/2$ of the exponent is plotted for reference.

We simulate the random fuse model [30] on a tilted square lattice, with periodic boundary conditions in the transverse direction. As we discussed in Sec. III, the current in each bond is obtained solving Kirchhoff equations, which we do numerically using a multigrid [44] relaxation algorithm with precision $\epsilon = 10^{-10}$. The distribution of thresholds is chosen to be uniform in the interval $[1 - \Delta, 1 + \Delta]$ [45]. We impose an external current $I$ through the lattice and we increase it at an infinitesimal rate. When a bond fails, we recompute the currents to see if other failures occur. The process is continued until a path of broken bonds spans the lattice and no current flows anymore.

We determine the cluster size distribution $n(s,I)$, which is defined as the number of clusters formed by $s$ neighboring broken bonds when the applied current is $I$. The moments $[M_k(I) \equiv \int s^k n(s,I) ds$ is the $k$th moment] of $n(s,I)$ describe much of the physics associated with the breakdown process. We determine $n(s,I)$ by averaging over the various threshold distribution configurations. The first moment $M_1(I)$ is the total number of broken bonds due to the current $I$ and is therefore proportional to $\phi$. According to our mean-field picture, the average $\langle m \rangle$ of the quantity $m = dM_1(I) / dI$ should then diverge close to the breakdown as $(I_c - I)^{-1/2}$. In Fig. 1, we plot the number of bonds $m$ that break for a given value of the current, in a particular realization of the process. We see that the breakdown is highly inhomogeneous with avalanches of increasing amplitude. In order to test the scaling, we plot in Fig. 2 $\langle m \rangle^{-2}$ as a function of the reduced current $I / I_c$, where $I_c$ is the average breakdown current, and we see that the graph is linear.

We also measure the distribution of avalanche sizes, integrating over all the values of the current. The mean-field analysis predicts that $P(m,I) \sim m^{-3/2} f(m(I_c - I))$, which yields an exponent $\tau' = 5/2$ when the distribution is integrated over the current. In fact we see that our data are consistent with this exponent [Fig. (3)]. We have also checked that the cutoff of the distribution increases with the system size. A similar result ($\tau \simeq 2.7$) for smaller lattice sizes ($L = 40$) was previously reported by Hansen and Hemmer [46], who also pointed out the similarity with the predictions of the FBM.

---

PRE 59
AVALANCHES IN BREAKDOWN AND FRACTURE PROCESSES
5053

![img-3.jpeg](img-3.jpeg)
FIG. 4. The average avalanche size in the spring network scaled with the mean-field exponent $(\gamma = 1/2)$ as a function of the applied stress $F$, for two different values of the system size $L$. The linearity of the plot supports the validity of the mean-field calculations.

# V. SCALING IN THE FRACTURE OF A SPRING NETWORK

The study of fractures in an elastic medium is carried out by molecular dynamics (MD) simulation on a lattice model with elastic restoring forces. Our model consists of an $L \times L$ ($L = 20$ and 50) square network with central and rotationally invariant bond-bending forces. The potential energy of the network is [34]

$$
V = \frac {a}{2} \sum_ {\langle i j \rangle} \left(\delta r _ {i j}\right) ^ {2} g _ {i j} + \frac {b}{2} \sum_ {\langle i j k \rangle} \left(\delta \theta_ {i j k}\right) ^ {2} g _ {i j} g _ {j k}, \tag {14}
$$

where $\delta r_{ij}$ is the change in the length of the spring between the nearest neighbor sites $\langle ij\rangle$ from its equilibrium value (taken to be unity), and $\delta \theta_{ijk}$ is the change in the angle between the adjacent springs $ij$ and $jk$ from its equilibrium value $\pi /2$ which is taken to ensure the square lattice structure of the lattice at equilibrium. $g_{ij} = 1$ if the spring $ij$ is present and is 0 otherwise. $a$ and $b$ are the force constants of the central and the bond-bending force terms, respectively. In terms of arbitrary length and time scales $l_0$ and $t_0$, the equations of motion in dimensionless variables involve the parameters $\lambda_1 = a t_0^2 /m$ and $\lambda_{2} = b t_{0}^{2} / m l_{0}^{2}$, where $m$ is the mass associated with the lattice sites. We choose $l_{0}$ to be the lattice spacing (most naturally). The ratio $\lambda_2 / \lambda_1 = b / a l_0^2$ is then a characteristic of the system under consideration. We choose $\lambda_{1} = 1$ and $\lambda_{2} = 0.1$. The small value of $\lambda_{2}$, much less than the value of $\lambda_{1}$, allows the fracture to develop without much deformation of the network. We start with all the springs intact so that $g_{ij} = 1$ for all neighboring $ij$'s and with each spring we associate a random breaking threshold $D_{ij}$, chosen from a uniform distribution $D\in [0,2]$.

We impose a constant external force $F$ on the sites of the boundary and the system is allowed to evolve dynamically using Verlet's algorithm [34],

$$
\vec {r _ {i}} (t + \Delta t) = 2 \vec {r _ {i}} (t) - \vec {r _ {i}} (t - \Delta t) + \vec {F _ {i}} (\Delta t) ^ {2}. \tag {15}
$$

Here, $F_{i}$ is the force [as determined from Eq. (14)] and $\vec{r_i} (t)$ is the position vector of the site $i$ at time $t$. The simulation involves discrete time $t$ in steps of $\Delta t$. If the simulation runs for $n$ iterations, then the elapsed time is $t = n\Delta t$ while the

![img-4.jpeg](img-4.jpeg)
FIG. 5. The avalanche size distributions in the spring network for systems with two values of system size plotted in log-log scale. A line with the mean-field value $\tau' = 5/2$ of the exponent is plotted for reference.

real time elapsed is $nt_0\Delta t$. One way to speed up the relaxation process would be to choose a large value for $\Delta t$. However, there is an upper limit to this value for the iteration process to remain numerically stable. This limit is proportional to the convergence time for the fastest developing components of the stress distribution, which is generally very small in disordered systems. We choose $\Delta t = 0.01$. In addition, we add to the evolution a small viscous force to damp out excessive oscillations. In the course of evolution, if any spring $ij$ stretches beyond its cutoff value $D_{ij}$, the spring snaps irreversibly and $g_{ij}$ for that spring is set to zero. We increase the external force $F$ by small steps and at each step we compute the number of broken bonds, which constitute an avalanche. To average over disorder, the simulation is repeated for 50 different configurations of threshold values $D$.

The fracture in the network takes place in a series of bursts of bond (spring) breaking processes. In such a burst, bonds break from different parts of the network and the fracture grows. We keep track of the clusters formed by the connected broken bonds which, when spanning the network, causes its macroscopic breakdown.

We study here the same quantity analyzed in the preceding section, namely, the susceptibility and the avalanche distribution. In Fig. 4, we plot $\langle m\rangle^{-2}$ as a function of the stress and we find the linearity as expected. The critical breaking stress $F_{c}$ can readily be found from the points of intersection. Next, we consider the distribution $P(m)$ of the value of $m$ integrated over all the values of $\sigma$ up to $F_{c}$. We expect the behavior $P(m)\simeq m^{-5 / 2}$ in the mean-field theory. Figure 5 compares our simulation results with the mean-field prediction. The data presented in the figure are binned, where for different neighboring $m$ values, the corresponding $P(m)$ values are combined in one bin, and the result is plotted as the arithmetic mean of the two extreme $m$ values in the bin.

# VI. CLUSTER ANALYSIS: NUCLEATION OR PERCOLATION?

The avalanche size defined in the previous sections does not represent the geometric structure of the cracks, but only counts the number of bonds breaking at each time step. A geometrical characterization of the damage can be obtained

---

ZAPPERI, RAY, STANLEY, AND VESPIGNANI
PRE 59

![img-5.jpeg](img-5.jpeg)
FIG. 6. The average cluster size as a function of the current for different system sizes. Note that the cluster size does not diverge.

by studying the cluster size defined by counting the number of connected broken bonds.

In the fuse model, the average cluster size $S \equiv M_2 / M_1$ increases with $I$. However, by plotting $S$ for different system sizes, we observe that the cluster size is not diverging (Fig. 6). To clarify this point, we confirm that $S(I_c)$ does not show scaling with the lattice size $L$. We find similar results for the spring network, where the cluster size distribution has an exponential cutoff that does not change with the lattice size. We also study the number of clusters $n_c \equiv M_0$ as a function of the current and for different system sizes (see Fig. 7). We observe that $n_c$ scales as

$$
n _ {c} = L ^ {2} g (I / L), \tag {16}
$$

which is expected for a first-order transition. We obtain a similar scaling plot for the spring network (see Fig. 8).

Next we study the behavior of the lattice conductivity in the fuse model. For a given realization of the disorder the conductivity has a discrete jump at the breakdown [Fig. 9(a)]. We also plot the conductivity averaged over different realizations of the disorder and we observe a smooth curve with a slope at the breakdown that becomes sharper as the system size increases [Fig. 9(b)]. In the spring network, we calculate the lattice elasticity $Y$, which shows similar behavior as a function of the applied stress (Fig. 10).

Two principal scenarios have been proposed to explain the scaling behavior of avalanches prior to rupture. The first scenario invokes a continuous phase transition with a diverging characteristic length [47]. The various cracks inside the lattice should grow until one of them finally rules over the others, becoming the incipient spanning cluster. This is precisely what happens in percolation when the occupation probability $p$ is increased toward the percolation threshold $p_c$. If this scenario is true for fracture, we would expect the cluster characteristic size to diverge, contrary to our results. In the random fuse network a percolation transition is expected only in the limit of infinitely wide disorder distributions [48], when the strength of the disorder clearly dominates over the interactions.

The second scenario, in favor of which we presented numerical and theoretical evidence, describes fracture as a first-

![img-6.jpeg](img-6.jpeg)

![img-7.jpeg](img-7.jpeg)
FIG. 7. (a) The number of clusters as a function of the current in the fuse model for different system sizes. (b) The corresponding scaled plot.

order phase transition close to a spinodal-like instability. The elastic state is considered to be metastable, as soon as a nonzero stress is applied. Due to the presence of disorder, the system evolves through a series of metastable states towards the final instability. This occurs with the nucleation of cracks growing up to a critical size $s_c$ at which they coalesce, forming the macroscopic crack. Contrary to percolation, in this case there is no incipient spanning cluster prior to rupture.

What explains then the scaling in the avalanche statistics and the susceptibility? We recall that elastic (or electric)

![img-8.jpeg](img-8.jpeg)
FIG. 8. The scaled number of clusters as a function of the stress in the spring network for different system sizes.

---

PRE 59

AVALANCHES IN BREAKDOWN AND FRACTURE PROCESSES

5055

![img-9.jpeg](img-9.jpeg)

![img-10.jpeg](img-10.jpeg)
FIG. 9. (a) The conductivity as a function of the current for a single realization of the disorder, for different system sizes. (b) The conductivity as a function of $I / I_{c}$ averaged over different realizations of the disorder. Note that the discrete jump, indicative of a first-order transition, is smoothed for small system sizes.

forces are long range. When nucleation occurs close to a spinodal instability—which is well defined only for mean-field or long-range interactions—one expects a divergent susceptibility [5]. This is not naively related to the fluctuation of a geometrical quantities such as the crack size, which is not diverging at the spinodal. In order to describe geometrically the susceptibility, it is necessary to define the

![img-11.jpeg](img-11.jpeg)
FIG. 10. The elasticity of the spring network as a function of the applied stress.

clusters in a peculiar way, considering each site connected with all the others within the range of interactions [37]. These fluctuations are therefore different from those encountered in a second-order phase transition.

The spinodal point is a quite peculiar critical point which, rigorously speaking, exists only in mean-field theory, but can be detected when long-range interactions are present. In this respect, no scaling is observed in the avalanche distributions when the stress transfer after breaking is local, such as in the local load-sharing fiber bundle model studied in Refs. [42,46].

# VII. EXPERIMENTAL COMPARISON AND OPEN PROBLEMS

The above results clarify the nature of the breakdown process in the presence of quenched disorder. We have found that the breakdown is preceded by avalanches distributed as power laws. The scaling exponents are in quantitative agreement with the prediction of mean-field calculations. We have discussed that only globally defined quantities such as $\langle m(f)\rangle$ and $P(m)$ display scaling, while locally defined quantities, such as $S$, do not show any singular behavior. For a second-order phase transition, we would expect local quantities to show scaling. For instance, in percolation we have $S\sim (p - p_c)^{-\gamma}$, where $p$ is the concentration of broken bonds. On the other hand, first-order transitions usually do not show any precursor and scaling is not observed. An exception to this rule is represented by first-order transitions close to a spinodal point, for which some global quantities display scaling [37]; we argue that this case is relevant to the behavior observed before breakdown [49].

The observation that mean-field scaling is present in the fracture of two different network models suggests that this behavior is rather robust and does not depend on the fine details of the models, such as the tensorial structure of the interactions, the dynamics, or the boundary conditions. A more stringent test of our conclusions should come from the analysis of experimental data. In particular, the experimental setup discussed in Ref. [18] resembles some of the features of our model. An external pressure is slowly increased until the material (wood or fiberglass) breaks. In this process acoustic energy is released in bursts, whose amplitude shows a net increase as the material approaches the breakdown point [18]. The integrated distribution of burst energies $E$ was found to follow a power law with an exponent roughly equal to $-2$, which must be compared to $\tau = 5/2$, if one assumes that $m$ in our paper is proportional to $E$ in Ref. [18]. We see that there is a discrepancy in the results, although this may be due to the statistics. We have also tried to analyze the scaling of the average energy released at pressure $P$, but we could not obtain a firm conclusion due to the large statistical uncertainties. Interesting results have been recently obtained in three-dimensional simulations of fuse networks [50].

In mean-field theory, driven disordered systems behave similarly to their homogeneous, thermally driven, counterparts, if we compare the scaling of avalanches with that of the droplets. This applies to the RFIM [38,39], which shows features similar to those of spinodal nucleation [5], and to the fracture models we have studied. However, one should be careful not to interpret these analogies too strictly, since in

---

ZAPPERI, RAY, STANLEY, AND VESPIGNANI
PRE 59

driven disordered systems the notions of metastability, spinodal point, and nucleation are not well defined. In particular, the identification of $\phi$ and $f$ with the order and control parameters is justified only in MF theory. In two dimensions, simple homogeneous scaling fails in the presence of disorder. The breakdown current $I_{c}$ has a logarithmic size dependence [31],

$$
I _ {c} \sim \frac {L}{\ln L}, \tag {17}
$$

which cannot be interpreted in MF theory. A similar dependence is also present in the fraction of broken bond before breakdown $\phi_c$. While for finite systems the picture we have presented is completely consistent, it is not obvious how to perform the $L \to \infty$ limit. In order to obtain intensive parameters in this limit one should rescale $f$ and $\phi$ by an appropriate logarithmic factor. This can be done implicitly analyzing the data in terms of $f / f_c$, as in Ref. [18]. Finally, we note that in most cases the final breakdown starts from existing defects in the material. In our simulations, we restricted our attention to the case in which these defects were smaller than the discretization unit.

In conclusion, we have shown that two different models of breakdown and fracture share the same mean-field scaling exponents approaching the rupture point. The behavior observed in these models is analogous to spinodal nucleation in thermally driven homogeneous systems. At the breakdown point, the macroscopic quantities (elasticity, conductivity) are discontinuous and the characteristic crack size $S$ stays finite in the large $L$ limit. In addition, the statistics of global quantities (i.e., the number of broken bonds) display clear mean-field scaling in analogy with spinodal nucleation. The direct application of these ideas to experiments still remains an open question.

Note added in proof. Avalanches were studied in the fracture of a spring model similar to ours [51]. We thank J. V. Andersen for pointing this out to us.

# ACKNOWLEDGMENTS

The Center for Polymer Studies is supported by the NSF. S.Z. acknowledges financial support from the EC TMR Research Network under Contract No.

ERBFMRXCT960062. A.V. and S.Z. acknowledge partial support from the EC Network under Contract No. ERBFMRXCT980183. We thank G. Caldarelli, P. Cizeau, S. Ciliberto, A. Guarino, A. Hansen, H. J. Herrmann, W. Klein, A. Petri, S. Roux, and F. Sciortino for interesting discussions and useful remarks. We are particularly grateful to S. Ciliberto and A. Guarino who kindly provided us with the data of their experiments.

# APPENDIX

We derive here the scaling law for the approach to the instability in mean-field theory. We define $f \equiv I / L$ and $h(\phi) \equiv \sqrt{\phi(2\phi - 1)}$ and we rewrite Eq. (9) as

$$
\phi = 1 - \int_ {0} ^ {f / h (\phi)} \rho (D) d D. \tag {A1}
$$

By taking the derivative over $f$ on both sides of the equation, we obtain for the susceptibility

$$
\frac {d \phi}{d f} = - \frac {\rho (f / h (\phi))}{1 - \rho (f / h (\phi)) f h ^ {\prime} / h (\phi) ^ {2}}. \tag {A2}
$$

When the denominator is equal to zero, the system reaches the instability and the susceptibility diverges, which defines the critical values $\phi_c$ and $f_c$,

$$
1 - \rho \left(f _ {c} / h \left(\phi_ {c}\right)\right) f _ {c} h ^ {\prime} \left(\phi_ {c}\right) / h \left(\phi_ {c}\right) ^ {2} = 0. \tag {A3}
$$

The Taylor expansion of Eq. (A1) around $(\phi_c, f_c)$ yields

$$
\begin{array}{l} \delta \phi \equiv \phi - \phi_ {c} = \rho \left(f _ {c} / h \left(\phi_ {c}\right)\right) \left[ f _ {c} h ^ {\prime} \left(\phi_ {c}\right) \delta \phi / h \left(\phi_ {c}\right) ^ {2} \right. \\ \left. - \delta f / h \left(\phi_ {c}\right) \right] + A \delta \phi^ {2} + B \delta f \delta \phi , \tag {A4} \\ \end{array}
$$

where $\delta f \equiv (f - f_c)$ and $A, B$ are two constants. The term proportional to $\delta \phi$ vanishes because of Eq. (A3), leaving an equation of the form

$$
\delta f \sim \delta \phi^ {2}, \tag {A5}
$$

which is the scaling relation reported in Eq. (10). This relation thus holds for any analytic normalizable distribution function, but it is also true in the case of a uniform distribution, as can be easily shown by a direct calculation.

[1] Non-linearity and Breakdown in Soft Condensed Matter, edited by K. K. Bardhan, B. K. Chakrabarti, and A. Hansen (Springer-Verlag, Berlin, 1994); B. K. Chakrabarti and L. G. Benguigui, Statistical Physics of Fracture and Breakdown in Disordered Systems (Oxford University Press, Oxford, 1997).
[2] A. A. Griffith, Philos. Trans. R. Soc. London, Ser. A 221, 163 (1920).
[3] J. D. Gunton, M. San Miguel, and P. S. Sahini, in Phase Transitions and Critical Phenomena, edited by C. Domb and J. L. Lebowitz (Academic, London, 1983), Vol. 8.
[4] Fracture, an Advanced Treatise, edited by H. Liebowitz (Academic Press, New York, 1968), Vol. 1-7.
[5] C. Unger and W. Klein, Phys. Rev. B 29, 2698 (1984); 31, 6127 (1985). For a review see L. Monette, Int. J. Mod. Phys. B 8, 1417 (1994).
[6] J. B. Rundle and W. Klein, Phys. Rev. Lett. 63, 171 (1989).
[7] R. L. B. Selinger, Z.-G. Wang, W. M. Gelbart, and A. Ben-Saul, Phys. Rev. A 43, 4396 (1991); Z.-G. Wang, U. Landman, R. L. B. Selinger, and W. M. Gelbart, Phys. Rev. B 44, 378 (1991).
[8] R. L. B. Selinger, Z.-G. Wang, and W. M. Gelbart, J. Chem. Phys. 95, 9128 (1991).
[9] L. Golubovic and A. Pedrera, Phys. Rev. E 51, 2799 (1995); L. Golubovic and S. Feng, Phys. Rev. A 43, 5223 (1991).
[10] A. Buchel and J. P. Sethna, Phys. Rev. Lett. 77, 1520 (1996); Phys. Rev. E 55, 7669 (1997).

---

PRE 59

AVALANCHES IN BREAKDOWN AND FRACTURE PROCESSES

5057

[11] R. Englman and Z. Jaeger, Physica A 168, 665 (1990), and references therein.

[12] Statistical Models for the Fracture of Disordered Media, edited by H. J. Herrmann and R. Roux (North-Holland, Amsterdam, 1990).

[13] A. Hansen and P. C. Hemmer, Trends Stat. Phys. 1, 213 (1994).

[14] F. Tzschichholz and H. J. Herrmann, Phys. Rev. E 51, 1961 (1995).

[15] S. Zapperi, P. Ray, H. E. Stanley, and A. Vespignani, Phys. Rev. Lett. 78, 1408 (1997).

[16] G. Caldarelli, F. Di Tolla, and A. Petri, Phys. Rev. Lett. 77, 2503 (1996).

[17] S. Zapperi, A. Vespignani, and H. E. Stanley, Nature (London) 388, 658 (1997).

[18] A. Garcimartin, A. Guarino, L. Bellon, and S. Ciliberto, Phys. Rev. Lett. 79, 3202 (1997); A. Guarino, A. Garcimartin and S. Ciliberto, Eur. Phys. J. B 6, 13 (1998).

[19] C. Maes, A. Van Moffaert, H. Frederix, and H. Strauven, Phys. Rev. B 57, 4987 (1998).

[20] A. Petri, G. Paparo, A. Vespignani, A. Alippi, and M. Costantini, Phys. Rev. Lett. 73, 3423 (1994).

[21] G. Cannelli, R. Cantelli, and F. Cordero, Phys. Rev. Lett. 70, 3923 (1993).

[22] J. Weiss and J.-R. Grasso, J. Phys. Chem. B 101, 6113 (1997).

[23] P. Diodati, F. Marchesoni, and S. Piazza, Phys. Rev. Lett. 67, 2239 (1991).

[24] B. Gutenberg and C. F. Richter, Bull. Seismol. Soc. Am. 34, 185 (1944).

[25] S. Zapperi, P. Cizeau, G. Durin, and H. E. Stanley, Phys. Rev. B 58, 6353 (1998), and references therein.

[26] S. Field, J. Witt, F. Nori, and X. Ling, Phys. Rev. Lett. 74, 1206 (1995).

[27] S. Ciliberto and C. Laroche, J. Phys. I 4, 223 (1994).

[28] A. H. Thompson, A. J. Katz, and R. A. Raschke, Phys. Rev. Lett. 58, 29 (1987).

[29] B. Suki, A.-L. Barabási, Z. Hantos, F. Peták, and H. E. Stanley, Nature (London) 368, 615 (1994).

[30] L. de Arcangelis, S. Redner, and H. J. Herrmann, J. Phys. (France) Lett. 46, L585 (1985).

[31] P. Duxbury, P. D. Beale, and P. L. Leath, Phys. Rev. Lett. 57, 1052 (1986).

[32] L. de Arcangelis and H. J. Herrmann, Phys. Rev. B 39, 2678 (1989).

[33] B. Kahng, G. G. Batrouni, S. Redner, L. de Arcangelis, and H. J. Herrmann, Phys. Rev. B 37, 7625 (1988).

[34] P. Ray and G. Date, Physica A 229, 26 (1996).

[35] J. B. Rundle, W. Klein, and S. Gross, Phys. Rev. Lett. 76, 4285 (1996); G. Vasconcelos, ibid. 76, 4865 (1996); J. B. Rundle, E. Preston, S. McGinnis, and W. Klein, ibid. 80, 5698 (1998); in Proceedings of the Santa Fe Institute Workshop on Reduction and Predictability of Natural Disasters, Santa Fe, NM, 1994, edited by J. B. Rundle, D. L. Turcotte, and W. Klein (Addison-Wesley, Reading, MA, 1995).

[36] L. Monette and W. Klein, Phys. Rev. Lett. 63, 2336 (1992).

[37] D. Heerman, W. Klein, and D. Stauffer, Phys. Rev. Lett. 49, 1262 (1982); T. Ray and W. Klein, J. Stat. Phys. 61, 891 (1990).

[38] J. P. Sethna, K. Dahmen, S. Karta, J. A. Krumhansl, and J. D. Shore, Phys. Rev. Lett. 70, 3347 (1993).

[39] K. Dahmen and J. P. Sethna, Phys. Rev. B 53, 14 872 (1996).

[40] S. Kirkpatrick, Rev. Mod. Phys. 45, 574 (1973).

[41] H. A. Daniels, Proc. R. Soc. London, Ser. A 183, 405 (1945); S. L. Phoenix and H. M. Taylor, Adv. Appl. Probab. 5, 200 (1973).

[42] P. C. Hemmer and A. Hansen, J. Appl. Mech. 59, 909 (1992); M. Kloster, A. Hansen, and P. C. Hemmer, Phys. Rev. E 56, 2615 (1997).

[43] M. Acharaya and B. K. Chakrabarti, Phys. Rev. E 53, 140 (1996); M. Acharaya, P. Ray, and B. K. Chakrabarti, Phys. Rev. A 224, 287 (1996).

[44] W. H. Press and S. A. Teukolsky, Comput. Phys. 5, 514 (1991).

[45] We made the choice $\Delta = 1$ in order to avoid the “ductile-brittle” crossover at a finite value of the lattice size (see Ref. [33]). Other broad analytic distributions give rise to similar results.

[46] A. Hansen and P. C. Hemmer, Phys. Lett. A 184, 394 (1994).

[47] D. Sornette and J. V. Andersen, Eur. Phys. J. B 1, 353 (1998).

[48] S. Roux, A. Hansen, H. Herrmann, and E. Guyon, J. Stat. Phys. 52, 237 (1988).

[49] Our conclusions have been criticized by the authors of Ref. [47], who probably misinterpreted our results. Reference [47] claims that we have shown, in Ref. [15], that the crack size diverges, which would contradict the hypothesis of a first-order transition. This is not the case, as is shown in Fig. 6. In addition, [47] criticizes the analogy between the breakdown and the spinodal point, noting that spinodal decomposition is qualitatively different from fracture. Probably this comment is due to incorrect identification of spinodal nucleation with spinodal decomposition.

[50] V. I. Räisänen, M. J. Alava, and R. M. Nieminen, Phys. Rev. B 58, 14 288 (1998).

[51] K.-T. Leung and J. V. Andersen, Europhys. Lett. 38, 589 (1997); K.-T. Leung et al., Phys. Rev. Lett. 80, 1916 (1998).
letters to nature

# Plasticity and avalanche behaviour in microfracturing phenomena

Stefano Zapperi*, Alessandro Vespignani† &amp; H. Eugene Stanley*

* Center for Polymer Studies and Department of Physics, Boston University, Boston, Massachusetts 02215, USA
† Instituut-Lorentz, University of Leiden, PO Box 9506, 2300 RA, Leiden, The Netherlands

Inhomogeneous materials, such as plaster or concrete, subjected to an external elastic stress display sudden movements owing to the formation and propagation of microfractures. Studies of acoustic emission from these systems reveal power-law behaviour¹. Similar behaviour in damage propagation has also been seen in acoustic emission resulting from volcanic activity² and hydrogen precipitation in niobium³. It has been suggested that the underlying fracture dynamics in these systems might display self-organized criticality⁴, implying that long-ranged correlations between fracture events lead to a scale-free cascade of 'avalanches'. A hierarchy of avalanche events is also observed in a wide range of other systems, such as the dynamics of random magnets⁵ and high-temperature superconductors⁶ in magnetic fields, lung inflation⁷ and seismic behaviour characterized by the Gutenberg-Richter law⁸. The applicability of self-organized criticality to microfracturing has been questioned⁹,¹⁰, however, as power laws alone are not unequivocal evidence for it. Here we present a scalar model of microfracturing which generates power-law behaviour in properties related to acoustic emission, and a scale-free hierarchy of avalanches characteristic of self-organized criticality. The geometric structure of the fracture surfaces agrees with that seen experimentally. We find that the critical steady state exhibits plastic macroscopic behaviour, which is commonly observed in real materials.

Quasi-static models of fracture propagation have been extensively studied in the past¹¹. Such analyses have been mainly focused on the geometrical properties of the macroscopic crack, although some dynamical effects have also been studied¹²,¹³. Recently, avalanches and other dynamical properties have been investigated in a model for hydraulic fracturing¹⁴. However, the amplitude distribu

tion associated with the acoustic emission signal did not reveal any scaling behaviour.

The mesoscopic description of an elastic disordered medium is usually obtained by discretizing macroscopic elastic equations. In the theory of linear elasticity¹⁵, these equations relate the stress tensor $s_{\alpha \beta}$ to the strain tensor $\epsilon_{\gamma \delta}$ via the Hooke tensor $C_{\alpha \beta \gamma \delta}$:

$$
s _ {\alpha \beta} = \sum_ {\gamma , \delta} C _ {\alpha \beta \gamma \delta} \epsilon_ {\gamma \delta} \tag {1}
$$

In highly inhomogeneous materials, like concrete, linear elasticity breaks down owing to the formation and the propagation of microcracks. It is still possible to describe the system using equation (1) by using an effective Hooke tensor $\hat{C}$. The 'damage' $D$ is defined through the relation between $C$ and $\hat{C}$ (ref. 16),

$$
\hat {C} = (1 - D) C \tag {2}
$$

where the tensor indices have been omitted for simplicity. The full tensorial formalism can be quite complex to handle numerically. Fortunately, many essential features of fracture phenomenology can be described using scalar models¹¹,¹⁷,¹⁸. There is a formal analogy between the scalar elasticity problem and an equivalent electrical problem; one identifies the current $I$ with the stress, the voltage $V$ with the strain, and the conductivity $\sigma$ with the Hooke tensor: we will use this electrical analogy.

To study the system at a mesoscopic scale, we discretize the problem by considering a resistor network¹⁷ on a tilted square lattice. We introduce the disorder, due to the inhomogeneities present in the material, by assigning a random failure threshold $I_{\mathrm{c}}$ to each resistor, where $I_{\mathrm{c}}$ is drawn from a uniform distribution in the interval [0,1]. In the classic 'fuse' model¹⁷,¹⁹, if the current flowing in a resistor exceeds the failure threshold, the bond is removed from the lattice (that is, the electrical conductivity drops to zero). In this way the system develops a macroscopic crack and eventually the lattice breaks apart. We adopt a different breaking rule: when the current in a bond exceeds the threshold, we impose permanent 'damage' to the bond by decreasing the conductivity of the bond by a factor $a \equiv (1 - D)$. Describing the local damage with a continuous parameter corresponds to studying the system at a scale larger than the microscopic crack scale, but smaller than the homogeneous macroscopic scale.

After a bond failure we choose at random a new threshold for the bond in order to model the microscopic rearrangements in the material. The model in this form is quite slow to simulate numerically. A big reduction in the simulation time can be obtained by also

![img-0.jpeg](img-0.jpeg)
Figure 1 The damage for a system of size $L = 64$. a, In the early stage, after 500 avalanches; b, in the steady state, after 1,000 avalanches. c, The final crack, which develops in the highly damaged region. Damaged parts are shown in red and undamaged parts in yellow; absent bonds (the crack) are shown in black.

![img-1.jpeg](img-1.jpeg)

![img-2.jpeg](img-2.jpeg)

Nature © Macmillan Publishers Ltd 1997

NATURE | VOL 388 | 14 AUGUST 1997

---

letters to nature

changing the thresholds of the bonds that neighbour a damaged bond. This local rearrangement does not change the properties of the model but makes it easier to obtain statistics of sufficiently high quality.

The simulation proceeds as follows. We apply an external voltage difference between two opposite edges of the lattice, while periodic boundary conditions are imposed on the other direction. We compute the currents in each bond by solving numerically the Kirchoff equations, using a multigrid $^{20}$  relaxation algorithm with precision  $\epsilon = 10^{-12}$ . The voltage is then slowly increased until the current in some bond reaches its threshold. The bond is damaged and the disorder is changed according to the rules specified above. We then compute new currents and repeat the process until no unstable bonds are present. Owing to the long-range elastic interactions and the 'redistribution' of the disorder, a single bond failure can be followed by an avalanche of additional failures.

We study the system in the limit of 'slow driving': the timescale over which fractures form and propagate is much faster than the timescale of the external driving. This is a common characteristic of systems that display self-organized criticality (SOC). In fact, for SOC systems the control parameter is always related to the ratio between two timescales. In this situation, however, the existence of a timescale separation makes the system very close to the critical point for a wide range of internal parameters.

We start the simulation with undamaged material: all the conductivities are set equal to one. In the early stage of the process only small rearrangements take place. This is also evident by observing the structure of the microfractures in the system (Fig. 1a): the damage is homogeneously scattered throughout the system. Increasing the voltage leads to a corresponding increase of the total current flowing in the system: macroscopically the material behaves elastically. Deviations from linear elasticity start to appear as the activity increases. Eventually, the system reaches a steady-state which is macroscopically 'plastic' (Fig. 2), in the sense that the increase of the voltage is balanced by the damage in such a way that the current is kept approximately constant. In this state the activity is highly fluctuating and avalanches of all sizes occur. Plastic behaviour is not uncommon in stressed synthetic materials[21].

The damage in the steady state tends to be organized in linear bands (Fig. 1b), arising from the coalescence of the underlying microfractures. A similar geometrical structure has been observed in microfracturing experiments on concrete[22,23]. We note that a plastic steady state characterized by highly fluctuating activity has been recently obtained in molecular dynamic studies of granular solids[14] and foams[25] under shear.

In the plastic steady state, we investigate the statistical properties of rupture sequences (Fig. 3a) in time and magnitude during fracturing. We define the avalanche size  $s$  as the number of bonds damaged for a given voltage increment, and find that the avalanche size probability distribution function  $P(s)$  exhibits a power-law behaviour

$$
P (s) \sim s ^ {- \tau} \tag {3}
$$

where  $\tau = 1.19 \pm 0.01$ . By computing the distribution for different lattice sizes, we observe that the cut-off scales with the system size (Fig. 3b). This is the fingerprint of a scale-free activity; an absence of characteristic lengths in the system.

We next compute the distribution of the time duration  $T$  of each avalanche, obtaining a power-law decay

$$
P (T) \sim T ^ {- \alpha} \tag {4}
$$

where  $\alpha = 1.30 \pm 0.01$ . Again we find that the cut-off scales with the system size.

We also study the distribution of energy bursts, which is directly related to the acoustic-emission signal recorded experimentally. In this case also we find a power-law distribution if the energy is rescaled by the energy of the unbroken lattice, as pointed out in

![img-3.jpeg](img-3.jpeg)
Figure 2 The  $I - V$  characteristics of the present model for different values of the parameter  $a$  (see text). Note the crossover at  $V \approx 12$  between linear elasticity and plasticity.

![img-4.jpeg](img-4.jpeg)

![img-5.jpeg](img-5.jpeg)
Figure 3 a, The number of broken bonds  $s$  as a function of time. b, The avalanche size distribution for different system sizes ( $L = 16, 32, 64$ ). The statistical analysis is performed only in the steady state for  $a = 0.9$ , averaging over  $2 \times 10^4$  avalanches.

NATURE|VOL 388|14 AUGUST 1997

Nature © Macmillan Publishers Ltd 1997

---

letters to nature

![img-6.jpeg](img-6.jpeg)
Figure 4 The distribution of energy bursts, related to the experimentally observed acoustic emission. We fit the power-law distribution with an exponent equal to $1.2 \pm 0.1$.

refs 26 and 27. The results for a lattice of size $L = 64$ are shown in Fig. 4.

Another quantity of interest is the distribution of time intervals $\Delta t$ between two avalanches in the steady state (Fig. 5). We find a power decay which is reminiscent of the Omori law in earthquake statistics$^{28}$

$$
P (\Delta t) \sim (\Delta t) ^ {- \gamma} \tag {5}
$$

where $\gamma \approx 1$. The above behaviour provides another indication that the system is critical in the plastic steady state, which develops critical correlations and scaling behaviour through a self-organization process. The critical exponents seem to be independent of the changes in the damage parameter $\alpha$ within numerical uncertainties.

In our model the steady state could in principle last forever. However, in realistic situations, the damage description should fail at a given point. After a certain number of failure events, a bond will no longer respond elastically. This observation can be modelled in a natural way by allowing for only a finite number of failures per bond. In other words, when the conductivity of a bond reaches a given value $\sigma_{\mathrm{c}}$ owing to the repeated failures, the bond is no longer considered to be elastic and is removed from the lattice. The parameter $\sigma_{\mathrm{c}}$ adjusts the duration of the steady-state: for high values of $\sigma_{\mathrm{c}}$, the steady state is never reached and fracture is brittle, whereas a low value of $\sigma_{\mathrm{c}}$ produces a plastic steady state. In both cases a macroscopic crack will eventually form. In Fig. 1c we observe that the crack develops in the region of high damage and has a rough structure. Owing to the limited system size, we were not able to calculate reliably the roughness exponent.

We note that to observe this behaviour the system must be driven at a constant voltage. We have also performed simulations in which the system is driven by imposing a constant current: in this case no steady state is observed and the system is driven to an instability corresponding to the critical current of the voltage-driven experiment. One can still fit the non-stationary distribution of avalanches with a power law but the system is clearly not SOC. With our model we can therefore reconcile the controversy$^{9,10}$ between SOC and 'sweeping of an instability'$^{29}$ as possible explanations of microfracturing experiments: either of the two phenomena can arise according to the driving conditions. It would be interesting to test this prediction experimentally by comparing avalanche signals in stress-driven and strain-driven experiments. In interpreting experimental results, it is important to keep in mind that SOC requires a 'stationary' signal. In fracture phenomena this can be obtained in the plastic regime.

![img-7.jpeg](img-7.jpeg)
Figure 5 The distribution of quiescent intervals $\Delta t$ between two avalanches in the plastic state. Plotted for reference is a line with slope corresponding to $\gamma = 1$ in equation (5).

Received 2 April; accepted 3 June 1997.

1. Petri, A., Papiro, G., Vespignani, A., Alippi, A. &amp; Costantini, M. Experimental evidence for critical dynamics in microfracturing processes. Phys. Rev. Lett. 73, 3423-3426 (1994).
2. Diodati, P., Marchesoni, F. &amp; Piazza, S. Acoustic emission from volcanic rocks: an example of self-organized criticality. Phys. Rev. Lett. 67, 2239-2242 (1991).
3. Cannelli, G., Cantelli, R. &amp; Cordero, F. Self-organized criticality of the fracture processes associated with hydrogen precipitation in niobium by acoustic emission. Phys. Rev. Lett. 70, 3923-3926 (1993).
4. Bak, P., Tang, C. &amp; Wiesenfeld, K. Self-organized criticality: an explanation of t/f noise. Phys. Rev. Lett. 59, 381-384 (1987).
5. Cote, P. J. &amp; Meisel, L. V. Self-organized criticality and the Barkhausen effect. Phys. Rev. Lett. 67, 1334-1337 (1991).
6. Field, S., Witt, J., Nori, F. &amp; Ling, X. Superconducting vortex avalanches. Phys. Rev. Lett. 74, 1206-1209 (1995).
7. Suki, B., Barabási, A.-L., Hantos, Z., Peták, F. &amp; Stanley, H. E. Avalanches and power-law behaviour in lung inflation. Nature 368, 615-618 (1994).
8. Gutenberg, B. &amp; Richter, C. F. Frequency of earthquakes in California. Bull. Seionol. Soc. Am. 34, 185-188 (1944).
9. Sornette, D. Power laws without parameter tuning: an alternative to self-organized criticality. Phys. Rev. Lett. 72, 2306 (1994).
10. Cannelli, G., Cantelli, R. &amp; Cordero, F. Reply to Sornette D., 'Power laws without parameter tuning: an alternative to self-organized criticality'. Phys. Rev. Lett. 72, 2307 (1994).
11. Herrmann, H. J. &amp; Roux, S. (eds) Statistical Models for the Fracture of Disordered Media (North Holland, Amsterdam, 1990).
12. Sornette, D. &amp; Vanneste, C. Dynamics and memory effects in rupture of thermal fuse networks. Phys. Rev. Lett. 68, 612-615 (1992).
13. Miltenberger, P., Sornette, D. &amp; Vanneste, C. Fault self-organization as optimal random paths selected by critical spatiotemporal dynamics of earthquakes. Phys. Rev. Lett. 71, 3604-3607 (1993).
14. Teschichholz, F. &amp; Herrmann, H. J. Simulations of pressure fluctuations and acoustic emission in hydraulic fracturing. Phys. Rev. E 51, 1961-1970 (1995).
15. Landau, L. D. &amp; Lifschitz, E. M. Theory of Elasticity (Pergamon, New York, 1960).
16. Wilshire, B. &amp; Owen, D. R. J. Engineering Approaches to High Temperature Design (Pineridge, Swansea, UK, 1983).
17. De Arcangelis, L., Redner, S. &amp; Herrmann, H. J. A random fuse model for breaking processes. J. Phys. (Paris) 46, L585-L590 (1985).
18. Herrmann, H. J., Kertész, J. &amp; de Arcangelis, L. Fractal shapes of deterministic cracks. Europhys. Lett. 10, 514-519 (1991).
19. De Arcangelis, L. &amp; Herrmann, H. J. Scaling and multiscaling laws in random fuse networks. Phys. Rev. B 39, 2678-2684 (1989).
20. Press, W. H. &amp; Tsukolski, S. A. Multigrid methods for boundary value problems. Comput. Phys. 5, 154-519 (1991).
21. Chen, W. F. Plasticity in Reinforced Concrete (McGraw-Hill, New York, 1982).
22. Stroeven, P. in Interfaces and Cementous Composites (ed. Maso, J. C.) 187-196 (Spoon, London, 1993).
23. Stroeven, P. Some observations on microcracking in concrete subjected to various loading regimes. Eng. Frac. Mech. 35, 775-782 (1990).
24. Tillemans, H. J. &amp; Herrmann, H. J. Simulating deformations of granular solids under shear. Physica A 217, 261-288 (1995).
25. Okuzono, T. &amp; Kawasaki, K. Intermittent flow behavior of random foams: a computer experiment on foam rheology. Phys. Rev. E 51, 1246-1253 (1995).
26. Caldarelli, G., Di Tolla, F. &amp; Petri, A. Self organization and annealed disorder in fracturing process. Phys. Rev. Lett. 77, 2503-2506 (1996).
27. Sahimi, M. &amp; Arbabi, S. Scaling laws for fracture of heterogeneous materials and rock. Phys. Rev. Lett. 77, 3689-3692 (1996).
28. Omori, F. J. Coll. Sci. Imper. Univ. Tokyo 7, 111 (1894).
29. Sornette, D. Sweeping of an instability: an alternative to self-organized criticality to get powerlaws with parameter tuning. J. Phys. I France 4, 209-221 (1994).

Acknowledgements. We thank G. Caldarelli, R. Cuerno, J. Kertesz, H. J. Herrmann, K. B. Lauritsen, A. Petri, C. Rebbi and P. Stroeven for suggestions and discussions. The Center for Polymer Studies is supported by NSF.

Correspondence should be addressed to S.Z. (e-mail: zapperi@bu.edu).

Nature © Macmillan Publishers Ltd 1997

NATURE VOL 388 14 AUGUST 1997
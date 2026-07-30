# Response to Referee Reports — ER12738

## Response to Referee 1

### Point 1 (R1-1): Physical grounding of the surface-diffusion parameter $T_s$

**Referee Comment:**
> *Ts controls the number of post-attachment lateral diffusion steps and therefore governs the ratio between the molecular relaxation timescale and the fibril growth rate. In real type I collagen fibrillogenesis, this ratio is modulated by temperature, collagen concentration, pH, and ionic strength, all experimentally accessible quantities. The authors acknowledge that Ts has no direct mapping to biochemical conditions (e.g., pH), yet proceed to speculate in the concluding paragraph about evolutionary fine-tuning of fibril compactness and its role in diseases such as pulmonary emphysema and aortic aneurysm. These biological inferences are unsupported without at least a qualitative discussion of how Ts relates to measurable physical or physiological variables. The manuscript would be strengthened considerably by such a discussion, even at the order-of-magnitude level.*

**Author Response:**
We thank the Referee for highlighting the need to clarify the physical basis of $T_s$. During collagen fibrillogenesis, the resulting molecular organization depends on the competition between the incorporation of new material and the opportunity for local rearrangement during growth. We denote by $\tau_{\mathrm{dep}}$ the characteristic timescale of molecular incorporation within a local growth region and by $\tau_{\mathrm{rel}}$ the characteristic timescale of local surface rearrangement. Accordingly, the ratio $\tau_{\mathrm{dep}}/\tau_{\mathrm{rel}}$ provides a conceptual measure of the opportunity for rearrangement before continued growth modifies the local environment. A larger ratio corresponds to more effective relaxation relative to incorporation, whereas a smaller ratio corresponds to growth with more limited relaxation.

Experimental studies show that temperature and collagen concentration influence nucleation and assembly kinetics, as well as the resulting fibril morphology (Kadler et al., 1988; Yang and Kaufman, 2009; Gobeaux et al., 2008). In turn, pH, ionic strength, and buffer composition modify electrostatic interactions, lateral association, and fibril growth kinetics (Kalbitzer and Pompe, 2018; Morozova and Muthukumar, 2018). These conditions may affect incorporation and relaxation simultaneously, thereby changing the effective balance represented by $\tau_{\mathrm{dep}}/\tau_{\mathrm{rel}}$.

Our algorithm represents this physical competition in a discrete, coarse-grained form through $T_s$. After attachment, each molecule is allowed up to $T_s$ lateral surface-diffusion attempts to search for a configuration with lower exposed surface area. Consequently, increasing $T_s$ represents a greater effective opportunity for post-attachment relaxation relative to continued growth. The parameter is not itself a physical time and does not represent a direct change in any single experimental variable. Rather, it captures the net effect that physicochemical assembly conditions may exert on the relative opportunity for local rearrangement during growth.

We have revised the model description to make this interpretation explicit. Because the model contains no calibrated physical time, it cannot presently assign a unique or quantitative value of $T_s$ to a particular temperature, pH, collagen concentration, ionic strength, or buffer composition. Establishing even an order-of-magnitude correspondence would require experimental estimates of the relevant incorporation and rearrangement timescales, followed by calibration against measured growth kinetics or fibril morphology. We have also removed the evolutionary and disease-specific extrapolations from the conclusion, which is now limited to the model result that greater effective post-attachment relaxation produces more compact fibrils and greater resistance to failure in the simulations.

---

### Point 2 (R1-2): Attribution of Self-Organized Criticality

**Referee Comment:**
> *The authors claim that the rupture process exhibits SOC on the basis that the avalanche size distribution follows a power law. This reasoning is insufficient. SOC requires that a system spontaneously evolves toward a critical state without external tuning of a control parameter, the canonical example being the Bak-Tang-Wiesenfeld sandpile. In the present model, the external force $F$ is continuously increased by the experimenter until failure occurs. The system is driven, not self-organizing.*
>
> *Critically, two of the papers the authors themselves cite to support the SOC claim (refs. [42] and [43], Zapperi et al., PRL 1997 and PRE 1999) make no reference to SOC. Instead, Zapperi et al. explicitly characterize the breakdown point as a first-order transition and draw an analogy with spinodal nucleation, a fundamentally different phenomenology. The correct terminology for the dynamics observed here is "avalanche statistics in driven disordered fracture," not SOC.*
>
> *Furthermore, the power-law regime in Fig. 9(a) spans at most two orders of magnitude in avalanche size, a marginal range. No statistical validation of the power-law hypothesis is presented (e.g., maximum likelihood estimation of the exponent, Kolmogorov-Smirnov test, or comparison with alternative distributions following the methodology of Clauset et al., SIAM Review 51, 661, 2009). The claim of scale-free behavior therefore rests on insufficiently rigorous grounds.*

**Author Response:**
We thank the Referee for this important correction. We agree that the observation of an approximately linear regime in a binned log-log avalanche-size distribution is not sufficient to establish Self-Organized Criticality. In our model, the external force $F$ is progressively increased, damage is irreversible, and failed molecules do not recover. The system therefore does not autonomously evolve toward a stationary critical state.

We have removed the SOC and scale-free terminology throughout the manuscript and now describe the observed behavior as stochastic local-avalanche dynamics in a driven disordered fracture process. We have also removed the interpretation of the fitted slope as evidence of a change in criticality, load-sharing universality, or a crossover between local and global load sharing. Until the distributional hypothesis is tested on the raw discrete event sizes, the existing straight-line fits to the binned data are presented only as descriptive summaries and not as statistical validation of a pure power law. The requested maximum-likelihood estimation, goodness-of-fit testing, and comparison with alternative distributions will be addressed separately in our statistical reanalysis.

---

### Point 4 (R1-4): Cross-sectional fractal dimension and three-dimensional mechanical structure

**Referee Comment:**
> *The fractal dimension is measured in 2D but used to characterize a 3D mechanical problem. $D_f$ is estimated from 2D cross-sectional projections ($x$-$z$ plane), yet the backbone identification and the entire fracture simulation are three-dimensional. The relationship between the 2D cross-sectional $D_f$ and the 3D structural properties that govern mechanical response is not established. The authors use the 2D $D_f$ as a proxy for overall fibril compactness without justification. This connection should either be derived or explicitly discussed as an assumption with its limitations.*

**Author Response:**
We thank the Referee for pointing out that the original manuscript did not adequately establish the connection between the cross-sectional fractal dimension and the three-dimensional mechanical structure. The cross-sectional $D_f$ characterizes transverse packing, which is directly relevant to the rupture model because the tensile stress at each axial position is determined by the load-bearing area $N(i)$ of the corresponding cross-section, while molecular resistance depends on coordination within the three-dimensional backbone.

To test this connection explicitly, for each $T_s$ we obtained $D_f$ from the ensemble mass--radius curve constructed using 11 transverse cross-sections from each of 50 independent fibrils. From the corresponding three-dimensional load-bearing backbones, we measured four mechanically relevant descriptors: the mean cross-sectional load-bearing area $\langle N\rangle$; the mean molecular coordination $\langle K\rangle$; the axial coefficient of variation of the load-bearing area,

$$
\mathrm{CV}(N)=\frac{\mathrm{SD}[N(i)]}{\langle N\rangle},
$$

which quantifies the relative variation of $N(i)$ along the 201 axial layers; and the mean molecular stress exposure at unit force, $\langle\sigma_M\rangle_{F=1}$, obtained by evaluating the molecular stress defined in Eq. (3) at $F=1$ and averaging it over the backbone molecules. These descriptors were averaged over the independent fibrils, with their uncertainties reported as standard errors of the mean. The uncertainty in $D_f$ corresponds to the standard error of the linear mass--radius fit. Because the relationships are monotonic and approach plateaus rather than remaining linear, associations were evaluated using Spearman's rank correlation coefficient, $\rho$ ([Spearman, 1904](https://doi.org/10.2307/1412159)), between the ten $T_s$-averaged conditions.

The cross-sectional $D_f$ was positively associated with the mean load-bearing area ($\rho=0.988$) and mean molecular coordination ($\rho=1.000$), and inversely associated with the axial variability of the load-bearing area ($\rho=-0.782$) and mean molecular stress exposure at unit force ($\rho=-0.964$). Thus, increasing $D_f$ accompanies cross-sections that contain more load-bearing material, greater molecular coordination, reduced axial heterogeneity, and lower mean stress exposure for the same applied force.

Taken together, these results provide direct numerical validation that $D_f$ captures structural changes relevant to axial load bearing: increasing $D_f$ corresponds to larger, better-coordinated, and more axially uniform load-bearing backbones, with lower mean stress exposure for the same applied force. Within its stated scope, which is the comparison of fibril ensembles generated at different $T_s$, $D_f$ therefore provides a compact and quantitatively supported proxy for mechanically relevant transverse compactness. We have revised the manuscript to make this interpretation and its scope explicit.

---

### Point 6 (R1-6): Molecular aspect ratio

**Referee Comment:**
> *The aspect ratio of model molecules (18:1) differs substantially from that of real collagen molecules ($\approx 200{:}1$). The impact of this simplification on the fractal dimension and packing geometry should be acknowledged.*

**Author Response:**
We thank the Referee and agree that the reduced molecular aspect ratio is an important limitation. The model uses rods with an aspect ratio of $18{:}1$, substantially smaller than the approximately $200{:}1$ aspect ratio of real collagen molecules. We now acknowledge that this simplification may affect intermolecular overlaps and coordination, packing and void geometry, the measured cross-sectional fractal dimension, and rupture statistics. Since its quantitative effects were not assessed, the reported results are interpreted as trends of the coarse-grained model rather than as quantitative predictions for real collagen fibrils.

---

### Point 7 (R1-7): Phenomenological damage function

**Referee Comment:**
> *The phenomenological function $f(F)$ in Eq. (5) is purely empirical. Its form is not derived from the model and the physical interpretation of the parameters $\alpha$ and $\beta$, while discussed qualitatively, would benefit from more precise justification.*

**Author Response:**
We thank the Referee for this observation and agree that Eq. (5) is empirical and is not derived from the microscopic rupture rules of the model. We have revised the manuscript to identify it explicitly as a phenomenological interpolation of the simulated damage curves. The power-law and exponential contributions are now described only as providing the flexibility needed to represent the gradual curvature and the steep high-force increase, respectively. Accordingly, $\alpha$ and $\beta$ are treated as empirical shape parameters, and we no longer associate them with distinct microscopic damage mechanisms. Their variation with $T_s$ is retained only as a compact description of the systematic changes in the damage curves.

---

## Response to Referee 2

### Point 1 (R2-1): Loading protocol and stability of the system

**Referee Comment:**
> *My main concern is the loading protocol. Equation (4) defines the probability of failure. As long as fibers carry load, this probability remains finite. This seems to imply that, at any finite load, the bundle would fail after a finite time, with a characteristic time depending on the load level. The authors state that during a sweep through the system, each fiber is given a chance to fail according to Eq. (4), and if no failure occurs, the external load is increased. This procedure appears somewhat artificial. If I understand the model correctly, the bundle is not fully relaxed after a sweep: failure could continue in a subsequent sweep at the same load level. Moreover, fiber removal increases ($\sigma_M$) and decreases ($K$), both of which increase the rupture probability ($P_R$). Thus, the system does not seem to be in a stable state when the external load is further increased. The authors should clarify this point in the manuscript.*

**Author Response:**
We thank the Referee for identifying an ambiguity in our use of the term "stable." We agree that, if Eq.~(4) were interpreted as a continuous-time hazard rate and the fibril were held indefinitely at fixed $F$, a finite removal probability would imply the possibility of delayed failure. This is not the process represented by our model.

Our simulations follow the discrete tensile-loading protocol introduced for simulated collagen fibrils by Parkinson et al. (1997), which is now cited at this point in the revised Methods. At a prescribed force $F$, every molecule in the load-bearing backbone is assessed once. If at least one molecule is removed, the backbone is reassessed and another sweep is performed at the same force. The first complete sweep with no new removals terminates that force step, and only then is the force increased by $\Delta F=0.5$. Parkinson et al. use the same stopping rule: the skeleton and stress state are reassessed after breaking events, and the force is increased only when no new breaking event occurs.

We have revised the Methods to make clear that a zero-removal sweep is an **operational stopping criterion** defining a quiescent configuration within this discrete loading algorithm. It is not intended to establish thermodynamic stability or to predict the long-time response under a force held constant indefinitely. The sweep index has no calibrated physical duration, and $P_R$ is a per-assessment removal probability, not a continuous-time kinetic rate. Consequently, creep, fatigue, and delayed rupture under sustained loading are outside the scope of the model.

This clarification preserves the original simulation protocol and the resulting data while stating its physical interpretation and limitation explicitly.

---

### Point 3 (R2-3): Definition of avalanches

**Referee Comment:**
> *Since load sharing according to Eq. (2) is global within a cross section, it seems that no particular stress concentration can develop around failed (removed) fibers in that cross section. If this interpretation is correct, then the definition of avalanches may require further justification. If the stress field is not localized around failed clusters, it is not obvious why avalanches should be defined as steps in the growth of connected failed clusters. An alternative, and possibly more natural, definition would be to regard an avalanche as the set of fibers that fail between two consecutive increments of the external force. The authors should make this aspect of the work clearer.*

**Author Response:**
We thank the Referee for this important observation. We agree that Eq. (2) distributes the load uniformly within each cross-section and that our model does not include a localized elastic stress-redistribution kernel. Nevertheless, removing a molecule directly modifies the cross-sectional stresses only in the sections it previously occupied and reduces the coordination number $K$ of its nearest neighbors. Consequently, damage evolution retains a local structural component even though load is uniformly shared within each affected cross-section.

We quantify this component by partitioning all molecules removed at a fixed force $F$ into nearest-neighbor connected clusters. Following the global-avalanche/local-cluster distinction used by [Laurson, Santucci, and Zapperi, *Phys. Rev. E* **81**, 046116 (2010)](https://doi.org/10.1103/PhysRevE.81.046116), we refer to each connected component as a local avalanche (or avalanche cluster). Spatially disconnected clusters are counted as distinct events, so multiple local avalanches may occur at the same $F$. This is an operational classification of local damage and is not intended to imply a standard local-load-sharing mechanism. We have clarified this definition and its physical motivation in the revised Methods.

---

### Point 4 (R2-4): Power-law statistics and SOC

**Referee Comment:**
> *The interpretation of power-law statistics in terms of self-organized criticality should be treated with caution. In rupture processes the system is gradually destroyed, and there is no healing mechanism by which failed fibers could recover and carry load again. Therefore, the analogy with self-organized critical systems may be problematic unless it is carefully qualified. I suggest that the authors either provide a more detailed justification for this interpretation or reformulate the discussion in more cautious terms.*

**Author Response:**
We agree with the Referee. Because the fracture process is externally driven and irreversible, with no healing mechanism, we no longer interpret the avalanche statistics as evidence of Self-Organized Criticality. The revised manuscript instead describes the process as stochastic local-avalanche dynamics during progressive damage in a driven disordered system. We have removed the SOC and scale-free terminology and explicitly state that the current binned linear fits do not by themselves validate a power-law distribution.

---

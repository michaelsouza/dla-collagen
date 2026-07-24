# Response to Referee Reports — ER12738

## Response to Referee 1

### Point 1 (R1-1): Physical grounding of the surface-diffusion parameter $T_s$

**Referee Comment:**
> *Ts controls the number of post-attachment lateral diffusion steps and therefore governs the ratio between the molecular relaxation timescale and the fibril growth rate. In real type I collagen fibrillogenesis, this ratio is modulated by temperature, collagen concentration, pH, and ionic strength, all experimentally accessible quantities. The authors acknowledge that Ts has no direct mapping to biochemical conditions (e.g., pH), yet proceed to speculate in the concluding paragraph about evolutionary fine-tuning of fibril compactness and its role in diseases such as pulmonary emphysema and aortic aneurysm. These biological inferences are unsupported without at least a qualitative discussion of how Ts relates to measurable physical or physiological variables. The manuscript would be strengthened considerably by such a discussion, even at the order-of-magnitude level.*

**Author Response:**
We thank the Referee for this insightful comment. We fully agree that $T_s$ serves as an effective, coarse-grained kinetic parameter representing the net competition between post-attachment surface relaxation ($\tau_{\mathrm{rel}}$) and molecular accretion/incorporation rate ($\tau_{\mathrm{dep}}$), governed by the combined physicochemical conditions of the solution (temperature, pH, ionic strength, monomer concentration, and buffer composition), rather than a one-to-one quantitative mapping to a single variable.

In response to the Referee's suggestion, we have made the following revisions to the manuscript:
1. **Methods / Model Formulation (Section II, Paragraph 1):** We explicitly frame $T_s$ as a dimensionless kinetic control parameter proportional to $\tau_{\mathrm{dep}}/\tau_{\mathrm{rel}}$, detailing how experimental variables (such as temperature, pH, and ionic strength) alter the relaxation-to-growth balance during fibrillogenesis (citing Yang et al., 2009; Kalbitzer et al., 2018; Morozova et al., 2018).
2. **Discussion (Section IV):** We clarified that $T_s$ functions as a coarse-grained parameter representing the net balance of physicochemical assembly conditions, acknowledging that our model does not establish a 1-to-1 mapping or separate calibration for individual experimental variables.
3. **Conclusion (Section V):** We have removed the unsupported evolutionary fine-tuning speculations and disease-specific extrapolations (e.g., emphysema, aortic dissection, aneurysm). We now state strictly that physicochemical assembly conditions control structural compactness and the resulting mechanical resilience of collagen fibrils through the surface-relaxation parameter $T_s$.

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

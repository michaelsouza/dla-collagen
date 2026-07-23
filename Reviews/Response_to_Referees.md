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

## Response to Referee 2

### Point 1 (R2-1): Loading protocol and stability of the system

**Referee Comment:**
> *My main concern is the loading protocol. Equation (4) defines the probability of failure. As long as fibers carry load, this probability remains finite. This seems to imply that, at any finite load, the bundle would fail after a finite time, with a characteristic time depending on the load level. The authors state that during a sweep through the system, each fiber is given a chance to fail according to Eq. (4), and if no failure occurs, the external load is increased. This procedure appears somewhat artificial. If I understand the model correctly, the bundle is not fully relaxed after a sweep: failure could continue in a subsequent sweep at the same load level. Moreover, fiber removal increases ($\sigma_M$) and decreases ($K$), both of which increase the rupture probability ($P_R$). Thus, the system does not seem to be in a stable state when the external load is further increased. The authors should clarify this point in the manuscript.*

**Author Response:**
We thank the Referee for raising this important question. We apologize for the brevity of our original description, which led to a misunderstanding of our loading protocol.

We wish to clarify that our simulation **already implements the exact iterative relaxation procedure** suggested by the Referee to ensure mechanical stability at each force level before increasing the external load:

1. **Iterative Relaxation at Constant Force:** At a given force level $F$, when one or more molecules detach during a sweep, the load-bearing geometry changes, increasing local stresses $\sigma(i)$ and decreasing coordination numbers $K$. Rather than increasing the external load immediately, our algorithm performs **iterative sweeps at the same force level $F$**, recalculating $\sigma(i)$, $K$, and $P_R$ after every pass. These sweeps repeat until a full sweep results in **zero additional removals**, confirming that the backbone has reached a fully relaxed, mechanically stable state under load $F$. After relaxation, the set of all molecules removed at force $F$ is partitioned into spatially contiguous clusters of nearest neighbors; each such cluster constitutes an **individual avalanche of size $s$**. Multiple independent avalanches may therefore be recorded at a single force level. This local, spatial definition of avalanches captures the correlated propagation of micro-damage through nearest-neighbor interactions.
2. **Quasistatic Loading Protocol:** The external force is incremented ($F \to F + \Delta F$) **only after** mechanical equilibrium is established at force $F$.
3. **Physical Meaning of $P_R$:** In this quasistatic (athermal) framework, $P_R$ is evaluated per discrete load step to model stochastic variations in local bond detachment thresholds under quasistatic loading, rather than serving as a continuous-time thermal rate in a time-dependent creep or fatigue process. Once the system reaches equilibrium at force $F$ (no remaining molecules satisfy $u < P_R$), no further detachments occur at that load level.

We have revised Section III (Model / Rupture Protocol, Paragraph 5) of the manuscript to state this iterative relaxation protocol explicitly.

---

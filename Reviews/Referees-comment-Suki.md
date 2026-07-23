# Reports ER12738/Tavares

## Referee R1 

---

The authors present a computational study of collagen fibril formation using a modified diffusion-limited aggregation (DLA) model in which a surface diffusion parameter Ts controls the degree of lateral compaction after molecular attachment. They characterize the resulting morphology through the fractal dimension Df of 2D cross-sections, and couple the growth model to a probabilistic fracture simulation to investigate rupture statistics. They report that increasing Ts drives a crossover from fractal to compact packing (Df rising from 1.71 to 1.96) and that the avalanche size distribution follows a power law P(s) ~ s^{−γ}, with γ increasing from ≈ 2.3 to ≈ 2.8 as Ts increases, crossing the mean-field ELS value γ = 5/2. The authors interpret this progression as a crossover from local to global load-sharing universality, and attribute the overall rupture dynamics to Self-Organized Criticality (SOC).

The coupling of a structural growth model with a stochastic fracture framework to study the relationship between fibril morphology and failure statistics is a legitimate and interesting approach. However, the manuscript contains several conceptual errors and unsupported claims that must be addressed before it can be considered for publication.

### MAJOR CONCERNS

#### R1-1. The model parameter Ts lacks physical grounding

Ts controls the number of post-attachment lateral diffusion steps and therefore governs the ratio between the molecular relaxation timescale and the fibril growth rate. In real type I collagen fibrillogenesis, this ratio is modulated by temperature, collagen concentration, pH, and ionic strength, all experimentally accessible quantities. The authors acknowledge that Ts has no direct mapping to biochemical conditions (e.g., pH), yet proceed to speculate in the concluding paragraph about evolutionary fine-tuning of fibril compactness and its role in diseases such as pulmonary emphysema and aortic aneurysm. These biological inferences are unsupported without at least a qualitative discussion of how Ts relates to measurable physical or physiological variables. The manuscript would be strengthened considerably by such a discussion, even at the order-of-magnitude level.

**Author [Suki] comments:**

THIS DOES NOT NEED ANY NEW COMPUTATIONS. IF THE CONDITIONS ARE RIGHT - INCLUDING TEMPERATURE, pH AND MONOMER CONCENTRATION IN SOLUTION - FIBRILS NATURALLY START ASSEMBLING. BUT THIS PROCESS IS SLOW AND NOT TOO EFFICIENT. IN TISSUES, CELLS CONTRIBUTE A LOT, THE SECRETE THE COLLAGEN MONOMERS OR EVEN MICROFIBRILS AT THE RIGHT POSITION TO DEPOSIT THEM PROPERLY. SINCE WE DO NOT MODEL CELLS EXPLICITELY,THE LATERAL DIFFUSION IS KIND OF MIMICKING THE CELL'S CONTRIBUTION. Ts INCORPORATES THIS MECHANISM, BUT WE DO NOT HAVE ANY KNOWLEDGE HOW THE CELL FIGURES OUT WHERE TO DEPOSIT AND WHETHER TO ADD ANY LOCAL TENSION. HENCE, IN OUR MODEL, WE NEED TO FIGURE OUT WHAT Ts WORKS BEST. IT'S ALMOST LIKE FIGURING OUT WHAT THE CELL DOES WHEN IT BUILDS FIBERS. ONE POSSIBLE ANSWER TO THIS QUESTION IS TO ADD A RATIONALE WHEN WE INTRODUCE Ts, RATHER THAN EXPLAIN SOMETHING IN THE DISCUSSION.

#### R1-2. The attribution of Self-Organized Criticality is incorrect

The authors claim that the rupture process exhibits SOC on the basis that the avalanche size distribution follows a power law. This reasoning is insufficient. SOC requires that a system spontaneously evolves toward a critical state without external tuning of a control parameter, the canonical example being the Bak-Tang-Wiesenfeld sandpile. In the present model, the external force F is continuously increased by the experimenter until failure occurs. The system is driven, not self-organizing.

Critically, two of the papers the authors themselves cite to support the SOC claim (refs. [42] and [43], Zapperi et al., PRL 1997 and PRE 1999) make no reference to SOC. Instead, Zapperi et al. explicitly characterize the breakdown point as a first-order transition and draw an analogy with spinodal nucleation, a fundamentally different phenomenology. The correct terminology for the dynamics observed here is "avalanche statistics in driven disordered fracture," not SOC.

Furthermore, the power-law regime in Fig. 9(a) spans at most two orders of magnitude in avalanche size, a marginal range. No statistical validation of the power-law hypothesis is presented (e.g., maximum likelihood estimation of the exponent, Kolmogorov-Smirnov test, or comparison with alternative distributions following the methodology of Clauset et al., SIAM Review 51, 661, 2009). The claim of scale-free behavior therefore rests on insufficiently rigorous grounds.

**Author [Suki] comments:**

MAYBE WE JUST ELIMINATE SOC ALTOGETHER FROM THE PAPER. WE WILL HAVE TO DO THE TESTS THE REVIEWER ASKS. I ATTACHED A PAPER THAT USES MAXIMUM LIKELIHOOD ESTIMATION. WE COULD ALSO TRY THE POWER LAW WITH AN EXPONENTIAL CUTOFF AND A LOGNORMAL PERHAPS AND SHOW THAT HOPFULLY THE POWERLAW HOLDS. BUT I HAVE TO SAY THAT IN A DIFFERENT STUDY WE FOUND THAT POWER LAW WITH EXPONENTIAL CUTOFF IS MUCH BETTER THAN THE PLAIN POWER LAW. IN FACT FITTING A STRAIGHT LINE TO THE BINNED DATA IS NOT AS GOOD AS USING ALL DATA WITHOUT ARBITRARY BINNING METHOD IN THE MAXIMUM LIKELIHOOD ESTIMATION.

#### R1-3. The interpretation of γ > 5/2 has no support in fiber bundle theory

The authors interpret their measured exponent γ ≈ 2.8 (at high Ts) as evidence of a regime beyond equal load sharing (ELS), signaling a crossover to global load-sharing universality. This interpretation is incorrect.

In fiber bundle models, γ = 5/2 is the exact mean-field result for ELS, the limiting case of maximally global stress redistribution (Hemmer & Hansen, J. Appl. Mech. 59, 909, 1992; Daniels, Proc. R. Soc. London A 183, 405, 1945). There is no established theoretical framework that predicts or interprets exponents above 5/2 in this context.

Moreover, Pradhan, Hansen & Chakrabarti (Rev. Mod. Phys. 82, 499, 2010), also cited by the authors, demonstrate that within ELS, the avalanche exponent undergoes a crossover from γ = 5/2 (generic regime, away from failure) to γ = 3/2 (near the critical breakdown point). That is, as stress redistribution becomes maximally global near rupture, the exponent DECREASES, not increases. The authors' claim that γ > 5/2 signals increasingly global load sharing is therefore the opposite of what the established theory predicts.

The observed deviation from 5/2 is more plausibly attributable to finite-size effects, limited ensemble statistics (10 fibrils per Ts value), the restricted range over which the power law is fitted, or the specific definition of avalanche adopted in the model. A sensitivity analysis with respect to the Weibull modulus m (fixed at m = 2 throughout, following ref. [35]) would also help assess the robustness of the exponents.

**Author [Suki] comments:**

HERE AGAIN PROPER ESTIMATION OF THE EXPONENT IS EXTREMELY IMPORTANT. WHAT IF THE REVIEWER IS RIGHT AT THE VARIATION IN EXPONENT IS AN ARTIFACT OF LEAST SQUARES FITTING? UNTIL WE FIGURE OUT THE PROPER EXPONENTS, WE CAN'T SAY MUCH. ALSO, IF POSSIBLY ADDING MORE SIMULATIONS AND/OR INCREASING THE SYSTEM SIZE MIGHT BE USEFUL. 

#### R1-4. The fractal dimension is measured in 2D but used to characterize a 3D mechanical problem

Df is estimated from 2D cross-sectional projections (x-z plane), yet the backbone identification and the entire fracture simulation are three-dimensional. The relationship between the 2D cross-sectional Df and the 3D structural properties that govern mechanical response is not established. The authors use the 2D Df as a proxy for overall fibril compactness without justification. This connection should either be derived or explicitly discussed as an assumption with its limitations.

**Author [Suki] comments:**

THIS NEEDS TO BE DONE AND COULD BE VERY INTERESTING. 

#### R1-5. The central structural-mechanical connection is purely empirical

The key result of the paper, that Df and γ saturate together at Ts ≥ 512, is presented as if it were a derived causal relationship. In fact, it is a numerical correlation observed in simulation. No theoretical framework is provided that connects the fractal dimension of the fibril cross-section to the avalanche exponent of the fracture process. The statement that "the fibril's fractal dimension serves as a quantitative bridge between structural compactness and failure statistics" (Conclusion) overstates what has been demonstrated. The authors should reframe this as an empirical observation and discuss what theoretical framework might, in the future, explain such a connection.

**Author [Suki] comments:**

THE REVIEWER IS RIGHT. THE EASY SOLUTION IS TO TONE DOWN THIS CLAIM. THE HARDER IS TO FIND SOME TRUE RELATIOSHIP BETWEEN Df AND THE EXPONENT WHICH I DON'T KNOW HOW TO DO. 

### MINOR COMMENTS

#### R1-6. Aspect ratio of model molecules

The aspect ratio of model molecules (18:1) differs substantially from that of real collagen molecules (≈ 200:1). The impact of this simplification on the fractal dimension and packing geometry should be acknowledged.

#### R1-7. Justification of the phenomenological function f(F)

The phenomenological function f(F) in Eq. (5) is purely empirical. Its form is not derived from the model and the physical interpretation of the parameters α and β, while discussed qualitatively, would benefit from more precise justification.

### RECOMMENDATION

The manuscript requires major revision. The authors should: (1) provide physical grounding for the parameter Ts; (2) replace the SOC terminology with an accurate description of driven disordered fracture; (3) revise the interpretation of γ > 5/2 in light of established fiber bundle theory; (4) address the 2D/3D inconsistency in the fractal dimension analysis; and (5) reframe the Df–γ correlation as an empirical finding rather than a derived result. The statistical treatment of the power-law distributions must also be made rigorous.

## Referee R2

The authors present a computational study of the assembly of collagen fibrils and their rupture behavior under axial loading. The assembly process is modeled by three-dimensional diffusion-limited aggregation, complemented by a surface relaxation mechanism. The duration of this relaxation process is an important model parameter, as it controls the final geometrical structure of the collagen fibril. The authors show that, in the plane perpendicular to the fibril axis, the resulting geometry is consistent with the structure of DLA clusters, and that with increasing relaxation time the fractal dimension increases towards 2.

In the second part of the paper, the authors investigate the rupture of the bundle of chain molecules under a slowly increasing axial load. The molecules do not essentially break; rather, they detach from each other, so the failure mechanism resembles a kind of fiber pull-out in the terminology of fiber-bundle models. The failure model is stochastic: the load acting on load-bearing fibers is affected by the load-bearing cross-sectional area along the fibril axis, while the failure probability depends on the local neighborhood of a fiber. The authors obtain power-law statistics for avalanche sizes and argue that, as the structure becomes more compact, a transition occurs that is similar to the crossover from localized to equal-load-sharing behavior in fiber-bundle models.

The paper is clearly written, and the presentation of the model and of the numerical procedure is easy to follow. The data shown in the figures support the main arguments of the authors. In my view, the analysis of the collagen fibril structure and its mapping to DLA clusters is rather straightforward, while the main novelty of the work lies in the failure simulations and in the analysis of avalanche statistics. Before making a recommendation on publication, however, I believe that the authors should clarify several important points.

### R2-1. Loading protocol and stability of the system

My main concern is the loading protocol. Equation (4) defines the probability of failure. As long as fibers carry load, this probability remains finite. This seems to imply that, at any finite load, the bundle would fail after a finite time, with a characteristic time depending on the load level. The authors state that during a sweep through the system, each fiber is given a chance to fail according to Eq. (4), and if no failure occurs, the external load is increased. This procedure appears somewhat artificial. If I understand the model correctly, the bundle is not fully relaxed after a sweep: failure could continue in a subsequent sweep at the same load level. Moreover, fiber removal increases (\sigma_M) and decreases (K), both of which increase the rupture probability (P_R). Thus, the system does not seem to be in a stable state when the external load is further increased. The authors should clarify this point in the manuscript.
   
**Author [Suki] comments:**

THIS SHOULD BE EASY, JUST EXPANDING THE EXPLANATION. BUT LOOKING AT THE EQUATIONS AGAIN, I WONDER WHAT WOULD HAPEN IF IN EQUATION 4, WE USED THE MAXIMUM SIGMA, NOT THE AVERAGE SIGMA FROM EQUATION 3. USUALLY THINGS BREAK AT THE MAXIMUM STRESS. 

### R2-2. Localized vs. equal load sharing

The authors discuss localized and more equal load-sharing regimes in their interpretation. However, in the simulations, load sharing appears to be determined by Eqs. (2) and (3), which seem to impose equal load sharing within a cross section. If I understand correctly, information about the local structure enters only through (K) in the rupture probability. The authors should discuss more clearly in what precise sense the model realizes localized or equal-load-sharing behavior.

**Author [Suki] comments:**

AGAIN, JUST EXPANDING THE TEXT. 

### R2-3. Definition of avalanches

Since load sharing according to Eq. (2) is global within a cross section, it seems that no particular stress concentration can develop around failed (removed) fibers in that cross section. If this interpretation is correct, then the definition of avalanches may require further justification. If the stress field is not localized around failed clusters, it is not obvious why avalanches should be defined as steps in the growth of connected failed clusters. An alternative, and possibly more natural, definition would be to regard an avalanche as the set of fibers that fail between two consecutive increments of the external force. The authors should make this aspect of the work clearer.

**Author [Suki] comments:**

I THINK THIS COULD LEAD TO GROUPPING 2 DISTINCT AVALANCHES FAR FROM EACH OTHER. BUT HE MAKES A POINT ABOUT STRESS CONCENTRATION WHICH I ALSO MENTIONED IN RESPONSE TO HIS FIRST COMMENT. NEVERTHELESS, STRESS CONCENTRATIONS SHOULD NATURALLY DEVELOP RIGHT AFTER A MOLECULE IS REMOVED SINCE THE FORCE IS THE SAME, BUT THE LOAD SHARING POSSIBILITY IS REDUCED. AGAIN, POSSIBLY SOME CLARIFICATION HERE MIGHT BE ENOUGH.

### R2-4. Power-law statistics

The interpretation of power-law statistics in terms of self-organized criticality should be treated with caution. In rupture processes the system is gradually destroyed, and there is no healing mechanism by which failed fibers could recover and carry load again. Therefore, the analogy with self-organized critical systems may be problematic unless it is carefully qualified. I suggest that the authors either provide a more detailed justification for this interpretation or reformulate the discussion in more cautious terms.

**Author [Suki] comments:**

I THINK HE IS RIGHT. WE JUST NEED TO REMOVE CALLING THIS SOC. MAYBE IN A FOLLOW-UP, LOADING AND BREAKING COULD BE COUPLED WITH BUILDING BY ADDING MONOMERS. IF THE BUILDING OCCURS IN SUCH A WAY THAT THE RELAXATION DURING Ts REINFORCES THE FIBER BY ADDING MOST MATERIAL WHERE THE NUMBER OF CONTACTS IS THE SMALLEST PER CROSS SECTION (OR THE LOCAL STIFFNESS IS THE LOWEST), THEN SOME SOC-TYPE OF BEHAVIOR MIGHT EMERGE.
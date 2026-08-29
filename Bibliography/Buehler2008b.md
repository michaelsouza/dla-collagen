JOURNAL OF THE MECHANICAL BEHAVIOR OF BIOMEDICAL MATERIALS I (2008) 59-67

ELSEVIER

available at www.sciencedirect.com

ScienceDirect

journal homepage: www.elsevier.com/locate/jmbbm

SCIENCE DIRECT

Research paper

# Nanomechanics of collagen fibrils under varying cross-link densities: Atomistic and continuum studies

Markus J. Buehler*

Laboratory for Atomistic and Molecular Mechanics, Department of Civil and Environmental Engineering, Massachusetts Institute of Technology, 77 Massachusetts Ave. Room 1-272, Cambridge, MA 02139, USA

# ARTICLEINFO

Article history:

Received 8 February 2007

Received in revised form

5 April 2007

Accepted 6 April 2007

Published online 15 June 2007

Keywords:

Collagen

Tropocollagen

Fibril

Fracture

Brittle

Cross-link density

Nanomechanics

# ABSTRACT

Collagen is a protein material with intriguing mechanical properties — it is highly elastic, shows large fracture strength and plays a crucial role in making Nature's structural materials tough. Collagen based tissues consist of collagen fibrils, each of which is composed out of a staggered array of ultra-long tropocollagen molecules extending to several hundred nanometers. Albeit the macroscopic properties of collagen based tissues have been studied extensively, less is known about the nanomechanical properties of tropocollagen molecules and collagen fibrils, their elementary building blocks. In particular, the relationship between molecular properties and tissue properties remains a scarcely explored aspect of the science of collagen materials. Results of molecular multi-scale modeling of the nanomechanical properties of the large-strain deformation regime of collagen fibrils under varying cross-link densities are reported in this paper. The results confirm the significance of cross-links in collagen fibrils in improving its mechanical strength. Further, it is found that cross-links influence the nature of its large-deformation and fracture behavior. Cross-link deficient collagen fibrils show a highly dissipative deformation behavior with large yield regimes. Increasing cross-link densities lead to stronger fibrils that display an increasingly brittle deformation character. The simulation results are compared with recent nanomechanical experiments at the scale of tropocollagen molecules and collagen fibrils.

© 2007 Elsevier Ltd. All rights reserved.

# 1. Introduction

Collagen, the most abundant protein on earth, is a fibrous structural protein with superior mechanical properties, and provides an intriguing example of a hierarchical biological nanomaterial (Bozec and Horton, 2005; Bhattacharjee and Bansal, 2005; Anderson, 2005; Sun et al., 2004; An et al., 2004; Lees, 2003; Sun et al., 2002; Hellmich and Ulm, 2002; Jager and Fratzl, 2000; Waite et al., 1998; Borel and Monboisse, 1993;

Lees, 1987; Fratzl et al., 2004; Hulmes et al., 1995). Collagen consists of tropocollagen (TC) molecules that have lengths of  $L \approx 300 \mathrm{~nm}$  with approximately  $1.5 \mathrm{~nm}$  in diameter, leading to an aspect ratio of close to 200 (Bozec and Horton, 2005; Bhattacharjee and Bansal, 2005; Sun et al., 2004; Hulmes et al., 1995; Puxkandl et al., 2002; Sasaki and Odajima, 1996). Staggered arrays of TC molecules form fibrils, which arrange to form collagen fibers. A schematic of the main hierarchical features of collagen is shown in Fig. 1.

* Tel.: +1 617 452 2750; fax: +1 617 258 6775.
E-mail address: mbuehler@MIT.EDU.
1751-6161/$ - see front matter © 2007 Elsevier Ltd. All rights reserved.
doi:10.1016/j.jmbbm.2007.04.001

---

JOURNAL OF THE MECHANICAL BEHAVIOR OF BIOMEDICAL MATERIALS I (2008) 59-67

![img-0.jpeg](img-0.jpeg)
Fig. 1 – Schematic view of some of the hierarchical features of collagen, ranging from the amino acid sequence level at nanoscale up to the scale of collagen fibers with lengths on the order of $10\,\mu\mathrm{m}$. The present study is focused on the mechanical properties of collagen fibrils, consisting of a staggered array of TC molecules. The red lines in the graph indicate intermolecular cross-links that are primarily developed at the ends of tropocollagen molecules. In this paper, particular attention is paid to the mechanical properties as a function of varying cross-link densities. (For interpretation of the references to colour in this figure legend, the reader is referred to the web version of this article.)

Collagen plays an important role in many biological tissues, including tendon, bone, teeth, cartilage or in the eye's cornea (Bozec and Horton, 2005; Bhattacharjee and Bansal, 2005; Hellmich and Ulm, 2002; Borel and Monboisse, 1993; Puxkandl et al., 2002; Bozec et al., 2005; Buehler, in press). Severe mechanical tensile loading of collagen is significant under many physiological conditions, such as in joints and in bone (Nalla et al., 2005; Ritchie et al., 2004).

Despite the significance of the large-deformation behavior of collagen based tissues, few studies have been reported focusing on analyzing the fundamental deformation mechanisms under mechanical load. In particular, the relation of the molecular and intermolecular properties with tissue properties are not understood well. Moreover, the limiting factors in strength of collagen fibrils, and the origins of toughness remain largely unknown. Experimental efforts focused on the deformation mechanics of collagen fibrils at nanoscale, including characterization of changes of D-spacing and fibril orientation (Hulmes et al., 1995; Sasaki and Odajima, 1996; Orgel et al., 1995), analyses that featured in X-ray diffraction (Hulmes et al., 1995) and synchrotron radiation experiments (Puxkandl et al., 2002). Other experimental studies were focused on the averaged response of arrays of collagen fibrils, considering nanoscale deformation mechanisms (Gupta et al., 2005).

Most research was focused on the macroscopic, overall mechanical properties of collagen fibers and scales beyond, for example of tissues, often without explicitly considering the molecular nanoscale structure (Bozec et al., 2005). Other studies focused on the properties of individual TC molecules, without linking to the macroscopic materials' response (Bhattacharjee and Bansal, 2005; Sun et al., 2004; An et al., 2004; Lorenzo and Caffarena, 2005).

There exist few models that link properties of individual molecules with the overall mechanical response of fibrils or fibers, considering the different types of chemical bonding and nanoscale mechanics and geometry. Constitutive models of the mechanical behavior of collagen fibrils typically feature empirical parameters or are derived from experimental observations. However, such models are not predictive since they are not based on fundamental molecular details of the chemical bonding in collagen.

## 1.1. Predictive atomistic based modeling of deformation and fracture collagen

In order to develop a fundamental and quantitative understanding of collagen mechanics, theoretical models encompassing the mesoscopic scales between the atomistic and the macroscopic level, considering atomistic and chemical interactions during deformation are vital. This represents an alternative strategy capable of predicting the properties of collagen tissue from the bottom up.

In order to achieve this goal, a parameter free atomistic based model of the mechanical properties of collagen fibrils, based solely on atomistic simulation input data (Buehler, 2006a,b) can be used.

## 1.2. Research strategy

To understand the influence of cross-links on the deformation mechanics of collagen fibrils, a series of computational experiments of pulling individual collagen fibrils with increasing density of cross-links is carried out. All results are compared with a control system of a cross-link free collagen fibril. Systematic increases of the density of cross-links enable one to observe the difference in mechanical behavior. Particular attention is paid to the small- and large-deformation behavior and the effect of intermolecular cross-links on the mechanical properties and deformation mechanisms.

In particular, studies are carried out that focus on the changes in the elastic and fracture behavior of the collagen fibril as the parameters are varied. An analysis of the molecular mechanisms allows one to develop a mechanistic understanding of the deformation behavior of collagen fibrils.

## 2. Molecular model of collagen fibrils

### 2.1. Reactive mesoscopic model: Formulation

The studies reported in this paper are carried out using a reactive mesoscopic model describing TC molecules as a collection of particles interacting according to multi-body potentials, as described in a series of earlier publications (Buehler, 2006a,b). The present paper describes an application of this molecular model, and thus details about model development are omitted.

The mesoscopic, molecular model does not contain full atomistic information about all atoms in the residues and all side chains, since it is based on the idea of representing

---

JOURNAL OF THE MECHANICAL BEHAVIOR OF BIOMEDICAL MATERIALS I (2008) 59-67

Table 1 – Model parameters of the mesoscale model (1 kcal/mol/Å = 69.479 pN)

|  Equilibrium bead distance r₀ (in Å) | 14.00  |
| --- | --- |
|  Critical hyperelastic strain r₁ (in Å) | 18.20  |
|  Bond breaking distance r_break (in Å) | 21.00  |
|  Tensile stiffness parameter k_T(0) (in kcal/mol/Å²) | 17.13  |
|  Tensile stiffness parameter k_T(1) (in kcal/mol/Å²) | 97.66  |
|  Cross-link tensile stiffness parameter k_XL (in kcal/mol/Å²) | 17.00  |
|  Cross-link equilibrium distance r_XL (in Å) | 18.00  |
|  Cross-link bond breaking distance r_break_XL (in Å) | 19.80  |
|  Equilibrium angle ψ₀ (in degrees) | 180.00  |
|  Bending stiffness parameter k_B (in kcal/mol/rad²) | 14.98  |
|  Dispersive parameter ε (in kcal/mol) | 10.6  |
|  Dispersive parameter σ (in Å) | 14.72  |
|  Mass of each mesoscale particle (in amu) | 1358.7  |

the entire tropocollagen molecule as a collection of ‘beads’ or ‘super-atoms’. The reason for this simplification is that a full atomistic resolution with all atoms, water molecules and side chains at time scales of microseconds and length scales of several hundred nanometers cannot be addressed using any computational model and computational equipment currently available. The mesoscale model enables one to carry out simulations at the required time and length scales and provides a compromise between accuracy and feasibility. The model includes the effects of a pure water phase. In principle, the model could be extended to include other interstitial fluids, solvents or specific concentrations of water. This would involve carrying out full atomistic simulations of these cases along with repeated training of the mesoscale model parameters.

The total energy is given by

$$
E = E _ {\mathrm {T}} + E _ {\mathrm {B}} + E _ {\text {inter}}. \tag {1}
$$

where $E_{\mathrm{T}}$ describes the energy contributions due to stretching, $E_{\mathrm{B}}$ energy contributions due to bending, and $E_{\mathrm{inter}}$ intermolecular interactions. The parameters of the mesoscopic model are summarized in Table 1.

The bending energy contributions of triplets of particles are defined by

$$
\phi_ {\mathrm {B}} (\psi) = \frac {1}{2} k _ {\mathrm {B}} \left(\psi - \psi_ {0}\right) ^ {2}. \tag {2}
$$

with $k_{\mathrm{B}}$ relating to the bending stiffness of the molecule (Buehler, 2006a,b, 2007). The nonlinear stress-strain behavior of a single molecule under tensile loading is modeled with a bilinear model (Buehler and Gao, 2006; Buehler et al., 2003). The force between two particles is

$$
F _ {\mathrm {T}} (r) = - \frac {\partial \phi_ {\mathrm {T}} (r)}{\partial r}, \tag {3}
$$

where

$$
\frac {\partial \phi_ {\mathrm {T}} (r)}{\partial r} (r) = H \left(r _ {\text {break}} - r\right) \left\{ \begin{array}{l l} k _ {\mathrm {T}} ^ {(0)} \left(r - r _ {0}\right) &amp; \text {if } r &lt; r _ {1}, \\ k _ {\mathrm {T}} ^ {(1)} \left(r - \bar {r} _ {1}\right) &amp; \text {if } r \geqslant r _ {1}. \end{array} \right. \tag {4}
$$

In Eq. (4), $H(r - r_{\mathrm{break}})$ is the Heaviside function $H(a)$, which is defined to be zero for $a &lt; 0$, and one for $a \geqslant 0$, and $k_T^{(0)}$ as well as $k_T^{(1)}$ for the small- and large-deformation spring constants. The parameter $\bar{r}_1 = r_1 - k_T^{(0)} / k_T^{(1)}(r_1 - r_0)$ is

Fig. 2 – Schematic showing how the presence of cross-links is modeled by increased adhesion at the ends of each molecule, in segments of $60\,\mathrm{\AA}$ to the left and right of each tropocollagen molecule. Implementing a variation of the amplification of the adhesion strength constitutes a simplistic model for varying cross-link densities. A parameter $\beta$ is introduced that describes the increase of adhesion at the ends of each TC molecule, so that $\tau_{\mathrm{XL}} = \beta \cdot \tau$ ($\tau$ is the adhesion force/length between two TC molecules). The parameter $\beta = 15$ corresponds to the case when approximately one cross-link is present at each end of a tropocollagen molecule.
![img-1.jpeg](img-1.jpeg)
Regular adhesion
Increased adhesion

determined from force continuity conditions. The function $E_{\mathrm{T}}$ is given by integrating $F_{\mathrm{T}}(r)$ over the radial distance.

Intermolecular interactions are modeled by a Lennard-Jones (LJ) potential

$$
\phi_ {\text {inter}} (r) = 4 \varepsilon_ {\mathrm {LJ}} \left(\left[ \frac {\sigma_ {\mathrm {LJ}}}{r} \right] ^ {12} - \left[ \frac {\sigma_ {\mathrm {LJ}}}{r} \right] ^ {6}\right). \tag {5}
$$

with $\sigma_{\mathrm{LJ}}$ as the distance and $\varepsilon_{\mathrm{LJ}}$ as the energy parameter (these parameters do not relate to stress or strain). The parameter $\varepsilon_{\mathrm{LJ}}$ directly determines the strength of the intermolecular adhesion, since $\tau \sim \varepsilon_{\mathrm{LJ}}$, where $\tau$ is the adhesion force per unit length of a tropocollagen molecule (Buehler, 2006a,b). The parameter $\tau \approx 5.55\,\mathrm{pN}/\mathrm{\AA}$ for interaction between two fully hydrated molecules at pH 7 without any cross-links present, as described earlier (Buehler, 2006a).

The presence of intermolecular cross-links effectively leads to an increased intermolecular adhesion in the region where cross-links are formed. To model the effect of cross-links, the adhesion parameter $\varepsilon_{\mathrm{LJ}}$ is modified to account for the stronger interaction between molecules. Variation of the parameter $\varepsilon_{\mathrm{LJ}}$ along the molecular axis enables one to account for specific spatial distributions of cross-links. Experimental analyses of the molecular geometry suggests that intermolecular aldol cross-links between lysine or hydroxylysine residues (Lodish et al., 1999; Bailey, 2001; Robins and Bailey, 1973) primarily develop at the ends of tropocollagen molecules (Lodish et al., 1999; Alberts et al., 2002). The aldol cross-link is a C–C bond that forms between side chains of the residues of two tropocollagen molecules.

Fig. 2 depicts a schematic that shows how the presence of cross-links is modeled by increased adhesion at the ends of each molecule, in segments of $60\,\mathrm{\AA}$ to the left and right end of each tropocollagen molecule.

According to this idea, the LJ potential parameter $\varepsilon_{\mathrm{LJ}}$ is increased by a factor $\beta \geqslant 1$ compared with the rest of

---

the molecule in regions where cross-links are formed, and therefore

ε *L**J*, *X**L* = *β* ⋅ *ε*_{*L**J*}.

For a choice β = 12.5, the additional shear force exerted at the end of the molecule corresponds to ≈4.2 nN, which is on the order of the bond strength of covalent cross-link bonds (Lantz et al. 2001; Grandbois et al. 1999). The parameter β = 12.5 therefore corresponds to the case when approximately one cross-link is present at each end of a tropocollagen molecule, leading to a cross-link density of 2.2 × 10^{24}/m^{3} (the cross-link density is defined as the number of cross-links per unit volume). Similarly, doubling the value β = 25 corresponds to two covalent cross-links.

The total potential energy of the system is given by the sum over all pairwise and three-body interactions m (I = {T. inter}):

E *I* = ∑ pairs φ *I*(*r*) and E *B* = ∑ angles φ *B*(*ψ*).

All parameters used in the molecular model are determined from full atomistic simulations, as described in more detail in earlier publications on this topic (Buehler, 2006a,b).

### 2.2. Model geometry, modeling procedure and application of mechanical load

A two-dimensional plane stress model of collagen fibrils with periodic boundary conditions in the in-plane direction orthogonal to the pulling orientation is considered here, with an array of 2 × 5 tropocollagen molecules (total number of TC molecules is 10). The collagen fibrils show the characteristic staggered arrangement as observed in experiment. The entire system contains 2000 particles (each tropocollagen molecule is represented by 200 particles). Each particle has two degrees of freedom as it is free to move in the x- and y-direction of the simulation domain.

The plane stress condition is used to mimic the fact that the system is not periodic in the out of plane direction. Fully three-dimensional models are computationally very expensive. However, the model could treat such cases as well since there is no intrinsic limitation to a two-dimensional case.

No additional constraints other than the molecular interactions are applied to the system.

Simulations are carried out in two steps, (i) relaxation, followed by (ii) loading. Relaxation is achieved by slowly heating up the system, then annealing the structure at constant temperature, followed by energy minimization. Finite temperature calculations enable the structure to reassemble more easily, whereas energy minimization ensures finding the energetically optimal configuration of the molecules. If the initial relaxation is not carried out, pulling may be applied to a structure that is not in equilibrium and yield may be observed that is actually not due to the applied load but due to rearrangements towards the equilibrium structure. After relaxation, the structure displays the characteristics of collagen fibrils in agreement with experiment (Bozec and Horton, 2005; Bhattacharjee and Bansal, 2005; Anderson, 2005; Sun et al. 2004; An et al. 2004; Lees, 2003; Sun et al. 2002; Hellmich and Ulm, 2002; Jager and Fratzl, 2000; Waite et al. 1998; Borel and Monboisse, 1993; Lees, 1987; Fratzl et al. 2004; Hulmes et al. 1995; Puxkandl et al. 2002).

The integration time step is Δt = 55 fs. To model tensile deformation of collagen fibrils, displacement boundary conditions are implemented by continuously displacing a set of particles in the boundary regions (in a region 40 Å to the left and right of the end of the collagen fibril).

The simulations are carried out by constantly minimizing the potential energy as the external strain is applied, where a displacement rate of 0.4 m/s is used for all simulations reported in this paper. Such rather high strain rates are a consequence of the timescale limitation of the molecular model; total times spans of several microseconds are the most that can be simulated since the time step has to be on the order of several femtoseconds. Overcoming these limitations is a major challenge in the field of molecular modeling. Models such as the Extended Bell Theory (Ackbarow and Buehler, in press, 2007) constitute useful methods to address this problem rigorously.

The virial stress is used to calculate the stress tensor (Tsai, 1979) for analyses of the stress--strain behavior. The strain is defined as ε = (x - x_{0})/x_{0}, where x_{0} is the initial, undeformed length of the collagen fibril, and x is the current, deformed length. It is noted that the extension ratio or stretch λ is related to the strain via λ = 1 + ε.

### 2.3. Definition of terms and nomenclature

The yield stress σ_{Y} is defined as the stress at which permanent deformation of the collagen fibril begins. This is characterized either by intermolecular shear or by molecular fracture, leading to permanent deformation. The yield strain ε_{Y} is defined as the critical strain at which these mechanisms begin.

The fracture stress σ_{F} is defined as the largest stress in the stress--strain curve, corresponding to the maximum load the collagen fibril can sustain. The fracture strain ε_{F} is the corresponding strain at which the largest stress occurs.

## 3. Computational results: Molecular modeling

### 3.1. Tensile deformation: Stress--strain curves

Fig. 3 depicts the stress--strain curve for various cross-link densities, expressed in terms of the parameter β. For small values of cross-link densities (β < 10), the fibril starts to yield at strain in the range of 5%--10%, and shows rather long dissipative deformation paths, leading to fracture at strains between 50% and 100%.

It is found that larger cross-link densities lead to larger yield strains, larger yield stresses as well as larger fracture stresses. At a critical cross-link density corresponding to one cross-link per molecule (β ≈ 15) the second, steeper elastic regime is activated. This strong increase in tangent modulus corresponds to stretching of the protein backbone. This molecular deformation mode dominates after the uncoiling of the tropocollagen molecule under breaking of H-bonds

---

JOURNAL OF THE MECHANICAL BEHAVIOR OF BIOMEDICAL MATERIALS I (2008) 59-67

![img-2.jpeg](img-2.jpeg)
Fig. 3 – Stress versus strain of a collagen fibril, for different cross-link densities. The results clearly show that larger cross-link densities lead to larger yield strains, larger yield stresses as well as larger fracture stresses. For larger cross-link densities, the second elastic regime (seen as much steeper, second slope) is activated. As the cross-link density increases, the collagen fibril shows a more ‘brittle-like’ deformation behavior. For values of $\beta &gt; 25$, the deformation mechanisms is characterized by molecular fracture, and as a consequence, the maximum fracture stress of the collagen fibril does not increase with increasing cross-link densities. This cross-link density corresponds to the case when two cross-links per molecule are present.

(Buehler, 2006a). The results clearly confirm the significance of the presence and density of cross-links on the deformation behavior.

Large elastic tensile strains of up to $50\%$ are possible since each TC molecule itself can sustain strains of up to $50\%$ tensile deformation (this is shown in Fig. 4, curve for a single TC molecule). In the collagen fibril, such large strains at the molecular scale are only possible if strong links exist which prevent molecular slip and therefore enable transfer of large loads to the individual TC molecules. As shown in the present work, developing cross-links between molecules is a possible means of achieving this situation.

## 3.2. Comparison: Single tropocollagen molecule and collagen fibril

Fig. 4 shows a comparison between the stress-strain curves of a collagen fibril ($\beta = 25$) and a single TC molecule, for tensile strains below $40\%$. Both structures are completely in the elastic regime (the tropocollagen molecule fractures at approximately $50\%$ tensile strain and the collagen fibril starts to yield at slightly above $40\%$ strain). The results depicted in Fig. 4 show that the stresses in the single TC molecule are larger than in the collagen fibril.

Fig. 5(a) plots the tangent modulus of the stress-strain curve depicted in Fig. 4. The results clearly indicate that the tangent modulus of the single tropocollagen molecule is larger than that of a collagen fibril. Fig. 5(b) plots the ratio of the moduli as a function of applied strain, suggesting that the

![img-3.jpeg](img-3.jpeg)
Fig. 4 – Stress versus strain, comparing a collagen fibril ($\beta = 25$) with a single TC molecule. Both structures are completely in the elastic regime (the TC molecule fractures at approximately $50\%$ tensile strain and the collagen fibril starts to yield at slightly above $40\%$ strain). This plot shows that the stresses in the single TC molecule are larger than in the collagen fibril, and that the tangent modulus is larger throughout deformation. This agrees well with experimental results (Sasaki and Odajima (1996)).

![img-4.jpeg](img-4.jpeg)

![img-5.jpeg](img-5.jpeg)
Fig. 5 – Subplot (a): Tangent modulus versus strain, comparing a single TC molecule and a collagen fibril (cross-link parameter $\beta = 25$). Subplot (b): Ratio of tangent modulus of a single TC molecule by a collagen fibril, as a function of strain (the collagen fibril considered has a cross-link parameter $\beta = 25$). The results clearly show that the tangent modulus of the single TC molecule is approximately $40\%$ larger, except for the transition region during which the modulus of the fibril is larger (between $20\%$ and $30\%$ fibril strain).

---

JOURNAL OF THE MECHANICAL BEHAVIOR OF BIOMEDICAL MATERIALS I (2008) 59-67

![img-6.jpeg](img-6.jpeg)
Fig. 6 – Yield stress and fracture stress of a collagen fibril as a function of the cross-link density, expressed by the adhesion parameter $\beta$. For large cross-link densities, the material behavior becomes increasingly brittle and the failure strength (or yield strength, equivalently) does not depend on the cross-link density any more (saturation of yield stress) since failure is controlled by fracture of individual TC molecules.

modulus of a single tropocollagen molecule is approximately $40\%$ larger throughout deformation. This agrees well with experimental results, suggesting an increase of the stiffness from fibril to molecule close to $40\%$ (Sasaki and Odajima, 1996).

Even though cross-links are stiffer than the TC molecule itself, the overall density of cross-links is rather small so that the stiffening effect is negligible. The origin of the softening is the combination of rather weak intermolecular interactions with the single molecule elasticity along most of the axial length of the TC molecules. This leads to an effective softening of the fibrillar structure even when cross-links are present. This may change for extremely large cross-link densities, for example when cross-links form along the entire axial dimension of the chain.

## 3.3. Yield stress and fracture stress analysis

Fig. 6 depicts the yield stress of a collagen fibril as a function of the cross-link density. The plot shows that for larger cross-link densities, the material becomes stronger. However, when $\beta &gt; 25$, the yield stress and fracture stress do not depend on the cross-link density any more as the yield stress reaches a plateau value. The plateau can be explained by a change in molecular deformation mechanism from predominantly intermolecular shear (for $\beta &lt; 25$) to molecular fracture (for $\beta &gt; 25$). Whereas the strength of the fibril is controlled by intermolecular adhesion for $\beta &lt; 25$, the strength is dominated by the molecular fracture properties. This observation confirms a change in mechanisms as suggested in an earlier study (Buehler, 2006b).

As the cross-link density increases, the collagen fibril becomes more 'brittle-like'. The increasingly brittle character is clearly illustrated by the ratio of fracture stress versus yield stress, as shown in Fig. 7. For smaller values of $\beta &lt; 15$, the stress-strain curves show a stiffening effect after onset of yield, similar to work-hardening as known in metal plasticity (see also Fig. 3). However, this stress increase decreases

![img-7.jpeg](img-7.jpeg)
Fig. 7 – Ratio of fracture stress versus yield stress as a function of the cross-link density, expressed by the adhesion parameter $\beta$. For smaller values of $\beta$, the stress-strain curves show a stiffening effect after onset of yield, similar to work-hardening as known in metal plasticity. However, this stress increase decreases with increasing cross-link density. The data shows that when $\beta &gt; 15$, the material becomes 'brittle-like', characterized by immediate drop of the stress after onset of yield without dissipative deformation.

with increasing cross-link density. The data shows that as the cross-link parameter exceeds 15, the material becomes 'brittle-like', characterized by immediate drop of the stress after onset of yield without dissipative deformation.

An analysis of the stress-strain behavior provides further insight into the elastic and plastic deformation modes. Fig. 8(a) depicts the yield strain $\varepsilon_{\mathrm{Y}}$, fracture strain $\varepsilon_{\mathrm{F}}$ and amount of dissipative strain (the difference $\varepsilon_{\mathrm{F}} - \varepsilon_{\mathrm{Y}}$), as a function of cross-link parameter. Fig. 8(b) shows the ratio of the amount dissipative strain over yield strain, defined as $(\varepsilon_{\mathrm{F}} - \varepsilon_{\mathrm{Y}}) / \varepsilon_{\mathrm{Y}}$, for varying cross-link densities. Both graphs corroborate the notion that for increasing cross-link densities, the material becomes increasingly 'brittle-like'.

## 3.4. Comparison with experimental results

This section is dedicated to a brief discussion of our computational results in light of recent experimental reports of stretching experiments of tropocollagen molecules and individual collagen fibrils.

Table 2 provides an overview of moduli obtained for single tropocollagen molecules. The comparison shows that our predictions for the moduli are close to experimental results, albeit fall into the higher end of the range of values reported.

Table 3 summarizes results for elastic moduli of collagen fibrils from various sources. Unlike as for the single molecule case the agreement between experiment and simulation is not as good. A few important observations are discussed in more detail. Recently, MEMS devices were used to carry out tensile studies of single collagen fibrils (Eppell et al., 2006). The authors obtained a small-deformation modulus of approximately $0.4\mathrm{GPa}$, and a large-deformation modulus of $12\mathrm{GPa}$. The absolute values of the small-strain moduli are approximately 10 times smaller than in our simulation results.

---

JOURNAL OF THE MECHANICAL BEHAVIOR OF BIOMEDICAL MATERIALS I (2008) 59-67

![img-8.jpeg](img-8.jpeg)

![img-9.jpeg](img-9.jpeg)
Fig. 8 - Subplot (a): Yield strain  $\varepsilon_{\mathrm{Y}}$ , fracture strain  $\varepsilon_{\mathrm{F}}$  and amount of dissipative strain (the difference  $\varepsilon_{\mathrm{F}} - \varepsilon_{\mathrm{Y}}$ ), as a function of cross-link parameter. Subplot (b): Ratio of width of dissipative strain over yield strain,  $(\varepsilon_{\mathrm{F}} - \varepsilon_{\mathrm{Y}}) / \varepsilon_{\mathrm{Y}}$ , for varying cross-link densities. Both graphs clearly show that for increasing cross-link densities, the material becomes increasingly 'brittle-like'.

One possible explanation for this disagreement could be entropic effects that may make the fibril softer in particular in the small-deformation regime. Such entropic effects are not considered in the present study, since all molecules are completely stretched out to their contour length at the

beginning of the simulation and thus enter the energetic stretching regime instantaneously.

Another possible reason may be the large deformation rates used in atomistic modeling (Buehler, 2006a), which often lead to overestimation of forces during mechanical deformation. Considering smaller deformation rates, for instance, may lead to smaller values for Young's modulus, as typically unfolding forces are larger for larger deformation rates (e.g. based on concepts related to Bell theory (Ackbarow and Buehler, in press, 2007)). Since the molecular model used in this study is based solely on atomistic input data, overestimation of the modulus value from the MD simulations will be transported throughout the multi-scale modeling scheme. This may explain why the values reported in the present work are close to the upper end of the range of experimental measurements.

However, the ratio of large-strain modulus to small-strain modulus is on the same order of magnitude, being  $\approx 24 - 30$  in experiment and  $\approx 8.4$  in simulation. The transition from small- to large-deformation modulus occurs at strains of approximately  $30\%$ , which is found in both experiment and simulation.

It has been suggested in Eppell et al. (2006) that the tensile strength may be greater than 1 GPa, which is corroborated by our results that suggest strengths ranging from 300 MPa (cross-link deficient fibrils) to 6 GPa (highly cross-linked collagen fibrils). These values agree with the strengths predicted in our simulation (see Fig. 6, for example). On the other hand, other results (Sasaki and Odajima, 1996; Borsato and Sasaki, 1997) show much lower failure stresses on the order of several MPa. Possible explanations for this discrepancy could be molecular defects, high loading rates or different geometries in those experiments (Sasaki and Odajima, 1996; Borsato and Sasaki, 1997) that do not resemble the perfect patterns as considered in our study.

# 4. Discussion

Large-scale molecular modeling has been employed to predict the small- and large-deformation mechanics of collagen fibrils, as a function of varying cross-link densities. The results suggest that the cross-link density governs the large deformation and in particular the yield or fracture mechanics.

Table 2 - Comparison of Young's modulus of single tropocollagen molecules, experiment and computation

|  Study, case and approach | Young's modulus (GPa)  |
| --- | --- |
|  Single molecule stretching (Lorenzo and Caffarena, 2005) | 4.8 ± 1  |
|  Atomistic modeling |   |
|  Single molecule stretching (Buehler, 2006a) | ≈7  |
|  Reactive atomistic modeling |   |
|  Single molecule stretching (Vesentini et al., 2005) | 2.4  |
|  Atomistic modeling |   |
|  X-ray diffraction (Sasaki and Odajima, 1996) | ≈3  |
|  Brillouin light scattering (Harley et al., 1977) | 9  |
|  Brillouin light scattering (Cusack and Miller, 1979) | 5.1  |
|  Estimate based on persistence length (Hofmann et al., 1984) | 3  |
|  Estimate based on persistence length (Sun et al. (2004); Vesentini et al., 2005) | 0.35–12  |

---

However, it influences the small-deformation mechanics only marginally (see, e.g. Fig. 3).

The model predicts that collagen fibrils are capable of undergoing extremely large deformation without fracturing; how much of this is elastic or dissipative depends on the cross-link densities. It is found that two prominent molecular mechanisms of permanent deformation dominate: molecular glide and molecular rupture.

Formation of covalent cross-links are essential to reach the elastically stiffer, second regime in the stress--strain curve of collagen, which corresponds to backbone stretching in the tropocollagen molecule. This phenomenon can be understood based on the mechanisms and the effect of the presence of cross-links: The increased traction at the end of the molecule allows for larger molecular strains to be reached. The larger strains give rise to larger overall yield and fracture stress. However, collagen fibrils become more ‘brittle-like' under these conditions as their ability to undergo dissipative, plastic deformation is reduced. These findings confirm some of the key hypotheses put forward in Buehler (2006b), including effect of cross-links in making the material appear more ‘brittle', observed deformation mechanics and reduction of elastic modulus. This is confirmed by several analyses shown in Figs. 7 and 8, for instance.

The results improve the understanding of how molecular changes during ageing contribute to modifications of tissue properties. Ageing of organisms is primarily controlled by changes in the protein structure of elastin and collagen, when increased cross-linking between molecules develops due to non-enzymatic processes. These changes in the molecular architecture may lead to diseases that are induced by the modification of the mechanical properties of tissues (Bailey and Sethna, 2003). The analysis confirms that cross-linking indeed leads to stiffening and increasing ‘brittleness' of collagen based tissues. It is noted that the results shown in Fig. 3 are in good qualitative agreement with the results of stress--strain responses of collagen during ageing (see Fig. 3 in Reference Bailey and Sethna (2003)). Both the present model and experiment predict a stronger and less dissipative behavior with the development of additional cross-links.

It is found that the material properties of collagen are scale dependent. A softening of the modulus is observed when tropocollagen molecules are assembled into a collagen fibril. The modeling suggests a reduction of modulus on the order of 40%, which is close to experimental results (Sasaki and Odajima, 1996; Borsato and Sasaki, 1997) of similar comparisons between the mechanics of collagen fibrils and tropocollagen molecules (see Fig. 5). This can also be found by taking a simple average value of all values for tropocollagen molecules reported in the literature (5.1 GPa, average of Table 2) divided by the average value of moduli for the collagen fibril (2.8 GPa, average of Table 3), which suggests an increase of modulus by approximately 80%.

The results show several features of the stress--strain behavior also found in experiment (Hulmes et al. 1995; Puxkandl et al. 2002; Eppell et al. 2006), notably the two regimes of moduli with a strong progressive stiffening with increasing strains. However, the magnitude of the stress is different, as MD modeling predicts larger stresses and larger moduli than seen in experiment.

A limitation of the present study is that spatial inhomogeneities of cross-link distributions are not considered. In principle, this can be implemented straightforwardly. Also, changes of molecular properties along the molecular length have not been considered, an important characteristic feature of many collagen based tissues. This aspect is particularly significant to account for entropic effects that stem from more floppy labile regions of the tropocollagen molecules (Miles and Bailey, 2001). These important aspects will be addressed in future work.

An improved understanding of the nanomechanics of collagen may help in the development of biomimetic materials, or for improved scaffolding materials for tissue engineering applications (Kim et al. 1999; Yung and Mooney, in press). Diseases such as Ehlers--Danlos (Lichtenstein et al. 1973), Osteogenesis imperfecta, scurvy or the Caffey disease (Glorieux, 2005) are caused by defects in the molecular structure of collagen altering the intermolecular and molecular properties due to genetic mutations, modifying the mechanical behavior of collagen fibrils.

## Conclusion

Deformation and fracture are fundamental phenomena with major implications on the stability and reliability of machines, buildings and biological systems. All deformation processes begin with erratic motion of individual atoms around flaws or defects that quickly evolve into formation of macroscopic fractures as chemical bonds rupture rapidly, eventually compromising the integrity of the entire structure. However, most existing theories of fracture treat matter as a continuum, neglecting the existence of atoms or nanoscopic features. Clearly, such a description is questionable. An atomistic approach as discussed in this paper provides unparalleled insight into the complex atomic-scale deformation processes, linking nano to macro, without relying on empirical input.

The study reported here illustrates that molecular multi-scale modeling of collagen can be used to predict the elastic

---

JOURNAL OF THE MECHANICAL BEHAVIOR OF BIOMEDICAL MATERIALS 1 (2008) 59-67

and fracture properties of hierarchical protein materials, marvelous examples of structural designs that balance a multitude of tasks, representing some of the most sustainable material solutions that integrate structure and function across the scales.

Breaking the material into its building blocks enables one to perform systematic studies of how microscopic design features influence the mechanical behavior at larger scales. The studies elucidate intriguing material concepts that balance strength, energy dissipation and robustness by selecting nanopatterned, hierarchical features.

## Acknowledgements

MJB is grateful for helpful discussions with Yu Ching Yung (Harvard University). This research was partly supported by the Army Research Office (ARO), grant number W911NF-06-1-0291, program officer Dr. Bruce LaMattina.

## REFERENCES

Anderson, D., 2005. vol. Ph.D. University of Toronto, Toronto, Canada.
An, K.N., Sun, Y.L., Luo, Z.P., 2004. Biorheology 41, 239-246.
Alberts, B., Johnson, A., Lewis, J., Raff, M., Roberts, K., Walter, P., 2002. Molecular Biology of the Cell. Taylor &amp; Francis.
Ackbarow, T., Buehler, M.J., 2007. In: Devanathan, R., Caturla, M.J., Kubota, A., Chartier, A., Phillipot, S. (Eds.), Multiscale Modeling of Materials (Mater. Res. Soc. Symp. Proc. 978E, Warrendale, PA, 2007) paper # 0978-GG10-05.
Ackbarow, T., Buehler, M.J. Journal of Materials Science (in press).
Bozec, L., Horton, M., 2005. Biophysical Journal 88, 4223-4231.
Bhattacharjee, A., Bansal, M., 2005. IUBMB Life 57, 161-172.
Borel, J.P., Monboisse, J.C., 1993. Comptes Rendus Des Seances De La Societe De Biologie Et De Ses Filiales 187, 124-142.
Bozec, L., de Groot, J., Odlyha, M., Nicholls, B., Nesbitt, S., Flanagan, A., Horton, M., 2005. Ultramicroscopy 105, 79-89.
Buehler, M.J., 2006a. Journal of Materials Research 21, 1947-1961.
Buehler, M.J., 2006b. Proceedings of the National Academy of Sciences of United States of America 103, 12285-12290.
Buehler, M.J., Nanotechnology (in press).
Buehler, M.J., 2007. Biophysical Journal 93 (1), doi:10.1529/biophysj.106.102616.
Buehler, M.J., Gao, H., 2006. Nature 439, 307-310.
Buehler, M.J., Abraham, F.F., Gao, H., 2003. Nature 426, 141-146.
Bailey, A.J., 2001. Mechanisms of Ageing And Development 122, 735-755.
Borsato, K.S., Sasaki, N., 1997. Journal of Biomechanics 30, 955-957.
Bailey, N.P., Sethna, J.P., 2003. Physical Review B 68.
Cusack, S., Miller, A., 1979. Journal of Molecular Biology 135, 39-51.
Eppell, S.J., Smith, B.N., Kahn, H., Ballarini, R., 2006. Journal of the Royal Society Interface 3, 117-121.
Fratzl, P., Gupta, H.S., Paschalis, E.P., Roschger, P., 2004. Journal of Materials Chemistry 14, 2115-2123.

Gupta, H.S., Messmer, P., Roschger, P., Bernstorff, S., Klaushofer, K., Fratzl, P., 2004. Physical Review Letters 93.
Gupta, H.S., Wagermaier, W., Zickler, G.A., Aroush, D.R.B., Funari, S.S., Roschger, P., Wagner, H.D., Fratzl, P., 2005. Nano Letters 5, 2108-2111.
Grandbois, M., Beyer, M., Rief, M., Clausen-Schaumann, H., Gaub, H.E., 1999. Science 283, 1727-1730.
Glorieux, F.H., 2005. Journal of Clinical Investigation 115, 1142-1144.
Harley, R., James, D., Miller, A., White, J.W., 1977. Nature 267, 285-287.
Hellmich, C., Ulm, F.J., 2002. Journal of Biomechanics 35, 1199-1212.
Hofmann, H., Voss, T., Kuhn, K., Engel, J., 1984. Journal of Molecular Biology 172, 325-343.
Hulmes, D.J.S., Wess, T.J., Prockop, D.J., Fratzl, P., 1995. Biophysical Journal 68, 1661-1670.
Jager, I., Fratzl, P., 2000. Biophysical Journal 79, 1737-1746.
Kim, B.S., Nikolovski, J., Bonadio, J., Mooney, D.J., 1999. Nature Biotechnology 17, 979-983.
Lees, S., 2003. Biophysical Journal 85, 204-207.
Lees, S., 1987. International Journal of Biological Macromolecules 9, 321-326.
Lorenzo, A.C., Caffarena, E.R., 2005. Journal of Biomechanics 38, 1527-1533.
Lodish, H., Berk, A., Zipursky, S.L., Matsudaira, P., Baltimore, D., Darnell, J.E., 1999. Molecular Cell Biology. W H Freeman &amp; Co, New York.
Lantz, M.A., Hug, H.J., Hoffmann, R., van Schendel, P.J.A., Kappenberger, P., Martin, S., Baratoff, A., Guntherodt, H.J., 2001. Science 291, 2580-2583.
Lichtenstein, J.R., Martin, G.R., Kohn, L.D., Byers, P.H., McKusick, V.A., 1973. Science 182, 298-300.
Miles, C.A., Bailey, A.J., 2001. Micron 32, 325-332.
Nalla, R.K., Kruzic, J.J., Kinney, J.H., Ritchie, R.O., 2005. Biomaterials 26, 217-231.
Orgel, J.P.R.O., Irving, T.C., Miller, A., Wess, T.J., 1995. Proceedings of the National Academy of Sciences of United States of America 103, 9001-9005.
Puxkandl, R., Zizak, I., Paris, O., Keckes, J., Tesch, W., Bernstorff, S., Purslow, P., Fratzl, P., 2002. Philosophical Transactions of the Royal Society of London Series B-Biological Sciences 357, 191-197.
Ritchie, R.O., Kruzic, J.J., Muhlstein, C.L., Nalla, R.K., Stach, E.A., 2004. International Journal of Fracture 128, 1-15.
Robins, S.P., Bailey, A.J., 1973. Biochemical Journal 135, 657-665.
Sun, Y.L., Luo, Z.P., Fertala, A., An, K.N., 2002. Biochemical and Biophysical Research Communications 295, 382-386.
Sasaki, N., Odajima, S., 1996. Journal of Biomechanics 29, 1131-1136.
Sun, Y.L., Luo, Z.P., Fertala, A., An, K.N., 2004. Journal of Biomechanics 37, 1665-1669.
Tsai, D.H., 1979. Journal of Chemical Physics 70, 1375-1382.
van der Rijt, J.A.J., van der Werf, K.O., Bennink, M.L., Dijkstra, P.J., Feijen, J., 2006. Macromolecular Bioscience 6, 697-702.
Vesentini, S., Fitie, C.F.C., Montevecchi, F.M., Redaelli, A., 2005. Biomechanics And Modeling In Mechanobiology 3, 224-234.
Waite, J.H., Qin, X.X., Coyne, K.J., 1998. Matrix Biology 17, 93-106.
Yung, Y.C., Mooney, D.J. In: Fisher, J.P. (Ed.), CRC Biomedical Engineering Handbook. CRC Press, Boca Raton, FL (in press).
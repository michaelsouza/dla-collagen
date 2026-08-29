# Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

Markus J. Buehler[^1] [Address all correspondence to this author. e-mail: mbuehler@MIT.EDU
DOI: 10.1557/JMR.2006.0236 Department of Civil and Environmental Engineering, Massachusetts Institute of Technology, Cambridge, Massachusetts 02139]

###### Abstract

We report studies of the mechanical properties of tropocollagen molecules under different types of mechanical loading including tension, compression, shear, and bending. Our modeling yields predictions of the fracture strength of single tropocollagen molecules and polypeptides, and also allows for quantification of the interactions between tropocollagen molecules. Atomistic modeling predicts a persistence length of tropocollagen molecules $\xi$ $\approx$ 23.4 nm, close to experimental measurements. Our studies suggest that to describe large-strain or hyperelastic properties, it is critical to include a correct description of the bond behavior and breaking processes at large bond stretch, information that stems from the quantum chemical details of bonding. We use full atomistic calculations to derive parameters for a mesoscopic bead-spring model of tropocollagen molecules. We demonstrate that the mesoscopic model enables one to study the finite temperature, long-time scale behavior of tropocollagen fibers, illustrating the dynamics of solvated tropocollagen molecules for different molecular lengths.

## I. INTRODUCTION

Biological materials may be essential for facing critical challenges related to increased energy needs, needs for new medical applications, novel concepts in sensor and actuator design, reliability and robustness of devices, conservation of resources, and development of new structural materials. The combination of (i) high-level structural control of matter as achieved in nanoscience and nanotechnology, and (ii) integration of living and nonliving systems into technologies and their interfaces may play a critical role in the coming decades. With increasing complexity, materials start to resemble systems or machines, so that the borderlines between concepts such as “machine” and “material” start to disappear. These concepts have been used systematically by nature for millions of years, and their exploitation for technological applications holds great promise. In particular, the structure and behavior of proteins and materials based on proteins plays an overarching role in determining the function and properties of biological systems.

In recent years, proteins have indeed been proposed as the basis for new materials for technological applications.1^{--}6 Materials based on proteins hold particular promise because of their great flexibility in usage and their applications. Genetically engineered biopolymers based on recombinant DNA technologies have been developed by Tirrell and coworkers1^{--}5 for various applications, including pH sensitive hydrogels.2 This is an example for the vanishing borderline between technology and biology, enabling new critical breakthroughs for novel material concepts, allowing translation of nature’s structural concepts into engineered materials.1^{--}6

Together with such new experimental techniques for synthesis and characterization,1^{--}6 a sound theoretical understanding and the availability of accurate models are essential for developing engineering applications of such complex materials. The properties of biological materials are determined from complex interaction of individual scale-specific properties and their interactions. To date it remains unclear how different properties interact, and which are most important, but it is believed that the hierarchical design plays a vital role. In particular, many biological materials are poorly understood in terms of their mechanical behavior, and fundamental fracture and deformation theories are missing, in particular those including the effects of the hierarchical design. Our goal is to develop such theoretical understanding of the cross-scale relationships between small scales (e.g. primary structure) and macroscopic scales (e.g. quaternary structure). We hypothesize that such cross-scale interactions can play a significant role in determining the mechanical behavior of materials and that nature or biology utilizes

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

such principles systematically. However, these concepts are not yet understood within the context of scientific or engineering principles, and thus, exploitation for engineering remains elusive.

We propose a bottom-up approach in understanding biological materials, focusing on the finest atomistic scales of detail governed by quantum mechanics (QM) as the starting point, reaching up to large, macroscopic scales, using hierarchical multi-scale modeling. This could be viewed as an alternative, supplemental method with respect to many experimental efforts starting at the macroscopic level reaching down to ever finer scales. We believe that theoretical modeling as presented in this paper may eventually help to advance technology to make systematic use of biological polymers such as collagen, even beyond medical applications. We believe that atomistic based modeling, in conjunction with mesoscopic and continuum approaches, may be an extremely fruitful approach in understanding the interactions of materials across the scales. These techniques include differential multi-scale simulation methods that allow description of material behavior across hierarchies of scales, ranging from the atomistic scale to the continuum engineering scale, while including modeling of the chemistry during formation and breaking of bonds by using reactive force fields.

In this article, we focus on the mechanical properties of tropocollagen molecules and assemblies of those into fibril-like structures. We chose collagen since it is one of the most abundant protein-based structural materials, for which the atomic structure is relatively well-known,[7-9] in contrast to other protein-based biological materials such as elastin.[10,11] The aim of this paper is to develop a systematic understanding of the macroscopic mechanical response of tropocollagen fibers and its bundles based on their fundamental, atomistic ultrastructure using atomistic modeling techniques.

# A. Structure of collagen and mechanical properties

Collagen plays a critical role in many biological tissues and materials, including tendon, bone, teeth, cartilage, and many other materials.[12] Collagen and its components have been studied extensively in the past decades, primarily using experimental techniques, focusing on various aspects of collagen, including its structure, chemical properties, and interactions with other materials. For example, x-ray diffraction experiments have been carried out to help elucidate its structure.[13] Collagen shows, as many other biological materials do, a complex hierarchical structure.[8] Figure 1 is a visualization of the different design hierarchies, ranging from the nanoscopic scale of polypeptides to microscopic collagen fibers.[9] Each tropocollagen molecule consists of a spatial

![img-0.jpeg](img-0.jpeg)
FIG. 1. (a) Simplistic, schematic view of some of the hierarchical features of collagen, ranging from the amino acid, polypeptide level up to the scale of collagen fibers. In this article, we focus on the mechanical properties of tropocollagen fibers, a triple helical molecule self-assembly to form collagen fibrils, the constituents of collagen fibers. (b) Collagen triple helical structure, embedded in a skin of water molecules.

arrangement of three polypeptides. These three molecules or polypeptides are arranged in a helical structure, stabilized mainly by H-bonding between different residues. Every third residue in each of these molecules is a glycine (GLY) amino acid, and about one fourth of the molecule consists of proline (PRO) and hydroxyproline (HYP). The structure of collagen has been known since classical works by Ramachandran in 1951, focusing on theoretical understanding of how tropocollagen molecules are stabilized. Recently, various types of tropocollagen molecules have been crystallized and analyzed using x-ray diffraction techniques to determine their exact atomic configuration. Transmission electron microscopy (TEM) experiments have also been used to study the structure of collagen in various environments, including in bone, in particular focusing on larger length scale features and its three-dimensional arrangement.

# B. Literature review

There are several reports of experimental studies focused on the mechanics of single tropocollagen fibers. $^{7,15-20}$ However, despite its relatively simple structure, $^{13}$ collagen molecules have rarely been studied using molecular dynamics (MD) studies. In one of the few

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

reports we found in the literature, Lorenzo and coworkers $^{21}$ have recently reported investigations of the mechanical properties of collagen fibers, using MD studies, focusing on their Young's modulus. Other studies focused on the stability of collagen molecules $^{22}$ and other structural investigations, $^{23}$ or the effect of point mutations on the stability. $^{24-26}$ Some researchers modeled collagen at the continuum scale, using techniques such as finite element modeling (FEM). $^{23,27}$ In a recent study, molecular models of collagen have been linked to collagen mechanics. $^{28}$

However, no atomic-scale, consistent studies have been carried out on collagen with the aim of elucidating its fundamental properties such as bending stiffness, response to tensile stretching, and the interaction of several collagen fibers with each other, in particular, under shear loading. Furthermore, none of the previously reported studies have investigated the large-strain, permanent or plastic or fracture behavior of single fibers of tropocollagen, and the self-assembly processes associated with those molecules. The lack of such studies motivates the investigations reported in this article, aiming at an atomistic based, fundamental development of mechanics of collagen.

## C. Hypothesis, strategy, and research objectives

To understand the mechanical properties of more complex collagen-based materials such as tendon or bone, it is critical to begin with a thorough understanding of the behavior of the smallest levels of detail, tropocollagen molecules. We hypothesize that these molecules show a strongly nonlinear behavior, in particular under large stretch. Further, we believe that the complex interactions of different types of attractive and repulsive forces in assemblies of tropocollagen molecules govern their overall behavior. Failure to understand the atomic details prevents development of theoretical models of collagen-based materials.

To investigate the properties of collagen, we will use a combination of atomistic modeling using nonreactive and reactive force fields and mesoscale modeling. Atomistic modeling has evolved into a significant tool to model fracture in materials, which has been widely applied to crystalline materials at various length scales.[29,30] Here we extend those models to describe the fracture behavior of biological materials based on proteins.

In the literature, to the best of our knowledge, there is no thorough investigation of various aspects of mechanics of collagen fibers, including tensile stiffness, bending stiffness, interaction of various tropocollagen molecules, or fracture and plasticity of the building blocks of collagen. We address the following questions ranging from the atomic scale to the domain of assemblies of tropocollagen molecules: (i) Atomic or nanoscale: How does

a tropocollagen molecule respond to mechanical stretching force, in particular at large stretches? How does it fracture? How can these properties be linked to the folded structure? (ii) Molecular scale: How can the overall behavior of a single tropocollagen molecule be described using concepts of continuum theories or mesoscopic descriptions, in which the effects of individual atoms, solvent, and other interactions are condensed into simplified interactions? (iii) Ultra-long collagen molecules: How do ultra-long collagen molecules with realistic lengths of several hundred nanometers behave in solution?

## D. Outline of this paper

We proceed as follows. After a brief review of our computational technique in Sec. II, we report atomistic modeling of the mechanics of single collagen fibers under different types of loading in Sec. III. Section IV is dedicated to development of a mesoscopic model of collagen based on a combination of beads. Such models enable us to develop larger models, in both time and space, to study the behavior of collagen fibers beyond the persistent length, as well as larger bundles of tropocollagen molecules. In Sec. V, we provide a discussion of the results.

## II. COMPUTATIONAL TECHNIQUE: CLASSICAL AND REACTIVE FORCE FIELDS AND VISUALIZATION

Definition of the atomic interactions by force fields is at the heart of MD methods, as it defines the complete materials behavior. The basis for our investigations is the CHARMM force field, $^{31}$ a widely used model to describe the behavior of proteins and related materials and structures. However, for extreme mechanical loading and large deformation close to the breaking point, such classical approaches fail, and new methods are required that take into consideration the behavior of chemical bonds at large deformation. We use a new generation of reactive force fields to account for these chemical effects in protein mechanics.

## A. Classical force fields: CHARMM

The basis for our studies is the classical force field CHARMM, $^{31}$ implemented in the MD program NAMD. $^{32,33}$ The CHARMM force field $^{31}$ is widely used in the protein and biophysics community and provides a basic description of proteins. It is based on harmonic and anharmonic terms describing covalent interactions, in addition to long-range contributions describing van der Waals (vdW) interactions, ionic (Coulomb) interactions, and hydrogen bonding. Because the bonds between atoms are modeled by harmonic springs or its variations,

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

bonds between atoms cannot be broken, and new bonds cannot be formed. Also, the charges are fixed and cannot change, and the equilibrium angles do not change, depending on stretch. We have added an extension to the standard CHARMM force field to include a description of the hydroxyproline residue [HYP in the Protein Data Bank (PDB) file], which is not one of the 20 natural amino acids. We follow the procedure suggested in Ref. 34.

## B. Reactive force field: A new bridge to integrate chemistry and mechanics

Reactive force fields represent a major milestone in overcoming the limitations of classical force fields in not being able to describe chemical reactions. For mechanical properties, this translates into the properties of molecules at large strain, a phenomenon referred to as hyperelasticity. Several types of reactive potentials have been proposed in recent years.[35-38] Reactive potentials can overcome the limitations of empirical force fields and enable large-scale simulations of thousands of atoms with quantum mechanics accuracy. The reactive potentials, originally only developed for hydrocarbons,[35,36,38] have been extended recently to cover a wide range of materials, including metals, semiconductors, and organic chemistry in biological systems such as proteins.[37,39-47] Here we use the ReaxFF formulation.[38] We use a particular type of the ReaxFF potentials as suggested in Refs. 38 and 44 with slight modifications to include additional QM data suitable for protein modeling.[48]

Reactive potentials are based on a formulation more sophisticated than most nonreactive potentials. A bond length/bond order relationship is used to obtain a smooth transition from non-bonded to single-, double-, and triple-bonded systems. All connectivity-dependent interactions (that means valence and torsion angles) are formulated to be bond-order dependent. This ensures that their energy contributions disappear upon bond dissociation so that no energy discontinuities appear during reactions. The reactive potential also features non-bonded interactions (shielded van der Waals and shielded Coulomb). The reactive formulation uses a geometry-dependent charge calculation scheme similar to QEq $^{49}$ that accounts for polarization effects and modeling of charge flow. This is a critical breakthrough leading to a new bridge between QM and empirical force fields. All interactions feature a finite cutoff of approximately $10\AA$. Figure 2 shows a comparison between reactive and non-reactive formulations, illustrating that both descriptions agree for small deviations from the equilibrium but disagree significantly for large strains.

## C. Preprocessing, post-processing, and visualization

Preprocessing of the simulations is done using the CMDF framework, $^{39,50}$ a new computational Python-based

![img-1.jpeg](img-1.jpeg)
FIG. 2. Reactive versus nonreactive force fields. Whereas nonreactive force fields such as CHARMM or AMBER do not allow for bonds to break and form, the new generation of reactive force fields enables modeling of chemical bonds of different strength, competing during complex deformation mechanisms of materials. In this paper, we use both approaches, reactive and nonreactive formulations, applied to the mechanics of protein-based materials.

simulation environment capable of seamless integration of various file formats, computational engines, including molecular, and crystal building tools. We use the VMD program for visualization,[51,52] suitable for both atomistic, molecular, and mesoscale data. Python scripts are used to analyze and post-process the simulation data, as required for example to compute statistical averages of force-displacement curves.

## D. Computational procedure

Our tool is MD modeling, as widely used to model the behavior of materials and molecules.[53] We build the crystal unit cells according to x-ray diffraction data obtained by experiment. These structures are taken directly from the Protein Data Bank (PDB). We use the crystal structure PDB ID 1QSU, with $1.75\AA$ resolution, as reported by Kramer and coworkers.[13] The 1QSU is a triple-helical collagen-like molecule with sequence $(\mathrm{Pro - Hyp - Gly})_4\mathrm{-Glu - Lys - Gly - (Pro - Hyp - Gly})_5$

The charges of each atom are assigned according to the CHARMM rules implemented in the tLEaP program. Hydrogen atoms are added according to pH 7, and the protonation states of individual amino acids are assigned according to pH 7 as well. The CHARMM input files (structure and topology files) are then used to perform NAMD calculations. For ReaxFF calculations, no typing is necessary, and charges are determined dynamically during the simulation. Hydrogen atoms are added using the NAMD/CHARMM procedure, according to the same conditions as outlined above. We include crystallographic water in the simulations, and also add a skin of water of a few angstrom surrounding each tropocollagen molecule or, in the case of two molecules, surrounding

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

the overall geometry. We ensure that the whole molecule assembly is embedded in water. This configuration (for a single fiber) is visualized in Fig. 1(b).

Before finite temperature, dynamical calculations are performed, we carry out an energy minimization for several thousand steps, making sure that convergence is achieved, thus relieving any potential overlap in vdW interactions after adding hydrogen atoms. In the second step, we anneal the molecule after heating it up to a temperature $T = 300 \mathrm{~K}$. The heat up rate is $\Delta T = 25 \mathrm{~K}$ every 25 steps, and we keep the temperature fixed after the final temperature $T = 300 \mathrm{~K}$ is achieved (then we apply a temperature control in a NVT ensemble $^{53}$ ). We also ensure that the energy remains constant after the annealing procedure. The relaxed initial length of each molecule (consisting of 30 residues in each of the three chains) is $L_{0} = 84 \AA$.

Depending on the details of the loading case, we then apply mechanical forces using various types of constraint and investigate the response of the molecule due to the applied loading. Typically, we obtain force-versus-displacement data, which is then used to extract mechanical quantities such as stress and strain, using continuum mechanical concepts by drawing analogies between the molecular level and continuum mechanical theories. Steered MD is based on the concept of adding restraint force to groups of atoms by extending the Hamiltonian by an additional restraint potential of the form $1 / 2\mathrm{k}_{\mathrm{SMD}}$ $(r - r_h)^2$. Unless indicated otherwise, we use a steered molecular dynamics (SMD) scheme[32] with spring constant $\mathrm{k_{SMD}} = 10\mathrm{kcal / mol / A^2}$. It was shown in previous studies that this is a reasonable choice leading to independence of the measured molecular mechanical properties from the choice of the SMD spring constant.[21]

# III. COMPUTATIONAL RESULTS USING ATOMISTIC MODELING

In the following section, we present a suite of studies with different mechanical loading. The different loading cases studied in this article are summarized in Fig. 3. The different loading conditions and the objective of the specific calculation are: tensile testing (obtain Young's modulus) [Fig. 3(a)]; compression (compression resistance) [Fig. 3(a)]; bending (bending stiffness and persistence length) [Fig. 3(b)]; shearing two fibers (obtain fiber-fiber interactions) [Fig. 3(c)]; disintegrating a single fiber, by pulling out a single fiber (resistance with respect to extreme mechanical impact) [Fig. 3(d)].

# A. Tensile and compressive loading

## 1. Elastic deformation

First we discuss tensile testing of the fibers using the nonreactive force field. After careful equilibrium of the

![img-2.jpeg](img-2.jpeg)
(a)

![img-3.jpeg](img-3.jpeg)
(b)

![img-4.jpeg](img-4.jpeg)
(c)

![img-5.jpeg](img-5.jpeg)
(d)
FIG. 3. Overview of various load cases studied in this work. Our load cases include (a) tensile loading in the axial direction of the molecule (also including compressive test), (b) bending test, (c) shear test, and (d) mechanically stimulated disintegration of a tropocollagen by pulling out a single fiber. Note that in case (d), the polypeptide that is pulled out (highlighted) is not fixed at the left end, whereas the other two polypeptides are fixed.

structure of the collagen molecule, we apply a force at one end while we keep the other end of the molecule fixed. The loading case is shown in Fig. 3(a). By slowly increasing the load applied to the collagen molecule, while measuring the displacement $d$, we compute force-displacement curves. The force versus displacement curve $F(d)$ can be used to determine a stress versus strain curve, by proper normalization:

$$
\sigma (d) = \frac {F (d)}{A _ {\mathrm {C}}} \quad , \tag {1}
$$

where $A_{\mathrm{C}}$ denotes an equivalent area of the cross-section of a collagen molecule (see Sec. III. B on further details how this quantity is estimated), and $A_{\mathrm{C}} = \pi \cdot R^{2} \approx 214.34 \, \text{\AA}^{2}$, assuming that $R = 8.26 \, \text{\AA}$ (obtained from studies of an assembly of two tropocollagen molecules as described in Sec. III. C). Note that the stress is typically dependent on the stretch $d$. The local (in terms of strain) Young's modulus $E(d)$ is given by

$$
E (d) = \frac {d _ {0}}{A _ {\mathrm {C}}} \frac {\partial F (d)}{\partial d}, \tag {2}
$$

where $d_0$ is the initial, undeformed length of the collagen fiber, and $d_0 = 84\AA$. Note that Young's modulus is independent of the length of the molecule. The definition

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

in Eq. (2) is a consequence of the fact that the stretching force is expressed as a function of stretch $d$ rather than strain $(\sigma = E\epsilon)$.

Figure 4 shows force versus displacement plots for tensile loading for three different loading rates. The loading rates in the three cases are $\dot{r}_{\lambda} = 0.0001 \, \text{\AA/step}$, $\dot{r}_{\lambda} = 0.0002 \, \text{\AA/step}$, and $\dot{r}_{\lambda} = 0.001 \, \text{\AA/step}$. Young's modulus is determined as the tangential slope corresponding to $10\%$ tensile strain. Young's modulus is obtained as $E_{\mathrm{tens}} = 6.99 \, \mathrm{GPa}$, $E_{\mathrm{ten}} = 8.71 \, \mathrm{GPa}$, and $E_{\mathrm{ten}} = 18.82 \, \mathrm{GPa}$ for increasing loading rates as specified above. We observe an increase in stiffness for higher loading rates. These results indicate that collagen fibers show a rate-dependent elastic response.

Our estimate for Young's modulus is in somewhat agreement with results reported in Ref. 21, presenting a value for Young's modulus of around $4.8 \pm 1.0$ GPa (although they assumed a smaller radius of each tropocollagen molecule of $R \approx 7.65\,\text{\AA}$). The reason for the difference of our results could be the different force field used, different boundary conditions, or different strain.

Figure 5 depicts snapshots of the tropocollagen molecule under increasing stretch. At large strains, the helical structure is lost, and the three polypeptides appear as individual strands, then defining its elasticity by the behavior of covalent bonds. This is also confirmed in the force-strain plot (Fig. 4). The "local" Young's modulus associated with large strains is given by $E_{\mathrm{tens}}^{\mathrm{large}} = 46.7$ GPa (slope indicated in Fig. 4).

Under compressive loading, we observe that the collagen fiber can sustain only a relatively small load before

![img-6.jpeg](img-6.jpeg)
FIG. 4. Force versus strain, pulling of a single collagen fiber. An initial regime of flat, almost linear, elastic extension is followed by onset of nonlinear stiffening behavior at larger strains beyond $35\%$ strain. This behavior can be explained by the fact that the tertiary helical structure of the tropocollagen molecule begins to disappear and the elasticity of each covalent bond in the single strand governs the elastic response. This is also verified in Fig. 5. This represents a significant distinction for the results obtained with reactive force fields, suggesting failure due to strain/force localization. The loading rates in the three cases are $\dot{r}_{\lambda} = 0.0001\,\text{\AA/step}$ (red curve), $\dot{r}_{\lambda} = 0.0002\,\text{\AA/step}$ (blue curve), and $\dot{r}_{\lambda} = 0.001\,\text{\AA/step}$ (cyan curve).

buckling. Figure 6 shows load versus displacement curves, and Fig. 7 depicts several snapshot as the collagen molecule is subjected to compressive loading. The maximum force level sustained before buckling is $E_{\mathrm{max,compr}} \approx 1050$ pN, reached at about $5\%$ compressive strain. Young's modulus under compressive loading, calculated for very small strains up to $1.25\%$, is given by $E_{\mathrm{comp}} \approx 29.86$ GPa. This indicates that the elastic tensile/compressive behavior is asymmetric around the equilibrium position, with significantly higher compressive modulus than tensile modulus. However, the maximum load that can be sustained under pure compression is much lower than that under tension due to buckling. We note, however, that the situation may be quite different in bundles of tropocollagen molecules due to geometric constraints (the fibrils, see also the schematic in Fig. 1).

## 2. Fracture of tropocollagen molecules

Now we focus on the mechanical behavior of collagen fibers using a reactive force field. The dominating forces in collagen fibers are always in the axial direction of the tropocollagen molecule, so this type of loading is most critical in terms of the mechanical integrity.

Questions that we would like to investigate include: Under which conditions do classical, nonreactive force fields break down, and what are the limitations of these methods? Do the results agree for small deformation? The main question is, how are the mechanical properties different once mechanical deformation is large and formation and breaking of bonds are allowed? We pulled the fiber until fracture occurs and study the details of the fracture mechanisms. A central question we would like to address is, to which strain and deformation levels (or, equivalently, applied force level), can we rely on the assumption of nonreactive force fields (this becomes important later when we discuss the mesoscale model).

We observe that the shape of the fiber changes from a straight shape to an S-like shape as the load increases. This change of shape leads to an increasing radius of curvature in localized regions of the fiber (towards the left and right ends). These regions with high curvature represent regions of higher tensile stress. In agreement with this notion, we observe that those regions lead to onset of failure. This is shown in Figs. 8(a)-8(e).

A possible explanation for the transformation into the S-like shape may be the different energy expression in the reactive potential. The change of bond behavior at large deformation is not linear, but instead, it is nonlinear, eventually leading to bond rupture. This observation underlines the importance of large-strain bond rupture behavior, as found in several other studies of fracture of brittle materials.[29,30] The observation of transformation into an S-shaped structure will be discussed in future works, in particular with respect to the accuracy and fitting of the reactive potential.

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

![img-7.jpeg](img-7.jpeg)
FIG. 5. Stretching of a single collagen fiber using a classical nonreactive CHARMM force field. The helical structure unfolds with increasing strain and vanishes at large deformation, the three strands become independent, and the covalent bonds between atoms govern the elasticity. This loss in tertiary helical structure is represented by a change in tangent elasticity, as seen in Fig. 4, at strains beyond 35%.

![img-8.jpeg](img-8.jpeg)
FIG. 6. Compressive loading of the single fiber and a loading rate of $\dot{r}_{\mathrm{h}} = 0.0002 \, \text{\AA}/\text{step}$. The behavior under compression is significantly different from that under tension, also revealing an asymmetry of the elastic properties at small strains. The tropocollagen molecule starts to buckle at about 5% compressive strain.

![img-9.jpeg](img-9.jpeg)
FIG. 7. Collagen molecule under compressive loading (water molecules are not shown). The results suggest that upon a relatively small load, the tropocollagen molecule starts to buckle and goes into a bending mode.

Figure 8(f) shows several plots of force versus strain. The strength of the tropocollagen molecule is determined to be $F_{\max, \text{tens}} \approx 2.35 \times 10^{4} \, \text{pN}$, reached at about 5% tensile strain. We find that the CHARMM description

and the ReaxFF model agree for small strains up to approximately 10 percent strain.

We have repeated the tensile calculation for a single polypeptide out of the three making up the tropocollagen molecule. The strength of an individual polypeptide molecule is determined to be $F_{\max, \text{tens}} \approx 0.713 \times 10^{4} \, \text{pN}$, reached at about 3.7% tensile strain. This is significantly lower than that of the tropocollagen molecule [see Fig. 8(f), curve (iii)].

## B. Bending a single tropocollagen molecule and its persistence length

We perform a computational experiment to describe the bending of a single fiber by clamping it at the boundaries and applying a force in the center of the collagen fiber, as shown in Fig. 3(b). This is equivalent to the three-point bending test widely used in engineering. From the force-displacement data obtained by atomistic modeling, the bending stiffness $EI$ is given by

$$
EI = \frac{dL^3}{48F_{\text{appl}}} \tag{3}
$$

where $F_{\text{appl}}$ is the applied force and $d$ is the bending displacement. Figure 9 depicts a load versus displacement curve. Based on the simulation results, we estimate $EI = 9.71 \times 10^{-29} \, \text{Nm}^2$. The persistent length can be estimated to be

$$
\xi = \frac{EI}{k_{\mathrm{B}}T} \tag{4}
$$

where $k_{\mathrm{B}}$ is the Boltzmann constant, and $T$ is the temperature. At $T = 300 \, \mathrm{K}$, we find the persistence length $\xi \approx 23.4 \, \mathrm{nm}$, which is close to results obtained by experimental investigations suggesting a persistence length

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

![img-10.jpeg](img-10.jpeg)

![img-11.jpeg](img-11.jpeg)
FIG. 8. (a-e) Modeling fracture of a single collagen fiber. We observe a transformation from the initial straight shape to an S-shaped structure at large strains, leading to fracture of an individual polypeptide. This transformation is found consistently for a variety of loading conditions. (f) Comparing results for (i) nonreactive (CHARMM) modeling, with (ii) and (iii) reactive force field modeling. Curves (i) and (ii) show the results of stretching force versus strain for a tropocollagen molecule, and curve (iii) depicts the results for stretching of a single polypeptide. Both theories agree at small strains (up to about  $10\%$ ) but deviate strongly at large strains. For the ReaxFF calculations we use  $\mathrm{k_{SMD}} = 10\mathrm{kcal / mol / A^2}$  and loading rate  $\dot{r}_{\lambda} = 0.0005\AA /$  step [curve (ii)] and  $\dot{r}_{\lambda} = 0.00015\AA /$  step. The ReaxFF calculations are carried out with much fewer water molecules than the CHARMM calculations due to computational limitations.

of  $14.5 \pm 7.3 \mathrm{~nm}$ . This value is similar to other experimental reports in the literature.

# C. Shearing two tropocollagen molecules

We continue with shearing experiments of an assembly of two tropocollagen molecules. The objective is to gain insight into the mechanisms and type of interactions between two tropocollagen molecules in aqueous solution. We start with the geometry as depicted schematically in Fig. 3(d). We first equilibrate the system without

application of any mechanical shear load. We find that the equilibrium distance between two molecules depends on the presence of solvent, and it is reduced if solvent is present. With solvent present, we find an equilibrium distance between two tropocollagen molecules of  $r_{\mathrm{EQ}} \approx 16.52$  Å. All studies reported here are carried out with water molecules present. We note that this equilibrium distance leads to a molecular radius of 8.26 Å.

We perform calculations with three different loading rates,  $\dot{r}_{\lambda} = 0.0002\AA/\mathrm{step}$ ,  $\dot{r}_{\lambda} = 0.00005\AA/\mathrm{step}$ , and  $\dot{r}_{\lambda} = 0.000025\AA/\mathrm{step}$ . We find that the resulting values

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

![img-12.jpeg](img-12.jpeg)
FIG. 9. Bending displacement response of a single collagen fiber embedded in a water skin to bending [three-point bending loading case as shown in Fig. 3(b)]. For this simulation, we choose  $\mathrm{k_{SMD}} = 0.01$  kcal/mol/Å² and a loading rate  $\dot{r}_{\mathrm{A}} = 0.000,001$  Å/step. The results suggest a linear dependence of force and bending displacement for small deformation.

are strain rate dependent. The maximum force decreases with decrease in loading rate, assuming values  $F_{\mathrm{max,shear}} \approx 2900 \mathrm{pN}$ ,  $F_{\mathrm{max,shear}} \approx 1,100 \mathrm{pN}$ , and  $F_{\mathrm{max,shear}} \approx 750 \mathrm{pN}$ , corresponding to the strain rates provided above. Using a linear extrapolation to vanishing loading rate, we estimate a maximum shear force of  $F_{\mathrm{max,shear}} \approx 466 \mathrm{pN}$ , corresponding to adhesion strength  $\tau_{\mathrm{max}} = 5.55 \mathrm{pN} / \AA$ .

Figures 10(a)–10(d) depict snapshots of the system as it undergoes shear deformation. Figure 11(e) depicts the force versus displacement curve as obtained during the shearing experiment, for the largest and smallest loading rate.

# D. Pulling a single polypeptide out of a tropocollagen molecule

Here we study pulling a single fiber out of the tropocollagen molecule. The results are shown in Fig. 11. We find that the critical force required for pulling out a single fiber is  $F_{\mathrm{max, tens}} \approx 1.15 \times 10^{4} \mathrm{pN}$ . This is lower than the

![img-13.jpeg](img-13.jpeg)
(c)

![img-14.jpeg](img-14.jpeg)
(d)

![img-15.jpeg](img-15.jpeg)
(e)
Displacement (Angstrom)
FIG. 10. (a-d) The dynamics of shearing two collagen tropocollagen molecules. The solvation water molecules are not shown here, although they are present in the simulation. The upper fiber is clamped at the left end whereas a force is applied at the right end of the lower fiber. Once the applied force reaches a critical value, we observe (b) onset of sliding, eventually (d) fracturing the molecular assembly. (e) Shear force versus displacement: curve (i) loading rate  $\dot{r}_{\mathrm{A}} = 0.000,2\AA/\mathrm{step}$ , and curve (ii) loading rate  $\dot{r}_{\mathrm{A}} = 0.000,025\AA/\mathrm{step}$ . The plot reveals that the maximum shear force decreases with decreasing strain rate. In both cases, a level of maximum force is followed by a regime of constant decay of the force due to continuous loss of adhesion area due to sliding of the two molecules across each other (since  $F_{\mathrm{shear}} \sim \tau_{\mathrm{max}} d_{\mathrm{s}}$ , with  $d_{\mathrm{s}}$  being the contact length between two fibers, and  $\tau_{\mathrm{max}}$  being the maximum shear force per unit length).

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

![img-16.jpeg](img-16.jpeg)
FIG. 11. Pulling out a single polypeptide out of a tropocollagen molecule. The maximum force approaches $1.18 \times 10^{4} \mathrm{pN}$. We choose a loading rate $\dot{r}_{\mathrm{k}} = 0.002 \AA/\mathrm{step}$. A linear regime is following by a slight stiffening regime at strains larger than $22\%$.

maximum strength of a triple helical molecule, being $F_{\mathrm{max,tens}} \approx 2.4 \times 10^{4}$ pN. However, the maximum strength of a single polypeptide is $F_{\mathrm{max,tens}} \approx 0.713 \times 10^{4}$ pN, lower than the maximum pulling out force. This indicates that pulling out of a single fiber is not possible due to rupture of the polypeptide during pulling. This underlines the mechanical stability of the tropocollagen molecule, being resistant to disintegration of pulling out single fibers.

## IV. MESOSCOPIC MODEL

The atomistic modeling results, carried out at the level of individual polypeptide chains, tropocollagen molecules, and assemblies of those helped to develop a better qualitative and quantitative understanding of the competing mechanisms and forces during deformation of collagen at a microscopic level. This information is now used to develop a mesoscopic model, in which beads connected by different types of springs represent collagen molecules, whereas all parameters are completely derived from atomistic calculations. The motivation for these studies is the desire to model larger length and time scales. This is similar to training empirical potentials from quantum mechanical data, as done successfully in the past.[54] The reduction of degrees freedom in the mesoscale model enables one to study very long tropocollagen molecules with lengths on the order of several hundred nanometers, as well as bundles of tropocollagen molecules. This approach enables reaching a "material scale" and makes the overall mechanics of the material accessible to atomic and molecular scale modeling.

We replace a piece of collagen molecule of length $84\AA$ with 6 beads or particles, thus reducing the number of particles by a factor of several hundred. In addition to reduction of degrees of freedom, we can now also use

much larger time step for integration of the equations of motion, as each bead has a large mass of several thousand atomic mass units, enabling time steps of around 20 fs.

We emphasize that the influence of the solvent on the behavior of the tropocollagen molecules is captured in the model constants, so that no explicit modeling of those is required, further simplifying the computational task.

## A. Model development: Training from pure atomistic results using energy and force matching

The goal here is to develop the simplest model possible to perform large-scale studies of the mechanics of collagen molecules, eventually leading to understanding of the behavior of assemblies of such fibers. We assume that we can write the total energy of the system as

$$
E = E _ {\mathrm {T}} + E _ {\mathrm {B}} + E _ {\text {w e a k}}. \tag {5}
$$

The bending energy is given by

$$
\phi_ {\mathrm {B}} (\varphi) = \frac {1}{2} k _ {\mathrm {B}} \left(\varphi - \varphi_ {0}\right) ^ {2}, \tag {6}
$$

with $k_B$ as the spring constant relating to the bending stiffness. The resistance to tensile load is characterized by

$$
\phi_ {\mathrm {T}} (r) = \frac {1}{2} k _ {\mathrm {T}} \left(r - r _ {0}\right) ^ {2}, \tag {7}
$$

where $k_{\mathrm{T}}$ refers to the resistance of the molecule to deform under tensile load. In addition, we assume weak, dispersive interactions between either different parts of each molecule or different molecules, defined by a Lennard-Jones (LJ) function

$$
\phi_ {\text {w e a k}} (r) = 4 \epsilon \left(\left[ \frac {\sigma}{r} \right] ^ {1 2} - \left[ \frac {\sigma}{r} \right] ^ {6}\right), \tag {8}
$$

with $\sigma$ as the distance parameter and $\epsilon$ describing the energy well depth at equilibrium. Note that the total energy contribution of each part is given by the sum over all pair-wise and triple (angular) interactions in the system

$$
E _ {\mathrm {I}} = \sum_ {\text {p a i r s}} \phi_ {1} (r) \quad \text {a n d} \quad E _ {\mathrm {B}} = \sum_ {\text {a n g l e s}} \phi_ {\mathrm {B}} (\varphi). \tag {9}
$$

## 1. Equilibrium distances of beads and corresponding masses

The mass of each bead is determined by assuming a homogeneous distribution of mass in the molecular model (which is an excellent assumption). The total mass of the tropocollagen molecule used in our studies is given by 8152.2 amu. We divide the total length of the tropocollagen molecule used in the MD studies into $N_{\mathrm{MD}} = 6$ pieces, each bead containing 5 amino acid residues. Each bead then has a weight of 1358.7 amu. Because the total length of the molecule is $L_0 = 84 \AA$, the beads are

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

separated by a distance $r_0 = 14 \, \text{\AA}$. The beads represent different sequences in tropocollagen that when added together make the entire sequence.

## 2. Dispersive and nonbonding interactions

The LJ parameters are determined from the calculations of shearing two collagen fibers. In all these considerations, we assume that a pair-wise interaction between different tropocollagen molecules is sufficient, and that there are no multi-body contributions. Based on these assumptions, we model the interactions between different molecules using a LJ 12:6 potential. The distance parameter $\sigma$ is given by

$$
\sigma = \frac {D}{\sqrt [ 6 ]{2}} \approx 14.72 \, \text{\AA}, \tag {10}
$$

where $D$ is the equilibrium distance as measured in the MD simulations, $D = 16.52\,\text{\AA}$.

The shear strength (experiment described in Sec. III. C) can be used to extract the LJ parameters for the weak, dispersive interactions between two fibers. Note that this interaction includes the effect of solvation water and other bonding (e.g., H-bonds etc.).

The maximum force in a LJ potential, assuming a single LJ bond is given by

$$
F _ {\max , \mathrm {L J}} = \frac {\Lambda \cdot \epsilon}{\sigma}, \tag {11}
$$

while noting that $\Lambda \approx 2.3964$ for the LJ 12:6 potential. The parameter $\sigma$ is already determined, leaving only $\epsilon$ to train using a force-matching approach.

The parameter $\epsilon$ can be obtained by requiring a force balance at the point of rupture:

$$
F _ {\max , \mathrm {L J}} N _ {\mathrm {M D}} = \tau_ {\max } \cdot L = F _ {\max } \quad . \tag {12}
$$

This expression can be used to determine $\epsilon$ as

$$
\epsilon = \frac {F _ {\max} \cdot \sigma}{\Lambda \cdot N _ {\mathrm {M D}}} \quad . \tag {13}
$$

From atomistic modeling, we calculate $F_{\mathrm{max}}$ allowing to estimate numerical values for $\epsilon$. We find that $\epsilon \approx 11.06$ kcal/mol predicted from Eq. (13).

Based on the extrapolation of shear force $F_{\mathrm{max, shear}} \approx 466\,\mathrm{pN}$ corresponding to vanishing strain rate (see discussion in Sec. III. C), we finally arrive at a value $\epsilon \approx \mathrm{kcal/mol}$. This value is used in the mesoscopic model.

Even though not implemented in this model, variations of the adhesion strength between different tropocollagen molecules because of sequence patterns could easily be modeled by changing $\epsilon$ along the molecular length.

## 3. Tensile spring parameter

The tensile spring constant is determined from various calculations of stretch versus deformation, while being constrained to the regime of small loads and consequently small displacements. The spring constant $k_{\mathrm{T}}$ is then defined as

$$
k _ {T} = \frac {N _ {\mathrm {M D}} F _ {\text {a p p l}}}{\Delta d}, \tag {14}
$$

with $\Delta d = L - L_{0}$ being the displacement of the atomistic model due to applied force $F_{\mathrm{appl}}$. Based on the low-strain rate tensile testing data discussed in Sec. III, we find that $k_{\mathrm{T}} \approx 15.41 \, \mathrm{kcal/mol/Å}^2$.

## 4. Bending spring parameter

Using an argument of energy conservation between the atomistic and the mesoscale model, we arrive at an expression for the bending stiffness parameter $k_{\mathrm{B}}$

$$
k _ {\mathrm {B}} = \frac {48 \cdot E I \cdot d ^ {2}}{8 r _ {0} ^ {3} \left(\theta - \varphi_ {0}\right) ^ {2}}, \tag {15}
$$

where $\theta = 2\tan^{-1}(d / r_0)$, and $d = F_{\mathrm{appl}}8r_0^2 /(48\cdot EI$. Note that $\theta$ is the angle corresponding to the displacement $d$ resulting from an applied force $F_{\mathrm{appl}}$. We find that $k_{\mathrm{B}}\approx 14.98\,\mathrm{kcal / mol / rad}^2$. These expressions are valid only for small deformations. The approach of fitting the continuum elastic model to the bead model is visualized in Fig. 12.

## B. Example modeling results with mesoscopic model

Table I summarizes all parameters used in the mesoscopic model. In the mesoscopic model, beads only interact with their nearest neighbors to ensure that Eq. (11) is valid.

![img-17.jpeg](img-17.jpeg)
(a)

![img-18.jpeg](img-18.jpeg)
FIG. 12. Matching conditions between the (a) continuum, atomistic and (b) mesoscale model. We match the energy of both deformation states to extract parameters for the mesoscopic model.

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

TABLE I. Summary of mesoscopic parameters derived from atomistic modeling, corresponding to Eqs. (10), (13), (14), and (15), as well as the discussion presented throughout Sec. IV.

|  Equilibrium head distance r0(Å) | 14.00  |
| --- | --- |
|  Tensile stiffness parameter kT(kcal/mol/Å2) | 15.41  |
|  Equilibrium angle φ0(degrees) | 180.00  |
|  Bending stiffness parameter kB(kcal/mol/rad2) | 14.98  |
|  Dispersive parameter ε(kcal/mol) | 6.87  |
|  Dispersive parameter σ(Å) | 14.72  |

![img-19.jpeg](img-19.jpeg)
FIG. 13. The dynamics of a long single tropocollagen molecule, lengths (a)  $L = 14 \mathrm{~nm}$ , (b)  $L = 28 \mathrm{~nm}$ , and (c)  $L = 280 \mathrm{~nm}$  in water solvent, using the mesoscale model at  $T = 300 \mathrm{~K}$ . The mesoscale model enables simulations approaching several microseconds. Such large-scale studies approaching microsecond time scales would not be possible using full atomistic modeling. The results indicate that as the length of the tropocollagen molecule is increased beyond the persistence length, the molecule shows significant bending.

Here we report some example applications of the mesoscopic models and leave more extensive studies to future publications.

The models are implemented in the massively parallelized modeling code LAMMPS (http://www.cs.sandia.gov/~sjplimp/lammps.), capable of running on large computing clusters. The example calculations reported here are carried out in single CPU environments.

Our computational modeling is performed with a number of moles, volume, and temperature (NVT) ensemble. All studies are carried out at  $T = 300 \mathrm{~K}$ .

We focus on the long-time dynamical behavior of a tropocollagen molecule with different lengths, including  $L = 14 \mathrm{~nm}$ ,  $L = 28 \mathrm{~nm}$ , and  $L = 280 \mathrm{~nm}$  in aqueous solution, a study not possible with pure atomistic methods. Snapshots of those simulations are shown in Fig. 13.

![img-20.jpeg](img-20.jpeg)
FIG. 14. Overview of the various levels of mechanical strengths for different loading cases, as obtained by atomistic simulation, for a tropocollagen molecule with length  $L_{0} = 84$  Å. It is evident that the tensile fracture strength is largest with about  $23,500$  pN, while the shear strength of an assembly of two tropocollagen molecules is lowest, on the order of  $466$  pN, corresponding to adhesion shear strength  $\tau_{\mathrm{max}} = 5.55$  pN/Å. These results suggest that the shear between two fibers may play a critical role during deformation of collagen fibrils and fibers.

The observation of the dynamics of the tropocollagen molecule indicates that the tropocollagen molecule described in the mesoscopic model is indeed beyond its persistence length, in the present case  $L / \xi \approx 12$ .

# V. DISCUSSION AND CONCLUSION

We have reported atomistic modeling to calculate the elastic, plastic, and fracture properties of tropocollagen molecules. Using full atomistic calculations, we presented a suite of calculations of different mechanical loading types to gain insight into the deformation behavior of tropocollagen molecules. Our results suggest that it is critical to include a correct description of the bond behavior and breaking processes at large bond stretch, information stemming from the quantum chemical details of bonding. A critical outcome of these studies is the observation that tropocollagen molecules undergo a transition from straight molecules to an S-shaped structure at increasingly large tensile stretch. As a consequence, we find that rupture of a single fiber does not occur homogeneously and thus at random locations, but instead, a local stress concentration develops leading to rupture of the molecule. Such information about the fracture behavior of collagen may be essential to understand the role of collagen components in biological materials. For example, the mechanics of collagen fibers at large stretch may play a critical role in the mechanical properties of bone during crack propagation, and elucidation of its

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

mechanical response in particular at large strains is of critical importance during crack bridging in bonelike hard tissues.56–58

We believe that reactive modeling that takes into account the complexity of chemical bonding may be critical in understanding the fracture and deformation behavior of many other biological and protein-based materials. Further, we find a strong rate dependence of the mechanical properties, including Young’s modulus (see Sec. III. A. 1 and Fig. 4) and shear strength (see Sec. III. C and Fig. 10). This is in agreement with the fact that collagen is known to be a viscoelastic material.

We find that the properties of collagen are scale dependent. For example, the fracture strength of individual polypeptides is different from the fracture strength of a tropocollagen molecule (see Fig. 8). This agrees with the notion that the properties of many biological hierarchical materials are scale-dependent.

Our results provide estimates of the fracture and deformation strength for different types of loading, enabling a comparison of different relative strengths. Figure 14 provides an overview of the strength properties of tropocollagen molecules, summarizing the relative quantitative strength under different types of loading. The results suggest that the tensile strength of tropocollagen molecules is largest, approaching $2.4 \times 10^{4} \mathrm{pN}$, while the shear deformation constitutes the weakest link in the system, on the order of $466 \mathrm{pN}$. This further suggests the importance of shear deformation on collagen mechanics and opens the possibility to improve the material behavior by tuning the shear resistance, for example by introducing cross-linking. Indeed, such crosslinking is known to exist in many collagen-based materials.

The simple mesoscale model reported here opens up several possibilities for future studies, particularly at the scale of fibrils and possibly fibers. The mesoscopic model can be used to describe tensile experiments of pulling long molecules, naturally including the effects of entropy. Such results can be immediately compared with experiments.7 The mesoscopic model can also be used to probe how changes in the sequence would influence macroscopic properties, including the possibility of cross links. Such effects could be captured using the reactive potential. Our numerical methods could eventually be developed into engineering tools for recombinant DNA technologies.

Future studies could be used to further improve the mesoscopic model. For example, so far we have not included the effect of variations in adhesion strength along the axial direction of tropocollagen molecules. Similar methods as those discussed in Sec. III. C could be used for collagen molecules with different sequences leading to different adhesion parameters. The importance of chemistry could also be investigated in studies related to

enzymatic activity in the proximity of collagen. Additional work could thus focus on addressing some of those aspects, including degradation of collagen due to enzymes, or other chemicals in the environment, similar to stress-assisted cracking. We believe that the new reactive force fields are a promising approach to address some of those aspects of collagen mechanics.

## ACKNOWLEDGMENTS

We acknowledge helpful discussions and collaboration with Dr. A. van Duin and W. Goddard regarding reactive force fields and their implementation. We further acknowledge stimulating discussions with Dr. David Tirrell in the general field of mechanical properties of biological protein-based materials.

## REFERENCES

1. R. Langer and D.A. Tirrell: Designing materials for biology and medicine. *Nature* 428, 487 (2004).
2. W.A. Petka, J.L. Harden, K.P. McGrath, D. Wirtz, and D.A. Tirrell: Reversible hydrogels from self-assembling artificial proteins. *Science* 281, 389 (1998).
3. S.A. Maskarinec and D.A. Tirrell: Protein engineering approaches to biomaterials design. *Curr. Opin. Biotechnol.* 16, 422 (2005).
4. J.M. Smeenk, M.B.J. Otten, J. Thies, D.A. Tirrell, H.G. Stunnenberg, and J.C.M. van Hest: Controlled assembly of macromolecular beta-sheet fibrils. *Angew. Chem., Int. Ed.* 44, 1968 (2005).
5. M.L. Mock, T. Michon, J.C.M. van Hest, and D.A. Tirrell: Stereoselective incorporation of an unsaturated isoleucine analogue into a protein expressed in E. coli. *Chembiochem.* 7, 83 (2006).
6. M.R. Diehl, K.C. Zhang, H.J. Lee, and D.A. Tirrell: Engineering cooperativity in biomotor-protein assemblies. *Science* 311, 1468 (2006).
7. L. Bozec and M. Horton: Topography and mechanical properties of single molecules of type I collagen using atomic force microscopy. *Biophys. J.* 88, 4223 (2005).
8. A. Bhattacharjee and M. Bansal: Collagen structure: The Madras triple helix and the current scenario. *IUBMB Life* 57, 161 (2005).
9. J.P. Borel and J.C. Monboisse: Collagens—Why such a complicated structure. *C. R. Seances Soc. Biol. Fil.* 187, 124 (1993).
10. S.M. Mithieux and A.S. Weiss: Elastin, in *Fibrous Proteins: Coiled-Coils, Collagen and Elastomers*. Advances in Protein Chemistry, Vol. 70, edited by D.A.D. Parry and J.M. Squire (Elsevier Academic Press, Amsterdam, 2005), p. 437.
11. B. Li and V. Daggett: Molecular basis for the extensibility of elastin. *J. Muscle Res. Cell Motil.* 23, 561 (2002).
12. C. Hellmich and F.J. Ulm: Are mineralized tissues open crystal foams reinforced by crosslinked collagen? Some energy arguments. *J. Biomech.* 35, 1199 (2002).
13. R.Z. Kramer, M.G. Venugopal, J. Bella, P. Mayville, B. Brodsky, and H.M. Berman: Staggered molecular packing in crystals of a collagen-like peptide with a single charged pair. *J. Mol. Biol.* 301, 1191 (2000).
14. M. Zervakis, V. Gkoumplias, and M. Tzaphlidou: Analysis of fibrous proteins from electron microscopy images. *Med. Eng. Phys.* 27, 655 (2005).

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

15. B.E. Layton, S.M. Sullivan, J.J. Palermo, G.J. Buzby, R. Gupta, and R.E. Stallcup: Nanomanipulation and aggregation limitations of self-assembling structural proteins. Microelectron. J. 36, 644 (2005).
16. K.N. An, Y.L. Sun, and Z.P. Luo: Flexibility of type I collagen and mechanical property of connective tissue. *Biorheology* 41, 239 (2004).
17. Y.L. Sun, Z.P. Luo, A. Fertala, and K.N. An: Stretching type II collagen with optical tweezers. J. Biomech. 37, 1665 (2004).
18. Y.L. Sun, Z.P. Luo, A. Fertala, and K.N. An: Direct quantification of the flexibility of type I collagen monomer. Biochem. Biophys. Res. Commun. 295, 382 (2002).
19. P.J. Arnoux, J. Bonnoit, P. Chabrand, M. Jean, and M. Pithioux: Numerical damage models using a structural approach: Application in bones and ligaments. Eur. Phys. J. Appl. Phys. 17, 65 (2002).
20. J.H. Waite, X.X. Qin, and K.J. Coyne: The peculiar collagens of mussel byssus. Matrix Biol. 17, 93 (1998).
21. A.C. Lorenzo and E.R. Caffarena: Elastic properties, Young's modulus determination and structural stability of the tropocollagen molecule: A computational study by steered molecular dynamics. J. Biomech. 38, 1527 (2005).
22. A.V. Persikov, J.A.M. Ramshaw, A. Kirkpatrick, and B. Brodsky: Electrostatic interactions involving lysine make major contributions to collagen triple-helix stability. Biochemistry 44, 1414 (2005).
23. M. Israelowitz, S.W.H. Rizvi, J. Kramer, and H.P. von Schroeder: Computational modeling of type I collagen fibers to determine the extracellular matrix structure of connective tissues. Protein Eng. Des. Sel. 18, 329 (2005).
24. S.D. Mooney and T.E. Klein: Structural models of osteogenesis imperfecta-associated variants in the COL1A1 gene. Mol. Cell. Proteomics 1, 868 (2002).
25. S.D. Mooney, P.A. Kollman, and T.E. Klein: Conformational preferences of substituted prolines in the collagen triple helix. Biopolymers 64, 63 (2002).
26. S.D. Mooney, C.C. Huang, P.A. Kollman, and T.E. Klein: Computed free energy differences between point mutations in a collagen-like peptide. Biopolymers 58, 347 (2001).
27. J.E. Bischoff, E.M. Arruda, and K. Grosh: Finite element modeling of human skin using an isotropic, nonlinear elastic constitutive model. J. Biomech. 33, 645 (2000).
28. J.W. Freeman and F.H. Silver: Elastic energy storage in unmineralized and mineralized extracellular matrices (ECMs): A comparison between molecular modeling and experimental measurements. J. Theor. Biol. 229, 371 (2004).
29. M.J. Buehler, F.F. Abraham, and H. Gao: Hyperelasticity governs dynamic fracture at a critical length scale. Nature 426, 141 (2003).
30. M.J. Buehler and H. Gao: Dynamical fracture instabilities due to local hyperelasticity at crack tips. Nature 439, 307 (2006).
31. A.D. MacKerell, D. Bashford, M. Bellott, R.L. Dunbrack, J.D. Evanseck, M.J. Field, S. Fischer, J. Gao, H. Guo, S. Ha, et al.: All-atom empirical potential for molecular modeling and dynamics studies of proteins. J. Phys. Chem. B 102, 3586 (1998).
32. J.C. Phillips, R. Braun, W. Wang, J. Gumbart, E. Tajkhorshid, E. Villa, C. Chipot, R.D. Skeel, L. Kale, and K. Schulten: Scalable molecular dynamics with NAMD. J. Comput. Chem. 26, 1781 (2005).
33. M.T. Nelson, W. Humphrey, A. Gursoy, A. Dalke, L.V. Kale, R.D. Skeel, and K. Schulten: NAMD: A parallel, object oriented molecular dynamics program. Int. J. Supercomp. Appl. High Perf. Comput. 10, 251 (1996).

34. D. Anderson: Collagen self-assembly: A complementary experimental and theoretical perspective. University of Toronto, 2005.
35. D.W. Brenner, O.A. Shenderova, J.A. Harrison, S.J. Stuart, B. Ni, and S.B. Sinnott: A second-generation reactive empirical bond order (REBO) potential energy expression for hydrocarbons. J. Phys.: Condens. Matter 14, 783 (2002).
36. S.J. Stuart, A.B. Tutein, and J.A. Harrison: A reactive potential for hydrocarbons with intermolecular interactions. J. Chem. Phys. 112, 6472 (2000).
37. A.C.T.v. Duin, A. Strachan, S. Stewman, Q. Zhang, X. Xu, and W.A. Goddard: ReaxFF SiO: Reactive force field for silicon and silicon oxide systems. J. Phys. Chem. A 107, 3803 (2003).
38. A.C.T.v. Duin, S. Dasgupta, F. Lorant, and W.A. Goddard: ReaxFF: A reactive force field for hydrocarbons. J. Phys. Chem. A 105, 9396 (2001).
39. M.J. Buehler, A.C.T.v. Duin, and W.A. Goddard: Multi-paradigm modeling of dynamical crack propagation in silicon using a reactive force field. Phys. Rev. Lett. 96, 09505 (2006).
40. A. Strachan, A.C.T. van Duin, D. Chakraborty, S. Dasgupta, and W.A. Goddard: Shock waves in high-energy materials: The initial chemical events in nitramine RDX. Phys. Rev. Lett. 91, 098301 (2003).
41. K.D. Nielson, A.C.T.v. Duin, J. Oxgaard, W. Deng, and W.A. Goddard: Development of the ReaxFF reactive force field for describing transition metal catalyzed reactions, with application to the initial stages of the catalytic formation of carbon nanotubes. J. Phys. Chem. A 109, 49 (2005).
42. S.S. Han, A.C.T. van Duin, W.A. Goddard, and H.M. Lee: Optimization and application of lithium parameters for the reactive force field, ReaxFF. J. Phys. Chem. A. 109, 4575 (2005).
43. K. Chenoweth, S. Cheung, A.C.T. van Duin, W.A. Goddard, and E.M. Kober: Simulations on the thermal decomposition of a poly(dimethylsiloxane) polymer using the ReaxFF reactive force field. J. Am. Chem. Soc. 127, 7192 (2005).
44. A. Strachan, E.M. Kober, A.C.T. van Duin, J. Oxgaard, and W.A. Goddard: Thermal decomposition of RDX from reactive molecular dynamics. J. Chem. Phys. 107, 3803 (2005).
45. S. Cheung, W.Q. Deng, A.C.T. van Duin, and W.A. Goddard: ReaxFF(MgH) reactive force field for magnesium hydride systems. J. Phys. Chem. A 109, 851 (2005).
46. K.D. Nielson, A.C.T. van Duin, J. Oxgaard, W. Deng, and W.A. Goddard: Development of the ReaxFF reactive force field for describing transition metal catalyzed reactions, with application to the initial stages of the catalytic formation of carbon nanotubes. J. Phys. Chem. A 109, 493 (2005).
47. L. Tao, M.J. Buehler, A.C.T.v. Duin, and W.A. Goddard: Mixed hybrid Dreiding-ReaxFF calculations for modeling enzymatic reactions in proteins. (2005, unpublished).
48. D. Datta, A.C.T.v. Duin, and W.A. Goddard: Extending ReaxFF to biomacromolecules. (2005, unpublished).
49. A.K. Rappé and W.A. Goddard: Charge equilibration for molecular-dynamics simulations. J. Phys. Chem. 95, 3358 (1991).
50. M.J. Buehler, J. Dodson, P. Meulbroek, A. Duin, and W.A. Goddard: The computational materials design facility (CMDF): A powerful framework for multiparadigm multi-scale simulations, in Combinatorial Methods and Informatics in Materials Science, edited by M.J. Fasolka, Q. Wang, R.A. Potyrailo, T. Chikyow, U.S. Schubert, and A. Korkin (Mater. Res. Soc. Symp. Proc. 894, Warrendale, PA, 2006), p. 327.
51. J. Stone, J. Gullingsrud, P. Grayson, and K. Schulten: A system for interactive molecular dynamics simulation, in 2001 ACM Symposium on Interactive 3D Graphics, edited by J.F. Hughes and C.H. Sequin (ACM Press, New York, 2001), pp. 191-194.

J. Mater. Res., Vol. 21, No. 8, Aug 2006

---

M.J. Buehler: Atomistic and continuum modeling of mechanical properties of collagen: Elasticity, fracture, and self-assembly

52. W. Humphrey, A. Dalke, and K. Schulten: VMD: Visual molecular dynamics. J. Mol. Graphics 14, 33 (1996).
53. M.P. Allen and D.J. Tildesley, Computer Simulation of Liquids (Oxford University Press, New York, 1989).
54. F. Ercolessi and J.B. Adams: Interatomic potentials from 1st principle-calculations—the force matching method. Europhys. Lett. 28, 583 (1994).
55. S. Plimpton: Fast parallel algorithms for short-range molecular dynamics. J. Comput. Phys. 117, 1 (1995).
56. R.O. Ritchie, J.J. Kruzic, C.L. Muhlstein, R.K. Nalla, and E.A. Stach: Characteristic dimensions and the micro-mechanisms of fracture and fatigue in "nano" and "bio" materials. Int. J. Fract. 128, 1 (2004).

57. R.K. Nalla, J.J. Kruzic, J.H. Kinney, and R.O. Ritchie: Mechanistic aspects of fracture and R-curve behavior in human cortical bone. Biomaterials 26, 217 (2005).
58. R.K. Nalla, J.H. Kinney, and R.O. Ritchie: Effect of orientation on the in vitro fracture toughness of dentin: The role of toughening mechanisms. Biomaterials 24, 3955 (2003).
59. D.A. Pearlman, D.A. Case, J.W. Caldwell, W.S. Ross, T.E. Cheatham, S. Debolt, D. Ferguson, G. Seibel, and P. Kollman: AMBER, A package of computer-programs for applying molecular mechanics, normal-mode analysis, molecular dynamics and free-energy calculations to simulate the structural and energetic properties of molecules. Comput. Phys. Commun. 91, 1 (1995).

J. Mater. Res., Vol. 21, No. 8, Aug 2006
1961
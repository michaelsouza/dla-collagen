ELSEVIER

PII: S0021-9290(96)00151-0

J. Biomechanics, Vol. 30, No. 6, pp. 549–554, 1997
© 1997 Elsevier Science Ltd. All rights reserved
Printed in Great Britain
0021-9290/97 $17.00 + .00

# THE MECHANICAL PROPERTIES OF SIMULATED COLLAGEN FIBRILS

John Parkinson,* Andy Brass,* Giles Canova† and Yves Brechet†

* School of Biological Sciences, 2.205 Stopford Building, University of Manchester, Oxford Road, Manchester M13 9PT, U.K.; and † Laboratoire de Thermodynamique et Physico-Chimie Metallurgiques, ENSEEG, 1130 Rue de la Piscine, Domaine Universitaire, BP 75, 38402 Saint-martind'heres Cedex, France

Abstract—Previous theoretical studies of the mechanical properties of tissues such as skin, bone and tendon, have used approaches based on composite materials and have tended to neglect the contribution of individual microscopic components. In this paper, we examine the relationship between the fine structure of a collagen fibril and its relative tensile strength. Collagen is a fibrous protein which provides associated tissues with the majority of their tensile strength. It is present in the form of elongated structures termed fibrils which are created by the self-assembly of rod-like collagen molecules in an entropy-driven process termed fibrillogenesis. Mutations that alter the primary structure of the collagen molecule, interfere with this assembly process and can lead to the potentially fatal brittle bone disease, osteogenesis imperfecta. Here we investigate the mechanical properties of a range of computer-generated aggregates. The aggregates, created by the diffusion limited aggregation of rods, were subjected to a simple tensile test based on local rules of damage accumulation. In the test, core samples are 'extracted' from the aggregates, and the network of particles involved in the transmission of stress resolved. Increasing stress applied to the core leads to the removal of individual rods from this network; the tensile strength is determined from the force necessary to form a discontinuous network. Using this approach, we have shown that collagen fibril morphology is critical in determining its tensile strength. We suggest a possible mechanism to account for the increasing severity of osteogenesis imperfecta associated with the distance of mutation from the N-terminal of the collagen molecule. © 1997 Elsevier Science Ltd

Keywords: Collagen; Mechanical properties; Computer modeling.

# INTRODUCTION

Type I collagen is a fibrous protein which forms a major part of the extracellular matrix, providing a structural scaffold for other components. It is present in the form of elongated fibres (termed fibrils) in tissues such as skin, bone and tendon. Individual fibrils can be greater than 500 µm in length, 500 nm in diameter and contain more than 10⁷ molecules (Parry and Craig 1984). They form by the self-assembly of rod-like collagen molecules (~300 nm in length by 1.5 nm in diameter) in an entropy driven process termed fibrillogenesis (Kadler et al., 1987).

Mutations in the primary sequence of collagen molecules, are linked with a variety of heritable diseases including Ehlers-Danlos syndrome and osteogenesis imperfecta (OI). OI is typically characterised by brittle bones but may also involve other tissues rich in type I collagen to produce blue sclera, abnormal teeth, thin skin and weak tendons (Prockop and Kivirikko, 1995). These characteristics arise from mutations leading to changes in the structural characteristics of the collagen molecules. Interestingly, the severity of the disease phenotype appears to be related to the position of the mutation in

relation to the amino-terminal of the molecule (Byers and Steiner, 1992). What is not known is how these changes alter the mechanical properties of collagenous tissues.

Although collagen fibrils have little strength in either bending or torsion, the presence of covalent cross-links results in an ability to resist high tensile stresses (Parry, 1988). This allows them to act as reinforcing fibres in bone and to transmit stress in tissues such as skin and tendon. A number of experimental and theoretical studies of the mechanical properties of these tissues have already been undertaken (e.g. Katz, 1980; Okada et al., 1992; Woo et al., 1993). Such approaches have tended to treat the tissue as a homogenous composite in which the mechanical interactions between the matrix components and collagen fibrils at a microstructural level are neglected. Studies of cancellous bone, for example, have tended to model the tissue as a porous cellular composite material (Katz, 1980; Mammone and Hudson, 1993; Martin, 1991). In an attempt to determine how microscopic changes in tissue components may affect mechanical strength, this paper presents an investigation into the role of collagen fibril morphology.

Due to their relatively small size, it has not been possible to investigate the mechanical properties of individual collagen fibrils. Recently, however, a computer model of collagen fibril formation has been proposed which realistically simulates the formation of a range of different fibril morphologies (Parkinson et al., 1995). By applying ideas based on the fracture of disordered media,

Received in final form 8 August 1996.

Address correspondence to: Andy Brass, School of Biological Sciences, 2.205 Stopford Building, University of Manchester, Oxford Road, Manchester M13 9PT, U.K.

---

550
J. Parkinson et al.

it is possible to investigate the mechanical properties of these aggregates (Charmet et al., 1990; Decitres et al., 1994). Using such an approach, aggregates (represented by a network of undeformable nodes connected by elastic bonds) are subjected to random bond breaking processes which lead to their eventual fracture. During a typical simulation, a bond in the network is chosen and broken at random with a probability dependent on the force being applied to it. In the next step, the network is allowed to relax until it has attained a new mechanical equilibrium. The process then proceeds by a sequence of bond breaking and relaxation steps until the structure has failed.

It is hypothesised that changes in fibril morphology affect their ability to sustain a load and may therefore be responsible for the production of a range of disease phenotypes including OI. Previously, we have described a model which realistically simulates the formation of collagen fibrils (Parkinson et al., 1995). Here we apply local rules of damage accumulation to determine the tensile strength of these computer generated aggregates and show how the architecture of a fibril may influence its tensile strength.

## METHODS

The generation and subsequent analysis of the aggregates described in this paper were undertaken by computer simulation. Aggregates were generated by the diffusion limited aggregation of rods of size $18 \times 1 \times 1$ on a three-dimensional semi-hexagonal lattice. A seed rod was placed at the centre of the lattice. Rods were released at a large distance from the seed and allowed to move at random through the lattice (simulating brownian motion) until either:

1. They encountered a suitable site on the surface of the aggregate, in which case they adhered.
2. They moved twice the distance of release from the aggregate, in which case they were destroyed and a new rod released.

Rods were released parallel to the long plane of the lattice and were not allowed to rotate (to reflect the fact that collagen molecules always align in parallel). Simulations were run using collagen-specific rules of binding in which a suitable site on the surface of the lattice was one which led to an integral overlap of $D$ (where $D = 4$ lattice units). Surface diffusion was included in the model by allowing particles a certain amount of time, $T_{\mathrm{S}}$, to laterally explore the surface of the aggregate at random. After $T_{\mathrm{S}}$ trials (a trial being defined as a direction chosen at random whether or not it was rejected due to it allowing the rod to leave the aggregate surface) the rod was placed in that site which led to the creation of the least amount of surface. For a more detailed explanation see Parkinson et al. (1995). The aggregates were composed of 50,000 rods.

In order to assess the structural properties of these aggregates, a core of 'material' was extracted from the middle of each aggregate. In addition to measuring the density, $\rho$, of each core, the connectivity between the monomers within the cores was investigated by determining the active skeleton (defined as the series of inter-connecting blocks which are involved in the transmission of stress from the one end of the core sample to the other). For the aggregates created with lower values of $T_{\mathrm{S}}$, the number of particles in the active skeleton was found to be highly dependent upon the size of the core sample taken. Therefore, in order to minimise boundary effects, a core size of $200 \times 16 \times 16$ lattice units was used. The blocks in the skeleton are termed 'particles' and are individual occupied sites in the lattice (as opposed to a rod, used to model a collagen molecule, which consists of 18 such particles). The active skeleton was obtained using the following algorithm (see Fig. 1):

Firstly the core sample is divided into $16 \times 16$ sections and the particles in the first section ($x = 1$) initially is marked as 'connected'. In the following section ($x = 2$), particles adjacent to the 'connected' particles of the first section are similarly marked as 'connected'. In addition any particles neighbouring 'connected' particles in the same section are also marked. The process is then repeated for each of the following sections to obtain a branching network which connects both ends of the core. However, this process will also generate branches

![img-0.jpeg](img-0.jpeg)
Fig. 1. Diagram showing how the active skeleton of an aggregate core is obtained. (A) A core sample of size $200 \times 16 \times 16$ lattice units is obtained from the aggregate. (B) This is then divided into $16 \times 16$ lattice unit sections (occupied lattice sites being coloured grey). (C) In the first section ($x = 1$), all the particles are marked as connected (coloured black). In the next section ($x = 2$) all the particles connected to the black particles in the previous section are marked connected (coloured black). In addition, particles laterally adjacent to the connected particles are also marked as connected (cross-hatched). The process is repeated for each of the following sections. Particles which are not part of the active skeleton can be seen in the third section ($x = 3$) coloured grey. The process is then repeated in the opposite direction using only sites originally marked as connected. For a further explanation see text.

---

The mechanical properties of simulated collagen fibrils
551

which do not contribute to the transfer of stress across the whole section. To remove these redundant branches from the structure, the process of marking particles as 'connected' was undertaken in the reverse direction (i.e. starting at $x = 200$ and finishing at $x = 1$). During this process, only particles which were previously marked as 'connected' were used. Particles marked as 'connected' in both directions are those bearing the stress across the core sample and are therefore part of the active skeleton.

To determine the uniaxial tensile strength of the core samples, an increasing force was applied to the active skeletons until they failed. The application of a force, $F$, to the core samples, assesses two problems: how is stress distributed within the aggregate and what is the local criterion for fracture. It is clear that stress distribution and fracture are closely related. As stress is applied to a material, breaks occur where the stress is maximum leading to structural reorganisation and hence a novel stress distribution. For the purposes of this model, the following algorithm was used to determine the tensile strength of the core samples: the core is divided into layers of one lattice unit thickness. Mechanical equilibrium imposes that the load is constant along the sample. Therefore, an equipartition of stress was assumed for each element in a slice, $i$, of the core. For each slice, the number of particles in the active skeleton was $N(i)$. The stress, $\sigma(i)$, for each particle in this slice, may therefore be approximated by

$$
\sigma(i) = F / N(i). \tag{1}
$$

Imposing stress on the core sample leads to breakage of the interactions binding two laterally associated particles (termed bonds). Each particle is connected to $n$ neighbours in the skeleton, depending upon the local geometry. The strength of the bond between two laterally associated particles is denoted as $\sigma_{c}$ and is assumed to be constant. Therefore, the stress necessary to free a given particle is given by $n\sigma_{c}$. However, each particle is part of a rod assumed to behave as a collagen molecule. Due to the triple helical nature of these molecules, fracture within a collagen fibril will arise from the breakage of inter-molecular interactions rather than the collagen molecules themselves. Therefore, rather than assigning a probability of each particle being removed from the active skeleton, individual rods were assigned a probability, $P_{b}$, of removal from the skeleton. This probability was determined from the stress being placed on a rod, $\sigma$ (the average of the values of $\sigma(i)$ for the various slices containing the rod), and obtained from:

$$
P_{b} = \left(\sigma / n \sigma_{c}\right)^{m} \tag{2}
$$

where $m$ is a constant which describes the dispersion in the strength of interactions between two particles. This exponent is related to the Weibull modulus (Ashby and Jones, 1986): if $m$ is very large, fracture will be entirely deterministic, if $m$ is very small, fracture thresholds will occur over a wider range. The precise value of the Weibull modulus is normally obtained by experiment. However, since no such experiments have been undertaken on collagen fibrils, it is necessary to investigate

a range of different values for $m$ in order to assess its impact. $\sigma_{c}$, the typical strength of the bond between two particles, was chosen as unity and is the unit of stress with respect to the inter-particle interaction.

To determine the tensile strength of each core sample therefore, the active skeleton was assessed and a force, $F$, imposed on it. The stress in each particle was calculated and rods were removed with the probability given by [equation (2)]. To keep the model as simple as possible, the aggregates were assumed to be brittle. Hence, no deformation was allowed in the simulations and once rods were removed from the active skeleton, they did not reassociate. After the rods had been assessed and the appropriate particles removed, the skeleton was reassessed and the stress re-evaluated. The procedure was repeated, increasing $F$ (in increments of 0.5) only when no new breaking events occurred. For each value of $F$, the percentage of particles remaining in the active skeleton was calculated. While $F$ increases, this percentage decreases, the fracture of the aggregate occurring when no particles are left in the active skeleton. This simple procedure allows the computation of the tensile strength, $F_{c}$, of the fibril (i.e. the force at point of fracture).

# RESULTS

Figure 2 shows two aggregates containing 50,000 rods created with $T_{\mathrm{S}} = 1$ and $T_{\mathrm{S}} = 10,000$. Both aggregates clearly have a fibrillar morphology. However, the structure grown with $T_{\mathrm{S}} = 10,000$ is more compact than the aggregate grown with $T_{\mathrm{S}} = 1$. Figure 3 shows how the density, $\rho$, of core samples obtained for a range of aggregates increases with $T_{\mathrm{S}}$. The graph reveals an asymptotic relationship demonstrating a limit for the value of $T_{\mathrm{S}}$ above which aggregate morphology remains unaffected (i.e. only a finite amount of time is needed to completely explore the surface of the aggregate). In order to obtain more information about the structure of these cores, the degree of connectivity between the monomers within the cores was investigated by generating the active skeletons which bear the load across the cores.

Figure 4 shows the active skeletons in the core samples of the two aggregates displayed in Fig. 2. The active skeleton obtained from the aggregate created with $T_{\mathrm{S}} = 1$, appears to be a diffuse structure with many particles not being involved in the transmission of stress. In contrast, most of the particles in the core obtained from the aggregate created with $T_{\mathrm{S}} = 10,000$, pertain to the active skeleton which appears as a dense, continuous structure. The percentage of particles in the active skeleton was plotted against $T_{\mathrm{S}}$ (see Fig. 3). There is a clear correlation between $T_{\mathrm{S}}$ and the percentage of particles in the active skeleton. This percentage being a measure of the efficiency of the structure to bear the load.

In order to determine their relative tensile strengths, the core samples were fractured as outlined in Methods. Figure 5A shows graphs of the percentage of particles in the skeleton against applied force (calculated using $m = 2$) for a range of aggregates grown with different values of $T_{\mathrm{S}}$. Figure 5B shows the number of broken bonds against applied force for the same aggregate cores. The aggregate cores react to the stress by the breaking of

---

552
J. Parkinson et al.

![img-1.jpeg](img-1.jpeg)
Fig. 2. Three-dimensional views of aggregates created with different values of surface diffusion. The aggregates were composed of 50,000 rods. The colour of the rods indicate the time of arrival (pale rods being last to accrete). (A) and (B) $T_{\mathrm{S}} = 1$, (C) and (D) $T_{\mathrm{S}} = 10,000$.

![img-2.jpeg](img-2.jpeg)
Fig. 3. Graphs showing how the density and the number of particles in the active skeleton in a core of an aggregate, varies with the time of surface diffusion, $T_{\mathrm{S}}$.

![img-3.jpeg](img-3.jpeg)
Fig. 4. Diagrams showing the cores from the aggregates shown in Fig. 2. The active skeleton is shaded dark, particles which are not part of the active skeleton are shown as transparent pale rods. The cores have dimensions of $200 \times 16 \times 16$ lattice units. (A) and (C) $T_{\mathrm{S}} = 1$, (B) and (D) $T_{\mathrm{S}} = 10,000$.

bonds, the number of broken bonds therefore gives a measure of strain. Hence, if it is assumed that each broken bond is associated with an increase in plastic deformation, the curve shown in Fig. 5B is equivalent to a stress/strain curve for damage plasticity. The graphs suggest that as the time of surface diffusion, $T_{\mathrm{S}}$, increases, there is a corresponding increase in the force necessary to fracture the core samples (tensile strength). In addition there is an increase in the number of bonds which need to be broken. It may therefore be concluded that the strength of an aggregate is related to the amount of surface diffusion allowed during growth.

Figure 6A and B show similar graphs for different values of $m$ for an aggregate created with $T_{\mathrm{S}} = 10,000$. The graphs demonstrate that for the same structure of the aggregate, the tensile strength decreases dramatically when the stochastic aspect of fracture is increased ($m$ small). The local average fracture stress, $\langle \sigma \rangle$, may be written as:

$$
\langle \sigma \rangle = n \sigma_ {c} \frac {m + 1}{m + 2}
$$

As $m\Rightarrow \infty$, $\langle \sigma \rangle$ approaches $n\sigma_{c}$ whilst as $m\Rightarrow 0$, $\langle \sigma \rangle$ approaches $\frac{1}{2} n\sigma_{c}$ (3)

---

The mechanical properties of simulated collagen fibrils

![img-4.jpeg](img-4.jpeg)

![img-5.jpeg](img-5.jpeg)
Fig. 5. Graphs showing how the percentage of particles in the skeleton (A) and the number of broken bonds (B), varies with increase in force, $F$ with $m = 2$, for a range of aggregate cores created with different values of $T_{\mathrm{S}}$.

![img-6.jpeg](img-6.jpeg)

![img-7.jpeg](img-7.jpeg)
Fig. 6. Graphs showing how the percentage of particles in the skeleton (A) and the number of broken bonds (B), varies with increase in force, $F$ applied to an aggregate core created with $T_{\mathrm{S}} = 10,000$ for a range of different values of $m$.

![img-8.jpeg](img-8.jpeg)

![img-9.jpeg](img-9.jpeg)
Fig. 7. Summary of information comparing the critical force of fracture, $F_{c}$ with the fibril density (A) and the percentage of particles in the active skeleton (B) for five values of $m$. The results are standardised by the critical force of fracture for the aggregate grown using $T_{\mathrm{S}} = 10,000$.

This indicates that the average local fracture stress decreases by a half between $m = \infty$ and $m = 0$. However, from Fig. 6, the decrease in overall tensile strength is much faster. Therefore, fracture is not only affected by changes in the average local fracture stress. In addition there must be huge collective effects determined by the architecture of the fibril.

The information regarding the tensile strength of the fibrils is summarised in Fig. 7A and B. The critical force of fracture (giving a measure of tensile strength), $F_{\mathrm{c}}$, is compared with fibril density and the percentage of particles in the active skeleton for four different values of $m$. From the figure, it can be seen that the density of the aggregate is relatively important in determining the strength of the structures. However, the greatest contribution of tensile strength arises from the percentage of particles pertaining to the active skeleton, demonstrating the importance of fibril architecture in determining its strength.

# DISCUSSION

In this paper, we have described a model tensile test which was applied to a range of simulated collagen

---

554
J. Parkinson et al.

fibrils. Using this model we were able to explore the relationship between fibril morphology and mechanical strength. Although the model neglected elastic deformation, it was found to simulate several features of typical stress/mechanical loading situations. Taking the number of broken bonds as a measure of strain in the fibril, the plot of the number of broken bonds against force is equivalent to a stress/strain curve for damage plasticity. In addition, the model features a slow drop in the number of particles involved in the structural integrity of the aggregates until a critical force is applied at which point the aggregate fails. Results obtained from subjecting the aggregate structures to stress revealed that the denser fibrils were much more resistant to stress than the less dense fibrils. However, the greatest contribution to tensile strength was found to be the degree of connectivity within the fibril structure. As with other natural materials, the strength of the structure is therefore much more dependant upon its architecture than upon the strength of each individual bond (Gibson and Ashby, 1988).

From these results it is possible to gain some insights into the relationship between disease genotype and phenotype for mutations associated with brittle bone disease, osteogenesis imperfecta. In general, the severity of the disease phenotype is related to the position of the mutation in the triple helix (Byers and Steiner, 1992). In many cases, the mutation interrupts the normal processing of the collagen molecule, which as a result can become overglycosylated (Torre-Blanco et al., 1992). It is therefore postulated that as the site of mutation moves further from the N-terminus of the collagen molecule, so the collagen molecule becomes more overglycosylated. The presence of extra sugar residues on the collagen molecules may interfere with the normal assembly process, preventing further rearrangement of molecules on the aggregate surface (simulated by decreasing the time of surface diffusion, $T_{\mathrm{S}}$, during aggregate growth). This results in the formation of fibrils with decreased density and connectivity and hence tensile strength. Hence those mutations leading to the highest levels of glycosylation will lead to the most severe phenotypes. It should, however, be noted that mutations in the collagen structure may also alter other properties in the tissue such as the amount of collagen secreted by the cell and the ability of the collagen to interact with other matrix components. However, this study strongly suggests how genotype and disease phenotype may be related.

In addition to investigating the different material properties of collagen fibrils obtained from a range of tissues and organisms, the model could easily be adapted to simulate the mechanics of more complicated fibril structures such as fibres and osteons.

## REFERENCES

Ashby, M. F. and Jones, D. R. H. (1986) Engineering Materials 2: An Introduction to Microstructures, Processing and Design. Pergamon, Oxford.
Byers, P. H. and Steiner, R. D. (1992) Osteogenesis imperfecta. Ann. Rev. Med. 43, 269–282.
Charmet, J. C., Roux, S. and Guyon, E. (eds.) (1990) Disorder and Fracture. Plenum, New York.
Decitres, X. D., Brechet, Y., Kubin, L. P. and Braillon, P. (1994) Numerical modelling of the evolution of the architecture of trabecular bone — damage accumulation and failure. Modell. Sim. Mat. Engng 2, 135–146.
Gibson, L. J. and Ashby, M. F. (1988) Cellular Solids: Structure and Properties. Pergamon, Oxford.
Kadler, K. E., Hojima, Y. and Prockop, D. J. (1987) Assembly of collagen fibrils de Novo by the cleavage of the type I pC-collagen with procollagen C-proteinase. J. Biol. Chem. 260, 15, 696–15, 701.
Katz, J. L. (1980) The structure and biomechanics of bone. In The mechanical Properties of Biological Materials, eds J. F. V. Vincent and J. D. Currey, pp. 137–168. Cambridge University Press. Cambridge.
Mammone, J. F. and Hudson, S. M. (1993) Micromechanics of bone strength and fracture. J. Biomechanics 26, 439–446.
Martin, R. B. (1991) Determinants of the mechanical properties of bone. J. Biomechanics (suppl. 1) 24, 79–88.
Okada, T., Hayashi, T. and Ikada, Y. (1992) Degradation of collagen suture in vitro and in vivo. Biomaterials 13, 448–454.
Parkinson, J., Kadler, K. E. and Brass, A. (1995) Simple physical model of collagen fibrillogenesis based on diffusion limited aggregation. J. Mol. Biol. 247, 823–831.
Parry, D. A. D. (1988) The molecular and fibrillar structure of collagen and its relationship to the mechanical properties of connective tissue. Biophys. Chem. 29, 195–209.
Parry, D. A. D. and Craig, A. S. (1984) Growth and development of collagen fibrils in connective tissue. In Ultrastructure of the Connective Tissue Matrix, eds. A. Ruggeri and P. M. Motta, pp. 34–64. Martinus Nijhoff, Boston.
Prockop, D. J. and Kivirikko, K. I. (1995) Collagens: molecular biology, diseases and potentials for therapy. Ann. Rev. Biochem. 64, 403–434.
Torre-Blanco, A., Adachi, E., Hojima, Y., Wootton, J. A. M., Minor, R. P. and Prockop, D. J. (1992) Temperature-induced post-translational over-modification of type I procollagen. J. Biol. Chem. 267, 2650–2655.
Woo, S. L.-Y., Johnson, G. A. and Smith, B. A. (1993) Mathematical modelling of ligaments and tendons. J. Biomech. Engng Trans. ASME 115, 468–473.
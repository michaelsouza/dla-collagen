Check for updates

# Nature designs tough collagen: Explaining the nanostructure of collagen fibrils

Markus J. Buehler†

Department of Civil and Environmental Engineering, Massachusetts Institute of Technology, 77 Massachusetts Avenue, Room 1-272, Cambridge, MA 02139

Edited by L. B. Freund, Brown University, Providence, RI, and approved June 23, 2006 (received for review April 22, 2006)

Collagen is a protein material with superior mechanical properties. It consists of collagen fibrils composed of a staggered array of ultra-long tropocollagen (TC) molecules. Theoretical and molecular modeling suggests that this natural design of collagen fibrils maximizes the strength and provides large energy dissipation during deformation, thus creating a tough and robust material. We find that the mechanics of collagen fibrils can be understood quantitatively in terms of two critical molecular length scales  $\chi_{\mathrm{S}}$  and  $\chi_{\mathrm{R}}$  that characterize when (i) deformation changes from homogeneous intermolecular shear to propagation of slip pulses and when (ii) covalent bonds within TC molecules begin to fracture, leading to brittle-like failure. The ratio  $\chi_{\mathrm{S}} / \chi_{\mathrm{R}}$  indicates which mechanism dominates deformation. Our modeling rigorously links the chemical properties of individual TC molecules to the macroscopic mechanical response of fibrils. The results help to explain why collagen fibers found in nature consist of TC molecules with lengths in the proximity of  $300\mathrm{nm}$  and advance the understanding how collagen diseases that change intermolecular adhesion properties influence mechanical properties.

deformation | fracture | mechanics | tropocollagen | length scale

Materials found in nature often feature hierarchical structures ranging from the atomistic and molecular scales to macroscopic scales (1-5). Many biological materials found in living organisms, often protein-based, feature a complex hierarchical design.

Collagen, the most abundant protein on earth, is a fibrous structural protein with superior mechanical properties, and it provides an intriguing example of a hierarchical biological nanomaterial (4, 6-18). Collagen consists of tropocollagen (TC) molecules that have lengths of  $L \approx 280 \mathrm{~nm}$  and diameters of  $\approx 1.5 \mathrm{~nm}$ , leading to an aspect ratio of  $\approx 190$  (6, 7, 9, 18-20). Staggered arrays of TC molecules form fibrils, which arrange to form collagen fibers (Fig. 1).

Collagen plays an important role in many biological tissues, including tendon, bone, teeth, and cartilage (6, 7, 13, 15, 19, 21). Severe mechanical tensile loading of collagen is significant under many physiological conditions, as in joints and in bone (22, 23). Despite significant research effort over the past couple of decades, the geometry and typical length scales found in collagen fibrils, the deformation mechanisms under mechanical load, and, in particular, the relationship between those mechanisms and collagen's molecular and intermolecular properties, are not well understood. Moreover, the limiting factors of the strength of collagen fibrils and the origins of toughness remain largely unknown.

Some experimental efforts focused on the deformation mechanics of collagen fibril at nanoscale, including the characterization of changes of D-spacing and fibril orientation (18, 20, 24), analyses that featured x-ray diffraction (18) and synchrotron radiation experiments (19). Other experimental studies were focused on the averaged response of arrays of collagen fibrils, considering nanoscale deformation mechanisms (3).

However, most research has been focused on the macroscopic, overall mechanical properties of collagen fibers and scales beyond, for example, of tissues, often without explicitly considering the mo

![img-0.jpeg](img-0.jpeg)
Fig. 1. Schematic view of some of the hierarchical features of collagen, ranging from the amino acid sequence level at nanoscale up to the scale of collagen fibers with lengths on the order of  $10\mu \mathrm{m}$ . Here we focus on the mechanical properties of collagen fibrils consisting of a staggered array of TC molecules.

lecular nanoscale structure (21). Other studies focused on the properties of individual TC molecules without linking to the response of macroscopic materials (7, 9, 10, 25, 26).

To develop a fundamental and quantitative understanding of collagen mechanics, it is critical to develop theoretical models encompassing the mesoscopic scales between the atomistic and macroscopic levels. There exists no model that links the properties of individual molecules with the overall mechanical response of fibrils or fibers, considering the different types of chemical bonding and nanoscale mechanics and geometry. The role of the staggered structure and the reasons for the specific length scales and high aspect ratio of TC molecules remain unexplained.

An improved understanding of the nanomechanics of collagen may help in the development of biomimetic materials or for improved scaffolding materials for tissue engineering applications (27). Diseases such as Ehlers-Danlos (28), osteogenesis imperfecta, Scurvy, or the Caffey disease (29) are caused by defects in the molecular structure of collagen altering the intermolecular and molecular properties due to genetic mutations, which modifies the mechanical behavior of collagen fibrils.

Here we use a hierarchical multiscale modeling scheme based on atomistic and molecular simulation to describe the mechanical properties of collagen under large stretch, leading to permanent deformation or fracture. We show that the key to understanding the mechanics of collagen is to consider the interplay between the mechanics of individual TC molecules with characteristic length

www.pnas.org/cgi/doi/10.1073/pnas.0603216103

PNAS | August 15, 2006 | vol. 103 | no. 33 | 12285-12290

---

![img-1.jpeg](img-1.jpeg)

![img-2.jpeg](img-2.jpeg)

![img-3.jpeg](img-3.jpeg)

![img-4.jpeg](img-4.jpeg)
Fig. 2. Study of a BM assembly of TC molecules. (a) Simplistic model of a collagen fibril used to study the dependence of the BM fibril tensile strength  $F_{\mathrm{F}}$  on molecular length and adhesion strength. (b) The variation of  $F_{\mathrm{F}}$  due to changes of the adhesion strength [tensile strength normalized by  $F_{\mathrm{F}}(\tau_{\mathrm{shear}})$  and adhesion strength normalized by  $\tau_{\mathrm{shear}}$ , considering fully hydrated TC molecules without cross-links,  $\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &lt; 1$ ]. (c)  $F_{\mathrm{F}}$  as a function of molecular length [normalized by its maximum value  $F_{\mathrm{F}}(L / \chi_{\mathrm{S}} = 1)$ , for  $\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &lt; 1$ ]. At the critical molecular length  $(L / \chi_{\mathrm{S}} = 1)$ , the tensile force saturates, corresponding to a change from homogeneous shear to propagation of slip pulses. (d) The transition from homogeneous shear to brittle-like rupture of TC molecules, depicting  $F_{\mathrm{F}}$  and the dissipated energy (both normalized by reference values for  $\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &gt; 1$ ). Energy dissipation is maximized when  $L / \chi_{\mathrm{R}} = 1$ , when the transition from shear to molecular rupture occurs. (e) The effects for variations in cross-link density on the BM fibril strength (normalized by the strength of the cross-link-free BM fibril) for a collagen molecule with a length of 840 Å, assuming a regular distribution of cross-links. The BM fibril strength approaches a finite value for large cross-link densities.

![img-5.jpeg](img-5.jpeg)

scales, the intermolecular chemical interactions, and the mesoscopic properties arising from hundreds of molecules arranged in fibrils. We explore the mechanics of collagen by considering different nanostructural designs, and pay specific attention to the details of molecular and intermolecular properties and their impact on the mechanical properties.

# Results and Discussion

Under macroscopic tensile loading of collagen fibrils, the forces are distributed predominantly as tensile load carried by individual and as shear forces between different TC molecules (Fig. 1, fibrils). This model is similar to the shear-tension model suggested for bone (2, 3, 5, 17).

Energetic effects rather than entropic contributions govern the elastic and fracture properties of collagen fibrils and fibers. The fracture strength of individual TC molecules is largely controlled by covalent polypeptide chemistry. The shear strength between two TC molecules is controlled by weak dispersive and hydrogen bond interactions and by some intermolecular covalent cross-links.

Deformation Modes of Collagen Fibrils: Critical Molecular Length Scales. We first consider a simplistic model of a collagen fibril by focusing on a staggered assembly of two TC molecules (Fig. 2a). The shear resistance between two TC molecules, denoted  $\tau_{\mathrm{shear}}$ , leads to a contact length-dependent force,

$$
F _ {\text {t e n s}} = \tau_ {\text {s h e a r}} L _ {\mathrm {C}} = \alpha \tau_ {\text {s h e a r}} L, \tag {1}
$$

where  $L_{\mathrm{C}}$  is the contact length, and  $F_{\mathrm{tens}}$  is the applied force in the axial molecular direction, which can alternatively be expressed as

tensile stress  $\sigma_{\mathrm{tens}} = F_{\mathrm{tens}} / A_{\mathrm{c}}$  by considering the molecular cross-sectional area  $A_{\mathrm{c}}$ . The parameter  $\alpha$  describes the fraction of contact length relative to the molecular length,  $\alpha = L_{\mathrm{C}} / L$ . Because of the staggered geometry, the shear resistance increases linearly with  $L$ , thus  $F_{\mathrm{tens}} \sim \tau_{\mathrm{shear}} L$ . This model holds only if shear deformation between the molecules is homogeneous along the axial direction.

An alternative to homogeneous intermolecular shear is propagation of slip pulses due to localized breaking of intermolecular "bonds." In the spirit of Griffith's energy argument describing the onset of fracture, nucleation of slip pulses is controlled by the applied tensile stress  $\sigma_{\mathrm{R}}$ , where

$$
\sigma_ {\mathrm {R}} = \sqrt {2 E \gamma}, \tag {2}
$$

where  $E$  is Young's modulus of an individual TC molecule, and  $\gamma$  relates to the energy required to nucleate a slip pulse.

When  $\sigma_{\mathrm{tens}} &lt; \sigma_{\mathrm{R}}$ , deformation is controlled by homogeneous shear between TC molecules. However, when  $\sigma_{\mathrm{tens}} \geq \sigma_{\mathrm{R}}$ , intermolecular slip pulses are nucleated, which leads to a critical molecular length

$$
\chi_ {\mathrm {S}} = \frac {\sqrt {2 \gamma E}}{\tau_ {\text {s h e a r}} \alpha} A _ {\mathrm {C}}. \tag {3}
$$

For fibrils in which  $L &lt; \chi_{\mathrm{S}}$ , the predominant deformation mode is homogeneous shear. When  $L &gt; \chi_{\mathrm{S}}$ , propagation of slip pulses dominates. The strength of the fibril is then independent of  $L$  (Eq. 3), approaching  $\tau_{\mathrm{shear}} \alpha \chi_{\mathrm{S}}$ . This concept is somewhat similar to the flaw tolerance length scale proposed for mineral platelets in bone (2).

The length scale  $\chi_{\mathrm{S}}$  depends on the material parameters and interaction between molecules. If  $\gamma$  assumes very large values, for instance because of high cross-linking density or the effects of solvents (e.g., low water concentration), the tensile forces in each TC molecule (Eq. 1, or  $F_{\mathrm{tens}} \sim L$ ) reaches the tensile strength of TC molecules, denoted by  $F_{\mathrm{max}}$ , before homogeneous shear or slip pulses are nucleated. ( $F_{\mathrm{max}}$  is a material constant that ultimately depends on the molecular structure of the TC molecule, including the influence of the chemical environment, e.g., the presence of enzymes.)

Considering  $F_{\mathrm{tens}} = F_{\mathrm{max}}$  leads to a second critical molecular length scale,

$$
\chi_ {\mathrm {R}} = \frac {F _ {\mathrm {m a x}}}{\tau_ {\mathrm {s h e a r}} \alpha}. \tag {4}
$$

This molecular length  $\chi_{\mathrm{R}}$  characterizes when the transition from molecular shear to brittle-like rupture of individual TC molecules occurs. The response of collagen fibrils to mechanical load changes from shear or glide between TC molecules, to molecular fracture as  $L$  increases. For  $L &gt; \chi_{\mathrm{R}}$ , TC molecules break during deformation, whereas, for  $L \leq \chi_{\mathrm{R}}$ , deformation is characterized by homogeneous intermolecular shear.

The integrity of a complete collagen fibril is controlled by the strength of the weakest link. Thus, the interplay of the critical length scales  $\chi_{\mathrm{S}} / \chi_{\mathrm{R}}$  controls the deformation mechanism.

When  $\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &lt; 1$ , slip-pulse nucleation governs at large molecular lengths, whereas, when  $\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &gt; 1$ , fracture of individual TC molecules occurs. In both cases the strength does not increase by making  $L$  larger than  $\chi_{\mathrm{S}}$  or  $\chi_{\mathrm{R}}$ . The maximum strength of the fibril is reached at  $L = L_{\chi} = \min (\chi_{\mathrm{R}}, \chi_{\mathrm{S}})$ , which is true for any arbitrary length  $L$  of a TC molecule. For  $L / L_{\chi} &lt; 1$ , homogeneous intermolecular slip dominates deformation. For molecules with  $L &gt; L_{\chi}$  either slip pulses or fracture set in, depending on which of the two length scales  $\chi_{\mathrm{S}}$  or  $\chi_{\mathrm{R}}$  is smaller. For short TC molecules, the strength of collagen fibrils tends to be small and depends on  $L_{\mathrm{C}}$ . When  $L \sim L_{\chi}$ , the maximal tensile strength of fibrils is reached.

www.pnas.org/cgi/doi/10.1073/pnas.0603216103

Buehler

---

Furthermore, choosing $L \approx L_{\chi}$ leads to maximized energy dissipation during deformation. The work necessary to separate two fibers in contact along a length $L_{\mathrm{C}}$ under macroscopic tensile deformation is

$$
E _ {\text {d i s s}} = \int_ {l - 0} ^ {l - L _ {\mathrm {C}}} l \tau_ {\text {s h e a r}} d l = \frac {1}{2} L _ {\mathrm {C}} ^ {2} \tau_ {\text {s h e a r}}. \tag {5}
$$

Eq. 5 predicts an increase of the dissipated energy with increasing molecule length, therefore favoring long molecules. If $\chi_{\mathrm{R}} &lt; \chi_{\mathrm{S}}$, the critical length $L_{\chi}$ constitutes an upper bound for $L_{\mathrm{C}}$, because molecules rupture before shear deformation sets in. After bond rupture and formation of shorter molecules, $E_{\mathrm{diss}}$ decreases significantly, suggesting that $L &gt; L_{\chi}$ is not favored. Energy dissipation is at a maximum for $L \approx L_{\chi}$. If $\chi_{\mathrm{S}} &lt; \chi_{\mathrm{R}}$, the dissipated energy can be approximated (assuming $\mathrm{L_C} &gt; \chi_{\mathrm{S}}$) by

$$
E _ {\text {d i s s}} \approx \left(\frac {1}{2} \alpha^ {2} \chi_ {\mathrm {S}} ^ {2} \tau_ {\text {s h e a r}} + \left(L _ {\mathrm {C}} - \alpha \chi_ {\mathrm {S}}\right) \cdot F _ {\max }\right), \tag {6}
$$

suggesting that, after a quadratic increase for small molecular lengths, the dissipated energy increases linearly with $L_{\mathrm{C}}$.

Molecular Modeling of Bimolecular (BM) Assemblies. All simulations are carried out by using the mesoscopic molecular bead model of collagen. In the spirit of computational experiments (30, 31), we explore how different nanoscale designs and modifications in molecular properties influence the mechanical properties of collagen fibrils.

First, we focus on computational experiments of shearing an assembly of two TC molecules using steered molecular dynamics (see Fig. 2a) (32). The overlap $\alpha = 3/4$, according to x-ray diffraction analyses of collagen fibrils (18).

This BM model serves as a simplistic representation of the fibril microstructure. (Note that the strength of the BM fibril is reduced compared with a complete collagen fibril.) We use a reference (control) system of fully hydrated, cross-link-free fibril. Full atomistic modeling reveals that $F_{\mathrm{max}} \approx 24 \times 10^{3} \mathrm{pN}$ and $\tau_{\mathrm{shear}} \approx 5.55 \mathrm{pN} / \AA$, and $\chi_{\mathrm{R}} \approx 436 \mathrm{nm}$ for this case (see the supporting information, which is published on the PNAS web site).

Our objective is to demonstrate the dependence of the deformation mode (intermolecular shear, propagation of slip pulses, or brittle-like rupture) on the TC molecule length and adhesion strength between TC molecules.

Fig. 2b depicts the normalized BM fibril tensile strength for different values of the normalized adhesion strength, $\tau_{\mathrm{shear}}^{*} / \tau_{\mathrm{shear}}$, when $\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &lt; 1$. The adhesion strength $\tau_{\mathrm{shear}}^{*} = \mu \tau_{\mathrm{shear}}$, where $0 &lt; \mu &lt; 4$.

The results corroborate the predictions made by Eq. 1: The stronger the adhesion between two molecules, the larger the strength of a collagen fibril. Increased adhesion between TC molecules could be due to increased cross-linking density [for example, during aging (33)].

Fig. 2c shows the BM tensile strength as a function of variations of the molecular length $L / \chi_{\mathrm{S}}$ and for $\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &lt; 1$. In agreement with the considerations reported above, we find a transition in deformation mode from homogeneous shear between two TC molecules to a regime in which slip pulses are nucleated as $L$ is increased. Analysis of the molecular displacement fields shows the existence of slip pulses as proposed theoretically. The strength of the fibril approaches a finite value when $L &gt; \chi_{\mathrm{S}}$.

By considering the point of transition between homogeneous shear and slip pulses, we estimate $\chi_{\mathrm{S}}^{\mathrm{BM}} \approx 42 \mathrm{~nm}$. Therefore $\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &lt; 1$, indicating that either homogeneous shear or slip pulse propagation dominate deformation.

Fig. 2d depicts the transition from homogeneous shear to brittle-like rupture of TC molecules when $\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &gt; 1$. This condition is realized by modifying the properties of the mesoscale model to feature lower molecular fracture forces. ($r_{\mathrm{break}}$ is chosen at $14.5\AA$, which leads to a smaller value of $F_{\mathrm{max}}$; thus, $\chi_{\mathrm{R}}$ decreases to $\approx 250\AA$.) The plot depicts both the strength of the BM fibril and the dissipated energy. The dissipated energy is maximized when $L \approx \chi_{\mathrm{R}}$, in agreement with the theoretical model. Repeated fracture of TC molecules results in formation of a large number of smaller TC segments, leading to a reduction in strength.

Fig. 2e depicts how the tensile strength of BM fibrils depends on the cross-linking density. The BM fibril strength increases with larger cross-linking density but starts to saturate for cross-link densities beyond $0.01\AA^{-1}$. For larger cross-linking densities, the ratio $\chi_{\mathrm{S}} / \chi_{\mathrm{R}}$ changes to values larger than one and molecular rupture occurs.

The computational results corroborate the theoretical analysis reported above and confirm the existence of the two length scales and the interplay of dominating deformation modes characterized by the factor $\chi_{\mathrm{S}} / \chi_{\mathrm{R}}$.

Molecular Modeling of Mechanical Properties of Larger Collagen Fibrils. We now model the deformation behavior of a more realistic fibril geometry as shown in Fig. 1 (beside the label "fibril"), by studying the change in mechanical properties due to variations in molecule length $L$.

Because of the staggered design of collagen fibrils with an axial displacement of $\approx 25\%$ of the molecular length (18), the contact length between TC molecules in a fibril is proportional to $L$. The length scales suggested in Eqs. 3 and 4 therefore have major implications on the deformation mechanics of collagen fibrils.

We consider fully hydrated cross-link-free collagen fibrils serving as a model for cross-link-deficient collagen. Fig. 3 shows the stress versus strain response of a collagen fibril for different molecular lengths $L$. The results suggest that the onset of plastic deformation, the maximum strength, and large-strain mechanics of collagen fibrils depend on the molecular length.

Fig. 4a shows the normalized elastic strength of the fibril as a function of molecular length $L$. The results suggest an increase up to $\approx 200\mathrm{nm}$, then reaching a plateau value of $\approx 0.3\mathrm{GPa}$ (results normalized by this value). The elastic uniaxial strains of collagen fibrils reach up to $\approx 5\%$. The maximum stress reaches up to $0.5\mathrm{GPa}$ during plastic deformation.

The molecular length at which the saturation occurs corresponds to a change in deformation mechanism, from homogeneous shear $(L\rightarrow 0)$ to nucleation of slip pulses $(L\rightarrow \infty)$. The corresponding molecular length provides an estimate for the critical molecular length scale $\chi_{\mathrm{S}}\approx 200\mathrm{nm}$.

This length scale $\chi_{\mathrm{S}}$ is larger in the actual collagen fibril geometry compared with the simplistic BM model [see Molecular Modeling of Bimolecular (BM) Assemblies]. Unlike in the BM case, where loading is applied at the ends of the molecule, in the actual fibril geometry the distribution of shear forces along the molecular axis is more homogeneous. This change in boundary conditions generally favors homogeneous shear over slip-pulse nucleation. Furthermore, nucleation of slip pulses requires bending of the molecule and is therefore energetically more expensive because of geometric confinement due to the lattice-like arrangement in which different molecules are immediately neighboring other molecules (Fig. 1).

We note that $\chi_{\mathrm{R}} \approx 436 \mathrm{~nm}$, as described in the previous section (it is a material property of the reference system). Therefore, the ratio $\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &lt; 1$, suggesting a competition between slip pulses and homogeneous shear as the molecular length is varied. This result suggests that cross-link-deficient collagen may predominantly undergo intermolecular shear deformation.

Fig. 4b depicts the energy dissipated during deformation per unit volume. We observe a continuous increase with molecule length $L$, reaching a maximum at a critical molecular length $L_{\chi}$, then a slight decrease. Energy dissipation increases further at ultra-large molecular lengths beyond $400 \mathrm{~nm}$ because of longer

Buehler

PNAS | August 15, 2006 | vol. 103 | no. 33 | 12287

---

![img-6.jpeg](img-6.jpeg)
Fig. 3. Stress versus strain of a collagen fibril for different molecular lengths (model for cross-link-deficient collagen, because no covalent cross-links are present in the collagen fibril). The longer the molecular length, the stronger the fibril. The maximum elastic strength achieved by collagen fibrils approaches $\sim 0.3$ GPa, with the largest stress at $\sim 0.5$ GPa. The onset of intermolecular shear can be recognized by the deviation of the stress-strain behavior from a linear elastic relationship.

shear paths during slip-pulse propagation. The modest increase in energy dissipation for ultra-long molecules may be an inefficient solution, because assembling such ultra-long molecules into regular fibrils is challenging.

# Conclusion

Our results suggest that the length of TC molecules and strength of intermolecular interactions plays a significant role in determining the deformation mechanics, explaining some of the structural features of collagen found in nature.

The two length scales $\chi_{\mathrm{S}}$ and $\chi_{\mathrm{R}}$ provide a quantitative description of the three different deformation mechanisms in collagen fibrils: (i) intermolecular shear, (ii) slip-pulse propagation, and (iii) fracture of individual TC molecules (see Figs. 2-4).

The governing deformation mechanism is controlled by the ratio $\chi_{\mathrm{S}} / \chi_{\mathrm{R}}$: Whether molecular fracture ($\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &gt; 1$) or slip pulses ($\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &lt; 1$) dominate deformation, the strength of the fibril approaches a maximum at $L_{\chi} = \min (\chi_{\mathrm{R}}, \chi_{\mathrm{S}})$ that cannot be overcome by increasing $L$. When $L \approx L_{\chi}$, tensile forces due to shear are in balance with either the fracture strength of TC molecules ($\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &gt; 1$) or with the critical load to nucleate slip pulses ($\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &lt; 1$). In either case, the maximum strength of the fibril is reached when $L \approx L_{\chi}$, including maximum energy dissipation.

When the length of collagen molecules is close to the critical length scale $L_{\chi}$, two objectives are satisfied: (i) Under large deformation, TC molecules reach their maximum strength without leading to brittle fracture, and (ii) energy dissipation during deformation is maximized. This concept may explain the typical staggered geometry of collagen fibrils found in experiment with extremely long molecules, leading to large energy dissipation during deformation (Fig. 4).

The mechanisms of deformation and their dependence on the molecular design are summarized in a deformation map shown in Fig. 5.

Slip pulses are nucleated by localized larger shear stresses at the end of the TC molecules. Thus, cross-links at these locations provide a molecular-scale mechanism to prevent slip-pulse nucleation because this leads to an increase of the energy required to nucleate slip pulses and, thus, to a larger value of $\gamma$. This increase of $\gamma$ results in an increase of $\chi_{S}$ due to the scaling law

$$
\chi_ {\mathrm {s}} \sim \sqrt {\gamma}. \tag {7}
$$

![img-7.jpeg](img-7.jpeg)

![img-8.jpeg](img-8.jpeg)
Fig. 4. Elastic strength and energy dissipation of the collagen fibril. (a) The critical stress at the onset of plastic shear between TC molecules. An initial regime of linear increase of strength with molecular length is followed by a regime of finite strength at a plateau value. (b) The dissipated energy during deformation per unit volume in a collagen fibril as a function of molecular length normalized by the maximum value. An initial steep increase is followed by a plateau regime, with a local maximum of $\sim 220\mathrm{nm}$. The smooth curve is a fit of a third-order expansion to the simulation data.

As a consequence, the ratio $\chi_{\mathrm{S}} / \chi_{\mathrm{R}}$ increases, making collagen fibrils stronger. Remarkably, this nanoscale distribution of cross-links agrees with the natural collagen design seen in experiment, often showing cross-links at the ends of the TC molecules [reminiscent of crack bridging (23, 34)] (3-5).

Cross-links provide additional strength to the fibrils, in agreement with experiment (33). However, extremely large cross-link densities lead to negative effects because the material is not capable of dissipating much energy during deformation, leading to a brittle collagen that is strong but not tough. Such behavior is observed in dehydrated collagen or in aged collagen featuring higher cross-link density (33). In contrast, decreased crosslinking as it occurs in Ehlers-Danlos V disease (28, 29) leads to a significantly reduced tensile strength of collagen, as $\chi_{\mathrm{S}} / \chi_{\mathrm{R}} &lt; 1$. The ratio $L / L_{\chi}$ decreases, resulting in skin and joint hyperextensibility due to extremely weak collagen tissue incapable of dissipating significant energy.

Our model can be used to study different design scenarios. A design with many cross-links and short molecules would lead to a very brittle collagen, even in the hydrated state. Such behavior would be highly disadvantageous under physiological conditions. In contrast, long molecules provide robust material behavior with significant dissipation of energy (Fig. 4). Some experiments (19) support the notion that cross-link-deficient collagen shows wide yield regions and large plastic deformation, as seen in Fig. 4a.

Both elastic strength and energy dissipation approach a finite value for large molecular lengths, making it inefficient to create collagen fibrils with TC molecules much longer than $L_{\chi}$, which is on the order of a few hundred nanometers (Fig. 4). This length scale agrees somewhat with experimental results of TC molecules with lengths of $\approx 300 \mathrm{~nm}$ (6, 7, 9, 18-20).

Large deformation is a critical physiological condition for collagen-rich tissue. The risk of catastrophic brittle-like failure needs to be minimized to sustain optimal biological function. The nanoscale ultrastructure of collagen may be designed to provide robust material behavior under large deformation by choosing long TC molecules. Robustness is achieved by the

www.pnas.org/cgi/doi/10.1073/pnas.0603216103

Buehler

---

![img-9.jpeg](img-9.jpeg)
Fig. 5. Deformation map of collagen fibrils. The mechanical response is controlled by two length scales, $\chi_S$ and $\chi_R$. Intermolecular shear governs deformation for small molecular lengths, leading to a relatively small strength of the collagen fibril. For large molecular lengths, either intermolecular slip pulses ($\chi_S / \chi_R &lt; 1$) or rupture of individual TC molecules ($\chi_S / \chi_R &gt; 1$) dominate. The maximum strength and maximum energy dissipation of the collagen fibril is reached at a critical molecular length scale $L_c$ that is defined as the minimum $\chi_S$ and $\chi_R$. The regime $\chi_S / \chi_R &gt; 1$ refers to the case of strong intermolecular interactions (e.g., increased cross-link densities or due to the effects of solvents that effectively increase molecular adhesion). Physiological collagen typically features long molecules with variations in molecular interaction so that either intermolecular shear (e.g., slip pulses) or molecular fracture are expected to dominate.

design for maximum strength and maximized energy dissipation by shear-like mechanisms. The requirement for maximum energy dissipation (Eqs. 5 and 6) plays a crucial role in determining the optimal molecular length $L_{\mathrm{op}}$. The layered design of collagen fibrils plays a vital role in enabling long deformation paths with large dissipative stresses. This is reminiscent of the "sacrificial bond" concept that is known from other protein materials (5).

The properties of collagen are scale-dependent (19). The fracture strength of an individual TC molecule (11.2 GPa) differs from the fracture strength of a collagen fibril (0.5 GPa). Similarly, Young's modulus of an individual TC molecule is $\sim 7$ GPa, whereas Young's modulus of a collagen fibrils is smaller, approaching 5 GPa (for $L \approx 224$ nm). This decrease of Young's modulus is in qualitative agreement with experiment (20).

Quantitative theories of the mechanics of collagen have many applications, ranging from the development of new biopolymers to studies in tissue engineering for which collagen is used as a scaffolding material (27). In addition to optimization for mechanical properties, other design objectives, such as biological function, chemical properties, or functional constraints, may be responsible for the structure of collagen. However, the physiological significance of large mechanical deformation of collagen fibers suggests that mechanical properties could indeed be an important design objective.

# Materials and Methods

Slip-Pulse Nucleation and Propagation. This analysis is based on a one-dimensional model of fracture initially proposed by Hellan (35). The model describes a one-dimensional strip of material attached on a substrate that is under tensile loading in the axial direction. At a critical load, the energy released per advancement length of the adhesion front is equal to the energy required to break the bonding between the material strip and the substrate, leading to initiation of failure front. The failure front, corresponding to a dynamic crack tip, propagates at a fraction of the sound velocity,

eventually displacing the material permanently in the direction of the applied load.

We apply this model to intermolecular deformation in collagen fibrils. The energy release rate is given by

$$
G_0 = \frac{\sigma_{\mathrm{R}}^2}{2E}, \tag{8}
$$

where $E$ is Young's modulus of the TC molecule and $\sigma_{\mathrm{R}}$ is the applied tensile stress. With $\gamma$ as the energy necessary to nucleate this defect, at the onset of nucleation the condition

$$
G_0 = \gamma \tag{9}
$$

needs to be satisfied [similar to the Griffith condition (36)]. The detachment front corresponds to the front of decohesion. Combining Eqs. 8 and 9 and solving for $\sigma_{\mathrm{R}}$ leads to Eq. 2. Bonds behind the fracture front reform, thus forming a slip pulse. The slip pulse is a region with increased tensile strain in the TC molecule (several nanometers wide).

The existence of slip pulses is not a consequence of the discretization of the mesoscale model. Instead, this theoretical framework is developed based on continuum mechanics, assuming a homogeneous distribution of adhesive interactions along the molecular surface.

Reactive Mesoscopic Model. We use a reactive mesoscopic model describing TC molecules as a collection of beads interacting according to interparticle multibody potentials. The total energy is

$$
E = E_{\mathrm{T}} + E_{\mathrm{B}} + E_{\mathrm{weak}}. \tag{10}
$$

The bending energy is

$$
\phi_{\mathrm{B}}(\phi) = \frac{1}{2} k_{\mathrm{B}} (\phi - \phi_0)^2, \tag{11}
$$

with $k_{\mathrm{B}}$ relating to the bending stiffness of the molecule. We approximate the nonlinear stress-strain behavior under tensile loading with a bilinear model that has been used successfully in earlier studies of fracture (30, 31) (the function $E_{\mathrm{T}}$ is given by integrating $F_{\mathrm{T}}(r)$ over the radial distance). The force between two particles is

$$
F_{\mathrm{T}}(r) = - \partial \phi_{\mathrm{T}}(r) / \partial r, \tag{12}
$$

where

$$
\frac{\partial \phi_{\mathrm{T}}}{\partial r}(r) = H(r_{\text{break}} - r) \begin{cases} k_{\mathrm{T}}^{(0)}(r - r_0) &amp; \text{if } r &lt; r_1, \\ k_{\mathrm{T}}^{(1)}(r - \tilde{r}_1) &amp; \text{if } r \geq r_1. \end{cases} \tag{13}
$$

In Eq. 13, $H(r - r_{\mathrm{break}})$ is the Heaviside function $H(a)$, which is defined to be zero for $a &lt; 0$ and one for $a \geq 0$. The parameters $k_{\mathrm{T}}^{(0)}$ and $k_{\mathrm{T}}^{(1)}$ are the small- and large-deformation spring constants, respectively. The parameter $\tilde{r}_1 = r_1 - k_{\mathrm{T}}^{(0)} / k_{\mathrm{T}}^{(1)}(r_1 - r_0)$ from force continuity conditions.

Intermolecular interactions are described by a 12:6 Lennard-Jones potential

$$
\phi_{\mathrm{weak}}(r) = 4 \varepsilon \left( \left[ \frac{\sigma}{r} \right]^{12} - \left[ \frac{\sigma}{r} \right]^{6} \right), \tag{14}
$$

with $\sigma$ as the distance, and $\varepsilon$ as energy parameter.

The total energy is given by the sum over all pairwise and three-body interactions $\mathrm{I} = \{\mathrm{T}, \mathrm{weak}\}$:

$$
E_{\mathrm{I}} = \sum_{\text{pairs}} \phi_{\mathrm{I}}(r) \quad \text{and} \quad E_{\mathrm{B}} = \sum_{\text{angles}} \phi_{\mathrm{B}}(\phi). \tag{15}
$$

Buehler

PNAS | August 15, 2006 | vol. 103 | no. 33 | 12289

---

The parameters are calculated directly from full atomistic results, without empirical fitting. The parameters of the mesoscopic model are summarized in Table 1 for the reference state of fully hydrated TC molecules (for further details, particularly with regard to how the parameters of the molecular model are determined based on reactive and nonreactive atomistic simulations of individual TC molecules, see the supporting information).

Intermolecular cross-links are modeled by a harmonic spring, with $F_{\mathrm{XL}}(r) = -\partial \phi_{\mathrm{XL}}(r) / \partial r = -H(r - r_{\mathrm{break,XL}})k_{\mathrm{XL}}(r - r_{0,\mathrm{XL}})$. The numerical values are chosen to yield a cross-link strength of $\approx 2,110~\mathrm{pN}$ (37). We assume an equidistant distribution of $N_{\mathrm{CL}}$ cross-links along $L_{c}$. Different choices for $N_{\mathrm{CL}}$ lead to different cross-link densities $\rho_{\mathrm{N}} = N_{\mathrm{CL}} / L_{c}$.

We consider a two-dimensional model of collagen fibrils with periodic boundary conditions in the in-plane direction orthogonal to the pulling orientation.

Modeling Procedure. Simulations are carried out in two steps, (i) relaxation followed by (ii) loading. Relaxation is achieved by slowly heating up the system, then annealing the structure at constant temperature, followed by energy minimization. After relaxation, the structure displays the characteristics of collagen fibrils in agreement with experiment (4, 6-19).

For the simulations with single TC molecules and two TC molecules, we use force boundary conditions in a steered molecular dynamics scheme. For collagen fibrils, we use displacement boundary conditions, continuously displacing particles in the boundary. The simulations are carried out by constantly minimizing the potential energy as the external strain is applied.

We use the virial stress to calculate the stress tensor (38). Further details are provided in the supporting information.

Computing Techniques and Computational Laboratory. The molecular simulations described here were carried out with an extended version of the LAMMPS MD code (39), compiled with a GNU C++ compiler (LINUX; RedHat, Raleigh, NC) at the Atomistic Mechanics Modeling Laboratory (Massachusetts Institute of Technology). Visualization is done with visual molecular dynamics software (VMD) (40).

M.J.B. thanks Yu Ching Yung (Harvard University, Cambridge, MA) for helpful discussions on biological materials in general and W. A. Goddard and A. van Duin (both at California Institute of Technology, Pasadena, CA) for discussions related to reactive force fields and implementation. M.J.B. was supported by the Department of Civil and Environmental Engineering of Massachusetts Institute of Technology.

Table 1. Summary of the parameters used in the mesoscopic molecular model, chosen based on full atomistic modeling of solvated TC molecules (1 kcal·mol⁻¹·Å⁻¹ = 69.479 pN)

|  Parameters | Value  |
| --- | --- |
|  Equilibrium bead distance $r_0$, Å | 14.00  |
|  Critical hyperelastic distance $r_1$, Å | 18.20  |
|  Bond breaking distance $r_{\text{break}}$, Å | 21.00  |
|  Tensile stiffness parameter $k_1^{(0)}$, kcal·mol⁻¹·Å⁻² | 17.13  |
|  Tensile stiffness parameter $k_1^{(1)}$, kcal·mol⁻¹·Å⁻² | 97.66  |
|  Cross-link tensile stiffness parameter $k_{\text{XL}}$, kcal·mol⁻¹·Å⁻² | 17.00  |
|  Cross-link equilibrium distance $r_{\text{XL}}$, Å | 18.00  |
|  Cross-link bond breaking distance $r_{\text{break,XL}}$, Å | 19.80  |
|  Equilibrium angle $\varphi_0$, ° | 180.00  |
|  Bending stiffness parameter $k_B$, kcal·mol⁻¹·rad⁻² | 14.98  |
|  Dispersive parameter $\varepsilon$, kcal/mol | 6.87  |
|  Dispersive parameter $\sigma$, Å | 14.72  |
|  Mass of each mesoscale particle, atomic mass units | 1,358.7  |

1. Arzt, E., Gorb, S. &amp; Spolenak, R. (2003) Proc. Natl. Acad. Sci. USA 100, 10603-10606.
2. Gao, H., Ji, B., Jäger, I. L., Arzt, E. &amp; Fratzl, P. (2003) Proc. Natl. Acad. Sci. USA 100, 5597-5600.
3. Gupta, H. S., Wagermaier, W., Zickler, G. A., Aroush, D. R. B., Funari, S. S., Roschger, P., Wagner, H. D. &amp; Fratzl, P. (2005) Nano Lett. 5, 2108-2111.
4. Jager, I. &amp; Fratzl, P. (2000) Biophys. J. 79, 1737-1746.
5. Peterlik, H., Roschger, P., Klaushofer, K. &amp; Fratzl, P. (2006) Nat. Mater. 5, 52-55.
6. Bozec, L. &amp; Horton, M. (2005) Biophys. J. 88, 4223-4231.
7. Bhattacharjee, A. &amp; Bansal, M. (2005) IUBMB Life 57, 161-172.
8. Anderson, D. (2005) Ph.D. thesis (Univ. of Toronto, Toronto, Canada).
9. Sun, Y. L., Luo, Z. P., Fertala, A. &amp; An, K. N. (2004) J. Biomech. 37, 1665-1669.
10. An, K. N., Sun, Y. L. &amp; Luo, Z. P. (2004) *Biorheology* 41, 239-246.
11. Lees, S. (2003) Biophys. J. 85, 204-207.
12. Sun, Y. L., Luo, Z. P., Fertala, A. &amp; An, K. N. (2002) Biochem. Biophys. Res. Commun. 295, 382-386.
13. Hellmich, C. &amp; Ulm, F. J. (2002) J. Biomech. 35, 1199-1212.
14. Waite, J. H., Qin, X. X. &amp; Coyne, K. J. (1998) Matrix Biol. 17, 93-106.
15. Borel, J. P. &amp; Monboisse, J. C. (1993) C. R. Seances Soc. Biol. Ses Fil. 187, 124-142.
16. Lees, S. (1987) Int. J. Biol. Macromol. 9, 321-326.
17. Fratzl, P., Gupta, H. S., Paschalis, E. P. &amp; Roschger, P. (2004) J. Mater. Chem. 14, 2115-2123.
18. Hulmes, D. J. S., Wess, T. J., Prockop, D. J. &amp; Fratzl, P. (1995) Biophys. J. 68, 1661-1670.
19. Puxkandl, R., Zizak, I., Paris, O., Keckes, J., Tesch, W., Bernstorff, S., Purslow, P. &amp; Fratzl, P. (2002) Philos. Trans. R. Soc. London Ser. B 357, 191-197.
20. Sasaki, N. &amp; Odajima, S. (1996) J. Biomech. 29, 1131-1136.
21. Bozec, L., de Groot, J., Odlyha, M., Nicholls, B., Nesbitt, S., Flanagan, A. &amp; Horton, M. (2005) Ultramicroscopy 105, 79-89.

22. Nalla, R. K., Kruzic, J. J., Kinney, J. H. &amp; Ritchie, R. O. (2005) Biomaterials 26, 217-231.
23. Ritchie, R. O., Kruzic, J. J., Muhlstein, C. L., Nalla, R. K. &amp; Stach, E. A. (2004) Int. J. Fract. 128, 1-15.
24. Orgel, J. P. R. O., Irving, T. C., Miller, A. &amp; Wess, T. J. (2006) Proc. Natl. Acad. Sci. USA 103, 9001-9005.
25. Lorenzo, A. C. &amp; Caffarena, E. R. (2005) J. Biomech. 38, 1527-1533.
26. Vesentini, S., Fitie, C. F., Montevecchi, F. M. &amp; Redaelli, A. (2005) Biomech. Model. Mechanobiol. 3, 224-234.
27. Yung, Y. C. &amp; Mooney, D. J. (2006) in CRC Biomedical Engineering Handbook, ed. Bronozino, J. D. (CRC, Boca Raton, FL), chap. 6, pp. 1-14.
28. Lichten, J. R., Martin, G. R., Kohn, L. D., Byers, P. H. &amp; McKusick, V. A. (1973) Science 182, 298-300.
29. Glorieux, F. H. (2005) J. Clin. Invest. 115, 1142-1144.
30. Buehler, M. J. &amp; Gao, H. (2006) Nature 439, 307-310.
31. Buehler, M. J., Abraham, F. F. &amp; Gao, H. (2003) Nature 426, 141-146.
32. Nelson, M. T., Humphrey, W., Gursoy, A., Dalke, A., Kale, L. V., Skeel, R. D. &amp; Schulten, K. (1996) Int. J. Supercomput. Appl. High Perform. Comput. 10, 251-268.
33. Bailey, A. J. (2001) Mech. Ageing Dev. 122, 735-755.
34. Nalla, R. K., Kinney, J. H. &amp; Ritchie, R. O. (2003) Biomaterials 24, 3955-3968.
35. Hellan, K. (1984) Introduction to Fracture Mechanics (McGraw-Hill, New York).
36. Griffith, A. A. (1920) Phil. Trans. R. Soc. London Ser. A 221, 163-198.
37. Lantz, M. A., Hug, H. J., Hoffmann, R., van Schendel, P. J. A., Kappenberger, P., Martin, S., Baratoff, A. &amp; Guntherodt, H. J. (2001) Science 291, 2580-2583.
38. Tsai, D. H. (1979) J. Chem. Phys. 70, 1375-1382.
39. Plimpton, S. J. (1995) J. Comp. Phys. 117, 1-19.
40. Humphrey, W., Dalke, A. &amp; Schulten, K. (1996) J. Mol. Graphics 14, 33-38.

www.pnas.org/cgi/doi/10.1073/pnas.0603216103

Buehler
# Deformation and failure of protein materials in physiologically extreme conditions and disease

Markus J. Buehler, Yu Ching Yung

## Abstract

Biological protein materials feature hierarchical structures that make up a diverse range of physiological materials. The analysis of protein materials is an emerging field that uses the relationships between biological structures, processes and properties to probe deformation and failure phenomena at the molecular and microscopic level. Here we discuss how advanced experimental, computational and theoretical methods can be used to assess structure--process--property relations and to monitor and predict mechanisms associated with failure of protein materials. Case studies are presented to examine failure phenomena in the progression of disease. From this materials science perspective, a de novo basis for understanding biological processes can be used to develop new approaches for treating medical disorders. We highlight opportunities to use knowledge gained from the integration of multiple scales with physical, biological and chemical concepts for potential applications in materials design and nanotechnology.

## Keywords

Biological, Chemical, Molecular, Molecular, Molecular

## Proteins are essential building blocks of life, forming a diverse group of biological materials that ranges from spider silk to bone, and from tendons to the skin, all of which play an important part in providing key biological functions1-7. These materials are distinct from the conventional categories of structure and material, as they represent the merger of these two concepts through hierarchical formation of structural elements that range from the nanoscale to the macroscale (Fig. 1a, b).

Protein materials are abundant in biology and play an essential part in the biological function of all cells and tissues within organisms. Many such materials with mechanical function form structural filaments, trusses or fibres, whereas others retain the globular structure of their protein constituents. Biological protein materials are commonly characterized by where they reside with respect to their associated tissue, to serve as either extracellular or intracellular protein materials1. Intracellular protein materials provide the architecture of a cell and include vimentin, microtubules, actin (proteins from a cell's cytoskeleton) and lamins (forming the cell's nuclear envelope)1-3. Extracellular protein materials, secreted by cells into the surrounding microenvironment, include elastin and collagen1,4,5. Other protein materials such as fibrin6-9 appear in biological processes such as the clotting of blood. Distinct protein materials in organisms cannot be considered in isolation. For instance, lamins are connected to extracellular protein materials (such as collagen) through cytoskeletal proteins (for example actin and nesprin).

Here we focus on defining structural components of biological protein materials from a materials science perspective, and on their role in mechanical materials phenomena, specifically materials failure, in diseased or altered physiological conditions. Advances in experimental, theoretical and computational materials science have led to a deeper understanding through the linking of structure to process and property (Fig. 1c). An overview of failure in biological systems, broadly defined as the loss of its ability to provide an intended physiological function, will be specifically presented in the context of material breakdown due to a range of causes, including altered chemical or physical boundary conditions (such as extreme forces), weakening of tissues due to structural flaws because of genetic defects, or the inability of a tissue to provide its function because of the interaction with an ectopic or foreign material.

Within the biological sciences, the field of genomics has advanced our knowledge base through the successful sequencing of entire genomes. Extensive efforts have been made to move beyond genomics, where fields such as systems biology provide explanations of mechanisms of how genes affect phenotypes and biological function10,11. More recently, a movement to understand the materials science of proteins, aimed at developing relationships between structure (of biological protein materials), process (for example self assembly) and property (for example strength or elasticity), shows great promise in contributing to a deeper understanding of biological systems. This study of material properties of hierarchical protein structures and their effect on molecular and microscopic properties, by using mechanistic insight based on structure--process--property relations in the biological context (Fig. 1d), provides a basis for understanding disease processes. This could help in developing new approaches to treating genetic and infectious diseases, injury and trauma, as well as in improving engineered materials by translating material concepts from biology. Associated materials science challenges and opportunities are summarized in Table 1.

Materials in biology often involve non-protein components such as crystal platelets (in bone, dentin and nacre, for example), which have important effects on their mechanical properties. They also contain larger-scale structural features, which influence the overall mechanical properties (for example porosities and interaction with fluids). Although proteins are an important element that affects most materials in biology, they alone do not provide the information necessary to characterize all relevant material properties. The discussion of these effects is beyond the scope of this review.

The cascaded arrangements of building blocks at defined length scales form hierarchical structures (for example molecules, filaments, mesoscale structures) which control a material's properties. Figure 1a, b shows the structure of two example materials, showing lamin intermediate filaments (in the following referred to as ‘lamins')12-15 and collagen (for example tendon and cornea)4,5, and illustrates how structure and material converge.

---

REVIEW ARTICLE

NATURE MATERIALS DOI: 10.1038/NMAT2387

![img-0.jpeg](img-0.jpeg)

![img-1.jpeg](img-1.jpeg)

![img-2.jpeg](img-2.jpeg)

![img-3.jpeg](img-3.jpeg)
Figure 1 | Examples of hierarchical multiscale structures of biological protein materials. Here we show lamin intermediate filaments (lamins), collagenous tissues (tendon) and the materials science paradigm for the analysis of biological protein materials. a, Structure of lamins.  $\alpha$ -Helical protein domains assemble into dimers, which form filaments that define a lattice-like lamin network of the cell's nucleus. Lamina mesh network snapshot adapted and reprinted with permission from ref. 16. © 1986 NPG. Cell nucleus image ©TenOfAllTrades. b, Structure of collagenous tissues, from nanoscale to macroscale. Tropocollagen (TC) molecules assemble to form fibrils, which form fibres that provide the structural basis of collagen tissues such as tendon. Collagen fibril image reprinted with permission from ref. 76. © 2002 Elsevier. Image of Achilles tendon from SPL. c, Materials science triangle that links structure, process and property. d, Materials science paradigm applied to the hierarchical structure of protein materials (H, refers to hierarchy levels  $i = 0$  to  $N$ , R, refers to material property requirements at hierarchy levels  $i = 0$  to  $N$ ). The cycle initiates at  $\mathsf{H}_0$  (process  $\mathsf{H}_0$ , the only level at which protein expression occurs) to form protein constituents (structure  $\mathsf{H}_0$ ). Their properties (property  $\mathsf{H}_0$ ) control the association at the next hierarchical level (process  $\mathsf{H}_i$  leading to structure  $\mathsf{H}_i$ ). This cycle continues through all hierarchical levels  $i = 0$  to  $N$ , where process and structure  $\mathsf{H}_i$  and beyond denote protein assembly stages. At each stage, the properties of the structure control the assembly at the next level. Overall, properties at different hierarchical levels (properties  $\mathsf{H}_i$ ) are regulated by corresponding physiological demands (requirements  $\mathsf{R}_i$ ), which are sensed and transduced intracellularly to activate genetic regulation, resulting in changes to process  $\mathsf{H}_0$ .

Lamins provide structural support to the cell's nucleus and form an interface between the cell's cytoskeleton and chromatin. Figure 1a shows the structure of lamins $^{12-15}$ , characterized by a hierarchical assembly of  $\alpha$ -helix-based protein domains. The basic building block of lamins is an  $\alpha$ -helical coiled-coil dimeric molecule. Lamin dimers form filaments that develop into a network with a lattice-like structure, found primarily at a cell's nuclear membrane $^{16}$ . Because the cell's cytoskeleton itself is coupled to the surrounding extracellular matrix (for example collagen) by adhesion proteins, macroscopic deformation of tissues typically leads to deformation of the cell nucleus $^{17-20}$ . The lamin network thus aids the coupling of tissue-level mechanical signals to complex biochemical processes (such as gene regulation) within the cell nucleus $^{16,17,21,22}$ . The study

of strain-regulated mechanisms of cell response falls broadly into the field of mechanotransduction $^{3,23}$ . Lamins represent a model material that illustrates the intimate connection between structural material and biochemical properties. Recent studies have provided substantial evidence that underlines the role of lamins in cancer and genetic diseases $^{17,21,22,24}$ .

Collagen, the most abundant protein on the Earth, is a fibrous structural protein with superior mechanical properties. It is found in a number of tissues exposed to severe tensile or compressive loading, including tendon, bone, teeth, cartilage and the cornea $^{4,25-29}$ . The hierarchical structure of collagen is summarized in Fig. 1b. Collagen consists of triple helical tropocollagen molecules that appear as 'nano-ropes' with lengths of around  $300~\mathrm{nm}$  (ref. 30). Staggered

NATURE MATERIALS | VOL 8 | MARCH 2009 | www.nature.com/naturematerials

---

NATURE MATERIALS DOI:10.1038/NM412387

REVIEW ARTICLE

Table 1 | Key materials science challenges associated with the study of biological protein materials, examples and opportunities for further development of methods.

|  Materials science challenge | Example | Significance | Need for model development  |
| --- | --- | --- | --- |
|  Confinement effects | Change of material properties at different length scales and timescales (for example size effects, pulling rate effects) | Adaptation of universal or diverse protein structures, biomaterials | Constitutive material models with explicit consideration of hierarchies  |
|  Environmental effects | Effects of chemicals and solvent (for example pH) on formation, function and material breakdown | Tissue remodelling, protein filament adaptation/remodelling, mechanotransduction (chemomechanical signalling) | Chemomechanical models of tissues, atomistic-level descriptions that integrate mechanics and chemistry  |
|  Material failure | Material degradation in genetic and infectious diseases, failure due to impact and stress in injuries or trauma | Mechanisms of genetic diseases (for example osteogenesis imperfecta, progeria, muscle dystrophies, Alzheimer's disease), nanomedicine | Constitutive strength models with explicit consideration of hierarchies, plasticity/failure models (for example rupture of hydrogen bonds), disease models (such as role of molecular defects and misfolds)  |
|  Multiscale synthesis or fabrication | Structure control, from nanoscale to macroscale; how to control implementation of hierarchies | Synthesis of synthetic biofibres (such as spider silk) and bioinspired or biomimetic materials (scaffolding protein materials for tissue engineering, interfaces between microdevices and biological systems) | Integration of universal and diverse elements in hierarchical structures, translation from biology to nanotechnology (carbon nanotubes, nanowires, peptides)  |
|  Multiscale characterization | Structure measurement at various timescales and length scales (for example assembly stages), characterization of mechanisms of deformation | Application of atomic force microscopy, optical/magnetic tweezers, microfluidic devices, transmission electron microscopy for material characterization, integration of measuring and imaging approaches across multiple scales to aid model development | Statistical analysis, high-throughput methods, error/uncertainty analysis  |

arrays of tropocollagen molecules form fibrils, which combine to form collagen fibres and then to form tissues such as tendon, which functions as glue between muscle and bone. Tropocollagen molecules show extreme extensibility, withstanding up to  $50\%$  tensile strain before catastrophic failure. This, along with their ability to sustain stresses of several gigapascals, is crucial for their physiological mechanical role in tissues[31]. The staggered arrangement of molecules into fibrils provides the basis for its ability to dissipate mechanical energy through molecular sliding rather than leading to catastrophic failure[32-34]. This staggered architecture plays a key part in increasing the toughness of various collagen materials such as tendon or bone. The overall hierarchical arrangement is important because, through structures formed at characteristic geometric length scales, it enables superior molecular properties to be visible at larger, biologically important, intermediate mesoscales. A possible concept to explain the observed length scales at each hierarchical level is that they are a result of structural adaptation towards maximizing target material properties (such as strength and dissipation) through geometric size effects, as discussed in the context of bone[35]. Several genetic diseases are related to defects in the collagen structure, leading to mechanically compromised tissues (an example is the brittle bone disease osteogenesis imperfecta).

The biological materials introduced above feature properties that are characteristic for this entire class of materials, including robustness, adaptability and multifunctionality $^{4,11}$ . Robustness is defined as the degree of separation between stability and failure, and is crucial to understanding the role of protein materials in biology, for both physiological and pathological conditions (such as varying pH, forces or structural changes). Adaptability refers to the ability of a material to cope with environmental changes by changing its structural arrangement to cope better with changed conditions. For example, tissue remodelling in bone plays a crucial part in improving the material's damage tolerance through its

intrinsic ability to repair itself $^{36}$ . The underlying mechanism is that small cracks, formed because of physiological mechanical load, are detected by 'bone remodelling units' and removed from the tissue before they reach a critical size at which catastrophic failure would occur. Such mechanisms show the intricate connections between tissue formation and overall failure properties. In vivo, the structures of protein materials self-maintain or adapt by means of feedback loops by translating spontaneous demands in the microenvironment (through intracellular signalling) to regulate gene activation or deactivation. Ultimately, this alters the material's structural makeup to better suit the local physiological needs (Fig. 1d). Multifunctionality refers to the material's ability to provide multiple functions such as mechanical strength and the ability to control biochemical processes (as observed in lamins that have structural as well as biochemical roles). Many protein materials show graceful degradation, reflecting the material's ability to induce a controlled breakdown of a system's function after damage without leading to catastrophic failure and without affecting materials in the environment. The hierarchical structure may be the basis for these unique properties, distinguishing them from many engineered materials.

The formation of protein materials in biological systems occurs through self assembly of protein molecules whose structure is encoded in an organism's DNA. Protein molecules are composed of long polymer chains, constructed of amino acid monomers, and synthesized by a translation process that converts the genetic information transcribed from DNA into RNA into a polypeptide sequence of amino acids. Protein synthesis is initiated at precise sites during mRNA translation and terminated when signalled by the presence of encoded stop codons (messages). Once a protein molecule is constituted, the polypeptide chain folds into its unique three-dimensional (3D) conformation with the aid of chaperone proteins $^{1}$ . Functional activation of the protein structure often involves binding with other molecules to form the protein's intended

NATURE MATERIALS | VOL 8 | MARCH 2009 | www.nature.com/naturematerials

---

REVIEW ARTICLE

NATURE MATERIALS DOI: 10.1038/NMAT2387

![img-4.jpeg](img-4.jpeg)
a

![img-5.jpeg](img-5.jpeg)
b

![img-6.jpeg](img-6.jpeg)
c

![img-7.jpeg](img-7.jpeg)
d

![img-8.jpeg](img-8.jpeg)
e
Figure 2 | Formation and assembly of biological protein materials, including cellular expression of proteins and assembly into larger-scale hierarchical structures. a, Generation of protein molecules through translation from the DNA genetic code, leading to the expression of individual 3D protein molecules. b, Schematic biological assembly of lamins $^{16}$  and experimental visualization. The self assembly of protein molecules into large-scale structures proceeds through a complex process that involves several intermediate structural steps. For lamins, assembly occurs first by association of two dimers into tetramers, then by a period of growth in the axial direction (I), followed by growth in the radial direction (II and III). Experimental visualizations of the assembly process of lamins are obtained from electron microscopy studies (rat liver lamin A/C, scale bar  $100\mathrm{nm}$ ). Adapted and reprinted with permission from ref. 14. © 2004 Annual Reviews. c, Experimental visualization of the assembly of tropocollagen into collagen microfibrils based on contact-mode atomic force microscopy height images. The characteristic regular-spaced banding structure of collagen microfibrils is visible in the marked region where multiple tropocollagen molecules begin to interact (black, 0 nm height, white, 35 nm height). Adapted and reprinted with permission from ref. 76. © 2002 Elsevier. d, Schematic diagram of the biological process of formation of spider silk protein filaments in a spider's spinning duct, involving a controlled change of pH, solvent chemicals and mechanical shear, leading to the formation of the  $\beta$ -sheet-rich spider silk filaments $^{30}$ . e, Synthetic process of spider silk formation, realized in a microfluidic device (left), together with a micrograph (right) of the resulting synthetic fibres (scale bar  $10\mu m$ ). Adapted and reprinted with permission from ref. 39. © 2008 National Academy of Sciences USA.

functional structure $^{1}$  (Fig. 2a). In vivo, many protein materials obtain their specific functionality by post-translational modifications, which include hydroxylations (for example during formation of tropocollagen's hydroxyproline residues), phosphorylations and glycosylations (for example during formation of cartilage tissues), as well as enzymatic crosslinking. These modifications are particularly important for the material properties of tissues, as they control the interaction between proteins and with other material components (such as inorganic materials or sugar-based components) as well as their bioactive properties. These modifications are particularly difficult to mimic ex vivo or through synthetic approaches,

posing a challenge in the development of biomimicking and biocompatible materials.

The resultant individual protein components self-assemble at different timescales to form a protein structure with hierarchical geometrical entities (Fig. 1a, b). Assembly mechanisms have been investigated based on the combination of imaging tools with controlled assembly conditions (pH, temperature, solvent). This approach has elucidated the mechanism of lamin assembly[14,37] (Fig. 2b). In this process, lamin dimer association and axial growth are followed by radial growth to form larger fibrils, resulting in formation of a network. Figure 2b also shows the direct

NATURE MATERIALS | VOL 8 | MARCH 2009 | www.nature.com/naturematerials

---

NATURE MATERIALS DOI:10.1038/NMAT2387

REVIEW ARTICLE

![img-9.jpeg](img-9.jpeg)
a

![img-10.jpeg](img-10.jpeg)
b
Figure 3 | Universality and diversity of biological protein materials. a, Degree of structural diversity and universality in protein materials, plotted against biological length scales (equivalent to hierarchical levels). Inset, a visualization of the topoisomerase protein (biological role is to cut strands of the DNA double helix; visualization using visual molecular dynamics $^{142}$ ). This inset illustrates how universal motifs define the overall functional properties of this protein, whereas the entire protein structure represents diversity. See also Table 2. AH,  $\alpha$ -helix; BS,  $\beta$ -sheet; RC, random coil; AA, amino acid. b, Placement of mesoscale science of protein materials, between single-molecule studies and micromechanical and continuum-type biomechanics applications.

Table 2 | Occurrence of protocols in four sample materials, illustrating that some protocols are universal to all protein materials whereas others are specific.

|  Protocol | Biological protein material  |   |   |   |
| --- | --- | --- | --- | --- |
|   | Collagen (tendon) | Lamin | Spider silk | Amyloids  |
|  DNA nucleotides* (ACGT) | ✓ | ✓ | ✓ | ✓  |
|  Vimentin DNA sequence† | ✓ |  |  |   |
|  Collagen DNA sequence† |  | ✓ |  |   |
|  Spider silk DNA sequence† |  |  | ✓ |   |
|  Amyloid DNA sequence† |  |  |  | ✓  |
|  DNA double-helical structure* | ✓ | ✓ | ✓ | ✓  |
|  Protein building blocks* (20 AAs) | ✓ | ✓ | ✓ | ✓  |
|  Motifs* AH, BS, RC | ✓ | ✓ | ✓ | ✓  |
|  Collagen fibril† | ✓ |  |  |   |
|  Lamin filaments† |  | ✓ |  |   |
|  β-Nanocrystal composite† |  |  | ✓ |   |
|  Cross-β fibril structure† |  |  |  | ✓  |

*Universal; †diverse. AH, α-helix; BS, β-sheet; RC, random coil; AA, amino acid.

experimental visualization of these assembly processes. A snapshot of the assembly process for collagen fibrils is shown in Fig. 2c, revealing the characteristic banding structure of collagen fibrils when multiple molecules assemble into microfibrils. The biological process of in vivo assembly of many structural protein materials involves a dynamic change of physical and chemical conditions, as has been shown for the synthesis of spider silk $^{38,39}$  (Fig. 2d).

In addition to studies of naturally occurring biological protein materials, recent research led to the development of techniques that enable one to change their structural makeup, and to design and synthesize synthetic analogues $^{40-44}$  through recombinant DNA techniques, RNA interference knockdowns or sequence insertions. Two primary routes of development pursued include ex vivo assembly (for example self-assembling peptide systems $^{40,41,44}$ ) and in vivo expression of protein materials (for example through bacterial hosts $^{42,45}$ ). The ability to control the DNA sequence information at a fundamental level provides us with the ability to engineer the structure of protein materials at the molecular (amino acid) scale. EAK16, for example, belongs to an interesting class of self-assembled peptides that constitutes a material platform for a variety of biological, biomimetic and nanotechnology applications $^{46}$ . Knowledge of the details of the in vivo processes enables one to mimic these processes

ex vivo, as has been demonstrated for spider silk fibres in microfluidic devices $^{39}$  (Fig. 2e).

The ability to control self assembly synthetically and genetically provides a powerful framework for the study of the links between structure, property and process. The approach of adding and deleting molecular domains with distinct chemical functionality has made possible the detailed study of the mechanisms of self-assembly processes (for example identification of essential protein domains) $^{47-50}$ . This allows one to determine how changes to the protein structure alter biological function and disease properties.

The evolution of protein materials through genetic selection and structural alterations has resulted in a specific set of protein building blocks that define their structure. Protein materials exist in abundant variety, and the need exists to formulate a widely applicable model to categorize all such materials systematically, in order to establish a fundamental understanding, and to make use of hierarchical structural building blocks to develop a new generation of advanced nanomaterials $^{51-53}$ . A protocol is defined here as a term that encompasses a general analysis of protein materials that describes the use of structural building blocks (for example  $\alpha$ -helices,  $\beta$ -sheets, random coils) during their formation and function, and the process or mechanism of use of this material (for example synthesis,

NATURE MATERIALS | VOL 8 | MARCH 2009 | www.nature.com/naturematerials

---

breakdown, self assembly). The phenomenon of universality exists ubiquitously in biology, where certain protocols are commonly found in all protein materials (such as the use of hierarchical levels of building blocks: DNA nucleotides, DNA double helical structure, α-helices, β-sheets and the process of transcription/translation, protein synthesis). However, other protocols are highly specialized (such as the use of specific DNA sequences for a particular protein structure, the resultant protein motifs of tendon fascicles, lattice-like lamin structure, and so on), thus representing diversity. Protocols can therefore be classified as either universal or diverse.

Universal and diverse protocols are distributed heterogeneously across hierarchical levels (Fig. 3a and Table 2). The four DNA nucleotides (ACGT) represent a universal protocol common to all protein materials, where their arrangements in diverse patterns form the immense variety of genetic sequences found in biology. Genetic sequences are universally encoded in a double-helical DNA structure, regardless of the specific nucleotide sequence. Through the universal process of transcription and translation, protein molecules are synthesized into a 1D sequence of the universal 20 amino-acid building blocks. Virtually all proteins contain one or more of these universally found motifs: α-helices, β-sheets and random coils. These universal motifs arrange into unique, diverse larger-scale protein structures (for example enzymes, fibres, filaments). A greater diversity of protocols is generally found at higher levels, suggesting that biological functionality is associated with structural diversity. Universality is associated with protocols that can be used to derive diverse functionality at larger hierarchical levels. A fundamental difference between engineered materials and naturally formed biological materials is that functionality in biology can be created by arranging universal building blocks in different patterns, rather than by inventing new types of building block. The formation of hierarchical arrangements provides the structural basis that allows the existence of universality and diversity within a single material. This combination of dissimilar concepts may explain how protein materials are capable of combining disparate material properties, such as high strength and high robustness, together with multifunctionality.

Biological functionality must be understood at varying scales. Biochemistry focuses on biological functionality at molecular scales. The mesoscale, which encompasses length scales ranging from nanometres to micrometres and timescales of nanoseconds to microseconds, is a particularly important level necessary to understand how specific protein materials derive their unique properties and what role they play (in both physiological and pathological phenomena; Fig. 3b). The mesoscale science of protein materials, through the linking of molecular properties to properties of protein materials at the microscale, thus represents an important frontier of materials research with great potential for fundamental contributions to biology and medicine as well as for the de novo synthesis of engineered materials.

The approach of making use of universal building blocks to create diverse multifunctional hierarchical structures has been successfully applied in current macroscale engineering paradigms. For example, in the design of structures such as buildings or bridges, universal constituents (bricks, cement, steel trusses, glass) are combined to create multifunctionality (structural support, living space, thermal properties, light harvesting) at larger length scales. The challenge of using similar concepts that span to the nanoscale, as exemplified in biological protein materials by merging structure and material, could lead to the emergence of new technological concepts. A key obstacle in the development of new materials lies in our inability to control the structure formation directly at multiple hierarchical levels. The concept of universality and diversity and the knowledge gained from how to characterize these materials at different hierarchical levels may help in addressing these challenges.

Nature's use of a limited number of universal building blocks, arranged in a variety of ways, is a limitation as well as a strength of biological systems. For example, although the performance of structural tissues in our body is poor compared with most engineered materials (such as steel or concrete), their performance is remarkably good considering their inferior building blocks. Understanding these material concepts and their translation to the design of synthetic materials could provide us with new concepts for materials design based on inexpensive, abundant and environmentally benign constituents.

## Multiscale failure mechanisms of protein materials

The stability and failure mechanisms of biological protein materials play an integral part in defining their functional role in biological systems. In this context, a bottom-up description must begin with the study of the properties of individual protein molecules. A variety of experimental, theoretical and computational tools have been developed to assess structure--process--property relations and to monitor and predict materials failure mechanisms.

In biological protein materials, each hierarchical level has its own defects and failure mechanism. Over multiple hierarchical levels, there are two primary types of response. First, if a material is able to tolerate defects and failure at specific scales, it retains its overall integrity because the presence of multiple hierarchical levels decreases the overall probability of catastrophic failure. Second, some defects and failure mechanisms lead to a catastrophic breakdown of the material (for example in genetic disease, where proteins are misfolded owing to errors in the DNA code). Many physiological conditions exist in the realm where the material is able to tolerate defects and failure mechanisms (such as microcracks in bone^{36}), and many diseases originate because of the material's inability to mitigate material defects and breakdown. In both cases, the basic mechanisms of failure can be evident through the breaking of hydrogen bonds, protein unfolding, sliding of molecules against each other and breaking of crosslinks. Failure occurs because the intramolecular bonding (for example hydrogen bonds) is crucial to defining the structure of protein building blocks. Similarly, adhesion forces due to a charged surface or hydrophobic forces between molecules, fibrils, fibres and filaments are elementary to providing function at larger length scales. Often, these failure mechanisms are competing and depend on loading rate, pH, density of crosslinks or molecular geometry^{34,54--56}. These biological failure mechanisms can be analogous to failure in engineering materials, which is mediated by defects such as cracks, dislocations or mass transport along grain boundaries. The quantitative analysis of multiscale failure mechanisms provides great potential in explaining the role of materials in their respective biological context.

Advances in experimental techniques have allowed the structural characterization of protein materials across multiple scales (Fig. 4). Techniques such as nuclear magnetic resonance (NMR) spectroscopy and X-ray crystallography have advanced our ability to identify 3D protein structures^{57}. Site-specific studies using NMR, a technique that allows internal molecular motions to be probed while spanning a range of timescales with precise spatial resolution, have provided insight into the dynamics of large protein complexes^{58}. The analysis of molecular-scale deformation mechanisms has also been achieved through use of X-ray crystallography, providing structural and temporal information about mechanisms of deformation and assembly (for example in intermediate filaments, tendon or bone)^{25,32,50,59}. The development of the Protein Data Bank in the 1970s enhanced this progression, serving as a public repository for tens of thousands of 3D atomistic protein structures, identifying the structure of numerous proteins from varying species sources^{60}. X-ray tomography provides insight into the internal structure of a wide range of length scales encountered in protein memes^{61}. The high penetrating power of X-ray tomography, coupled with a near absence of reflection at the interface of dissimilar materials, makes this an ideal probe for reconstructing the morphology and composition of proteins at high resolutions (up to 50 nm)^{61}.

---

NATURE MATERIALS DOI: 10.1038/NMAT2387

REVIEW ARTICLE

![img-11.jpeg](img-11.jpeg)
Figure 4 | Tools for characterization and modelling of deformation and failure of biological protein materials. Respective timescale and length-scale domains of applicability are shown. Experimental methods include X-ray diffraction, transmission electron microscopy, atomic force microscopy (AFM), optical/magnetic tweezers; microelectromechanical systems (MEMS) testing and nanoindentation. Theoretical and simulation tools include quantum mechanics/density functional theory (QM/DFT), molecular dynamics (MD), coarse-grained models and mesoscale atomistically informed continuum theories, as well as continuum models. The lower part of the figure indicates classes or scales of protein materials that can be studied with these types of technique. a, Coarse-graining process in the development of mesoscale models, here illustrating the representation of the full-atomistic description of a tropocollagen molecule by a collection of 'super-atoms' or beads, reaching length scales and timescales several orders larger. b, Deformation of a lamin intermediate filament (LIF) using AFM. Adapted and reprinted with permission from ref. 141. © 2007 NPG. c, Tensile stretching experiment of a collagen fibril with a MEMS device (scale bar  $2\mu \mathrm{m}$ ). Reprinted with permission from ref. 82. © 2006 Royal Society.

Mass spectroscopy provides information about the chemical content of protein materials. Fourier-transform infrared (FTIR) spectroscopy is a related approach that elucidates information about chemical bonding and is an established tool used for the structural characterization of proteins $^{62,63}$ . Developments in single-molecule force spectroscopy have made it possible to study chemical, mechanical and structural properties using manipulation techniques such as atomic force microscopy (AFM) and optical/magnetic tweezers $^{20,64-72}$ . The force-measuring capability of AFM also makes it possible to elucidate molecular determinants of mechanical stability and the role of force-induced conformational changes of proteins in the regulation of physiological function $^{73,74}$ , and it has been used to image the surface structure and assembly patterns (for example in bone and collagen $^{72,75-77}$ ). AFM has also been effectively used in combination with fluorescent techniques for imaging, as reported in studies of fibrin stretching $^{6}$ . In a recent study, in situ fluorescent labelling was used to visualize unfolding of cytoskeletal proteins in cells under different mechanical loading conditions $^{78}$ , providing a

quantitative link between cellular-scale deformation and underlying molecular-scale rupture mechanisms. The basic concept of this approach is that protein unfolding due to rupture leads to the exposure of binding sites, which can be used to bind fluorescent markers for imaging. This technique has shown that protein rupture occurs as an underlying mechanism in cells under mechanical load $^{78}$ . Nanoindentation is another method used to probe the mechanical response of protein material composition and structure at multiple length scales $^{79}$ , and has allowed the characterization of multiscale mechanical behaviour, as demonstrated for bone $^{80,81}$ . The development of devices based on microelectromechanical systems (MEMS) provides the ability to carry out tensile tests of micrometre-sized samples, as demonstrated for individual collagen fibrils $^{82}$ . The available experimental methods cover a broad range of timescales and length scales. Remaining challenges include specificity with respect to the handling of individual molecules and filaments, their control at very short timescales, and the ability to observe mechanisms directly at molecular scales.

NATURE MATERIALS | VOL 8 | MARCH 2009 | www.nature.com/naturematerials

---

REVIEW ARTICLE

NATURE MATERIALS DOI: 10.1038/NMAT2387

![img-12.jpeg](img-12.jpeg)
a

![img-13.jpeg](img-13.jpeg)
b

![img-14.jpeg](img-14.jpeg)
c

![img-15.jpeg](img-15.jpeg)
d
Figure 5 | Chemomechanical behaviour of protein constituents.

a, Schematic diagram of the energy-distance curve of a protein domain transitioning from the folded to the unfolded state. The inset depicts this process during unfolding of a convolution in an  $\alpha$ -helix protein domain. State I corresponds to the case when donor-acceptor pairs form hydrogen bonds (H-bonds) in an  $\alpha$ -helix convolution. The dotted line represents a second state II, corresponding to the unfolded configuration of an  $\alpha$ -helix convolution when hydrogen bonds are broken. The transition between the two local minima occurs through an activated state I-II in a 3D deformation path (timescale of rupture is approximately 60 ps, where state I-II is reached after 20 ps and state II after another 40 ps; the concurrent breaking of all three to four hydrogen bonds within a convolution of the  $\alpha$ -helix represents the basic mechanism of rupture)[55]. b, Mechanism of deformation of a single tropocollagen molecule under tension, showing the dynamics of hydrogen-bond breaking under stretching of a single tropocollagen molecule (hydrogen bonds break at a rate of two hydrogen bonds for every  $1\%$  increase in strain)[86]. c, Resulting effective energy landscape for such a process, showing how the energy barrier is reduced because of a laterally applied force  $F$  (the inset displays the loading condition of an  $\alpha$ -helix protein domain under tensile loading). d, Strength properties of several protein domains as a function of deformation speed ( $\alpha$ -helices and  $\beta$ -sheets, data plotted from refs 55,67,70,142). Faster deformation (that is, short timescales) generally leads to an increased rupture force. The dotted lines are included to guide the eye; they approximate regimes of straight lines in the plot of  $F$  against  $\ln(v)$ .

Complementing experimental approaches, atomistic simulation methods provide a bottom-up description of materials based on the dynamical trajectory of each atom, by considering their atomic interactions. Molecular dynamics (commonly abbreviated as MD) solves each atom's equation of motion[83]. In classical molecular dynamics, the 3D structure of an atom is approximated by a point particle. The numerical integration of Newton's law  $(F = ma)$ , by considering appropriate force fields, enables one to simulate a large ensemble of atoms that represents a larger material volume. The atomic interactions are described by decomposing the behaviour of chemical bonds into stretching, bending or rotation contributions[83-85]. Because of computational limitations, atomistic-based simulation approaches are typically limited to billions of particles (that is, length scales below micrometres) and timescales of less than a microsecond.

Despite the shortcomings with respect to accessible timescales and length scales, the uniqueness of atomistic methods is the ability to directly visualize the dynamics of deformation and failure. For

example, results of molecular dynamics simulations elucidated mechanisms of hydrogen-bond rupture in protein domains, as shown in Fig. 5a (inset) $^{55}$ . Similar hydrogen-bond failure mechanisms have been observed in other proteins, such as  $\beta$ -sheet crystals $^{55}$ . Studies analysing the deformation and failure mechanisms of tropocollagen molecules found that initial molecular rotation is followed by hydrogen-bond breaking and subsequent stretching of the protein's polypeptide backbone, followed by covalent bond rupture, explaining collagen's characteristic stiffening $^{31,86}$  (Fig. 5b). Molecular dynamics simulations have also been useful in defining experimental protocols for in situ fluorescent labelling by identifying key rupture mechanisms and exposing domains $^{78}$ .

Larger length scales and timescales can be reached through the use of a hierarchy of simulation techniques, integrated through multiscale methods (Fig. 4). These methods are based on the concept of informing coarser scales from finer scales, enabling one to establish direct links between chemical structure and larger scales. In multiscale approaches, groups of atoms in protein structures are often represented by 'super-atoms' or beads, thereby effectively reducing the degrees of freedom (a coarse-graining approach for tropocollagen is shown in Fig. 4a). The direct comparison between molecular dynamics simulation (in particular coarse-graining methods) and experiment has become more viable owing to the emergence of experimental tools that reach ever smaller scales.

At molecular and submolecular scales, an integrated chemomechanical approach is mandatory to describe the failure properties of biological protein materials. Theoretical approaches that link chemistry and mechanics are often derived from a phenomenological theory originally postulated by Bell more than 30 years ago[87-90]. Several sophisticated, advanced models are now available[91-96] and the 'original' Bell model is less often used in the analysis of protein rupture. However, the ideas behind Bell's model provide the intellectual foundation for many theories. The basic concept of the interplay of applied forces and the resulting energy landscape change is illustrated in Fig. 5c. The Bell model is based on a statistical approach to describe the likelihood of bond rupture under the presence of an energy barrier  $E_{\mathrm{b}}$ , which is reduced due to an applied force  $F$  at the failure point  $x_{\mathrm{b}}$ . The probability for a bond to break is expressed using an Arrhenius expression, which predicts that the lifetime of a bond decreases exponentially as the energy barrier decreases under the applied force. Expressions that relate the failure force  $F$  to the pulling rate  $\nu$  applied to a protein predict a characteristic logarithmic dependence of the rupture force as a function of timescales or pulling rate  $\nu$ , resulting in a dependence of the form  $F(\nu; x_{\mathrm{b}}E_{\mathrm{b}}) = a(x_{\mathrm{b}},T)\ln (\nu) + b(x_{\mathrm{b}},E_{\mathrm{b}},T)$  (where  $a$  and  $b$  are parameters that depend on the energy landscape and temperature  $T$ ).

Figure 5d displays a set of experimental and computational results, illustrating this type of relationship. Each straight line reflects a particular rupture mechanism, characterized by an energy barrier  $E_{\mathrm{b}}$  and a transition state distance  $x_{\mathrm{b}}$ . Variations of pulling rates often induce a change in failure mechanism. The analysis of the results of the pulling rate dependence of forces allows the interpretation of experimental and computational results through the determination of effective energy barriers and transition states, and provides insight into microscopic failure mechanisms.

The original Bell model does not provide a direct link between the atomistic chemical structure of a bond (or arrangements of bonds) and the resulting behaviour. For instance, the effective energy barrier shown in Fig. 5c may represent a cluster of several weak bonds that break simultaneously, or a single, stronger bond. The model further does not capture the effect that the energy landscape itself may change as the protein deforms. Other models have been reported that describe the strength of proteins in dependence on the force rate (the rate of increase of force over time)[91-96]. Some models also

NATURE MATERIALS | VOL 8 | MARCH 2009 | www.nature.com/naturematerials

---

NATURE MATERIALS DOI: 10.1038/NMAT2387

REVIEW ARTICLE

![img-16.jpeg](img-16.jpeg)
a

![img-17.jpeg](img-17.jpeg)

![img-18.jpeg](img-18.jpeg)

![img-19.jpeg](img-19.jpeg)
Figure 6 | Integration of theory, simulation and experimental techniques. a, Results of an elastic network model calculation, used to describe the anisotropic failure properties of a larger protein structure. Reprinted with permission from ref. 98. © 2008 APS. b, Entropic elastic behaviour of stretching a single tropocollagen (TC) molecule, comparing experiment (optical tweezers), coarse-grained mesoscale simulation (molecular dynamics, MD) and theory (worm-like-chain model, WLC). Data replotted from refs 31 and 103;  $x / L$  is the ratio of extension  $x$  to contour length  $L$ . c, Young's modulus prediction of a single tropocollagen molecule. The graph shows a comparison between experimental and full-atomistic molecular dynamics simulation results (based on averages from literature sources summarized in ref. 86; error bars correspond to standard deviation). d, Comparison between experimental and theoretical modelling of stretching a long titin filament, obtained through the application of a theoretical approach that involves the Bell model and a worm-like-chain description for protein elasticity. Reprinted with permission from ref. 104. © 1998 APS.

![img-20.jpeg](img-20.jpeg)

![img-21.jpeg](img-21.jpeg)

include a description of the transition between multiple transition states, effectively describing the occurrence of several straight lines in the  $F - \ln (\nu)$  domain $^{91-96}$  (similar to the overall behaviour shown in Fig. 5d).

Challenges in linking simulation and experiment include differences in accessible timescales and length scales. For example, the computational prediction of the 3D folded structure of proteins directly from the amino acid sequence is, despite advances in recent years, still at a relatively early stage and can typically only be applied reliably to simpler protein structures, as the timescales for protein folding are beyond current computational capabilities[97].

Because biological protein materials feature properties that are strongly length-scale and timescale dependent, the explicit consideration of particular scales for the quantitative comparison of measurements and theory is essential. Measurements at different timescales and length scales lead to significant variations in material properties. For timescales, this can be observed in the results of strength properties reviewed in Fig. 5d $^{33,67,79}$ . This plot explains why many molecular dynamics simulations predict a vastly different behaviour from experimental studies, because they are carried out at different timescales. An implication of these strong size effects is that one cannot directly use single-molecule measurements to infer larger-scale properties, and that homogenization approaches commonly used for crystalline materials cannot be applied directly.

A multiscale analysis that explicitly calculates or measures material properties at multiple scales is compulsory.

Despite these challenges, several studies have led to direct comparison between experiment and theory. Protein strength models have been extended to more complex protein geometries, a vital step to arrive at structure-process-property relationships of strength properties[98-100]. Figure 6a shows an elastic bond network model for protein unfolding mechanics, which combines an elastic model of a network of bonds with a bond fracture model based on Bell's concept[98]. The model, here applied to green fluorescent protein, treats bonds as springs and provides a direct structure-property relationship between the geometry and bond rupture (for example the protein's mechanical anisotropy). It is capable of accurately reproducing experimental results reported earlier for the same protein structure[101] (for comparison see Fig. 6a).

A major success is the use of the worm-like-chain model to describe entropic elasticity[49,102]. The use of Bell-type strength models in conjunction with worm-like-chain models resulted in quantitative agreement between theory and experiment. Figure 6b depicts the comparison of an optical tweezers experiment of stretching a single tropocollagen molecule with results from molecular dynamics simulation (based on the mesoscale coarse-grained model shown in Fig. 4a) and the theoretical worm-like-chain model[31,102,103]. All three approaches provide a

NATURE MATERIALS | VOL 8 | MARCH 2009 | www.nature.com/naturematerials

---

consistent description of the protein's entropic elastic behaviour. Measurements and theoretical predictions of the stiffness of single tropocollagen molecules at larger deformation (when hydrogen bonds within the molecules are being stretched) are compared in Fig. 6c, revealing good agreement between various experimental and molecular dynamics simulation approaches. Under large forces and displacements, the worm-like-chain model fails and rupture of hydrogen bonds within protein domains dominates (see Fig. 5a, b)^{69}. This behaviour has been captured in quantitative models that combine the worm-like-chain model with the Bell model as reported previously^{104,105}. Figure 6d shows a comparison between experimental and theoretical results based on an elastically coupled protein model that predicts elastic and strength properties^{104}. The theoretical prediction and experimental results are in good agreement, suggesting that this model can accurately reflect the interplay of strength and elasticity.

A recent paper further illustrates the integration of experiment and theory, where measurements of molecular rupture forces between single actin filaments and two actin-binding proteins provide key insight into the competition of rupture mechanisms under different pulling rates^{54}. It was observed that whereas the breaking of α-actinin/actin clusters dominates at slow pulling rates, the breaking of filamin/actin clusters governs at higher pulling rates. This quantitative understanding of competing mechanisms is a crucial element in the development of failure models of soft tissues. Studies of fibrin provide another example of a protein material where experiment, theory and simulation have been effectively combined to improve our understanding of its material properties^{6,7}. The initial observation of extreme extensibility of fibrin (>300% strain)^{6} motivated single-molecule studies^{8} as well as molecular dynamics simulations^{9}, which suggested that the particular coiled-coil structure of this protein provides the structural basis for fibrin's great extensibility.

## Role of protein materials in disease

Throughout the past century, the focus on addressing diseases has derived primarily from a biochemical approach. However, advancements and increased understanding have yielded a greater appreciation of the role of materials science of protein materials in various medical disorders. In this section, the role of biologically relevant material properties in the progression or activation of diseased states will be discussed.

Alzheimer's disease, Parkinson's disease, type II diabetes and prion diseases^{106--109} have been linked to the formation of foreign material deposits in tissues. These material deposits, referred to as amyloid plaques, are highly ordered hierarchical assemblies of β-sheet protein domains that form spontaneously (Fig. 7a)^{110--113}. Once formation is initiated, amyloid plaques grow uncontrollably to length scales of micrometres and persist under a wide range of pH conditions. The mechanical robustness of these plaques has been attributed to the large number of hydrogen bonds as well as to steric and hydrophobic interactions between different parts of the β-sheet structures^{110,114,115}, although the exact structure--process--property relationships for this material remain to be investigated. The properties of amyloid fibrils have been probed using AFM techniques and molecular dynamics simulations^{55,68,111,116,117}. It is understood that the formation of amyloid plaque deposits leads to neurotoxicity, which interferes with the biological function of the native tissue^{108,109}. The mechanical robustness of amyloid plaques and the body's failure to eliminate these material deposits remain the primary reasons for our inability to reverse the progression of this disease. An improved understanding of how the hierarchical structure of amyloid plaques contributes to their extreme mechanical stability could lead to new strategies for treatment through targeting selective breakdown of these material deposits in situ.

Hutchinson--Gilford progeria syndrome, a genetic rapid ageing disease, is caused by a structural defect in the lamin nuclear membrane^{22,118--120}. The progression of this disease has been associated with mechanical failure of the cell's nuclear membrane in tissues subject to mechanical loading. A recent study based on live-cell imaging and micropipette aspiration has shown that progeria nuclear membranes display a reduced deformability and feature the formation of fractures on application of mechanical load^{22}. The cause of these fractures is attributed to changes in the lamin microstructure, where filaments form more ordered domains that prevent the dissipation of mechanical stress. This structural alteration leads to a change in the deformation mechanism, from a dissipative mode (‘ductile') in healthy cells to a catastrophic, localized failure mode (‘brittle') in diseased cells (Fig. 7b, c). These mechanisms appear predominantly in cells that are subjected to mechanical deformation, particularly in endothelial and smooth muscle cells of the vascular system. Perhaps a loss of mechanical integrity in the cell's nuclear membrane can influence gene regulation by triggering a wide range of biochemical processes that lead to the rapid ageing phenomenon. However, the exact molecular failure mechanisms remain unknown and their investigation represents an opportunity for future research where a materials science approach could make an important contribution. This disease illustrates how material failure due to structural flaws within a protein material can lead to the breakdown of critical biological components. Many other genetic diseases resulting from structural flaws in the lamin protein network have been identified, generally referred to as ‘laminopathies'^{118--120}.

Other genetic disorders in collagenous tissues have been linked to the alteration of the material structure owing to mutations in the genes that encode the tropocollagen molecule. Osteogenesis imperfecta is a genetic disease that increases the susceptibility of bones to catastrophic brittle fracture. The origin of this disease resides in changes to the structure of tropocollagen molecules caused by the substitution of a single glycine amino acid (Fig. 7d)^{121,122}. Some collagen mutations prevent the formation of triple helical molecules (procollagen suicide), whereas other mutations cause structural changes to tropocollagen molecules, leading to bending (caused, for example, by kinks induced by amino acid substitutions), reduced mechanical stiffness (caused, for example, by changes in the volume and hydrophobicity), or changes in the intermolecular adhesion (caused, for example, by changes in surface charges)^{121--123}. At mesoscopic length scales, these molecular-level changes lead to poor fibril packing^{124,125} and a decrease in crosslink density^{125,126}. Changes in the size and shape of mineral crystals in bone (for example less organized, more rounded crystals) have also been reported^{127--129} and are possibly due to a change in the ability of tropocollagen to bind to the mineral phase of bone^{130,131}. At larger length scales, the effects of osteogenesis imperfecta mutations lead to inferior mechanical properties of tendon and bone^{132} (Fig. 7d). A mechanically inferior collagen matrix in addition to an increased and less organized mineral content, and an overall reduced bone volume caused by reduced bone turnover^{133}, may explain the phenomenon of brittle bones, an important feature of osteogenesis imperfecta^{125}. A related disease in which collagen mutations play a key role is Alport's syndrome, in which a mutation in the collagen gene alters the glomerular basement membrane of kidneys^{134}. The progression of mechanical failure of the glomerular basement membrane eventually leads to the kidney's inability to filter blood, resulting in renal failure.

The change of cell stiffness in cancer cells has been shown by using a microfluidic optical cell stretcher^{135}. Studies of AFM indentation of cells confirmed that cancer cells display a reduced stiffness compared with that of healthy cells^{136} (Fig. 7e). This mechanical signature of cancer cells could perhaps be used to define new diagnostic approaches in cancer detection. The

---

NATURE MATERIALS DOI: 10.1038/NMAT2387

REVIEW ARTICLE

![img-22.jpeg](img-22.jpeg)
a

![img-23.jpeg](img-23.jpeg)
b

![img-24.jpeg](img-24.jpeg)
c

![img-25.jpeg](img-25.jpeg)
d

![img-26.jpeg](img-26.jpeg)
e
Figure 7 | Role of changes in biological protein material properties in diseases. a, Structure of amyloids, spanning from the chemical structure of individual hydrogen bonds to the scale of amyloid plaques. Included is a visualization of molecular models proposed for amyloid fibrils ('cross-  $\beta$ -structure' and '  $\beta$ -helix'). Protofilament structure reprinted with permission from ref. 143. © NPG. b, Effect of lamin mutations in progeria on the mechanical properties of the cell nuclear membrane (scale bar  $5\mu m$ , fluorescent imaging). The cell nuclear membrane forms localized fractures under large mechanical loading. c, Change in the lamin microstructure due to genetic mutation, and effect on deformation mechanism (b and c reprinted with permission from ref. 22. © 2006 National Academy of Sciences USA). d, Geometry of point mutations in osteogenesis imperfecta (OI) in the tropocollagen molecule (upper part), and effect on mechanical properties of tendon, where the maximum strain and maximum stress of tendon are severely reduced under mutations (lower part, data plotted from ref. 132). e, Mechanical signature of cancer versus normal cells, revealing that cancer cells are softer than normal cells. Adapted and reprinted with permission from ref. 136. © 1997 NPG.

approach based on microfluidic stretching $^{135}$  may provide an effective high-throughput platform for cancer diagnosis. Studies of cell mechanics using optical tweezers have revealed that malaria-infected cells become stiffer, preventing normal blood flow through lung capillaries $^{137}$ . The elastic cellular microenvironment (for example the stiffness of collagen-based extracellular matrix) has been shown to control stem cell differentiation into neuron, muscle or bone cells $^{138}$ .

These case studies illustrate that the change of material properties is a crucial element in many diseases. Translation of this knowledge would allow detection of diseases by measuring material properties rather than by focusing on symptomatic biochemical readings alone. Altogether, understanding the role of different hierarchical levels of protein materials in diseases could potentially bring about a new paradigm of approaches to address medical disorders; however, further research is needed to elucidate the underlying multiscale failure mechanisms.

# Future directions

Along with biomedical applications, understanding of the material concepts in protein materials could also be used to advance nanomaterials for engineering applications. Material properties of nanomaterials are often found to be superior to those of conventional engineering materials. For instance, carbon nanotubes are one of the strongest materials known but have rarely been used in structural materials because of our inability to use their properties at larger length scales. Understanding protein materials could provide knowledge that would eventually be translated to connecting disparate material scales, from nanoscales to macroscales. We may then be able to apply these material concepts to make use of the full potential (higher strength, higher robustness) of multiscale engineered materials. An intriguing application may be the development of a new material platform based on concepts similar to those found in biological protein materials. However, rather than using the universal protein constituents (such as  $\alpha$ -helices,  $\beta$ -sheets,

NATURE MATERIALS | VOL 8 | MARCH 2009 | www.nature.com/naturematerials

---

REVIEW ARTICLE

NATURE MATERIALS DOI: 10.1038/NMAT2387

random coils or tropocollagen), we could instead use building blocks such as carbon nanotubes, nanowires and self-assembled peptides. Some steps towards this goal have been taken in recent studies, where conducting metallic nanowires were grown through the use of amyloids as templates $^{139}$ .

Biology makes use of hierarchical structures in an intriguing way to create multifunctional materials. Even though biochemical and image-based diagnostics will remain important, the integration of scales, as well as the mixing of physical, biological and chemical concepts into new engineering designs, could complement the current practice of disease diagnosis and treatment, as well as the design of new materials, and thereby unfold many opportunities for technological innovations. The wide impact of the use of materials science approaches in biology and biomedical sciences has yet to be demonstrated. In some specific areas such as bone (for example osteoporosis), cartilage (for example arthritis), cardiovascular aspects and, particularly, in the context of tissue engineering and regenerative medicine, materials science approaches have started to play an important part in the biomedical literature.

In addition to mechanical deformation and failure mechanisms of protein materials, the investigation of other material properties could be of great interest. Optical properties (for example in the eye's cornea and lens), photoelectric properties (for example photosynthesis in plants), electrical (for example synapses, the links between neuron cells), motility (for example in muscle tissues) or thermal properties (for example thermal management) are critically important and could be studied using a materials science approach. The study of materials failure could provide an interesting platform to advance our understanding of diseases.

# References

1. Alberts, B. et al. Molecular Biology of the Cell. (Taylor &amp; Francis, 2002).
2. Wang, N. &amp; Stamenovic, D. Mechanics of vimentin intermediate filaments. J. Muscle Res. Cell. Motil. 23, 535-540 (2002).
3. Ingber, D. E. et al. in International Review of Cytology: A Survey of Cell Biology Vol 150, 173-224 (Academic, 1994).
4. Fratzl, P. &amp; Weinkamer, R. Nature's hierarchical materials. Prog. Mater. Sci. 52, 1263-1334 (2007).
5. Gelse, K., Poschl, E. &amp; Aigner, T. Collagens — structure, function, and biosynthesis. Adv. Drug Deliv. Rev. 55, 1531-1546 (2003).
6. Liu, W. et al. Fibrin fibers have extraordinary extensibility and elasticity. Science 313, 634-634 (2006).
7. Weisel, J. W. Biophysics: Enigmas of blood clot elasticity. Science 320, 456-457 (2008).
8. Brown, A. E. X., Litvinov, R. I., Discher, D. E. &amp; Weisel, J. W. Forced unfolding of the coiled-coils of fibrinogen by single molecule AFM. Biophys. J. 92, 39-41 (2007).
9. Lim, B. B. C., Lee, E. H., Sotomayor, M. &amp; Schulten, K. Molecular basis of fibrin clot elasticity. Structure 16, 449-459 (2008).
10. Ideker, T., Galitski, T. &amp; Hood, L. A new approach to decoding life: Systems biology. Annu. Rev. Genom. Hum. Genet. 2, 343-372 (2001).
11. Kitano, H. Computational systems biology. Nature 420, 206-210 (2002).
12. Kim, S. &amp; Coulombe, P. A. Intermediate filament scaffolds fulfill mechanical, organizational, and signaling functions in the cytoplasm. Genes Dev. 21, 1581-1597 (2007).
13. Kreplak, L. &amp; Fudge, D. Biomechanical properties of intermediate filaments: from tissues to single filaments and back. BioEssays 29, 26-35 (2007).
14. Herrmann, H. &amp; Aebi, U. Intermediate filaments: Molecular structure, assembly mechanism, and integration into functionally distinct intracellular scaffolds. Annu. Rev. Biochem. 73, 749-789 (2004).
15. Strelkov, S. V., Herrmann, H. &amp; Aebi, U. Molecular architecture of intermediate filaments. BioEssays 25, 243-251 (2003).
16. Aebi, U., Cohn, J., Buhle, L. &amp; Gerace, L. The nuclear lamina is a meshwork of intermediate-type filaments. Nature 323, 560-564 (1986).
17. Rowat, A. C., Lammerding, J., Herrmann, H. &amp; Aebi, U. Towards an integrated understanding of the structure and mechanics of the cell nucleus. BioEssays 30, 226-236 (2008).
18. Vaziri, A. &amp; Gopinath, A. Cell and biomolecular mechanics in silico. Nature Mater. (2007).
19. Vaziri, A. &amp; Mofrad, M. R. K. Mechanics and deformation of the nucleus in micropipette aspiration experiment. J. Biomech. 40, 2053-2062 (2007).

20. Lim, C. T., Zhou, E. H., Li, A., Vedula, S. R. K. &amp; Fu, H. X. Experimental techniques for single cell and single molecule biomechanics. Mater. Sci. Eng. C: Biomim. Supramol. Syst. 26, 1278-1288 (2006).
21. Wilson, K. L., Zastrow, M. S. &amp; Lee, K. K. Lamins and disease: Insights into nuclear infrastructure. Cell 104, 647-650 (2001).
22. Dahl, K. N. et al. Distinct structural and mechanical properties of the nuclear lamina in Hutchinson-Gilford progeria syndrome. Proc. Natl Acad. Sci. USA 103, 10271-10276 (2006).
23. Ingber, D. E. Cellular mechanotransduction: putting all the pieces together again. FASEB J. 20, 811-827 (2006).
24. Omary, M. B., Coulombe, P. A. &amp; McLean, W. H. I. Mechanisms of disease: Intermediate filament proteins and their associated diseases. N. Engl. J. Med. 351, 2087-2100 (2004).
25. Hulmes, D. J. S., Wess, T. J., Prockop, D. J. &amp; Fratzl, P. Radial packing, order, and disorder in collagen fibrils. Biophys. J. 68, 1661-1670 (1995).
26. Sasaki, N. &amp; Odajima, S. Elongation mechanism of collagen fibrils and force-strain relations of tendon at each level of structural hierarchy. J. Biomech. 29, 1131-1136 (1996).
27. Orgel, J. P. R. O., Irving, T. C., Miller, A. &amp; Wess, T. J. Microfibrillar structure of type I collagen in situ. Proc. Natl Acad. Sci. USA 103, 9001-9005 (1995).
28. Weiner, S. &amp; Wagner, H. D. The material bone: Structure mechanical function relations. Annu. Rev. Mater. Sci. 28, 271-298 (1998).
29. Nalla, R. K., Kinney, J. H. &amp; Ritchie, R. O. Mechanistic fracture criteria for the failure of human cortical bone. Nature Mater. 2, 164-168 (2003).
30. Ramachandran, G. N. &amp; Kartha, G. Structure of collagen. Nature 176, 593-595 (1955).
31. Buehler, M. J. &amp; Wong, S. Y. Entropic elasticity controls nanomechanics of single tropocollagen molecules. Biophys. J. 93, 37-43 (2007).
32. Gupta, H. S. et al. Cooperative deformation of mineral and collagen in bone at the nanoscale. Proc. Natl Acad. Sci. USA 103, 17741-17746 (2006).
33. Gupta, H. S. et al. Evidence for an elementary process in bone plasticity with an activation enthalpy of 1 eV. J. R. Soc. Interf. 4, 277-282 (2007).
34. Buehler, M. J. Nature designs tough collagen: Explaining the nanostructure of collagen fibrils. Proc. Natl Acad. Sci. USA 103, 12285-12290 (2006).
35. Gao, H., Ji, B., Jäger, I. L., Arzt, E. &amp; Fratzl, P. Materials become insensitive to flaws at nanoscale: Lessons from nature. Proc. Natl Acad. Sci. USA 100, 5597-5600 (2003).
36. Taylor, D., Hazenberg, J. G. &amp; Lee, T. C. Living with cracks: Damage and repair in human bone. Nature Mater. 6, 263-266 (2007).
37. Janmey, P. A., Leterrier, J. F. &amp; Herrmann, H. Assembly and structure of neurofilaments. Curr. Opin. Colloid Interf. Sci. 8, 40-47 (2003).
38. Bini, E., Knight, D. P. &amp; Kaplan, D. L. Mapping domain structures in silks from insects and spiders related to protein assembly. J. Mol. Biol. 335, 27-40 (2004).
39. Rammensee, S., Slotta, U., Scheibel, T. &amp; Bausch, A. R. Assembly mechanism of recombinant spider silk proteins. Proc. Natl Acad. Sci. USA 105, 6590-6595 (2008).
40. Petka, W. A., Harden, J. L., McGrath, K. P., Wirtz, D. &amp; Tirrell, D. A. Reversible hydrogels from self-assembling artificial proteins. Science 281, 389-392 (1998).
41. Zhao, X. J. &amp; Zhang, S. G. Molecular designer self-assembling peptides. Chem. Soc. Rev. 35, 1105-1110 (2006).
42. Langer, R. &amp; Tirrell, D. A. Designing materials for biology and medicine. Nature 428, 487-492 (2004).
43. Smeenk, J. M. et al. Controlled assembly of macromolecular beta-sheet fibrils. Angew. Chem. Int. Edn 44, 1968-1971 (2005).
44. Mershin, A., Cook, B., Kaiser, L. &amp; Zhang, S. G. A classic assembly of nanobiomaterials. Nature Biotechnol. 23, 1379-1380 (2005).
45. van Hest, J. C. M. &amp; Tirrell, D. A. Protein-based materials, toward a new level of structural control. Chem. Commun. 1897-1904 (2001).
46. Zhang, S. G., Lockshin, C., Cook, R. &amp; Rich, A. Unusually stable beta-sheet formation in an ionic self-complementary oligopeptide. Biopolymers 34, 663-672 (1994).
47. Kreplak, L., Aebi, U. &amp; Herrmann, H. Molecular mechanisms underlying the assembly of intermediate filaments. Exp. Cell Res. 301, 77-83 (2004).
48. Strelkov, S. V., Schumacher, J., Burkhard, P., Aebi, U. &amp; Herrmann, H. Crystal structure of the human lamin a coil 2B dimer: Implications for the head-to-tail association of nuclear lamins. J. Mol. Biol. 343, 1067-1080 (2004).
49. Schietke, R. et al. Mutations in vimentin disrupt the cytoskeleton in fibroblasts and delay execution of apoptosis. Eur. J. Cell Biol. 85, 1-10 (2006).
50. Sokolova, A. V. et al. Monitoring intermediate filament assembly by small-angle X-ray scattering reveals the molecular architecture of assembly intermediates. Proc. Natl Acad. Sci. USA 103, 16206-16211 (2006).
51. Alon, U. Simplicity in biology. Nature 446, 497 (2007).
52. Csete, M. E. &amp; Doyle, J. C. Reverse engineering of biological complexity. Science 295, 1664-1669 (2002).

NATURE MATERIALS | VOL 8 | MARCH 2009 | www.nature.com/naturematerials

---

NATURE MATERIALS DOI:10.1038/NMAT2387

REVIEW ARTICLE

53. Ackbarow, T. &amp; Buehler, M. J. Hierarchical coexistence of universality and diversity controls robustness and multi-functionality in protein materials. Theor. Comput. Nanosci. 5, 1193-1204 (2008).
54. Ferrer, J. M. et al. Measuring molecular rupture forces between single actin filaments and actin-binding proteins. Proc. Natl Acad. Sci. USA 105, 9221-9226 (2008).
55. Ackbarow, T., Chen, X., Keten, S. &amp; Buehler, M. J. Hierarchies, multiple energy barriers and robustness govern the fracture mechanics of alpha-helical and beta-sheet protein domains. Proc. Natl Acad. Sci. USA 104, 16410-16415 (2007).
56. Buehler, M. J., Keten, S. &amp; Ackbarow, T. Theoretical and computational hierarchical nanomechanics of protein materials: Deformation and fracture. Prog. Mater. Sci. 53, 1101-1241 (2008).
57. Astbury, W. T. &amp; Street, A. X-ray studies of the structures of hair, wool and related fibres. J. General. Phil. Trans. R. Soc. A 230, 75-101 (1931).
58. Mittermaier, A. &amp; Kay, L. E. Review: New tools provide new insights in NMR studies of protein dynamics. Science 312, 224-228 (2006).
59. Gupta, H. S. et al. Synchrotron diffraction study of deformation mechanisms in mineralized tendon. Phys. Rev. Lett. 93 (2004).
60. Bernstein, F. C. et al. Protein Data Bank: Computer-based archival file for macromolecular structures. J. Mol. Biol. 112, 535-542 (1977).
61. Le Gros, M. A., McDermott, G. &amp; Larabell, C. A. X-ray tomography of whole cells. Curr. Opin. Struct. Biol. 15, 593-600 (2005).
62. Jackson, M. &amp; Mantsch, H. H. The use and misuse of FTIR spectroscopy in the determination of protein-structure. Crit. Rev. Biochem. Molec. Biol. 30, 95-120 (1995).
63. Haris, P. I. &amp; Chapman, D. The conformational analysis of peptides using Fourier-transform IR spectroscopy. Biopolymers 37, 251-263 (1995).
64. Prater, C. B., Butt, H. J. &amp; Hansma, P. K. Atomic force microscopy. Nature 345, 839-840 (1990).
65. Fisher, T. E., Oberhauser, A. F., Carrion-Vazquez, M., Marszalek, P. E. &amp; Fernandez, J. M. The study of protein mechanics with the atomic force microscope. Trends Biochem. Sci. 24, 379-384 (1999).
66. Oberhauser, A. F., Badilla-Fernandez, C., Carrion-Vazquez, M. &amp; Fernandez, J. M. The mechanical hierarchies of fibronectin observed with single-molecule AFM. J. Mol. Biol. 319, 433-447 (2002).
67. Rief, M., Gautel, M., Oesterhelt, F., Fernandez, J. M. &amp; Gaub, H. E. Reversible unfolding of individual titin immunoglobulin domains by AFM. Science 276, 1109-1112 (1997).
68. Mostaert, A. S., Higgins, M. J., Fukuma, T., Rindi, F. &amp; Jarvis, S. P. Nanoscale mechanical characterisation of amyloid fibrils discovered in a natural adhesive. J. Biol. Phys. 32, 393-401 (2006).
69. Marszalek, P. E. et al. Mechanical unfolding intermediates in titin modules. Nature 402, 100-103 (1999).
70. Sotomayor, M. &amp; Schulten, K. Single-molecule experiments in vitro and in silico. Science 316, 1144-1148 (2007).
71. Lim, C. T., Dao, M., Suresh, S., Sow, C. H. &amp; Chew, K. T. Large deformation of living cells using laser traps. Acta Mater. 52, 1837-1845 (2004).
72. Hassenkam, T. et al. High-resolution AFM imaging of intact and fractured trabecular bone. Bone 35, 4-10 (2004).
73. Shao, Z. F., Mou, J., Czajkowsky, D. M., Yang, J. &amp; Yuan, J. Y. Biological atomic force microscopy: What is achieved and what is needed. Adv. Phys. 45, 1-86 (1996).
74. Fisher, T. E., Marszalek, P. E. &amp; Fernandez, J. M. Stretching single molecules into novel conformations using the atomic force microscope. Nature Struct. Biol. 7, 719-724 (2000).
75. Kadler, K. E., Holmes, D. F., Graham, H. &amp; Starborg, T. Tip-mediated fusion involving unipolar collagen fibrils accounts for rapid fibril elongation, the occurrence of fibrillar branched networks in skin and the paucity of collagen fibril ends in vertebrates. Matrix Biol. 19, 359-365 (2000).
76. Rainey, J. K., Wen, C. K. &amp; Goh, M. C. Hierarchical assembly and the onset of banding in fibrous long spacing collagen revealed by atomic force microscopy. Matrix Biol. 21, 647-660 (2002).
77. Fantner, G. E. et al. Sacrificial bonds and hidden length dissipate energy as mineralized fibrils separate during bone fracture. Nature Mater. 4, 612-616 (2005).
78. Johnson, C. P., Tang, H. Y., Carag, C., Speicher, D. W. &amp; Discher, D. E. Forced unfolding of proteins within cells. Science 317, 663-666 (2007).
79. Oliver, W. C. &amp; Pharr, G. M. Measurement of hardness and elastic modulus by instrumented indentation: Advances in understanding and refinements to methodology. J. Mater. Res. 19, 3-20 (2004).
80. Thompson, J. B. et al. Bone indentation recovery time correlates with bond reforming time. Nature 414, 773-776 (2001).
81. Tai, K., Dao, M., Suresh, S., Palazoglu, A. &amp; Ortiz, C. Nanoscale heterogeneity promotes energy dissipation in bone. Nature Mater. 6, 454-462 (2007).
82. Eppell, S. J., Smith, B. N., Kahn, H. &amp; Ballarini, R. Nano measurements with micro-devices: mechanical properties of hydrated collagen fibrils. J. R. Soc. Interf. 3, 117-121 (2006).

83. Karplus, M. &amp; McCammon, J. A. Molecular dynamics simulations of biomolecules. Nature Struct. Biol. 9, 646-652 (2002).
84. Wang, W., Donini, O., Reyes, C. M. &amp; Kollman, P. A. Biomolecular simulations: Recent developments in force fields, simulations of enzyme catalysis, protein-ligand, protein-protein, and protein-nucleic acid noncovalent interactions. Annu. Rev. Biophys. Biomol. Struct. 30, 211-243 (2001).
85. Mackerell, A. D. Empirical force fields for biological macromolecules: Overview and issues. J. Comput. Chem. 25, 1584-1604 (2004).
86. Gautieri, A., Buehler, M. J. &amp; Redaelli, A. Deformation rate controls elasticity and unfolding pathway of single tropocollagen molecules. J. Mech. Behavior Biomed. Mater. 2, 130-137 (2009).
87. Bell, G. I. Models for specific adhesion of cells to cells. Science 200, 618-627 (1978).
88. Kramers, H. A. Brownian motion in a field of force and the diffusion model of chemical reactions. Physica 7, 10 (1940).
89. Hanggi, P., Talkner, P. &amp; Borkovec, M. Reaction-rate theory: fifty years after Kramers. Rev. Mod. Phys. 62, 251-341 (1990).
90. Zhurkov, S. N. Kinetic concept of the strength of solids. Int. J. Fracture Mech. 1, 311-323 (1965).
91. Evans, E. Probing the relation between force, lifetime, and chemistry in single molecular bonds. Annu. Rev. Biophys. Biomol. Struct. 30, 105-128 (2001).
92. Merkel, R., Nassoy, P., Leung, A., Ritchie, K. &amp; Evans, E. Energy landscapes of receptor-ligand bonds explored with dynamic force spectroscopy. Nature 379, 50-53 (1999).
93. Evans, E. &amp; Ritchie, K. Dynamic strength of molecular adhesion bonds. Biophys. J. 72, 1541-1555 (1997).
94. Dudko, O. K., Hummer, G. &amp; Szabo, A. Intrinsic rates and activation free energies from single-molecule pulling experiments. Phys. Rev. Lett. 96 (2006).
95. Hummer, G. &amp; Szabo, A. Kinetics from nonequilibrium single-molecule pulling experiments. Biophys. J. 85, 5-15 (2003).
96. Hummer, G. &amp; Szabo, A. Free energy reconstruction from nonequilibrium single-molecule pulling experiments. Proc. Natl Acad. Sci. USA 98, 3658-3661 (2001).
97. Snow, C. D., Sorin, E. J., Rhee, Y. M. &amp; Pande, V. S. How well can simulation predict protein folding kinetics and thermodynamics? Annu. Rev. Biophys. Biomol. Struct. 34, 43-69 (2005).
98. Dietz, H. &amp; Rief, M. Elastic bond network model for protein unfolding mechanics. Phys. Rev. Lett. 100, 098101 (2008).
99. Seifert, U. Rupture of multiple parallel molecular bonds under dynamic loading. Phys. Rev. Lett. 84, 2750-2753 (2000).
100. Erdmann, T. &amp; Schwarz, U. S. Stability of adhesion clusters under constant force. Phys. Rev. Lett. 92, 4 (2004).
101. Dietz, H., Berkemeier, F., Bertz, M. &amp; Rief, M. Anisotropic deformation response of single protein molecules. Proc. Natl Acad. Sci. USA 103, 12724-12728 (2006).
102. Bustamante, C., Marko, J. F., Siggia, E. D. &amp; Smith, S. Entropic elasticity of lambda-phage DNA. Science 265, 1599-1600 (1994).
103. Sun, Y. L., Luo, Z. P., Fertala, A. &amp; An, K. N. Stretching type II collagen with optical tweezers. J. Biomech. 37, 1665-1669 (2004).
104. Rief, M., Fernandez, J. M. &amp; Gaub, H. E. Elastically coupled two-level systems as a model for biopolymer extensibility. Phys. Rev. Lett. 81, 4764-4767 (1998).
105. Keten, S. &amp; Buehler, M. J. Strength limit of entropic elasticity in beta-sheet protein domains. Phys. Rev. E 78, 061913 (2008).
106. Mesquida, P., Riener, C. K., MacPhee, C. E. &amp; McKendry, R. A. Morphology and mechanical stability of amyloid-like peptide fibrils. J. Mater. Sci. Mater. Med. 18, 1325-1331 (2007).
107. Iconomidou, V. A. &amp; Hamodrakas, S. J. Natural protective amyloids. Curr. Protein Pept. Sci. 9, 291-309 (2008).
108. Hardy, J. &amp; Selkoe, D. J. Medicine: The amyloid hypothesis of Alzheimer's disease. Progress and problems on the road to therapeutics. Science 297, 353-356 (2002).
109. Selkoe, D. J. Alzheimer's disease: Genes, proteins, and therapy. Physiol. Rev. 81, 741-766 (2001).
110. Knowles, T. P. et al. Role of intermolecular forces in defining material properties of protein nanofibrils. Science 318, 1900-1903 (2007).
111. Smith, J. F., Knowles, T. P. J., Dobson, C. M., MacPhee, C. E. &amp; Welland, M. E. Characterization of the nanoscale properties of individual amyloid fibrils. Proc. Natl Acad. Sci. USA 103, 15806-15811 (2006).
112. Dutt, A., Drew, M. G. B. &amp; Pramanik, A. Beta-sheet mediated self-assembly of dipeptides of Omega-amino acids and remarkable fibrillation in the solid state. Org. Biomol. Chem. 3, 2250 (2005).
113. Burkoth, T. S. et al. Structure of the beta-amyloid((10-35)) fibril. J. Am. Chem. Soc. 122, 7883-7889 (2000).
114. Chiti, F. &amp; Dobson, C. M. Protein misfolding, functional amyloid, and human disease. Annu. Rev. Biochem. 75, 333-366 (2006).
115. Dobson, C. M. Protein folding and misfolding. Nature 426, 884-890 (2003).

NATURE MATERIALS | VOL 8 | MARCH 2009 | www.nature.com/naturematerials

---

REVIEW ARTICLE

NATURE MATERIALS DOI: 10.1038/NMAT2387

116. Nguyen, H. D. &amp; Hall, C. K. Molecular dynamics simulations of spontaneous fibril formation by random-coil peptides. Proc. Natl Acad. Sci. USA 101, 16180 (2004).
117. Hwang, W., Zhang, S. G., Kamm, R. D. &amp; Karplus, M. Kinetic control of dimer structure formation in amyloid fibrillogenesis. Proc. Natl Acad. Sci. USA 101, 12916-12921 (2004).
118. Gruenbaum, Y., Margalit, A., Goldman, R. D., Shumaker, D. K. &amp; Wilson, K. L. The nuclear lamina comes of age. Nature Rev. Mol. Cell Biol. 6, 21-31 (2005).
119. Burke, B. &amp; Stewart, C. L. Life at the edge: The nuclear envelope and human disease. Nature Rev. Mol. Cell Biol. 3, 575-585 (2002).
120. Lammerding, J. et al. Lamin A/C deficiency causes defective nuclear mechanics and mechanotransduction. J. Clin. Invest. 113, 370-378 (2004).
121. Prockop, D. J. &amp; Kivirikko, K. I. Collagens: molecular biology, diseases, and potentials for therapy. Annu. Rev. Biochem. 64, 403-434 (1995).
122. Byers, P. H., Wallis, G. A. &amp; Willing, M. C. Osteogenesis imperfecta: translation of mutation to phenotype. J. Med. Genet. 28, 433-442 (1991).
123. Gautieri, A., Vesentini, S., Redaelli, A. &amp; Buehler, M. J. Single molecule effects of osteogenesis imperfecta mutations in tropocollagen protein domains. Protein Sci. 18, 161 - 168 (2009).
124. McBride, D. J., Choe, V., Shapiro, J. R. &amp; Brodsky, B. Altered collagen structure in mouse tail tendon lacking the  $\alpha 2(\mathrm{I})$  chain. J. Mol. Biol. 270, 275-284 (1997).
125. Miller, A., Delos, D., Baldini, T., Wright, T. M. &amp; Camacho, N. P. Abnormal mineral-matrix interactions are a significant contributor to fragility in oim/oim bone. Calcif. Tissue Int. 81, 206-214 (2007).
126. Sims, T. J., Miles, C. A., Bailey, A. J. &amp; Camacho, N. P. Properties of collagen in OIM mouse tissues. Connect. Tissue Res. 44, 202-205 (2003).
127. Grabner, B. et al. Age- and genotype-dependence of bone material properties in the osteogenesis imperfecta murine model (oim). Bone 29, 453-457 (2001).
128. Camacho, N. P. et al. The material basis for reduced mechanical properties in oim bones. J. Bone Mineral. Res. 14, 264-272 (1999).
129. Fratzl, P., Paris, O., Klaushofer, K. &amp; Landis, W. J. Bone mineralization in an osteogenesis imperfecta mouse model studied by small-angle X-ray scattering. J. Clin. Invest. 97, 396-402 (1996).
130. Rauch, F. &amp; Glorieux, F. H. Osteogenesis imperfecta. Lancet 363, 1377-1385 (2004).
131. Miller, E., Delos, D., Baldini, T., Wright, T. M. &amp; Camacho, N. P. Abnormal mineral-matrix interactions are a significant contributor to fragility in oim/oim bone. Calcif. Tissue Int. 81, 206-214 (2007).
132. Misof, K., Landis, W. J., Klaushofer, K. &amp; Fratzl, P. Collagen from the osteogenesis imperfecta mouse model (oim) shows reduced resistance against tensile stress. J. Clin. Invest. 100, 40-45 (1997).

133. Chavassieux, P., Seeman, E. &amp; Delmas, P. D. Insights into material and structural basis of bone fragility from diseases associated with fractures: How determinants of the biomechanical properties of bone are compromised by disease. Endocrine Rev. 28, 151-164 (2007).
134. Hudson, B. G., Tryggvason, K., Sundaramoorthy, M. &amp; Neilson, E. G. Alport's syndrome, Goodpasture's syndrome, and type IV collagen. N. Engl. J. Med. 348, 2543-2556 (2003).
135. Guck, J. et al. Optical deformability as an inherent cell marker for testing malignant transformation and metastatic competence. Biophys. J. 88, 3689-3698 (2005).
136. Cross, S. E., Jin, Y.-S., Rao, J. &amp; Gimzewski, J. K. Nanomechanical analysis of cells from cancer patients. Nature Nanotech. 2, 780-783 (2007).
137. Dao, M., Lim, C. T. &amp; Suresh, S. Mechanics of the human red blood cell deformed by optical tweezers. J. Mech. Phys. Solids 51, 2259-2280 (2003).
138. Engler, A. J., Sen, S., Sweeney, H. L. &amp; Discher, D. E. Matrix elasticity directs stem cell lineage specification. Cell 126, 677-689 (2006).
139. Scheibel, T. et al. Conducting nanowires built by controlled self-assembly of amyloid fibers and selective metal deposition. Proc. Natl Acad. Sci. USA 100, 4527-4532 (2003).
140. Humphrey, W., Dalke, A. &amp; Schulten, K. VMD: Visual molecular dynamics. J. Mol. Graphics 14, 33 (1996).
141. Herrmann, H., Bar, H., Kreplak, L., Strelkov, S. V. &amp; Aebi, U. Intermediate filaments: from cell architecture to nanomechanics. Nature Rev. Mol. Cell Biol. 8, 562-573 (2007).
142. Lantz, M. A. et al. Stretching the alpha-helix: a direct measure of the hydrogen-bond energy of a single-peptide molecule. Chem. Phys. Lett. 315, 61-68 (1999).
143. www.nature.com/horizon/proteinfolding/highlights/figures/s3_nonspec1_f1.html.

## Acknowledgements

This research was supported by the Army Research Office (W911NF-06-1-0291), the National Science Foundation (CAREER Grant CMMI-0642545 and MRSEC DMR-0819762), the Air Force Office of Scientific Research (FA9550-08-1-0321), the Office of Naval Research (N00014-08-1-00844) and the Defense Advanced Research Projects Agency (DARPA) (HR0011-08-1-0067). M.J.B. acknowledges support through the Esther and Harold E. Edgerton Career Development Professorship. We thank L. Kreplak, U. Aebi, H. Herrmann, P. Fratzl, M. Rief, H. Gaub, T. Scheibel and K. Dahl for communications.

NATURE MATERIALS | VOL 8 | MARCH 2009 | www.nature.com/naturematerials
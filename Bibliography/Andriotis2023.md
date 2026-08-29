Acta Biomaterialia 163 (2023) 35-49

ELSEVIER

Contents lists available at ScienceDirect

Acta Biomaterialia

journal homepage: www.elsevier.com/locate/actbio

Acta Biomaterialia

Review article

# Mechanics of isolated individual collagen fibrils

Orestis G. Andriotis, Mathis Nalbach, Philipp J. Thurner*

Institute for Lightweight Design and Structural Biomechanics, TU Wien, Vienna, A-1060, Austria

# ARTICLE INFO

Article history:

Received 30 March 2022

Revised 15 November 2022

Accepted 5 December 2022

Available online 10 December 2022

Keywords:

Collagen

Structure-function relationship

Mechanics

# ABSTRACT

Collagen fibrils are the fundamental structural elements in vertebrate animals and compose a structural framework that provides mechanical support to load-bearing tissues. Understanding how these fibrils initially form and mechanically function has been the focus of a myriad of detailed investigations over the last few decades. From these studies a great amount of knowledge has been acquired as well as a number of new questions to consider. In this review, we examine the current state of our knowledge of the mechanical properties of extant fibrils. We emphasize on the mechanical response and related deformation of collagen fibrils upon tension, which is the predominant load imposed in most collagen-rich tissues. We also illuminate the gaps in knowledge originating from the intriguing results that the field is still trying to interpret.

# Statement of significance

Collagen is the result of millions of years of biological evolution and is a unique family of proteins, the majority of which provide mechanical support to biological tissues. Cells produce collagen molecules that self-assemble into larger structures, known as collagen fibrils. As simple as they appear under an optical microscope, collagen fibrils display a complex ultrastructural architecture tuned to the external forces that are imposed upon them. Even more complex is the way collagen fibrils deform under loading, and the nature of the mechanisms that drive their formation in the first place. Here, we present a cogent synthesis of the state-of-knowledge of collagen fibril mechanics. We focus on the information we have from in vitro experiments on individual, isolated from tissues, collagen fibrils and the knowledge available from in silico tests.

© 2022 The Authors. Published by Elsevier Ltd on behalf of Acta Materialia Inc.

This is an open access article under the CC BY license (http://creativecommons.org/licenses/by/4.0/)

# 1. Introduction

Ancient cultures (Greeks and Romans) used collagen as the original source of glue. Glue was made through denaturation, i.e., boiling, of collagen-rich biological tissues such as bones, tendons and skin. Hence, the name collagen, which in Greek means, a glue-generating substance (from the latinized form of Greek kolla "glue" + -gen "giving birth to"). In a wider context, we may consider collagen to be the glue that holds cells, biological tissues, and ultimately human bodies together. Importantly, collagen is much more than that; it provides both macroscopic mechanical function and microscopic mechanical feedback in the human body.

Collagen stands for a superfamily of closely related, but genetically distinct molecules. To date, 28 different types of collagen have been identified in vertebrates, which are encoded by 44 genes [1]. The 28 members of the collagen superfamily have been further classified, based on the supramolecular architecture collagen molecules form. An in-depth information on the collagen family can be found in the review by Ricard-Blum [2] and further introduction to collagen structure and mechanics at various length scales can be found in the book edited by Fratzl [3]. In brief, fibril-forming collagens, as the name implies, self-assemble (in the extra-cellular space) into heterotypic collagen fibrils from collagen types I, II, III, V, XI, XXIV and XXVII. Collagen fibrils are reported to possess a semi-crystalline ultrastructure [4]. Importantly, collagen fibrils are heterotypic, i.e. they are built up by a mixture of the different types of fibril-forming collagen molecules. Studies focused on the mechanics of individual collagen fibrils have been conducted on samples sourced from tendons. Such collagen fibrils, are sometimes confusingly mentioned as collagen type I, but they are in fact heterotypic made up of a mixture of collagen type I, III

https://doi.org/10.1016/j.actbio.2022.12.008

1742-7061/© 2022 The Authors. Published by Elsevier Ltd on behalf of Acta Materialia Inc. This is an open access article under the CC BY license

(http://creativecommons.org/licenses/by/4.0/)

---

and V molecules [5,6]. The fibril-forming collagen type I is found in a variety of biological tissues across the body such as bones, skin, tendons, ligaments, sclera, cornea and in blood vessels [21]. Accounting for about 90% of collagen, type I is the most ubiquitous of all collagens. As such, collagen type I molecules are found in the highest concentration compared to type III and V. But lungs [7] and skin [8] contain relative amounts of type III to type I higher compared to the relative amount found in tendons (or ligaments) [9]. To date, studies on individual collagen fibril mechanics focused on samples primarily sourced from tendons, mainly because of the ease of extracting intact collagen fibrils and hence our review implicitly considers collagen types I, III and V.

Other collagen subgroups, not considered in detail in this review, are the fibril-associated collagens with interrupted triple helices (FACITs; type IX, XII, XIV, XVI, XIX, XX, XXI, XXII), the network forming collagens (type IV, VI, VII, VIII and X), the transmembrane collagens or also known as membrane-associated collagens with interrupted triple helices (MACITs; types XIII, XVII, XXIII, XXV), the multiplexins (types XV and XVIII) and two, currently, unclassified collagen types, the type XXVI and XXVIII.

More than 25% of the total protein mass content of the human body is composed by collagen [10]. This makes collagen one of the most abundant extracellular matrix (ECM) components in multicellular organisms. In an evolutionary sense, collagen is strongly conserved; vertebrates and echinoderms, share genetically almost identical collagen types. The primary function of collagen is to provide structural support and mechanical function, particularly in collagen-rich tissues. Being the main structural proteins of ECM and therefore of the cell microenvironment, collagens play a role in cell behavior, and are involved in cell adhesion [11] and migration [12], [13], [14], [15]. In this context, collagen fibrils contribute to tissue remodeling during growth [16], [17], [18], differentiation [19] and wound healing [20].

Collagen fibrils bear a unique architecture [4], which is similar across different biological tissues. Nevertheless, these tissues deliver a broad spectrum of functions characterized by different mechanical properties. In musculoskeletal tissues, collagen fibrils facilitate the force transfer from muscles to tendons and bones to support locomotion. In the lungs, collagen fibrils and their microscale organization in both the airways and the parenchyma provide the structural stability necessary during breathing [22,23]. Chronic lung pathologies such as asthma [24,25] and idiopathic pulmonary fibrosis [26] leading to impaired lung functionality from nanoscale alterations at the collagen fibril level, manifest the importance of collagen fibril mechanics for lung mechanics and function. In the cornea, the narrow diameter distribution of collagen fibrils and their unique highly aligned and highly packed organization into lamellae [27] forms a tissue transparent to the visible spectrum of light, facilitating the ability of sight and vision. Additionally, in the cornea, collagen fibrils and their organization greatly contribute to the mechanical strength required for sustaining corneal curvature [28].

Molecular structure [29], post-translational modifications [30,31], intrafibrillar cross-linking [32], [33], [34] and collagen type [35] are some of the various parameters responsible for the specific mechanical function and properties of individual collagen fibrils. However, exactly how the mechanics of collagen fibrils are specified and what the mechanical properties entail is a matter of ongoing research: how do collagen fibrils achieve the variety of mechanical functionalities required by the different tissues, which mechanisms are at work and how are these combined or interdependent on each other? Seeking answers to these questions by studying collagen fibril mechanics has been the focus of a number of studies [29,31], [32], [33], [34,36], [37], [38], [39], [40], [41], [42], [43], [44,45], [46], [47], [48], [49], [50], [51], [52], [53], [54], [55], [56], [57], [58], [59], [60], [61], [62], [63], [64], [65], [66], [67], [68], [69], [70], [71], [72], [73], [74].

Collagen fibrils should not be considered merely passive elements of the ECM. Instead, constant and tissue-dependent collagen fibril remodeling provides for a more dynamic interplay with cells. In addition, the formation of collagen fibrils seems highly dependent on the forces applied to them or their unassembled components. Collagen fibrils play a pivotal role for cell behavior [11,75,76] and the dynamic mechanobiological interplay between cells and collagen fibrils enriches our current understanding of their role in tissue homeostasis and cell mechanotransduction in health and disease. Efforts have been made for mechanistic models to describe collagen fibril mechanics [40,44,77,78]. But there is yet a gap in knowledge to be filled, rising from the fact that the current models either do not or use only a small amount of unbound water and are limited to small spatial and temporal simulation times. Also the molecular dynamics simulations aiming to mechanistically explain collagen fibril mechanics, are either employed on structural models of a theoretical subunit of collagen fibrils [4] or simplify the structure through coarse grain models [41], yet in both cases simulating the case of a dehydrated collagen fibril.

In this review, we will discuss the current state-of-the-art of the mechanical properties of isolated and individual collagen fibrils measured in vitro. Importantly, we make the distinction, for this review, of focusing only on mechanics and related studies assessing individual and isolated collagen fibrils rather than a collection of fibrils or a fibril within a collection of other fibrils.

## Origin of collagen fibril samples

Included studies in this review tested either a) native collagen fibrils isolated mechanically from tissues, such as tendons, the dermis of the Cucumaria frondosa and human biopsies, b) or reconstituted collagen fibrils from soluble collagen in acetic acid solution. Soluble collagen can either be prepared [79] or purchased, and native-type collagen fibrils are formed from that solution as a result of the intrinsic property of collagen to self-assemble. In vitro reconstitution of collagen fibril from solution takes place, as proposed by Holmes et al. [80] by diluting, neutralizing and warming of the collagen solution. A list of the publications and the sample origin is included in Table 1.

## Quantifying the mechanics of individual collagen fibrils

The mechanics of individual collagen fibrils have experimentally been studied via atomic force microscopy (AFM) or micro-electromechanical system (MEMS) devices and in different loading scenarios. Nanoindentation [49,69,81] and bending [71], [72], [73] tests have been conducted with AFM. Moreover, nanotensile tests have been conducted with AFM [33,36,58,63], [64], [65,82], MEMS [42,51,60,61] devices, while also dedicated instruments [34,83] were developed to overcome the low-throughput of both AFM- and MEMS-based tests. To date, these mechanical tests have been conducted in various environmental conditions, i.e. from air-dried, controlled-humidity to fully submerged in aqueous solutions and/or with varying salt concentration and pH [42,45,46,49,51,60,61,[69], [70], [71], [72], [73],81].

Since the first tensile tests of collagen fibrils were reported [65], 94 collagen fibrils were mechanically characterized under tension with AFM- and MEMs-based tests, 66 of which were tested while hydrated and the rest 15 while air-dried [33,36,42,51,[60], [61], [62], [63], [64], [65],71,82]. Svensson et al. [34] increased the specimen number tested in tension by developing a device using a) a piezoelectric actuator to apply and measure displacement, and b) a microscopic cantilever with a capacitance sensor to measure the applied force. The device developed by Svensson et al. [34] offers high throughput tensile testing of collagen fibrils [34] up to fracture but suffers from noise at low forces compared to an AFM (due to the long cantilever that has natural oscillating frequencies of tenths of Hz) and lacks the

---

Table 1
Indentation modulus of individual collagen fibrils, native and reconstituted, (deposited on a stiff substrate) measured via indentation-type AFM.

|  Indentation modulus, Eind | Key finding | Environment & Conditions | Analysis method | Contact (AFM tip/sample) | ~kAFM (N/m) | Indentation depth1 | Sample origin | Ref.  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  1-2 Gpa2 | Eind increases above 10% indentation depth | Air-dry (<45% humidity) | Hertz | Sphere/cylinder | 1 - 2 | n/a | Cucumaria frondosa - native | [49]  |
|  5-11.5 GPa | Employed Oliver-Pharr method | Air-dry | Oliver-Pharr | Sphere/flat; Ac(h) = π (2Reffh - b2) | 4.5 | h/D3 ≤ 0.1 | Rat tail tendon - native | [69]  |
|  1.9 ± 0.5 GPa | Eind decreased from GPa to MPa upon hydration | Air-dry | Hertz | Sphere/sphere | 40 | h/D ≤ 0.4 | Bovine Achilles tendon - reconstituted | [45]  |
|  1.2 ± 0.1 MPa |  | Buffer (100 mM sodium phosphate pH7) | Hertz | Sphere/flat | 0.3 | h/D ≤ 0.4 | Bovine Achilles tendon - reconstituted | [45]  |
|  2.1 ± 0.4 MPa - 172.5 ± 59 MPa | Eind can be tuned upon exposure to solutions | Various solutions (salt, pH and ethanol) | Hertz | Sphere/sphere | 0.3 | h/D ≤ 0.4 | Bovine Achilles tendon - reconstituted | [46]  |
|  1.2 - 2.2 GPa | Eind higher in overlap compared to gap regions | Air-dry | Hertz; elliptical contact area | Sphere/cylinder | 4.1 | h/D ≤ 0.05 | Bovine Achilles tendon - reconstituted | [54]  |
|  7.0 ± 1.5 GPa | Validation study: Reconstructed AFM tip shape. Compared AFM-based nanoindentation vs. conventional nanoindentation on polymers as well as various data analysis for collagen fibril characterization | Air-dry | Hertz | Sphere/sphere | 40 | h/D ≤ 0.1 | WT4 mice tail tendon - native | [81]  |
|  6.9 ± 1.5 GPa |  | Air-dry | Hertz | Sphere/cylinder | 40 | h/D ≤ 0.1 | WT mice tail tendon - native | [81]  |
|  9.3 ± 1.3 GPa |  | Air-dry | Oliver-Pharr | Sphere/flat; Ac(h) = π (2Reffh - b2) | 40 | h/D ≤ 0.1 | WT mice tail tendon - native | [81]  |
|  9.4 ± 1.7 GPa |  | Air-dry | Oliver-Pharr | Empirical function5 | 40 | h/D ≤ 0.1 | WT mice tail tendon - native | [81]  |
|  3.2 ± 1.1 GPa |  | Air-dry | Oliver-Pharr | Empirical function | 40 | h/D ≤ 0.1 | Rat tail tendon - native | [81]  |
|  6.6 ± 0.7 GPa |  | Air-dry | Oliver-Pharr | Empirical function | 40 | Human bronchi - native | [81] |   |
|  ~2-50 Mpa6 | Eind a. increased with indentation speed b. decreased upon exposure to temperature | Nanopure water | Sneddon | Conical tip | 0.7 | h ~30 nm | Rat tail tendon - native | [39]  |
|  ~1-10 Mpa7 |  | Nanopure water | Sneddon | Conical tip | 0.25 | h ~30 nm | Rat tail tendon - native | [39]  |
|  7.9 ± 2.8 GPa | Lower packing density in air-dried OIM fibrils, resulting in lower Eind vs. WT ones | Air-dry | Oliver-Pharr | Empirical function | 40 | h/D ≤ 0.1 | WT mice tails tendons - native | [31]  |
|  5.3 ± 2.2 GPa |  | Air-dry | Oliver-Pharr | Empirical function | 40 | h/D ≤ 0.1 | OIM8 mice tails tendons - native | [31]  |
|  3.3 ± 0.5 MPa | Less hydration in OIM collagen fibrils resulted in higher Eind vs. WT ones | PBS9 (pH7.4) | Oliver-Pharr | Conical with spherical apex | 0.32 - 0.48 | h/D ≤ 0.1 | WT mice tails tendons - native | [31]  |
|  16.2 ± 3.0 MPa |  | PBS (pH7.4) | Oliver-Pharr | Conical with spherical apex | 0.32 - 0.48 | h/D ≤ 0.1 | OIM mice tails tendons - native | [31]  |
|  17.3 ± 3.9 MPa | Eind reduced over damaged ("kinked") regions of the fibrils | PBS (pH7.4) / Control | Sneddon | Conical | 0.7 | Fitted portion for h/D = 0.1 | Bovine tail tendons - native | [38]  |
|  6.6 ± 2.1 MPa |  | PBS (pH7.4) / Kinked | Sneddon | Conical | 0.7 | Fitted portion for h/D = 0.1 | Bovine tail tendons - native | [38]  |
|  2.1 ± 1.2 MPa |  | PBS (pH7.4) / Very kinked | Sneddon | Conical | 0.7 | Fitted portion for h/D = 0.1 | Bovine tail tendons - native | [38]  |
|  0.1 - 1.4 MPa | Eind increased with increasing concentration of collagen type I | PBS | Hertz | Sphere/sphere | 0.2 | h/D ≤ 0.15 | In vitro fibrillogenesis | [35]  |
|  ~15 Mpa | Eind increased up to 24-fold upon partial dehydration | PBS (pH7.4) | Sneddon | Conical | 0.48 | h/D ≤ 0.1 | WT mice tails tendons - native | [36]  |
|  ~370 Mpa |  | PBS (pH7.4) + 3.5M PEG10 | Sneddon | Conical | 0.48 | h/D ≤ 0.1 | WT mice tails tendons - native | [36]  |
|  Sphere (Ri)/cylinder (Rf) | Effective radius: Reff = √Rf2Rf / (Rf + Rf)  |   |   |   |   |   |   |   |
|  Sphere (Ri)/sphere (Rf) | Effective radius: Reff = RfRf / (Rf + Rf)  |   |   |   |   |   |   |   |
|  1 | Indentation depth is noted here as percentage of collagen fibril height, D  |   |   |   |   |   |   |   |
|  2 | Reduced modulus reported in Heim et al. (2007)  |   |   |   |   |   |   |   |
|  3 | h/D: ratio of indentation depth to fibril diameter, D. For h/D≤0.1, Bueckle's rule is satisfied [90].  |   |   |   |   |   |   |   |
|  4 | WT = wild type  |   |   |   |   |   |   |   |
|  5 | Empirical function of AFM tip determined after image reconstruction. AFM height image of TGT1 calibration grating  |   |   |   |   |   |   |   |
|  6 | Data from three collagen fibrils. Baldwin et al. (2014) showed how the indentation modulus increases up to 10-fold with indentation speed.  |   |   |   |   |   |   |   |
|  7 | Temperature exposure - indentation modulus decreased with increasing temperature exposure. Collagen fibrils were exposed to temperature, then cooled down to 25° and measured.  |   |   |   |   |   |   |   |
|  8 | OIM = osteogenesis imperfecta mouse  |   |   |   |   |   |   |   |
|  9 | PBS = phosphate buffer saline  |   |   |   |   |   |   |   |
|  10 | PEG = poly-ethylene glycol  |   |   |   |   |   |   |   |

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

![img-0.jpeg](img-0.jpeg)

![img-1.jpeg](img-1.jpeg)

![img-2.jpeg](img-2.jpeg)
Fig. 1. (A) Three-dimensional view of an air-dried collagen fibril on a glass microscope slide. Collagen fibrils are identified by their characteristic D-periodicity. In a typical AFM cantilever-based nanoindentation test, the cantilever is driven towards the sample and deflects  $(\mathrm{d}_{\mathrm{max}})$  while a small portion of the AFM tip indents  $(\mathrm{h}_{\mathrm{max}})$  the surface of the sample (with permission from [81]). (B) Scanning electron microscopy and three-dimensional atomic force microscopy image of the reconstructed AFM tip apex, accompanied by the cross-sectional area as a function of the tip height (with permission from [36]). (C) Force volume map of an isolated individual collagen fibril. The force volume map is partitioned in a two-dimensional array of positions where the indents are conducted i.e., force-indentation data are recorded (with permission from [36]). (D) Cross-section height profile of the collagen fibril from which the diameter is determined (with permission from [36]). (E) Experimental force-indentation data (with permission from [81]).

![img-3.jpeg](img-3.jpeg)

![img-4.jpeg](img-4.jpeg)

control of force and displacement. The mechanics of collagen fibrils at high forces  $(&gt;100\mathrm{nN})$  up to fracture are important for informing tissue-level mechanics, whereas, studying collagen fibrils at low forces  $(&lt; 100\mathrm{nN}$ , forces the cells exert on their environment [84,85]) is important for mechanotransduction. A device recently developed by Nalbach et al. could bridge this gap [83] by performing tests under various loading scenarios i.e., quasistatic, dynamic loading, stress relaxation and creep tests (the latter currently not possible with most AFM instruments).

# 3.1. Nanoindentation tests

Atomic force microscopy cantilever-based nanoindentation is perhaps the most time-efficient test for mechanical characterization of individual collagen fibrils [45,46,49,69,71-73,81] and generally materials at the nanoscale.

AFM-based nanoindentation is easy to use, because of the minimal sample preparation and yields high-throughput data compared to bending or tensile tests at the nanoscale.

AFM also allows the identification of individual isolated collagen fibrils, via recognition of the characteristic D-banding or D-periodicity through contact- or intermittent contact mode imaging in air-dried state ( $\sim 67$  nm; periodic corrugations of the collagen fibril surface as seen in Fig. 1A). The sharp AFM tip apex (Fig. 1B), located at the end of a bendable cantilever, is used to perform

force-indentation tests (for example in a force volume map format; Fig. 1C) over a region of interest. The pixel resolution of the region of interest i.e., force volume map should be such that at least one pixel, i.e., a force-indentation test (Fig. 1D) will be conducted at the crest of the fibril. To analyze force-indentation data and provide an estimate of the indentation modulus, several theories and models based on contact mechanics can be used. What is important to know for data analysis is the shape of the projected contact which is defined by the geometry of the AFM tip apex and the sample. The AFM tip apex, is either assumed to have a perfect geometric shape (conical, spere, paraboloid) [38,39,45,46,49,69,86] or is experimentally reconstructed via (AFM) imaging a calibration grating [81], eventually providing an empirical function of the contact area (Fig. 1E). On the other hand, collagen fibrils have either been assumed as spheres or cylinders of radius R, and as flat.

Regardless of the limitations associated with nanoindentation tests on collagen fibrils, valuable knowledge has been gained over the last two decades on the mechanical behavior of collagen fibrils.

# 3.2. Nanotensile tests

The first nanotensile test methods were published in 2006 by Eppel et al. [42], who designed a micro-electro-mechanical system (MEMS) (Fig. 2A) and by van der Rijt et al. [65], who employed the atomic force microscope (AFM) in force spectroscopy

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

![img-5.jpeg](img-5.jpeg)

![img-6.jpeg](img-6.jpeg)

![img-7.jpeg](img-7.jpeg)

![img-8.jpeg](img-8.jpeg)
Fig. 2. Overview of the three different methods for tensile testing of individual, isolated collagen fibrils. (A) The MEMS platform (adapted from Liu et al. [52] with permission). The collagen fibril is suspended between the fixed end and strain gage pad. The strain gage pad is connected to the moving pad via beams of known stiffness. Displacement of the moving pad causes deflection of the beams that is proportional to the force exerted on the collagen fibril. The deflection is measured optically. (B) With the AFM method, a segment of a collagen fibril is glued to the substrate and the AFM cantilever with epoxy resin. By an upward translation of the cantilever, the collagen fibril is deformed and the force exerted is proportional to the measured cantilever deflection (adapted with permission from [36]). (C) Bowstring stretching with the AFM. The collagen fibril is glued to the substrate on two sites and subsequently loaded in a bowstring geometry. The force is measured by torsional bending of the cantilever. (D) NanoTens instrument (from Nalbach et al. [83], with permission under CC BY 4.0). A magnetic microsphere is glued to the collagen fibril. By application of an external magnetic field, the magnetic microsphere is lifted and picked up with a fork-like gripper that is mounted on a fiber-optic force probe. The force, proportional to the cantilever deflection, that arises due to an upward movement of the force probe is measured with an interferometer.

mode (Fig. 2B) for tensile testing of individual isolated collagen fibrils. Both methods were further adapted to enable dynamic tensile tests of fully hydrated collagen fibrils up to failure [33,52,60,71]. In 2016, a further AFM method was presented by Quigley et al. [58], who loaded collagen fibrils in a bowstring geometry (Fig. 2C), in contrast to the force spectroscopy geometry. Svensson et al. [34,87] built a custom instrument to perform tensile studies by pulling the collagen fibril in the focal plane of a light microscope and optically measuring the local elongation of the collagen fibril. Recently, Nalbach et al. [83] developed a tensile testing device, the (NanoTens Fig. 2D), which allows for quick coupling and uncoupling of samples via a non-permanent connection between collagen fibrils and the force sensor.

# 4. Collagen fibril mechanics

# 4.1. Indentation modulus influenced by environmental/experimental factors

Hydration of collagen fibrils in an aqueous solution [31,36,45,46], reduced their indentation modulus by three-orders of magnitude (down to several MPa from GPa) and was accompanied by an increase in collagen fibril height (diameter) compared to the air-dried state. Conversely, dehydration of collagen fibrils in ethanol [31,46] or by exposing them to various concentrations of poly-ethylene glycol [36] increased their indentation modulus and decreased their height (or diameter).

Additionally, exposing collagen fibrils to temperatures above  $50^{\circ}\mathrm{C}$  and up to  $62^{\circ}\mathrm{C}$  decreased their indentation modulus, also

accompanied by an up to  $30\%$  increase of fibril height [39]. In the same study, Baldwin et al. [39] showed that increasing the indentation speeds above  $100~\mu \mathrm{m / s}$ , resulted in an increase of indentation modulus. In the above cases (with an exception to the effect of indentation speed), increase in indentation modulus was accompanied by a decrease in fibril height and vice versa.

Upon hydration, the axial separation between collagen molecules increases [88] and therefore the molecular packing density is reduced in the radial direction of the fibril. One may then conclude as a result of the decrease in molecular packing density (also manifesting upon exposure to higher temperatures), collagen molecules have more space to deform and rearrange upon an axial compressive load. Therefore, the molecules would be more compliant, which results in a reduced indentation modulus at the collagen fibril level.

The influence of indentation speed on indentation modulus highlights the time-dependent response to axial loading. As indentation speeds increase, certain relaxation mechanisms of the collagen molecules do not take place resulting in an apparent increase of molecular packing density and increase in indentation modulus.

# 4.2. Collagen fibril ultrastructure and indentation modulus

The D-periodicity of  $67~\mathrm{nm}$  in collagen fibrils is characterized by the overlap and gap regions because of a periodic offset of collagen molecules along the long axis of collagen fibrils [89]. Overlap regions have slightly higher packing density compared to the gap regions [89] and Minary-Jolandan et al. [54] and Grant et al.

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

[47] reported a slightly higher indentation modulus in the overlap compared to the gap regions.

Kink formations localized at damaged regions along collagen fibrils and sharp bents of the fibrils are also domains of the fibrils that have been associated with reduced indentation modulus [38,39]. The D-periodicity, damaged areas and bents of the fibrils show variations in the molecular packing density that has influenced the indentation modulus measured in these areas.

An intriguing question is, what makes collagen fibrils to kink periodically upon overload at the fascicle level or close to the fracture site of collagen fibrils? As speculated by Baldwin et al. [38], kinks could be the result of compressive load normal to the long fibril axis, once the normal tensile load is removed. Yet unknown is the origin of this periodic compressive load and why collagen fibril kink formations vary among tendon locations [68] and between collagen fibrils from positional and energy-storing tendons [56]. To this end, tensile tests on individual collagen fibrils by means of quasistatic, creep or stress relaxation, dynamic mechanical analysis performed in combination with structural assessment and molecular dynamics simulations may provide further insights.

Beyond changes in ultrastructure, the composition of collagen fibrils has been reported to influence the indentation modulus too. For example, in the osteogenesis imperfecta mouse (OIM) model, genetic mutations [31] resulting in primary structure alterations of collagen molecules, were associated with impaired hydration at the collagen fibril level and increased indentation modulus. In addition, a relative increase in the amount of collagen moleculestype III compared to type I constituting heterotypic collagen fibrils was associated with a reduction in the indentation modulus [35]. Although, the latter effect lacks a mechanistic explanation as to why this decrease in mechanics is influenced by the presence of collagen type III, in the case of OIM, the increase in indentation modulus of hydrated collagen fibrils (compared to WT ones) was suggested to result from changes in the molecular packing density due to less hydrated OIM compared to WT collagen fibrils [31].

# 4.3. Tensile behavior of collagen fibrils

Based on estimations of their length being  $14 - 50\mathrm{mm}$  [91], collagen fibrils have an aspect ratio in the range of  $14\times 10^{4} - 50\times$ $10^{4}$ . Because of this, collagen fibrils in mammals predominantly withstand tensile loads in vivo. Under tension, collagen fibrils show a non-linear elastic [36,65], viscous (time-dependent) [64,70], and

permanent damage behavior [33,56]. However, the non-linearity and viscous behavior do not necessarily arise from the same deformation mechanisms. Phenomenologically, the unique and distinct response of collagen fibrils under tension is described by a three-phase behavior (phase I, II and II; Fig. 3) [33].

# 4.3.1. Three-phase stress-strain evolution: deformation mechanisms

Collagen molecules, within the collagen fibril structure, show local variations along their structure characterized by kink formations and micro-unfolding of the triple helix [30,44]. The kinks are prevalent at the gap regions [4,44]. Molecular dynamics simulations predicted the different possible deformation mechanisms during tension of a collagen fibril to be straightening, uncoiling, intermolecular sliding, intramolecular sliding, and backbone stretching of collagen molecules [41,44,92,93].

Upon tension at lower forces molecular kinks straighten [44] and small regions of the triple helix uncoil [41], while at higher loads the backbone of the triple helix is stretched [44]. As predicted by Zhou et al. uncoiling and straightening take place at lower forces leading to lower stiffness, compared to backbone stretching of the collagen molecule, which leads to a higher stiffness [92]. Depalle et al. suggested these deformation mechanisms take place at increasing stretch levels upon fibril tension [41]. However, experiments yield varying results which suggest that the different deformation mechanisms may occur simultaneously with some being prevalent depending on load and sample conditions.

In phase I, straightening, and aligning of collagen molecules gradually takes place resulting in a convex "toe" region of the stress-strain evolution. From about  $2\%$  strain, this region transitions to an almost linear increase characterized by straightening and uncoiling of the collagen triple helix [41]. With increasing strain in phase I, intermolecular sliding starts to take place [41] until it, eventually, becomes the dominant deformation mechanism.

Phase II initiates at about  $10\%$  of fibril strain. Onset of phase II is characterised by a decline of the stress-strain slope, hence the tangent tensile modulus decreases (softening). Collagen fibrils with low intermolecular cross-link density, or containing only immature cross-links, deform to failure in phase II. In contrast, collagen fibrils with a sufficiently large number of mature or sugar-based intermolecular cross-links enter phase III at  $15\%$  to  $20\%$  strain [33]. Phase III is indicated by a second increase in the tangent tensile modulus. This increase is thought to be due to hindrance of further intermolecular sliding by intermolecular cross-links, resulting

![img-9.jpeg](img-9.jpeg)
Fig. 3. (A) Experimental tensile stress-strain curve up to fracture of a collagen fibril from human patellar tendon measured with AFM. The stress-strain curve shows three distinct phases. The presence of the three-phase stress-strain curves is assumed to be associated with different deformation mechanisms taking place in each phase. In phase I, collagen molecules are straightened, and uncoiled/unwound. In phase II, the collagen fibril begins to deform by intermolecular sliding, resulting in a decrease of the slope of the stress-strain diagram. In phase III, intermolecular cross-links restrict further intermolecular sliding, and the molecular backbone is stretched. This leads to an elevated resistance against deformation as shown by the increased slope in the stress-strain diagram. The slope of the stress-strain diagram is plotted in B and corresponds to the tangent modulus. One can observe two local maxima of the tangent modulus, one in phase I and one in phase III. In case of reduced intermolecular cross-link density, the collagen fibril fails without distinct stiffening, i.e., the phase III behavior is absent. Image from Svensson et al. [33] with permission.

![img-10.jpeg](img-10.jpeg)

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

Table 2 Nanotensile properties of individual collagen fibrils, namely phase I and III tangent tensile modulus, strength and failure strain. Data is represented mean  $\pm$  std or geometric mean (geometric SE).

|  Phase I Tangent modulus (GPa) | Phase III Tangent modulus (GPa) | Strength (MPa) | Failure strain (%) | Sample origin | Method | Environment & Conditions | Reference  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  0.4 | n/a | n/a | n/a | Rat tail tendon 10 weeks old | AFM | Hydrated, phosphate-buffered saline (PBS) | [82]  |
|  1.1 | n/a | n/a | n/a | Cross-linked with glutaraldehyde | AFM | Hydrated, PBS | [82]  |
|  0.5 ± 0.4 | n/a | 230 ± 160 | 80 ± 44 | Sea cucumber (dermis) | MEMS | Hydrated, PBS | [60]  |
|  0.08 - 0.25 |  | n/a | n/a | Sea cucumber (dermis) | MEMS | Hydrated, PBS | [61]  |
|  0.6 ± 0.2 | n/a | 60 ± 10 | 13 ± 2 | Bovine Achilles tendon - reconstituted | AFM | Hydrated, PBS | [71]  |
|  0.7 ± 0.1 | n/a | 170 ± 10 | 30 ± 2 | Cross-linked with EDC/NHS | AFM | Hydrated, PBS | [71]  |
|  1.8 ± 0.3 | n/a | 290 ± 10 | 22 ± 2 | Cross-linked with glutaraldehyde | AFM | Hydrated, PBS | [71]  |
|  3.5 ± 0.4 | 4.3 ± 1.4 | 540 ± 140 | 20 ± 1 | Human patellar tendon | AFM | Hydrated, PBS | [33]  |
|  2.2 ± 0.9 | n/a | 200 ± 110 | 16 ± 4 | Rat tail tendon, 12 weeks old | AFM | Hydrated, PBS | [33]  |
|  0.3 ± 0.1 | n/a | 71 ± 23 | 63 ± 21 | Rat patellar tendon | MEMS | Not specified (presumably hydrated in PBS) | [52]  |
|  1.8 - 4.8 | n/a | 638 - 1134 | n/a | Reconstituted collagen fibril from calf skin | MEMS | Ambient, 60% relative humidity | [51]  |
|  1.6 (1.3 - 2.0) | n/a | 80 (70-100) | 20 (16-25) | Rat tail tendon, 16 weeks | Custom | Hydrated, PBS | [34]  |
|  2.8 (2.4 - 3.1) | 6.0 (3.5-10.3) | 420 (310-570) | 23 (20-26) | Cross-linked with MGO | Custom | Hydrated, PBS | [34]  |
|  2.0 (1.6 - 2.4) | 2.6 | 150 [120-190] | 14 (11-18) | Rat Achilles tendon, 16 weeks | Custom | Hydrated, PBS | [34]  |
|  2.4 (2.3-2.6) | 4.7 (3.3-6.8) | 410 [330-500] | 37 (31-45) | Cross-linked with MGO | Custom | Hydrated, PBS | [34]  |
|  0.4 - 0.8 | n/a | n/a | n/a | Mice tail tendon, 6-month-old | AFM | Hydrated, PBS | [36]  |
|  3.9 ± 0.7 | 9.1 ± 4.0 | 1020 ± 330 | 26.6 ± 3.1 | Human patellar tendon, male, 26 ± 6 years old | Custom | Hydrated, PBS | [32]  |
|  4.6 ± 1.3 | 10.8 ± 3.3 | 1210 ± 280 | 26.9 ± 3.6 | Human patellar tendon, male, 66 ± 1 years old | Custom | Hydrated, PBS | [32]  |
|  0.1 - 1.0 | n/a | n/a | n/a | Reconstituted collagen fibril from calf skin | MEMS | Hydrated, PBS | [70]  |

in an increase of shear resistance [33,41]. Hence, increased tensile load is exerted directly onto the bonded chains of the molecules, and the molecular backbones are stretched. Table 2 summarizes a selection of the tensile mechanical properties of individual collagen fibrils measured in aqueous solution only.

# 4.3.2. Non-linear stress-strain evolution in phase I

A modulus has often been calculated from the first derivative of stress vs. strain and presented as a function of strain [32-34,62,63,65], which we refer to as tangent modulus. The majority, if not all, of current literature reports tangent moduli data from the loading curve only, because to date tests conducted a single cycle until fracture [32-34,62,63]. We believe that subsequent studies relied on the tangent modulus of the loading curve to crosscompare values with preceding literature. However, this may be less intuitive because only the unloading part of the curve, before permanent damage settles in, would reflect the elastic response of the collagen fibril.

The tangent modulus in phase I has been reported to range from 0.4 GPa, for collagen fibrils from rat tail tendon of an animal at 10 weeks age [65], up to  $(4.6 \pm 1.3)$  GPa for human patellar tendon collagen fibrils of patients at  $(66 \pm 1)$  years age [87].

# 4.3.3. Effect of hydration in phase I

Hydration and intermolecular cross-linking have also shown to affect the tangent modulus which was decreased upon hydration from 5 GPa to 0.5 GPa (collagen fibrils from rat tail tendon) [65] and from 0.9 GPa to 0.5 GPa (collagen fibrils from sea cucumber) [60]. Corroborated by AFM cantilever-based nanoindentation tests, hydration of collagen fibrils results in increased intermolecular separation is increased due to the presence of higher amount of water molecules found as bound and unbound (bulk) water within the fibril (Fig. 4A). At native hydration, a monolayer of water is

expected to build around collagen molecules (Fig. 4B) [88,94,95]. Weak intermolecular forces decrease with hydration resulting in facilitated molecular deformation mechanisms.

Andriotis et al. [36] systematically explored and quantified the impact of partial dehydration by exerting osmotic pressure on collagen fibrils within buffer solution. They achieved this by adding poly-ethylene glycol (PEG) of different concentrations to phosphate buffered saline (PBS) in between tensile tests on a single collagen fibril from a mouse tail tendon. The tensile modulus increased by up to 6-fold in partially hydrated collagen fibril in  $2.6\mathrm{M}$  PEG compared to the exact same fibril fully hydrated in PBS. By AFM nanoindentation, collagen fibrils were found to shrink in presence of higher osmotic pressure by about  $15\%$  applying the same dehydration protocol. The effect of partial dehydration was gradually increasing with increasing PEG concentration leading to the conclusion that collagen fibril mechanical properties can be tuned by hydration and osmotic pressure. This is in agreement with results from studies that employed MEMS devices where experiments are conducted in a controlled humidity environment, but not in a fully hydrated aqueous solution [51,60,70].

# 4.3.4. Effect of intermolecular cross-links in phase I

Intermolecular cross-linking, i.e., covalent bonds between adjacent collagen molecules, is the second proposed mechanism to influence the collagen fibril tensile properties at  $&lt; 10\%$  strain. Physiologically, two main types of cross-links have been identified in collagen-rich tissues a) enzymatic (subdivided into immature and mature) and b) non-enzymatic (sugar-induced) cross-links [96,97].

For studying the effect of enzymatic (i.e. physiological) occurring cross-links on collagen fibril mechanics, collagen fibrils from energy storing tendons, e.g., patellar, Achilles' or superficial digital flexor tendons (SDFT) have been compared to ones from positional tendons, e.g., tail or common digital extensor tendons

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

![img-11.jpeg](img-11.jpeg)

![img-12.jpeg](img-12.jpeg)
Fig. 4. (A) High osmotic pressure results in lower intermolecular distance. Weak intermolecular interactions change proportionally resulting in the stiffness being a function of the water concentration. At lower water concentration (purple-brown) or intermolecular distance the collagen fibril is stiffer compared to collagen fibrils with high water concentration (yellow). The figure is adapted with permission from Andriotis et al. [36]. (B) The tiple helix of a 30-residue long part of a collagen molecule (PDB: 1CGD) is shown on top without and below with the water monolayer as predicted by [95], with permission under a CC By 4.0 license from the RCSB PDB (10.2210/pdb1CGD/pdb).

(CDET) [33,34,98]. This is because these tendons show differences in the cross-link profile and density [98].

The effect of nonenzymatic cross-linking on fibril mechanics, has been investigated by either a) in vitro cross-linking collagen fibrils with a methylglyoxal (MGO; a fast reacting agent mimicking the formation of cross-links between lysine and arginine residues [97]) or b) by testing collagen fibrils harvested by young and old individuals [87]. Both enzymatic and non-enzymatic cross-links form at specific locations on the collagen molecules. There were however studies in which artificial unspecific cross-linking was investigated via 1-ethyl-3-(3-dimethyl-aminopropyl) carbodiimide hydrochloride (EDC) in the presence of N-hydroxysuccinimide (NHS) [71] and glutaraldehyde [71,82]. Below we narrow our discussion to the enzymatic and non-enzymatic cross-links.

Enzymatic cross-links: Svensson et al. attributed the higher tangent moduli in collagen fibrils from human patellar tendon compared to rat tail tendon samples (3.5 GPa vs. 2.2 GPa) to the higher concentration of mature enzymatic HP cross-links in the human patellar tendons (890 mmol/mol), compared to rat tail one (8.7 mmol/mol) [33]. Additionally, Svensson et al. reported an increase of the mature HP cross-link with age in both Achilles' (90 vs. 278 mmol/mol) and tail tendon (0 vs. 2 mmol/mol) [34].

Non-enzymatic cross-links: Svensson et al. did not find significant differences in the tangent modulus of fibrils due to age and tissue type, i.e. collagen fibrils from tail and Achilles' tendons [34]. However, tangent modulus in collagen fibrils from Achilles' tendons increased from 1.9 GPa in to 2.6 GPa after MGO treatment [34].

Because of the inconsistency with previous results comparing human patellar and rat tail tendons, this raised the question of

whether human patellar tendon collagen fibrils reach a maximum value for tensile modulus due to a finite number of possible crosslinking sites along a collagen molecule. A small number of human patellar tendon samples, which Svensson et al. cross-linked with MGO only resulted in a modest increase in tensile modulus opposed to the strong increase previously seen in rat tail and Achilles' tendon samples [34].

Experiments show that cross-linking increases the tangent modulus in phase I. The large divergence of phase I tangent moduli in different species and between specific cross-link densities is however elusive [33,34]. This raises the question, if a positive correlation between cross-link density and intermolecular spacing exists, which may originate in a superposition of hydration and crosslinking mechanisms [37].

In light of the results obtained from multiscale modeling, the influence of cross-links on the phase I tangent moduli is puzzling [40,41]. Both Buehler [40] and Depalle et al. [41] did not find an effect of cross-link density on the phase I tensile modulus of collagen fibrils by molecular dynamics and multiscale models. But currently, there is no mechanistic explanation of how intermolecular cross-links contribute to the mechanical behavior at low strains.

Generally, the thought seems to be that the predominant deformation mechanisms in phase I are straightening and uncoiling. From this perspective it is not intuitive that cross-linking should influence phase I. Nevertheless, studies [32-34] report stiffer behavior in phase I in samples that exhibit higher concentration of some form of cross-links. One possible explanation is that intermolecular sliding is present already in phase I, but perhaps not dominant. If this sliding is inhibited by the cross-linking, the stiffness would increase in phase I. Performing creep experiments

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

![img-13.jpeg](img-13.jpeg)
Fig. 5. Stress-strain diagram of human patellar tendon, native and MGO cross-linked rat tail tendon collagen fibrils. All collagen fibrils were tested up to failure. The human patellar tendon fibril and the MGO cross-linked rat tail tendon fibril show a three-phase behavior with a distinct phase of stiffening from strains of about  $15\%$ . In contrast, the native rat tail tendon collagen fibril only shows a two-phase behavior. This figure is adapted from Svensson et al. [32], with permission under CC BY 4.0 license.

in phase I while intermolecular sliding is assumed to occur, one would expect a) not to reach a plateau in strain increase and b) failure should occur already in phase I. But recent studies [51,70] have not confirmed this which could suggest that intermolecular sliding does not take place but rather cross-linking inhibits uncoiling and straightening. This hypothesis seems to favor rather AGEs, to enzymatic cross-links, as the theoretical attainable concentration of AGEs per molecule is higher and not confined at the end regions of the collagen molecules.

# 4.3.5. Transitions phase I-II and phase II-III

Commencing with a strain of between  $5\%$  to  $10\%$  a gradual decrease of the tangent modulus is observed in stress strain curves (Fig. 3) this marks the transition from phase I to phase II. The current mechanistic interpretation for the decrease in stiffness and tangent modulus is molecular sliding, i.e., between adjacent collagen molecules [41]. Intermolecular sliding is thought to be the dominant deformation mechanism, analogous to stick-slip friction, and happens after most collagen molecules are straightened and (partly) uncoiled [40,41,99-101]. There is no strict definition or criterion of a force or strain threshold for the onset of phase II, so no quantitative value for the onset have been reported. Qualitatively, the decrease of tensile modulus and hence molecular sliding is observed for all types of collagen fibrils, independent from hydration [51] or cross-link density [33,34,56].

In phase II, cross-links play a well investigated role in the deformation mechanism. With increasing force and strain, cross-links restrict molecular sliding [40]. However, as experimentally reported by Svensson et al. [33] not all collagen fibrils show the ability to inhibit molecular sliding during tension. A subset of collagen fibrils deform until failure and shown only a phase II behavior [33]. In contrast, other collagen fibrils display a gradual increase of the tangent modulus at strain values of  $15\%$  to  $20\%$  [33,56]. This marks the onset to phase III behavior.

Phase III is governed by molecular backbone stretching [41]. Human patellar tendon samples did show three-phase behavior in contrast to rat tail tendon samples [33]. Fig. 5 shows the tensile three-phase stress-strain diagram of individual collagen fibrils originated from human patellar tendon, MGO cross-linked rat tail tendon, and the tensile two-phase stress-strain of a collagen fibril from native rat tail tendon.

Collagen fibrils from human patellar tendon bear a larger concentration of mature enzymatic HP cross-links than the ones from

rat tail tendons [33]. Tangent modulus of the human patellar tendon fibrils reached a mean of 4.3 GPa in phase III compared to 3.5 GPa in phase I. Quigley et al. [56] tested collagen fibrils sourced from two functionally distinct tendons, namely the positional CDET (common digital extensor tendon) and the energy storing SDFT (superficial digital flexor tendon) of 24-36 month old steer, up to fracture. Collagen fibrils from SDFT had a 0.8 GPa average tangent modulus in phase III, which was about  $15\%$  higher than the tangent modulus they reported for phase II. In contrast, collagen fibrils from CDET tendons did not show such an increase in tangent modulus at strains above  $10\%$ . In total, 19 out of 21 SDFT (energy storing) collagen fibrils while only 5 out of 17 CDET (positional) ones showed three-phase-behavior. As Quigley et al. [56] did not conduct assays to determine cross-link density they could not correlate chemical modifications with mechanical data. Nevertheless, based on previous data the observations by Quigley et al. were explained as in vivo tuning of the mechanical properties of individual collagen fibrils via mature cross-links to meet physiological requirements at the macro scale [56]. Svensson et al. used a similar approach, testing collagen fibrils from tendons with different physiological requirements [34]. In contrast to Quigley et al. [56], Svensson et al. did not observe three-phase-behavior for either, energy storing Achilles' or positional tail tendon collagen fibrils, sourced from 16-week-old Wistar rats despite observed difference in cross-link density of mature enzymatic HP cross-links (278 mmol/mol vs. 2 mmol/mol). The absence of phase III in Achilles' tendon collagen fibrils is at first glance contradictory to the findings in energy storing SDFT collagen fibrils by Quigley et al. [34,57,58], leading Svensson et al. to raise the question whether mature enzymatic cross-links are truly the sole cause of three-phase-behavior [34].

However, it is important to note that the cross-link density in the fibrils from Wistar rats Achilles tendon (278 mmol/mol) was much lower compared to fibrils from human patellar tendon previously investigated by Svensson et al. (890 mmol/mol). It seems that there is a critical concentration required to achieve three-phase behavior. This idea is also supported by coarse grain models of collagen fibrils [41]. Interestingly, Depalle et al. could only achieve three-phase-behavior in their models when doubling the strength of mature cross-links and above  $60\%$  cross-link densities, which corresponds to 1200 mmol/mol [41]. In contrast, the model by Depalle et al. did not show three-phase-behavior at a density of  $20\%$  (or concentration of 400 mmol/mol) of double-strong mature cross-links [41]. Nevertheless, Svensson et al. observed distinct three-phase-behavior after in vitro cross-linking the Wistar rat tail and Achilles' tendon collagen fibrils with MGO [33].

This suggests that in sufficient concentration, both mature enzymatic cross-links and AGE cross-links could produce phase III behavior. In this context, it is important to note, that three-phase behavior was never observed in collagen fibrils from rats or mice at tens of weeks of age, in contrast to collagen fibrils from energy-storing tendons of animals at tens of years of age. Even though there is experimental evidence that both, enzymatic and nonenzymatic cross-links, contribute to the overall mechanical behavior, it is not clear to which extent each type of the natural cross-links contribute individually. Molecular dynamics simulations by Buehler et al. hint the necessity of two cross-links per collagen molecule for substantial hardening to occur, while this effect is enhanced by the presence of mature, trivalent cross-links [40]. To further investigate this question, mechanical data of a wider age span, from weeks to tens of years of age, of one species in combination with comprehensive quantification of a broader range of enzymatic and non-enzymatic cross-links is required.

From the studies conducted to date, the consensus is that specific deformation mechanisms are dominant in phases I, II and III (Table 3), yet it is unclear if and how much deformation

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

Table 3 Description and dominance of the different deformation mechanisms during collagen fibril tensile stretching.

|  Deformation mechanism | Description | Phase | Reference  |
| --- | --- | --- | --- |
|  Straightening | Alignment of a collagen molecule by straightening of kinks and twisted segments | I | [44]  |
|  Uncoiling | Partial unfolding of helical domains, breaking of H-bonds | I | [40,44]  |
|  Intermolecular sliding | Shearing of one molecule with respect to one or more neighboring molecules | II | [43,104]  |
|  Backbone stretching | Alignment and stretching of peptide bonds with load direction | III | [40]  |
|   | Disentanglement of the alpha chains within one collagen molecule | III | [93]  |

![img-14.jpeg](img-14.jpeg)
Fig. 6. (A) AFM images of rupture sites of collagen fibrils that were tested up to failure. Two types of failure modes can be distinguished (with permission from Svensson et al. [33]). One type, that is largely intact over the entire length as determined by the presence of D-banding in the AFM images and the other type with a highly disrupted topography. (B) AFM image over the entire length of a collagen fibril of the latter type. (C) Confocal microscope image of the same collagen fibril after staining with CHP. Kinking and delamination as observed with the AFM correlates to molecular damage indicated by the fluorescence signal in confocal microscopy. One site, indicated with a white arrow in panels B and C, is intact and D-banding is present in the AFM image. (B) and (C) are from Quigley et al. [56] with permission under the CC BY 4.0 license.

mechanisms, dominant in one phase, also contribute to the other phases.

# 4.3.6. Damage of collagen fibril under tensile loading

Closely related to the diverging mechanical behavior at strain above  $10\%$  is the observation of diverging failure modes that seem to be associated with the cross-link density and the related deformation mechanism contributing to damage of individual collagen fibrils [40,41]. Svensson et al. [33] observed largely intact human patellar tendon collagen fibrils after loading to failure in contrast to heavily disrupted rat tail tendon collagen fibrils throughout the entire length. Quigley et al. further investigated the failure modes through AFM imaging, second harmonic generation (SHG) imaging microscopy and a collagen hybridizing peptide assay (CHP) of ruptured collagen fibrils of a positional and an energy storing tendon [57]. The surface of ruptured collagen fibrils from positional tendons is highly disorganized and shows delamination as well as kink formation in contrast to the highly organized D-banding in undisrupted collagen fibrils (Fig. 6) as determined by AFM imaging. Interestingly, delamination and kink formation are interrupted by small sections of intact D-banding. SHG imaging resulted in  $30\%$  reduction in maximum forward scattered intensity projection images of positional tendon collagen fibrils that indicate molecular level disruption. In energy storing tendon a reduction of only  $2\%$  was measured. Although SHG imaging allows for quantification of overall molecular damage, it does not discriminate between molecular alignment and molecular denaturation. To measure molecular denaturation solely, both types of ruptured collagen fibrils were stained with fluorescently labeled CHP. CHP binds to unfolded regions of the alpha chains of collagen molecules, i.e. by forming a triple helix with two of the unfolded alpha chains, but not native collagen [93], resulting in an increased fluorescence signal of denatured collagen fibrils, when performing confocal microscope imag

ing. Given the nature of CHP binding only those locations, damage here is defined by one alpha chain being pulled out of an initially intact collagen molecule resulting in a disruption of the triple helix. Only ruptured collagen fibrils from positional tendon showed an elevated fluorescent signal indicating collagen molecule damage (Fig. 6).

# 4.3.7. Cyclic loading

Molecular damaged within the collagen fibril occurs when an alpha chain is pulled out of the collagen molecule resulting in a disrupted and unfolded collagen molecule. To further assess molecular damage in the context of physiological repeated mechanical deformation, Iqbal et al. applied AFM imaging and a CHP assay on collagen fibrils from positional tendon after a single cycle test [50]. They found a sigmoidal relationship between mean fluorescence intensity and collagen fibril strain with a steep increase of the fluorescence intensity being between  $7\%$  and  $13\%$  strain. A similar observation was made by Zitnay et al. [93], who measured the fluorescence intensity of CHP stained collagen fascicles after a single stretch cycle. In comparison to results from molecular dynamics simulations, it is suggested that in a shear-dominated deformation, collagen alpha- chains from one collagen molecule, covalently bound via cross-links to alpha-chains of neighboring collagen molecules are pulled-out of the triple helical structure [99]. Damage in phase I was also inferred from observing the residual strain and hysteresis in other studies, in which collagen fibrils were cyclically loaded and unloaded. Van der Rijt et al. [65] cyclically loaded collagen fibrils, and observed residual strain and hysteresis, upon stretching a collagen fibril above  $90\mathrm{MPa}$  in a dry or above  $20\mathrm{MPa}$  in a hydrated state. The occurrence of residual strain after loading a collagen fibril is confirmed by the findings in several other studies [59,64,71]. Svensson et al. [64], however, did not measure residual strains after stretching collagen fibrils about to

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

![img-15.jpeg](img-15.jpeg)

![img-16.jpeg](img-16.jpeg)
Fig. 7. Stress-strain diagram of a cyclically loaded collagen fibril at  $60\%$  humidity. After cyclical loading, the collagen fibril is tested up to failure. Hysteresis is observed in the stress-strain diagram that is quantified in panel E. After the first cycle, a drop of the hysteresis is observed. The inelastic strain, e.g. the strain at zero stress after unloading, is increasing over the first three cycles to reach a constant value as shown in panel C. From Liu et al. [51] with permission.

![img-17.jpeg](img-17.jpeg)

![img-18.jpeg](img-18.jpeg)

![img-19.jpeg](img-19.jpeg)

4% strain (phase I). Hence, there may be a threshold for the onset of residual strains, perhaps associated with the onset of molecular sliding and possibly the onset of the damage mechanism proposed by Zitnay et al. [93]. Shen et al. [59] cyclically loaded dry collagen fibrils, which resulted in a gradual decrease of the point at which the slope of the stress-strain curves begins to decrease (phase I to phase II transition), which may be explained with the accumulation of damage.

To explore this further, Liu et al. [51] systematically investigated the hysteresis and progression of residual strain of cyclically stretched collagen fibrils to phase I, II, and post-phase II strains. In their study, the authors used partially hydrated collagen fibrils (60% humidity in air). After cyclic loading, all collagen fibrils were tested up to fracture. Liu et al. observed a residual strain that gradually increased until a plateau after about three cycles is reached, which is higher for fibrils pulled to higher strains, i.e., corresponding to phase I, II, or III (Fig. 7). The hysteresis generally dropped after the first cycle to reach a steady state. After 60 min of relaxation, residual strains as well as the first cycle hysteresis partially recovered. Partial recovery of the residual strain was in agreement with reported results by Svensson et al. and Shen et al. [59,64]. Subsequent tensile tests to fracture reveal toughening and strengthening of collagen fibrils that were cyclically stretched to strains in phase II and post-phase II (phase III). The drop of the hysteresis can be explained by molecular straightening and uncoiling, thought to be dominant deformation mechanisms in phase I. Uncoiling of collagen molecules can be associated with breaking of

hydrogen bonds [102], which partially reform to drive recovery of mechanical properties as suggested by the authors. Collagen fibrils, that are stretched to phase II, are thought to exhibit intermolecular sliding, resulting in gradual increase of residual strain during cyclic loading [51]. In addition, intermolecular sliding is hypothesized to be the dominant mechanism behind strengthening and toughening in the subsequent fracture test. While Liu et al. [51] suggested that there is no nanoscale damage accumulation in phase I, this is contradicting the interpretation and opinions expressed of damage accumulation in phase I [33,50,70]. However, direct comparison of these hypotheses is intricate as any observations involving molecular sliding heavily involve hydration of collagen fibrils due to molecular separation and a potential role of water molecules as a lubricant [88,103].

In summary, although phase I is generally thought to be dominated by deformation mechanisms of uncoiling and straightening, existing evidence suggest that damage accumulation may also occur, i.e., disruption of the tight triple helix as an alpha chain is pulled out of the molecule. The evidence in question is permanent strains observed after stretching in phase I as well as higher phase I stiffness observed after artificial crosslinking of fibrils with low native crosslink density (cf. Fig. 6). Additionally, creep experiments in phase I also suggest damage in phase I as a possible deformation mechanism. However, a systematic investigation of damage onset lacks to date. Overall, the various deformation mechanisms are likely dominant in a specific phase but may also contribute to other phases.

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

![img-20.jpeg](img-20.jpeg)
Fig. 8. (A) Stress-strain diagram of a collagen fibril loaded at strain-rates from  $0\%/\mathrm{s}$  to  $157\%/\mathrm{s}$ . The derivative modulus at maximum strain increases with strain-rate, an indication of time-dependent deformation effects (From Svensson et al. [64] with permission). (B) Stress-relaxation of individual collagen fibril by Yang et al. [71]. The position of a piezo actuator, that performs the pulling motion, is held constant at a target collagen fibril strain while the force is recorded. A two-term Prony-series is fitted to the stress over time data to acquire the time constants  $\tau_{1}$  and  $\tau_{2}$ . Panel B from Yang et al. [71] with permission.

![img-21.jpeg](img-21.jpeg)

# 4.3.8. Collagen fibril viscoelastic and inelastic behavior

The hysteresis observed in the study by Liu et al., (Fig. 7) indicate that phenomenologically collagen fibrils behave viscoelastic and/or inelastic [51]. In this subsection the current phenomenological findings are discussed and related to possible mechanisms identified mostly from molecular dynamics studies. Liu et al. quantified hysteresis by calculating the loss coefficient, defined as the ratio of dissipated to the supplied elastic energy per cycle and found a moderate loss of about  $5 - 10\%$ . They also found inelastic strains of up to  $13\%$  (depending on the cyclic regime imposed). It is important to note that the collagen fibrils the authors investigated were in a humid environment (air-dried with  $60\%$  humidity) rather than fully hydrated in aqueous solution, which may have influenced the results.

Viscoelasticity does not only manifest itself in energy dissipation, but also in deformation-rate-dependent mechanical behavior. Deformation-rate-dependent tensile moduli was observed by a number of studies [36,61,63,64,70,71] and is qualitatively shown in the stress-strain diagram in Fig. 8A. Svensson et al. [63] reported a  $7.6\%$  increase of the tangent modulus on average across all samples by increasing the pulling velocity from  $9.8~{\mu\mathrm{m}}/\mathrm{s}$  to  $314.0~{\mu\mathrm{m}}/\mathrm{s}$ .

Svensson et al. [64] separated a viscous and an elastic component of the stress-strain curve by deriving a stress-strain curve that only represents the quasistatic elastic component. They did this by performing a stepwise tensile experiment with step sizes between  $0.3\mu \mathrm{m}$  and  $0.5\mu \mathrm{m}$  and allowing the collagen fibril to relax for 5 min between each step. This elastic component is subtracted from dynamic stress-strain curves of deformation-rates from  $5\%$  strain/s to  $157\%$  strain/s (Fig. 8A). The resulting viscous components showed linear stress-strain relationships and their slopes increased with increasing strain rates. The slope increase was best fitted to strain-rate with a power-law function and a power lower than one. Svensson et al. concluded that the viscosity is a decreasing function of strain rate, which associated with interstitial water in the collagen fibril. This causes hydroplaning of collagen molecules at high strain rates and therefore reduces the friction between them [64,103].

Viscoelasticity as a function of hydration and strain rate was also explored by Andriotis et al. [36], which is in agreement with the ideas and analysis proposed by Svensson et al. [64]. Andriotis et al. also reported an increase in stress at a given strain with increasing strain rate at all hydration levels investigated. In a further analysis, Handelshauser et al. [105] reported that the tensile load of collagen fibrils can be fitted with a non-linear Maxwell model

(a nonlinear spring and a nonlinear dashpot in series), exhibiting thixotropic behavior, similar to the interpretation of Svensson et al. [64].

Finally, also stress relaxation experiments have been performed and interpreted in a small number of studies. Specifically, Shen et al. [61] and Yang et al. [71] fitted a Maxwell-Wiechert model (a Prony series with  $n = 2$ ) to stress relaxation data from sea cucumber and bovine Achilles' tendon collagen fibrils (Fig. 8B), respectively.

Shen et al. [61] and Yang et al. [71] performed relaxation stress tests in phase II (14% and 30% strain) and phase I (5%–7% strain), respectively, and both reported short and long relaxation times suggesting that there are at least two time-dependent mechanisms. The relaxation time was associated to the molecular rearrangement of water and collagen molecules by Shen et al. [61]. In addition, Yang et al. [71] investigated, how cross-linking affected the viscoelasticity of collagen fibrils, by performing similar relaxation experiments (in phase I) on native and artificially cross-linked collagen fibrils (with glutaraldehyde). Importantly, Yang et al. [71] suggested (by fitting a two-term Prony series model [106] to relaxation data) that glutaraldehyde-induced cross-linking significantly increased the short and long-time constants [71]. Yang et al. [71] suggested intermolecular sliding to be the major mechanism behind both time constants. Intermolecular sliding is hampered by intermolecular cross-linking of both types thus both long time constants increase.

In vitro experiments proposed that the viscoelastic behavior of collagen fibrils under tension could be explained by water hydroplaning [103] as interstitial water and water rearrangement [61] promotes sub-fibrillar elements to slip against each other. Intermolecular sliding was another mechanism proposed to influence the viscous behavior of collagen fibrils under tension [71] and water rearrangement. However, molecular dynamics simulations suggested that rupture and reformation of H-bonds is the most highly cause of the time-dependent mechanical properties in collagen fibrils [107-109]. Creep tests on collagen molecules revealed that while the collagen triple helix unwinds and straightens, intramolecular H-bonds rupture and collagen-water H-bonds are forming [107-109]. This mechanism goes well in agreement with earlier work on statistical mechanics (Bell's model) [110]) that suggested the velocity at which H-bond rupture depends on the applied force, which in turn shows the time-dependency of the mechanical response of H-bonds. It is very well possible that not only one mechanism is at play, i.e., H-bond rupture and reformation,

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

but it is not clear which effect is dominating the viscous response of collagen fibrils. In contrast, it seems that intermolecular sliding is the dominant mechanism responsible for the inelastic behavior.

# 5. Insights and outlook on collagen fibril nanomechanics

Collagen fibrils are complex structures, made up of different types of collagen molecules, and undergoing chemical modifications throughout their lifetime. Mechanically, collagen fibrils serve a multitude of functions such as providing toughness to hard tissues, extensibility to lungs and skin, and transmission of forces from muscles to bones in tendons facilitating, in this way, locomotion. The mechanical properties of individual collagen fibrils are influenced by their composition and chemical (posttranslational) modifications, i.e., the formation and density of enzymatic and non-enzymatic cross-links. AFM-based nanoindentation results have shown that hydration, temperature, and collagen type mixture influence indentation modulus, mostly via influencing the molecular packing density. However, collagen fibrils transmit and withstand predominantly tensile forces. In tensile loading experiments, isolated collagen fibrils show either a two- or a three-phase behavior, which is linked to cross-link types and densities present. To date, several deformation mechanisms have been suggested and, in this context, phenomenological studies are complemented with molecular dynamics simulations. Existing results suggest that several deformation mechanisms are present in different phases with one or two dominating certain phases. Studies have shown that hydration and cross-linking largely influence nanotensile mechanics in terms of stiffness and strength. In addition, collagen fibrils show both viscoelastic and inelastic behavior. Here, H-bond breakage and reformation as well as molecular sliding could be the key mechanisms explaining rising stiffness with strain-rate and the thixotropic behavior. Overall, the situation is likely more complex. Collagen fibrils are composed of more than one collagen type, which may influence enzymatic and non-enzymatic cross-linking and the extent of hydration. At the same time, chemical modifications may also influence hydration, resulting in interrelated factors influencing the nanotensile mechanics. This is schematically shown in Fig. 9. Given the already sparse data available, further studies ideally coupled with chemical analysis and computer models are

![img-22.jpeg](img-22.jpeg)
Fig. 9. Collagen fibril mechanics is influenced by a multitude of factors. The relative amount and diversity of collagen molecules composing the fibril may influence what exactly chemical modifications take place, the interactions of water molecules and hence hydration, which may be influenced by the chemical modifications as well (Artist's impression of collagen molecules and collagen fibril; courtesy of Lydia Andrioti).

direly needed to deepen our understanding. Nevertheless, experimental advances and molecular dynamics simulations have already provided us with important mechanistic insights.

# Declaration of Competing Interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Acknowledgement

O.G.A and P.J.T. gratefully acknowledge funding from the Vienna Science and Technology Fund (WWTF), Grant No. LS19-035. The authors acknowledge TU Wien Bibliothek for financial support through its Open Access Funding Programme.

# References

[1] J. Myllyharju, K.I. Kivirikko, Collagens and collagen-related diseases, Ann. Med. 33 (1) (2001) 7-21.
[2] S. Ricard-Blum, The collagen family, Cold Spring Harb. Perspect. Biol. 3 (1) (2011) a004978.
[3] P. Fratzl, Collagen: structure and mechanics, an introduction, in: Collagen, Springer, 2008, pp. 1-13.
[4] J.P. Orgel, T.C. Irving, A. Miller, T.J. Wess, Microfibrillar structure of type I collagen in situ, Proc. Natl. Acad. Sci. 103 (24) (2006) 9001-9005.
[5] G. Cameron, I. Alberts, J. Laing, T.J. Wess, Structure of type I and type III heterotypic collagen fibrils: an X-ray diffraction study, J. Struct. Biol. 137 (1-2) (2002) 15-22.
[6] D.R. Keene, L.Y. Sakai, H.P. Bächinger, R.E. Burgeson, Type III collagen can be present on banded collagen fibrils regardless of fibril diameter, J. Cell Biol. 105 (5) (1987) 2393-2402.
[7] J.M. Kirk, B.E. Heard, I. Kerr, M. Turner-Warwick, G.J. Laurent, Quantitation of types I and III collagen in biopsy lung samples from patients with cryptogenic fibrosing alveolitis, Coll. Relat. Res. 4 (3) (1984) 169-182.
[8] C. Lovell, K. Smolenski, V. Duance, N. Light, S. Young, M. Dyson, Type I and III collagen content and fibre distribution in normal human skin during ageing, Br. J. Dermatol. 117 (4) (1987) 419-428.
[9] I. Williams, K. McCullagh, I. Silver, The distribution of types I and III collagen and fibronectin in the healing equine tendon, Connect. Tissue Res. 12 (3-4) (1984) 211-227.
[10] G.B. Smejkal, C. Fitzgerald, Revised estimate of total collagen in the human body, J. Biomed. Res. Environ. Sci. 3 (8) (2017) 001-002.
[11] J. Jokinen, E. Dadu, P. Nykvist, J. Käpylä, D.J. White, J. Ivaska, P. Vehviläinen, H. Reunanen, H. Larjava, L. Häkkinen, Integrin-mediated cell adhesion to type I collagen fibrils, J. Biol. Chem. 279 (30) (2004) 31956-31963.
[12] E. Hadjipanayi, V. Mudera, R.A. Brown, Guiding cell migration in 3D: a collagen matrix with graded directional stiffness, Cell Motil. Cytoskeleton 66 (3) (2009) 121-128.
[13] K. Poole, K. Khairy, J. Friedrichs, C. Franz, D.A. Cisneros, J. Howard, D. Mueller, Molecular-scale topographic cues induce the orientation and directional movement of fibroblasts on two-dimensional collagen surfaces, J. Mol. Biol. 349 (2) (2005) 380-386.
[14] J. Friedrichs, A. Taubenberger, C.M. Franz, D.J. Muller, Cellular remodelling of individual collagen fibrils visualized by time-lapse AFM, J. Mol. Biol. 372 (3) (2007) 594-607.
[15] C. Xue, J. Wyckoff, F. Liang, M. Sidani, S. Violini, K.-L. Tsai, Z.-Y. Zhang, E. Sahai, J. Condeelis, J.E. Segall, Epidermal growth factor receptor overexpression results in increased tumor cell motility in vivo coordinately with enhanced intravasation and metastasis, Cancer Res. 66 (1) (2006) 192-197.
[16] J.E. Marturano, J.D. Arena, Z.A. Schiller, I. Georgakoudi, C.K. Kuo, Characterization of mechanical and biochemical properties of developing embryonic tendon, Proc. Natl. Acad. Sci. 110 (16) (2013) 6370-6375.
[17] D.E. Birk, J.F. Southern, E.I. Zycband, J.T. Fallon, R.L. Trelstad, Collagen fibril bundles: a branching assembly unit in tendon morphogenesis, Development 107 (3) (1989) 437-443.
[18] H.K. Graham, D.F. Holmes, R.B. Watson, K.E. Kadler, Identification of collagen fibril fusion during vertebrate tendon morphogenesis. The process relies on unipolar fibrils and is regulated by collagen-proteoglycan interaction, J. Mol. Biol. 295 (4) (2000) 891-902.
[19] X. Liu, X. Long, W. Liu, Y. Zhao, T. Hayashi, M. Yamato, K. Mizuno, H. Fujisaki, S. Hattori, S.-i. Tashiro, Type I collagen induces mesenchymal cell differentiation into myofibroblasts through YAP-induced TGF-  $\beta 1$  activation, Biochimie 150 (2018) 110-130.
[20] E. Brauer, E. Lippens, O. Klein, G. Nebrich, S. Schreivogel, G. Korus, G.N. Duda, A. Petersen, Collagen fibrils mechanically contribute to tissue contraction in an in vitro wound healing scenario, Advanced Science 6 (9) (2019) 1801780.
[21] M.J. Mienaltowski, D.E. Birk, Structure, physiology, and biochemistry of collagens, in: Progress in Heritable Soft Connective Tissue Diseases, 2014, pp. 5-29.

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

[22] B. Suki, J.H. Bates, Extracellular matrix mechanics in lung parenchymal diseases, Respir. Physiol. Neurobiol. 163 (1-3) (2008) 33-43.
[23] E.R. Weibel, J. Gil, Structure-function relationships at the alveolar level, Bioeng. Aspects Lung 3 (1977) 1-81.
[24] S.T. Holgate, H.S. Arshad, G.C. Roberts, P.H. Howarth, P. Thurner, D.E. Davies, A new look at the pathogenesis of asthma, Clin. Sci. 118 (7) (2010) 439-450.
[25] W. Manuyakorn, P.H. Howarth, S.T. Holgate, Airway remodelling in asthma and novel therapy, Asian Pac. J. Allergy Immunol. 31 (1) (2013) 3.
[26] M.G. Jones, O.G. Andriotis, J.J. Roberts, K. Lunn, V.J. Tear, L. Cao, K. Ask, D.E. Smart, A. Bonfanti, P. Johnson, Nanoscale dysregulation of collagen structure-function disrupts mechano-homeostasis and mediates pulmonary fibrosis, Elife 7 (2018) e36354.
[27] D.M. Maurice, The structure and transparency of the cornea, J. Physiol. 136 (2) (1957) 263-286.
[28] C. Boote, S. Dennis, R.H. Newton, H. Puri, K.M. Meek, Collagen fibrils appear more closely packed in the prepupillary cornea: optical and biomechanical implications, Invest. Ophthalmol. Vis. Sci. 44 (7) (2003) 2941-2948.
[29] M.J. Buehler, Nature designs tough collagen: explaining the nanostructure of collagen fibrils, Proc. Natl. Acad. Sci. 103 (33) (2006) 12285-12290.
[30] S.-W. Chang, S.J. Shefelbine, M.J. Buehler, Structural and mechanical differences between collagen homo-and heterotrimers: relevance for the molecular origin of brittle bone disease, Biophys. J. 102 (3) (2012) 640-648.
[31] O. Andriotis, S. Chang, M. Vanleene, P. Howarth, D. Davies, S. Shefelbine, M. Buehler, P. Thurner, Structure-mechanics relationships of collagen fibrils in the osteogenesis imperfecta mouse model, J. R. Soc. Interface 12 (111) (2015) 20150701.
[32] R.B. Svensson, C.S. Eriksen, P.H. Tran, M. Kjaer, S.P. Magnusson, Mechanical properties of human patellar tendon collagen fibrils. An exploratory study of aging and sex, J. Mech. Behav. Biomed. Mater. 124 (2021) 104864.
[33] R.B. Svensson, H. Mulder, V. Kovanen, S.P. Magnusson, Fracture mechanics of collagen fibrils: influence of natural cross-links, Biophys. J. 104 (11) (2013) 2476-2484.
[34] R.B. Svensson, S.T. Smith, P.J. Moyer, S.P. Magnusson, Effects of maturation and advanced glycation on tensile mechanics of collagen fibrils from rat tail and Achilles tendons, Acta Biomater. 70 (2018) 270-280.
[35] M. Asgari, N. Latifi, H.K. Heris, H. Vali, L. Mongeau, In vitro fibrillogenesis of tropocollagen type III in collagen type I affects its relative fibrillar topology and mechanics, Sci. Rep. 7 (1) (2017) 1-10.
[36] O.G. Andriotis, S. Desissaire, P.J. Thurner, Collagen fibrils: nature's highly tunable nonlinear springs, ACS Nano 12 (4) (2018) 3671-3680.
[37] O.G. Andriotis, K. Elsayad, D.E. Smart, M. Nalbach, D.E. Davies, P.J. Thurner, Hydration and nanomechanical changes in collagen fibrils bearing advanced glycation end-products, Biomed. Opt. Express. 10 (4) (2019) 1841-1855.
[38] S.J. Baldwin, L. Kreplak, J.M. Lee, Characterization via atomic force microscopy of discrete plasticity in collagen fibrils from mechanically overloaded tendons: nano-scale structural changes mimic rope failure, J. Mech. Behav. Biomed. Mater. 60 (2016) 356-366.
[39] S.J. Baldwin, A.S. Quigley, C. Clegg, L. Kreplak, Nanomechanical mapping of hydrated rat tail tendon collagen I fibrils, Biophys. J. 107 (8) (2014) 1794-1801.
[40] M.J. Buehler, Nanomechanics of collagen fibrils under varying cross-link densities: atomistic and continuum studies, J. Mech. Behav. Biomed. Mater. 1 (1) (2008) 59-67.
[41] B. Depalle, Z. Qin, S.J. Shefelbine, M.J. Buehler, Influence of cross-link structure, density and mechanical properties in the mesoscale deformation mechanisms of collagen fibrils, J. Mech. Behav. Biomed. Mater. 52 (2015) 1-13.
[42] S. Eppell, B. Smith, H. Kahn, R. Ballarini, Nano measurements with micro-devices: mechanical properties of hydrated collagen fibrils, J. R. Soc. Interface 3 (6) (2006) 117-121.
[43] P. Fratzl, K. Misof, I. Zizak, G. Rapp, H. Amenitsch, S. Bernstorff, Fibrillar structure and mechanical properties of collagen, J. Struct. Biol. 122 (1-2) (1998) 119-122.
[44] A. Gautieri, S. Vesentini, A. Redaelli, M.J. Buehler, Hierarchical structure and nanomechanics of collagen microfibrils from the atomistic scale up, Nano Lett. 11 (2) (2011) 757-766.
[45] C.A. Grant, D.J. Brockwell, S.E. Radford, N.H. Thomson, Effects of hydration on the mechanical response of individual collagen fibrils, Appl. Phys. Lett. 92 (2008) 233902.
[46] C.A. Grant, D.J. Brockwell, S.E. Radford, N.H. Thomson, Tuning the elastic modulus of hydrated collagen fibrils, Biophys. J. 97 (11) (2009) 2985-2992.
[47] C.A. Grant, M.A. Phillips, N.H. Thomson, Dynamic mechanical analysis of collagen fibrils at the nanoscale, J. Mech. Behav. Biomed. Mater. 5 (1) (2012) 165-170.
[48] A.J. Heim, T.J. Koob, W.G. Matthews, Low strain nanomechanics of collagen fibrils, Biomacromolecules 8 (11) (2007) 3298-3301.
[49] A.J. Heim, W.G. Matthews, T.J. Koob, Determination of the elastic modulus of native collagen fibrils via radial indentation, Appl. Phys. Lett. 89 (18) (2006) 181902.
[50] S.A. Iqbal, D. Deska-Gauthier, L. Kreplak, Assessing collagen fibrils molecular damage after a single stretch-release cycle, Soft Matter 15 (30) (2019) 6237-6246.
[51] J. Liu, D. Das, F. Yang, A.G. Schwartz, G.M. Genin, S. Thomopoulos, I. Chasiotis, Energy dissipation in mammalian collagen fibrils: cyclic strain-induced damping, toughening, and strengthening, Acta Biomater. 80 (2018) 217-227.
[52] Y. Liu, R. Ballarini, S.J. Eppell, Tension tests on mammalian collagen fibrils, Interface Focus 6 (1) (2016) 20150080.

[53] A. Masic, L. Bertinetti, R. Schuetz, S.-W. Chang, T.H. Metzger, M.J. Buehler, P. Fratzl, Osmotic pressure induced tensile forces in tendon collagen, Nat. Commun. 6 (1) (2015) 1-8.
[54] M. Minary-Jolandan, M.-F. Yu, Nanomechanical heterogeneity in the gap and overlap regions of type I collagen fibrils with implications for bone heterogeneity, Biomacromolecules 10 (9) (2009) 2565-2570.
[55] C.J. Peacock, L. Kreplak, Nanomechanical mapping of single collagen fibrils under tension, Nanoscale 11 (30) (2019) 14417-14425.
[56] A.S. Quigley, S. Bancelin, D. Deska-Gauthier, F. Legare, L. Kreplak, S.P. Veres, In tendons, differing physiological requirements lead to functionally distinct nanostructures, Sci. Rep. 8 (1) (2018) 1-14.
[57] A.S. Quigley, S. Bancelin, D. Deska-Gauthier, F. Légare, S.P. Veres, L. Kreplak, Combining tensile testing and structural analysis at the single collagen fibril level, Sci. Data 5 (1) (2018) 1-8.
[58] A.S. Quigley, S.P. Veres, L. Kreplak, Bowstring stretching and quantitative imaging of single collagen fibrils via atomic force microscopy, PLoS One 11 (9) (2016) e0161951.
[59] Z.L. Shen, M.R. Dodge, H. Kahn, R. Ballarini, S.J. Eppell, Stress-strain experiments on individual collagen fibrils, Biophys. J. 95 (8) (2008) 3956-3963.
[60] Z.L. Shen, M.R. Dodge, H. Kahn, R. Ballarini, S.J. Eppell, In vitro fracture testing of submicron diameter collagen fibril specimens, Biophys. J. 99 (6) (2010) 1986-1995.
[61] Z.L. Shen, H. Kahn, R. Ballarini, S.J. Eppell, Viscoelastic properties of isolated collagen fibrils, Biophys. J. 100 (12) (2011) 3008-3015.
[62] R.B. Svensson, P. Hansen, T. Hassenkam, B.T. Haraldsson, P. Aagaard, V. Kovanen, M. Krogsgaard, M. Kjaer, S.P. Magnusson, Mechanical properties of human patellar tendon at the hierarchical levels of tendon and fibril, J. Appl. Physiol. 112 (3) (2012) 419-426.
[63] R.B. Svensson, T. Hassenkam, C.A. Grant, S.P. Magnusson, Tensile Properties of Human Collagen Fibrils and Fascicles Are Insensitive to Environmental Salts, Biophys. J. 99 (12) (2010) 4020-4027.
[64] R.B. Svensson, T. Hassenkam, P. Hansen, S.P. Magnusson, Viscoelastic behavior of discrete human collagen fibrils, J. Mech. Behav. Biomed. Mater. 3 (1) (2010) 112-115.
[65] J.A. Van Der Rijt, K.O. Van Der Werf, M.L. Bennink, P.J. Dijkstra, J. Feijen, Micromechanical testing of individual collagen fibrils, Macromol. Biosci. 6 (9) (2006) 697-702.
[66] S.P. Veres, J.M. Harrison, J.M. Lee, Repeated subrupture overload causes progression of nanoscaled discrete plasticity damage in tendon collagen fibrils, J. Orthop. Res. 31 (5) (2013) 731-737.
[67] S.P. Veres, J.M. Harrison, J.M. Lee, Mechanically overloading collagen fibrils viscoils collagen molecules, placing them in a stable, denatured state, Matrix Biol. 33 (2014) 54-59.
[68] S.P. Veres, J.M. Lee, Designed to fail: a novel mode of collagen fibril disruption and its relevance to tissue toughness, Biophys. J. 102 (12) (2012) 2876-2884.
[69] M.P. Wenger, L. Bozec, M.A. Horton, P. Mesquida, Mechanical properties of collagen fibrils, Biophys. J. 93 (4) (2007) 1255-1263.
[70] F. Yang, D. Das, K. Karunakaran, G.M. Genin, S. Thomopoulos, I. Chasiotis, Nonlinear time-dependent mechanical behavior of Mammalian collagen fibrils, Acta Biomater. (2022).
[71] L. Yang, K.O. van der Werf, P.J. Dijkstra, J. Feijen, M.L. Bennink, Micromechanical analysis of native and cross-linked collagen type I fibrils supports the existence of microfibrils, J. Mech. Behav. Biomed. Mater. 6 (2012) 148-158.
[72] L. Yang, K.O. van der Werf, C.F. Fitie, M.L. Bennink, P.J. Dijkstra, J. Feijen, Mechanical properties of native and cross-linked type I collagen fibrils, Biophys. J. 94 (6) (2008) 2204-2211.
[73] L. Yang, K.O. van der Werf, B.F. Koopman, V. Subramaniam, M.L. Bennink, P.J. Dijkstra, J. Feijen, Micromechanical bending of single collagen fibrils using atomic force microscopy, J. Biomed. Mater. Res. A 82 (1) (2007) 160-168.
[74] S.R. Saumdar, D.P. Knight, N.J. Terrill, A. Karunaratne, F. Cacho-Nerio, M.M. Knight, H.S. Gupta, The secret life of collagen: temporal changes in nanoscale fibrillar pre-strain and molecular organization during physiological loading of cartilage, ACS Nano 11 (10) (2017) 9728-9737.
[75] J. Heino, The collagen family members as cell adhesion proteins, Bioessays 29 (10) (2007) 1001-1010.
[76] D.P. McDaniel, G.A. Shaw, J.T. Elliott, K. Bhadriraju, C. Meuse, K.-H. Chung, A.L. Plant, The stiffness of collagen fibrils influences vascular smooth muscle cell phenotype, Biophys. J. 92 (5) (2007) 1759-1769.
[77] M. Milazzo, A. David, G.S. Jung, S. Danti, M.J. Buehler, Molecular origin of viscoelasticity in mineralized collagen fibrils, Biomater. Sci. 9 (9) (2021) 3390-3400.
[78] M. Milazzo, G.S. Jung, S. Danti, M.J. Buehler, Mechanics of mineralized collagen fibrils upon transient loads, ACS Nano 14 (7) (2020) 8307-8316.
[79] N. Rajan, J. Habermehl, M.-F. Cote, C.J. Doillon, D. Mantovani, Preparation of ready-to-use, storable and reconstituted type I collagen from rat tail tendon for tissue engineering applications, Nat. Protoc. 1 (6) (2006) 2753-2758.
[80] D. Holmes, M. Capaldi, J. Chapman, Reconstitution of collagen fibrils in vitro: the assembly process depends on the initiating procedure, Int. J. Biol. Macromol. 8 (3) (1986) 161-166.
[81] O.G. Andriotis, W. Manuyakorn, J. Zekonyte, O.L. Katsamenis, S. Fabri, P.H. Howarth, D.E. Davies, P.J. Thurner, Nanomechanical assessment of human and murine collagen fibrils via atomic force microscopy cantilever-based nanoindentation, J. Mech. Behav. Biomed. Mater. 39 (2014) 9-26.

---

O.G. Andriotis, M. Nalbach and P.J. Thurner

Acta Biomaterialia 163 (2023) 35-49

[82] P. Hansen, T. Hassenkam, R.B. Svensson, P. Aagaard, T. Trappe, B.T. Haraldsson, M. Kjaer, P. Magnusson, Glutaraldehyde cross-linking of tendon—Mechanical effects at the level of the tendon fascicle and fibril, Connect. Tissue Res. 50 (4) (2009) 211–222.
[83] M. Nalbach, F. Chalupa-Gantner, F. Spoerl, V. de Bar, B. Baumgartner, O.G. Andriotis, S. Ito, A. Ovsianikov, G. Schitter, P.J. Thurner, Instrument for tensile testing of individual collagen fibrils with facile sample coupling and uncoupling, Rev. Sci. Instrum. 93 (5) (2022) 054103.
[84] J.L. Tan, J. Tien, D.M. Pirone, D.S. Gray, K. Bhadriraju, C.S. Chen, Cells lying on a bed of microneedles: an approach to isolate mechanical force, Proc. Natl. Acad. Sci. 100 (4) (2003) 1484–1489.
[85] O. Du Roure, A. Saez, A. Buguin, R.H. Austin, P. Chavrier, P. Siberzan, B. Ladoux, Force mapping in epithelial cell migration, Proc. Natl. Acad. Sci. 102 (7) (2005) 2390–2395.
[86] S.J. Baldwin, L. Kreplak, J.M. Lee, MMP-9 selectively cleaves non-D-banded material on collagen fibrils with discrete plasticity damage in mechanically-overloaded tendon, J. Mech. Behav. Biomed. Mater. 95 (2019) 67–75.
[87] C. Couppé, R.B. Svensson, S.V. Skovlund, J.K. Jensen, C.S. Eriksen, N.M. Malmgaard-Clausen, J.D. Nybing, M. Kjaer, S.P. Magnusson, Habitual side-specific loading leads to structural, mechanical, and compositional changes in the patellar tendon of young and senior lifelong male athletes, J. Appl. Physiol. 131 (4) (2021) 1187–1199.
[88] G.D. Fullerton, A. Rahal, Collagen structure: the molecular source of the tendon magic angle effect, J. Magn. Reson. Imaging 25 (2) (2007) 345–361.
[89] R. Fraser, T. MacRae, A. Miller, E. Suzuki, Molecular conformation and packing in collagen fibrils, J. Mol. Biol. 167 (2) (1983) 497–521.
[90] H. Bueckle, J. Westbrook, H. Conrad, The Science of Hardness Testing and Its Research Applications, American Society for Metals, Materials Park, Ohio, 1973.
[91] R.B. Svensson, A. Herchenhan, T. Starborg, M. Larsen, K.E. Kadler, K. Qvortrup, S.P. Magnusson, Evidence of structurally continuous collagen fibrils in tendons, Acta Biomater. 50 (2017) 293–301.
[92] Z. Zhou, M. Minary-Jolandan, D. Qian, A simulation study on the significant nanomechanical heterogeneous properties of collagen, Biomech. Model. Mechanobiol. 14 (3) (2015) 445–457.
[93] J.L. Zitnay, Y. Li, Z. Qin, B.H. San, B. Depalle, S.P. Reese, M.J. Buehler, S.M. Yu, J.A. Weiss, Molecular level detection and localization of mechanical damage in collagen enabled by collagen hybridizing peptides, Nat. Commun. 8 (1) (2017) 1–12.
[94] G.D. Fullerton, M.R. Amurao, Evidence that collagen and tendon have monolayer water coverage in the native state, Cell Biol. Int. 30 (1) (2006) 56–65.
[95] J. Bella, B. Brodsky, H.M. Berman, Hydration structure of a collagen peptide, Structure 3 (9) (1995) 893–906.

[96] M. Saito, K. Marumo, Collagen cross-links as a determinant of bone quality: a possible explanation for bone fragility in aging, osteoporosis, and diabetes mellitus, Osteop. Int. 21 (2) (2010) 195–214.
[97] V.M. Monnier, G.T. Mustata, K.L. Biemel, O. Reihl, M.O. Lederer, D. Zhenyu, D.R. Sell, Cross-linking of the extracellular matrix by the maillard reaction in aging and diabetes: an update on "a puzzle nearing resolution, Ann. N. Y. Acad. Sci. 1043 (1) (2005) 533–544.
[98] H. Birch, T. Smith, E. Draper, A. Bailey, N. Avery, A. Goodship, Collagen crosslink profile relates to tendon material properties, Matrix Biol. (25) (2006) 574.
[99] M.J. Buehler, Atomistic and continuum modeling of mechanical properties of collagen: elasticity, fracture, and self-assembly, J. Mater. Res. 21 (8) (2006) 1947–1961.
[100] S.G. Uzel, M.J. Buehler, Molecular structure, mechanical behavior and failure mechanism of the C-terminal cross-link domain in type I collagen, J. Mech. Behav. Biomed. Mater. 4 (2) (2011) 153–161.
[101] R. Usha, V. Subramanian, T. Ramasami, Role of secondary structure on the stress relaxation processes in rat tail tendon (RTT) collagen fibre, Macromol. Biosci. 1 (3) (2001) 100–107.
[102] M.E. Launey, M.J. Buehler, R.O. Ritchie, On the mechanistic origins of toughness in bone, Annu. Rev. Mater. Res. 40 (2010) 25–53.
[103] F.H. Silver, A. Ebrahimi, P.B. Snowhill, Viscoelastic properties of self-assembled type I collagen fibers: molecular basis of elastic and viscous behaviors, Connect. Tissue Res. 43 (4) (2002) 569–580.
[104] N. Sasaki, S. Odajima, Elongation mechanism of collagen fibrils and force-strain relations of tendon at each level of structural hierarchy, J. Biomech. 29 (9) (1996) 1131–1136.
[105] M. Handelshauser, M. Marchetti-Deschmann, P.J. Thurner, O.G. Andriotis, Collagen Fibril Tensile Response Described by a Nonlinear Maxwell Fluid Model, Available at SSRN 3940868.
[106] A.S. Wineman, K.R. Rajagopal, Mechanical Response of Polymers: An Introduction, Cambridge University Press, 2000.
[107] A. Gautieri, M.J. Buehler, A. Redaelli, Deformation rate controls elasticity and unfolding pathway of single tropocollagen molecules, J. Mech. Behav. Biomed. Mater. 2 (2) (2009) 130–137.
[108] A. Gautieri, S. Vesentini, A. Redaelli, M.J. Buehler, Viscoelastic properties of model segments of collagen molecules, Matrix Biol. 31 (2) (2012) 141–149.
[109] H. Ghodsi, K. Darvish, Investigation of mechanisms of viscoelastic behavior of collagen molecule, J. Mech. Behav. Biomed. Mater. 51 (2015) 194–204.
[110] G.I. Bell, Models for the specific adhesion of cells to cells: a theoretical framework for adhesion mediated by reversible bonds between cell surface molecules, Science 200 (4342) (1978) 618–627.
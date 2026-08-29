Review of Scientific Instruments

RESEARCH ARTICLE | MAY 06 2022

# Instrument for tensile testing of individual collagen fibrils with facile sample coupling and uncoupling

Mathis Nalbach 📞 ; Franziska Chalupa-Gantner 📞 ; Felix Spoerl 📞 ; Victor de Bar; Benedikt Baumgartner 📞 ; Orestis G. Andriotis; Shingo Ito; Aleksandr Ovsianikov; Georg Schitter 📞 ; Philipp J. Thurner 📧

[📧] Check for updates

Rev. Sci. Instrum. 93, 054103 (2022)

https://doi.org/10.1063/5.0072123

![img-0.jpeg](img-0.jpeg)

# Articles You May Be Interested In

Longitudinal variations in the Poisson's ratio of collagen fibrils

Appl. Phys. Lett. (April 2011)

Effects of hydration on the mechanical response of individual collagen fibrils

Appl. Phys. Lett. (June 2008)

Poisson's ratio of collagen fibrils measured by small angle X-ray scattering of strained bovine pericardium

J. Appl. Phys. (January 2015)

AI

MAD CITY LAW INC.

Think Nano® | Positioning | Microscopy | Solutions

Nanopositioning Systems • Micropositioning Systems

Atomic Force Microscopes • Single Molecule Microscopes

Custom Solutions

^{}[]

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

# Instrument for tensile testing of individual collagen fibrils with facile sample coupling and uncoupling

Cite as: Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

Submitted: 20 September 2021 • Accepted: 12 April 2022 •

Published Online: 6 May 2022

Mathis Nalbach, $^{1,2}$  Franziska Chalupa-Gantner, $^{3,4,5}$  Felix Spoerl, $^{1,3}$  Victor de Bar, $^{1}$

Benedikt Baumgartner, $^{1}$  Orestis G. Andriotis, $^{1}$  Shingo Ito, $^{2,3}$  Aleksandr Ovsianikov, $^{3,4,a}$  Georg Schitter, $^{2}$  and Philipp J. Thurner $^{1,4,a,b}$

# AFFILIATIONS

$^{1}$ Institute of Lightweight Design and Structural Biomechanics, TU Wien, Gumpendorfer Straße 7/Objekt 8, 1060 Vienna, Austria
$^{2}$ Automation and Control Institute, TU Wien, Gußhausstraße 27-29/E376, 1040 Vienna, Austria
$^{3}$ Institute of Materials Science and Technology, TU Wie, Getreidemarkt 9/E308, 1060 Vienna, Austria
$^{4}$ Austrian Cluster for Tissue Regeneration, Vienna, Austria
$^{5}$ Department of Mechanical and System Engineering, University of Fukui, 3-9-1 Bunkyo, Fukui 910-8507, Japan

a)URL: www.tissue-regeneration.at
b) Author to whom correspondence should be addressed: philipp.thurner@tuwien.ac.at

# ABSTRACT

Collagen is the major structural protein in human bodies constituting about  $30\%$  of the entire protein mass. Through a self-assembly process, triple helical collagen molecules assemble into high aspect-ratio fibers of tens to hundreds of nanometer diameter, known as collagen fibrils (CFs). In the last decade, several methods for tensile testing these CFs emerged. However, these methods are either overly time-consuming or offer low data acquisition bandwidth, rendering dynamic investigation of tensile properties impossible. Here, we describe a novel instrument for tensile testing of individual CFs. CFs are furnished with magnetic beads using a custom magnetic tweezer. Subsequently, CFs are lifted by magnetic force, allowing them to be picked-up by a microgripper structure, which is mounted on a cantilever-based interferometric force probe. A piezo-lever actuator is used to apply tensile displacements and to perform tensile tests of tethered CFs, after alignment. Once the mechanical tests are finished, CFs are removed from the microgripper by application of a magnetic field. Our novel instrument enables tensile tests with at least 25-fold increased throughput compared to tensile testing with an atomic force microscope while achieving force resolution  $(p - p)$  of  $10\mathrm{nN}$  at a strain resolution better than  $0.1\%$ .

© 2022 Author(s). All article content, except where otherwise noted, is licensed under a Creative Commons Attribution (CC BY) license (http://creativecommons.org/licenses/by/4.0/). https://doi.org/10.1063/5.0072123

# I. INTRODUCTION

The extra-cellular matrix (ECM) of the human body is largely made up of a single family of proteins: the collagens. The major subtype of the collagen family is the fibril forming type I collagen. Type I collagen is ubiquitous throughout the entire human body. It is responsible for the structural integrity of a range of connective tissues, such as bones, skin, tendons, blood vessels, and organs. Furthermore, type I collagen is an important determinant of ECM stiffness and, therefore, crucial for cell mechanosensing and

mechanotransduction. Collagen fibrils form through a self-assembly process into nano-scale fibers with high aspect ratios. Typically, collagen fibrils have diameters of  $20 - 300\mathrm{nm}^1$  at a length of up to several millimeters. Unique to collagen fibrils is the structured surface of  $67~\mathrm{nm}$  periodicity over their entire length, which arises due to a staggered aggregation of single collagen molecules during fibrillogenesis. Due to their high biomechanical importance, mechanical and structural characterization of individual collagen fibrils has garnered growing attention. However, the size of collagen fibrils makes mechanical characterization challenging and

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-1

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

requires nanomanipulation tools, such as the atomic force microscope (AFM). Mechanical properties of collagen fibrils are often studied through AFM nano-indentation. $^{7-10}$ This, however, does not provide information on the physiological relevant mechanical properties of collagen fibril mechanics, as they are naturally mostly loaded in tension. Van der Rijt et al. $^{11}$ were the first to perform tensile tests of individual collagen fibrils using an AFM. They mounted a collagen fibril between the AFM cantilever tip and a substrate via a series of sophisticated gluing steps using epoxy glue. First, the collagen fibril was glued on two sites at a distance of about $30\mu \mathrm{m}$ with one site being on a Teflon AF covered area. Second, after curing for at least $24\mathrm{h}$, a calibrated AFM cantilever was glued onto the epoxy droplet that was on the Teflon AF covered area. After an additional $24\mathrm{h}$ curing step, the collagen fibril could be tested in tension while being submerged in aqueous media. Since then, a series of studies applying a similar method were published. $^{12-17}$ In addition, a number of groups began to develop novel methods to study single collagen fibrils in tension. Eppell and colleagues developed a micro-electromechanical system (MEMS) based method to test collagen fibrils to failure. $^{18,19}$ One end of a collagen fibril is glued on a stationary part, whereas the other end is glued on a moving part of the MEMS device. The moving part is connected to a piezo-actuator over rods of known geometry. The stiffness of the rods is calculated, and their deflection is measured during a tensile test using a CCD camera mounted on a light microscope. By that, collagen fibril strain and stress are calculated frame by frame. Another emerging method is to stretch the collagen fibril like a bowstring when the collagen fibril is glued onto a microscope slide on two sites. $^{20,21}$ Here, force is measured by torsional bending of an AFM cantilever, while strain is measured using optical microscope images captured with a CCD camera. Despite this technological advance, the aforementioned methods are either overly time consuming and sophisticated, i.e., AFM approach, or provide very low bandwidth and resolution i.e., MEMS and bowstring stretching, rendering dynamic tensile force measurements at statistically relevant sample sizes impossible.

Our contribution is a novel instrument for tensile testing of single collagen fibrils at a minimum bandwidth of $1\mathrm{kHz}$, a force resolution (p-p) of $10\mathrm{nN}$, and a strain resolution better than $0.1\%$. Most importantly, the coupling of the collagen fibril to the force probe is reversible, and therefore, the same force probe can be used for hundreds of tests. This also means that in most cases, only one force probe is used to conduct an entire study. This increases fibril to fibril precision by avoiding inaccuracies in the calibration of a force probe for each individual tensile test. Furthermore, the coupling is facile and quick, compared to state-of-the-art methods, because curing of glue in a common permanent coupling method is avoided. Throughout this publication, the novel tensile testing instrument is termed NanoTens.

# II. EXPERIMENTAL SETUP

The key concept of the NanoTens is the method, by which the collagen fibril is attached to the force sensor. The attachment method also produces boundary conditions for the choice of force sensor. This choice is constrained by spatial requirements of the attachment method as well as the following specifications: Force

measurements on collagen fibrils should be conducted at a force resolution of $10\mathrm{nN}$ with a minimum sensor bandwidth of $1\mathrm{kHz}$. These values were chosen in view of future development steps that will enable force-controlled tensile tests. During force-controlled tests, the sensor signal is fed back and processed by a controller such that a low background noise is favored in the open loop configuration. Furthermore, tensile tests should be performed in aqueous media, particularly in physiological salt solutions, such as phosphate buffered saline (PBS), to mimic the physiological environment of collagen fibrils. Consequently, the force sensor has to be fully submerged in the liquid to avoid any disturbance from the liquid-air interface, which would render force measurements in the desired force range between unloaded to $10\mu \mathrm{N}$-loaded samples impossible. These requirements are fulfilled by the use of commercially available optical-fiber-based Fabry-Pérot interferometric force probes, in this case fiberoptic cantilever probe, operated with the OP1550 interferometer (Optics11, Netherlands). These force probes are essentially composed of a cantilever mounted on a glass block and an optical fiber to detect cantilever deflection (Fig. 1). The cantilever has a width of $150\mu \mathrm{m}$ and a variable length that determines cantilever stiffness. With a known cantilever stiffness, force can be calculated by multiplication of cantilever deflection, measured by the interferometer with cantilever stiffness. The stiffness of the force probe is measured by the manufacturer, and thus, cantilever stiffness is known prior to testing. For testing of collagen fibrils, force probes with a stiffness of $5\mathrm{N / m}$ are used. Furthermore, the cantilevers are

![img-1.jpeg](img-1.jpeg)
FIG. 1. Schematic of an Optics11 interferometric force probe equipped with a 2PP-printed microgripper. In the prongs of the microgripper, the spherical magnetic bead, attached with glue (beige) to the collagen fibril (stripe-pattern), can be seen. Cantilever deflection is measured via interference. Using the known cantilever stiffness, the force exerted onto the collagen fibril is calculated by multiplication of measured deflection with cantilever stiffness.

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-2

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

supplied by the manufacturer without an attached indentation tip and are, therefore, flat at the site where the microgripper is glued.

Below, the collagen fibril to the force sensor coupling mechanism is explained (Sec. II A) followed by a description of the experimental setup (Sec. II B). Subsequently, fabrication of the customized force probes (Sec. II C), magnetic bead micromanipulation (Sec. II D), and the tensile testing protocol (Sec. II E) are explained in detail.

# A. Collagen fibril to force sensor coupling mechanism

To make collagen fibrils accessible to tensile testing, they have to be separated using an established method. In brief, a fascicle is extracted from a tendon by use of sharp tweezers and a scalpel. The fascicle is placed on a microscope slide and kept moist with PBS or distilled water. Using sharp tweezers, the fascicle is split orthogonally to its long axis under a stereomicroscope and smeared onto a microscope glass slide. One has to take care that the fascicle is not getting dry, which would make it too stiff to be smeared out. At the same time, too much liquid inhibits collagen fibrils to adsorb on the microscope slide. To our knowledge, it is not known whether

physisorption of collagen fibrils on glass substrates impacts their mechanical properties, but the method described is a standard protocol that can be found in the literature. In a trial experiment, we imaged a region of interest of the surface area of a microscope slide that was previously covered with a collagen fibril with atomic force microscopy (AFM) in tapping mode. We did not observe any residuals of the collagen fibril. Collagen fibrils, which are separated by a few hundred micrometers, are chosen for mechanical investigation. One has to take care that exposed collagen fibrils are accessible for an AFM cantilever, needed for assessing collagen fibril D-banding, structural integrity, height (for future stress data calculation), and indentation modulus (optional). Due to the fixed orientation of the AFM cantilever in our AFM setup, the collagen fibril orientation has to be orthogonal to the long axis of the microscope slide. After collagen fibril deposition, the microscope slide is thoroughly washed with distilled water and subsequently dried in a vacuum desiccator. Drying in a vacuum desiccator is done to prevent potential degradation of collagen fibrils at ambient conditions. Whether this affects collagen fibril mechanical properties has not been studied yet but is certainly worth investigating. Another common practice is to dry samples using a stream of nitrogen.

![img-2.jpeg](img-2.jpeg)
FIG. 2. Schematic overview of the tensile testing instrument. The interferometric force probe, partially submerged into an aqueous solution, is mounted on a piezo-lever actuator that is supposed to load the collagen fibril. Due to loading, the cantilever deflects and the resulting interference signal is measured by the OP1550 interferometer. The piezo-lever actuator is mounted on a 3-DOF stepper motor translation stage for coarse positioning of the interferometric force probe. Piezo-lever actuator position and cantilever deflection are acquired with a CompactRIO (National Instruments, USA) controller that also commands the piezo-lever actuator position. Collagen fibril elongation was calculated by subtraction of the cantilever deflection from the piezo-lever actuator position.

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-3

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

Individual collagen fibrils appear as black lines when viewed with a light microscope. The plane of focus is defined as the x-y plane, while the orthogonal direction is the z-direction. Tensile tests are conducted with the microscopy slide located in the light microscope and collagen fibrils submerged into phosphate buffered saline (PBS), other physiologic salt solutions, or water. The direction of tensile testing is the z-direction. Coupling of the collagen fibril to the force sensor is achieved by gluing a two-photon-polymerization (2PP) printed microgripper onto the cantilever tip of the Optics11 interferometric force probe (Fig. 1). The microgripper consists of two prongs with a wedge-like aperture in between them. The prongs merge at the cantilever tip in a semicircle with a radius of  $10\mu \mathrm{m}$ . Furthermore, a magnetic bead, made of neodymium alloy (Product No. MQP-S-11-9-20001, Magnequench International LLC, China) and about  $30 - 50\mu \mathrm{m}$  diameter in size, is attached to the collagen fibril (see Sec. II D). By applying a magnetic field via a magnetic tweezer (see Sec. II E), the magnetic bead along with the collagen fibril is lifted and then picked up by the microgripper with the collagen fibril located in the wedge-like aperture. When pulling up the interferometric force probe, the magnetic bead is restrained by the prongs of the microgripper such that the collagen fibril is suspended between the substrate and the force probe. Consequently, a mechanical tensile test of the collagen fibril can now be conducted (see Sec. III for results). After mechanical testing, both the magnetic bead and the collagen fibril are extracted from the microgripper by application of a magnetic field.

# B. Overview of the instrument

Figure 2 displays a schematic overview of all components of the experimental setup. The center-piece of the instrument is the customized force probe with an attached collagen fibril. This force probe is mounted on a piezo-lever actuator (model: P-601.1SL, Physikinstrumente, Germany) with  $100\mu \mathrm{m}$  travel and  $2\mathrm{nm}$  resolution in closed loop configuration for actuation in the z-direction. The actuator is driven with a servo controller (model: E-625.SR, Physikinstrumente, Germany) in analog input configuration. In this configuration, the piezo-lever actuator position is proportional to the voltage applied at the analog input. The actual piezo-lever actuator position is measured with a strain gauge sensor and is available as an analog voltage signal at the E-625.SR servo controller. The piezo-lever actuator, in turn, is mounted on a 3-degrees-of-freedom (3-DOF) stepper motor translation stage (model: LNR25ZFS, Thorlabs, Great Britain) via a custom stainless-steel rod at an angle of  $45^{\circ}$  (Fig. 3). Through a clamping mechanism, the rod can be disengaged and the piezo-force probe assembly can be approached to the surface. The stepper motor translation stage has a travel of  $25\mathrm{mm}$  at nominal in x-, y-, and z-directions. It is driven by one controller (model: KST101, Thorlabs, Great Britain) for each direction. The stepper motor translation stage is mounted on a rigid, custom platform that is fixated onto an inverted light microscope (model: IX73, Olympus, Japan). The microscope is equipped with a manual x-y table for centering the sample in focus. To isolate the light microscope from floor vibrations and other noise sources, it is placed on an active optical table.

Once a collagen fibril or other nanofiber has been glued to the substrate at one end and it has been loaded into the microgripper at the other end, a mechanical test can be performed. Through

![img-3.jpeg](img-3.jpeg)
FIG. 3. Photograph of the tensile testing instrument integrated with an inverse light microscope. The piezo-lever actuator is mounted on the 3DOF stepper motor translation stage with a stainless-steel rod at an angle of  $45^{\circ}$ . The magnetic tweezer and the interferometric force probe are submerged into a fluid cell filled with PBS.

actuation of the piezo-lever actuator in the z-direction, the collagen fibril or other nanofiber is strained, and consequently, the cantilever of the force probe deflects, evoking a change of the interference signal of the optical fiber. The collagen fibril elongation equals the difference between the piezo-lever actuator position and cantilever deflection. The change of the interference signal is measured, analyzed, and linearized by the OP1550 interferometer. The interferometer outputs an analog voltage signal at a BNC connector with 16-bit resolution that is proportional to the measured force exerted onto the fibril. The piezo-lever actuator analog position signal and the interferometer analog force signal, both having a range of  $0 - 10\mathrm{V}$ , are acquired by a CompactRIO controller (Model No. c-RIO9054, National Instruments, USA) equipped with the 24-bit NI9239 module (National Instruments, USA). The piezo-lever actuator position is regulated by an analog voltage between 0 and  $10\mathrm{V}$  that is generated with the 16-bit module NI9263 (National Instruments, USA). Voltage generation and acquisition is conducted in real-time using the FPGA (field-programmable gate array) interface of the CompactRIO controller. Software is written in LabVIEW (National Instruments, USA), LabVIEW real-time, and LabVIEW FPGA.

# C. Fabrication of microgrippers via two photon polymerization (2PP)

Microgrippers (as shown in Fig. 4) were fabricated with a multiphoton lithography (MPL) set up using a tunable femtosecond NIR laser (model: MaiTai® eHP DeepSee™, Spectra-Physics, USA) with a repetition rate of  $80\mathrm{MHz}$  and a pulse duration of 70 fs after the microscope objective (model: C-Achroplan  $32\times /0.85$  water immersion, Zeiss, Germany). The setup is already described in detail by Dobos et al.[22] For structuring, a wavelength of  $800\mathrm{nm}$  was used with an intensity of  $30\mathrm{mW}$  and a writing speed of  $200\mathrm{mm/s}$ . The printing material was a 1:1 mixture of ethoxylated-(20/3)-trimethylolpropane triacrylate (Sartomer 415) trimethylolpropane

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-4

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

![img-4.jpeg](img-4.jpeg)

![img-5.jpeg](img-5.jpeg)
FIG. 4. (a) CAD model of the microgripper. The gripper is about  $160~\mu \mathrm{m}$  long,  $120~\mu \mathrm{m}$  wide, and  $50~\mu \mathrm{m}$  high. The platform behind the two prongs offers a flat area for mounting on the interferometric force probe as well as a height reserve to prevent incomplete 2PP-printing. (b) Light microscope image of a microgripper. On the platform, three linear marks can be seen. These marks are indicators for microgripper orientation. As grippers are printed upside down, the visibility of the marks indicates successful turning of the microgripper before gluing.

triacrylate (Genomer 1330) (ETA:TTA) with an addition of  $5\mathrm{mM}$  M2CMK photo initiator. As substrates, microscope coverslips with a thickness of  $0.13\mathrm{mm}$ , furnished with 3-(Trimethoxysilylpropyl)-methacrylate (Product No. 440159, Sigma-Aldrich, USA) functionalities following a silanization procedure, are used. Figure 4 shows a 3D model and an actual 2PP-printed microgripper.

Before printing the microgripper, the setup has to be calibrated for the surface of the cover slip to assure that the grippers are printed directly on the glass surface and adhere to it during the post-printing washing steps. This is done by gradually changing the z-position of the focal point relative to the cover slip. The first z-position, where polymerization is observed, is taken as the surface of the cover slip. However, due to a potential tilt of the cover slip, this single point on the surface of the cover slip is not representative for the entire surface. Hence, to avoid detachment from the glass cover slip during printing or post-processing, the first layers of the

grippers are produced several micrometers below the surface "inside" the glass. Consequently, to prevent from incomplete printing of the microgripper prongs, the microgrippers are printed upside down. Due to the upside-down printing, the microgrippers have to be turned before mounting on the cantilever of the interferometric force probe. After printing, receding non-polymerized material is washed away by developing the sample for several hours in 1-propanol with  $99.9\%$  purity (Sigma-Aldrich, USA). After washing, the grippers were dried with hexamethyldisilazane (Sigma-Aldrich, USA). Figure 5 displays the process of turning and mounting the microgrippers. Micromanipulation of microgrippers is done with an ultra-fine tungsten probe (Micro to Nano, The Netherlands) mounted on a 3-DOF manual translation stage. Disengaging the microgrippers from the cover slip is found to be easily facilitated when submerged into a droplet of distilled water. Turning the microgrippers is accomplished by pushing them against a cubic

![img-6.jpeg](img-6.jpeg)
FIG. 5. Gluing of the microgripper onto the cantilever of the interferometric force probe. (a) The microgripper before immersion in distilled water. (b) Disengaging the microgripper from the cover slip. (c) Turning by pushing against a turning structure. (d) Successfully turned microgripper indicated by the markers position. (e) Alignment of the cantilever. (f) Dipping the cantilever into epoxy resin. (g) Approaching the cantilever to the plateau of the microgripper. (h) Cantilever with a microgripper as used for force measurement.

![img-7.jpeg](img-7.jpeg)

![img-8.jpeg](img-8.jpeg)

![img-9.jpeg](img-9.jpeg)

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-5

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

2PP-printed structure while in aqueous media [Fig. 5(c)]. Markers on the attachment surface of the microgripper [Fig. 4(b)] indicate microgripper orientation and, hence, whether a microgripper was successfully turned. After drying, the cantilever of the interferometric force probe is aligned with the microgripper, dipped into 24-h curing epoxy resin (UHU, Germany), and pressed onto the attachment surface of the microgripper at a cantilever deflection of a maximum of  $1\mu \mathrm{m}$ . Subsequently, the cantilever deflection is reduced to  $\sim 100 - 200\mathrm{nm}$  and the assembly is left for curing overnight. A single prong of a microgripper typically has a width of  $w = 35\mu \mathrm{m}$ , a thickness  $t = 10\mu \mathrm{m}$ , and a length of  $l = 60\mu \mathrm{m}$ . The elastic modulus of ETA:TTA is estimated in the present application to be  $E = 1$  GPa according to Cicha et al.[23] and Stampfl et al.[24] With these values, the stiffness  $k$  of a single prong is calculated to be about  $40.5\mathrm{N / m}$  following  $k = (Ew t^3) / (4l^2)$ . Since the cantilever has two prongs and the actual site, where the force is transmitted from the collagen fibril to the cantilever, is closer than  $60~\mu \mathrm{m}$  to the platform, one can assume the bending stiffness of the entire microgripper at the force insertion point to be at least  $100.0\mathrm{N / m}$ . This stiffness is much larger than the typical stiffness of a cantilever (5 N/m), which is used for tensile testing collagen fibrils. Additionally, the deformation of the fibril is much larger compared to the uncorrected gripper deflection. Therefore, bending of the microgripper can be neglected when calculating collagen fibril strain. As the bending stiffness of the microgripper scales with the third power of the prong thickness, microgripper with thicker prongs can be printed if it is necessary for future applications. Gluing of the microgripper on the cantilever may affect the cantilever stiffness. To date, we did not quantify the stiffness of the modified force probe. However, we estimate the effect on accuracy to be small as the platform of the microgripper has a length of less than  $100~\mu \mathrm{m}$  compared to a cantilever length of almost  $1\mathrm{cm}$ . A change in length of  $1\%$  would result in a change of cantilever stiffness of about  $3\%$ . Certainly, this inaccuracy could either be accounted for by determining the stiffness of the modified force probe using a microbalance or by use of computer models e.g., finite element modeling.

# D. Single magnetic bead manipulation

The manipulation of magnetic beads as well as application of a magnetic field for lifting the collagen fibril is accomplished with a custom magnetic tweezer (Fig. 6). This tweezer is inspired from Kollmannsberger and Fabry[25] and consists of a metal core made

from Mu-metal (Vacuumschmelze, Germany) that was sharpened at one end on a turning lathe. The achieved tip radius is about  $50~\mu \mathrm{m}$  as per light microscopy inspection. Mu-metal was chosen as the core material for its low magnetic remanence resulting in a quasi-turn-off capability of the magnetic tweezer. Around the core, enameled coper wire is wound in four layers and 40 windings per each layer. The wound coil is fixated onto the Mu-metal core using a shrinking hose. The magnetic tweezer is powered with a laboratory power supply at a maximum current of 3 A (IPS 2303, RS PRO, United Kingdom). X-Y-Z-manipulation of the tweezer is achieved by mounting it on a manual and height adjustable 3D-stage on an optical post.

To attach magnetic beads onto single collagen fibrils (see Fig. 7), a single hair from an eyebrow is mounted onto a wooden toothpick using sticky tape. The hair is dipped into a container filled with quenched magnetic powder made from neodymium alloy and dragged over an outer edge of a microscope slide that is covered with collagen fibrils. 24-h curing epoxy resin is then mixed thoroughly (UHU-endfest, UHU, Germany), and a small droplet is transferred to the same microscope slide once more using an eyebrow hair. A single isolated magnetic bead is picked up by approaching the magnetic tweezer tip to it. To do so, the light microscope is focused onto the magnetic bead. When the tweezer tip is close, it becomes less blurry in the microscope view. The magnetic tweezer is then activated by applying a current of  $\sim 0.5$  A. Thereby, the magnetic bead leaps to the magnetic tweezer tip. For transferring the magnetic bead to the epoxy resin, the magnetic tweezer is deactivated and retracted to not attract further magnetic beads. For dipping the magnetic bead into the epoxy resin, a light microscope is focused on an edge of the epoxy resin, and the magnetic tweezer is activated with maximum current (3 A) and carefully approached toward the focus. The magnetic bead is then dipped into the epoxy resin at the edge that is in focus. Once a flow of the epoxy resin toward magnetic bead is observed, the magnetic tweezer is retracted and deactivated. By experience, the timespan of the magnetic bead being dipped into the epoxy should not last longer than  $2 - 3\mathrm{s}$ ; otherwise, the force between the epoxy resin and magnetic bead can become larger than the attraction force between the magnetic bead and magnetic tweezer (and the magnetic bead cannot be lifted and remains in the epoxy resin). Dipping the magnetic bead into the epoxy resin is a crucial step, as a sufficiently large epoxy meniscus is required around the magnetic bead. The larger the meniscus, the better the bonding between the magnetic bead and epoxy. (In a later step, just before tensile testing, the cured epoxy spot attached

![img-10.jpeg](img-10.jpeg)

![img-11.jpeg](img-11.jpeg)
FIG. 6. (a) Picture of the magnetic tweezer. The magnetic coil is covered by a shrinking hose for protection. (b) Light microscope image of the magnetic tweezer tip. The tip has a radius of about  $50~\mu \mathrm{m}$ .

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-6

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

![img-12.jpeg](img-12.jpeg)
FIG. 7. Gluing of single magnetic beads on collagen fibrils. (a) A spatially isolated magnetic bead is picked up by the magnetic tweezer. (b) While the magnetic tweezer is activated at maximum current, the magnetic bead is dipped into epoxy resin. (c) The magnetic bead is centered above a collagen fibril and then approached until in contact. (d) The deactivated magnetic tweezer is retracted, and the magnetic bead remains on the collagen fibril.

![img-13.jpeg](img-13.jpeg)

![img-14.jpeg](img-14.jpeg)

![img-15.jpeg](img-15.jpeg)

to the magnetic bead needs to be detached from the microscope slide. For a small meniscus, there is a chance that the magnetic bead detaches from the epoxy during this detachment.) Finally, the bead (with epoxy meniscus) is positioned above a collagen fibril and lowered onto it by approaching the magnetic tweezer toward the surface of the microscope slide, until epoxy resin is seen to run from the magnetic bead onto the microscope slide. After deactivation and retraction of the magnetic tweezer, the magnetic bead remains tethered to the collagen fibril as well as to the microscope slide. The other end of the collagen fibril is glued to the microscope slide by applying a droplet of epoxy resin using an ultra-fine tungsten probe (Model No. 52-001044, Micro to Nano, The Netherlands) at a desired distance to the magnetic bead. This distance should be matched to the z-piezo-lever actuator travel and specimen ultimate strain to enable tests until failure. In our case, testing collagen fibrils, this typical length was  $100\mu \mathrm{m}$ . After application of both the magnetic beads and the epoxy droplets (typically XX samples are prepared on each slide), the microscopy slide is dried in a vacuum desiccator for at least  $24\mathrm{h}$  or until measurement. Drying in a vacuum desiccator was found to yield more reliable detachment of the magnetic bead before tensile testing compared to drying in air at ambient conditions. Within  $30\mathrm{min}$ , about ten collagen fibrils can be prepared by this method, making it feasible to prepare around 20-30 collagen fibrils on a half-day, including dissection of a tendon and separation of single fibrils. The choice of the epoxy resin was made according to

the estimations by van der Rijt et al.,[11] who found only a negligible effect of the epoxy compliance on the measured collagen fibril strain. The strains and stress until failure were deemed useful, since the majority of collagen fibrils rupture in the central region when tested. In addition, we have already performed tensile tests on electrospun PLLA fibers (not part of this study and manuscript) with diameters from 250 to  $450\mathrm{nm}$  up to forces over  $50~\mu \mathrm{N}$  without visible slippage of the fiber out of the epoxy resin nor detachment of the magnetic beads from the fibers.

# E. Tensile testing protocol

As mentioned previously, collagen fibrils are investigated with the AFM prior to tensile testing by contact mode imaging in dry states and by AFM nanoindentation in PBS to assess the fibril height in both dry and hydrated states. For a detailed protocol, see Ref. 6. This is a necessity to validate the existence of collagen fibril D-banding, which is an indication a collagen fibril being present, and to assess the collagen fibril diameter. In brief, contact mode imaging is performed with a PNP-DB-A cantilever with  $0.48\mathrm{N / m}$  nominal stiffness (NanoWorld, Switzerland) over a collagen fibril segment of  $1.5\mu \mathrm{m}$  in length at the middle site between the magnetic bead and the epoxy droplet. The same segment is investigated through nanoindentation at  $1\mathrm{nN}$  setpoint after submerging into PBS using the same PNP-DB-A cantilever.

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-7

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

While still submerged in PBS (we have not yet performed tests in dry conditions), samples are transferred to the tensile testing instrument. With the help of an ultra-fine tungsten probe of the type used for application of epoxy droplets, collagen fibrils are cut behind the magnetic sphere. Then, by gently applying pressure on the magnetic sphere, the magnetic sphere along with the collagen fibril is disengaged from the microscope slide. Now, one end of the collagen fibril is tethered to the microscope slide, while the other end, which is attached to a magnetic sphere, is loose. Before a measurement can be conducted, the interferometer laser source has to be calibrated and

the output demodulation has to be linearized according to instructions by the manufacturer: The probe is placed in the environment in which testing will be carried out (in this case PBS), and the wavelength scan procedure of the OP1550 interferometer is initiated from the built-in interface. Thereby, gains and offset for optimizing the interferometer photodiode output are being set. Next, the cantilever of the force probe is brought into contact with a clean area of the microscope slide at a setpoint deflection of about $1\,\mu\mathrm{m}$. Once in contact, a demodulation calibration for linearization of the output signal is initiated from the interferometer interface. Datapoints for this are

![img-16.jpeg](img-16.jpeg)

![img-17.jpeg](img-17.jpeg)
FIG. 8. Sketches of the pick-up, testing, and re-initiation process. (a) Magnetic tweezer tip and microgripper are moved above a collagen fibril and into focus of the light microscope. (b) The magnetic tweezer is activated, causing a movement of the magnetic bead toward the magnetic tweezer tip. (c) The magnetic bead is picked up by the microgripper. (d) The collagen fibril is aligned with the z-axis and a tensile test is conducted. (e) After testing to failure, the magnetic tweezer is activated, (f) which causes the magnetic bead and remaining collagen fibril to move toward the magnetic tweezer. By that, the force probe is re-initiated and the next fibril can be picked up.

![img-18.jpeg](img-18.jpeg)

![img-19.jpeg](img-19.jpeg)

![img-20.jpeg](img-20.jpeg)

![img-21.jpeg](img-21.jpeg)

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-8

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

generated by subtle percussions of the optical table the light microscope is standing on. Alternatively, a piezo-lever actuator extension can be commanded during the linearization process to linearize the output over a larger range. Normally, a so-called geometric factor must also be determined to account for the different deflection of the cantilever between the location where deflection is measured with the optical fiber and the location where the force is transmitted from the collagen fibril to the microgripper. A geometric factor, which corrects for the deflection of the cantilever tip in relation to the optical fiber location, is determined by the manufacturer during their cantilever stiffness calibration. We use this pre-determined geometric factor to correct for the displacement of the collagen fibril force application point. This point is at a distance of about  $10 - 40\mu \mathrm{m}$  from the free cantilever edge [Figs. 10(m) and 12(a)]. Typically, the geometric factor is about 1.5 with a distance of about  $1 - 2\mathrm{mm}$  between the cantilever tip and the optical fiber, which is much larger than the uncertainty of the force application point. As discussed in Sec. III, the difference between the actual and nominal geometric factor only has a minor effect on force measurement accuracy.

After calibration and loosening the part of the collagen fibril with the magnetic bead from the substrate, everything is set up for tensile testing. The process of picking up a collagen fibril is visualized in Fig. 8. To lift the magnetic bead along with the collagen fibril, the tip of the magnetic tweezer is approached to the magnetic bead. At a distance of a few hundred micrometers, the magnetic tweezer is activated and the current is increased until the magnetic bead is moving toward the tip of the magnetic tweezer. Immediately, current is limited to a maximum of  $0.5\mathrm{A}$ , the magnetic tweezer is retracted by some hundred micrometers, and the magnetic bead is positioned above the epoxy droplet on the same collagen fibril by actuating the magnetic tweezer in the x-y-plane. By actuating the force probe with the stepper motor translation stage in x-y-z-directions, the microgripper is positioned below the magnetic bead with the magnetic bead roughly being close to the apex between the prongs of the microgripper. To pick up the magnetic bead, the stepper motor translation stage is then actuated in the z-direction until a force of about  $200\mathrm{nN}$  is measured. After deactivation and full retraction of the magnetic tweezer, the collagen fibril is aligned by scanning in the x-y-plane for the position of lowest force response. Prior to starting a tensile test, the collagen fibril is fully unloaded by actuation of the stepper motor translation stage in the z-direction. For tensile testing, only the piezo-lever actuator is employed and the fibril can be loaded in the desired loading patterns. Conditioning of the collagen fibril is advised before conducting a quantitative tensile test. We sometimes observe a slight movement of the magnetic bead during the very first tensile testing cycle. Thus, we introduced a conditioning step where we load and unload the collagen fibril with a piezo-lever actuator position maximum of  $5\mu \mathrm{m}$  for that the epoxy and magnetic bead can properly settle in the microgripper. Generally, the NanoTens can be used to test collagen fibrils up to failure, similar to a number of previously published studies that also use epoxy for coupling the collagen fibril on the substrate and force probe.[14,19,26-29] We did not observe any effect of compliance of the epoxy nor slippage of a collagen fibril out of the epoxy on either side. According to the manufacturer, the cantilevers can withstand a deflection of over  $10\mu \mathrm{m}$  without suffering damage. Usually, collagen fibrils fail in a force range between 5 and  $40~\mu \mathrm{N}$ , which roughly corresponds

![img-22.jpeg](img-22.jpeg)
FIG. 9. Light microscopy image of the remaining part of a collagen fibril after failure. We estimate the length of the part to be  $30~\mu \mathrm{m}$ . Consequently, the collagen fibril failed in the middle region of the tested segment, which was about  $100~\mu \mathrm{m}$  long.

to a cantilever deflection in the range from 0.5 to  $3\mu \mathrm{m}$ . In Fig. 9, the remaining part of a collagen fibril after testing to failure is shown. This part is  $\sim 30~\mu \mathrm{m}$  long, while the length of the tested segment was  $100~\mu \mathrm{m}$  in length. This shows that testing to failure is possible and that the collagen fibrils fail in the middle of the tested segment. After failure of the collagen fibril, the magnetic bead and remnant collagen fibril are withdrawn from the microgripper by coarsely approaching the magnetic tweezer tip and activation of the magnetic tweezer to the maximum current. Through this step, the instrument is set up for tensile testing the next collagen fibril.

# III. EXEMPLARY RESULTS AND COMPARISON TO LITERATURE

The protocol for tensile testing collagen fibrils (or other nanofibers) is as follows:

1. Collagen fibrils are sourced from collagenous tissue and deposited on microscope slides.
2. Application of magnetic beads and epoxy droplets and subsequent curing for at least  $24\mathrm{h}$  in a desiccator.
3. AFM imaging in contact mode of each collagen fibril to verify D-banding.
4. AFM nanoindentation in PBS to measure the collagen fibril diameter and indentation modulus.
5. Measurement of the collagen fibril length between the magnetic bead and epoxy droplet for strain calculation.
6. Disengagement of the magnetic beads.
7. Calibration of the interferometric force probe.
8. Lifting of the magnetic bead by activation of the magnetic tweezer and pick-up with the microgripper.
9. Conditioning of the collagen fibril.
10. Conduction of tensile tests.
11. Re-initiation of the interferometric force probe by "emptying" the microgripper.

The process of picking up a collagen fibril as observed under a light microscope is shown in Fig. 10. Before collagen fibrils are tensile tested, they are investigated through AFM nanoindentation to

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-9

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

![img-23.jpeg](img-23.jpeg)
FIG. 10. Overview of the entire experimental process. (a)-(d) Sample preparation from separation of a fascicle over deposition of individual collagen fibrils to attachment of magnetic beads and epoxy droplets. (e)-(h) AFM dry imaging and force indentation in PBS with an exemplary force curve. (i) Approach of the magnetic tweezer and the microgripper in vicinity to the magnetic bead that is attached to a collagen fibril (indicated with dashed line). (j) Collagen fibril is lifted by activation of the magnetic tweezer and positioned above the epoxy droplet on the other end of the collagen fibril. (k) The microgripper is positioned underneath the magnetic bead. (l) The collagen fibril is picked-up, the magnetic tweezer is deactivated, and the tensile test is conducted.

measure the collagen fibril diameter. Overall, interferometric force probe calibration, disengagement of the magnetic bead, and pick-up of the collagen fibril take about 5 min at a success rate of about  $90\%$ .

Exemplary force vs strain and stress vs strain diagrams of tensile tests of five collagen fibrils are displayed in Fig. 11. The samples tested are collagen fibrils sourced from mouse tail tendon of a 14 week old wild-type mouse. Prior to testing, the segment length of the tested collagen fibril is measured with the light microscope. Tensile tests are conducted at a strain rate of  $5\%/\mathrm{s}$ . Quantitative values for ultimate strain, ultimate strength, and collagen fibril diameter and initial collagen fibril length are given in Table I. Collagen fibrils

of the tested mouse tail tendon reach a peak force of  $5.0 \pm 1.1 \mu \mathrm{N}$ . After normalizing with the collagen fibril area in the hydrated state (assuming circular shape and diameter as per AFM nanoindentation measurements), the same fibrils display an ultimate tensile strength of  $0.11 \pm 0.06 \mathrm{GPa}$  at  $28.3\% \pm 8.4\%$  strain.

To validate the data measured with the NanoTens, it is compared with data available in the literature. Over the past two decades, several different methods were developed, and collagen fibrils from a small range of collagenous tissues sourced from animals at different ages and also with artificial cross-linking have been tested. For validation, a selection of these results is taken, mainly focusing on

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-10

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

![img-24.jpeg](img-24.jpeg)
FIG. 11. (a) Exemplary force vs strain diagram of five collagen fibrils tested to failure. (b) Measuring collagen fibril diameter of each tested collagen fibril before tensile testing enables calculation of stress by dividing the measured force by the collagen fibril area.

![img-25.jpeg](img-25.jpeg)

tissues from rodents. Svensson et al. $^{14}$  reported an ultimate modulus of  $(0.20 \pm 0.11)$  GPa at  $(16 \pm 4)\%$  strain for fibrils from tail-tendons of rats, 12 weeks of age. These results were obtained using AFM-based tensile tests. Svensson et al. normalized measured forces with cross-sectional areas of the dried collagen fibrils, in contrast to the method proposed here. As collagen fibrils swell by roughly  $50\%$  or even higher, $^{5,15}$  ultimate tensile strengths reported by Svensson et al. can be estimated to be about  $(0.10 \pm 0.06)$  GPa (when normalized to diameters in the hydrated state), which is also in agreement with  $(0.11 \pm 0.06)$  GPa reported here. However, we reported an ultimate strain of  $(28 \pm 8)\%$  deviating from  $(16 \pm 4)\%$  reported by Svensson et al. $^{14}$  This can be attributed to the different type of tissue being tested, the length of the collagen fibril  $(40 \mu \mathrm{m}$  by Svensson et al. $^{14}$  vs  $100 \mu \mathrm{m}$  in gauge length), and, therefore, end-effects and, most importantly, differences in strain rate  $(100\%/\mathrm{s}$  vs  $5\%/\mathrm{s})$ . Using a custom tensile testing device, Svensson et al. $^{26}$  reported an ultimate strength of 80 (70-100) MPa (mean and geometric standard error) at 20 (16-25)% ultimate strain of tail-tendon fibrils from rats, 16 weeks of age. Yang et al. $^{12}$  measured an ultimate strength of  $(60 \pm 10)$  MPa at  $(13 \pm 2)\%$  strain of reconstituted fibrils from bovine Achilles tendon collagen type I with AFM. Liu et al. $^{19}$  reported  $(71 \pm 23)$  MPa ultimate strength at  $(63 \pm 21)\%$  strain of rat patellar tendon fibrils measured with a custom micro-electromechanical system (MEMS). Overall, our results are well within the range of previously reported results; however, a precise cross-comparison is not possible due to varying testing protocols, sample geometries, the strain rate at which tensile tests are conducted, sample preparation (including the method of collagen fibril extraction and tissue

TABLE I. Measured ultimate mechanical properties (force f, stress  $\sigma$  and strain  $\varepsilon$  ) of the collagen fibril. The hydrated collagen fibril diameter is used for calculation of stress, and the initial length is used for calculation of strain. Data are represented in mean  $\pm$  std.

|   | fult(μN) | σult(GPa) | εult(%) | Diameter(nm) | Length(μm)  |
| --- | --- | --- | --- | --- | --- |
|  f1 | 5.0 | 0.16 | 28.3 | 208.2 | 100.2  |
|  f2 | 5.6 | 0.18 | 23.1 | 321.1 | 98.7  |
|  f3 | 3.1 | 0.05 | 40.5 | 289.5 | 102.9  |
|  f4 | 5.9 | 0.09 | 18.1 | 283.7 | 107.6  |
|  f5 | 5.2 | 0.07 | 33.5 | 306.8 | 98.6  |
|  Mean | 5.0 ± 1.1 | 0.11 ± 0.06 | 28.7 ± 8.7 | 281.9 ± 43.7 | 101.6 ± 3.8  |

storing conditions), unknown variabilities in chemical composition, conditions (dry/wet, temperature) during the test, and finally the experimental method itself. Certainly, the impact of the experimental method is narrowed by the proposed method. In contrast to the other existing methods, all collagen fibrils studied with the NanoTens can be investigated with the exact same interferometric force probe, leading to a better fibril to fibril precision and hence comparison across samples.

Beyond this feature, two more advantages of the proposed method in this work are the high-throughput and force resolution. The number of samples thus far reported in the literature is low mainly due to the high time-demand of such experiments. For comparison, an AFM-based tensile test requires about  $50\mathrm{h}$  time for sample preparation and testing an individual collagen fibril blocking the instrument during this time. In contrast, the preparation process for the NanoTens can be parallelized such that it takes about  $5\mathrm{min}$  to pick-up a collagen fibril with the proposed method adding only the time for the actual test. Compared to other methods that rely on CCD camera measurements for either force or strain, we achieve better resolution and are able to perform dynamic tensile testing. Tensile force is measured with  $10\mathrm{nN}$ $(\mathfrak{p} - \mathfrak{p})$  resolution while still achieving  $0.1\%$  strain resolution at a pulling speed of  $100~\mu \mathrm{m / s}$ , in the case of  $100~\mu \mathrm{m}$  long collagen fibrils and  $1\mathrm{kHz}$  sampling frequency. By increasing the sampling frequency, we could further increase pulling speed while maintaining  $0.1\%$  strain resolution. The maximum z-displacement in the current setup is  $100~\mu \mathrm{m}$ , which can be adapted to a larger travel range by employing another z-piezo-lever actuator. This, however, comes with a decrease of strain resolution at similar collagen fibril length. Further adjustment of the method can be made by performing tensile tests using force probes with different stiffnesses. If samples of lower stiffness are to be tested, a force probe with lower stiffness can be used, and vice versa, a stiffer probe for stiffer samples. Our experience so far is that the method is limited at the lower end to fibers with a diameter of around  $70\mathrm{nm}$ . This limitation essentially stems from the resolution of the inverted microscope: fibers or collagen fibrils need to be optically identifiable. The smallest fibers we could successfully test to date had diameters of about  $70\mathrm{nm}$  in air. The upper limit of the sample diameter is determined by the stiffness and strength of the fiber to be tested. With adaptations of the force probe as well as of the geometry of the microgripper, we estimate that forces of up to a few hundred  $\mu \mathrm{N}$  are feasible.

A limitation of the presented method is that the collagen fibril is pulled perpendicular to the focal plane of the light microscope.

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-11

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

![img-26.jpeg](img-26.jpeg)
FIG. 12. Process of extraction of a collagen fibril from the microgripper after mechanically testing it. (a) A collagen fibril aligned over the epoxy droplet on the substrate after tensile testing. (b) The microgripper is approached to the magnetic bead, and the force probe is approached toward the epoxy droplet and slightly moved to the right. (c) The magnetic bead is lifted and the microgripper is moved to the right. (d) Collagen fibril and magnetic bead deposited on the substrate. It can be picked-up following the procedure shown in Fig. 10 and mechanically tested again.

![img-27.jpeg](img-27.jpeg)

![img-28.jpeg](img-28.jpeg)

![img-29.jpeg](img-29.jpeg)

Consequently, the fibril cannot be observed during a tensile test, different to the method published by Svensson et al. [26,27] They optically measured local strains along the collagen fibril and by that could correct global strain (which is what is measured with the NanoTens) measurements for end-effects at sites where collagen fibrils emerge from epoxy resin. Estimation of end-effects is certainly important to achieve better accuracy in strain and tensile modulus measurements. This remains a possible improvement of the NanoTens in the future. While optical observation of the end-effects may also allow determination of potential movement of the magnetic bead in the microgripper during a tensile test, we have to date, after conditioning, never observed movements of the bead in the NanoTens during testing.

A clear advantage of the sample coupling mechanism presented here is that the attachment of the collagen fibril to the force probe is reversible. This means that an individual collagen fibril can be repeatedly lifted, picked-up, tested, and afterward placed down on the microscope slide again. To do so, a collagen fibril has to be extracted from the microgripper without damaging it. In Fig. 12, the process of extracting a collagen fibril from the microgripper following a tensile test is shown. In short, the stepper motor translation stage is moved by  $30\mu \mathrm{m}$  toward the microscope slide and the magnetic tweezer is approached to the magnetic bead. After activation of the magnetic field, the stepper motor translation stage is moved laterally to leave the lifted magnetic bead along with the attached collagen fibril. Without touching the magnetic bead, the magnetic tweezer is moved laterally and lowered to the microscope slide. After switching off the magnetic field, the magnetic tweezer is moved away from the magnetic bead until no more movement of the magnetic bead is visible.

To show the reproducibility of this procedure, we conducted an exemplary experiment. We subjected an individual collagen fibril three times to tensile strain by extending it  $10\mu \mathrm{m}$ , unloaded it, and placed it on the microscope slide after each run. Before each run, we adjusted the z-position of the force probe with the stepper motor translation stage to the point where  $\sim 100 - 200\mathrm{nN}$  of force was applied to the collagen fibril. We then aligned the collagen fibril in the x-y-plane to the position with minimum force response. Before conducting tensile tests with the piezo-lever actuator, we lowered the z-position of the stepper motor translation stage to avoid applying preload to the collagen fibril. Finally, the tensile test was conducted from this z-position to a piezo-lever actuator displacement of  $10\mu \mathrm{m}$ .

As the stepper motor translation stage has a bi-directional repeatability of  $3\mu \mathrm{m}$ , the exact starting z-position is different for each run. Consequently, the  $10\mu \mathrm{m}$  piezo-lever actuator displacement results in a different collagen fibril strain. This can be avoided in the future by performing the tensile tests from a specific preload of, for example, 50 or  $100\mathrm{nN}$ . The resulting stress vs strain diagram is shown in Fig. 13, where each run comprises three single curves. Overall, the single curves overlap almost perfectly, indicating good repeatability of the proposed method. Run 3 seems to have a slightly larger (by about  $0.1\%$  strain) toe region that could arise due to differences in alignment of the collagen fibril prior to mechanical testing or in the geometric factor compared to the other two runs. However, curves of run 3 are only offset to slightly higher strains, while the slope of the curves reaches the same values as in runs 2 and 3. Hence,

![img-30.jpeg](img-30.jpeg)
FIG. 13. Stress vs strain diagram of the same collagen fibril after repeated pickup and alignment. Each run is comprised of three measurements. Run 3 appears to be slightly affected by different alignment and placement of the magnetic bead in the microgripper. However, this only affects the behavior up to  $3\%$  strain by shifting the curve to the right by about  $0.1\% - 0.2\%$  strain. The slope, and thus the tensile modulus, is almost equal after repeated pick-up and alignment procedures, as determined by visual assessment of the stress vs strain curves.

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-12

---

Review of Scientific Instruments

ARTICLE

scitation.org/journal/risi

determination of the tensile modulus is repeatable. This approach offers the possibility to repeatedly measure the tensile modulus of a collagen fibril and, e.g., chemically modify it in between measurement runs.

Overall, including sample preparation as well as AFM imaging and nanoindentation, about 30–50 collagen fibers can be tested in a week, whereby AFM imaging and indentation prior to tensile testing are becoming the bottleneck. This is done with demonstrated accuracy and precision.

## IV. CONCLUSION

We report a new method to couple single collagen fibrils to a cantilever-based force probe with a non-permanent connection. This allows for facile and quick coupling and uncoupling of collagen fibrils compared to state-of-the-art-methods. Furthermore, the same force probe can be used for hundreds of tests, which means that in most cases only one force probe is used to conduct an entire study. This increases fibril to fibril precision by avoiding inaccuracies in the calibration of a force probe for each individual tensile test. The collagen fibril strain and force are measured with a minimum sampling frequency of 1 kHz, enabling dynamic measurements at 10 nN (p–p) force resolution and better than 0.1% strain resolution. We described in detail how magnetic beads are glued onto single collagen fibrils using a custom magnetic tweezer. The same tweezer is used to lift the collagen fibril by magnetic force setting it up to be picked up by a microgripper. The 2PP printed microgripper is mounted on a cantilever based interferometric force probe that is actuated by a piezo-lever actuator. Piezo-lever actuator position and collagen fibril force are measured by a CompactRIO system that is equipped with a FPGA. Future development steps will enable hardware closed-loop control of collagen fibril force and strain. By that, first true creep and relaxation tests on fibers at that scale will be conducted.

The proposed method is not only applicable for tensile testing of collagen fibrils. Any flexible fiber with diameters from about 70 nm up to 10 μm can be investigated in a force range from unloaded to 500 μN. In particular, electrospinning is a major research area with great potential for tissue engineering, while tensile mechanical properties of single fibers are not systematically investigated.

## ACKNOWLEDGMENTS

The authors would like to thank Professor Roland Bennewitz (INM Leibniz Institute for New Materials, Saarbrücken, Germany) for provision of the magnetic powder and Professor Peter Pietschmann (MedUni Wien, Vienna, Austria) for provision of mouse tail samples. This work was, in part, supported by a grant of the Austria Wirtschaftsservice Gesellschaft mbH (Grant No. P2018042).

## AUTHOR DECLARATIONS

### Conflict of Interest

The authors have no conflicts to disclose.

## DATA AVAILABILITY

The data that support the findings of this study are available from the corresponding author upon reasonable request.

## REFERENCES

1. T. J. Wess, *Advances* 70, 341 (2005).
2. K. E. Kadler, D. F. Holmes, J. A. Trotter, and J. A. Chapman, *Biochem. J* 316, 1 (1996).
3. O. G. Andriotis, W. Manuyakorn, J. Zekonyte, O. L. Katsamenis, S. Fabri, P. H. Howarth, D. E. Davies, and P. J. Thurner, *J. Mech. Behav. Biomed. Mater* 39, 9 (2014).
4. C. J. Peacock and L. Kreplak, *Nanoscale* 11, 14417 (2019).
5. S. J. Baldwin, A. S. Quigley, C. Clegg, and L. Kreplak, *Biophys. J* 107, 1794 (2014).
6. O. G. Andriotis, S. W. Chang, M. Vanleene, P. H. Howarth, D. E. Davies, S. J. Shefelbine, M. J. Buehler, and P. J. Thurner, *J. R. Soc., Interface* 12(111), 20150701 (2015).
7. A. J. Heim, W. G. Matthews, and T. J. Koob, *Appl. Phys. Lett* 89(18), 181902 (2015).
8. C. A. Grant, D. J. Brockwell, S. E. Radford, and N. H. Thomson, *Biophys. J* 97(11), 2985 (2009).
9. M. P. E. Wenger, L. Bozec, M. A. Horton, and P. Mesquida, *Biophys. J* 93, 1255 (2007).
10. S. J. Baldwin, J. Sampson, C. J. Peacock, M. L. Martin, S. P. Veres, J. M. Lee, and L. Kreplak, *J. Mech. Behav. Biomed. Mater* 110, 103849 (2020).
11. J. A. J. Van Der Rijt, K. O. Van Der Werf, M. L. Bennink, P. J. Dijkstra, and J. Feijen, *Macromol. Biosci* 6, 697 (2006).
12. L. Yang, K. O. van der Werf, P. J. Dijkstra, J. Feijen, and M. L. Bennink, *J. Mech. Behav. Biomed. Mater* 6, 148 (2012).
13. O. G. Andriotis, S. Desissaire, and P. J. Thurner, *ACS Nano* 12(4), 3671 (2018).
14. R. B. Svensson, H. Mulder, V. Kovanen, and S. P. Magnusson, *Biophys. J* 104, 2476 (2013).
15. P. Hansen, T. Hassenkam, R. B. Svensson, P. Aagaard, T. Trappe, B. T. Haraldsson, M. Kjaer, and P. Magnusson, *Connect. Tissue Res* 50, 211 (2009).
16. R. B. Svensson, T. Hassenkam, P. Hansen, and P. Magnusson, *J. Mech. Behav. Biomed. Mater* 3, 112 (2010).
17. R. B. Svensson, T. Hassenkam, C. A. Grant, and P. Magnusson, *Biophys. J* 99, 4020 (2010).
18. Z. L. Shen, M. R. Dodge, H. Kahn, R. Ballarini, and S. J. Eppell, *Biophys. J* 95, 3956 (2008).
19. Y. Liu, R. Ballarini, and S. J. Eppell, *Interface Focus* 6(1), 20150080 (2016).
20. A. S. Quigley, S. P. Veres, and L. Kreplak, *PLoS One* 11(9), e0161951 (2016).
21. A. S. Quigley, S. Banceli, D. Deska-gauthier, F. Légaré, L. Kreplak, and S. P. Veres, *Sci. Rep* 8, 4409 (2018).
22. A. Dobos, J. Van Hoorick, W. Steiger, P. Gruber, M. Markovic, O. G. Andriotis, A. Rohatschek, P. Dubruel, P. J. Thurner, S. Van Vlierberghe, S. Baudis, and A. Ovsianikov, *Adv. Healthcare Mater* 9, 1900752 (2020).
23. K. Cicha, T. Koch, J. Torgersen, Z. Li, R. Liska, and J. Stampfl, *J. Appl. Phys* 112(9), 094906 (2015).
24. J. Stampfl, S. Baudis, C. Heller, R. Liska, A. Neumeister, R. Kling, A. Ostendorf, and M. Spitzbart, *J. Micromech. Microeng* 18, 125014 (2008).
25. P. Kollmannsberger and B. Fabry, *Rev. Sci. Instrum* 78, 114301 (2007).
26. R. B. Svensson, S. T. Smith, P. J. Moyer, and S. P. Magnusson, *Acta Biomater* 70, 270 (2018).
27. R. B. Svensson, C. S. Eriksen, P. H. T. Tran, M. Kjaer, and S. P. Magnusson, *J. Mech. Behav. Biomed. Mater* 124(104864), (2021).
28. Z. L. Shen, M. R. Dodge, H. Kahn, R. Ballarini, and S. J. Eppell, *Biophys. J* 99, 1986 (2010).
29. J. Liu, D. Das, F. Yang, A. G. Schwartz, G. M. Genin, S. Thomopoulos, and I. Chasiotis, *Acta Biomater* 80, 217 (2018).

Rev. Sci. Instrum. 93, 054103 (2022); doi: 10.1063/5.0072123

© Author(s) 2022

93, 054103-13
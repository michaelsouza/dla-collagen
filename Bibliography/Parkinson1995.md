J. Mol. Biol. (1994) 247, 823-831

# JMB

# Simple Physical Model of Collagen Fibrilogenesis Based on Diffusion Limited Aggregation

John Parkinson, Karl E. Kadler and Andy Brass

School of Biological Sciences
2.205 Stopford Building
University of Manchester
Oxford Rd, Manchester
M13 9PT, UK

Type I collagen is a rod-like protein which self-assembles in a regular array to form elongated fibrils. The process of fibril formation, termed fibrillogenesis, is driven by the increase in entropy associated with loss of water from the bound monomers. A model based on diffusion limited aggregation (DLA) was used to investigate some of the mechanisms involved in this process. The aggregates created in the model displayed several features in common with collagen fibrils including an elongated morphology and a preference for tip growth. Analysis of these aggregates revealed a linear relationship between mass and distance from the tip, consistent with experimental observations. Intrafibrillar fluidity was introduced into the model by using a surface diffusion term. This led to the formation of aggregates with more compact morphologies. These results strongly implicate the role of diffusion limited growth in collagen fibril formation.

Keywords: diffusion limited aggregation; collagen; fibrillogenesis; self-assembly; computer modelling

# Introduction

Type I collagen is one of the most abundant proteins in tissues such as skin, bone, ligament and tendon where it occurs predominantly in the form of large elongated fibres called fibrils. The function of these fibrils is to provide structural strength within tissues and to form a framework within which other components of the extra-cellular matrix can interact (Kielty et al., 1993). Although fibril formation has been studied extensively for many years, the physical and/or biological mechanisms controlling fibril formation and morphology still remain unclear (for reviews and references see Kadler, 1994).

The soluble collagen precursor, procollagen, is a trimeric molecule and contains three distinct domains: an N-terminal propeptide, a central triple-helical collagenous domain and a C-terminal propeptide. Mature collagen is produced when the N- and C-propeptides are removed by the procollagen metallo-proteinases (for reviews, see Kadler &amp; Watson, 1995; Kadler et al., 1995). The resulting collagen molecule is rod-like (300 nm × 1.5 nm), and spontaneously self-assembles to form fibrils in a process known as fibrillogenesis (Prockop et al., 1979). These fibrils can vary greatly in length and diameter depending upon the conditions involved in growth. However, fibrils

grown in vitro are typically up to 500 nm in diameter, several tens of µm long and contain between 10⁴ and 10⁶ mature collagen molecules (values calculated from data presented by Parry &amp; Craig, 1984). Electron microscope analysis of fibrils has shown that the collagen molecules are staggered by integrals of D with respect to one another (where D = 67 nm), giving five possible binding conformations for collagen-collagen interaction (for a discussion, see Chapman &amp; Holmes, 1984) (see Figure 1).

Quantitative scanning transmission electron microscopy of the tapered ends of fibrils formed in vitro and in vivo show that the mass of a fibril tip increases linearly with distance from the end, suggesting that the tips are paraboloidal in shape (Holmes et al., 1992). Typically human fibrils increase in mass by around 17 molecules per D-period (mol/D: Kadler et al., 1990). However, values for the rate of mass increase within the range 2.5 to 150 mol/D have been observed for fibrils formed at different rates (D. F. Holmes, personal communication).

Several different models have been proposed to describe the way in which collagen molecules are laterally packed in fibrils. In one model, based on X-ray fibre diffraction, it has been proposed that molecules are arranged in a quasi-hexagonal lattice (Hulmes et al., 1981; Fraser et al., 1987). Other models propose that fibrils consist of sub-units, termed microfibrils, such as pentamers (Veis et al., 1967; Trus &amp; Piez, 1980). Calculations on the packing density of fibrils based on these models suggest that the

0022-2836/95/140823-08 $08.00/0

© 1995 Academic Press Limited

---

Simple Model of Collagen Fibrillogenesis

![img-0.jpeg](img-0.jpeg)
Figure 1. The collagen molecule is approximately 4.5D-periods in length. Electron microscopy has demonstrated that collagen molecules are staggered by integrals of $D$ with respect to each other. Therefore there are 5 specific ways in which 2 molecules can bind to each other, defined as the $0D$, $1D$, $2D$, $3D$ and $4D$ staggers, depending upon the length of the overhang.

quasi-hexagonal model most closely resembles experimental data (Hulmes &amp; Miller, 1979). Furthermore, electron microscope observations of fibrils formed in vitro in the absence of collagen specific cross-links show evidence of considerable lateral fluidity of collagen molecules (Watson et al., 1992).

It is known that collagen is capable of aggregating in vitro to produce fibrils with morphologies close to those seen in vivo (Miyahara et al., 1982; Kadler et al., 1987, 1990; Holmes et al., 1992). Thermodynamic studies of in vitro fibril formation as a function of collagen density have shown that the major contribution to the free energy of binding for collagen molecules to the growing fibril is entropic, the enthalpic contribution being positive (Kadler et al., 1987). This implies that the major driving force for fibril formation is the hydrophobic interaction between collagen molecules leading to the minimisation of surface exposed to water. The in vitro studies suggest that the collagen molecule itself contains all the information needed to control fibril formation. These processes of self-assembly and self-organisation may also play important roles in controlling fibrillogenesis in vivo. However, it is not known whether fibril morphology is controlled by specific collagen-collagen interactions occurring within the growing fibril, or whether the observed fibril morphologies might be expected for any self-aggregating system of rod-like particles.

A number of previous theoretical and mathematical studies have examined simple biological self-assembly processes such as virus coat assembly (Butler, 1984), amyloid plaque formation (Tomski &amp; Murphy, 1992) and microtubule assembly (Frieden, 1985; Dogterom &amp; Leibler, 1993). In these phenomena, the number of sites available to an accreting monomer either remains constant with respect to the size of the aggregate (amyloid plaque formation, micro tubule assembly) or occurs in a precise well-defined manner (virus coat assembly). Due to

their relative simplicity, these systems have proved amenable to mathematical analysis (for example with differential equations).

Such simple analyses are not possible on fibrillogenesis since the number of sites available to a newly accreting particle increases in an unpredictable fashion depending on the previous growth history of the fibril. This property of fibril growth makes a straightforward mathematical analysis impossible. Previously we adopted a novel approach involving the use of diffusion limited aggregation (DLA: Witten &amp; Sander, 1981, 1983; for a review, see Meakin, 1988) to model the aggregation of rod-like molecules in two-dimensions (Parkinson et al., 1994). Here, we have expanded this model to three-dimensions to simulate the aggregation of rod-like molecules from dilute solution. Surface diffusion was included in some simulations to model the intrafibrillar diffusion suggested by Watson et al. (1992). Several features of the behaviour of collagen in solution (e.g. angular motion) have been omitted from this model and could be included in future simulations. The question we wished to address here was "could the observed collagen fibril morphology have arisen through a simple physical process?"

# Results

Two sets of DLA simulations were performed, one using the non-specific binding rules, the other the collagen-specific binding rules. Aggregates of either 10,000 or 45,000 particles were grown in which the value of the surface diffusion time, $T_{S}$, was varied between 1 (no diffusion) and 10,000 (high surface mobility).

Figure 2 shows two aggregates containing 45,000 rods grown using the collagen-specific binding rules with high and low values of $T_{S}$. Both aggregates clearly have a fibrillar morphology (pencil shaped with two pointed ends), however the structure grown with $T_{S} = 1$ is very open and fractal-like, whereas the structure grown at $T_{S} = 10,000$ is much more compact.

Figure 3 shows a series of cross-sections taken perpendicular to the long axis of aggregates containing 10,000 rods for a range of $T_{S}$ values and grown using either the collagen-specific or non-specific binding rules for the rod-rod interactions. The results show that the aggregate density increases as a function of $T_{S}$. This observation was supported by calculations of the aggregate densities as a function of $T_{S}$ (Table 1). Table 1 lists the typical maximum radii and lengths measured for all of the 10,000-rod aggregates generated.

The mass per unit length profiles for a selection of the aggregates is shown in Figure 4. The profiles were obtained by counting the number of particles in cross-sections of uniform thickness. Each aggregate displayed a linear relationship between mass and distance from the tip irrespective of whether collagen-specific or non-specific binding rules were used, or whether the aggregate was compact $(T_{S} = 10,000)$ or open $(T_{S} = 1)$. In addition some

---

Simple Model of Collagen Fibrillogenesis
825

![img-1.jpeg](img-1.jpeg)
Figure 2. Computer images of 2 aggregates composed of 45,000 particles generated by the model. The aggregate shown in (a) and (b) was grown without surface diffusion; (c) and (d) are views of an aggregate grown with surface diffusion ($T_{S} = 10,000$). The colours indicate time of arrival of the rods, blue rods being the last to accrete to the cluster.

profiles also displayed abrupt changes in the gradient certain distances from the tip (e.g. at a distance of 600 lattice units from the tip of the aggregate grown using non-specific binding rules with $T_{S} = 10,000$). From the gradient of these lines it could be determined that all the aggregates increased in mass at 1 to $1.5\,\mathrm{mol}/D$ from tip to centre.

For all the simulations run using the collagen-specific binding rules the number and types of all the rod-rod overlaps was determined. Figure 5 shows the distribution of the different types of stagger within aggregates as a function of $T_{S}$. When surface diffusion was omitted from the simulation ($T_{S} = 1$), the $4D$ stagger was the predominant species. As $T_{S}$ increased there was a corresponding increase in the number of $0D$ and $1D$ staggers at the expense of $2D$, $3D$ and $4D$ staggers.

The results obtained from repeating the simulations on a cubic lattice were similar to those reported here (data not shown). This suggests that the choice of lattice is not an important parameter of the model.

## Discussion

### Aggregate morphology

All the aggregates formed in the simulations had a characteristic fibrillar morphology. The fractal-like aggregates obtained from the simulations run without surface diffusion are typical of those created using DLA growth models in that branch formation

was favoured. Branches appear when a nick occurs in an aggregate surface, new particles are then prevented from reaching the bottom of the nick since they are more likely, statistically, to encounter an edge first. Thus the outside of the aggregate effectively "screens" the interior from further growth leading to the rapid evolution of branches. In a similar way, the tips of elongated particles screen the rest of the aggregate from incoming particles resulting in the elongated morphologies observed. The density of the aggregates formed without surface diffusion was $10\%$ suggesting that the simulated aggregates are far more open than collagen fibrils (in which $80\%$ of the sites are thought to be occupied (Katz &amp; Li, 1973)).

The aggregates produced using the non-specific binding rules were consistently longer than those produced with the collagen-specific binding rules. One of the basic premises of DLA is a preference for tip growth (Stanley, 1992); the most likely way for two rods to attach is therefore at their tips. Using the non-specific binding rules rods often stick with an overlap of only one lattice unit whereas when using the collagen-specific binding rules the smallest such overlap is two lattice units (representing a $4D$ stagger). Therefore, on average, aggregates produced using the non-specific binding rules will contain more short overlap (and therefore longer bonds) than are allowed with the collagen-specific rules.

The number of particles included in the simulated aggregates was equivalent to the number of collagen molecules found in a small fibril (calculated from

---

Simple Model of Collagen Fibrilogenesis

data obtained by Parry &amp; Craig, 1984), making it possible to compare the simulated aggregates to collagen fibrils without having to make corrections for finite-size effects. Assuming that the rods in the simulations had the same dimensions as a collagen molecule, then from Table 1 the approximate aggregate dimensions would be $35\,\mu\mathrm{m} \times 0.1\,\mu\mathrm{m}$. The

dimensions of collagen fibrils grown *in vitro* are found to vary considerably depending upon factors such as the temperature of incubation and the concentration of C-proteinase (D. F. Holmes, personal communication). The fibrils produced by our model most closely resembled experimental fibrils grown at the relatively high temperature of

![img-2.jpeg](img-2.jpeg)
(a)

![img-3.jpeg](img-3.jpeg)
(b)

![img-4.jpeg](img-4.jpeg)
(c)

![img-5.jpeg](img-5.jpeg)
(d)

![img-6.jpeg](img-6.jpeg)
(e)

![img-7.jpeg](img-7.jpeg)
(a)

![img-8.jpeg](img-8.jpeg)
A
(b)

![img-9.jpeg](img-9.jpeg)
(c)

![img-10.jpeg](img-10.jpeg)
(d)

![img-11.jpeg](img-11.jpeg)
(b)
(e)
Figure 3. Cross sections through the centre of aggregates composed of 10,000 particles. A, Aggregates created using non-specific rules of binding. B, Aggregates created using collagen specific rules of binding. In each part (a) $T_{\mathrm{x}} = 1$, (b) $T_{\mathrm{x}} = 10$, (c) $T_{\mathrm{x}} = 100$, (d) $T_{\mathrm{x}} = 1000$, (e) $T_{\mathrm{z}} = 10,000$. The sections are 1 lattice unit in depth.

---

Simple Model of Collagen Fibrilogenesis
827

Table 1
Dimensions of aggregates consisting of 10,000 particles grown using a variety of different conditions

|   | T_{s} | Length (lattice units) | Radius (lattice units) | Density (% occupied sites)  |
| --- | --- | --- | --- | --- |
|  Collagen-specific binding rules | 1 | 2056 | 33 | 18  |
|   |  10 | 2048 | 24 | 30  |
|   |  100 | 2180 | 19 | 58  |
|   |  1000 | 2232 | 22 | 66  |
|   |  10,000 | 2172 | 24 | 54  |
|  Non-specific binding rules | 1 | 2299 | 40 | 9  |
|   |  10 | 2287 | 31 | 23  |
|   |  100 | 2352 | 18 | 61  |
|   |  1000 | 2335 | 18 | 60  |
|   |  10,000 | 2364 | 13 | 60  |

37°C using a relatively low concentration of C-proteinase.

This resemblance to fibrils grown at the relatively higher temperature of 37°C is a result of the implicit assumption in our model that all overlaps between rods were equally stable, i.e. an incoming rod was just as likely to attach to the aggregate by a 4D overlap (contact length 0.5D-periods) as it was with a 0D overlap (contact length 4.5D-periods). Fibrilogenesis is entropy-driven, i.e. by collagen molecules losing water by attaching to the aggregate (Kadler et al., 1987). The entropic contribution to the free energy of binding is -TΔS, where T is the temperature and ΔS is the change in entropy on binding. Over the range of temperatures, 24 to 41°C, the enthalpic contribution to the free energy of binding, H, is positive and approximately constant. A necessary condition for binding is therefore that:

$$
T \Delta S &gt; H \tag {1}
$$

The value of ΔS for short overlaps will be smaller than that for large overlaps (because less water is displaced on binding). At low temperatures equation (1) will only be satisfied for interactions with large overlaps whereas at higher temperatures it may be possible to satisfy equation (1) with smaller overlaps. As a 4D overlap is just as stable as a 0D overlap in the simulation this suggests that the aggregates should resemble the relatively high rather than low temperature fibril morphologies.

## Effect of surface diffusion

The inclusion of surface diffusion made the fibrils much more compact, increasing the density of the aggregates from 10% to 55 to 65%. The aggregates generated with high T<sub>s</sub> values were slightly longer than those generated at low values of T<sub>s</sub>. From Figure 4 it can be seen that the mass distributions for the high and low T<sub>s</sub> aggregates are similar, however the higher density of the high T<sub>s</sub> aggregates means that their actual radii are much smaller (Table 1). The density as a function of T<sub>s</sub> closely approaches an asymptote at around T<sub>s</sub> = 100. The maximum circumference to be explored by a

diffusing particle was of the order 200 lattice units (calculated from the values in Table 1). Therefore the maximum aggregate packing densities were obtained for any value of T<sub>s</sub> that allowed an attaching particle time to explore the majority of the fibril circumference.

## Mass per unit length profiles

All the aggregates formed in the simulations had linear mass per unit length profiles, irrespective of whether the structures were open or compact, formed with collagen-specific or non-specific binding rules, or had paraboloidal or highly branched tips. Recently, abnormal fibrils have been grown using collagen obtained from a patient suffering from Ehlers-Danlos syndrome. Scanning transmission electron microscope (STEM) analysis of these fibrils revealed a linear relationship between mass and distance from the tip despite the fact that such fibrils have irregular cross-sections (R. T. Watson, D. F. Holmes &amp; K.E.K., unpublished results). In certain aggregates there appeared to be an abrupt change in the gradient of the profiles at some distance from the tip. Such changes have also been observed in fibrils grown experimentally (D. F. Holmes, J. A. Chapman &amp; K.E.K., unpublished results) and may reflect the potentially large changes that apparent minor fluctuations in growth can have on fibril morphology. The gradient of the profiles obtained from our simulated fibrils, 1.5 mol/D, is small compared to those observed for human collagen fibrils (which can vary from 2.5 mol/D to 150 mol/D depending upon growth conditions), however, it does lie within the range of values observed for fibrils obtained from echinoderms (Trotter et al., 1994). It is interesting to note that whereas the mass profiles for mammalian and avian fibrils are flat along the shaft of the fibril (D. F. Holmes, personal communication), the simulated aggregates have triangular profiles similar to those observed in echinoderm fibrils (Trotter et al., 1994). These results suggest that there must be some additional mechanism, not included in our model, which acts to limit the maximum diameter that avian and mammalian fibrils can attain.

---

Simple Model of Collagen Fibrillogenesis

# Rod-rod interactions within the aggregates

Since the discovery that individual collagen molecules are staggered by integrals of $D$ with respect to each other, there has been much discussion as to the actual types of stagger that are important during collagen fibrillogenesis. Electron micrographs of initial aggregates suggest that the $4D$ stagger is important in fibrillogenesis (Ward et al., 1986; Fleischmajer et al., 1991). However, this is contrary to thermodynamic studies which suggest that the $1D$ stagger should be the predominant species within the fibril (Wallace, 1992). It is possible to explain these results in the framework of the DLA model. As explained previously, during growth of the aggregates new particles will preferentially accrete to the tips of other particles in the cluster. This will therefore lead to the production of a high number of staggers which have short overlaps (i.e. the $3D$ and $4D$ staggers). When surface diffusion is introduced into the model, although new rods will still preferentially accrete to the tips of other rods, the minimisation of surface area will cause these rods to migrate to sites that lead to the greatest contact with other rods. Hence in these simulations, the staggers with the most overlap (i.e. $0D$ and $1D$ staggers) will occur with a greater frequency. From the model we may conclude that during the initial stages of fibrillogenesis, there will be an abundance of $4D$ staggers (as observed in the electron micrographs). However, as the aggregates increase in size, so there is greater opportunity for the collagen molecules to minimise their surface area by increasing their contact with other collagen molecules. The entropic contributions will therefore lead to an increase in the number of $0D$ and $1D$ staggers.

# Conclusions

Here, we have investigated the structures of aggregates formed using an algorithm to simulate the aggregation of rod-like particles from solution via a diffusion/collision mechanism. Comparisons have then been made between these aggregates and collagen fibrils in an attempt to gain a deeper understanding of the processes controlling fibril morphology.

The results presented here show that the simulated and experimental systems share a number of features. All the simulations (run either with or without surface diffusion) had similar dimensions to collagen fibrils and showed linear mass per unit length profiles, irrespective of whether the fibrils generated were compacted or highly branched and open. Compact aggregates were only obtained when surface diffusion was included in the models. These data therefore suggest that much of the observed fibril morphology is simply a consequence of the aggregation of rod-like particles from solution. Specific collagen-collagen interactions do not appear to be important in determining fibril morphology. However, such interactions may be critical in the alignment of accreting molecules and to maintain stability in the fibril. The results from the simulations involving surface diffusion indicate that diffusion within fibrils is necessary for a dense compact morphology, and that mutations which affect the surface diffusion properties of collagen may seriously alter final fibril morphology.

Recently, Silver &amp; Miller (1994) have suggested a cellular automata model to describe collagen fibrillogenesis. In their model very specific growth rules were introduced to ensure that the morphology of the model matched the experimental data. Here, we have attempted to show that the growth process that occurs in collagen fibrillogenesis does not need such specific rules and that certain features can be explained by DLA. We believe that DLA is a useful tool in the investigation of protein aggregation and may be readily applied to phenomena such as microfibrils formed from fibronectin (Mosher, 1993). We are currently developing more sophisticated diffusion models to simulate the fluidity of collagen molecules within a fibril.

# Methods

The critical concentration of collagen for fibril formation in vitro is of the order $0.5\ \mu\mathrm{g/ml}$ (Kadler et al., 1987). At this concentration there are approximately $10^{12}$ collagen molecules/millilitre in solution. The collagen translational diffusion coefficient is $0.45\times 10^{-7}\ \mathrm{cm}^2/\mathrm{second}$ (Silver &amp; Trelstad, 1980) which means that an individual collagen molecule can move approximately $2\times 10^{-4}\ \mathrm{cm}$ in one second. Therefore, the volume around a growing fibril from which a mature collagen molecule could diffuse from within a second to attach to the aggregate is $(2\times 10^{-4})^3\ \mathrm{ml}$. If there are $10^{12}$ collagen molecules/ml then the total number of collagen molecules contained within this volume is approximately $8\ (= 10^{12}\times (2\times 10^{-4})^3)$, with the separation between collagen molecules being approximately $1.8\times 10^{-4}\ \mathrm{cm}$. Therefore at the critical collagen concentration, taking any part of the growing fibril, there will only be approximately eight collagen molecules close enough to the fibril surface to have a chance of colliding with it in any one second. These simple calculations suggest it is possible to think of fibril formation as a process in which isolated, independent, randomly diffusing collagen molecules collide with, and then stick to, the growing aggregate.

DLA has previously been used successfully to model processes such as electrochemical deposition and the shape of snowflakes (Matsushita et al., 1994; Nittman &amp; Stanley, 1987). In DLA a seed particle (nucleation) site is placed in the centre of a dilute 'virtual' solution of particles. Another particle is then placed at random a suitably large distance away from the nucleation site and allowed to undertake a random walk. If this particle collides with the nucleation site then it becomes part of the growing aggregate. This process is then repeated until an aggregate of the required size has been grown.

For computational simplicity most DLA simulations are performed on a lattice. The DLA process on a two-dimensional square lattice is illustrated in Figure 6. The lattice used to model fibrillogenesis was square in the plane horizontal to the growing aggregate and hexagonal in the perpendicular plane. This lattice geometry was chosen both for computational simplicity and because X-ray data suggests that collagen molecules can align

---

Simple Model of Collagen Fibrilogenesis
829

![img-12.jpeg](img-12.jpeg)
(a)

![img-13.jpeg](img-13.jpeg)
(b)
Figure 4. Graphs showing how the number of particles in a unit cross-section increases with distance from the tip: (a) aggregates grown using non-specific rules of binding, (b) aggregates grown using collagen-specific rules of binding. $(\diamondsuit)$, $T_{S} = 1$; $(\triangle)$, $T_{S} = 10,000$. Linear regression analysis indicates that the graphs have correlation coefficients in excess of 0.95. The gradients of the lines were found to be reproducible within the experimental fluctuations (e.g. for 5 independently generated structures with $T_{S} = 1$, gradients $= 1.20(\pm 0.08)\mathrm{mol} / D$).

in a quasi-hexagonal manner (Hulmes &amp; Miller, 1979). Collagen molecules were represented by rods that occupied 18 units $\times$ 1 unit $\times$ 1 unit on the lattice giving a $D$-period length of 4 and a rod length of $4.5D$-periods. During each step through the lattice, the row of occupied lattice sites that represented one collagen molecule moved as a single unit. In order to save computer processor time, and because collagen molecules are known to attach in parallel, the simulated collagen molecules were not allowed to rotate as they moved through the lattice.

Two different models were used in the simulations to describe the attachment of rods to the aggregate:

(1) Non-specific binding: rods adhered to the sides of other rods on first contact irrespective of whether or not the overlap was a $D$-period.
(2) Collagen specific binding: rods could only adhere if they overlapped by an integral $D$-period, i.e. by 0, 4, 8, 12 or 16 lattice units, representing 0-, 1-, 2-, 3- and 4-$D$ staggers, respectively.

By using these two binding models it was possible to determine, at least in part, the effect that some of the specific collagen-collagen interactions had on fibril morphology.

The DLA algorithm used in this study was very closely related to that used in two-dimensions. A rod was placed at the centre of the lattice and a second rod was placed at random at a distance of 200 lattice units from the surface of the first rod. The second rod began a random walk through the lattice until either: (1) it reached a distance of more than 400 lattice units from the first rod and was destroyed; (2) it encountered a suitable attachment site on the first rod (overlapping by an integer number of $D$-periods, see Figure 1) in which case it became part of the growing aggregate; (3) it encountered the seed rod, but in such a way that it did not overlap by an integer number of $D$-periods in which case it was reflected at random from the aggregate surface to continue the random walk until it either stuck or was destroyed. Note that for non-specific binding, rods would become part of the aggregate upon any contact with the aggregate surface.

---

Simple Model of Collagen Fibrilogenesis

![img-14.jpeg](img-14.jpeg)
Figure 5. Graph showing how the different types of stagger predominate when the time of surface diffusion $(T_{S})$ is increased. The bars indicate the percentage number of total bonds in aggregates composed of 10,000 particles. $\square$, $T_{S} = 1$; $\blacksquare$, $T_{S} = 10$; $\blacksquare$, $T_{S} = 100$; $\blacksquare$, $T_{S} = 1000$; $\blacksquare$, $T_{S} = 10,000$.

Another rod was then again placed at random at a distance of 200 lattice units from the surface of the growing aggregate and again started on a random walk until it was either destroyed or added to the aggregate. The process was repeated several thousand times to create aggregates composed of either 10,000 or 45,000 particles.

In some simulations surface diffusion was included using an algorithm in which particles attaching to the cluster were allowed a limited amount of time (defined as the surface diffusion time, $T_{S}$) to explore the surface of the aggregate to look for a more energetically favourable growth site (Garcia-Ruiz &amp; Otalora, 1991). A rod attaching to the surface of the growing aggregate underwent a further diffusion by moving laterally over the surface at random during the diffusion time, $T_{S}$ (equivalent to allowing a collagen molecule to roll across the surface of the aggregate at random). After $T_{S}$ trials (a trial being defined as a direction chosen at random whether or not it was rejected due to it allowing the rod to leave the aggregate surface) the rod was placed in the site that led

![img-15.jpeg](img-15.jpeg)
Figure 6. Theoretical model of diffusion limited aggregation on a 2-dimensional lattice. For an explanation see the text.

to the creation of the least amount of surface. If there were many such sites the rod was placed into the first of the minimum surface energy sites that it encountered.

The mass per unit length profile, dimensions, and density were recorded for every aggregate, as was a picture of the cross-section through the centre of the aggregate perpendicular to the long axis.

## Acknowledgements

J.P. is the recipient of a Wellcome Mathematical Biology Training Fellowship. K.E.K. is a recipient of a Senior Research Fellowship in Basic Biomedical Science with the Wellcome Trust (19512). We would like to thank Dr D. F. Holmes for many useful conversations.

## References

Butler, P. J. G. (1984). The current picture of the structure and assembly of tobacco mosaic virus. J. Gen. Virol. 65, 253-279.
Chapman, J. A. &amp; Hulmes, D. J. S. (1984). Electron microscopy of the collagen fibril. In Ultrastructure of the Connective Tissue Matrix (Ruggeri, A. &amp; Motta, P. M., eds), pp. 1-33, Martinus Nijhoff, Boston, The Hague, Dordrecht, Lancaster.
Dogterom, M. &amp; Leibler, S. (1993). Physical aspects of the growth and regulation of microtubule structures. Phys. Rev. Letters, 70, 1347-1350.
Fleischmajer, R., Perlish, J. S. &amp; Faraggiana, T. (1991). Rotary shadowing of collagen monomers, oligomers, and fibrils during tendon fibrillogenesis. J. Hist. Cytochem. 39, 51-58.
Fraser, R. D. B., Macrae, T. P. &amp; Miller, A. (1987). Molecular packing in type I collagen fibrils. J. Mol. Biol. 193, 115-125.
Frieden, C. (1985). Actin and tubulin polymerization: The use of kinetic methods to determine mechanism. Annu. Rev. Biophys. Biophys. Chem. 14, 189-210.
Garcia-Ruiz, J. M. &amp; Otalora, F. (1991). Diffusion limited aggregation. The role of surface diffusion. Physica A, 178, 415-420.

---

Simple Model of Collagen Fibrilogenesis

Holmes, D. F., Chapman, J. A., Prockop, D. J. &amp; Kadler, K. E. (1992). Growing tips of type I collagen fibrils formed *in vitro* are near-paraboloidal in shape, implying a reciprocal relationship between accretion and diameter. *Proc. Nat. Acad. Sci., U.S.A.* 89, 9855–9859.

Hulmes, D. J. S. &amp; Miller, A. (1979). Quasi-hexagonal molecular packing in collagen fibrils. *Nature (London)*, 282, 878–880.

Hulmes, D. J. S., Jesior, J.-C., Miller, A., Berthet-Colominas, C. &amp; Wolff, C. (1981). Electron microscopy shows periodic structure in collagen fibril cross sections. *Proc. Nat. Acad. Sci., U.S.A.* 78, 3567–3571.

Kadler, K. E. (1994). Extracellular matrix 1: Fibril-forming collagens. *Protein Profile*, 1, 519–638.

Kadler, K. E. &amp; Watson, R. B. (1995). Biochemistry of the procollagen C-peptidase. *Methods Enzymol*. In the press.

Kadler, K. E., Hojima, Y. &amp; Prockop, D. J. (1987). Assembly of collagen fibrils *de Novo* by cleavage of the type I pC-collagen with procollagen C-proteinase. *J. Biol. Chem.* 260, 15696–15701.

Kadler, K. E., Hojima, Y. &amp; Prockop, D. J. (1990). Collagen fibrils *in vitro* grow from pointed tips in the C- to N-terminal direction. *Biochem. J.* 268, 339–343.

Kadler, K. E., Lightfoot, S. J. &amp; Watson, R. B. (1995). Biochemistry of the procollagen N-peptidase. *Methods Enzymol*. In the press.

Katz, E. P. &amp; Li, S. T. (1973). The intermolecular space of reconstituted collagen fibrils. *J. Mol. Biol.* 73, 351–369.

Kielty, C. M., Hopkinson, I. &amp; Grant, M. E. (1993). The collagen family: structure, assembly, and organization in the extracellular matrix. In *Connective Tissue and its Heritable Disorders* (Royce, P. M. &amp; Steinmann, B., eds), pp. 103–147, Wiley-Liss, New York.

Matsushita, M., Sano, M., Hayakawa, Y., Honjo, H. &amp; Sawada, Y. (1984). Fractal structures of zinc metal leaves grown by electrodeposition. *Phys. Rev. Letters* 53, 286–289.

Meakin, P. (1988). The growth of fractal aggregates and their fractal measures. In *Phase Transitions and Critical Phenomena* (Domb, C. &amp; Lebowitz, J. L., eds), pp. 335–489, Academic Press, New York.

Miyahara, M., Njieha, F. K. &amp; Prockop, D. J. (1982). Formation of collagen fibrils *in vitro* by cleavage of procollagen with procollagen proteinases. *J. Biol. Chem.* 257, 8442–8448.

Mosher, D. F. (1993). Assembly of fibronectin into extracellular matrix. *Curr. Opin. Struct. Biol.* 3, 214–222.

Nittman, J. &amp; Stanley, H. E. (1987). Non-deterministic approach to anisotropic growth patterns with continuously tunable morphology: the fractal properties of some real snowflakes. *J. Phys. A.* 20, L1185–L1191.

Parkinson, J., Kadler, K. E. &amp; Brass, A. (1994). Self-assembly of rod-like particles in two dimensions: a simple model of collagen fibrillogenesis. *Phys. Rev. E*, 50, 2963–2966.

Parry, D. A. D. &amp; Craig, A. S. (1984). Growth and development of collagen fibrils in connective tissue. In *Ultrastructure of the Connective Tissue Matrix* (Ruggeri, A. &amp; Motta, P. M., eds), pp. 34–64, Martinus Nijhoff, Boston, The Hague, Dordrecht, Lancaster.

Prockop, D. J., Kivirikko, K. I., Tuderman, L. &amp; Guzman, N. A. (1979). The biosynthesis of collagen and its disorders. *New Eng. J. Med.* 301, 13–23.

Silver, D. &amp; Miller, J. (1994). Visualizing collagen fibril growth. *J. Mol. Graphics*, 12, 139–145.

Silver, F. H. &amp; Trelstad, R. L. (1980). Type I collagen in solution: structure and properties of fibril fragments. *J. Biol. Chem.* 255, 9427–9433.

Stanley, H. E. (1992). Fractal landscapes in physics and biology. *Physica A*, 186, 1–32.

Tomski, S. J. &amp; Murphy, R. R. (1992). Kinetics of aggregation of synthetic B-amyloid peptide. *Arch. Biochem. Biophys.* 294, 630–638.

Trotter, J. A., Thurmond, F. A. &amp; Koob, T. J. (1994). Molecular structure and functional morphology of echinoderm collagen fibrils. *Cell Tissue Res.* 275, 451–458.

Trus, B. L. &amp; Piez, K. A. (1980). Compressed microfibril models of the native collagen fibril. *Nature (London)*, 286, 300–301.

Veis, A., Anesey, J. &amp; Mussell, S. (1967). A limiting microfibril model for the three-dimensional arrangement within collagen fibres. *Nature (London)*, 215, 931–934.

Wallace, D. G. (1992). Early assembly pathways of type I collagen. *Biopolymers*, 32, 497–515.

Ward, N. P., Hulmes, D. J. S. &amp; Chapman, J. A. (1986). Collagen self-assembly *in vitro*: electron microscopy of initial aggregates formed during the lag phase. *J. Mol. Biol.* 190, 107–112.

Watson, R. B., Wallis, G. A., Holmes, D. F., Viljoen, D., Byers, P. &amp; Kadler, K. E. (1992). Ehlers Danlos syndrome type VIIB. *J. Biol. Chem.* 267, 9093–9100.

Witten, T. A. &amp; Sander, L. M. (1981). Diffusion-limited aggregation, a kinetic critical phenomenon. *Phys. Rev. Letters*, 47, 1400–1403.

Witten, T. A. &amp; Sander, L. M. (1983). Diffusion-limited aggregation. *Phys. Rev. B*, 27, 5686–5697.

Edited by F. E. Cohen

(Received 14 September 1994; accepted 18 January 1995)
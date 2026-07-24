# Issue #4 — Scientific support for the spatial avalanche definition

Date: 2026-07-23

## Question

Can the manuscript support, with primary literature, the following operational
definition?

> At each fixed force \(F\), molecules removed before the next force increment
> are partitioned into nearest-neighbor connected components; disconnected
> components at the same \(F\) are counted as separate avalanches.

The relevant distinction is between:

- **(a)** all failures during a load-holding/relaxation interval;
- **(b)** a spatially connected component;
- **(c)** a spatiotemporal cluster; and
- **(d)** another system-specific definition.

## Conclusion

An additional citation can help, but it should not be presented as proving that
spatial connectedness is the universal definition of an avalanche. The
strongest primary literature distinguishes a **global avalanche** from its
spatially connected **local avalanches (or clusters)**.

The manuscript's statistic is therefore defensible as an operational
distribution of **local avalanche clusters**. The safest wording is to say
explicitly that disconnected components are counted separately and that this
classification does not by itself establish causal nearest-neighbor stress or
energy transfer.

This matters because standard random-fuse and fiber-bundle papers usually use
definition (a), while crack-front experiments and models also analyze
definition (b). Both conventions exist.

## Best primary sources

### 1. Laurson, Santucci, and Zapperi (2010): best conceptual match

L. Laurson, S. Santucci, and S. Zapperi, “Avalanches and clusters in planar
crack front propagation,” *Physical Review E* **81**, 046116 (2010).
[Publisher DOI](https://doi.org/10.1103/PhysRevE.81.046116);
[author preprint](https://arxiv.org/abs/0911.2380).

**Classification: (d), with an explicit two-level distinction.**

- The global avalanche is the complete response triggered before the external
  drive resumes.
- That avalanche can contain several spatially disconnected components because
  of long-range interactions.
- The connected components are analyzed separately as “local avalanches (or
  clusters).”

This is the closest support for the manuscript's decision to avoid combining
distant components in the same size distribution. It supports the term
**local avalanche** or **avalanche cluster**, not the stronger claim that each
component is necessarily a separate causal cascade.

**Terminological risk:** citing this paper while using only “avalanche” could
strengthen the Referee's alternative interpretation, because the paper calls
the full relaxation the global avalanche and the connected pieces local
clusters.

### 2. Måløy et al. (2006): experimental use of connected avalanche clusters

K. J. Måløy, S. Santucci, J. Schmittbuhl, and R. Toussaint, “Local waiting time
fluctuations along a randomly pinned crack front,” *Physical Review Letters*
**96**, 045501 (2006).
[Publisher DOI](https://doi.org/10.1103/PhysRevLett.96.045501);
[author preprint](https://arxiv.org/abs/cond-mat/0512532).

**Classification: (b).**

The authors construct a local waiting-time/velocity map for a propagating crack
front, threshold the high-velocity activity, and extract connected regions.
The areas of those regions are analyzed as burst or avalanche-cluster sizes.
This is primary experimental evidence that spatially connected clusters are a
legitimate operational observable in fracture.

**Scope limitation:** this experiment does not collect discrete molecular
failures at a prescribed \(F\). It detects connected high-velocity regions in a
space-resolved crack-front trajectory. It is an analogous measurement
procedure, not a validation of the collagen model's dynamics.

### 3. Picallo and López (2008): clear counterexample from the random-fuse model

C. B. Picallo and J. M. López, “Energy dissipation statistics in the random
fuse model,” *Physical Review E* **77**, 046114 (2008).
[Publisher DOI](https://doi.org/10.1103/PhysRevE.77.046114);
[author preprint](https://arxiv.org/abs/0804.2321).

**Classification: (a).**

The authors define an avalanche as all fuses that burn between two consecutive
external voltage/current increments. Spatial connectedness is not required.
This is a useful counterexample: it confirms that the Referee's proposed
load-step definition is standard in part of the fracture literature, so the
response should describe the manuscript's connected-component definition as a
deliberate local observable rather than the uniquely correct convention.

## Audit of references already used in the manuscript

| Reference | Definition used | Relevance to the present choice |
|---|---|---|
| Zapperi et al., PRL 78, 1408 (1997), [DOI](https://doi.org/10.1103/PhysRevLett.78.1408) | **(a)**: failures triggered while the external current is held during redistribution. The authors explicitly report that avalanches need not be spatially connected. | Does not support identifying every connected component as a global avalanche. It supports distinguishing event size from crack geometry. |
| Zapperi et al., PRE 59, 5049 (1999), [DOI](https://doi.org/10.1103/PhysRevE.59.5049) | **(a)** for avalanches; **(b)** is analyzed separately as clusters of neighboring broken bonds. | Particularly important: the paper explicitly states that avalanche size counts bonds breaking at a step, whereas connected-bond cluster size characterizes crack geometry. |
| Zapperi, Vespignani, and Stanley, Nature 388, 658 (1997), [DOI](https://doi.org/10.1038/41737) | **(a)**: number of bonds damaged for a voltage increment. | Does not supply the connected-component definition. |
| Hemmer and Hansen, J. Appl. Mech. 59, 909 (1992), [DOI](https://doi.org/10.1115/1.2894060) | **(a)**: simultaneous/triggered fiber failures during redistribution. | Classical fiber-bundle usage favors the Referee's temporal/load-step convention. |
| Hansen and Hemmer, Phys. Lett. A 184, 394 (1994), [DOI](https://doi.org/10.1016/0375-9601(94)90511-8) | **(a)**: burst generated by load redistribution. | Local load sharing can create spatially localized damage, but the avalanche is defined dynamically, not by post hoc connected components alone. |
| Suki et al., Nature 368, 615 (1994), [DOI](https://doi.org/10.1038/368615a0); Barabási et al., PRL 76, 2192 (1996), [DOI](https://doi.org/10.1103/PhysRevLett.76.2192); Alencar et al., PRL 87, 088101 (2001), [DOI](https://doi.org/10.1103/PhysRevLett.87.088101) | **(d)**: a trigger opens a cascade of accessible downstream branches in a connected airway tree. | Supports Professor Suki's causal picture of a neighbor-connected cascade, but the airway topology and triggering rule make the cascade connected by construction. It is not a direct justification for inferring causality from collagen-cluster adjacency. |
| Beggs and Plenz, J. Neurosci. 23, 11167 (2003), [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC6741045/) | **(c)**: consecutive active time bins bounded by blank bins, across the electrode array; nearest-neighbor spatial continuity is not required. | Shows that “avalanche” can be a spatiotemporal operational grouping and need not be a connected spatial component. |
| Jaeger and Nagel, Science 255, 1523 (1992), [DOI](https://doi.org/10.1126/science.255.5051.1523) | **(d)**: a triggered cascade of grain motion/toppling. | Broad conceptual precedent only; it does not establish the manuscript's data-partition rule. |
| Godano, Alonzo, and Caruso, Phys. Earth Planet. Inter. 80, 199 (1993), [DOI](https://doi.org/10.1016/0031-9201(93)90042-8) | **(d)**: seismic events and their temporal clustering. | Not support for a nearest-neighbor connected-component definition. |

The references currently following the avalanche-definition sentence in
`Paper/paper_PRE.tex` are therefore broad examples of avalanche phenomena, not
direct support for the exact data-partition rule. Laurson et al. and, optionally,
Måløy et al. would be more targeted citations.

## Interpretation of Professor Suki's pre-submission comment

Professor Suki's concern is scientifically reasonable: two distant damage
regions at the same \(F\) need not be a single local cascade. Literature on
crack fronts explicitly distinguishes a global event from disconnected local
clusters, so separating the clusters is an established analysis choice.

The stronger proposed explanation—an avalanche is necessarily a contiguous
chain produced by energy transfer among neighbors—requires a local triggering
or load-redistribution mechanism. The collagen model's nearest-neighbor
connectivity criterion alone does not demonstrate that causality. Therefore,
the manuscript should defend the statistic as a **local, operational
classification of damage**, not as direct evidence of energy transfer between
neighboring molecules.

## Recommended short wording for Methods

> At each fixed force level \(F\), all molecules removed before the next force
> increment are partitioned into nearest-neighbor connected components. We
> refer to each component as a local avalanche (or avalanche cluster) of size
> \(s\); disconnected components are counted separately
> \cite{Laurson2010,Maloy2006}.

If the authors do not want to add two citations, Laurson et al. is the more
important one because it states the global/local distinction directly.

## Recommended short response to R2-3

> We thank the Referee for noting that avalanche definitions are not unique.
> Our statistic corresponds to local avalanche clusters rather than to the
> global load-step avalanche commonly used in fiber-bundle and random-fuse
> models. At each fixed \(F\), we partition the removed molecules into
> nearest-neighbor connected components and count disconnected components
> separately, so spatially distant damage regions are not merged solely because
> they occurred at the same force level. This global-avalanche/local-cluster
> distinction is also used in crack-front studies [Laurson et al., Phys. Rev. E
> 81, 046116 (2010)]. We have clarified that this is an operational
> classification of local damage and does not, by itself, imply a localized
> stress-redistribution kernel.

## Recommendation

Use **local avalanche** or **avalanche cluster** consistently in the definition,
figure captions, and \(P(s)\) discussion. Cite Laurson et al. near the
definition. Måløy et al. is useful optional experimental support.

Do not claim that the citation proves neighbor-to-neighbor energy transfer in
this model. Also do not cite Zapperi (1997/1999), the classical fiber-bundle
papers, or Beggs and Plenz as if they used the same connected-component
definition; they use alternative event partitions.

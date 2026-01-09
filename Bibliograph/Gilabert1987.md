HAL

open science

# The random fuse network as a model of rupture in a disordered medium

A. Gilabert, C. Vanneste, D. Sornette, E. Guyon

## To cite this version:

A. Gilabert, C. Vanneste, D. Sornette, E. Guyon. The random fuse network as a model of rupture in a disordered medium. Journal de Physique, 1987, 48 (5), pp.763-770. 10.1051/jphys:01987004805076300. jpa-00210496

HAL Id: jpa-00210496

https://hal.science/jpa-00210496v1

Submitted on 4 Feb 2008

HAL is a multi-disciplinary open access archive for the deposit and dissemination of scientific research documents, whether they are published or not. The documents may come from teaching and research institutions in France or abroad, or from public or private research centers.

L'archive ouverte pluridisciplinaire HAL, est destinée au dépôt et à la diffusion de documents scientifiques de niveau recherche, publiés ou non, émanant des établissements d'enseignement et de recherche français ou étrangers, des laboratoires publics ou privés.

---

J. Physique 48 (1987) 763-770

MAI 1987, PAGE 763

Classification

Physics Abstracts

62.20M — 64.60 — 02.50

# The random fuse network as a model of rupture in a disordered medium

A. Gilabert, C. Vanneste, D. Sornette and E. Guyon (*)

Laboratoire de Physique de la Matière Condensée, UA190,

Parc Valrose, 06034 Nice Cedex, France

(*) E.S.P.C.I., UA857, 10, rue Vauquelin, 75231 Paris Cedex 05, France

(Reçu le 16 septembre 1986, révisé le 4 décembre, accepté le 9 janvier 1987)

Résumé. — Des simulations numériques et des résultats expérimentaux obtenus sur un réseau discret de fusibles sont présentés pour illustrer le problème de rupture d'un milieu désordonné sous contrainte. La distribution des courants et le courant maximum en fonction de la densité de défauts dans le réseau sont comparés avec les estimations théoriques. Les interactions entre défauts et, en particulier, les effets de renforcement et d'écrantage sont mis en valeur. L'analogie entre les problèmes de rupture dans un réseau aléatoire de résistances et un système mécanique est discutée.

Abstract. — The rupture problem in a disordered system is investigated through numerical simulations and experiments in a discrete fusewire network. Statistical results on the current distribution and the maximum current as a function of the density of defects in the network are compared with theoretical interpretations. Specific defect interactions (enhancement and screening effects) are emphasized. We discuss the analogies for the rupture problem between resistor networks and mechanical systems.

# 1. Introduction.

Failure in stressed disordered systems is of large importance in science and technology and has received a considerable attention recently [1]. Classical examples of such systems are for instance the mechanical failure in elastic networks or the electric breakdown in resistor networks. Previous studies have considered different systems and have focused on various aspects of this problem: the scaling laws describing the breakdown of a fusewire network near the percolation threshold [2], the fracture and plasticity of an elastic network near the rigidity threshold [3], the breakdown strength in a fusewire or dielectric network [4], the fractal structure of the percolation cluster in the dielectric breakdown of a resistor network [5], the dependence of the pattern of failure on the distribution function of inhomogeneities in a random network of Hooke-type springs [6], etc.

We focus in this paper on an electrical model initially introduced by de Arcangelis et al. [2], which consists of resistive fuses and insulators randomly located on each bond of a lattice. An external current is applied to this electrical network. The scalar nature of the problem enables us to develop

simple pictures and concepts which, hopefully, can be translated to the more complicated case of vector or tensor fields involved in mechanical failure. The distribution of currents and, especially, the maximum current in the bonds of the network are first numerically studied as a function of the initial density $q$ of insulators. These statistical results are compared with theoretical estimates, but with no claim for a reference to a complete theory. In fact, the theory of ruptures is difficult due to the complex interplay between statistical and local properties of the system. Therefore, the following sections are devoted to the illustration of particular configurations: influence of the size of defects, interactions between them and examples of fractures. Local configurations leading either to the amplification or to the screening of the external stress are especially considered. These results will be illustrated not only by numerical simulations but by experiments on a discrete resistor network and on a continuous system consisting of sheets of colloidal graphite paper.

All along this work, the analogy between electrical and mechanical systems will be emphasized. Loosely speaking, the voltage (current) distribution in an electrical network can be compared to the strain

Article published online by EDP Sciences and available at http://dx.doi.org/10.1051/jphys:01987004805076300

---

JOURNAL DE PHYSIQUE
N° 5

(stress) distribution in a random elastic medium. Actually, this analogy is even exact with two-dimensional systems where isolated defects are submitted to antiplanar deformations [7]. In the following, we will use indiscriminately the mechanical language in the context of electrical breakdown.

## 2. General features.

On each bond of a lattice we place a fuse with probability $p$ and an insulator with probability $q = 1 - p$ (Fig. 1a). A fuse is a non-linear device depicted in figure 1b. When the current is less than a critical value $I_{\mathrm{c}}$, the fuse has a constant finite resistance. If the current exceeds $I_{\mathrm{c}}$, the fuse burns out and breaks irreversibly into an insulator. In the following, all the fuses are identical.

If the total current in the network is $I_{\mathrm{t}}$ and $m$ is the number of parallel columns, the current per bond in

![img-0.jpeg](img-0.jpeg)
a

![img-1.jpeg](img-1.jpeg)
b
Fig. 1. — (a) Random resistor network (external total current $I_{\mathrm{t}}$) with a probability $p$ of having a fuse of resistance $R$ (dark lines) and $q = 1 - p$ of having an insulator (dotted lines). (b) Non linear current-voltage characteristic of a fuse.

an intact network at $p = 1$ is $I_0 = I_t / m$. We will use this normalized value $I_0$ in order to obtain intrinsic quantities. When the network is initially flawed, the vacant bonds are the cause of the inhomogeneous distribution of voltages and currents, which in turn controls the damage process.

We have performed numerical simulations on such electrical networks of 696 or 2850 resistances with periodic boundary conditions in the transverse direction. The voltages at each node of the network were calculated by the Gauss-Seidel relaxation method. When studying particular configurations, it was convenient to make measurements on an actual electrical resistor network made of 696 resistances of $1\mathrm{k}\Omega$ distributed on a square lattice and biased by a total current $I_{\mathrm{t}} = 10\mathrm{mA}$. Some measurements were also performed on a continuous conducting sheet of colloidal graphite paper punched with $3\mathrm{mm}$ diameter holes.

## 3. Distribution of currents in the random resistor network.

In this section, we consider the resistor network previously defined, biased by a constant total current. The current distribution and the maximum current have been numerically calculated as a function of the density $q = 1 - p$ of insulating bonds (defects or elementary cracks). Figure 2 displays the stability diagram of a 2850 resistor network in the $(q, I_{\mathrm{c}} / I_0)$ plane. The maximum current $I_{\mathrm{m}}$ as a function of $q$ is represented by a continuous curve. For each value of $q$, this curve has been obtained by averaging $I_{\mathrm{m}}$ over 210 different configurations. If the fuse critical current $I_{\mathrm{c}}$ is larger than $I_{\mathrm{m}}$, the network will stay in the initial flawed configuration. In the other case $(I_{\mathrm{c}} \ll I_{\mathrm{m}})$, at least one bond will first burn out and will be likely to induce the propagation of a fracture. Hence, the $I_{\mathrm{m}}$-versus-$q$ curve separates the initially flawed regime (right region) from the damaged regime (left region) in which fuses begin to burn out. Once started, the fracture can develop or not through the entire network, depending on the initial concentration and the configuration of the missing bonds. In the following, we will just focus on the current necessary for breaking the first bond which often coincides with the current for breaking the entire network [8]. It is worth noticing that the curve $I_{\mathrm{m}}(q)$ is the electrical analog of the fracture stress as a function of the concentration of missing bonds which has been recently studied in a solid network [9].

In the same figure 2 are reported the histograms depicting the current distribution $n(I)$, i.e. the number of resistances supporting a given current $I$ as a function of $I$. As one goes to more and more initially flawed systems ($q$ increases), the current distribution broadens in a very typical non-Gaussian

---

N° 5
RUPTURE IN A DISORDERED MEDIUM
765

![img-2.jpeg](img-2.jpeg)
Fig. 2. — Numerical simulation of the stability diagram of a 2850 resistor network. $I_{\mathrm{c}}$, $I_{0}$ and $q = 1 - p$ are respectively the critical current of a fuse, the current per bond in the uniform network without defects and the concentration of missing links. The maximum current $I_{\mathrm{m}}$ (normalized to $I_{0}$) as a function of $q$ is represented by a continuous curve which has been obtained by averaging $I_{\mathrm{m}}$ over 210 different configurations of the network. The approximate location of the four regions discussed in the text is indicated along the curve (I, II, III and IV). $i_{\mathrm{s}} = 1.36$ indicates the starting value of the maximum current $I_{\mathrm{m}} / I_{0}$ when the first monomer defect appears in the network. Histograms of the current distribution are displayed for some values of $q_{\mathrm{r}}^{\prime}$ a) $q \approx 0.014$, b) $q \approx 0.070$, c) $q \approx 0.126$ and d) $q \approx 0.281$.

way which has been recently studied in reference [10] near the percolation threshold, while the peak at zero current (not displayed in the figure) increases, indicating that more and more of the present links do not support any current. Most of them correspond to « dead arms ».

In the following, those numerical results are discussed within the frame of theoretical descriptions in order to gain insight on the physical processes which explain the $I_{\mathrm{m}}$-versus-$q$ curve. This curve can be roughly divided in four regions indicated in figure 2. The first region concerns the $q \to 0$ limit where only isolated monomer defects are present in the network. It starts at a value $I_{\mathrm{m}} / I_0 = 1.36$ as explained in section 3.1. When $q$ increases, defects begin interacting and larger defects or clusters appear. The corresponding domain of the curve

$I_{\mathrm{m}}(q)$ (region II) will be compared with a recent theoretical explanation [4], which takes simultaneously account of the more or less hazardous nature of those defects and of their probability of presence in a given flawed network. When $q$ keeps increasing (region III), the interactions between defects give rise to complicated cooperative effects. A detailed analysis of this regime does not exist yet. However, the influence of other defects on a given one will be illustrated by specific examples in section 4. The last section of the curve (region IV) corresponds to the $q \rightarrow q_{\mathrm{c}}$ regime near the percolation threshold where the theoretical description utilizes scaling arguments.

3.1 MONOMER DEFECTS (REGION I). — The extreme limit $q = 0$ is easily understood. For $q = 0$, $(I_{\mathrm{m}} / I_0)(q) = 1$. The network being intact, the system breaks down as soon as $I_{\mathrm{c}}$ is smaller than $I_0$. At very low defect concentration ($q \ll 1$), the current distribution $n(I)$ displays lateral peaks on each side of the main peak centered at the initial value $I_0$. The main peak itself decreases and broadens. These lateral peaks correspond to the excess currents flowing through the bonds at the perimeter of isolated defects. Such a current distribution can be considered as the signature of the low defect concentration regime where there are only monomer defects which do not interact. In this case, a missing bond is equivalent to an extra dipole source in the perfect network, such that the net current in this bond is zero. Hence, the value of the current in a bond can be considered as the sum of the initial current $I_0$ plus the contribution $I_1$ due to the effective dipoles created by the defects. The computation can be made exactly for the case of a single bond using the Thevenin theorem [4, 11]. Figure 3 shows the current map created by such a simple defect as determined experimentally on an actual electrical network. In particular, this current map shows that as soon as a monomer defect appears in the network, the maximum current $I_{\mathrm{m}} / I_0$ jumps from the value $I_{\mathrm{m}} / I_0 = 1$ at $q = 0$ to the value $I_{\mathrm{m}} / I_0 = i_{\mathrm{b}}$ indicated in figure 2. The value of $i_{\mathrm{b}}$ depends on the network: $i_{\mathrm{b}} = 4 / \pi$ for the network considered in [2] and [4] where the bonds are positioned parallel and perpendicular to the network boundaries while $i_{\mathrm{b}} = 1.36$ for our network depicted in figure 1.

The effect of a defect (via its effective dipole) extends to rather large distances. Let us consider the contribution $I_{1}$ due to one defect located at the distance $r$ (normalized to the bond length) from the bond we look at. In the continuum limit, the distribution of voltages $V$ obeys the Laplace equation $\Delta V = 0$ with appropriate boundary conditions (the current entering the defect is zero and the current is uniform at large $r$). In 2D geometry, the potential

JOURNAL DE PHYSIQUE. — T. 48, N° 5, MAI 1987
50

---

766
JOURNAL DE PHYSIQUE
N° 5

![img-3.jpeg](img-3.jpeg)
Fig. 3. — Current distribution around an isolated defect measured in an experimental 696 resistor network. Current values are given by their difference in percentage with the current $I_0$ per bond in the uniform network without defects.

created by a dipole is proportional to $r^{-1}$, i.e. $I_{1} \propto \nabla V \propto r^{-2}$. An experimental illustration of this law is given in figure 4 where the evolution of the voltage measured near a circular hole punched in a conducting sheet of paper is plotted as a function of the distance from an other hole. This law is also verified in the discrete case. This situation is similar to the mechanical case where local stresses decay over long distances.

Such a long range effect of missing bonds in the network indicates that interactions between defects have to be generally considered except at $q \approx 0$.

## 3.2 THE ONSET OF INTERACTIONS BETWEEN DEFECTS (REGION II).

After considering single bond defects, it is natural to expect, when $q$ starts increasing, that some defects are close enough to interact and that finite clusters of missing bonds are present even at rather low $q$. Let us use the result of [4] where it is stated that the maximum disturbance in the current distribution is created by long thin defects oriented perpendicular to the average current flow. By solving the Laplace equation, the current $I_{\mathrm{tip}}$ on the bond just situated at the tip of a defect is given by the relation:

$$
I_{\mathrm{tip}} = I_{0}(1 + b n) \tag{1}
$$

where $n$ is the length of the defect and $b$ is a constant which depends on the lattice structure. Then, looking for the largest defect that is likely to occur in a network of size $m$, yields [4]

$$
n_{\max} \propto - \operatorname{Log}(m) / \operatorname{Log}(1 - p). \tag{2}
$$

![img-4.jpeg](img-4.jpeg)
Fig. 4. — Linear dependence of the measured voltage at the tip of a hole as a function of $r^{-2}$, where $r$ is the distance from a second hole (continuum limit represent by stars). The experiment was performed on graphite paper. The same curve for an experimental resistor network (discrete case represented by squares) is represented by a dotted line. Note also the good agreement with the $r^{-2}$ law except for very small distances $r$ ($r$ of the order of one bond length) due to discrete effects. The experimental scheme is shown in the insert.

Hence, assuming $I_{\mathrm{m}} = I_{\mathrm{tip}}$ when such a defect is present, yields by using (1):

$$
(I_{\mathrm{m}} / I_{0})(q) - 1 \propto - \operatorname{Log}(m) / \operatorname{Log}(q) \tag{3}
$$

valid at least in the low $q$ regime. Equation (3) corresponds to equation (1) of [4] but is written in our case for a current-biased instead of a voltage-biased network. In [4], the authors have verified the dependence of the breakdown voltage on the logarithm of the network size $m$. We focus here on the relation $I_{\mathrm{m}}(q)$ predicted by equation (3). Figure 5 shows that, at low $q$ (region II), the numerical results actually follow the linear dependence of $(I_{\mathrm{m}} / I_0 - 1)$ versus $(\operatorname{Log}(q))^{-1}$. However, the study of the current map in a rather large number of different flawed networks, reveals that if the hottest bond is sometimes associated with the tips of large defects, it corresponds very often to local interactions between small defects. Hence, notwithstanding the correct description of the maximum current as a function of $q$ by equation (3), further theoretical work is needed to understand its foundation. It is worth noticing that the same arguments can be adapted to the mechanical context in the case where

---

N° 5
RUPTURE IN A DISORDERED MEDIUM
767

![img-5.jpeg](img-5.jpeg)
Fig. 5. — Linear dependence of  $-\left(\ln q\right)^{-1}$  versus  $(I_{\mathrm{m}} / I_0 - 1)$  as predicted by equation (3). The data are the same as in figure 2. The numbers I, II and III indicate the different regions discussed in the text.

a brittle heterogeneous material like concrete is modelized by randomly distributed microcracks.

As already pointed out, such a result should only be valid in the low  $q$  regime (region II in Figs. 2 and 5). At larger  $q$ , interactions give rise to complicated cooperative effects. Therefore, when  $q$  increases, a change of regime is to be expected and is actually observed at  $q \approx 0.1$  in figure 5. However, in this regime (region III), a theoretical description is not available yet. Nevertheless other theoretical arguments can be used to obtain the  $I_{\mathrm{m}}$ -versus-  $q$  dependence near the percolation threshold (region IV).

3.3 THE  $q \to q_{\mathrm{c}}$  REGIME (REGION IV). — Due to strong finite size effects in the networks we have considered, we have not investigated this regime through numerical simulations or experiments. In particular, the maximum current in a bond saturates to the total applied current  $I_{\mathrm{t}} = mI_{0}$  near  $q_{\mathrm{c}}$ . Nevertheless, theoretical predictions can be made by using scaling arguments.

For  $q \approx q_{\mathrm{c}} = 1 - p_{\mathrm{c}}$ , the system is strongly flawed and the individual fuses must be very strong (large  $I_{\mathrm{c}}$ ) in order to sustain the applied current. We expect the power law

$$
\left(I _ {\mathrm {m}} / I _ {0}\right) (q) \propto \left| q - q _ {\mathrm {c}} \right| ^ {- (d - 1) v} \tag {4}
$$

where  $\upsilon$  is the critical exponent for the percolation correlation length  $\xi$  and  $d$  is the space dimension ( $d = 2$  in our simulations). This result can be com

pared with the critical current density  $j_{\mathrm{c}}$  in a superconductor-insulator composite when the volume fraction  $p$  of the superconducting component approaches the percolation threshold  $p_{\mathrm{c}}$  [12]:

$$
j _ {\mathrm {c}} \propto (p - p _ {\mathrm {c}}) ^ {(d - 1) v}
$$

where  $j_{\mathrm{c}}$  is equivalent to  $(I_{\mathrm{m}} / I_0)^{-1}$

In both cases, the intuitive idea is that near the percolation threshold, the current is carried by single channels of a superlattice with a mesh (or lattice size)  $\xi$  [13]. The current in such a channel is equal to the sum of the currents which should have been carried by the other missing bonds within the distance  $\xi$  from the channel and is therefore proportional to  $\xi^{(d - 1)}\propto |q - q_{\mathrm{c}}|^{-(d - 1)v}$ . Although the single channel picture is a poor representation of the percolation backbone for small values of  $d(d &lt; 6)$ , the expression for  $(I_{\mathrm{m}} / I_0)(q)$  remains valid since it has been verified numerically [14] that the backbone has at least one « bottleneck », i.e. a low-connectivity bond per length  $\xi$ .

Equation (4) is equivalent to equation (2) given in [4] except that the conductivity exponent  $t$  does not appear in our case as we have considered a current biased network. It is worth noticing that the exponent given in equation (4) is different from the equivalent exponent announced by D. Bergman [3] for a 2-D elastic network submitted to a mechanical stress. The origin of this difference lays in subtle arguments considering the essential part played by the torques acting on the bonds near the rupture of a mechanical network [15].

# 4. Interactions between defects : shielding and amplification effects (region III).

We now examine some specific interactions between defects by considering the problem of a large crack interacting with isolated defects. The choice of this particular problem is justified if one considers for example the simulations of Redner on a random fuse network [16]. It is shown that in a first stage, the damage develops by creation of (nearly) independent local defects. In a second stage a large crack develops and propagates across the lattice of already present structures. To be more specific, we will show out of a few configurations that, depending on their location, local defects can enhance or shield the propagation of a large crack. The shielding effect is well known in continuous mechanics where it is a practical procedure to stop the propagation of a crack by adding a hole at the location of the crack tip. We model these interaction problems by using again the random fuse network.

Let us first consider how the relative distribution of defects affects the maximum current at the tip of a macrocrack. Figures 6 and 7 consider two basic configurations where the gap separating two defects

---

768 JOURNAL DE PHYSIQUE N° 5

![img-6.jpeg](img-6.jpeg)
Fig. 6. — Experimental determination of the current $I_{\mathrm{tip}}$ at the tip (represented as a dotted resistor) of a 10 defect horizontal row in a resistor network versus the distance $d$ along the $x$ axis of a small defect made of three missing resistances ($I_{\mathrm{tip}}$ has been chosen in such a way that $I_{\mathrm{tip}} = 1$ for $d$ infinite). The theoretical curves of Kachanov et al. [17], which represent the stress intensity factor at the main crack tip versus the distance of the collinear microcrack, are displayed in the inserts.

![img-7.jpeg](img-7.jpeg)
Fig. 8. — Same as figure 6 but for a pair of defects displaced along the $x$ axis at a different $y$ position.

![img-8.jpeg](img-8.jpeg)
Fig. 7. — Same as in figure 6 but for a pair of defects displaced along the $y$ axis.

is perpendicular or parallel to the flux of current. The current $I_{\mathrm{tip}}$ measured at the tip of a macrocrack (ten missing bonds) in an experimental 696 resistor network is plotted versus the distance of a microcrack (three missing bonds). In figure 6, $I_{\mathrm{tip}}$ increases when the distance between the two cracks decreases along the $x$ axis (enhancement effect). On the contrary, in figure 7, $I_{\mathrm{tip}}$ decreases when their distance decreases along the $y$ axis (shielding effect). A more general case is shown in figure 8 where both enhancement and shielding effects are observed when the microcrack is shifted away from the macrocrack along the $y$ axis and its distance varies along the $x$ axis.

![img-9.jpeg](img-9.jpeg)

Those experimental results can be compared with the calculations of interactions between cracks in a solid performed by M. Kachanov and E. Montagut [17]. Considering the modification of the stress field on one fracture due to the stress field induced by another one, they have shown that the interaction of a crack with microcracks in a solid can significantly alter the stress concentration at the crack tip. Their results are shown in the inserts in figures 6, 7 and 8. They display the variation of the stress intensity factor in a brittle material at the tip of a large crack as a function of the position of another crack or of a pair of cracks. The observed behaviours (enhance

---

N° 5

RUPTURE IN A DISORDERED MEDIUM

ment and shielding effects) are in direct correspondence with the results obtained on the electrical network. The very similar results obtained with both elastic and resistor networks indicate that to some extent, qualitative transposition of mechanical problems into electrical problems can be made.

The preceding examples show clearly that the weakest point in a system is not always determined by the largest defect but depends also on shielding or enhancement effects which are to be expected when the defect concentration $q$ increases. Such interactions between defects will be essential to the way a solid disrupts and to the dynamics of rupture. Let us consider in the following, the breaking process introduced by de Arcangelis et al. [2] where at each step of the rupture sequence, the hottest bond is removed, the voltages at the nodes of the network are recalculated and the same process repeated again until a conducting path does not longer exist in the network. A first example of rupture in a 696 resistor experimental network is given in figure 9. In figure 9a, the fracture line develops between two macrocracks representing an initially flawed network. The addition in figure 9b of a pair of microcracks screens the bonds between the two macrocracks and favors the development of a fracture in an other area of the network.

![img-10.jpeg](img-10.jpeg)

![img-11.jpeg](img-11.jpeg)
Fig. 9. — Rupture process between two cracks in an experimental 696 resistor network. The figure gives the first five broken bonds in an initially flawed lattice where a few bonds (continuous lines) have been initially removed. The addition in figure 9b of two cracks screens the propagation at the left tip of the longest crack and favors that to the right.

A less academic and more general flawed situation is shown in figure 10, where the rupture patterns of a 696 resistor numerical network with $q \approx 0.13$ have been calculated according to the same breaking process. Figures 10a and 10b correspond to the same initially flawed network besides a cluster of four resistances which is missing in figure 10a (represented by four stars) and which is present in figure 10b. The chronological sequence of the rupture in both examples has been indicated by increasing integers. Except for the first bond burnt, the rupture sequences are different in the two figures. Actually, the second burnt bond in figure 10b from which the fracture propagates through the entire network becomes screened in figure 10a by the defect created by the absence of the four resistance cluster. It follows in figure 10a that the second bond burns in a completely different place and gives rise to a different fracture pattern.

![img-12.jpeg](img-12.jpeg)

![img-13.jpeg](img-13.jpeg)
Fig. 10. — Rupture process of a numerical random resistor network having an initial concentration of missing links $q \approx 0.135$. The only difference between a) and b) is due to a cluster of four bonds which are present in 10b and are missing in 10a (represented by four stars). The numbers indicate the chronological sequence of rupture of the successive hottest links.

## 5. Conclusion.

The goal of this paper has been to study and illustrate by numerical simulations but also by experiments in a random resistor network, some basic concepts which could be useful for the construction of a comprehensive and general theory of breakdown

---

770
JOURNAL DE PHYSIQUE
N° 5

phenomena in a disordered medium. The maximum current in a flawed network has been first studied as a function the density of defects. For a weakly flawed network, numerical simulations are in agreement with theoretical predictions where defects can be considered as locally interacting, even though the origin of this agreement needs further investigation. On the other hand, the theory predicts that the breakdown of a strongly flawed network near the percolation threshold is governed by a few conducting channels in a superlattice with a mesh $\xi$ where $\xi$ is the coherence length. For intermediate densities of defects, a detailed theory taking account of complicated interactions between defects is still missing.

The importance of such interactions has been emphasized by giving examples of defect configurations where enhancement or screening effects significantly modify the fracture propagation in the random resistor network. Such effects have been shown to be similar to the interaction of cracks previously predicted in solids.

Many problems concerning the breakdown of a disordered system remain to be studied. This work has considered the simple fuse model which can be compared with an elastic medium. It would also be interesting to develop electrical models to describe very ductile materials. The dynamics of the rupture has not been explored either. This is of upmost importance in many applications. We plan to investigate this aspect in future studies.

## Acknowledgments.

One of us (E. G.) would like to thank S. Redner and S. Roux for fruitful discussions.

## References

[1] See « Fragmentation, form and flow in fractured media », Proceedings of the F³-Conference (Neve Ilan, 1986), in Ann. Isr. Soc. 8 (1986), and references cited therein.

[2] DE ARCANGELIS, L., REDNER, S. and HERRMANN, H., J. Phys. Lett. 46 (1985) L585.

[3] BERGMAN, D. J., reference [1], p. 266.

[4] DUXBURY, P. M., BEALE, P. D. and LEATH, P. L., Phys. Rev. Lett. 57 (1986) 1052.

[5] TAKAYASU, H., Phys. Rev. Lett. 54 (1985) 1099.

[6] SAHIMI, M. and GODDARD, J. D., Phys. Rev. B 33 (1986) 7848.

[7] BUI, H. D., Mécanique de la rupture fragile (Masson Ed.) 1978, p. 45, fig. 95.

[8] This property depends on the scenario which governs the breakdown of the network. For instance, in [2] and [4], the network is voltage biased and the total voltage is adjusted at each step of the breaking process so that only one bond carries a current larger than the critical value. This bond is removed, the new distribution of voltages is calculated and the same procedure is repeated. Using this scenario, the voltages controlling the breakdown of the first bond and of the total network are generally different. For a network biased by a constant total current, the current needed to break the first bond generally concides (but not always) with the current necessary to break the entire network. A partial explanation for this difference can be given as follows: removing a bond in a voltage biased network usually involves a drop of the total current while removing a bond in a current biased network induces an increase of the average current per bond. Note also that the currents for breaking the first bond and the entire network become different in a current-biased network when the fuses have different resistances or critical currents (see Ref. [5] in the context of the dielectric breakdown).

[9] SIERADZKI, K. and RONG LI, Phys. Rev. Lett. 56 (1986) 2509.

[10] DE ARCANGELIS, L., REDNER, S. and CONIGLIO, A., Phys. Rev. B 31 (1985) 4725 and preprint « Multiscaling approach in random resistor and random superconducting networks » (1986).

[11] KIRKPATRICK, S., Rev. Mod. Phys. 45 (1973) 574.

[12] DEUTCHER, G., preprint, Chance and Matter, Les Houches (1986).

[13] CONIGLIO, A., in Physics of finely divided matter, ed. by N. Boccara and M. Daoud (Springer) 1985.

[14] KANTOR, Y., Statistical properties of low connectivity bonds in percolation clusters, preprint (1986).

[15] BERGMAN, D. J., GUYON, E. and ROUX, S., to be published.

[16] REDNER, S., in « Physics of finely divided matter », ed. by N. Boccara and M. Daoud (Springer) 1985.

[17] KACHANOV, M. and MONTAGUT, E., Interaction of a crack with certain microcrack arrays, to be published in Engin. Fract. Mech. (1986).
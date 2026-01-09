VOLUME 87, NUMBER 8

PHYSICAL REVIEW LETTERS

20 AUGUST 2001

# Avalanche Dynamics of Crackle Sound in the Lung

Adriano M. Alencar, $^{1,2}$  Sergey V. Buldyrev, $^{2}$  Arnab Majumdar, $^{2}$  H. Eugene Stanley, $^{2}$  and Béla Suki $^{1}$

$^{1}$ Department of Biomedical Engineering, Boston University, Boston, Massachusetts 02215

$^{2}$ Center for Polymer Studies and Department of Physics, Boston University, Boston, Massachusetts 02215

(Received 16 March 2001; published 1 August 2001)

We analyze a sequence of short transient sound waves, called "crackles," which are associated with explosive openings of airways during lung inflation. The distribution of time intervals between consecutive crackles  $\Delta t$  shows two regimes of power law behavior. We develop an avalanche model which fits the data over five decades of  $\Delta t$ . We find that the regime for large  $\Delta t$  is related to the dynamics of distinct avalanches in a Cayley tree, and the regime for small  $\Delta t$  is determined by the dynamics of crackle propagation within a single avalanche. We also obtain a mean-field solution of the model which provides information about lung inflation.

DOI: 10.1103/PhysRevLett.87.088101

The temporal patterns of natural events have been studied extensively to identify hidden dynamics in various processes, including such diverse phenomena as mass extinction in fossil records [1] and popping bubbles in aqueous foams [2]. Here we study a distinct form of popping sound called crackles, which are among the many lung sounds generated in the airways in a diseased lung during breathing.

Crackles are characterized by a rapid initial pressure deflection, called a spike, followed by a short duration ringing. Crackles are associated with the sudden opening of closed airways during lung inflation and have long been used as a qualitative diagnostic tool [3]. Studies of airway closure and opening indicate that, during inflation, airways open in avalanches triggered by overcoming a hierarchy of critical opening threshold pressures along the airway tree [4,5]. The distribution of interavalanche time intervals has been reported to be a power law for intervals ranging from 1 to  $20\mathrm{~s}$  [4]. Avalanches may be composed of discrete crackles which are natural probes containing information about the dynamics of avalanches. Here we analyze the intercrackle intervals from acoustic data spanning over 5 orders of magnitude, from  $10^{-4}$  to  $20\mathrm{~s}$ . These data allow us to extend the scaling region found in [4] to cover the range of 0.01 to  $20\mathrm{~s}$ . However, we also find a plateau between  $10^{-3}$  and  $10^{-2}\mathrm{~s}$  and discover a new scaling region for time intervals below  $10^{-3}\mathrm{~s}$ . We interpret the scaling behavior using a numerical model of avalanche dynamics of airway opening for which we also present a mean-field solution.

We analyze sound recordings from dog lung lobes during lung inflation [6]. The lung lobe was first degassed in a vacuum chamber collapsing almost all the airways, followed by a controlled inflation during which the pressure at the root of the airway tree was increased at a uniform rate from 0 to  $P_{\mathrm{max}} = 3$  kPa to fill the lung in  $t_{\mathrm{max}} = 120$  s. A microphone recorded the sound pressure  $S(t)$  at the root of the airway tree, the main bronchus of the lobe, as a function of time  $t$  (Fig. 1a). We detect the negative spikes in  $S(t)$  using a thresholding algorithm that can find an abrupt

PACS numbers: 87.19.-j, 43.25.+y

change in the derivative of  $S(t)$ . We use several thresholds between  $1\%$  and  $8\%$  of the maximum amplitude of  $S(t)$  to generate a time series of interspike intervals  $\Delta t$ . Two examples are shown in Figs. 1b and 1c. The magnitude of  $\Delta t$  fluctuates significantly with a decreasing envelope (Fig. 2a). The histogram of  $\Delta t$  has two power law regions extending through over 5 orders of magnitude interrupted by a plateau of one decade (Fig. 2b). The exponents of the two regions are  $\alpha = 1.90 \pm 0.05$  for  $\Delta t / t_{\mathrm{max}}$  between  $10^{-6}$  and  $10^{-5}$  and  $\beta = 1.99 \pm 0.28$  for  $\Delta t / t_{\mathrm{max}}$  between  $5 \times 10^{-4}$  and 0.2.

To understand the scaling behavior in Fig. 2b, we develop a dynamic model which takes into account the time

![img-0.jpeg](img-0.jpeg)
FIG. 1. Experimental data. (a) Time series of sound pressure  $S(t)$  during the first inflation of a dog lung lobe from the collapsed state recorded at a rate of  $22050\mathrm{Hz}$ ; (b) a magnified segment of  $S(t)$  with consecutive spikes. The interspike interval  $\Delta t \approx 0.2\mathrm{s}$  of this segment corresponds to the time difference between two spikes; (c) another segment from (a) with  $\Delta t \approx 0.02\mathrm{s}$ .

088101-1

0031-9007/01/87(8)/088101(4)$15.00

© 2001 The American Physical Society

088101-1

---

VOLUME 87, NUMBER 8

PHYSICAL REVIEW LETTERS

20 AUGUST 2001

![img-1.jpeg](img-1.jpeg)

![img-2.jpeg](img-2.jpeg)
FIG. 2. Data analysis. (a) Linear-log plot of one example of  $\Delta t$ , in seconds, against consecutive spike numbers. (b) The histogram of the interspike intervals for 12 different inflations using two different thresholds of the detection algorithm:  $1\%$  (triangles) and  $8\%$  (circles). Note that the exponents do not depend on the value of the threshold. The continuous line is the corresponding histogram of  $\Delta t$  from  $10^{4}$  simulations in a 14-generation symmetric tree.

required for an airway to open and the avalanche to propagate through a  $M$ -generation binary Cayley tree. When the lobe deflates to very low volumes, many peripheral airways close up by forming a liquid bridge between the collapsed airway walls [7]. Thus, each branch labeled  $(i,j)$  is closed at the beginning of the inflation  $(t = 0)$ , where  $i$  is the generation number from the root of the tree  $(i = 1,2,\dots,M)$  and  $j \in [0,2^i - 1]$  labels each branch within the  $i$ th generation. Experiments on flexible tube models indicate that the opening of a single airway can be characterized by a critical opening threshold pressure [8]. Thus, in our model all branches  $(i,j)$  are assigned a random threshold pressure  $P_{i,j}$  uniformly distributed between 0 and  $P_{\mathrm{max}}$  [5]. The inflation is simulated by applying an external pressure  $P_E(t)$  at the top of the tree, and uniformly increasing  $P_E(t) = Kt$  in infinitesimal increments, where  $K = P_{\mathrm{max}} / t_{\mathrm{max}}$  is a constant inflation rate. In the model, we rescale both time and pressure so that  $P_{\mathrm{max}} = 1$  and  $t_{\mathrm{max}} = 1$ , thus  $K = 1$ .

Since an airway opens when the pressure in its parent exceeds its critical threshold pressure, the airway  $(0,0)$  opens when  $P_{E} = P_{0,0}$  at  $t_{0,0} = P_{0,0}$ , where now  $t_{0,0}$  is the time associated with the opening of the root. Next, the two daughter airways  $(1,0)$  and  $(1,1)$  are checked; one or both will open if  $P_{E} \geq P_{1,0}$  and/or  $P_{E} \geq P_{1,1}$ , respectively. This opening process is then continued sequentially down the tree until no airway connected to the root is found with  $P_{i,j} \leq P_{E}$ . Note that the opening of a single branch can

lead to openings of others branches which have  $P_{i,j} &lt; P_E$ , defining an "avalanche" in which many airways open in cascade (Fig. 3a). Opening of an airway also generates a crackle sound locally, which we model as an acoustic spike. The size  $s$  of an avalanche is the number of segments whose threshold pressures are smaller than that of the first airway which triggers the avalanche. Since  $P_E$  increases linearly with time, the opening of the root of the avalanche, airway  $(i,j)$ , occurs at time  $t_{i,j} = P_{i,j}$ . Thus, the time difference between two consecutive avalanches is  $\Delta t = \Delta P$ , the pressure difference between  $P_E$  values that trigger two consecutive avalanches.

To understand the contribution of the interavalanche time differences in the model, we first assume that opening of all segments in an avalanche is instantaneous and the propagation time is negligible. This causes all crackles from the same avalanche to simultaneously arrive at the root. Thus, only interavalanche time intervals are present in this time series. From numerical simulations using  $M$  up to 20, we obtain a single power law where the experimental power law for small  $\Delta t$  is no longer present (Fig. 4a).

At  $t = 0$ , the root of the tree is closed and the probability of it being open is equal to the external pressure

![img-3.jpeg](img-3.jpeg)
FIG. 3. (a) Diagrams describing avalanche timing. Initially, just the root is open and the time for that event is  $t_{0,0}$ . The number of segments on the active surface that are closed is  $N = 2$ . The pressure increases and the left daughter opens at  $t_{1,0}$  and now  $N = 3$ . Following a new increase of pressure, the right daughter of the root opens at  $t_{1,1}$  and  $N = 4$ . Next, the left daughter opens at  $t_{2,2}$  which triggers an avalanche, where each segment of this avalanche has a time delay  $(t_1$  and  $t_2)$  with respect to  $t_{2,2}$ . When the avalanche stops  $N = 3$ ; (b) plot of the number of active segments  $N$  as a function of the external pressure  $P_E$  for three different realizations in a tree with 17 generations (thin lines). The thick line represents Eq. (6).

088101-2

088101-2

---

VOLUME 87, NUMBER 8

PHYSICAL REVIEW LETTERS

20 AUGUST 2001

![img-4.jpeg](img-4.jpeg)
FIG. 4. Data collapse of the distributions normalized with  $2^{M} / t_{\mathrm{max}}$ . (a) Numerical simulations for trees with  $M = 12$  generations (circles),  $M = 16$  generations (squares) and  $M = 20$  generations (triangles). The solid line represents Eq. (4) and the dashed line is the best fit for the numerical simulation with  $M = 20$ . (b) Experimental data for the threshold of  $1\%$ , scaled with  $M = 14$  (circles) and for the threshold of  $8\%$ , scaled with  $M = 10$  (squares). The dashed line is the best fit for the data with the threshold of  $1\%$ .

$P_{E}(0) = 0$ . During the time interval  $\Delta t_{n}$  between two consecutive avalanches,  $n$  and  $n + 1$ , the inflation is blocked by the closed airways, the "active surface." The closed airways on the active surface have threshold pressures  $P_{i,j}$  that are uniformly distributed between  $P_{E}(n)$  and 1, where  $P_{E}(n)$  is the external pressure that has produced the nth avalanche. The number of closed airways  $N(P_{E})$  defines the size of the active surface at each external pressure  $P_{E}$ . The next avalanche takes place when  $P_{E}$  becomes equal to the smallest  $P_{i,j}$  on the active surface:  $P_{E}(n + 1) = \min_{N(P_{E})} \{P_{i,j}\}$ . Thus, the time interval  $\Delta t_{n}$  is defined by  $\Delta t_{n} = \Delta P_{n} = \min_{N(P_{E})} \{P_{i,j}\}$ , where the minimum is taken over all  $N(P_{E})$  closed airways on the active surface. If  $P_{i,j}$  are independent and  $N$  is large enough, then  $\Delta t_{n}$  is distributed according to an exponential distribution [9]:

$$
\Pi_ {n} \left(\Delta t _ {n}\right) = \frac {1}{\overline {{\Delta t _ {n}}}} e ^ {- \Delta t _ {n} / \overline {{\Delta t _ {n}}}}, \tag {1}
$$

with a mean value of  $\overline{\Delta t}_n = (1 - P_E) / N(P_E)$ . The distribution of  $\Delta t$  during the entire inflation is thus the sum of exponential distributions corresponding to all  $n = 1,2,\ldots,n_{\max}$  avalanches, where  $n_{\max}$  is the total number of avalanches:

$$
\Pi (\Delta t) = \frac {1}{n _ {\max}} \sum_ {n = 1} ^ {n _ {\max}} \Pi_ {n} (\Delta t _ {n}). \tag {2}
$$

In order to evaluate this sum, we express it in terms of  $P_E$ . For each realization of threshold pressures, the variables  $N(P_E)$  and  $\overline{\Delta t_n}$  are step functions of  $P_E$ . Since our goal is to find the distribution of  $\Delta t$  for all realizations of disorder, we will replace  $N(P_E)$  and  $\overline{\Delta t_n}$  by their averages over many realizations denoted as  $\langle \dots \rangle$ . For clarity, we introduce a new notation

$$
\tau \left(P _ {E}\right) \equiv \langle \overline {{\Delta t _ {n}}} \rangle = \frac {\left(1 - P _ {E}\right)}{\langle N \left(P _ {E}\right) \rangle}. \tag {3}
$$

Accordingly, we will replace  $\Delta P_{n} \equiv P_{E}(n + 1) - P_{E}(n)$  by  $\tau(P_{E})$ . Taking into account Eq. (1), we approximate the sum in Eq. (2) by an integral from  $P_{E} = 0$  to  $P_{E} = 1$ , corresponding to the summation from  $n = 1$  to  $n = n_{\max}$ :

$$
\begin{array}{l} \Pi (\Delta t) \equiv \frac {1}{n _ {\mathrm {m a x}}} \sum_ {n = 1} ^ {n _ {\mathrm {m a x}}} \frac {\Pi_ {n} (\Delta t _ {n})}{\Delta P _ {n}} \Delta P _ {n} \\ \approx \frac {1}{n _ {\max }} \int_ {0} ^ {1} \frac {e ^ {- \Delta t / \tau \left(P _ {E}\right)}}{\tau^ {2} \left(P _ {E}\right)} d P _ {E}. \tag {4} \\ \end{array}
$$

In order to calculate  $\Pi (\Delta t)$ , we need to find an explicit expression for  $\langle N(P_E)\rangle$  since it is involved in Eq. (4) through Eq. (3). Suppose that on average the  $i$ th generation of the tree contains  $L_{i}$  open branches connected with  $2L_{i}$  branches at the next generation which can be either open or closed. The average number of open branches at generation  $i + 1$  is  $L_{i + 1}$ . Since the distribution of  $P_{i,j}$  is uniform between 0 and 1, the fraction of open branches is equal to  $P_{E}$ . Hence, the number of opened branches in the  $(i + 1)$ th generation is  $L_{i + 1} = 2P_{E}L_{i}$ . This recursion relation has a solution  $L_{i} = (2P_{E})^{i}$ . The number of closed branches connected to the root through open branches at generation  $i + 1$  is given by  $N_{i + 1} = 2L_{i} - L_{i + 1}$ , so

$$
N _ {i + 1} = 2 \left(1 - P _ {E}\right) \left(2 P _ {E}\right) ^ {i}, \tag {5}
$$

thus,

$$
\langle N \left(P _ {E}\right) \rangle = \sum_ {i = 1} ^ {M} N _ {i} = \frac {\left(2 P _ {E}\right) ^ {M} - 1}{2 P _ {E} - 1} \left(1 - P _ {E}\right). \tag {6}
$$

Figure 3b compares Eq. (6) with three different realizations of the numerical model for trees with  $M = 17$ . Substituting  $\langle N(P_E) \rangle$  from Eq. (6) into Eq. (3), we obtain

$$
\tau \left(P _ {E}\right) = \frac {2 P _ {E} - 1}{\left(2 P _ {E}\right) ^ {M} - 1}. \tag {7}
$$

Finally, substituting Eq. (7) into Eq. (4), we obtain the explicit form for the distribution. The normalization constant  $n_{\mathrm{max}}$  can be calculated as  $n_{\mathrm{max}} = \int_0^1 dP_E / \tau (P_E)\approx 2^M /M$ . For large  $M$ , the scaling properties of the integral in Eq. (4) can be estimated by the saddle point approximation: For  $\Delta t\ll 2^{-M}$  we have a uniform distribution,

$$
\Pi (\Delta t) \approx 2 ^ {M - 1}. \tag {8}
$$

This equation gives us an interpretation of the plateau region of the experimental distribution of  $\Delta t$ . For  $1/2^M \ll \Delta t \ll 1/M$ , we have a power law decay,

$$
\Pi (\Delta t) \approx 2 ^ {- M + 1} \Delta t ^ {- 2 - 1 / M}. \tag {9}
$$

088101-3

088101-3

---

VOLUME 87, NUMBER 8
PHYSICAL REVIEW LETTERS
20 AUGUST 2001

This equation gives us a mean-field interpretation of the exponent $\beta \approx 2$ from the experimental distribution of $\Delta t$. The approximations we have used affect only the finite size correction of $\beta$, which is in the order of $1 / M$.

Our model predicts that the crossover between the second power law regime with $\beta = 2$ and the plateau of the experimental distribution of $\Delta t$ scales with $M$ as $1 / 2^{M}$. Using this prediction, we estimate $M$ from the experimental data as $M \approx 14$, for the spike detection threshold of $1\%$, and $M \approx 10$ for the threshold of $8\%$. The two curves for different thresholds collapse after scaling them with the corresponding values of $M$ (Fig. 4b).

To interpret the first power law region of the experimental $\Pi (\Delta t)$ for $\Delta t / t_{\mathrm{max}} &lt; 10^{-5}$ (Fig. 2b), we recognize that, when an avalanche consisting of $s$ openings occurs, the segments in the avalanche do not open simultaneously. We assume that the $k$th crackle $(k = 1,2,3,\dots ,s)$ generated inside an avalanche arrives at the root of the avalanche with a time delay $t_k$ (Fig. 3a). The $t_k$ is taken to be proportional to the path length $\ell_{k}$ between the root of the avalanche and segment $k$ that generates the crackle: $t_k = \ell_k / \nu$, where $\nu$ is a characteristic propagation velocity. We implement the dynamics of avalanche propagation in the numerical model using a path length distribution similar to published data [10]. Changing $\nu$ shifts the first power law region in the simulated data to the left or right, but does not alter the exponents $\alpha$ and $\beta$. We find that using $\nu = 4.8~\mathrm{m / s}$ in the model reproduces the behavior of the experimental data over five decades of $\Delta t$. The continuous line in Fig. 2b shows the distribution of $\Delta t$ for a tree of 14 generations. There are two regions of power law behavior with exponents of $\alpha = 2.4$ and $\beta = 2.18$ similar to the experimental values of $\alpha = 1.9$ and $\beta = 2.0$.

Examining published opening times for $2\mathrm{mm}$ diameter airways [11], we estimate that the velocity of a "popping" type of opening is between 2 and $4\mathrm{m / s}$. The agreement with the model is good, since $\nu$ depends on various factors—including external pressure, airway diameter, surface tension, and viscosity of the lining fluid. Since $\nu \approx 5\mathrm{m / s}$ is consistent with the experimental data, $\nu$ is related to the opening time of an airway rather than the propagation velocity of sound in the airways, which is larger than $100\mathrm{m / s}$ [12].

Before concluding, we note the following: (i) From the mean-field calculation, we find that detectable crackles

come from the last 14 generations after the first closed airway in the lobe. The agreement of the model with experimental data is consistent with the possibility that, in the 14 generations of the airway tree from which we can detect crackles, the distribution of threshold pressures is uniform. (ii) The numerical simulations suggest that the first power law region is related to the distribution of opening time delays, which in turn is related to the length distribution of the airway segments. Since the airway tree is self-similar [13], the length distribution is a power law. Thus, the exponent $\alpha$ is likely to be related to the exponent of the airway length distribution. In summary, studying the dynamics of the lung crackle sounds may prove useful in obtaining structural information on the airway tree.

We thank NSF for support.

[1] R. V. Sole, S. C. Manrubia, M. Benton, and P. Bak, Nature (London) 388, 764 (1997).
[2] N. Vandewalle, J.F. Lentz, S. Dorbolo, and F. Brisbois, Phys. Rev. Lett. 86, 179 (2001).
[3] H. Pasterkamp, S. S. Kraman, and G. R. Wodicka, Am. J. Respir. Crit. Care Med. 156, 974 (1997).
[4] B. Suki, A.-L. Barabási, Z. Hantos, F. Peták, and H.E. Stanley, Nature (London) 368, 615 (1994).
[5] A.-L. Barabási, S. V. Buldyrev, H. E. Stanley, and B. Suki, Phys. Rev. Lett. 76, 2192 (1996).
[6] A. M. Alencar, Z. Hantos, F. Peták, J. Tolnai, T. Asztalos, S. Zapperi, J. S. Andrade, S. V. Buldyrev, H. E. Stanley, and B. Suki, Phys. Rev. E 60, 4659 (1999).
[7] R. D. Kamm and R. C. Schroter, Resp. Physiol. 75, 141 (1989).
[8] D. P. Gaver, R. Samsel, and J. Solway, J. Appl. Physiol. 69, 74 (1990).
[9] C. Derman et al., A Guide to Probability Theory and Application (Holt, Rinehart and Winston, New York, 1973), pp. 359-369; S.M. Ross, Introduction to Probability Models (Academic, New York, 1997), p. 578.
[10] E. R. Weibel, Morphometry of the Human Lung (Academic, New York, 1963).
[11] D. Y. K. Yap, W. D. Liebkemann, J. Solway, and D. P. Gaver, J. Appl. Physiol. 76, 2095 (1994).
[12] D.A. Rice and J.C. Rice, J. Acoust. Soc. Am. 82, 1139 (1987).
[13] M. F. Shlesinger and B. J. West, Phys. Rev. Lett. 67, 2106 (1991).

088101-4
088101-4
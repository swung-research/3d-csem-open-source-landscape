Introduction
############

Publications regarding 3D modelling in electromagnetic methods started to
appear as early as the 70's and 80's. These early publications where all
integral equation (IE) methods, having an anomaly embedded within a layered
medium, for loop-loop type transient EM measurements ([Raic74]_, [Hohm75]_,
[DaVe82]_, [NeHA86]_) and magnetotelluric (MT) measurements ([WaHW84]_).

In the 90's computer became sufficiently powerful that 3D modelling gained
traction, which resulted amongst other in the publication of the book
*Three-Dimensional Electromagnetics*, [OrSp99]_ by the SEG. Often cited
publications from that time are [MaSM94]_ (3D MT calculation), [DrKn94]_
(frequency- and time-domain modelling using a Yee grid and a global Krylov
subspace approximation), and [ANPS.96]_, [NeAl97]_ (low-to-high frequency
calculation on massively parallel computers).

The continuous improvement of computing power and the CSEM boom in the early
2000's in the hydrocarbon industry led to a wealth of publications. The amount
of available numerical solutions can be overwhelming and is part of the reason
why there are hundreds of publications about the topic. There are the different
methods to solve Maxwell's equation, such as the IE method ([Raic74]_,
[HuZh02]_, [ZhLY06]_, [TeSl10]_, [KrGK16]_, [KrBl17]_) and different variations
of the DE method, for instance FD ([Yee66]_, [MaSM94]_, [DrKn94]_, [Stre09]_,
[SHMS13]_), FE ([ScBS11]_, [DMMW12]_, [PKDH13]_, [GrKo15]_, [ZhKe16]_), FV
([MaZi90]_, [HaHe07]_, [JaFa14]_), and FI ([ClWe01]_, [Muld06]_). And these are
just the most common ones.

There are also many different types of discretization, where the most common
ones are regular grids (Cartesian, rectilinear), mostly using a Yee grid
([Yee66]_) or a Lebedev grid ([Lebe64]_), but also unstructured tetrahedral
grids ([ZhKe16]_, [CHLE17]_), OcTree meshes ([HaHe07]_), or hexagonal meshes
([CXHZ14]_).

The biggest variety of all exists probably in the available solvers to solve
the system of linear equations; direct solvers ([Stre09]_, [GrSR13]_,
[CSLK14]_, [JaSD14]_, [ONSB15]_, [WaMS18]_), indirect solvers ([Muld06]_,
[JaSD15]_) or a combination of both, so-called hybrid solvers ([LGLM18]_); the
solvers often use preconditioners such as the multigrid method ([ArAs02]_,
[Muld06]_, [JSDB16]_).

A very well written overview up to the year 2005 of the different approaches to
3D EM modelling is given by [Avde05]_. In the last 15 years the publications
with regards to 3D EM  modelling grew tremendously, driven probably by improved
computer powers.


==============================================================================

Overviews: From [Avde05]_
-------------------------

Over the last decade, the EM induction community had three large international
meetings entirely devoted to the theory and practice of three-dimensional (3-D)
electromagnetic (EM) modelling and inversion (see Oristaglio and Spies, 1999;
Zhdanov and Wannamaker, 2002; Macnae and Liu, 2003). In addition, two special
issues of Inverse Problems dedicated to the same subject have been recently
published (Lesselier and Habashy, 2000; Lesselier and Chew, 2004).

«I would like to conclude this review with the following general remark. The
most important challenge that faces the EM community today is to convince
software developers to put their 3-D EM forward and inverse solutions into the
public domain, at least after some time. This would have a strong impact on the
whole subject and the developers would benefit from feedback regarding the real
needs of the end-users.»

=> Use this quotation as a hook.


==============================================================================

*Just a list of ideas and notes so far.*

List codes, particularly papers presented that are, potentially, available or
not, but only by contacting the author. Mention change in coding practices,
development in the open, collaboration, bug reports, better documentation and
testing, etc. Example: [CHLE17]_ (open or not?)

Mention [MQJM13]_, which is a similar thing, but for 3D modelling and inversion
for MT.

Common features of our codes is:

- Not just open source, but also developed in the open and increasingly
  building a global community - also mention other projects as, e.g., pyGIMLi
  [RuGW17]_ and Fatiando (e.g., [Uied18]_).
- All codes we compare work in the Python eco-system (hard work underlying the
  Python API can differ though).
- Also modern dev, which includes CI testing, good documentation, issue
  tracking, and extensive discussion through Slack, Gitter, or similar, with
  dozens to hundreds of members (SimPEG 09-09-2019: 189 members), which
  constitutes a vibrant community and combines a huge spectrum from coders to
  first time users, and from academia to industry.

It is worth mentioning that there are many more open-source 3D electromagnetic
codes developed in other fields than geophysics. Examples include ... (TODO:
add at least three references). While these codes could potentially be used for
the same goals as presented here we restrict our review to codes purpose-built
for geophysical applications.

An integral part of this publication are the necessary instructions and codes
to reproduce all published results. In fact, the provided codes contain more
than just the results shown here, as including everything here would have made
the article to lengthy.

----

- Mention all use cases (ground water, geothermal, oil and gas, civil
  engineering, hazards).
- Mention other fields.
- Mention MT comparison paper.


Many 3D codes exist since long (SEG 3D book by oristaglio, etc). However, there
are a few key differences recently:

- Codes are *just available* (you don't have to write someone and ask if you
  could have the code)
- Codes are *easy installable* (e.g., ``pip install emg3d``)
- Codes are well documented and come with a lot of examples
- It is easy to get involved (GitHub/GitLab) and contribute
- It is easy to get help (Slack, GitHub/GitLab)

This will significantly increase the user base and the number of people who are
actually doing 3D EM modelling.

----

- Why need:

  - analytical solutions
  - semi-analytical solutions such as 1D codes (analytical [recursion] in k-f
    domain followed by numerical transformation).
  - need of comparison of more complex models.

- What exists:

  - very quick run-down of codes, methods, discretizations.
  - Thesis Raphael
  - LitRev Dieter

- What changed:

  - Python
  - Demand/Desire for reproducible research
  - Open-source has changed:

    - easy install
    - documented
    - bug/issues
    - communities
    - testing/benchmarks/coverage/style/quality

- What is this paper:

  - 4 codes, 2 FD 2 FE
  - 2 models, simple one after MT paper, complex Marlim one

- Outline of paper
- Zenodo, provide all codes to reproduce the results.


==============================================================================


There are many codes for EM - our focus here is on the application to
controlled-source electromagnetic measurements, even though all of the codes
can handle different setups too.

in such fields as the modelling of communication systems (antennas, radar,
satellites), medical imaging, and others.

time domain and frequency domain

1D, 2D, we look at 3D.


Common methods in geophysics are the

- integral equation (IE, [Raic74]_, [ZhLY06]_, [KrGK16]_), (scattering
  equation) (anomalies in layered background), computational effort comparably
  low

- differential equation such as finite difference (FD [Yee66]_, [WaHo93]_),
  simple to implement

- and finite volume (FV [MaZi90]_, [JaFa14]_),

- or and finite element (FE [CoNe04]_, [Stre09]_) (approximating the DE on
  edges and nodals), good for complex geometries,

- finite integration technique (FIT, [Weil77]_, [ClWe01]_, [Muld06]_)

OctTree meshes or severe stretching ([HaHe07]_)


Elmer FEM multiphysical simulation software
P. Råback, P.-L. Forsström, M. Lyly and M. Gröhn, Elmer - finite element package for the solution of partial differential equations, poster presentation, EGEE User Forum, 2007, Manchester, UK.
http://www.csc.fi/elmer


Many commercial, e.g., COMSOL Multiphysics; EMGS, RSI, KMS; the oil and service
companies.

Consortia (CEMI; Key)

Universities, e.g. Pottsdam (Streich, Grayver)

Computational cost IE < FD < FV < FE

Direct solvers vs indirect solvers, both its advantages and disadvantages;
memory, various sources.

Grids (regular grids, unstructured grids, Octree, tetrahedra, hexahedral,
adaptive, multigrids).

Boundary condition


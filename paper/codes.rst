Codes
#####

Each code should outline:

- Equation system it solves;
- the used discretization possibilities;
- domains (frequency, time);
- details (anisotropy; el. perm. and mag. perm.);
- other things (inversion; other methods);
- speed and memory estimation;
- plans for next features.

- Inversion capabilities
- Time/frequency
- transmitter types

emg3d
=====

The 3D CSEM modeller `emg3d` ([WeMS19]_) is a multigrid ([Fedo64]_) solver for
3D electromagnetic diffusion following [Muld06]_, with tri-axial electrical
anisotropy and isotropic magnetic permeability. The matrix-free solver can be
used as main solver or as preconditioner for one of the Krylov subspace methods
implemented in SciPy ([JOPO01]_), and the governing equations are discretized
on a staggered grid by the finite-integration technique ([Weil77]_), which can
be viewed as a finite-volume generalization of [Yee66]_'s scheme. The code is
written completely in Python using the NumPy ([WaCG11]_) and SciPy stacks,
where the most time- and memory-consuming parts are sped up through jitted
functions using Numba ([LaPS15]_).

The multigrid method is characterized by almost linear scaling both in terms
of CPU usage and RAM, and it is therefore a comparably low-memory consumption
solver (see results). However, the way multigrid is implemented also means some
additional constraints on the chosen grid. You can input any three-dimensional
grid into `emg3d`, but the implemented method works with the existing nodes,
meaning there are no new nodes created as coarsening is done by combining
adjacent cells. The more times the grid dimension can be divided by two the
better it is suited. Ideally, the dimension of the coarsest grid should be a
low prime, and grid dimensions are therefore given by their multiplication with
powers of two ({2,3,5}·2^n).

Currently `emg3d` can be used to model the electric and magnetic fields due to
arbitrary finite length electric dipole sources for a single frequency at a
time. Helper functions to calculate time-domain responses are in the works
(should be ready by publishing this article). Current development is focused
on adding inversion capabilities; averaging routines to implement strong
topography; and general anisotropy.

The 3D solver `emg3d` can be found in the GitHub organization of `empymod`
(`empymod.github.io <https://empymod.github.io>`_). The modeller `empymod`
([Wert17]_) is a 1D code which can calculate electric or magnetic responses due
to a 3D electric or magnetic source in a layered-earth model with vertical
transverse isotropic (VTI) resistivity, VTI electric permittivity, and VTI
magnetic permeability, from very low frequencies (DC) to very high frequencies
(GPR).

In the future it should be possible to use `emg3d` as a solver within the
`SimPEG` framework.

SimPEG
======

[CKHP15]_

PARDISO ([ScGa04]_)


custEM
======

[RoSG19]_

FEniCS ([ABHJ15]_)


PETGEM
======

[CPGC19]_

FEniCS ([ABHJ15]_)


MARE3DEM
========


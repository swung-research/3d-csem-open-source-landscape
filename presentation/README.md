# Open-Source Landscape for Three-Dimensional Controlled-Source Electromagnetic Modeling

- Dieter Werthmüller, *Delft University of Technology*;
- Raphael Rochlitz, *Leibniz Institute for Applied Geophysics*;
- Octavio Castillo Reyes, *Barcelona Supercomputing Center*;
- Lindsey Heagy, *University of California Berkeley*.

**Abstract submitted for the AGU Fall Meeting 2020.**
> - *Abstract ID:* 668928
> - *Abstract Title:* Open-Source Landscape for Three-Dimensional Controlled-Source Electromagnetic Modeling
> - *Final Paper Number:* GP005-06
> - *Presentation Type:* Oral Session
> - *Session Date and Time:* Monday, 14 December 2020; 10:00 - 11:00 PST
> - *Presentation Length:* 10:37 - 10:41 PST
> - *Session Number and Title:* GP005: Frontiers in Electromagnetic (EM) Geophysics I

## Abstract

The open-source landscape of three-dimensional modeling for controlled source
electromagnetic (CSEM) data has changed dramatically within the last five
years. While modeling large-scale CSEM data was previously the privilege of
large exploration companies or academic consortia, nowadays it is  possible for
everyone. This is not only thanks to open-source codes, but also to increased
computing power which makes it affordable for anyone to run 3D simulations.

We combined forces between four open-source CSEM codes to showcase the
capabilities of open-source CSEM modelers today. The four codes under
consideration are custEM, PETGEM, SimPEG, and emg3d. The former two are
finite-element (FE) codes using unstructured tetrahedral meshes, and the latter
two are finite-volume (FV) codes using structured octree or tensor meshes.
Besides layered and block models we also compare them for the realistic,
open-source resistivity model Marlim R3D and its accompanying CSEM data.

Comparing results of 3D CSEM computations are a crucial aspect of code
verification. The common way to verify codes is to compare results to
analytical or semi-analytical solutions, which only exist for very simplistic
models. The only method to verify complicated, realistic models is to compare
the results of different codes. Our comparisons show that all four codes yield
the same result within acceptable errors, independent of the chosen finite
element method (FE or FV) and of the applied discretization.

Our comparison of four codes not only verifies all four codes with each other,
but further, this project has motivated improvements in each of the code-bases
and demonstrates how collaboration between (open-source) projects is beneficial
and advances all participants. We hope that our efforts will help to ensure the
reliability of CSEM simulations, not only of the presented open-source codes,
but also for other open-source or proprietary projects.


## Recording

See
https://werthmuller.org/download/research/AGU20_OpenSource3DCSEMLandscape.mp4

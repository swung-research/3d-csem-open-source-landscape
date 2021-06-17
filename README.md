# Towards an open-source landscape for 3D CSEM modelling

> Werthmüller, D., R. Rochlitz, O. Castillo Reyes, and L. Heagy,
> Towards an open-source landscape for 3D CSEM modelling:
> Geophysical Journal International (accepted).


This repository contains the LaTeX source of the manuscript as well as the
necessary codes to reproduce all the results and figures.

**Repository structure**

    ├── environment.yml  # Python environment file
    ├── LICENSE          # CC-BY-SA-4.0 License
    ├── README.md        # this file
    ├── manuscript/      # LaTeX-files
    │   └── figures/     # figures used in manuscript
    ├── model-{MODEL}/   # for MODEL in {block, marlim}
    │   ├── README.md    # info about MODEL
    │   ├── {CODE}/      # for CODE in {custEM, emg3d, PETGEM, SimPEG}
    │   └── results/     # results of the different codes
    └── presentation/    # talk given at the AGU 2020

Each `model-{MODEL}/`-directory contains a `README.md` with more information
about the particular model.


## History

1. 2020-10-23: Submitted to Geophysical Journal International.
2. 2021-02-15: Revision I submitted.
3. 2021-04-15: Revision II submitted.
4. 2021-06-08: Revision III submitted.
5. 2021-06-16: Accepted.


## Data

The information in this repo is enough to reproduce all results and figures
shown in the manuscript. Our results are available at
[10.5281/zenodo.4535602](https://doi.org/10.5281/zenodo.4535602).


## Environment

The `environment.yml` file generates a
[conda-environment](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html)
(see [Anaconda Python Distribution](https://www.anaconda.com/distribution))
with all the required dependencies. To create the environment simply run

```bash
conda env create -f environment.yml
```
This will create a new conda environment called `csem`.

To activate the environment run
```bash
conda activate csem
```
and to deactivate it run
```bash
conda deactivate
```

To use this environment in the Jupyter notebook, you have to register it first:
```bash
python -m ipykernel install --user --name csem
```
Then, in the Jupyter notebook (or Jupyter lab), you can select it by going to
`Kernel`->`Change kernel` and select `csem`.

To completely remove the environment run
```bash
conda remove --name csem --all
```

_You need at least Python 3.7 to run (at least some of) the codes._


## Dependencies

Dependencies are a difficult topic, and no-one can guarantee that the scripts
will still work a few years down to road with many new releases of all
dependencies. We list here therefore the most important dependencies that were
used when creating the results.


Note that all notebooks (data creation, results, and computation of emg3d and
SimPEG) have a ``scooby``-report at the end, listing the most important
dependencies and their version.


### emg3d

The following is the emg3d-scooby report. You can get your own either in Python
via ``emg3d.Report()`` or in the terminal via ``emg3d --report``.

```
--------------------------------------------------------------------------------
  Date: Thu Jun 17 14:50:50 2021 CEST

                OS : Linux
            CPU(s) : 4
           Machine : x86_64
      Architecture : 64bit
               RAM : 15.5 GB
       Environment : Python

  Python 3.8.0 | packaged by conda-forge | (default, Nov 22 2019, 19:11:38)
  [GCC 7.3.0]

             numpy : 1.19.5
             scipy : 1.6.0
             numba : 0.52.0
             emg3d : 0.16.0
           empymod : 2.0.4
            xarray : 0.16.2
        discretize : 0.6.2
              h5py : 3.1.0
        matplotlib : 3.3.3
           IPython : 7.19.0

  Intel(R) Math Kernel Library Version 2020.0.4 Product Build 20200917 for
  Intel(R) 64 architecture applications
--------------------------------------------------------------------------------
```


### custEM

```
custEM     1.0.0
fenics     2019.1
pygimli    1.1.0
tetgen     1.51
```

### PETGEM

```
petgem     0.8
petsc      3.7
petsc4py   3.7
python     3.6.1
numpy      1.18.3
scipy      1.5.2
gmsh       4.5.4

```

### SimPEG

The following an excerpt from the SimPEG-scooby report. You can get your own
either in Python via ``SimPEG.Report()`` or in the terminal via ``python -c
'import SimPEG; print(SimPEG.Report())'``.

```
                OS : Linux
            CPU(s) : 8
           Machine : x86_64
      Architecture : 64bit
               RAM : 413.4 GB
       Environment : Python
  Python 3.7.9 | packaged by conda-forge | (default, Dec  9 2020, 21:08:20)
  [GCC 9.3.0]
            SimPEG : 0.14.3
        discretize : 0.6.2
       pymatsolver : 0.1.2
        vectormath : 0.2.2
        properties : 0.6.1
             numpy : 1.19.2
             scipy : 1.2.1
        matplotlib : 3.3.4
```
=======

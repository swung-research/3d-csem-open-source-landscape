# Open-source landscape for 3D CSEM modelling

> Werthmüller, D., R. Rochlitz, O. Castillo Reyes, and L. Heagy,
> Open-source landscape for 3D CSEM modelling:
> Submitted to Geophysical Journal International.


This repository contains the LaTeX source of the manuscript as well as the
necessary codes to reproduce all the results and figures.

**Repository structure**

    ├── environment.yml  # Python environment file
    ├── LICENSE          # CC-BY-SA-4.0 License
    ├── README.md        # this file
    ├── manuscript/      # LaTeX-files
    │   └── figures/     # figures used in manuscript
    └── model-{MODEL}/   # for MODEL in {block, marlim}
        ├── README.md    # info about MODEL
        ├── {CODE}/      # for CODE in {custEM, emg3d, PETGEM, SimPEG}
        └── results/     # results of the different codes

Each `model-{MODEL}/`-directory contains a `README.md` with more information
about the particular model.


## History

1. Submitted 2020-10-23 to Geophysical Journal International.


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

_You need at least Python 3.7 to run the codes._

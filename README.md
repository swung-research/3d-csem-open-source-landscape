# Status of the open-source landscape for 3D CSEM modelling


## Repository structure

    ├── environment.yml    # Requirements to reproduce it all (1)
    ├── literature         # Papers (2)
    └── manuscript
    │   ├── data           # Data for figures (3)
    │   ├── figures        # Figures for the paper
    │   └── notebooks      # Notebooks to create above figures
    └── model-{MODEL}      # 'block' or 'marlim'
        ├── {CODE}         # Each code has its folder
        └── results        # Result of each code

1. The environment-yaml. See section below.
1. This will not move to the public repo.
2. Will currently stay empty, and figures will be created using the files in
   `model-{MODEL}/results`. However, once the article is finished this folder
   should contain all data to create the figure, such that the
   `manuscript`-folder is self-contained and can reproduce the entire article.

**Each `model`-directory contains a README.md with instructions how to load the
model and how to save the data correctly, so that we all save it in the same
way.**


## Environment

We provide an `environment.yml` to ensure everything can be reproduced.
**Everyone should update this file** for the needs of their codes, and
**everyone should test that the environment works with their codes**. Please
limit it to the bare minimum, so we do not inflate it.

To create the environment simply run
```bash
conda env create -f environment.yml
```
This will create a new conda environment called `os-csem` (for open-source
CSEM).

To activate and deactivate the environment run
```bash
conda activate os-csem
conda deactivate os-csem
```

To completely remove the environment run
```bash
conda remove -name os-csem --all
```


## Manuscript

The current manuscript lives in the `manuscript`-directory. Build it by running

```bash
make html
```

in the `manuscript` directory, and subsequently open
`manuscript/_build/html/index.html` in your browser.

If you have `sphinx-autobuild` installed (`pip install sphinx-autobuild`), you
can type

```bash
make livehtml
```

This will automatically open a browser with the docs, watch the `manuscript`
directory, re-build whenever a source file has changed, and refresh the
browser.

# Status of the open-source landscape for 3D CSEM modelling


## Repository structure

    ├── literature         # Papers (1)
    └── manuscript
    │   ├── data           # Data for figures (2)
    │   ├── figures        # Figures for the paper
    │   └── notebooks      # Notebooks to create above figures
    └── model-{MODEL}      # 'block' or 'marlim'
        ├── {CODE}         # Each code has its folder
        └── results        # Result of each code

1. This will not move to the public repo.
2. Will currently stay empty, and figures will be created using the files in
   `model-{MODEL}/results`. However, once the article is finished this folder
   should contain all data to create the figure, such that the
   `manuscript`-folder is self-contained and can reproduce the entire article.

**Each `model`-directory contains a README.md with instructions how to load the
model and how to save the data correctly, so that we all save it in the same
way.**


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

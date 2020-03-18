Introduction
############

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

Discussion
##########

The landscape in 3D CSEM modelling greatly changed in the last five years or
so. While before there were only closed-source codes owned by companies or
consortia (e.g., CEMI), or codes that you had to obtain from the authors, often
without much documentation, there was recently a wave of openly released codes.

...


We see this only as the start. Much more comparisons and examples are required.
3D CSEM modelling is a difficult task, which requires many considerations:
It starts with the selection of the right code for the problem; then the
meshing is particularly difficult, choosing cells small enough to appropriately
represent the model yet to be as coarse as possible still achieving the desired
precision; the required model extent, particularly for shallow and marine cases
where the airwave has to be considered. The tricky part is that even if the
result is not correct it may look completely valid. The only options to verify
results are (a) by comparing different discretizations, and (b) by comparing
different codes.

Here we only consider frequency-domain results from frequency-domain
computations. Similar comparison for time-domain results from time-domain
computations, and frequency-domain results from time-domain computations and
vice versa using Fourier transforms would also be good.

The readily availability of many codes means there will be many more people
able to model 3D results, and not just a few specialists in the field. Whilst
this is amazing and will push the field much further it also means that the
same mistakes might happen over and over again, and comparisons and examples
like these can help to avoid this.


Future (?)
==========

Comment KK: *One thing that the community could really use is more test models
for various scenarios, and having them be easily accessible.*


MARE3DEM
========

This is, I thought, the right spot where Kerry Key could write a bit about
MARE3DEM, if (and I think only if) there are clear plans and a time-scale to
open-source it. Embedded in a wider summary of available codes (some research
required).

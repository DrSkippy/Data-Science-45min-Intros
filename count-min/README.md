This ipython notebook is a brief, interactive introduction to the Count Min (CM) Sketch,
a method of estimating the number of occurances of a particular item in a set.
The CM sketch is well-suited to estimating "heavy-hitters" in a streaming data set.

First, the notebook implements an algorithm for the CM sketch, taken from [here](https://tech.shareaholic.com/2012/12/03/the-count-min-sketch-how-to-count-over-large-keyspaces-when-about-right-is-good-enough/). Exact and approximate frequencies for the heavy hitters 
are calculated and compared for various configurations of the CM sketch. Some timing tests are done.

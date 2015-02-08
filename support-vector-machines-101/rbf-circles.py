#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

import sys
import json
import numpy as np
import matplotlib.pyplot as plt
try:
    import seaborn as sns
except ImportError as e:
    sys.stderr.write("seaborn not installed. Using default matplotlib templates.")
from sklearn.svm import SVC 
from sklearn.datasets import make_circles

# adapted from:
# http://scikit-learn.org/stable/auto_examples/svm/plot_svm_kernels.html
# http://scikit-learn.org/stable/auto_examples/decomposition/plot_kernel_pca.html


xx, yy = make_circles(n_samples=500, factor=0.1, noise=0.15)

clf = SVC(kernel='rbf')
clf.fit(xx, yy)

plt.figure(figsize=(8,6))

plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],
            facecolors='none', zorder=10, s=300)
plt.scatter(xx[:, 0], xx[:, 1], c=yy, zorder=10, cmap=plt.cm.Paired, s=100)
#plt.scatter(xx[:, 0], xx[:, 1], c=yy, zorder=10, s=100)

plt.axis('tight')

x_min = -1.5
x_max = 1.5
y_min = -1.5
y_max = 1.5


XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])

# Put the result into a color plot
Z = Z.reshape(XX.shape)
#plt.figure(fignum, figsize=(4, 3))
#plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)
plt.pcolormesh(XX, YY, Z > 0, alpha=0.1)
plt.contour(XX, YY, Z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'],
            levels=[-.5, 0, .5])

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.title('rbf kernel')

plt.show()



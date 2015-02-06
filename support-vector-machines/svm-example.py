#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

import sys
import pandas as pd
import numpy as np

from sklearn.datasets import make_blobs
from sklearn.svm import SVC

import matplotlib.pyplot as plt
try:
    import seaborn as sns
except ImportError as e:
    sys.stderr.write("seaborn not installed. Using default matplotlib templates.")

# cobbled together from refs:
# http://scikit-learn.org/stable/auto_examples/svm/plot_iris.html
# http://scikit-learn.org/stable/auto_examples/svm/plot_separating_hyperplane.html

if len(sys.argv) > 1:
    samples = int( sys.argv[1] )
    c_std=2.0
else:
    samples = 10 
    c_std=1.0

X, y = make_blobs(n_samples=samples, cluster_std=c_std, centers=2)


# make a plotting grid
h = .02  # step size in the mesh
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

# svm
clf = SVC(kernel='linear').fit(X, y)

# predict all points in grid
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

# separating plane and margins
w = clf.coef_[0]
a = -w[0] / w[1]
xxx = np.linspace(x_min, x_max)
yyy = a * xxx - (clf.intercept_[0]) / w[1]

# calculate the large margin boundaries defined by the support vectors 
b = clf.support_vectors_[0]
yyy_down = a * xxx + (b[1] - a * b[0])
b = clf.support_vectors_[-1]
yyy_up = a * xxx + (b[1] - a * b[0])

# plot margins 
plt.figure(figsize=(8,6))
plt.plot(xxx, yyy, 'k-', linewidth=1)
plt.plot(xxx, yyy_down, 'k--', linewidth=1)
plt.plot(xxx, yyy_up, 'k--', linewidth=1)

# plot decision contours 
Z = Z.reshape(xx.shape)
#plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)
plt.contourf(xx, yy, Z, alpha=0.25)

# plot data 
plt.scatter(X[:, 0], X[:, 1], 
            s=100,
            c=y, 
            alpha=0.8,
            cmap=plt.cm.Paired
            )

# plot support vectors
plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], 
            s=300, 
            facecolors='none'
            )

plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.xlabel('x')
plt.ylabel('y')

# SHOW ALL THE THINGS 
plt.show()


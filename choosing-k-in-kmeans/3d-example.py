#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

"""
This script is designed to run inline (%run 3d-example.py) in 
the corresponding IPython notebook. It generates a 3d scatter 
plot using scikit-learn data generation and with a number of 
samples and clusters determined by the variables near the top. 
"""

import argparse 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets import make_blobs
import seaborn as sns
from gap_stats import gap_statistics
from gap_stats import plot_gap_statistics 


def make_example_plot(args):
    """
    Create artificial data (blobs) and color them according to the
    appropriate blob center.
    """
    # read args 
    samples = args.samples 
    clusters = args.clusters 

    # create some data 
    X, y = make_blobs(n_samples=samples,
                        centers=clusters, 
                        n_features=3, 
                        # increase variance for illustration
                        cluster_std=1.5,
                        # fix random_state if you believe in determinism
                        #random_state=42
                        )

    # seaborn display settings
    sns.set(style='whitegrid', palette=sns.color_palette("Set2", clusters)) 

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(clusters):
        # for each center, add data to the figure w/ appropriate label
        ax.plot(X[y==i,0], 
                X[y==i,1], 
                X[y==i,2], 
                'o', 
                alpha=0.6,
                label='cluster {}'.format(i)
                )

    ax.set_title('{} labeled clusters (ground truth)'.format(clusters))
    ax.legend(loc='upper left')

    # seaborn settings - no, really set these things this time, please 
    sns.set(style='whitegrid', palette=sns.color_palette("Set2", clusters)) 

    #plt.show()

    # potentially return the data for later use 
    data = None
    if args.gap:
        data = (X, y) 
    return data 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--samples"
        , dest="samples"
        , type=int
        , default=100
        )
    parser.add_argument("-c","--clusters"
        , dest="clusters"
        , type=int
        , default=5
        )
    parser.add_argument("-g","--gap"
        , dest="gap"
        , type=bool
        , default=False
        )

    args = parser.parse_args()

    data = make_example_plot(args)

    if args.gap:
        # i just really prefer the dark theme
        sns.set(style='darkgrid', palette='deep')   
        # unpack
        X, y = data
        # run the gap statistic algorithm
        gaps, errs, difs = gap_statistics(X, ks=range(1, args.clusters+5))    
        # plot (intended for %matplotlib inline)
        plot_gap_statistics(gaps, errs, difs)


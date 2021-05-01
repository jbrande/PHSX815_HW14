#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import numpy as np
import re
import json


# import our Random class from python/Random.py file
sys.path.append(".")
from python.Random import Random

# main function for our coin toss Python code
if __name__ == "__main__":
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [-K integer] [-Npoints integer] [-output string]" % sys.argv[0])
        print ("-K:         (optional) the number of distributions to mix, if not given, default K=2. must be >= 1")
        print ("-Npoints:   (optional) the number of points per distributions, if not given, default K=10. must be >= 1")
        print ("-output:    (mandatory) the name of the output file to print to. must be given")
        print
        sys.exit(1)

    # number of clusters
    K = 2

    # number of points per cluster
    Npoints = 10

    # output file defaults
    doOutputFile = False

    # read the user-provided arguments from the command line (if there)
    if '-K' in sys.argv:
        p = sys.argv.index('-K')
        K = int(sys.argv[p+1])
        if K < 1:
            print("K must be >= 1")
            sys.exit(1)
    if '-Npoints' in sys.argv:
        p = sys.argv.index('-Npoints')
        Npoints = int(sys.argv[p+1])
        if Npoints < 1:
            print("Npoints must be >= 1")
            sys.exit(1)
    if '-output' in sys.argv:
        p = sys.argv.index('-output')
        OutputFileName = sys.argv[p+1]
        doOutputFile = True
    else:
        print("You must pass a filename!")
        sys.exit(1)
    
    # structure to hold results
    results = {
        "x": [],
        "y": [],
    }


    # easy mixture model, all distributions have equal probability, just straight sum each of them
    # means and variances are uniformlu random for each gaussian, in range mu=[-10, 10], sigma=[0, 2]
    # using numpy.random.multivariate_normal() to make this easier

    # need 2-D samples, since this is a 2-D space problem
    mus = np.random.uniform(-5, 5, (K,2))
    sigs = np.random.uniform(0, 2, (K,2))

    for k in range(K):
        # covariance matrix for 2-D gaussians
        cov = [[sigs[k][0], 0],[0, sigs[k][1]]]
        x, y =  np.random.multivariate_normal(mus[k], cov, Npoints).T
        results["x"] = results["x"] + x.tolist()
        results["y"] = results["y"] + y.tolist()

    # for later analysis, print the results as a JSON object to a file
    if doOutputFile:
        outfile = open(OutputFileName, 'w')
        outfile.write(json.dumps(results))
        outfile.close()
    else: # no else, something went wrong if this happens
        print("This wasn't supposed to happen, pass a valid output file name when rerunning this code.")
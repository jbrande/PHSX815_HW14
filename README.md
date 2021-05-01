# PHSX815_HW14

This homework generates some 2 dimensional data from a mixture model, and then runs K-means clustering to find the number of clusters in the data. Mixture.py makes some data, and Cluster.py runks k-means clustering to find the clusters.

Mixture.py can be run from the top directory as:
Usage: python/Mixture.py [-K integer] [-Npoints integer] [-output string]
-K:         (optional) the number of distributions to mix, if not given, default K=2. must be >= 1
-Npoints:   (optional) the number of points per distributions, if not given, default K=10. must be >= 1
-output:    (mandatory) the name of the output file to print to. must be given

Mixture.py will JSONify the results and print them to the top level directory in the given filename.

Cluster.py can be run from the top directory as:
Usage: python/Cluster.py [-input0 string] [-input1 string] [-Ndice int]
-input:      (mandatory) the name of the file which holds the mixture data
-K:                      (optional) the number of clusters to attempt to find in the data, default 2. must be >= 1

Cluster.py will iteratively run the algorithm, and save a plot of each step in the plots/ directory. Each Cluster is colored, the star point represents the current guessed cluster center, and the X point represents the centroid of the cluster, which is the guessed center for the next step. After each step, the points are reallocated to new clusters based on the centroids, and the algorithm repeats. The maximum number of iterations is currently 20.
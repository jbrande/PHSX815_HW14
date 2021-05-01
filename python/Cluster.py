# #! /usr/bin/env python

# imports of external packages to use in our code
import sys
import numpy as np
import re
import json

import matplotlib.pyplot as plt

# import our Random class from python/Random.py file
sys.path.append(".")
from python.Random import Random

# main function for our coin toss Python code
if __name__ == "__main__":
	# if no args passed (need at least the input file), dump the help message
	# if the user includes the flag -h or --help print the options
	if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) == 1:
		print ("Usage: %s [-input0 string] [-input1 string] [-Ndice int]" % sys.argv[0])
		print ("-input:      (mandatory) the name of the file which holds the mixture data")
		print ("-K:	 		 (optional) the number of clusters to attempt to find in the data, default 2. must be >= 1")
		print
		sys.exit(1)


	# number of clusters to try and find
	K = 2

	maxiter = 20 # maximum number of iterations to do before quitting

	# read the user-provided arguments from the command line (if there)
	if '-input' in sys.argv:
		p = sys.argv.index('-input')
		try:
			input0 = sys.argv[p+1]
		except IndexError as e:
			print("Must pass input filename")
	else:
		print("Must pass input filename")
	if '-K' in sys.argv:
		p = sys.argv.index('-K')
		K = int(sys.argv[p+1])
		if K < 1:
			print("K must be >= 1")
			sys.exit(1)


	# load json data from file
	res0 = ""
	with open(input0) as f:
		res0 = json.load(f)
		f.close()

	x = np.array(res0["x"])
	y = np.array(res0["y"])

	# get the number of points
	num_points = len(x)

	# keep track of how many iterations we're doing
	iteration = 0

	# need initial domain of data
	dmn = [[np.min(x), np.max(x)],[np.min(y), np.max(y)]]

	# get K initial uniformly random guesses
	means = np.random.uniform([dmn[0][0], dmn[1][0]], [dmn[0][1], dmn[1][1]], (K,2))

	# keep track of last guess to compare to, something outside of domain at first
	last = np.random.uniform([dmn[0][1], dmn[1][1]], [dmn[0][1] + 1, dmn[1][1] + 1], (K,2))

	# iteratively do K-means
	while iteration < maxiter:
		dists = []

		# find distances of all points to all guessed means
		for k in range(K):
			dist = np.sqrt((x - means[k][0])**2 + (y - means[k][1])**2)
			dists.append(np.array(dist))
		dists = np.array(dists)


		# keep track of the clusters 
		clusters = [ [[], []] for _ in range(K)] # K empty arrays to hold clusters

		# associate each point with its closest mean
		for i in range(num_points):
			ind = np.argmin(dists[:,i])
			clusters[ind][0].append(x[i])
			clusters[ind][1].append(y[i])


		# if any of the clusters are empty, quit. this happens sometimes when there are "too many" means for the number of points, or one guess is really bad and is far away
		# not sure how to handle this, so just die
		for k in range(K):
			if len(clusters[k][0]) == 0:
				print("empty cluster")
				sys.exit(1)

		# find centroids of clusters to see where to step to next
		centroids = []
		for k in range(K):
			cx = np.mean(clusters[k][0])
			cy = np.mean(clusters[k][1])
			centroids.append(np.array([cx, cy]))
		centroids = np.array(centroids)

		# plot a step
		fig = plt.figure(figsize=(5,5))
		for k in range(K):
			plt.plot(means[k][0], means[k][1], "*", markersize=10, c="C{}".format(k))
			plt.plot(centroids[k][0], centroids[k][1], "x", markersize=10, c="C{}".format(k))
			plt.plot(clusters[k][0], clusters[k][1], ".", markersize=2, c="C{}".format(k))
		plt.axis("equal")
		plt.xlabel("X")
		plt.ylabel("Y")
		plt.title("Iteration {}".format(iteration))
		fig.savefig("plots/iteration_{}.jpg".format(iteration), dpi=200)

		# check if new centroids are in the same place as the old means
		cdists = []
		for k in range(K):
			cdists.append(np.sqrt((centroids[k][0] - means[k][0])**2 + (centroids[k][1] - means[k][1])**2))

		# if the new cluster centroids and the old means are the same, stop iterating because we're done
		if np.array_equal(cdists, np.zeros(K)):
			break;

		# swap centers around for next iteration
		last = means
		means = centroids

		# increment iteration
		iteration = iteration + 1
#!/usr/bin/env python

import numpy as np

################################################
# Start input variables 
################################################

# Number of 
n_l = 7      # latent factors
n_i = 10     # items
n_a = 3      # artists
n_s = 2      # playlists
n_slots = 8  # slots

# latent factor vector for items
pi = np.array((n_i, n_l))

# latent factor vector for artists 
pa = np.array((n_a, n_l))

# latent factor vector for station s
vs = np.array((n_s, n_l))

# latent factor vector for station s at time slot k
vsk = np.array((n_s,n_slots,n_l)) #3D matrix

# bias for item i
ci = np.array((n_i))

# artist that has producted track i
ai = {} # simple hash table tid : aid

# slot time
slot = {}

# set of items played on station s, between t-w and t
pstw = {} # hash table of hash table of sets 

# set of songs,time played by station s
ps = {} # hash of set (of size 2)

# training of playlists
s = () # set of playlists

################################################
# End input variables 
################################################

# artist enhanced latent factors of the item
qi = lambda i: pi[i] + pa[ai[i]]

# artist enhanced bias: 
bi = lambda i: ci[i] + ci[ai[i]]

# affinity function
rsit = lambda s,i,t: bi(i) + np.transpose(qi(i)) * (vs[s] + vsk[s, slot[t]] + sum([qi(j) for j in pstw[s][t]])/math.sqrt(len(pstw[s][t])))

# probability that the item i will be played on station s at time t
pist = lambda i,s,t: math.exp(r(s,i,t)) / sum([math.exp(r(s,j,t)) for j,_t in ps[s]]) # TODO: Check the loop 

# probability to uniformly draw i in the training set (empirical frequency of i)
pis = {} # TODO: compute

# set of items uniformly drawn from the training set (with replacement)
I = () # TODO: compute

# weights
wist = lambda i,s,t: math.exp(r(s,i,t))/pis(i,s) / sum([math.exp(r(s,j,t))/pis(j,s) for j,_t in ps[s]]) # TODO: Check the loop 

# leaning rate
eta = lambda k: 0.005 / float(k)





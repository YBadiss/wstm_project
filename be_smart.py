#!/usr/bin/env python

import numpy as np
import init, inputs, helpers

################################################
# Start input variables 
################################################

# training of stationIds
S = inputs.S() # set of stationIds

# set of songs,time played by station s
ps = inputs.ps(S) # hash of set (of size 2)

# artist that has producted track i
ai = inputs.ai() # simple hash table tid : aid

# Number of 
n_l = 20      # latent factors
n_i = len(ai)     # items
n_a = len(set([artist for artist in ai.values()]))      # artists
n_s = len(S)      # playlists
n_slots = 8  # slots
w = 30*60    # time window 3O mins

################################################
# End input variables 
################################################

# latent factor vector for items
pi = init.pi(n_i, n_l)

# latent factor vector for artists 
pa = init.pa(n_a, n_l)

# latent factor vector for station s
vs = init.vs(n_s, n_l)

# latent factor vector for station s at time slot k
vsk = init.vsk(n_s,n_slots,n_l) #3D matrix

# bias for item i
ci = init.ci(n_i)

# bias for artist a
ca = init.ca(n_a)

# slot time
slot = helpers.slot

# set of items played on station s, between t-w and t
pstw = helpers.pstw(ps,w) # hash table of hash table of sets 

# artist enhanced latent factors of the item
qi = lambda i: pi[i] + pa[ai[i]]

# artist enhanced bias: 
bi = lambda i: ci[i] + ci[ai[i]]

# affinity function
rsit = lambda s,i,t: bi(i) + np.transpose(qi(i)) * (vs[s] + vsk[s, slot[t]] + sum([qi(j) for j in pstw[s][t]])/math.sqrt(len(pstw[s][t])))

# probability that the item i will be played on station s at time t
pist = lambda i,s,t: math.exp(r(s,i,t)) / sum([math.exp(r(s,track["id"],track["time"])) for track in ps[s]]) # TODO: Check the loop 

# probability to uniformly draw i in the training set (empirical frequency of i)
pis = init.pis(ps)

# weights
wist = lambda i,s,t: math.exp(r(s,i,t))/pis(i) / sum([math.exp(r(s,track["id"],track["time"]))/pis(track["id"]) for track in ps[s]]) # TODO: Check the loop 

# set of items uniformly drawn from the training set (with replacement)
I = () # TODO: compute
def update_I(I, r, s, i, t, pis):
  MAX_SIZE = 1000
  while len(I) < MAX_SIZE and sum([math.exp(r(s,j,t)) for j in I]) <= math.exp(r(s,i,y)):
    I.extend([helpers.uniform_sample_i(pis) for k in xrange(10)])

# leaning rate
eta = lambda k: 0.005 / float(k)

# differenciation
dr_pi = lambda s,i,t: (vs[s] + vsk[s, slot[t]] + sum([qi(j) for j in pstw[s][t]])/math.sqrt(len(pstw[s][t]))) + np.transpose(qi(i))*(1/math.sqrt(len(pstw[s][t])) if i in pstw[s][t] else 0)
dr_pa = lambda s,i,t: (vs[s] + vsk[s, slot[t]] + sum([qi(j) for j in pstw[s][t]])/math.sqrt(len(pstw[s][t]))) + np.transpose(qi(i))*(1/math.sqrt(len(pstw[s][t])) if i in pstw[s][t] else 0)
dr_vs = lambda s,i,t: np.transpose(qi(i))
dr_vsk = lambda s,i,t: np.transpose(qi(i))
dr_ci = lambda s,i,t: 1
dr_ca = lambda s,i,t: 1

delta_teta = lambda s,i,t,dr_teta,k: eta(k) * (dr_teta(s,i,t) - sum([wist(j,s,t) for j in I]) * dr_teta(s,i,t))

# learning
def doit():
  global S,I,ps,pi,dr_pi,pa,dr_pa,vs,dr_vs,vsk,dr_vsk,ci,dr_ci,ca,dr_ca
  STEP_CNT = 20
  for k in xrange(1, STEP_CNT + 1):
    update_I(I, r, s, i, t, pis)
    for s in S:
      for i,t in ps(s):
        for var, d in ((pi,dr_pi),
                      (pa,dr_pa),
                      (vs,dr_vs),
                      (vsk,dr_vsk),
                      (ci,dr_ci),
                      (ca,dr_ca)):
          var += delta_teta(s,i,t,d,k) # CORRECTION: the parameters are not EQUAL to detla_teta instead we add the delta to the original value


if __name__ == "__main__":
    doit()


#!/usr/bin/env python

import numpy as np
import init, inputs, helpers
import math
import sys, config
import time
import pdb

class Recommender:
  def __init__(self, n_l, n_slots, w):
    self.ai = inputs.ai() # simple hash table tid : aid
    # training of stationIds
    self.S = inputs.S() # set of stationIds
    # Id mapping dicts
    self.ids_to_item, self.item_to_ids = helpers.pack(self.ai.keys())
    self.ids_to_a, self.a_to_ids = helpers.pack(self.ai.values())
    self.ids_to_s, self.s_to_ids = helpers.pack(list(self.S))

    self.ai = inputs.adapt_ai(self.ai, self.a_to_ids, self.ids_to_item)
    self.S = inputs.adapt_S(self.S, self.s_to_ids)

    # set of songs,time played by station s
    self.ps = inputs.ps(self.S, self.item_to_ids, self.ids_to_s) # hash of set (of size 2)

    self.pis = init.pis(self.ps)

    self.I = np.array([])

    # Number of 
    self.n_l = n_l      # latent factors
    self.n_i = len(self.ai)     # items
    self.n_a = len(set(self.ai))      # artists
    self.n_s = len(self.S)      # playlists
    self.n_slots = n_slots  # slots
    self.w = w    # time window 3O mins

    # latent factor vector for items
    self.pi = init.pi(self.n_i, self.n_l)

    # latent factor vector for, ps artists 
    self.pa = init.pa(self.n_a, self.n_l)

    # latent factor vector for station s
    self.vs = init.vs(self.n_s, self.n_l)

    # latent factor vector for station s at time slot k
    self.vsk = init.vsk(self.n_s, self.n_slots, self.n_l) #3D matrix

    # bias for item i
    self.ci = init.ci(self.n_i)

    # bias for artist a
    self.ca = init.ca(self.n_a)

    # slot time
    self.slot = helpers.slot

    # set of items played on station s, between t-w and t
    self.pstw = helpers.pstw # hash table of hash table of sets
    self.pstw = helpers.memodict2(self.pstw, self.ps)


  def rsit(self, (s, i, t)):
    b = self.ci[i] + self.ca[self.ai[i]]
    term1 = self.pi[i] + self.pa[self.ai[i]]
    term2 = self.vs[s] + self.vsk[s, self.slot(t)] + (self.pi.take(self.pstw((s,t,self.w)), axis=0) + self.pa[self.ai.take(self.pstw((s,t,self.w)))]).sum()/np.sqrt(self.pstw((s,t,self.w)).size)
    return np.dot(term1 , term2)

  def wist(self, (I, i,s,t)):
    num = np.exp(self.rsit((s,i,t))) / helpers.getProba(self.pis,i)
    denom = sum([np.exp(self.rsit((s,tid,t))) / helpers.getProba(self.pis,tid) for tid in self.I])
    return num/denom

  def eta(self, k):
    return 0.005 / float(k)

  def dr_pi(self, s, i, t):
    term1 = self.vs[s] + self.vsk[s, self.slot(t)] + sum([self.pi[j] + self.pa[self.ai[j]] for j in self.pstw((s,t,self.w))]) / np.sqrt(self.pstw((s,t,self.w)).size)
    if i in self.pstw((s,t,self.w)):
      term2 = self.pi[i] + self.pa[self.ai[i]] / np.sqrt(self.pstw((s,t,self.w)).size)
      return term1 + term2
    else:
      return term1

  def dr_pa(self, s, i, t):
    return self.dr_pa(s,i,t)

  def dr_vs(self, s, i, t):
    return self.pi[i] + self.pa[self.ai[i]]

  def dr_vsk(self, s, i, t):
    return self.dr_vs(s,i,t)

  def dr_ci(self, s, i, t):
    return 1

  def dr_ca(self, s, i, t):
    return 1

  def delta_teta(self, s, i, t, dr_teta, k):
    return self.eta(k) * (dr_teta(s,i,t) - sum([self.wist((self.I, j,s,t)) * dr_teta(s,j,t) for j in self.I]))

  def update_I(self, s, i, t):
    MAX_SIZE = 1000
    if self.I.size < MAX_SIZE:
      sum_j = sum([np.exp(self.rsit((s,j,t))) for j in self.I])
      r_i = np.exp(self.rsit((s,i,t)))
      while (self.I.size < MAX_SIZE) and (sum_j <= r_i):
        new_j = np.array([helpers.uniform_sample_i(self.pis) for k in xrange(10)])
        sum_j += sum([np.exp(self.rsit((s,j,t))) for j in new_j])
        self.I = np.concatenate([self.I,new_j])

  def update(self, s, i, t, k):
    self.update_I(s,i,t)
    delta = [(var, self.delta_teta(s,i,t,d,k)) for var,d in (((self.pi,self.pa),self.dr_pi) , ((self.vs,self.vsk),self.dr_vs) , ((self.ci,self.ca),self.dr_ci))]
    [(np.clip(var1 + d,-1,1,var1), np.clip(var2 + d,-1,1,var2)) for ((var1,var2),d) in delta]



# learning
def doit(reco, step_cnt):
  for k in xrange(1, step_cnt + 1):
    print "Step %d"%(k) 
    for s in reco.S:
      st = time.time()
      print "\tStation %d"%(s)
      sys.stdout.flush()
      for i,t in zip(reco.ps[s]["tids"] , reco.ps[s]["times"]):
        reco.update(s,i,t,k)
      print time.time()-st
      return

if __name__ == "__main__":
  reco = Recommender(20, 8, 30*60)
  #reco.wist = helpers.memodict(reco.wist)
  reco.rsit = helpers.memodict(reco.rsit)
  doit(reco, 20)

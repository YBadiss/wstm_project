#!/usr/bin/env python

import numpy as np
import init, inputs, helpers
import math
import sys, config
import time, pdb
from random import random
import os

sys.setrecursionlimit(10000)

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

    self.I = np.array([], dtype=np.int32)

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
    self.time_slots , self.ps = helpers.get_time_slot(self.ps)


    # set of items played on station s, between t-w and t
    self.pstw = helpers.pstw # hash table of hash table of sets
    self.pstw = helpers.memodict2(self.pstw, self.ps)


  def rsit(self, (s, array_i, t)):
    term2 = self.getRsitTerm2((s,t))
    return (self.ci.take(array_i) + 
            self.ca.take(self.ai.take(array_i)) + 
            np.dot(self.pi.take(array_i, axis=0) + 
            self.pa.take(
              self.ai.take(array_i),axis=0),
              term2))

  def pstw_sum_base(self, (s, t)):
    return (self.pi.take(self.pstw((s,t,self.w)), axis=0).sum() + self.pa.take(self.ai.take(self.pstw((s,t,self.w))),axis=0).sum())/np.sqrt(self.pstw((s,t,self.w)).size)

  def getRsitTerm2(self, (s, t)):
    return self.vs[s] + self.vsk[s, self.time_slots[t]] + self.pstw_sum((s,t))

  def wist_base(self, (i,s,t)):
    num = np.exp(self.rsit((s,[i],t))) / self.pis['real'][i]
    denom = (np.exp(self.rsit((s,self.I,t))) / self.pis['real'].take(self.I)).sum()
    return num/denom

  def eta(self, k):
    return 0.005 / float(k)

  def dr_pi_base(self, (s, i, t)):
    return self.vs[s] + self.vsk[s, self.time_slots[t]] + self.pi[i] + self.pstw_sum((s,t))
    # term2 = self.pi[i] + self.pa[self.ai[i]] / np.sqrt(self.pstw((s,t,self.w)).size)
    # return term1 + term2

  def dr_pa_base(self, (s, i, t)):
    return self.vs[s] + self.vsk[s, self.time_slots[t]] + self.pa[self.ai[i]] + self.pstw_sum((s,t))
    # term2 = self.pi[i] + self.pa[self.ai[i]] / np.sqrt(self.pstw((s,t,self.w)).size)
    # return term1 + term2

  def dr_vs_base(self, (s, i, t)):
    return self.pi[i] + self.pa[self.ai[i]]

  def dr_vsk_base(self, (s, i, t)):
    return self.pi[i] + self.pa[self.ai[i]]

  def dr_ci(self, (s, i, t)):
    return 1

  def dr_ca(self, (s, i, t)):
    return 1

  def delta_teta(self, s, i, t, dr_teta, k):  
    return self.eta(k) * (dr_teta((s,i,t)) - sum([self.wist((j,s,t)) * dr_teta((s,j,t)) for j in self.I]))

  def update_I(self, s, i, t):
    MAX_SIZE = 100
    if self.I.size < MAX_SIZE:
      sum_j = 0
      if self.I.size > 0:
        sum_j = (np.exp(self.rsit((s,self.I,t)))).sum()
      r_i = np.exp(self.rsit((s,[i],t)))
      while (self.I.size < MAX_SIZE) and (sum_j <= r_i):
        new_j = np.array([self.pis['cumm'].searchsorted(random(), side='left') for k in xrange(10)])
        sum_j += (np.exp(self.rsit((s,new_j,t)))).sum()
        self.I = np.concatenate([self.I,new_j])

  def update(self, s, i, t, k):
    self.update_I(s,i,t)
    dpi = self.delta_teta(s,i,t,self.dr_pi,k)
    dpa = self.delta_teta(s,i,t,self.dr_pa,k)
    dvs = self.delta_teta(s,i,t,self.dr_vs,k)
    dvsk = self.delta_teta(s,i,t,self.dr_vsk,k)
    dci = self.delta_teta(s,i,t,self.dr_ci,k)
    dca = self.delta_teta(s,i,t,self.dr_ca,k)

    np.clip(self.pi[i] + dpi, -1, 1, self.pi[i])
    np.clip(self.pa[self.ai[i]] + dpa, -1, 1, self.pa[self.ai[i]])
    np.clip(self.vs[s] + dvs, -1, 1, self.vs[s])
    np.clip(self.vsk[s, self.time_slots[t]] + dvsk, -1, 1, self.vsk[s, self.time_slots[t]])
    self.ci[i] = min(max(self.ci[i] + dci,-1),1)
    self.ca[self.ai[i]] = min(max(self.ca[self.ai[i]] + dca,-1),1)

    # flush memoizatoin
    del self.wist
    del self.dr_pi
    del self.dr_pa
    del self.dr_vs
    del self.dr_vsk
    del self.getRsitTerm2
    del self.pstw_sum

    self.wist = helpers.memodict(self.wist_base)
    self.dr_pi = helpers.memodict(self.dr_pi_base)
    self.dr_pa = helpers.memodict(self.dr_pa_base)
    self.dr_vs = helpers.memodict(self.dr_vs_base)
    self.dr_vsk = helpers.memodict(self.dr_vsk_base)
    self.getRsitTerm2 = helpers.memodict(self.getRsitTerm2)
    self.pstw_sum = helpers.memodict(self.pstw_sum_base)

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
      print 'Size of I : %d'%(reco.I.size)
      # return

def first_call(step_cnt):
  reco = Recommender(20, 8, 30*60)
  reco.wist = helpers.memodict(reco.wist_base)
  reco.dr_pi = helpers.memodict(reco.dr_pi_base)
  reco.dr_pa = helpers.memodict(reco.dr_pa_base)
  reco.dr_vs = helpers.memodict(reco.dr_vs_base)
  reco.dr_vsk = helpers.memodict(reco.dr_vsk_base)
  reco.getRsitTerm2 = helpers.memodict(reco.getRsitTerm2)
  reco.pstw_sum = helpers.memodict(reco.pstw_sum_base)
  #reco.rsit = helpers.memodict(reco.rsit)
  doit(reco, step_cnt)
  save(reco) 

def save(reco):
  folder = './saved/%d/'%(time.time())
  os.makedirs(folder)
  np.save(folder+'wist',reco.pi)
  np.save(folder+'pa',reco.pa)
  np.save(folder+'vs',reco.vs)
  np.save(folder+'vsk',reco.vsk)
  np.save(folder+'ci',reco.ci)
  np.save(folder+'ca',reco.ca)
  np.save(folder+'ids_to_s',reco.ids_to_s)
  np.save(folder+'ids_to_item',reco.ids_to_item)
  np.save(folder+'ids_to_a',reco.ids_to_a)

if __name__ == "__main__":
  first_call(10)
  

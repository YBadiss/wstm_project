#!/usr/bin/env python
import numpy as np
from collections import Counter
import config

# Generate a matrix full of values uniformally distributed in [-1;1]
def random(*args):
  #cap = np.vectorize(lambda x: max(min(x,1),-1))
  #return cap(np.random.randn(*args))
  return np.clip(np.random.randn(*args).view('float64'),-1,1)

def pi(n_i,n_l):
  if config.DEBUG_MODE == True:
    return config.retrieve_store("tmp/pi", random(n_i,n_l))
  return random(n_i,n_l)

def pa(n_a, n_l):
  if config.DEBUG_MODE == True:
    return config.retrieve_store("tmp/pa", random(n_a, n_l))
  return random(n_a, n_l)

def vs(n_s, n_l):
  if config.DEBUG_MODE == True:
    return config.retrieve_store("tmp/vs", random(n_s, n_l))
  return random(n_s, n_l)

def vsk(n_s,n_slots,n_l):
  if config.DEBUG_MODE == True:
    return config.retrieve_store("tmp/vsk", random(n_s,n_slots,n_l))
  return random(n_s,n_slots,n_l)

def ci(n_i):
  if config.DEBUG_MODE == True:
    return config.retrieve_store("tmp/ci", random(n_i))
  return random(n_i)

def ca(n_a):
  if config.DEBUG_MODE == True:
    return config.retrieve_store("tmp/ca", random(n_a))
  return random(n_a)

def pis(ps):
  c = Counter()
  for l in ps.values():
    c += Counter(l['tids'])

  cnt = 0
  freqs = []
  #tids = []
  l = float(sum(c.values()))
  for i,n in sorted(c.items()):
    cnt += n
    freqs.append(cnt/l)
    #tids.append(i)
  return np.array(freqs, dtype=np.float64)


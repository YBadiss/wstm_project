#!/usr/bin/env python
import numpy as np
from collections import Counter

# Generate a matrix full of values uniformally distributed in [-1;1]
def random(*args):
  cap = np.vectorize(lambda x: max(min(x,1),-1))
  return cap(np.random.randn(*args))

def pi(n_i,n_l):
  return random(n_i,n_l)

def pa(n_a, n_l):
  return random(n_a, n_l)

def vs(n_s, n_l):
  return random(n_s, n_l)

def vsk(n_s,n_slots,n_l):
  return random(n_s,n_slots,n_l)

def ci(n_i):
  return random(n_i)

def ca(n_a):
  return random(n_a)

def pis(ps):
  c = Counter(reduce(list.__add__,[[i["tid"] for i in l] for l in ps.values()],[]))
  cnt = 0
  out = []
  l = sum(c.values())
  for i,n in sorted(c.items()):
    cnt += n
    out.append((cnt/float(l),i))
  return out


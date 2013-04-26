#!/usr/bin/env python

from bisect import bisect_left
from random import random
import numpy as np
import config, time

def slot(t):
  hour = time.gmtime(t).tm_hour
  return int(hour / 3.0)

def uniform_sample_i(pis):
	return pis.searchsorted(random(), side='left')

def getProba(pis, i):
	if i > 0:
		return pis[i] - pis[i-1]
	else:
		return pis[i]

# set of items played on station s, between t-w and t
def pstw(ps,(s,t,w)):
  start = ps[s]['times'].searchsorted(t-w, side='left')
  end = ps[s]['times'].searchsorted(t, side='right') + 1
  return ps[s]['tids'][start:end]

def pack(l):
  sl = sorted([int(e) for e in set(l)])
  dl = {}
  for i in xrange(len(sl)):
    dl[sl[i]] = i
  return sl,dl

def memodict2(f, ps):
  """ Memoization decorator for a function taking a single argument """
  class memodict(dict):
    def __missing__(self, key):
      ret = self[key] = f(ps, key)
      return ret
  return memodict().__getitem__

def memodict(f):
  """ Memoization decorator for a function taking a single argument """
  class memodict(dict):
    def __missing__(self, key):
      ret = self[key] = f(key)
      return ret
  return memodict().__getitem__

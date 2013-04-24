#!/usr/bin/env python

from bisect import bisect_left
from random import random
import time

def slot(t):
  hour = time.gmtime(t).tm_hour
  return int(hour / 3.0)

def uniform_sample_i(pis):
	frequencies = [f for f,_ in pis]
	return pis[min(bisect_left(frequencies, random()),len(pis)-1)][1]

# set of items played on station s, between t-w and t
def pstw(ps,t,w = 30*60):
  pstw = {}
  for s in ps:
    times = [track["time"] for track in ps[s]]
    start = bisect_left(times, t-w)
    end = bisect_left(times, t) + 1
    pstw[s] = ps[s][start : min(end , len(ps[s]))]
  return pstw

def pack(l):
  sl = sorted([int(e) for e in set(l)])
  dl = {}
  for i in xrange(len(sl)):
    dl[sl[i]] = i
  return sl,dl



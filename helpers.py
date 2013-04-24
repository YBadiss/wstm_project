#!/usr/bin/env python

def slot(t):
  hour = time.gmtime(t).tm_hour
  return int(hour / 3.0)

# set of songs,time played by station s
ps = inputs.ps(S) # hash of set (of size 2)

# set of items played on station s, between t-w and t
def pstw(ps,w):
  pstw = {}
  for s in ps:
    pstw[s] = {}


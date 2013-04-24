#!/usr/bin/env python

from bisect import bisect_left

def slot(t):
  hour = time.gmtime(t).tm_hour
  return int(hour / 3.0)

# set of items played on station s, between t-w and t
def pstw(ps,w,t):
  pstw = {}
  for s in ps:
    times = [track["time"] for track in ps[s]]
    start = bisect_left(times, t-w)
    end = bisect_left(times, t) + 1
    pstw[s] = ps[s][start : min(end , len(ps[s]))]
  return pstw


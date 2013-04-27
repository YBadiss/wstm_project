from be_smart import *
from heapq import *

NB_TRACKS = 10
NB_S = 2


r = Recommender(20, 8, 30*60)
#print r.pis['real']


master_heap = []
for s in xrange(len(r.ps)):
  s_heap = []
  for i in xrange(len(r.ps[s]['tids'])):
    track = r.ps[s]['tids'][i]
    freq = r.pis['real'][track]
    if len(s_heap) < NB_TRACKS:
      heappush(s_heap,(freq,i))
    else :
      heappushpop(s_heap, (freq,i))
  s_avg_f = sum([f for f,i in s_heap])/len(s_heap)
  if len(master_heap) < NB_S:
    heappush(master_heap, (s_avg_f,s,s_heap))
  else:
    heappushpop(master_heap, (s_avg_f,s,s_heap))
print master_heap
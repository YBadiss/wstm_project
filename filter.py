from be_smart import *
import inputs
from heapq import *
import json
import shutil
import os
import pdb

NB_TRACKS = 10
NB_S = 2

def loadJSON(filename):
  if os.path.exists(filename):
    with open(filename, "r") as fd:
      return json.loads(fd.read())
  return None

def clean_ai(path="./artists/"):
  ai = inputs.ai()
  S = inputs.S()
  tids = get_existing_tids(S)
  new_ai = {}
  ais_to_get = []

  for tid in tids:
    if tid in ai:
      new_ai[tid] = ai[tid]
    else:
      ais_to_get.append(tid)
  writeJSON(path+"artist_map.json", new_ai)
  writeJSON(path+"to_get.json", ais_to_get)

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

radios = {r.ids_to_s[s[1]]:[r.ids_to_item[t] for _,t in s[2]] for s in master_heap}
print radios

directory = './data_test/radios/'
with open(directory+"radios.json","w") as fd:
  fd.write(json.dumps([r for r in radios]))

pdb.set_trace()
for r in radios:
  #shutil.copytree('./radios/radio%d/'%(r),directory+'radio%d/'%(r))
  tracks = []
  for filename in os.listdir('./radios/radio%d/'%(r)):
    f_content = loadJSON('./radios/radio%d/'%(r) + filename) if filename.endswith(".json") else None
    if f_content:
      tracks.extend(f_content)
  
  os.makedirs(directory+'radio%d/'%(r))
  with open(directory + 'radio%d/tracks.json'%(r),'w') as fd:
    fd.write(json.dumps([track for track in tracks if track['tid'] in radios[r]]))

  clean_ai('./data_test/artists/')
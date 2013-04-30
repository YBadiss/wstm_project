from be_smart import *
from heapq import *
import json
import shutil
import os
import cleanArtists
import scrap
import pdb

# NB_TRACKS = 300
NB_S = 150

r = Recommender(20, 8, 30*60)
#print r.pis['real']

def clean_artists(S, tids):
  ai = inputs.loadJSON('./artists/artist_map.json')
  new_ai = {}
  ais_to_get = []

  for tid in tids:
    if str(tid) in ai:
      new_ai[str(tid)] = ai[str(tid)]
    else:
      ais_to_get.append(str(tid))
  cleanArtists.writeJSON("./data_test/artists/artist_map.json", new_ai)
  cleanArtists.writeJSON("./data_test/artists/to_get.json", ais_to_get)


master_heap = []
for s in r.ps:
  if len(master_heap) < NB_S:
    heappush(master_heap, (len(set(r.ps[s]['tids'])),s))
  else:
    heappushpop(master_heap, (len(set(r.ps[s]['tids'])),s))

  # for i in xrange(len(r.ps[s]['tids'])):
  #   track = r.ps[s]['tids'][i]
  #   freq = r.pis['real'][track]
  #   if len(s_heap) < NB_TRACKS:
  #     heappush(s_heap,(freq,track))
  #   else :
  #     heappushpop(s_heap, (freq,track))
  # s_avg_f = sum([f for f,i in s_heap])/len(s_heap)
  # if len(master_heap) < NB_S:
  #   heappush(master_heap, (s_avg_f,s,s_heap))
  # else:
  #   heappushpop(master_heap, (s_avg_f,s,s_heap))
pdb.set_trace()
arr = [int(r.ids_to_s[s]) for _,s in master_heap]
with open('./radios/radios.json', 'w') as fd:
  fd.write(json.dumps(arr))

cleanArtists.clean_ai()

# radios = {r.ids_to_s[s[1]]:[r.ids_to_item[t] for _,t in s[2]] for s in master_heap}
# print radios

# directory = './data_test/radios/'
# with open(directory+"radios.json","w") as fd:
#   fd.write(json.dumps([r for r in radios]))

tids = []
for r in radios:
  tracks = []
  for filename in os.listdir('./radios/radio%d/'%(r)):
    f_content = inputs.loadJSON('./radios/radio%d/'%(r) + filename) if filename.endswith(".json") else None
    if f_content:
      tracks.extend(f_content)
  os.makedirs(directory+'radio%d/'%(r))
  with open(directory + 'radio%d/tracks.json'%(r),'w') as fd:
    fd.write(json.dumps([track for track in tracks if track['tid'] in radios[r]]))
  tids.extend([t['tid'] for t in tracks])

# clean_artists([r for r in radios], tids)

# scrap.get_track_artists('./data_test/artists/to_get.json')
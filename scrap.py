#!/usr/bin/env python
from helper_tor import *

def doHit(url, max_try = 5):
  try_cnt = 0
  err = ""
  while try_cnt < max_try:
    try:
      try_cnt += 1
      hit = json.loads(urllib2.urlopen("http://api.deezer.com/2.0/" + url).read())
      if len(hit) == 0:
        err = "No content for " + url
      elif "error" in hit:
        err = hit["error"]["type"]
      else:
        return hit
    except:
      err = "urllib error"
  sys.stderr.write("\nError " + url + " : " + err)
  return None

def hit_user(u_id):
  hit = doHit("user/" + str(u_id) + "/playlists")
  if hit:
    return {u_id: sorted([playlist_meta["id"] for playlist_meta in hit["data"]])}
  else:
    return None

def hit_playlist(pid):
  hit = doHit("playlist/" + str(pid) + "/tracks")
  if hit:
    return {pid: sorted([track_meta["id"] for track_meta in hit["data"] if track_meta["type"] == "tack"])}
  else:
    return None
  
def hit_radios(r_id):
  hit = doHit("radio/" + str(r_id))
  if hit:
    return {r_id: {"title": hit["title"], "description": hit["description"]}} 
  else:
    return None

def hit_radio_tracks(r_id):
  if not needToHitRadio(r_id):
    return None
  start = int(time.time())
  hit = doHit("radio/" + str(r_id) + "/tracks")
  
  if hit:
    S_result = []
    a_result = {}
    total_time = 0
    for track in hit["data"]:
      S_result.append({"tid": track["id"], "time": start+total_time})
      a_result[track["id"]] = track["artist"]["id"]
      total_time += track["duration"]
    text_file = open(get_radio_file(r_id) , "w")
    text_file.write(json.dumps(S_result))
    text_file.close()
    updateNextHitRadio(r_id, total_time+start)
    return a_result
  else:
    return None


def parse_users():
  p = Pool(200)
  n = 0
  ROUND_CNT = 15000
  FILENAME = "users-p%d.json"
  try:
    while True:
      n += 1
      out = p.map(hit_user, xrange((n-1)*ROUND_CNT, n*ROUND_CNT))
      new_u = {}
      for o in out:
        if o != None:
          for u in o: 
            new_u[u] = o[u]
      text_file = open(FILENAME % n, "w")
      text_file.write(json.dumps(new_u))
      text_file.close()
      print time.asctime(time.localtime(time.time())),"- End round %d:" % (n)
      print "> %d new users" % (len(new_u))
      try:
        if TorConn.isTimeForNewId():
          TorConn.newTorId()
          print "> New IP: " + urllib2.urlopen("http://api.externalip.net/ip/").read()
        else:
          print "Keep same IP"
      except:
        pass
      sys.stdout.flush()
  except KeyboardInterrupt:
    print "End"


def get_playlists_ids():
  USERS_FILENAME = "users-p"
  user_file = [each for each in os.listdir(".") if each.startswith(USERS_FILENAME)]
  playlists = set([])
  for filename in user_file:
    with open(filename, 'r') as content_file:
      content = json.loads(content_file.read())
      for u in content:
        playlists |= set(content[u])
  return playlists


def parse_playlists():
  playlists = list(get_playlists_ids())
  print time.asctime(time.localtime(time.time())),"- Starting with %d playlists..." % (len(playlists))
  p = Pool(200)
  n = 16
  ROUND_CNT = 1000
  FILENAME = "playlists-p%d.json"
  try:
    while n*ROUND_CNT < len(playlists):
      n += 1
      out = p.map(hit_user, playlists[(n-1)*ROUND_CNT : min(n*ROUND_CNT, len(playlists))])
      new_u = {}
      for o in out:
        if o != None:
          for u in o: 
            new_u[u] = o[u]
      text_file = open(FILENAME % n, "w")
      text_file.write(json.dumps(new_u))
      text_file.close()
      print time.asctime(time.localtime(time.time())),"- End round %d:" % (n)
      print "> %d new playlists" % (len(new_u))
      try:
        if TorConn.isTimeForNewId():
          TorConn.newTorId()
          print "> New IP: " + urllib2.urlopen("http://api.externalip.net/ip/").read()
        else:
          print "Keep same IP"
      except:
        pass
      sys.stdout.flush()
  except KeyboardInterrupt:
    print "End"


def parse_radios(limit_radios):
  radios = range(1,limit_radios+1)
  print time.asctime(time.localtime(time.time())),"- Starting with %d radios..." % (len(radios))
  p = Pool(200)
  n = 0
  ROUND_CNT = 600
  FILENAME = "radios-p%d.json"
  try:
    while n*ROUND_CNT < len(radios):
      n += 1
      out = p.map(hit_radios, radios[(n-1)*ROUND_CNT : min(n*ROUND_CNT, len(radios))])
      new_u = {}
      for o in out:
        if o != None:
          for u in o: 
            new_u[u] = o[u]
      text_file = open(FILENAME % n, "w")
      text_file.write(json.dumps(new_u))
      text_file.close()
      print time.asctime(time.localtime(time.time())),"- End round %d:" % (n)
      print "> %d new radios" % (len(new_u))
      try:
        if TorConn.isTimeForNewId():
          TorConn.newTorId()
          print "> New IP: " + urllib2.urlopen("http://api.externalip.net/ip/").read()
        else:
          print "Keep same IP"
      except:
        pass
      sys.stdout.flush()
  except KeyboardInterrupt:
    print "End"


def get_radios():
  RADIOS_FILENAME = "radios-p"
  radio_files = [each for each in os.listdir(".") if each.startswith(RADIOS_FILENAME)]
  radios = []
  for filename in radio_files:
    with open(filename, 'r') as content_file:
      content = json.loads(content_file.read())
      radios += [int(r) for r in content]
  return radios


def get_radio_file(r_id):
  f = "./radios/radio%d/%s.json"%(r_id, time.strftime("%d_%H_%M_%S"))
  d = os.path.dirname(f)
  if not os.path.exists(d):
    os.makedirs(d)
  return f

def needToHitRadio(r_id):
  f = "./radios/radio%d/next_hit"%(r_id)
  if os.path.exists(f):
    with open(f, "r") as f:
      return int(f.read()) < int(time.time())
  return True

def updateNextHitRadio(r_id, next_time):
  f = "./radios/radio%d/next_hit"%(r_id)
  with open(f, "w") as f:
    f.write(str(int(next_time)))

def getSlot(t):
  hour = float(time.gmtime(t).tm_hour)
  return int(hour / 3.0)

def parse_tracks():
  #pdb.set_trace()
  radios = get_radios()
  print time.asctime(time.localtime(time.time())),"- Starting with %d radios..." % (len(radios))
  p = Pool(200)
  n = 0
  ROUND_CNT = 200
  FOLDERNAME = "radio%d"
  artist_map = readArtistMap()
  
  try:
    while n*ROUND_CNT < len(radios):
      n += 1
      out = p.map(hit_radio_tracks, radios[(n-1)*ROUND_CNT : min(n*ROUND_CNT, len(radios))])
      result = [e for e in out if e]
      print "%d radios actually hit."%(len(result))
      for r in result:
        artist_map.update(r)

      print time.asctime(time.localtime(time.time())),"- End round %d:" % (n)
      #pdb.set_trace()
      try:
        if TorConn.isTimeForNewId():
          TorConn.newTorId()
          print "> New IP: " + urllib2.urlopen("http://api.externalip.net/ip/").read()
        else:
          print "Keep same IP"
      except:
        pass
      sys.stdout.flush()
  except KeyboardInterrupt:
    print "End"
  writeArtistMap(artist_map)

def readArtistMap():
  f = "./artists/artist_map.json"
  if os.path.exists(f):
    with open(f, "r") as f:
      return json.loads(f.read())
  return {}

def writeArtistMap(a_map):
  f = "./artists/artist_map.json"
  d = os.path.dirname(f)
  if not os.path.exists(d):
    os.makedirs(d)
  with open(f, "w") as f:
    f.write(json.dumps(a_map))
  

if __name__ == "__main__":
  #parse_users()
  #parse_playlists()
  #parse_radios(60000)
  #hit_radio_tracks(6)
  parse_tracks()

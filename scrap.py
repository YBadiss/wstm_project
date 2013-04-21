#!/usr/bin/env python

import socks
import socket
from TorCtl import TorCtl
import time, sys, os, json 
from multiprocessing import Pool
import pdb

#pdb.set_trace();

class TorConnection:
  def __init__(self, waitTime):
    self.conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="test")
    self.lastChangeId = int(time.time())
    self.waitTime = waitTime

  def newTorId(self):
    TorCtl.Connection.send_signal(self.conn, "NEWNYM")
    self.lastChangeId = int(time.time())

  def isTimeForNewId(self):
    return (self.waitTime + self.lastChangeId) < time.time()


TorConn = TorConnection(60*5)

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection

# do not move up, needs to stand after the TOR code
import urllib2


def hit_user(u_id, try_cnt = 0):
  hit = ""
  try:
    hit = json.loads(urllib2.urlopen("http://api.deezer.com/2.0/user/" + str(u_id) + "/playlists").read())
    if len(hit) == 0:
      raise Exception("No Content from %d"%(u_id))
    if "error" in hit and hit["error"] != "DataException":
      raise Exception("Error from Deezer (on %d) - %s"%(u_id,hit["error"]))
  except Exception, e:
    if try_cnt > 20:
      sys.stderr.write("Could not get %d - %s"%(u_id,e))
      return "?" + str(u_id)
    return hit_user(try_cnt, try_cnt + 1)
  if "error" in hit or ("total" in hit and hit["total"] == 0) or "data" not in hit:
    return None
  return {u_id: sorted([playlist_meta["id"] for playlist_meta in hit["data"]])}

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


def hit_playlist(pid, try_cnt = 0):
  hit = ""
  try:
    hit = json.loads(urllib2.urlopen("http://api.deezer.com/2.0/playlist/" + str(pid) +"/tracks").read())
    if len(hit) == 0:
      raise Exception("No Content from %d"%(pid))
    if "error" in hit and hit["error"] != "DataException":
      raise Exception("Error from Deezer (on %d) - %s"%(pid,hit["error"]))
  except Exception, e:
    if try_cnt > 20:
      sys.stderr.write("Could not get %d - %s"%(pid,e))
      return "?" + str(pid)
    return hit_user(try_cnt, try_cnt + 1)
  if "error" in hit or ("total" in hit and hit["total"] == 0) or "data" not in hit:
    return None
  return {pid: sorted([track_meta["id"] for track_meta in hit["data"] if track_meta["type"] == "tack"])}


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


def hit_radios(r_id, try_cnt = 0):
  hit = ""
  try:
    hit = json.loads(urllib2.urlopen("http://api.deezer.com/2.0/radio/" + str(r_id)).read())
    if len(hit) == 0:
      raise Exception("No Content from %d"%(r_id))
    if "error" in hit and hit["error"]["type"] != "DataException":
      raise Exception("Error from Deezer (on %d) - %s"%(r_id,hit["error"]))
  except Exception, e:
    if try_cnt > 20:
      sys.stderr.write("Could not get %d - %s"%(r_id,e))
      return "?" + str(r_id)
    return hit_radios(try_cnt, try_cnt + 1)
  if "error" in hit:
    return None 
  return {r_id: {"title": hit["title"], "description": hit["description"]}} 


def hit_radios_simple():
  return json.loads(urllib2.urlopen("http://api.deezer.com/2.0/radio").read())
  

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
  f = "./radios/radio%d/%s"%(r_id, time.strftime("%d_%H_%M_%S"))
  d = os.path.dirname(f)
  if not os.path.exists(d):
    os.makedirs(d)
  return f

def do_hit_radio(r_id):
  f = "./radios/radio%d/next_hit"%(r_id)
  if os.path.exists(f):
    with open(f, "r") as f:
      return int(f.read()) < int(time.time())
  return True

def update_hit_radio_time(r_id, total_duration):
  f = "./radios/radio%d/next_hit"%(r_id)
  with open(f, "w") as f:
    f.write(str(int(time.time()) + total_duration))

def getSlot(t):
  hour = float(gmtime(t).tm_hour)
  return int(hour / 3.0)


def hit_radio_tracks(r_id, try_cnt = 0):
  if not do_hit_radio(r_id):
    return None
  hit = ""
  now = int(time.time())

  try:
    hit = json.loads(urllib2.urlopen("http://api.deezer.com/2.0/radio/" + str(r_id) + "/tracks").read())
    if len(hit) == 0:
      raise Exception("No Content from %d"%(r_id))
    if "error" in hit and hit["error"]["type"] != "DataException":
      raise Exception("Error from Deezer (on %d) - %s"%(r_id,hit["error"]))
  except Exception, e:
    if try_cnt > 20:
      sys.stderr.write("Could not get %d - %s"%(r_id,e))
      return None
    return hit_radio_tracks(try_cnt, try_cnt + 1)
  if "error" in hit:
    return None
  
  S_result = []
  a_result = {}
  total_time = 0
  for track in hit["data"]:
    S_result.append({"tid": track["id"], "duration": track["duration"], "slot": getSlot(now+total_time)})
    a_result[track["id"]] = track["artist"]["id"]
    total_time += track["duration"]
    
  text_file = open(get_radio_file(r_id) , "w")
  text_file.write(json.dumps(S_result))
  text_file.close()

  update_hit_radio_time(r_id, total_time)
  return a_result

 
def parse_tracks():
  pdb.set_trace()
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

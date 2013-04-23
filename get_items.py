#!/usr/bin/env python

from helper import *

def get_track_ids():
  directory = "./radios/"
  for root,dirs,files in os.walk(directory):
    for root,dirs,files in os.walk(dirs):
		for file in files:
       if file.endswith(".log") or file.endswith(".txt"):
           f=open(file, 'r')
           for line in f:
              if userstring in line:
                 print "file: " + os.path.join(root,file)             
                 break
           f.close()

def hit_track_info(t_id, try_cnt = 0):
  hit = ""
  try:
    hit = json.loads(urllib2.urlopen("http://api.deezer.com/2.0/track/" + str(t_id)).read())
    if len(hit) == 0:
      raise Exception("No Content from %d"%(u_id))
    if "error" in hit and hit["error"] != "DataException":
      raise Exception("Error from Deezer (on %d) - %s"%(t_id,hit["error"]))
  except Exception, e:
    if try_cnt > 20:
      sys.stderr.write("Could not get %d - %s"%(t_id,e))
      return None
    return hit_user(t_id, try_cnt + 1)
  if "error" in hit:
    return None
  return {'track': {'id': t_id, 'title': hit["title"], 'a_id': hit["artist"]["id"]}, 'artist': {'id': hit["artist"]["id"], 'name': hit["artist"]["name"]}};

def parse_tracks():
  p = Pool(200) 
  try:
    n += 1
    out = p.map(hit_track_info, )
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


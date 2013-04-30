#!/usr/bin/env python

import json
import os
import config
import numpy as np
import pdb

def ai():
  return loadJSON("./artists/artist_map.json")

def adapt_ai(ai, a_to_ids, ids_to_item):
  return np.array([a_to_ids[ai[str(item)]] for item in ids_to_item])

def S():
  TEST_RADIOS = [10, 16, 203, 264, 287]
  return TEST_RADIOS if config.DEBUG_MODE else loadJSON("./radios/radios.json")

def adapt_S(S, s_to_ids):
  return np.array([s_to_ids[s] for s in S])

def ps(S, item_to_ids, ids_to_s):
  ret_ps = {}
  directory = "./radios/radio%d/"
  no_artist = loadJSON('artists/to_get.json')
  for s in S:
    tids = []
    times = []

    for filename in os.listdir(directory%(ids_to_s[s])):
      f_content = loadJSON(directory%(ids_to_s[s]) + filename) if filename.endswith(".json") else None
      if f_content:
        tids.extend([item_to_ids[track["tid"]] for track in f_content if not str(track["tid"]) in no_artist])
        times.extend([track["time"] for track in f_content if not str(track["tid"]) in no_artist])

    np_tids = np.array(tids, np.int32)
    np_times = np.array(times, np.int32)
    indexer = np_times.argsort()
    np_times = np_times.take(indexer)
    np_tids = np_tids.take(indexer)

    ret_ps[s] = {"tids": np_tids, "times": np_times}
  pdb.set_trace()
  return ret_ps

def loadJSON(filename):
  if os.path.exists(filename):
    with open(filename, "r") as fd:
      return json.loads(fd.read())
  return None

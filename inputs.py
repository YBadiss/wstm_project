#!/usr/bin/env python

import json
import os
import pdb


def ai():
  return loadJSON("./artists/artist_map.json")

def adapt_ai(ai, item_to_ids, a_to_ids):
  return {item_to_ids[int(key)]: a_to_ids[ai[key]] for key in ai}

def S(test = True):
  TEST_RADIOS = [10, 16, 203, 264, 287]
  return TEST_RADIOS if test else loadJSON("./radios/radios.json")

def adapt_S(S, s_to_ids):
  return tuple(s_to_ids[s] for s in S)

def ps(S, item_to_ids, ids_to_s):
  ret_ps = {}
  directory = "./radios/radio%d/"
  for s in S:
    ret_ps[s] = []
    for filename in os.listdir(directory%(ids_to_s[s])):
      f_content = loadJSON(directory%(ids_to_s[s]) + filename) if filename.endswith(".json") else None
      if f_content:
        ret_ps[s].extend([{"tid": item_to_ids[track["tid"]], "time": track["time"]} for track in f_content])
  return ret_ps

def loadJSON(filename):
  if os.path.exists(filename):
    with open(filename, "r") as fd:
      return json.loads(fd.read())
  return None


def ps3(S):
  ret_ps = {}
  directory = "./radios/radio%d/"
  for s in S:
    ret_ps[s] = []
    for filename in os.listdir(directory%(s)):
      f_content = loadJSON(directory%(s) + filename) if filename.endswith(".json") else None
      if f_content:
        ret_ps[s].extend([{"tid": track["tid"], "time": track["time"]} for track in f_content])
  return ret_ps


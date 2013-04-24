#!/usr/bin/env python

import json
import os

def ai():
  return loadJSON("./artists/artist_map.json")

def S(test = True):
  TEST_RADIOS = [10, 16, 203, 264, 287]
  return TEST_RADIOS if test else loadJSON("./radios/radios.json")

def ps(S):
  ret_ps = {}
  directory = "./radios/radio%d/"
  for s in S:
    ret_ps[s] = []
    for filename in os.listdir(directory%(s)):
      f_content = loadJSON(filename) if filename.endswith(".json") else None
      if f_content:
        ret_ps[s].extend(f_content)
  return ret_ps

def pis(ps):
	

def loadJSON(filename):
  if os.path.exists(filename):
    with open(filename, "r") as fd:
      return json.loads(fd.read())
  return None


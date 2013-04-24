#!/usr/bin/env python

import json
import os

def getSlot(t):
  hour = time.gmtime(t).tm_hour
  return int(hour / 3.0)

def load_ai():
	return loadJSON("./artists/artist_map.json")

def load_S():
	return loadJSON("./radios/radios.json")

def load_ps(S):
	ret_ps = {}
	directory = "./radios/radio%d/"
	for s in S:
		ret_ps[s] = []
		for f in os.listdir(directory%(s)):
			f_content = loadJSON(f) if f.endswith(".json") else None
			ret_ps[s].extend(f_content if f_content else [])
	return ret_ps

def loadJSON(filename):
	if os.path.exists(filename):
		with open(filename, "r") as fd:
			return json.loads(fd.read())
	return None

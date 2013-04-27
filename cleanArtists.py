#!/usr/bin/env python

import json
import os
import inputs

def get_existing_tids(S):
  tids = []
  directory = "./radios/radio%d/"
  for s in S:
    for filename in os.listdir(directory%(s)):
      f_content = inputs.loadJSON(directory%(s) + filename) if filename.endswith(".json") else None
      if f_content:
        tids.extend([str(track["tid"]) for track in f_content])
  return tids

def clean_ai():
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
	writeJSON("./artists/artist_map.json", new_ai)
	writeJSON("./artists/to_get.json", ais_to_get)

def clean_S():
	S = inputs.S()
	directory = "./radios/radio%d/"
	writeJSON('./radios/radios.json', [s for s in S if os.path.exists(directory%(s))])

def writeJSON(filename, content):
  if os.path.exists(filename):
    with open(filename, "w") as fd:
      fd.write(json.dumps(content))
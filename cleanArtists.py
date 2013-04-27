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
	writeJSON("./artists/artist_map.json", {tid: ai[tid] for tid in tids})

def writeJSON(filename, content):
  if os.path.exists(filename):
    with open(filename, "w") as fd:
      fd.write(json.dumps(content))
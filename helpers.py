#!/usr/bin/env python

def getSlot(t):
  hour = time.gmtime(t).tm_hour
  return int(hour / 3.0)
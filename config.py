#!/usr/bin/env python

import numpy as np
import os.path

DEBUG_MODE = True

def retrieve_store(filename, value):
    if os.path.exists(filename):
      value = np.load(filename)
    else:
      np.save(filename,value)
    return value


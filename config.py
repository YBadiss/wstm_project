#!/usr/bin/env python

import numpy as np
import os.path

DEBUG_MODE = True

def retrieve_store(filename, value):
    if os.path.exists(filename+".npy"):
      value = np.load(filename+".npy")
    else:
      np.save(filename,value)
    return value


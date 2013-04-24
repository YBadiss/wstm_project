#!/usr/bin/env python
import numpy as np

# Generate a matrix full of values uniformally distributed in [-1;1]
def random(*args):
  return (2 * np.random.rand(*args)) - 1

def pi(n_i,n_l):
  return random(n_i,n_l)

def pa(n_a, n_l):
  return random(n_a, n_l)

def vs(n_s, n_l):
  return random(n_s, n_l)

def vsk(n_s,n_slots,n_l):
  return random(n_s,n_slots,n_l)

def ci(n_i):
  return random(n_i)

def ca(n_a):
  return random(n_a)


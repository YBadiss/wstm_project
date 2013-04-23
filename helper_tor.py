#!/usr/bin/env python

import socks
import socket
from TorCtl import TorCtl
import time, sys, os, json
from multiprocessing import Pool
import pdb

#pdb.set_trace();

class TorConnection:
  def __init__(self, waitTime):
    self.conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="test")
    self.lastChangeId = int(time.time())
    self.waitTime = waitTime

  def newTorId(self):
    TorCtl.Connection.send_signal(self.conn, "NEWNYM")
    self.lastChangeId = int(time.time())

  def isTimeForNewId(self):
    return (self.waitTime + self.lastChangeId) < time.time()


# TorConn = TorConnection(0)

# def create_connection(address, timeout=None, source_address=None):
#     sock = socks.socksocket()
#     sock.connect(address)
#     return sock

# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

# # patch the socket module
# socket.socket = socks.socksocket
# socket.create_connection = create_connection

# do not move up, needs to stand after the TOR code
import urllib2


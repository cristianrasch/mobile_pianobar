#!/usr/bin/env python

import android
import re
import types
from socket import *

class Client(object):
  host = '192.168.0.15'
  port = 12345
  buf_size = 4096
  addr = (host, port)
  
  def __init__(self):
    self.droid = android.Android()
    self.tcpCliSock = socket(AF_INET, SOCK_STREAM)
    self.tcpCliSock.connect(self.addr)
    self.regex = re.compile(r'"(.+?)" by "(.+?)" on "(.+?)"')
  
  def __del__(self):
    self.tcpCliSock.close()
    
  def parse(self, data):
    match = re.search(self.regex, data)
    return match.groups() if match else data
    
  def read(self):
    how_many = int(self.tcpCliSock.recv(4))
    data = self.tcpCliSock.recv(how_many)
    parsed_data = self.parse(data)
    if type(parsed_data) is types.TupleType:
      song, band, album = parsed_data
      self.droid.notify('Info', song+'\nby '+band+'\non '+album)
    else:
      self.droid.notify('Alert', data)
    
  def run(self):
    self.read()
    while True:
      data = raw_input('> ')
      if not data: break
      self.tcpCliSock.send(data)
      self.read()

if __name__ == '__main__':
  client = Client()
  client.run()

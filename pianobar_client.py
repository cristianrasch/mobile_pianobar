#!/usr/bin/env python

import android
import re
import types
from socket import *

class Client(object):
  host = '192.168.0.15'
  port = 12345
  
  def __init__(self):
    self.droid = android.Android()
    self.ip_regex = re.compile(r'\A\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\Z')
    self.track_regex = re.compile(r'"(.+?)" by "(.+?)" on "(.+?)"')
    self._config()
  
  def run(self):
    while True:
      data = raw_input('> ')
      # data = self.droid.dialogGetInput('pianobar', 'command').result
      if not data: break
      self.tcpCliSock.send(data)
      self._read()
  
  def _config(self):
    ip = self.droid.dialogGetInput('Server', 'IP address', self.host).result
    self.serverip = ip if re.match(self.ip_regex, ip) else self.host
    self.tcpCliSock = socket(AF_INET, SOCK_STREAM)
    self.tcpCliSock.connect((self.serverip, self.port))
  
  def _parse(self, data):
    match = re.search(self.track_regex, data)
    return match.groups() if match else data
    
  def _read(self):
    how_many = int(self.tcpCliSock.recv(4))
    data = self.tcpCliSock.recv(how_many)
    parsed_data = self._parse(data)
    if type(parsed_data) is types.TupleType:
      song, band, album = parsed_data
      self.droid.notify('Info', song+'\nby '+band+'\non '+album)
    else:
        self.droid.dialogCreateAlert('Info', parsed_data)
        self.droid.dialogSetPositiveButtonText('Continue')
        self.droid.dialogShow()
    
  def __del__(self):
    self.tcpCliSock.close()
  
if __name__ == '__main__':
  client = Client()
  client.run()

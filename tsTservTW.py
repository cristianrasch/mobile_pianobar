#!/usr/bin/env python

from twisted.internet import protocol, reactor
from time import ctime
from string import rjust
from pianobar import Wrapper

PORT = 12345

class TSServProtocol(protocol.Protocol):
  def connectionMade(self):
    self.clnt = self.transport.getPeer().host
    print '...connected from:', self.clnt
    self.pianobar = Wrapper()
    self._sendReponse(self.pianobar.run())
  
  def dataReceived(self, data):
    response = self.pianobar.execute(data)
    self._sendReponse(response)
  
  def _wrapData(self, data):
    length = str(len(data))
    size = rjust(length, 4, '0')
    # print 'size:', size
    return size+data

  def _sendReponse(self, response):
    res = '\n'.join(response)
    # print repr(res)
    wrapped_data = self._wrapData(res)
    self.transport.write(wrapped_data)

if __name__ == '__main__':
  factory = protocol.Factory()
  factory.protocol = TSServProtocol
  print 'waiting for connection...'
  reactor.listenTCP(PORT, factory)
  reactor.run()

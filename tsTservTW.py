#!/usr/bin/env python

from twisted.internet import protocol, reactor
from time import ctime
from string import rjust
from pianobar import Wrapper

PORT = 12345

class TSServProtocol(protocol.Protocol):
  def wrapData(self, data):
    size = rjust(str(len(data)), 4, '0')
    # print 'size:', size
    return size+data

  def sendReponse(self, response):
    res = '\n'.join(response)
    # print res
    self.transport.write(self.wrapData(res))
  
  def connectionMade(self):
    clnt = self.clnt = self.transport.getPeer().host
    print '...connected from:', clnt
    self.pianobar = Wrapper()
    self.sendReponse(self.pianobar.run())
  
  def dataReceived(self, data):
    response = self.pianobar.execute(data)
    self.sendReponse(response)

factory = protocol.Factory()
factory.protocol = TSServProtocol
print 'waiting for connection...'
reactor.listenTCP(PORT, factory)
reactor.run()


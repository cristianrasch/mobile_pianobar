#!/usr/bin/env python

from twisted.internet import protocol, reactor
from time import ctime
from pianobar import Wrapper

PORT = 12345

class TSServProtocol(protocol.Protocol):
  def connectionMade(self):
    clnt = self.clnt = self.transport.getPeer().host
    print '...connected from:', clnt
    self.pianobar = Wrapper()
    current_track = self.pianobar.run()
    print current_track
    self.transport.write(current_track)
  
  def dataReceived(self, data):
    response = self.pianobar.execute(data)
    self.transport.write('\n'.join(response))

factory = protocol.Factory()
factory.protocol = TSServProtocol
print 'waiting for connection...'
reactor.listenTCP(PORT, factory)
reactor.run()


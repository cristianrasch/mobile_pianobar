#!/usr/bin/env python
from twisted.internet import protocol, reactor

HOST = 'localhost'
PORT = 12345

class TSClntProtocol(protocol.Protocol):
  def sendData(self):
    data = raw_input('> ')
    if data:
      print '...sending %s...' % data
      self.transport.write(data)
    else:
      self.transport.loseConnection()

  # def connectionMade(self):
  #   self.sendData()

  def dataReceived(self, data):
    print data[4:]
    self.sendData()

class TSClntFactory(protocol.ClientFactory):
  protocol = TSClntProtocol
  clientConnectionLost = clientConnectionFailed = \
    lambda self, connector, reason: reactor.stop()

if __name__ == '__main__':
  reactor.connectTCP(HOST, PORT, TSClntFactory())
  reactor.run()

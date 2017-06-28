#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan

from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("Hello world!")

    def dataReceived(self, data):
        print "Server said:{}".format(data)
        self.transport.loseConnection()


class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed, reason:{}".format(reason)
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost, reason:{}".format(reason)
        reactor.stop()


reactor.connectTCP("localhost", 8080, EchoFactory())
reactor.run()

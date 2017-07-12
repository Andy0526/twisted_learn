#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan
from twisted.internet import protocol, reactor
from twisted.internet.protocol import connectionDone, Factory


class QuoteProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numConnections += 1

    def dataReceived(self, data):
        print "Number of active connections: ".format(self.factory.numConnections)
        print "> Received: {}\n> Sending: {}".format(data, self.getQuote())
        self.transport.write(self.getQuote())

    def getQuote(self):
        return self.factory.quote

    def connectionLost(self, reason=connectionDone):
        self.factory.numConnections += -1

    def updateQuote(self, quote):
        self.factory.quote = quote


class QuoteFactory(Factory):
    numConnections = 0

    def __init__(self, quote=None):
        self.quote = quote or "An apple a day keeps the doctor away"

    def buildProtocol(self, addr):
        return QuoteProtocol(self)


if __name__ == '__main__':
    reactor.listenTCP(8080, QuoteFactory())
    reactor.run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan
from twisted.internet import reactor
from twisted.internet.protocol import connectionDone, Factory
from twisted.protocols.basic import LineReceiver


class CharProtocol(LineReceiver):
    class USER_STATE(object):
        DEFAULT = 'REGISTER'
        CHAT = 'CHAT'

    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = self.USER_STATE.DEFAULT

    def connectionMade(self):
        self.sendLine("What's your name?")

    def connectionLost(self, reason=connectionDone):
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.broadcastMessage("{} has left the channel.".format(self.name))

    def lineReceived(self, line):
        if self.state == self.USER_STATE.DEFAULT:
            self.handle_REGISTER(line)
        else:
            self.handle_CHAT(line)

    def handle_REGISTER(self, name):
        if name in self.factory.users:
            self.sendLine("Name token, please choose anthoer.")
            return
        self.sendLine("Welcome, {}".format(name))
        self.broadcastMessage('{} has joined the channel.'.format(name))
        self.name = name
        self.factory.users[name] = self
        self.state = self.USER_STATE.CHAT

    def handle_CHAT(self, message):
        message = "<{}> {}".format(self.name, message)
        self.broadcastMessage(message)

    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return CharProtocol(self)


if __name__ == '__main__':
    reactor.listenTCP(8000, ChatFactory())
    reactor.run()

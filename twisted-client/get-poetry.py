#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan
import traceback

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, connectionDone

import optparse
import time


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...

This is the Get Poetry Now! client, Twisted version 2.0.
Run it like this:

  python get-poetry.py port1 port2 port3 ...

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python twisted-client-2/get-poetry.py 10001 10002 10003

to grab poetry from servers on ports 10001, 10002, and 10003.

Of course, there need to be servers listening on those ports
for that to work.
"""

    parser = optparse.OptionParser(usage)

    _, addresses = parser.parse_args()

    if not addresses:
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers.')

        return host, int(port)

    return map(parse_address, addresses)


class PoetryProtocol(Protocol):
    poem = ''
    task_no = 0
    first_call = True

    def dataReceived(self, data):
        if self.first_call:
            traceback.print_exc()
        self.first_call = False
        self.poem += data
        msg = 'Task {}: got {} bytes of poetry from {}'.format(self.task_no, len(data), self.transport.getPeer())
        print msg

    def connectionLost(self, reason=connectionDone):
        self.poemReceived(self.poem)

    def poemReceived(self, poem):
        self.factory.poem_finished(self.task_no, poem)


class PoetryClientFactory(ClientFactory):
    protocol = PoetryProtocol
    task_num = 1
    first_call = True

    def __init__(self, poetry_count):
        self.poetry_count = poetry_count
        self.poems = {}

    def buildProtocol(self, addr):
        if self.first_call:
            traceback.print_exc()
        self.first_call = False
        protocol_obj = ClientFactory.buildProtocol(addr)
        protocol_obj.task_no = self.task_num
        self.task_num += 1
        return protocol_obj

    def poem_finished(self, poem_no=None, poem=None):
        if poem_no:
            self.poems[poem_no] = poem
        self.poetry_count -= 1
        if self.poetry_count <= 0:
            self.report()
            reactor.stop()

    def report(self):
        for poem_no, poem in self.poems.iteritems():
            print 'Task {}: {} bytes of poetry, \ncontent:{}'.format(poem_no, len(poem), poem)

    def clientConnectionFailed(self, connector, reason):
        print 'Failed to connect to:{}'.format(connector.getDestination())
        self.poem_finished()


def poetry_main():
    addresses = parse_args()
    start = time.time()
    factory = PoetryClientFactory(len(addresses))
    for address in addresses:
        host, port = address
        reactor.connectTCP(host, port, factory)
    reactor.run()
    print 'Got {} poems, runtime:{}'.format(len(addresses), time.time - start)


if __name__ == '__main__':
    poetry_main()

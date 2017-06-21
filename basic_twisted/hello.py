#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan

from twisted.internet import reactor
import traceback


def hello():
    traceback.print_stack()
    print 'Hello from the reactor loop!'
    print 'Lately I feel like I\'m stuck in a rut.'


print type(reactor), reactor

reactor.callWhenRunning(hello)
print 'Starting the reactor'
reactor.run()

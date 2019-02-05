#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan
import logging

from twisted.web import server, resource
from twisted.internet import reactor


class Simple(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        import traceback
        logging.info(traceback.format_exc())
        print traceback.print_exc()
        return "<html>Hello, world!</html>"


site = server.Site(Simple())
reactor.listenTCP(8080, site)
reactor.run()

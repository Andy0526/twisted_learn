# -*- coding: utf-8 -*-

from twisted.internet import reactor
from twisted.web import server
from txrestapi.resource import APIResource
from txrestapi.methods import GET, POST, PUT, ALL


class MyResource(APIResource):

    @GET("/path1")
    def path1(self, request):
        return "path1"

    @POST("/path2")
    def path2(self, request):
        return "path2"

    @PUT("/path3")
    def path3(self, request):
        print request.args
        return "path3"

    @ALL("/")
    def default(self, request):
        return "default route"


if __name__ == "__main__":
    site = server.Site(MyResource())
    reactor.listenTCP(8080, site)
    reactor.run()

from twisted.web import server, resource
from twisted.internet import reactor


class Simple(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        self.putChild("", self)

    def render_GET(self, request):
        return "Hello, world!"

    def render_PUT(self, request):
        print request.content.getvalue()
        return "put done"


reactor.listenTCP(8080, server.Site(Simple()))
reactor.run()

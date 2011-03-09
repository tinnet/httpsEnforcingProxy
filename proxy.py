#!/usr/bin/env python

from twisted.web import proxy, http
from twisted.internet import reactor
from twisted.python import log
import sys
import re

# rules from https://gitweb.torproject.org/https-everywhere.git/tree/HEAD:/src/chrome/content/rules
RE1FROM = r"^http://(www\.)?twitter\.com/"
RE1TO = r"https://twitter.com/"


class BouncingProxyRequest(proxy.ProxyRequest):
    def process(self):
	print self.received_headers
        print self.requestHeaders
	print self.uri
        
        if re.match(RE1FROM, self.uri):
            self.redirect(re.sub(RE1FROM, RE1TO, self.uri))
	    self.finish()
        else:
            return proxy.ProxyRequest.process(self)

class BouncingProxy(proxy.Proxy):
    def __init__(self):
        self.requestFactory = BouncingProxyRequest
        proxy.Proxy.__init__(self)

log.startLogging(sys.stdout)

f = http.HTTPFactory()
f.protocol = BouncingProxy

reactor.listenTCP(8080,f)
reactor.run()

#!/usr/bin/env python

import sys
sys.path.extend(['lib', '../lib'])

from twisted.internet import reactor

import longurl

def cb(s):
    print "Title: %s" % s.title.encode('utf-8')
    print s.url.encode('utf-8')
    reactor.stop()

def go(u):
    lu = longurl.LongUrl()
    lu.expand(u).addCallback(cb)

reactor.callWhenRunning(go, sys.argv[1])
reactor.run()

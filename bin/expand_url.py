#!/usr/bin/env python

import sys
sys.path.extend(['lib', '../lib'])

from twisted.internet import reactor

import longurl

def cb(s):
    print s
    reactor.stop()

def go(u):
    lu = longurl.LongUrl()
    lu.expand(u).addCallback(cb)

reactor.callWhenRunning(go, sys.argv[1])
reactor.run()

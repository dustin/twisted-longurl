#!/usr/bin/env python

import sys
sys.path.extend(['lib', '../lib'])

from twisted.internet import reactor

import longurl

def cb(s):
    print s
    reactor.stop()

def go():
    lu = longurl.LongUrl()
    lu.getServices().addCallback(cb)

reactor.callWhenRunning(go)
reactor.run()

#!/usr/bin/env python

from __future__ import with_statement

import sys
import xml

from twisted.trial import unittest
from twisted.internet import defer
from twisted.web import error

sys.path.extend(['lib', '../lib'])
import longurl

class ParsingTest(unittest.TestCase):

    def __parse(self, fn, parser):
        with open("../" + fn) as f:
            return parser(f.read())

    def testServiceList(self):
        s = self.__parse("services.xml", longurl.Services)
        self.assertEquals(109, len(s))
        self.assertEquals('snipurl.com', s['snipurl.com'].name)
        urls = set(['snipurl.com', 'snurl.com', 'snipr.com', 'sn.im'])
        self.assertEquals(urls, set(s['snipurl.com'].domains))
        # Just verifies the repr produces something.
        self.assertTrue(repr(s))

class FakeHTTP(object):

    def __init__(self):
        self.d = defer.Deferred()
        self.rv = defer.Deferred()

    def getPage(self, *args, **kwargs):
        return self.d

def load_data(fn):
    with open("../" + fn) as f:
        return f.read()

class ServiceRequestTest(unittest.TestCase):

    def testGarbageResponse(self):
        fh = FakeHTTP()
        lu = longurl.LongUrl(client=fh)
        d = lu.getServices()
        d.addCallback(lambda x: self.fail("boo"))
        d.addErrback(lambda e: self.assertTrue(e.type == xml.parsers.expat.ExpatError))
        fh.d.callback("<not><html>")

    def testFailedRequest(self):
        fh = FakeHTTP()
        lu = longurl.LongUrl(client=fh)
        d = lu.getServices()
        d.addCallback(lambda x: self.fail("boo"))
        d.addErrback(lambda e: self.assertTrue(e.type == RuntimeError))
        fh.d.errback(RuntimeError("Blah"))

    def testOKRequest(self):
        fh = FakeHTTP()
        lu = longurl.LongUrl(client=fh)
        d = lu.getServices()
        def checkResult(s):
            self.assertEquals(109, len(s))
            self.assertEquals('snipurl.com', s['snipurl.com'].name)
            urls = set(['snipurl.com', 'snurl.com', 'snipr.com', 'sn.im'])
            self.assertEquals(urls, set(s['snipurl.com'].domains))

        d.addCallback(checkResult)
        d.addErrback(lambda e: self.fail(str(e)))
        fh.d.callback(load_data("services.xml"))

class ExpansionRequestTest(unittest.TestCase):

    def testFailedRequest(self):
        fh = FakeHTTP()
        lu = longurl.LongUrl(client=fh)
        d = lu.expand('http://whatever/')
        d.addCallback(lambda s: self.assertEquals('http://whatever/', s.url))
        d.addErrback(lambda e: self.fail("should not fail."))
        fh.d.errback(RuntimeError('Blah'))

    def testRedirection(self):
        fh = FakeHTTP()
        lu = longurl.LongUrl(client=fh)
        d = lu.expand('http://whatever/')
        def checkResults(s):
            self.assertEquals('http://www.spy.net/', s.url)
        d.addCallback(checkResults)
        fh.d.errback(error.PageRedirect("307", location="http://www.spy.net/"))

    def test200(self):
        fh = FakeHTTP()
        lu = longurl.LongUrl(client=fh)
        d = lu.expand('http://www.google.com/')
        def checkResults(s):
            self.assertEquals('http://www.google.com/', s.url)
        d.addCallback(checkResults)
        fh.d.callback("Good!")

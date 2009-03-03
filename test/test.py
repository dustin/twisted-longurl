#!/usr/bin/env python

from __future__ import with_statement

import sys
from twisted.trial import unittest

sys.path.extend(['lib', '../lib'])
import longurl

class ParsingTest(unittest.TestCase):

    def __parse(self, fn, parser):
        with open(fn) as f:
            return parser(f.read())

    def testServiceList(self):
        s = self.__parse("../test/services.xml", longurl.Services)
        self.assertEquals(109, len(s))
        self.assertEquals('snipurl.com', s['snipurl.com'].name)
        urls = set(['snipurl.com', 'snurl.com', 'snipr.com', 'sn.im'])
        self.assertEquals(urls, set(s['snipurl.com'].domains))

    def testExpandedURL(self):
        s = self.__parse("../test/expand.xml", longurl.ExpandedURL)
        self.assertEquals('Invalid Item', s.title)
        self.assertEquals('http://cgi.ebay.com/aw-cgi/eBayISAPI.dll?ViewItem&item=1698262135',
                          s.url)


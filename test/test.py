#!/usr/bin/env python

from __future__ import with_statement

import sys
import unittest

sys.path.extend(['lib', '../lib'])
import longurl

class ParsingTest(unittest.TestCase):

    def __parse(self, fn, parser):
        with open(fn) as f:
            return parser(f.read())

    def testServiceList(self):
        s = self.__parse("test/services.xml", longurl.Services)
        self.assertEquals(109, len(s))
        self.assertEquals('snipurl.com', s['snipurl.com'].name)
        urls = set(['snipurl.com', 'snurl.com', 'snipr.com', 'sn.im'])
        self.assertEquals(urls, set(s['snipurl.com'].domains))

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python

from __future__ import with_statement

import sys
import unittest

sys.path.extend(['lib', '../lib'])
import longurl

class ParsingTest(unittest.TestCase):

    def testServiceList(self):
        with open("test/services.xml") as f:
            s = longurl.Services(f.read())
            self.assertEquals(109, len(s))
            self.assertEquals('snipurl.com', s['snipurl.com'].name)
            urls = set(['snipurl.com', 'snurl.com', 'snipr.com', 'sn.im'])
            self.assertEquals(urls, set(s['snipurl.com'].domains))

if __name__ == '__main__':
    unittest.main()

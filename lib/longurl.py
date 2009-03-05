import urllib
import xml.dom.minidom

from twisted.internet import defer
from twisted.web import client

BASE_URL = "http://api.longurl.org/v1/"

class ResponseFailure(Exception):
    pass

class Service(object):
    "An individual service handled by longurl."

    def __init__(self, el):
        self.name = el.getElementsByTagName('name')[0].firstChild.data
        self.domains = []

        for d in el.getElementsByTagName('domain'):
            self.domains.append(d.firstChild.data)

    def __repr__(self):
        return "<Service name=%s, doms=%s>>" % (self.name, str(self.domains))

class Services(dict):
    "List of services handled by longurl"

    def __init__(self, content):
        document=xml.dom.minidom.parseString(content)
        assert document.firstChild.nodeName == "response"
        for r in document.getElementsByTagName('service'):
            s=Service(r)
            self[s.name] = s

class ExpandedURL(object):

    def __init__(self, content):
        document=xml.dom.minidom.parseString(content)
        assert document.firstChild.nodeName == "response"
        errMsgs = document.getElementsByTagName('messages')
        if errMsgs:
            raise ResponseFailure(errMsgs[0].firstChild.data)
        try:
            self.title = document.getElementsByTagName('title')[0].firstChild.data
        except IndexError:
            self.title = None
        self.url = document.getElementsByTagName('long_url')[0].firstChild.data

    def __repr__(self):
        return "<<ExpandedURL title=%s url=%s>>" % (self.title, self.url)

class LongUrl(object):

    def __init__(self, agent='twisted-longurl', client=client):
        self.agent = agent
        self.client = client

    def getServices(self):
        """Get a dict of known services.

        Key is service name, value is a Service object."""

        rv = defer.Deferred()
        d = self.client.getPage(BASE_URL + 'services', agent=self.agent)
        d.addCallback(lambda res: rv.callback(Services(res)))
        d.addErrback(lambda e: rv.errback(e))

        return rv

    def expand(self, u):
        """Expand a URL."""

        rv = defer.Deferred()
        d = self.client.getPage(BASE_URL + 'expand?url=' + urllib.quote(u),
                                agent=self.agent)
        d.addCallback(lambda res: rv.callback(ExpandedURL(res)))
        d.addErrback(lambda e: rv.errback(e))

        return rv

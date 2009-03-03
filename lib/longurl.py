import xml.dom.minidom

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
        self.title = document.getElementsByTagName('title')[0].firstChild.data
        self.url = document.getElementsByTagName('long_url')[0].firstChild.data

    def __repr__(self):
        return "<<ExpandedURL title=%s url=%s>>" % (self.title, self.url)


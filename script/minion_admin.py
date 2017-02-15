import urllib2
from urllib import urlencode

SERVER = 'control2.ops.ymatou.cn'
TOKEN = 'e1bb21fd6a07de88b87fee35fc730cdab76e896d'


class SaltHelper(object):
    server = SERVER

    def __init__(self, master, host, token=TOKEN):
        self.data = {"master": master, "minion": host}
        self.content_type = "application/x-www-form-urlencoded"
        self.auth_header = {"Authorization": "Token %s" % str(token), "Content-Type": self.content_type}

    def _req(self, path):
        content = urlencode(self.data)
        print content
        req = urllib2.Request(path, content, self.auth_header)
        result = urllib2.urlopen(req)
        result_content = result.read()
        print result_content
        return result_content

    def init_minion(self):
        return self._req('http://%s%s' % (self.server, '/salt/minion/init'))

    def accept_minion(self):
        return self._req('http://%s%s' % (self.server, '/salt/key/accept'))

    def delete_minion(self):
        return self._req('http://%s%s' % (self.server, '/salt/key/delete'))

    def run(self):
        return self.accept_minion(), self.init_minion()

    def reinstall(self):
        return self.delete_minion(), self.accept_minion(), self.init_minion()


data = """
WEB-10129958
"""
for d in data.strip().split('\n'):
    print d
    #SaltHelper(master='10.12.101.200', host=d).init_minion()

    print SaltHelper(master='10.12.101.200', host=d).reinstall()
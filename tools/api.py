# coding=utf-8
import httplib
import json
import logging
import urllib2
from urllib import urlencode

host = 'control.ops.ymatou.cn'
user = 'opsadmin'
passwd = 'control@8104'
path = '/api/token/'
cmd_path = 'http://control.ops.ymatou.cn/key/delete'

ContentType_Form = "application/x-www-form-urlencoded"

ContentType_Json = "application/json"

logger = logging.getLogger(__name__)


class BaseApi(object):
    type_list = None
    error_info = None
    content_type = ContentType_Json
    port = 80
    path, host, user, passwd, auth_data = None, None, None, None, None
    auth_header = None

    def __init__(self):
        self.path = path
        self.host = host
        self.user = user
        self.passwd = passwd
        self.auth_data = {
            'username': self.user,
            'password': self.passwd,
        }
        self.auth_header = {"Authorization": "Token %s" % self.get_token(), "Content-Type": self.content_type}

    def get_token(self):
        header = {"Content-Type": ContentType_Json}
        conn = httplib.HTTPConnection(self.host, self.port)
        conn.connect()
        content = json.dumps(self.auth_data)
        conn.request('POST', self.path, content, header)
        result = conn.getresponse().read()
        conn.close()
        return json.loads(result)['token']


class FormBaseApi(BaseApi):
    content_type = ContentType_Form
    cmd_path = None

    def req(self, data=None):
        if data:
            content = urlencode(data)
        else:
            content = None
        req = urllib2.Request(self.cmd_path, content, self.auth_header)
        result = urllib2.urlopen(req)
        result_content = result.read()
        logger.debug('path:%s data:%s' % (self.cmd_path, content))
        logger.debug(result_content)
        return json.loads(result_content)


class CmdApi(FormBaseApi):
    def __init__(self, _cmd_path):
        super(CmdApi, self).__init__()
        self.cmd_path = _cmd_path


class CmdControlApi(CmdApi):
    def __init__(self, _cmd_path):
        super(CmdControlApi, self).__init__(_cmd_path)

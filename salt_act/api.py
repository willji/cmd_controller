# coding=utf-8
import httplib
import json
import paramiko

from core.common import format_result, try_except, logger


class SshResult:
    """
    get the result of command by ssh
    """

    def __init__(self, host):
        self.host = host
        self.key = "/root/.ssh/id_rsa.pub"
        self.ssh = paramiko.SSHClient()

    def get(self, tgt, cmd):
        result = None
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host, 22, 'root', key_filename=self.key)
            std_in, std_out, std_err = self.ssh.exec_command(cmd)
            data = std_out.read()
            self.ssh.close()
            try:
                tmp_result = json.loads(data)
                result = format_result(0, tmp_result)
                logger.debug('get result: %s ' % result)
            except Exception, e:
                result = format_result(1, e.message + ' ' + str(data))
        except Exception, e:
            result = format_result(2, e.message)
        finally:
            return result


class SaltHttp:
    """
    get the result of command by htt
    """

    def __init__(self, master, port, token, path, data=None, timeout=30):
        self.master = master
        self.port = port
        self.token = token
        self.path = path
        self.data = data
        self.timeout = timeout

    @try_except
    def __request(self, method):
        header = {"token": self.token, "Content-Type": "application/json"}
        conn = httplib.HTTPConnection(self.master, self.port,timeout=self.timeout)
        conn.connect()
        conn.request(method, self.path, json.dumps(self.data), header)
        result = json.loads(conn.getresponse().read())
        # logger.debug('get result: %s ' % result)
        conn.close()
        return result

    def post(self, method='POST'):
        return self.__request(method)

    def get(self, method='GET'):
        return self.__request(method)

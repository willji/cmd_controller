from salt_act.api import SaltHttp
from pyzabbix import ZabbixAPI
import os
import sys
from threading import Thread, activeCount
import time

reload(sys)
sys.setdefaultencoding('utf-8')

MASTER = 'saltapi.pro.ymatou.cn'
TOKEN = '0cdffd479c53928502c4108728398f59'
ZABBIX_SERVER = 'http://zabbix.ymatou.cn'
FILE_PATH = 'C:/Users/huamaolin/Desktop/haproxy/allconfig/'

z_api = ZabbixAPI(ZABBIX_SERVER)
z_api.login('Admin', 'abcd@1234')
ips = []
for k in z_api.host.get(groupids='11', output=["host"]):
    ips.append(k['host'])

print  ips
class SaltTool(object):
    def __init__(self, tgt, ipaddress):
        self.ipaddress = ipaddress
        self.tgt = tgt

    @staticmethod
    def salt_api(send_data):
        return SaltHttp(MASTER, 80, TOKEN, '/cmd', send_data).post()

    def get_configs(self):
        result = None
        send_data = dict(tgt=self.tgt, func='cmd.shell', arg=['ls /usr/local/haproxy/etc'])
        rs = self.salt_api(send_data)
        if rs['retcode'] == 0:
            result = [str(x) for x in rs['stdout'][self.tgt].strip().split('\n') if str(x).endswith('.cfg')]
            self.process_file(result)
        return result

    def process_file(self, file_paths):
        for file_path in file_paths:
            self.get_file(file_path, len(file_paths))

    def get_file(self, file_path, count):
        send_data = dict(tgt=self.tgt, func='cp.get_file_str', arg=['/usr/local/haproxy/etc/%s' % file_path])
        rs = self.salt_api(send_data)
        if rs['retcode'] == 0:
            self.write_file(file_path, rs['stdout'][self.tgt], count)

    def write_file(self, file_path, content, count):
        try:
            folder_path = FILE_PATH + str(count) + '_' + self.ipaddress
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            with open(folder_path + '/' + file_path, 'w') as file_object:
                file_object.write(content)
        except Exception, e:
            print self.ipaddress, file_path, str(e)
            pass


def get_configs(minion, ipaddress):
    SaltTool(minion, ipaddress).get_configs()


fail_ips = []
for ip in ips:
    while activeCount() > 10:
        print activeCount()
        time.sleep(1)
    Thread(target=get_configs, args=(str(ip.replace('.', '')), str(ip))).start()

while True:
    time.sleep(1)
    print activeCount()
    if activeCount() < 2:
        break

print 'Finished get_haproxy'

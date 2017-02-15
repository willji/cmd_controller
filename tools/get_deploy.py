from salt_act.api import SaltHttp
import os
import sys
from threading import Thread, activeCount
import time

reload(sys)
sys.setdefaultencoding('utf-8')

MASTER = 'saltapi.pro.ymatou.cn'
TOKEN = '0cdffd479c53928502c4108728398f59'
ZABBIX_SERVER = 'http://zabbix.ymatou.cn'
FILE_PATH = 'D:\\discover\\deploy\\'

ips = ['10.11.26.28', '10.10.22.137', '10.11.35.31', '10.11.37.33', '10.11.29.38', '10.11.43.30', '10.11.35.35', '10.11.34.159', '10.11.29.13'
    , '10.11.29.83', '10.11.29.12', '10.11.26.26', '10.11.26.33'

       ]
ipstr = """
10.11.38.70
10.11.33.69
10.11.37.20
10.11.37.33
10.11.43.35
10.11.37.12
10.11.29.44
10.11.35.30
10.11.34.156
10.11.251.19
10.11.35.38
10.11.35.25
10.11.33.48
10.11.28.57
10.11.26.59
10.11.29.18
10.11.35.156
10.11.33.20
10.11.38.68
10.11.26.32
10.10.101.52
10.11.29.37
10.11.37.35
10.11.35.30
10.11.251.19
10.11.37.46
10.11.33.52
10.11.37.25
10.11.35.34
10.11.33.35
10.11.26.16
10.11.37.15
10.11.33.54
10.11.35.33
10.11.39.11
10.11.35.153
10.11.34.155
10.11.34.159
10.11.251.19
10.11.35.25
10.11.251.104
10.11.26.61
10.11.35.54
10.11.35.47
10.11.29.20
10.11.35.155
10.11.37.24
10.11.37.29
10.11.26.48
10.11.29.51
10.11.22.99
10.11.29.42
10.11.39.12
10.11.33.19
10.11.38.71
10.11.35.100
10.11.43.25
10.11.26.66
10.11.251.19
10.11.43.30
10.11.22.99
"""

ips = ipstr.split('\n')

class SaltTool(object):
    def __init__(self, tgt, ipaddress):
        self.ipaddress = ipaddress
        self.tgt = tgt

    @staticmethod
    def salt_api(send_data):
        return SaltHttp(MASTER, 80, TOKEN, '/cmd', send_data).post()

    def get_configs(self):
        result = None
        send_data = dict(tgt=self.tgt, func='cmd.shell', arg=['ls /usr/local/deploy'])
        rs = self.salt_api(send_data)
        if rs['retcode'] == 0:
            result = [str(x) for x in rs['stdout'][self.tgt].strip().split('\n')]
            self.process_file(result)
        return result

    def process_file(self, file_paths):
        for file_path in file_paths:
            self.get_file(file_path, 'start.sh', len(file_paths))
            self.get_file(file_path, 'stop.sh', len(file_paths))

    def get_file(self, file_path, file_name, count):
        send_data = dict(tgt=self.tgt, func='cp.get_file_str', arg=['/usr/local/deploy/%s/%s' % (file_path, file_name)])
        rs = self.salt_api(send_data)
        if rs['retcode'] == 0:
            self.write_file(file_path, file_name, rs['stdout'][self.tgt], count)

    def write_file(self, file_path, file_name, content, count):
        try:
            folder_path = FILE_PATH + file_path
            print folder_path
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            with open(folder_path + '/' + file_name, 'w') as file_object:
                if '-Xmx1096M' in content or 'stg' in content:
                    print '################## %s' % self.ipaddress
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

print 'Finished get_deploy.'

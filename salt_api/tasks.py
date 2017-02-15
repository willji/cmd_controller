# coding=utf-8
from celery import Task
from salt_act.act import SaltActAdmin, SaltAdmin
import urllib
import httplib2
from django.core.cache import cache
from salt_api.models import Master

EXPIRES_TIME_OUT = 180


class SaltAsyncRegTask(Task):
    def run(self, master, host):
        SaltAdmin(master, host).accept_key()
        SaltAdmin(master, host).init_minion()
        return '%s %s reg success' % (master, host)


class SaltAsyncDelTask(Task):
    def run(self, master, host):
        SaltAdmin(master, host).delete_key()
        return '%s %s del success' % (master, host)


class CacheSaltKeyTask(Task):
    def run(self, *args, **kwargs):
        rs = SaltActAdmin().get_salt_key()
        cache.set('salt_key_all', rs, 600)
        return 'cache ok'


class AutoRegMinionJobTask(Task):
    def run(self):
        for master in Master.objects.all():
            AutoRegKeysTask().apply_async((master,), expires=EXPIRES_TIME_OUT)


class AutoRegKeysTask(Task):
    def run(self, master):
        for item in SaltActAdmin().get_salt_key(master):
            if item['key'] and item['key']['minions_pre']:
                for minion in item['key']['minions_pre'][0:1]:
                    SaltAsyncRegTask().apply_async((item['master'], minion), expires=EXPIRES_TIME_OUT)
            if item['key'] and item['key']['minions_denied']:
                for minion in item['key']['minions_denied'][0:1]:
                    SaltAsyncDelTask().apply_async((item['master'], minion), expires=EXPIRES_TIME_OUT)
            if item['key'] and item['key']['minions_rejected']:
                for minion in item['key']['minions_rejected'][0:1]:
                    SaltAsyncDelTask().apply_async((item['master'], minion), expires=EXPIRES_TIME_OUT)


class AutoCheckMongoJobTask(Task):
    http = httplib2.Http()
    cookie = None
    site = 'http://tool.ymatou.cn/db'
    body = {'username': 'admin', 'password': '//ymt@#123'}

    def __req(self, url):
        return self.http.request(url % self.site, 'GET', headers=self.cookie)

    def check(self, url="%s/Home/GetServerDetail/"):
        return self.__req(url)

    def check_db(self, url="%s/DBAdmin/ShowInfo?id=(se)27(db)Ymt_Counter_Config&type=2"):
        return self.__req(url)

    def login(self, headers):
        url = '%s/Account/Valid/' % self.site
        response, content = self.http.request(url, 'POST', headers=headers, body=urllib.urlencode(self.body))
        self.cookie = {'Cookie': response['set-cookie']}

    def refresh(self, url='%s/home/refresh'):
        return self.__req(url)

    def run(self):
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.login(headers)
        response, content = self.check()
        response_db, content_db = self.check_db()
        if response.status != 200 or response_db.status != 200:
            self.refresh()
            print 'refresh ok'
        else:
            print 'check ok'

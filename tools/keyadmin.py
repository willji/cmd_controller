from api import CmdControlApi

site = 'http://control.ops.ymatou.cn/'


def try_except(func):
    def wrapped(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception, e:
            result = e.message
        finally:
            return result

    return wrapped


class SaltTool(object):
    def __init__(self):
        pass

    @staticmethod
    def __test_ping(master, minion):
        return CmdControlApi(site + 'salt/key/delete').req(dict(master=master, minion=minion))

    @staticmethod
    def __delete_key(master, minion):
        return CmdControlApi(site + 'salt/key/delete').req(dict(master=master, minion=minion))

    @try_except
    def __accept_key(self, master, minion):
        return CmdControlApi(site + 'salt/key/accept').req(dict(master=master, minion=minion))

    @try_except
    def __init_minion(self, master, minion):
        return CmdControlApi(site + 'salt/minion/init').req(dict(master=master, minion=minion))

    @staticmethod
    def __all_key():
        return CmdControlApi(site + 'salt/key/all').req()

    def get_minions(self):
        rs = self.__all_key()
        for master in rs:
            if master['master'] == '10.10.251.132':
                return master['key']['minions']

    def auto_init(self):
        rs = self.__all_key()
        for master in rs:
            for minion in master['key']['minions_pre']:
                print master['master'], minion
                print self.__accept_key(master['master'], minion)
                print self.__init_minion(master['master'], minion)

    def delete_key(self, master, minion):
        self.__delete_key(master, minion)

    def job_init(self):
        self.auto_init()

SaltTool().job_init()

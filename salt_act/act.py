# coding=utf-8
from api import SshResult, SaltHttp
from core.common import format_result, try_except, logger, RETCODE, STDERR, STDOUT
from salt_api.models import Minion, Master, Log, Module

Salt_CP_GET_DIR = 'cp.get_dir'

Salt_Grains = 'grains.item'

Salt_Sync_All = 'saltutil.sync_all'

Salt_GetIPADDRS = 'network.ip_addrs'

Salt_Supervisor_Install = 'supervisor_install'

Salt_Supervisor_Start = 'supervisor_start'

Agent_Install = 'agent_install'

Logviewer = 'logviewer'

Salt_guard = 'salt-guard'


class ExecCmdSaltBase(object):
    def __init__(self, master, host_name, salt_name, arg, timeout=300):
        self.master = master
        self.host_name = host_name
        self.salt_name = salt_name
        self.arg = arg
        self.timeout = timeout
        self.send_data = dict(tgt=self.host_name, func=self.salt_name, arg=self.arg, timeout=timeout)

    def run(self):
        pass


class ExecCmdSaltBaseByHttp(ExecCmdSaltBase):
    def run(self):
        return SaltHttp(self.master.ip, self.master.port, self.master.token, '/cmd', self.send_data,
                        self.timeout).post()


class ExecCmdSaltBaseBySSH(ExecCmdSaltBase):
    def run(self):
        cmd = 'salt %s %s ' % (self.host_name, self.salt_name)
        if self.arg:
            arg = ' '.join(self.arg)
            cmd += arg
        cmd += ' --out=json'
        return SshResult(self.master.ip).get(self.host_name, cmd)


class ExecCmdSalt(object):
    def __init__(self, host_name, salt_name, arg, timeout=300):
        self.host_name = host_name
        self.salt_name = salt_name
        self.arg = arg
        self.timeout = timeout

    @try_except
    def run(self):
        """
        exec salt command by salt
        :return:
        """
        hosts = Minion.objects.filter(ip__contains=self.host_name + '#')
        if len(hosts) == 0:
            return format_result(1, 'no this ip %s' % self.host_name)
        if Module.objects.filter(name=self.salt_name):
            salt_name = Module.objects.get(name=self.salt_name).salt_name
        else:
            salt_name = self.salt_name
        self.__log('start', salt_name=salt_name)
        result = self.__handle(hosts[0].name, salt_name)
        if result[RETCODE] == 0:
            result[STDOUT] = {self.host_name: result[STDOUT][hosts[0].name]}
        self.__log('end', salt_name=salt_name, result=str(result))
        logger.debug('result type:%s ' % type(result))
        logger.debug('result:%s ' % result)
        return result

    def __log(self, action, salt_name='', result=None):
        arg_str = str(self.arg)
        if isinstance(self.arg, tuple):
            arg_str = ' '.join(self.arg)
        all_cmd = "salt -S  '%s' %s %s " % (self.host_name, salt_name, arg_str)
        if result:
            Log.objects.create(host=self.host_name, module=self.salt_name, arg=all_cmd, action=action, result=result)
        else:
            Log.objects.create(host=self.host_name, module=self.salt_name, arg=all_cmd, action=action)

    def __handle(self, host, salt_name):
        result = None
        for master in Minion.objects.get(name=host).master.all():
            result = ExecCmdSaltBaseByHttp(master, host, salt_name, self.arg, self.timeout).run()
            if result[RETCODE] != 1:
                break
        return result


class ExecCmd(ExecCmdSalt):
    pass


class SaltAdmin(object):
    minion = None

    def __init__(self, master_ip, host, timeout=30):
        self.master_ip = master_ip
        self.host = host
        self.master = Master.objects.get(ip=self.master_ip)
        self.timeout = timeout

    def init(self):
        if Minion.objects.filter(name=self.host):
            self.minion = Minion.objects.get(name=self.host)

    def __salt_api(self, path='/cmd', data=None):
        if not data:
            data = {'host': self.host}
        return SaltHttp(self.master_ip, self.master.port, self.master.token, path, data, self.timeout).post()

    def __log(self, module, action, arg='', result='no result'):
        if isinstance(arg, tuple):
            arg = [str(x) for x in arg]
        Log.objects.create(host=self.host, module=module, arg=arg, action=action, result=result)

    @try_except
    def delete_key(self):
        self.init()
        self.__log(module='delete_key', action='start')
        if self.__salt_api(path='/key/delete')[RETCODE] == 0:
            if self.minion:
                self.minion.master.remove(self.master)
                self.minion.delete()
        self.__log(module='delete_key', action='end')
        return format_result(0, 'all done')

    def __get_ip(self, save=False):
        result = self.__salt_api(data=self.__get_send_data('%s' % Salt_GetIPADDRS))
        m_ip = 'none'
        if result[RETCODE] == 0:
            m_ip = '#'.join(result[STDOUT][self.host]) + '#'
        if save:
            self.minion.ip = m_ip
            self.minion.save()
        else:
            return m_ip

    def __get_send_data(self, func, arg=()):
        return {'tgt': self.host, 'func': func, 'arg': arg}

    def __sync(self):
        return self.__salt_api(data=self.__get_send_data('%s' % Salt_Sync_All))

    @try_except
    def init_minion(self):
        self.init()
        self.__log(module='init', action='start')
        self.__get_ip(save=True)
        if self.minion.kernel.lower() == 'none':
            self.__get_kernel(save=True)
        elif self.minion.kernel.lower() == 'windows':
            self.__cp_char_det()
        # add log agent
        self.__sync()
        result = self.__install_logviewer()
        self.__log(module='init', action='end', result=result)
        return result

    @try_except
    def accept_key(self):
        self.__log(module='accept_key', action='start')
        result = self.__salt_api(path='/key/accept')
        if result[RETCODE] == 0 and result[STDOUT] == self.host:
            m_kernel = self.__get_kernel()
            m_ip = self.__get_ip()
            if len(Minion.objects.filter(name=self.host)) == 0:
                minion = Minion(ip=m_ip, kernel=m_kernel, name=self.host)
                minion.save()
                minion.master.add(self.master)
            else:
                masters = [x.ip for x in Minion.objects.get(name=self.host).master.all()]
                if self.master.ip in masters:
                    Minion.objects.filter(name=self.host).update(kernel=m_kernel, ip=m_ip)
                else:
                    Minion.objects.get(name=self.host).master.add(self.master_ip)
            result = format_result(0, 'done')
        else:
            result = format_result(1, 'failed')
        self.__log(module='accept_key', action='end', result=result)
        return result

    def __cp_char_det(self):
        return self.__salt_api(
            data=self.__get_send_data(Salt_CP_GET_DIR, arg=('salt://file/chardet', 'C:\\salt\\bin\\Lib',)))

    def __get_kernel(self, save=False):
        result = self.__salt_api(data=self.__get_send_data(Salt_Grains, arg=('kernel',)))
        m_kernel = 'none'
        if result[RETCODE] == 0:
            m_kernel = result[STDOUT][self.host]['kernel']
        if save:
            self.minion.kernel = m_kernel
            self.minion.save()
        else:
            return m_kernel

    def __install_logviewer(self):
        # host_name, salt_name, arg, timeout=300
        ExecCmdSalt(self.minion.ip.split('#')[0], '%s' % Salt_Supervisor_Install, (), timeout=self.timeout).run()
        ExecCmdSalt(self.minion.ip.split('#')[0], '%s' % Salt_Supervisor_Start, (), timeout=self.timeout).run()
        ExecCmdSalt(self.minion.ip.split('#')[0], '%s' % Agent_Install, ('%s' % Logviewer,), timeout=self.timeout).run()
        return ExecCmdSalt(self.minion.ip.split('#')[0], '%s' % Agent_Install, ('%s' % Salt_guard,), timeout=self.timeout).run()


class SaltActAdmin(object):
    @staticmethod
    @try_except
    def get_module_name():
        return format_result(0, [{"name": x.name, "describe": x.describe} for x in
                                 Module.objects.filter(private_status=False)])

    @staticmethod
    def __get_salt_key(master, timeout):
        result = {'master': master.ip}
        keys = SaltHttp(master.ip, master.port, master.token, '/key/all', timeout).get()
        if keys[RETCODE] == 0:
            result['key'] = keys[STDOUT]
        else:
            result['key'] = keys[STDERR]
        return result

    def get_salt_key(self, master=None, timeout=30):
        if master:
            return [self.__get_salt_key(master,timeout)]
        else:
            return [self.__get_salt_key(master, timeout) for master in Master.objects.all()]

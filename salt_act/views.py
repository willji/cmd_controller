# coding=utf-8
# Create your views here.
from django.http import HttpResponse
import json
from act import ExecCmdSalt, ExecCmd, SaltAdmin, SaltActAdmin
from rest_framework import permissions
from rest_framework.views import APIView
from core.common import logger
from django.core.cache import cache


class BaseViewAdmin(APIView):
    http_method_names = ['post']
    permission_classes = (permissions.IsAuthenticated,)
    format_json = True

    def init(self, request):
        pass

    def run(self):
        pass

    def post(self, request):

        self.init(request)
        result = self.run()
        logger.info('request result:  %s ' % result)
        if self.format_json:
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse(result)

    def get(self, request):
        return self.post(request)


class CmdBaseViewAdmin(BaseViewAdmin):
    host = None
    module_name = None
    arg = None
    timeout = 300
    format_json = False

    def init(self, request):
        self.host = request.POST.get('host')
        self.module_name = request.POST.get('module_name')
        self.timeout = int(request.POST.get('timeout', 300))


class ExecCmdSaltView(CmdBaseViewAdmin):
    def init(self, request):
        super(ExecCmdSaltView, self).init(request)
        self.arg = request.POST.get('arg')

    def run(self):
        logger.info('class:{},host:{},module_name:{},args:{},timeout:{}'
                    .format(self.__class__.__name__, self.host, self.module_name, self.args, self.timeout))
        return ExecCmdSalt(self.host, self.module_name, self.arg, self.timeout).run()


class ExecCmdView(CmdBaseViewAdmin):
    n_arg = ()
    format_json = True

    def init(self, request):
        super(ExecCmdView, self).init(request)
        if 'arg' in request.POST:
            arg = request.POST.get('arg').split('#')
            self.n_arg = tuple(arg)

    def run(self):
        logger.info('class:{},host:{},module_name:{},n_arg:{},timeout:{}'
                    .format(self.__class__.__name__, self.host, self.module_name, self.n_arg, self.timeout))
        return ExecCmd(self.host, self.module_name, self.n_arg, self.timeout).run()


class SaltGetKeyAllView(BaseViewAdmin):
    http_method_names = ['get']
    timeout = 30

    def run(self):
        salt_key_all = cache.get('salt_key_all')
        if salt_key_all:
            return salt_key_all
        else:
            return SaltActAdmin().get_salt_key(timeout=self.timeout)


class SaltKeyBaseView(BaseViewAdmin):
    master = None
    host = None

    def init(self, request):
        self.master = request.POST.get('master')
        self.host = request.POST.get('minion')
        self.timeout = int(request.POST.get('timeout', 30))
        logger.info('class:{},host:{},timeout:{}'.format(self.__class__.__name__, self.host, self.timeout))


class SaltAcceptKeyView(SaltKeyBaseView):
    def run(self):
        return SaltAdmin(self.master, self.host, timeout=self.timeout).accept_key()


class SaltDeleteKeyView(SaltKeyBaseView):
    def run(self):
        return SaltAdmin(self.master, self.host, timeout=self.timeout).delete_key()


class SaltInitMinionView(SaltKeyBaseView):
    def run(self):
        return SaltAdmin(self.master, self.host, timeout=self.timeout).init_minion()


class SaltGetModuleNameView(BaseViewAdmin):
    http_method_names = ['get']

    def run(self):
        return SaltActAdmin().get_module_name()

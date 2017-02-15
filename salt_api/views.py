# Create your views here.
from rest_framework import permissions
from salt_api.models import Master, Minion, Module, Log
from salt_api.serializers import MasterSerializer, MinionSerializer, ModuleSerializer, LogSerializer
from rest_framework import viewsets
from rest_framework import filters


class ViewSetBae(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)


class MasterViewSet(ViewSetBae):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer
    filter_fields = ('name', 'ip',)


class MinionViewSet(ViewSetBae):
    queryset = Minion.objects.all()
    serializer_class = MinionSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('ip', 'name', 'kernel',)
    search_fields = ('ip', 'name')


class ModuleViewSet(ViewSetBae):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    filter_fields = ('name',)


class LogViewSet(ViewSetBae):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    filter_fields = ('module', 'action')

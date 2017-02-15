from django.contrib import admin
from salt_api.models import Log, Minion, Master, Module


# Register your models here.
class LogAdmin(admin.ModelAdmin):
    list_display = ('host', 'module', 'arg', 'action', 'result', 'created_date', 'modified_date')
    list_filter = ('host', 'module', 'created_date')
    fields = ('host', 'module', 'arg', 'action', 'result')
    search_fields = ('host', 'module', 'arg', 'action', 'result')


class MinionAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'kernel')
    list_filter = ('name', 'ip', 'kernel', 'master')
    fields = ('name', 'ip', 'kernel', 'master')
    search_fields = ('name', 'ip', 'kernel', 'master')


class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'port', 'token', 'env')
    list_filter = ('name', 'ip')
    fields = ('name', 'ip', 'port', 'token', 'env')
    search_fields = ('name', 'ip', 'port', 'env')


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'salt_name', 'wmi_name', 'ansible_name', 'private_status', 'describe')
    list_filter = ('name', 'salt_name')
    fields = ('name', 'salt_name', 'private_status')
    search_fields = ('name', 'salt_name', 'wmi_name', 'ansible_name')


admin.site.register(Module, ModuleAdmin)
admin.site.register(Master, MasterAdmin)
admin.site.register(Minion, MinionAdmin)
admin.site.register(Log, LogAdmin)

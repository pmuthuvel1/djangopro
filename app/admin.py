# -*- coding: utf-8 -*-

from django.contrib import admin
from app.models import ServerConf, NetworkConf, ServiceList, FileList, ScriptList,MachineDetail,LoginDetail,ConfigType,ConfigPath,ScriptPath

class ServerConfAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fields = ('name', 'port', 'user', 'password', 'service_list', 'file_list', 'script_list')
    search_fields = ('name', 'port', 'user')
    filter_horizontal = ('service_list', 'file_list', 'script_list')

class NetworkConfAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fields = ('interface', 'address', 'netmask', 'network',
            'broadcast', 'gateway')
    search_fields = ('interface', 'address', 'netmask', 'network',
            'broadcast', 'gateway')

class ServiceListAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fields = ('name',)
    search_fields = ('name',)

class FileListAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('path',)

class ScriptListAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('path',)


class LoginDetailAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('path',)

class ConfigPathInline(admin.StackedInline):
    model = ConfigPath
    extra = 1
        
class ConfigTypeAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('path',)
    inlines =[ConfigPathInline]
    
class ScriptPathInline(admin.StackedInline):
    model = ScriptPath
    extra = 1
    
class MachineDetailAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('path',)
    inlines =[ScriptPathInline]
        
                
admin.site.register(ServerConf, ServerConfAdmin)
admin.site.register(NetworkConf, NetworkConfAdmin)
admin.site.register(ServiceList, ServiceListAdmin)
admin.site.register(FileList, FileListAdmin)
admin.site.register(ScriptList, ScriptListAdmin)

admin.site.register(MachineDetail, MachineDetailAdmin)
admin.site.register(LoginDetail, LoginDetailAdmin)
admin.site.register(ConfigType, ConfigTypeAdmin)
#admin.site.register(ConfigPath, ConfigPathAdmin)


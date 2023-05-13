from django.contrib import admin

# Register your models here.
from .models import DBLogs, DBInfos


class DBLogsAdmin(admin.ModelAdmin):
    # 需要展示的列
    list_display = (
        'id',
        'database',
        'sql'
    )
    list_filter = ['database']
    search_fields = ('id', 'database')


class DBInfosAdmin(admin.ModelAdmin):
    # 需要展示的列
    list_display = (
        'id',
        'host',
        'user',
        'password',
        'database',
        'port',
        'is_delete'
    )
    list_filter = ['database', 'host', 'is_delete']
    search_fields = ('id', 'host', 'database')


# 把models下的DBLog和admin注册到一起
admin.site.register(DBLogs, DBLogsAdmin)
admin.site.register(DBInfos, DBInfosAdmin)
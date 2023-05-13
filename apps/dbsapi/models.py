

from django.db import models
from utils.base_models import BaseModel


class DBLogs(BaseModel):
    id = models.AutoField(verbose_name="id主键", primary_key=True, help_text="id主键")
    database = models.ForeignKey('DBInfos', on_delete=models.CASCADE, related_name='dblogs',
                                 verbose_name='数据库信息', help_text='数据库信息')
    # db_name = models.CharField(verbose_name='数据库名称', default='localhost', max_length=50, help_text='执行sql数据库名称')
    sql = models.CharField(verbose_name='执行的sql', max_length=200, help_text='执行的sql')

    class Meta:
        db_table = 'gk_dblogs'
        verbose_name = '执行sql的日志信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class DBInfos(BaseModel):
    id = models.AutoField(verbose_name="id主键", primary_key=True, help_text="id主键")
    host = models.CharField(verbose_name='主机地址', max_length=50, help_text='主机地址')
    user = models.CharField(verbose_name='用户名', max_length=50, help_text='用户名')
    password = models.CharField(verbose_name='密码', max_length=50, help_text='密码')
    database = models.CharField(verbose_name='数据库名称', max_length=50, unique=True, help_text='数据库名称')
    port = models.IntegerField(verbose_name='端口',  help_text='端口')

    # 定义子类，用于设置当前数据模型的元数据信息
    class Meta:
        db_table = 'gk_dbinfos'
        verbose_name = '数据库信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.database

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     move_list = ['create_time', 'update_time', 'is_delete']  # 需要调整顺序字段的列表 
    #     for item in move_list:
    #         self.fields.move_to_end(item, last=True)


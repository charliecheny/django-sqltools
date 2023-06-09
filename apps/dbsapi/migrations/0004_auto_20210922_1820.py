# Generated by Django 3.2.5 on 2021-09-22 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbsapi', '0003_auto_20210922_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbinfos',
            name='is_delete',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='逻辑删除', verbose_name='逻辑删除'),
        ),
        migrations.AlterField(
            model_name='dblogs',
            name='is_delete',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='逻辑删除', verbose_name='逻辑删除'),
        ),
    ]

from rest_framework import serializers
from .models import DBLogs, DBInfos


class DBLogModelSerializer(serializers.ModelSerializer):

    database_id = serializers.PrimaryKeyRelatedField(label="DBInfos ID", queryset=DBInfos.objects.all())
    database = serializers.StringRelatedField(label='所属数据库')

    class Meta:
        model = DBLogs
        # 排除字段（不输出）
        # exclude = ('create_time', 'update_time', 'is_delete')
        fields = ("id", "database", "database_id", "sql", "create_time")
        read_only_fields = ("create_time",)
        # 给db_name和sql 添加只输入属性
        # extra_kwargs = {
        #     'db_name': {
        #         'write_only': True
        #     },
        #     'sql': {
        #         'write_only': True
        #     }
        # }

    def create(self, validated_data):
        # 库里面存储的是database_id(关联表)，需要转成模型对象的database,然后才能存储
        database = validated_data.pop("database_id")
        validated_data["database"] = database
        return DBLogs.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'database_id' in validated_data:
            database = validated_data.pop("database_id")
            validated_data["database"] = database
        return super().update(instance, validated_data)


class DBInfoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DBInfos
        exclude = ('update_time', 'is_delete')  # 不包含
        # 给db_name和sql 添加只输入属性
        extra_kwargs = {
            # 'host': {
            #     'write_only': True
            # },
            'user': {
                'write_only': True
            },
            'password': {
                'write_only': True
            },
            'port': {
                'write_only': True
            },
            'create_time': {
                'read_only': True
            },
        }


class DBInfoNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = DBInfos
        fields = ('id', 'database')
from django.http import HttpResponse
from rest_framework import viewsets, status
from .models import DBLogs, DBInfos
from . import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.mysql_tools import fetchall_to_dict, exec_sql


# 查询日志记录
class DBSApiViewSet(viewsets.ModelViewSet):
    queryset = DBLogs.objects.all()
    serializer_class = serializers.DBLogModelSerializer

    # 查询sql记录一条日志进表里
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data  # 获取执行sql的数据库id和语句
        # data的值 OrderedDict([('database_id', <DBInfos: teach>), ('sql', 'select * from student;')])
        # 判断database_id是否存在，存在则执行查询操作，不存在则抛出异常
        db_info_model = DBInfos.objects.filter(id=data.get('database_id').id, is_delete=False)
        if db_info_model:
            db_info = db_info_model.values('host', 'user', 'password', 'port', 'database')[0]
            res = fetchall_to_dict(db_info=db_info, sql=data['sql'])  # 调用执行sql的方法
            serializer.save()  # 记录执行日志
            data = serializer.data  # 获取序列化输出的数据
            data.update({'results': res})  # 把执行结果放进去
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'msg': '数据库{}未找到，请先添加相关配置'.format(data.get('database_id').id)},
                            status=status.HTTP_400_BAD_REQUEST)

    # 执行update or delete sql,记录一条日志进表里
    @action(methods=['post'], detail=False)
    def exec(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data  # 获取执行sql的名称和语句
        # data.get('database_id')获取的是一个对象，再用对象访问id属性
        db_info_model = DBInfos.objects.filter(dblogs__id=data.get('database_id').id, is_delete=False)
        if db_info_model:
            db_info = db_info_model.values('host', 'user', 'password', 'port', 'database')[0]
            res = exec_sql(db_info=db_info, sql=data['sql'])  # 调用执行sql的方法
            serializer.save()
            # 调用完保存方法后，不能再使用validated_data
            data = serializer.data
            data.update({'results': res})
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'msg': '数据库{}未找到，请先添加相关配置'.format(data.get('database_id').id)},
                            status=status.HTTP_400_BAD_REQUEST)


# 数据库配置信息写入
class DBInfoViewSet(viewsets.ModelViewSet):
    queryset = DBInfos.objects.all()
    serializer_class = serializers.DBInfoModelSerializer

    def perform_destroy(self, instance: DBInfos):
        instance.is_delete = True
        instance.save()

    @action(methods=['get'], detail=True, url_path='dbslogs')
    def dblogs(self, request, pk=None):
        dblogs_model = DBLogs.objects.filter(database_id=pk, is_delete=False)
        one_list = []
        for obj in dblogs_model:
            one_list.append({
                'id': obj.id,
                'sql': obj.sql
            })
        return Response(data=one_list)

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        """
        不同的action选择不同的序列化器
        :return:
        """
        if self.action == 'names':
            return serializers.DBInfoNameSerializer
        #     elif self.action == 'run':
        #         return ProjectsRunSerializer
        else:
            return self.serializer_class


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.http import JsonResponse


def teacherpage(request):
    return render(request, 'tableDemo.html')


def teacherInfo(request):
    """
    查询结果必须是json格式:{"total": 2,"rows": [{},{}]}
    """
    if request.method == "GET":
        # search_kw = request.GET.get('search_kw', None)
        # 获取分页参数用于查询对应页面数据，page为第几页，size为每页数据条数
        page_num = request.GET.get('page', 1)
        size = request.GET.get('size', 10)
        # 查询全部
        dbinfos = DBInfos.objects.all()
        # 使用分页器返回查询的页数和size
        paginator = Paginator(dbinfos, per_page=size)
        page_object = paginator.page(page_num)

        # 总数
        total = dbinfos.count()
        # 查询list of dict
        rows = [model_to_dict(i) for i in page_object]
        # print(rows)
        return JsonResponse({'total': total, 'rows': rows})

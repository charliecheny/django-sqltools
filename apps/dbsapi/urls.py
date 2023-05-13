from django.urls import path, include
from . import views
from rest_framework import routers

# 创建SimpleRouter路由对象
router = routers.SimpleRouter()

# 为视图类注册路由
router.register('dbsapi', views.DBSApiViewSet)
router.register('dbsinfo', views.DBInfoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('dbsinfos/info', views.teacherInfo),
    path('dbsinfos/page', views.teacherpage),
]
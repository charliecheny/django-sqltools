"""SQLTools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.staticfiles.views import serve


def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)


schema_view = get_schema_view(
    openapi.Info(
        title='dbsapi工具接口文档',
        default_version='v1',
        terms_of_service='https://localhost:8000/dbsapi',
        contact=openapi.Contact(email='charlie.yang@gaodun.com')
    ),
    public=True,
)
# 系统路由
urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
    path('admin/', admin.site.urls),
    path('', include('dbsapi.urls')),

    path('docs/', include_docs_urls(title='dbsapi工具接口文档')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='swagger-redoc'),
]

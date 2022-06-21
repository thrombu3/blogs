"""day62_BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from django.views.static import serve
from day62_BBS import settings  # django其实有两个配置文件

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 注册接口
    url(r'^register/', views.register, name='register_view'),
    # 登录接口
    url(r'^login/', views.login, name='login_view'),
    # 图片验证码接口
    url(r'^get_code/', views.get_code),
    # 首页接口
    url(r'^home/', views.home, name='home_view'),
    # 修改密码
    url(r'^set_pwd/', views.set_pwd, name='set_pwd_view'),
    # 注销登录
    url(r'^logout/', views.logout),
    # 暴露指定的任意资源(固定语法)
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

    # 文章点赞点踩(防止被顶替 尽量写在含有正则表达式的路由上方)
    url(r'^up_or_down/$', views.up_or_down),
    # 文章评论功能(防止被顶替 尽量写在含有正则表达式的路由上方)
    url(r'^comment/$', views.comment),

    # 后台管理
    url(r'^backend/$', views.backend, name='back_view'),
    url(r'^add/article/$', views.add_article, name='add_article_view'),
    url(r'^file_upload/$', views.file_upload),
    url(r'^edit/article/$', views.edit_article, name='edit_article_view'),  # 换一种携带方式玩玩
    url(r'^delete/article/$', views.delete_article),  # 换一种携带方式玩玩

    # 头像修改
    url(r'^update/avatar/$',views.update_avatar,name='update_avatar_view'),

    # 个人站点页面  jason/category/1
    url(r'^(?P<username>\w+)/$', views.site, name='site_view'),
    # 侧边栏筛选功能
    # url(r'^(?P<username>\w+)/(?P<condition>category)/(?P<category_id>\d+)/', views.site),
    # url(r'^(?P<username>\w+)/(?P<condition>tag)/(?P<tag_id>\d+)/', views.site),
    # url(r'^(?P<username>\w+)/(?P<condition>archive)/(?P<year_month>\w+)/', views.site),
    # 筛选功能三合一优化
    url(r'^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<params>.*)/', views.site),
    # 文章详情页
    url(r'^(?P<username>\w+)/articles/(?P<article_id>\d+)/', views.article_detail, name='article_view')
]

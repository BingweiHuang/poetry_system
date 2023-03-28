# blog/urls.py

from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import search_views
from main.views.sign_in_view import SignInView
from main.views.update_password_view import UpdatePasswordView


'''
# 5种方法都开放
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'accounts', viewset=account_views.AccountRViewSet)
'''


ci_list = search_views.CiViewSet.as_view({
    'get': 'list',  # 处理get请求，获取多个记录
    # 'post': 'create'  # 处理post请求，添加单个记录
})
ci_detail = search_views.CiViewSet.as_view({
    'get': 'retrieve',  # 处理get请求，获取单个记录
    # 'put': 'update',  # 处理put请求，修改单个记录
    # 'delete': 'destroy',  # 处理delete请求，删除单个记录
})

shi_list = search_views.ShiViewSet.as_view({
    'get': 'list',  # 处理get请求，获取多个记录
})
shi_detail = search_views.ShiViewSet.as_view({
    'get': 'retrieve',  # 处理get请求，获取单个记录
})

fly_list = search_views.FlyViewSet.as_view({
    'get': 'list',  # 处理get请求，获取多个记录
})
fly_detail = search_views.FlyViewSet.as_view({
    'get': 'retrieve',  # 处理get请求，获取单个记录
})
shijing_list = search_views.ShijingViewSet.as_view({
    'get': 'list',  # 处理get请求，获取多个记录
})
shijing_detail = search_views.ShijingViewSet.as_view({
    'get': 'retrieve',  # 处理get请求，获取单个记录
})


urlpatterns = [

    # re_path(r'^posts/$', account_views.PostList.as_view()),
    # re_path(r'^posts/(?P<pk>[0-9]+)$', account_views.PostDetail.as_view()),

    # 视图集

    re_path(r'^cis/$', ci_list),
    re_path(r'^cis/(?P<pk>[0-9]+)$', ci_detail),

    re_path(r'^shis/$', shi_list),
    re_path(r'^shis/(?P<pk>[0-9]+)$', shi_detail),

    re_path(r'^flys/$', fly_list),
    re_path(r'^flys/(?P<pk>[0-9]+)$', fly_detail),

    re_path(r'^shijings/$', shijing_list),
    re_path(r'^shijings/(?P<pk>[0-9]+)$', shijing_detail),

]


urlpatterns = format_suffix_patterns(urlpatterns)


'''
# 5种方法都开放
urlpatterns += router.urls
'''

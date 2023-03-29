# blog/urls.py

from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import account_views
from main.views.sign_in_view import SignInView
from main.views.update_password_view import UpdatePasswordView


'''
# 5种方法都开放
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'accounts', viewset=account_views.AccountRViewSet)
'''

# 自定义开放哪些方法
# user_list = account_views.UserViewSet.as_view({
#     'post': 'create'  # 处理post请求，添加单个记录
# })
#
# user_detail = account_views.UserViewSet.as_view({
#     'put': 'update',  # 处理put请求，修改单个记录
# })

post_list = account_views.PostViewSet.as_view({
    'get': 'list',  # 处理get请求，获取多个记录
    'post': 'create'  # 处理post请求，添加单个记录
})
post_detail = account_views.PostViewSet.as_view({
    'get': 'retrieve',  # 处理get请求，获取单个记录
    'put': 'update',  # 处理put请求，修改单个记录
    'delete': 'destroy',  # 处理delete请求，删除单个记录
})

follow_list = account_views.FollowViewSet.as_view({
    'get': 'list',  # 处理get请求，获取多个记录
    'post': 'create'  # 处理post请求，添加单个记录
})
follow_detail = account_views.FollowViewSet.as_view({
    'get': 'retrieve',  # 处理get请求，获取单个记录
    # 'put': 'update',  # 处理put请求，修改单个记录
    'delete': 'destroy',  # 处理delete请求，删除单个记录
})

account_list = account_views.AccountViewSet.as_view({
    'get': 'list',  # 处理get请求，获取多个记录
    # 'post': 'create'  # 处理post请求，添加单个记录
})
account_detail = account_views.AccountViewSet.as_view({
    'get': 'retrieve',  # 处理get请求，获取单个记录
    'put': 'update',  # 处理put请求，修改单个记录
    # 'delete': 'destroy',  # 处理delete请求，删除单个记录
})

like_list = account_views.LikeViewSet.as_view({
    'get': 'list',  # 处理get请求，获取多个记录
    'post': 'create'  # 处理post请求，添加单个记录
})
like_detail = account_views.LikeViewSet.as_view({
    'get': 'retrieve',  # 处理get请求，获取单个记录
    # 'put': 'update',  # 处理put请求，修改单个记录
    'delete': 'destroy',  # 处理delete请求，删除单个记录
})

comment_list = account_views.CommentViewSet.as_view({
    'get': 'list',  # 处理get请求，获取多个记录
    'post': 'create'  # 处理post请求，添加单个记录
})
comment_detail = account_views.CommentViewSet.as_view({
    'get': 'retrieve',  # 处理get请求，获取单个记录
    # 'put': 'update',  # 处理put请求，修改单个记录
    'delete': 'destroy',  # 处理delete请求，删除单个记录
})

shi_collection_list = account_views.ShiCollectionViewSet.as_view({
    'get': 'list',  # 处理get请求，获取多个记录
    'post': 'create'  # 处理post请求，添加单个记录
})
shi_collection_detail = account_views.ShiCollectionViewSet.as_view({
    'get': 'retrieve',  # 处理get请求，获取单个记录
    # 'put': 'update',  # 处理put请求，修改单个记录
    'delete': 'destroy',  # 处理delete请求，删除单个记录
})

ci_collection_list = account_views.CiCollectionViewSet.as_view({
    'get': 'list',  # 处理get请求，获取多个记录
    'post': 'create'  # 处理post请求，添加单个记录
})
ci_collection_detail = account_views.CiCollectionViewSet.as_view({
    'get': 'retrieve',  # 处理get请求，获取单个记录
    # 'put': 'update',  # 处理put请求，修改单个记录
    'delete': 'destroy',  # 处理delete请求，删除单个记录
})

urlpatterns = [

    # re_path(r'^posts/$', account_views.PostList.as_view()),
    # re_path(r'^posts/(?P<pk>[0-9]+)$', account_views.PostDetail.as_view()),

    # 视图集

    re_path(r'^sign_in/$', SignInView.as_view()),
    re_path(r'^update_password/$', UpdatePasswordView.as_view()),
    re_path(r'^get_qiniu_token/$', account_views.GetQiniuTokenView.as_view()),
    re_path(r'^login/$', account_views.MyTokenObtainPairView.as_view()),

    re_path(r'^posts/$', post_list),
    re_path(r'^posts/(?P<pk>[0-9]+)$', post_detail),

    re_path(r'^follows/$', follow_list),
    re_path(r'^follows/(?P<pk>[0-9]+)$', follow_detail),

    re_path(r'^accounts/$', account_list),
    re_path(r'^accounts/(?P<pk>[0-9]+)$', account_detail),

    re_path(r'^likes/$', like_list),
    re_path(r'^likes/(?P<pk>[0-9]+)$', like_detail),

    re_path(r'^comments/$', comment_list),
    re_path(r'^comments/(?P<pk>[0-9]+)$', comment_detail),

    re_path(r'^shi_collections/$', shi_collection_list),
    re_path(r'^shi_collections/(?P<pk>[0-9]+)$', shi_collection_detail),

    re_path(r'^ci_collections/$', ci_collection_list),
    re_path(r'^ci_collections/(?P<pk>[0-9]+)$', ci_collection_detail),

]


urlpatterns = format_suffix_patterns(urlpatterns)


'''
# 5种方法都开放
urlpatterns += router.urls
'''

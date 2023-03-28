import traceback

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.filters.account_filters import AccountFilter, PostFilter, FollowFilter, LikeFilter, CommentFilter
# from main.filters import PostFilter
from main.models.account_models import Account, Follow, Like, Post, Comment
from django.core.cache import cache

from django.contrib.auth import get_user_model

from main.utils.MyResponse import MyResponse

User = get_user_model()

from main.pagination import MyPageNumberPagination
from main.permissions import IsAuthorOrReadOnly, IsFanOrReadOnly, IsUserOrReadOnly, DelCommentOrReadOnly
from main.serializers.account_serializers import AccountSimpleSerializer, AccountSerializer, \
    FollowSerializer, PostSerializer, LikeSerializer, CommentSerializer, MyTokenObtainPairSerializer

from main.throttles import UserReadRateThrottle, AnonReadRateThrottle

from rest_framework.views import APIView

'''
# blog/views.py
# 使用基础APIView类




class ArticleList(APIView):
    """
    List all articles, or create a new article.
    """
    def get(self, request, format=None):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            # 注意：手动将request.user与author绑定
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetail(APIView):
    """
    Retrieve, update or delete an article instance.
    """
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''


'''

# blog/views.py
# 使用Generic APIView & Mixins
from rest_framework import mixins
from rest_framework import generics

class PostList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # 将request.user与author绑定。调用create方法时执行如下函数。
    def perform_create(self, serializer):
        serializer.save(author=Account.objects.get(id=self.request.user.id))


class PostDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

'''




'''
# generic class-based views
from rest_framework import generics

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class =ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
'''



'''
'''
import random
from django.template import loader
from django.core.mail import EmailMessage
from poetry_system import settings

{
    "email": "909140058@qq.com"
}




# 视图集
# blog/views.py
from rest_framework import viewsets

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     def get_serializer_class(self):
#         if self.action == 'create':
#             return UserSignSerializer
#         elif self.action == 'update':
#             return UserUpdateSerializer
#         return UserSignSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = ([IsAuthenticated, IsAuthorOrReadOnly])
    # permission_classes = ([permissions.IsAuthenticatedOrReadOnly])
    filterset_class = PostFilter
    ordering_fields = ['create_date'] # 排序选项
    ordering = ['-create_date'] # 默认排序
    # throttle_classes = [AnonReadRateThrottle, UserReadRateThrottle] # 针对用户限流

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

# class AccountRViewSet(viewsets.ReadOnlyModelViewSet):
# ReadOnlyModelViewSet仅提供list和detail可读动作
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = ([IsAuthenticated, IsUserOrReadOnly])
    filterset_class = AccountFilter
    ordering_fields = ['id', 'fan_count']  # 排序选项
    ordering = ['id']  # 默认排序


    

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = ([IsAuthenticated, IsFanOrReadOnly])
    # permission_classes = ([permissions.IsAuthenticated])


    filterset_class = FollowFilter

    ordering_fields = ['create_date']  # 排序选项
    ordering = ['-create_date']  # 默认排序

    # throttle_classes = [AnonReadRateThrottle, UserReadRateThrottle] # 针对用户限流
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def perform_create(self, serializer):
        serializer.save(fan_id=self.request.user.id)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = ([IsAuthenticated, IsAuthorOrReadOnly])


    filterset_class = LikeFilter

    ordering_fields = ['create_date']  # 排序选项
    ordering = ['-create_date']  # 默认排序

    # throttle_classes = [AnonReadRateThrottle, UserReadRateThrottle] # 针对用户限流
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = ([IsAuthenticated, DelCommentOrReadOnly])


    filterset_class = CommentFilter

    ordering_fields = ['create_date']  # 排序选项
    ordering = ['-create_date']  # 默认排序

    # throttle_classes = [AnonReadRateThrottle, UserReadRateThrottle] # 针对用户限流
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
                          exception=response.exception, content_type=response.content_type)
    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)



from qiniu import Auth

# 需要填写你的 Access Key 和 Secret Key
access_key = 'y4ZwWAHm_a3nQyt5zoEzVn34CmwWf8jxZR7ca8az'
secret_key = 'fNgZtp243HGNpE-dr5dtffwnnoYxFVzgN-j6-Z8C'
# 构建鉴权对象
def qn_token():
    q = Auth(access_key, secret_key)
    # 要上传的空间，你的存储空间
    bucket_name = 'metric-poetry'
    # 生成上传 Token
    token = q.upload_token(bucket_name)

    return token

# 生成上传七牛云的token
class GetQiniuTokenView(APIView):
    """
    获取七牛云上传token
    """
    permission_classes = ([IsAuthenticated])
    def get(self, request):
        token = qn_token()
        return MyResponse({'qn_token': token}, status=200)


from rest_framework_simplejwt.views import TokenObtainPairView
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
from rest_framework import generics
from django_filters import rest_framework as filters
from main.models.account_models import Account, Follow, Like, Post, Comment, ShiCollection, CiCollection, Work


class AccountFilter(filters.FilterSet):
    email = filters.CharFilter(field_name="email", lookup_expr='exact')
    username = filters.CharFilter(field_name="username", lookup_expr='exact')
    nickname = filters.CharFilter(field_name="nickname", lookup_expr='icontains')
    # avatar_url = filters.CharFilter(field_name="avatar_url", lookup_expr='exact')
    # introduction = filters.CharFilter(field_name="introduction", lookup_expr='icontains')
    display_works = filters.BooleanFilter(field_name="display_works", lookup_expr='exact')
    display_collections = filters.BooleanFilter(field_name="display_collections", lookup_expr='exact')
    min_follow_count = filters.NumberFilter(field_name="follow_count", lookup_expr='gte')
    max_follow_count = filters.NumberFilter(field_name="follow_count", lookup_expr='lte')
    min_fan_count = filters.NumberFilter(field_name="fan_count", lookup_expr='gte')
    max_fan_count = filters.NumberFilter(field_name="fan_count", lookup_expr='lte')
    min_post_count = filters.NumberFilter(field_name="post_count", lookup_expr='gte')
    max_post_count = filters.NumberFilter(field_name="post_count", lookup_expr='lte')



    class Meta:
        model = Account
        fields = []

class PostFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name="author__id", lookup_expr='exact')
    content = filters.CharFilter(field_name="content", lookup_expr='icontains')
    # min_like_count = filters.NumberFilter(field_name="like_count", lookup_expr='gte')
    # max_like_count = filters.NumberFilter(field_name="like_count", lookup_expr='lte')
    # min_comment_count = filters.NumberFilter(field_name="comment_count", lookup_expr='gte')
    # max_comment_count = filters.NumberFilter(field_name="comment_count", lookup_expr='lte')
    create_date = filters.IsoDateTimeFromToRangeFilter(field_name="create_date")
    # 提交 create_date_after 和 create_date_before

    class Meta:
        model = Post
        fields = []

class FollowFilter(filters.FilterSet):
    fan = filters.NumberFilter(field_name="fan__id", lookup_expr='exact')
    follow = filters.NumberFilter(field_name="follow__id", lookup_expr='exact')
    create_date = filters.IsoDateTimeFromToRangeFilter(field_name="create_date")
    # 提交 create_date_after 和 create_date_before

    class Meta:
        model = Follow
        fields = []

class LikeFilter(filters.FilterSet):
    post = filters.NumberFilter(field_name="post__id", lookup_expr='exact')
    author = filters.NumberFilter(field_name="author__id", lookup_expr='exact')
    create_date = filters.IsoDateTimeFromToRangeFilter(field_name="create_date")
    # 提交 create_date_after 和 create_date_before

    class Meta:
        model = Like
        fields = []

class CommentFilter(filters.FilterSet):
    post = filters.NumberFilter(field_name="post__id", lookup_expr='exact')
    author = filters.NumberFilter(field_name="author__id", lookup_expr='exact')
    content = filters.NumberFilter(field_name="content", lookup_expr='icontains')
    create_date = filters.IsoDateTimeFromToRangeFilter(field_name="create_date")
    # 提交 create_date_after 和 create_date_before

    class Meta:
        model = Comment
        fields = []

class ShiCollectionFilter(filters.FilterSet):
    shi = filters.NumberFilter(field_name="shi__id", lookup_expr='exact')
    author = filters.NumberFilter(field_name="author__id", lookup_expr='exact')
    create_date = filters.IsoDateTimeFromToRangeFilter(field_name="create_date")
    # 提交 create_date_after 和 create_date_before

    class Meta:
        model = ShiCollection
        fields = []

class CiCollectionFilter(filters.FilterSet):
    ci = filters.NumberFilter(field_name="ci__id", lookup_expr='exact')
    author = filters.NumberFilter(field_name="author__id", lookup_expr='exact')
    create_date = filters.IsoDateTimeFromToRangeFilter(field_name="create_date")
    # 提交 create_date_after 和 create_date_before

    class Meta:
        model = CiCollection
        fields = []

class WorkFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name="author__id", lookup_expr='exact')
    title = filters.NumberFilter(field_name="title", lookup_expr='icontains')
    content = filters.NumberFilter(field_name="content", lookup_expr='icontains')
    display = filters.BooleanFilter(field_name="display", lookup_expr='exact')
    topping = filters.BooleanFilter(field_name="topping", lookup_expr='exact')
    update_date = filters.IsoDateTimeFromToRangeFilter(field_name="update_date")
    create_date = filters.IsoDateTimeFromToRangeFilter(field_name="create_date")
    # 提交 create_date_after 和 create_date_before

    class Meta:
        model = Work
        fields = []
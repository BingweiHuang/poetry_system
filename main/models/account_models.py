from datetime import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from main.models.poetry_models import Shi, Ci

'''
 用户表
'''
class Account(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(default="", max_length=254)
    username = models.CharField(default="" ,max_length=12)
    nickname = models.CharField(default="" ,max_length=10)
    avatar_url = models.URLField(default="", max_length=255)
    introduction = models.CharField(default="", max_length=30)
    display_works = models.BooleanField(default=True)
    display_collections = models.BooleanField(default=True)
    follow_count = models.IntegerField(default=0)
    fan_count = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)
    follows = models.ManyToManyField("self",symmetrical=False, through='Follow', related_name='fans') # symmetrical:是否对称 through:中间表

    class Meta:
        db_table = 'account'
        ordering = ['id']
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

'''
 关注表(中间表)
'''
class Follow(models.Model):
    fan = models.ForeignKey(Account, related_name='fan', on_delete=models.CASCADE, blank=True, null=True)
    follow = models.ForeignKey(Account, related_name='follow', on_delete=models.CASCADE, blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return "follow:{},fan:{}".format(self.follow, self.fan)

    class Meta:
        db_table = 'follow'
        ordering = ['-create_date']
        verbose_name = "Follow"
        verbose_name_plural = "Follows"

'''
 帖子表
'''
class Post(models.Model):
    author = models.ForeignKey(Account, related_name='post_author', on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(default="", max_length=255)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    create_date = models.DateTimeField(default=timezone.now, blank=False)
    # liked_by = models.ManyToManyField(Account, related_name='liked_by_account', through='Like') # through:中间表
    # commented_by = models.ManyToManyField(Account, related_name='commented_by_account', through='Comment') # through:中间表

    class Meta:
        db_table = 'post'
        ordering = ['-create_date']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

'''
 点赞表(中间表)
'''
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)
    author = models.ForeignKey(Account, related_name='post_like_authors', on_delete=models.CASCADE, blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        db_table = 'like'
        ordering = ['-create_date']
        verbose_name = "Like"
        verbose_name_plural = "Likes"

'''
 评论表(中间表)
'''
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Account, related_name='post_comment_authors', on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(default="", max_length=255)
    create_date = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        db_table = 'comment'
        ordering = ['-create_date']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

class ShiCollection(models.Model):
    shi = models.ForeignKey(Shi, related_name='shi_collection_shis', on_delete=models.CASCADE)
    author = models.ForeignKey(Account, related_name='shi_collection_authors', on_delete=models.CASCADE, blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        db_table = 'shi_collection'
        ordering = ['-create_date']
        verbose_name = "ShiCollection"
        verbose_name_plural = "ShiCollections"

class CiCollection(models.Model):
    ci = models.ForeignKey(Ci, related_name='ci_collection_cis', on_delete=models.CASCADE)
    author = models.ForeignKey(Account, related_name='ci_collection_authors', on_delete=models.CASCADE, blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        db_table = 'ci_collection'
        ordering = ['-create_date']
        verbose_name = "CiCollection"
        verbose_name_plural = "CiCollections"

class Work(models.Model):
    author = models.ForeignKey(Account, related_name='work_author', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=10, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    display = models.BooleanField(default=True) # 是否公开
    topping = models.BooleanField(default=False) # 置顶
    create_date = models.DateTimeField(auto_now_add=True, blank=False)
    update_date = models.DateTimeField(auto_now=True, blank=False)

    class Meta:
        db_table = 'work'
        ordering = ['-topping', '-create_date']
        verbose_name = "Work"
        verbose_name_plural = "Works"
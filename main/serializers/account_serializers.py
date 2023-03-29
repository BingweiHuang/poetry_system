from django.core.validators import RegexValidator, EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from main.models.account_models import Account, Follow, Like, Post, Comment, ShiCollection, CiCollection
from django.forms import model_to_dict

from django.contrib.auth import get_user_model

from main.models.poetry_models import Shi, Ci
from main.serializers.search_serializers import ShiSerializer, CiSerializer

User = get_user_model()

def content_gt_10(value):
    if len(value) < 10:
        raise serializers.ValidationError('内容字符长度不能低于10！')

class AccountSimpleSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField()
    avatar_url = serializers.URLField()

    class Meta:
        model = Account
        fields = ('id', 'nickname', 'avatar_url')
        read_only_fields = ('id', 'nickname', 'avatar_url')

class AccountSerializer(serializers.ModelSerializer):

    # fans = AccountSimpleSerializer(many=True, read_only=True)
    # follows = AccountSimpleSerializer(many=True, read_only=True)

    follow_id = serializers.SerializerMethodField()

    username = serializers.CharField(min_length=4, max_length=12, validators=[UniqueValidator(queryset=Account.objects.all(), message='该账号已经存在！')])
    nickname = serializers.CharField(min_length=1, max_length=10,)
    introduction = serializers.CharField(min_length=1, max_length=30,)


    class Meta:
        model = Account
        fields = ('__all__')
        # exclude = ['follows']
        read_only_fields = ('id', 'user',  'email', 'follow_count', 'fan_count', 'post_count', 'fans', 'follows')

    def get_follow_id(self, obj):
        user_id = self.context['request'].user.id
        res = 0
        if user_id != obj.id:
            qs = Follow.objects.filter(fan_id=user_id, follow_id=obj.id)
            if qs.exists():
                res = model_to_dict(qs[0])['id']
        return res

class FollowSerializer(serializers.ModelSerializer):


    fan = AccountSimpleSerializer(read_only=True)
    follow = AccountSimpleSerializer(read_only=True)

    # 覆盖原Model的字段 都需要显式带上：read_only=True
    # fan = serializers.ReadOnlyField(source='fan.id')
    # follow = serializers.ReadOnlyField(source='follow.id')
    create_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    # 额外的
    follow_id = serializers.IntegerField(required=True, write_only=True)


    class Meta:
        model = Follow
        fields = '__all__'
        extra_fields = ['follow_id']
        read_only_fields = ['id', 'fan', 'follow', 'create_date']

    def validate_follow_id(self, value):

        fan_id = self.context['request'].user.id

        if not Account.objects.filter(id=value).exists():
            raise serializers.ValidationError("被关注者不存在！")

        if fan_id == value:
            raise serializers.ValidationError("不能自己关注自己！")

        if Follow.objects.filter(fan_id=fan_id, follow_id=value).exists():
            raise serializers.ValidationError("已经关注了该用户！")

        return value

    # def create(self, validated_data):
    #     follow = Follow(fan_id=validated_data['fan_id'], follow_id=validated_data['follow_id'])
    #     follow.save()
    #
    #     return follow



class LikeInPostSerializer(serializers.ModelSerializer):
    author = AccountSimpleSerializer(read_only=True)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'author', 'create_date']
        read_only_fields = ['id', 'author', 'create_date']


class CommentInPostSerializer(serializers.ModelSerializer):
    author = AccountSimpleSerializer(read_only=True)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'create_date']
        read_only_fields = ['id', 'author', 'content', 'create_date']


class PostSerializer(serializers.ModelSerializer):
    author = AccountSimpleSerializer(read_only=True)
    content = serializers.CharField(required=True, max_length=255, validators=[content_gt_10])
    liked_by = AccountSimpleSerializer(many=True, read_only=True)
    post_likes = LikeInPostSerializer(many=True, read_only=True)
    post_comments = CommentInPostSerializer(many=True, read_only=True)
    create_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    # post_comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    like_id = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        extra_fields = ['post_likes', 'post_comments']
        read_only_fields = ['id', 'author', 'create_date', 'post_likes', 'post_comments', 'like_count', 'comment_count']

    def validate_content(self, value):
        user_id = self.context['request'].user.id
        if Post.objects.filter(author_id=user_id, content=value).exists():
            raise serializers.ValidationError("您已发表过内容一模一样的帖子！")

        return value

    def get_like_id(self, obj):
        user_id = self.context['request'].user.id
        res = 0
        qs = Like.objects.filter(author_id=user_id, post_id=obj.id)
        if qs.exists():
            res = model_to_dict(qs[0])['id']
        return res

class LikeSerializer(serializers.ModelSerializer):
    # author = AccountSimpleSerializer(read_only=True)
    # post = PostSerializer(read_only=True)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    post_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Like
        fields = ('__all__')
        extra_fields = ['post_id']
        read_only_fields = ('id', 'author', 'post', 'create_date')

    def validate_post_id(self, value):
        user_id = self.context['request'].user.id
        if not Post.objects.filter(id=value).exists():
            raise serializers.ValidationError("该帖子不存在或已被删除！")

        if Like.objects.filter(author_id=user_id, post_id=value).exists():
            raise serializers.ValidationError("您已点赞过该帖子！")

        return value


class CommentSerializer(serializers.ModelSerializer):
    author = AccountSimpleSerializer(read_only=True)
    # post = serializers.ReadOnlyField(source="post.id")
    content = serializers.CharField(min_length=1, max_length=255)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    post_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_fields = ['post_id']
        read_only_fields = ['author', 'post', 'create_date']

    def validate_post_id(self, value):
        if not Post.objects.filter(id=value).exists():
            raise serializers.ValidationError("该帖子不存在或已被删除！")

        return value

    def validate(self, attrs):
        user_id = self.context['request'].user.id

        if Comment.objects.filter(author_id=user_id, post_id=attrs['post_id'], content=attrs['content']).exists():
            raise serializers.ValidationError("不能对同一帖子进行内容相同的评论！")

        return attrs

class ShiCollectionSerializer(serializers.ModelSerializer):
    # author = AccountSimpleSerializer(read_only=True)
    shi = ShiSerializer(read_only=True)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    shi_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = ShiCollection
        fields = ('__all__')
        extra_fields = ['shi_id']
        read_only_fields = ('id', 'author', 'shi', 'create_date')

    def validate_shi_id(self, value):
        user_id = self.context['request'].user.id
        if not Shi.objects.filter(id=value).exists():
            raise serializers.ValidationError("该诗不存在！")

        if ShiCollection.objects.filter(author_id=user_id, shi_id=value).exists():
            raise serializers.ValidationError("您已收藏过该诗！")

        return value

class CiCollectionSerializer(serializers.ModelSerializer):
    # author = AccountSimpleSerializer(read_only=True)
    ci = CiSerializer(read_only=True)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    ci_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = CiCollection
        fields = ('__all__')
        extra_fields = ['ci_id']
        read_only_fields = ('id', 'author', 'ci', 'create_date')

    def validate_ci_id(self, value):
        user_id = self.context['request'].user.id
        if not Ci.objects.filter(id=value).exists():
            raise serializers.ValidationError("该诗不存在！")

        if CiCollection.objects.filter(author_id=user_id, ci_id=value).exists():
            raise serializers.ValidationError("您已收藏过该诗！")

        return value


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # print(user)
        # 添加额外信息
        token['email'] = user.email
        return token
from django.core.validators import RegexValidator, EmailValidator
from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from main.models.poetry_models import Ci, Shi, Fly, WordFrequency, Shijing
from main.models.account_models import Post, ShiCollection, CiCollection
from django.core.cache import cache

from django.contrib.auth import get_user_model

User = get_user_model()

class CiSerializer(serializers.ModelSerializer):

    collection_id = serializers.SerializerMethodField()

    class Meta:
        model = Ci
        fields = '__all__'

    def get_collection_id(self, obj):
        user_id = self.context['request'].user.id
        res = 0
        if user_id:
            qs = CiCollection.objects.filter(author_id=user_id, ci_id=obj.id)
            if qs.exists():
                res = model_to_dict(qs[0])['id']
        return res

class ShiSerializer(serializers.ModelSerializer):

    content = serializers.SerializerMethodField()
    collection_id = serializers.SerializerMethodField()

    class Meta:
        model = Shi
        fields = '__all__'

    def get_content(self, obj):
        return obj.content.split('\n')[:-1]

    def get_collection_id(self, obj):
        user_id = self.context['request'].user.id
        res = 0
        if user_id:
            qs = ShiCollection.objects.filter(author_id=user_id, shi_id=obj.id)
            if qs.exists():
                res = model_to_dict(qs[0])['id']
        return res

class FlySerializer(serializers.ModelSerializer):


    class Meta:
        model = Fly
        fields = '__all__'

class ShijingSerializer(serializers.ModelSerializer):


    class Meta:
        model = Shijing
        fields = '__all__'
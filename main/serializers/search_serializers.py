from django.core.validators import RegexValidator, EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from main.models.poetry_models import Ci, Shi, Fly, WordFrequency, Shijing
from main.models.account_models import Post
from django.core.cache import cache

from django.contrib.auth import get_user_model

User = get_user_model()

class CiSerializer(serializers.ModelSerializer):


    class Meta:
        model = Ci
        fields = '__all__'

class ShiSerializer(serializers.ModelSerializer):

    content = serializers.SerializerMethodField()

    class Meta:
        model = Shi
        fields = '__all__'

    def get_content(self, obj):
        return obj.content.split('\n')[:-1]

class FlySerializer(serializers.ModelSerializer):


    class Meta:
        model = Fly
        fields = '__all__'

class ShijingSerializer(serializers.ModelSerializer):


    class Meta:
        model = Shijing
        fields = '__all__'
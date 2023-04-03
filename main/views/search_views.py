import datetime

from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from main.filters.search_filters import CiFilter, ShiFilter, FlyFilter, ShijingFilter
from main.models.poetry_models import Ci, Shi, Fly, WordFrequency, Shijing

from main.serializers.search_serializers import CiSerializer, ShiSerializer, FlySerializer, ShijingSerializer


class CiViewSet(viewsets.ModelViewSet):
    queryset = Ci.objects.all()
    serializer_class = CiSerializer
    filterset_class = CiFilter
    ordering_fields = ['id']  # 排序选项
    ordering = ['id']  # 默认排序

    def get_queryset(self):
        arg = self.request.GET
        content = arg.get("content")

        qs = Ci.objects.all()

        if content:  # content 有多个关键字
            keyword_list = set(content.split(' '))
            for keyword in keyword_list:
                if keyword != '':
                    qs = qs.filter(content__contains=keyword)

        return qs

class ShiViewSet(viewsets.ModelViewSet):
    queryset = Shi.objects.all()
    serializer_class = ShiSerializer
    filterset_class = ShiFilter
    ordering_fields = ['id']  # 排序选项
    ordering = ['id']  # 默认排序

    def get_queryset(self):
        arg = self.request.GET
        content = arg.get("content")

        qs = Shi.objects.all()

        if content:  # content 有多个关键字
            keyword_list = set(content.split(' '))
            for keyword in keyword_list:
                if keyword != '':
                    qs = qs.filter(content__contains=keyword)

        return qs


class FlyViewSet(viewsets.ModelViewSet):
    queryset = Fly.objects.all()
    serializer_class = FlySerializer
    filterset_class = FlyFilter
    ordering_fields = ['id']  # 排序选项
    ordering = ['id']  # 默认排序

    permission_classes = ([IsAuthenticated])

    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)
    #     return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
    #                       exception=response.exception, content_type=response.content_type)

    @method_decorator(cache_page(60 * 60 * 2)) # 两小时缓存
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        # response["Expires"] = datetime.datetime.now()
        return response

    # def update(self, request, *args, **kwargs):
    #     response = super().update(request, *args, **kwargs)
    #     return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
    #                       exception=response.exception, content_type=response.content_type)
    #
    # def destroy(self, request, *args, **kwargs):
    #     response = super().destroy(request, *args, **kwargs)
    #     return MyResponse(data=response.data, status=response.status_code, template_name=response.template_name,
    #                       exception=response.exception, content_type=response.content_type)

    @method_decorator(cache_page(60 * 60 * 2)) # 两小时缓存
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # response["Expires"] = datetime.datetime.now()
        return response

    def get_queryset(self):
        arg = self.request.GET
        have = arg.get("have")
        no_have = arg.get("no_have")

        qs = Fly.objects.all()

        if have:  # have 有多个关键字
            keyword_list = set(have.split(' '))
            for keyword in keyword_list:
                if keyword != '':
                    qs = qs.filter(content__contains=keyword)  # 含有

        if no_have:  # no_have 有多个关键字
            keyword_list = set(no_have.split(' '))
            for keyword in keyword_list:
                if keyword != '':
                    qs = qs.filter(~Q(content__contains=keyword))  # 不含有

        return qs


class ShijingViewSet(viewsets.ModelViewSet):
    queryset = Shijing.objects.all()
    serializer_class = ShijingSerializer
    filterset_class = ShijingFilter
    ordering_fields = ['id']  # 排序选项
    ordering = ['id']  # 默认排序

    def get_queryset(self):
        arg = self.request.GET
        content = arg.get("content")

        qs = Shijing.objects.all()

        if content:  # content 有多个关键字
            keyword_list = set(content.split(' '))
            for keyword in keyword_list:
                if keyword != '':
                    qs = qs.filter(content__contains=keyword)

        return qs
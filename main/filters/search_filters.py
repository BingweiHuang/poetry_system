from rest_framework import generics
from django_filters import rest_framework as filters
from main.models.poetry_models import Ci, Shi, Fly, WordFrequency, Shijing


class CiFilter(filters.FilterSet):

    rhythmic = filters.CharFilter(field_name="rhythmic", lookup_expr='icontains')
    dynasty = filters.CharFilter(field_name="dynasty", lookup_expr='exact')
    author = filters.CharFilter(field_name="author", lookup_expr='exact')
    complete = filters.BooleanFilter(field_name="complete", lookup_expr='exact')
    # content = filters.CharFilter(field_name="content", lookup_expr='icontains')
    three_hundred = filters.BooleanFilter(field_name="three_hundred", lookup_expr='exact')

    class Meta:
        model = Ci
        fields = []

class ShiFilter(filters.FilterSet):

    title = filters.CharFilter(field_name="title", lookup_expr='icontains')
    dynasty = filters.CharFilter(field_name="dynasty", lookup_expr='exact')
    author = filters.CharFilter(field_name="author", lookup_expr='exact')
    # content = filters.CharFilter(field_name="content", lookup_expr='icontains')
    yan = filters.NumberFilter(field_name="yan", lookup_expr='exact')
    rhyme_type = filters.NumberFilter(field_name="rhyme_type", lookup_expr='exact')
    rhyme = filters.CharFilter(field_name="rhyme", lookup_expr='exact')
    metric = filters.BooleanFilter(field_name="metric", lookup_expr='exact')
    jue = filters.NumberFilter(field_name="jue", lookup_expr='exact')
    qi = filters.BooleanFilter(field_name="qi", lookup_expr='exact')
    ru = filters.BooleanFilter(field_name="ru", lookup_expr='exact')
    three_hundred = filters.BooleanFilter(field_name="three_hundred", lookup_expr='exact')

    class Meta:
        model = Shi
        fields = []

class FlyFilter(filters.FilterSet):

    kind = filters.NumberFilter(field_name="kind", lookup_expr='exact')
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')
    dynasty = filters.CharFilter(field_name="dynasty", lookup_expr='exact')
    author = filters.CharFilter(field_name="author", lookup_expr='exact')
    # content = filters.CharFilter(field_name="content", lookup_expr='icontains')
    fly_number = filters.BooleanFilter(field_name="fly_number", lookup_expr='exact')
    fly_season = filters.BooleanFilter(field_name="fly_season", lookup_expr='exact')
    fly_position = filters.BooleanFilter(field_name="fly_position", lookup_expr='exact')
    fly_weather = filters.BooleanFilter(field_name="fly_weather", lookup_expr='exact')
    fly_color = filters.BooleanFilter(field_name="fly_color", lookup_expr='exact')
    fly_wine_vessel = filters.BooleanFilter(field_name="fly_wine_vessel", lookup_expr='exact')
    fly_reduplicate = filters.BooleanFilter(field_name="fly_reduplicate", lookup_expr='exact')

    class Meta:
        model = Fly
        fields = []

class ShijingFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='exact')
    section = filters.CharFilter(field_name="section", lookup_expr='exact')
    chapter = filters.CharFilter(field_name="chapter", lookup_expr='exact')
    # content = filters.CharFilter(field_name="content", lookup_expr='icontains')

    class Meta:
        model = Shijing
        fields = []
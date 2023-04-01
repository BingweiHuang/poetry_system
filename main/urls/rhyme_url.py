# blog/urls.py

from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from main.views.rhyme_views import AllRhymeView
from main.views.rhyme_views import GetRhymeView
from main.views.rhyme_views import SearchRhymeView
from main.views.rhyme_views import FirstSentenceView
from main.views.rhyme_views import MetricPoetryView

urlpatterns = [

    re_path(r'^all_rhyme/$', AllRhymeView.as_view()),
    re_path(r'^get_rhyme/$', GetRhymeView.as_view()),
    re_path(r'^search_rhyme/$', SearchRhymeView.as_view()),
    re_path(r'^first_sentence/$', FirstSentenceView.as_view()),
    re_path(r'^metric_poetry/$', MetricPoetryView.as_view()),

]


urlpatterns = format_suffix_patterns(urlpatterns)


'''
# 5种方法都开放
urlpatterns += router.urls
'''

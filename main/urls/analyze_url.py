# blog/urls.py

from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from main.views.analyze.word_list_view import WordListView
from main.views.analyze.word_frequency_view import WordFrequencyView
from main.views.analyze.rhythmic_statistics_view import RhythmicStatisticsView
from main.views.analyze.poetry_statistics_view import PoetryRhymeStatisticsView, PoetryStyleStatisticsView
from main.views.analyze.author_output_view import AuthorOutputView

urlpatterns = [

    re_path(r'^word_list/$', WordListView.as_view()),
    re_path(r'^word_frequency/$', WordFrequencyView.as_view()),
    re_path(r'^rhythmic_statistics/$', RhythmicStatisticsView.as_view()),
    re_path(r'^poetry_rhyme_statistics/$', PoetryRhymeStatisticsView.as_view()),
    re_path(r'^poetry_style_statistics/$', PoetryStyleStatisticsView.as_view()),
    re_path(r'^author_output/$', AuthorOutputView.as_view()),

]


urlpatterns = format_suffix_patterns(urlpatterns)


'''
# 5种方法都开放
urlpatterns += router.urls
'''

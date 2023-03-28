import traceback

from django.forms import model_to_dict
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models.poetry_models import WordFrequency
from main.permissions import IsAuthorOrReadOnly
from main.utils.MyResponse import MyResponse

avi_l = [
    ['n', 's', 'nr', 'ns', 'nt', 'nl', 'ng', 'nz', 'm'], # 单字 多字
    ['n', 's', 'nr', 'ns', 'nt', 'nl', 'ng', 'nz', 'm'], # 单字 多字
    ['v', 'vg', 'vd', 'vn', 'vf', 'vx', 'vi'], # 动词
    ['a', 'ag', 'ad', 'al', 'an'], # 形容词
    ['ns', 'nsf'], # 地名
]

class WordFrequencyView(APIView):
    permission_classes = ([IsAuthorOrReadOnly])

    # /analyze/word_frequency?num=5&dynasty=5&word_len=2&phrase=a ag ad al an

    # 0：毛泽东诗词 1：纳兰性德词 2：宋词 3：五代词 4：宋诗 5：唐诗 6：王国维词 7：诗经
    def get(self, request):
        arg = request.GET
        try:
            num = arg.get("num", 100)
            phrase = arg.get("phrase")
            dynasty = arg.get("dynasty")
            word_len = int(arg.get("word_len", -1))

            kwargs = {}

            # print(num, phrase, dynasty, word_len)
            if phrase:  # phrase 有多个关键字
                phrase_list = set(phrase.split(' '))
                kwargs["phrase__in"] = phrase_list
            if dynasty:
                kwargs["dynasty"] = dynasty
            if word_len == 1:
                kwargs["word_len"] = word_len
            elif word_len == 2:
                kwargs["word_len__gte"] = word_len

            qs = WordFrequency.objects.filter(**kwargs).filter(~Q(word__in=['一', '...'])).order_by('-num')

            word_list = [model_to_dict(word) for word in qs]
            word_list = [{'name': word['word'], 'value': word['num']} for word in word_list[:int(num)]]

            datas = {
                "word_list": word_list,
            }

            return MyResponse(datas, 200)
        except Exception as e:
            traceback.print_exc()
            return MyResponse({'result': "查询失败"} ,status=500)

    def post(self, request):
        arg = request.POST
        try:
            num = arg.get("num", 100)
            phrase = arg.get("phrase")
            dynasty = arg.get("dynasty")
            word_len = int(arg.get("word_len", -1))

            kwargs = {}

            # print(num, phrase, dynasty, word_len)
            if phrase:  # phrase 有多个关键字
                phrase_list = set(phrase.split(' '))
                kwargs["phrase__in"] = phrase_list
            if dynasty:
                kwargs["dynasty"] = dynasty
            if word_len == 1:
                kwargs["word_len"] = word_len
            elif word_len == 2:
                kwargs["word_len__gte"] = word_len

            qs = WordFrequency.objects.filter(**kwargs).filter(~Q(word__in=['一', '...'])).order_by('-num')

            word_list = [model_to_dict(word) for word in qs]
            word_list = [{'name': word['word'], 'value': word['num']} for word in word_list[:int(num)]]

            datas = {
                "word_list": word_list,
            }

            return MyResponse(datas, 200)
        except Exception as e:
            traceback.print_exc()
            return MyResponse({'result': "查询失败"} ,status=500)
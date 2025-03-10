import traceback

from django.forms import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from main.models.poetry_models import Shi, Shijing
from main.models.poetry_models import Ci
from rest_framework.response import Response

from main.permissions import StaffOnly


class WordListView(APIView):
    permission_classes = ([IsAuthenticated, StaffOnly])

    # def get_permissions(self):


    # /analyze/word_list?author=毛泽东&dynasty=近现代&word_list=春 夏 秋 冬
    # /analyze/word_list?author=毛泽东&dynasty=近现代&word_list=红旗 人民
    # /analyze/word_list?author=苏轼&dynasty=宋代&shici=shi&word_list=春 夏 秋 冬
    # /analyze/word_list?dynasty=宋代&shici=shi&word_list=春秋 江山 落花 乾坤

    @method_decorator(cache_page(60 * 60 * 24 * 2))  # 14天
    def get(self, request):
        arg = request.GET
        try:
            word_list = arg.get("word_list")
            author = arg.get("author")
            dynasty = arg.get("dynasty")
            shici = arg.get("shici")

            word_dict = {}
            if word_list:  # word_list 有多个关键字
                keyword_list = set(word_list.split(' '))
                for keyword in keyword_list:
                    if keyword != '':
                        word_dict[keyword] = 0

            if len(word_dict) > 6:
                return Response({"result": "词数必须在[1,6]！"}, 400)

            kwargs = {}

            if author and author != '':
                kwargs["author"] = author
            if dynasty and dynasty != '':
                kwargs["dynasty"] = dynasty

            if dynasty == '近现代' and author == '毛泽东':
                qs = Shi.objects.filter(**kwargs)
                qs2 = Ci.objects.filter(**kwargs)

                the_list = [model_to_dict(poem) for poem in qs]
                the_list += [model_to_dict(poem) for poem in qs2]

            elif dynasty == '不限':
                the_list = []
                models = [Ci, Shi, Shijing]
                for model in models:
                    the_list += [model_to_dict(poem) for poem in model.objects.all()]

            else:
                if shici == 'shi':
                    the_model = Shi
                elif shici == 'ci':
                    the_model = Ci
                elif shici == 'shijing':
                    the_model = Shijing

                the_list = [model_to_dict(poem) for poem in the_model.objects.filter(**kwargs)]


            for poem in the_list:
                for word in word_dict:
                    word_dict[word] += poem['content'].count(word)

            res_list = [{'name': key, 'value': word_dict[key]} for key in word_dict.keys()]
            datas = {
                # "word_dict": word_dict.sort(key=lambda x: x[1]),
                "word_list": sorted(res_list, key = lambda x:x['value'], reverse=True),
            }

            '''
            print(datas['word_list'])
            '''


            return Response(datas, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'result': "查询失败"} ,status=500)
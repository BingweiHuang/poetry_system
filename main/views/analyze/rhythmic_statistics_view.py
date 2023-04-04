import traceback

from django.forms import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from collections import Counter


from main.models.poetry_models import Ci


class RhythmicStatisticsView(APIView):
    permission_classes = ([IsAuthenticated])

    # /analyze/rhythmic_statistics?author=苏轼&dynasty=宋代&num=10
    # /analyze/rhythmic_statistics?author=李煜&dynasty=五代&num=10
    # /analyze/rhythmic_statistics?author=李清照&dynasty=宋代&num=10
    # /analyze/rhythmic_statistics?author=毛泽东&dynasty=近现代&num=10
    # /analyze/rhythmic_statistics?dynasty=近现代&num=10
    # /analyze/rhythmic_statistics?dynasty=宋代&num=10
    # /analyze/rhythmic_statistics?dynasty=五代&num=10

    @method_decorator(cache_page(60 * 60 * 24 * 14))  # 14天
    def get(self, request):
        arg = request.GET
        try:
            author = arg.get("author", "")
            dynasty = arg.get("dynasty")
            num = arg.get("num", 100)

            kwargs = {}

            if author and author != '':
                kwargs["author"] = author
            if dynasty and dynasty != '不限':
                kwargs["dynasty"] = dynasty

            qs = Ci.objects.filter(**kwargs)
            the_list = [model_to_dict(poem) for poem in qs]

            rhythmic_List = [poem['rhythmic'].split('·')[0] for poem in the_list]
            counter = Counter(rhythmic_List)
            count_pairs = counter.most_common()
            count_pairs = [{'name': i[0], 'value': i[1]} for i in count_pairs[:int(num)]]

            '''
            print(count_pairs)
            '''

            datas = {
                # "word_dict": word_dict.sort(key=lambda x: x[1]),
                "word_list": count_pairs,
            }

            return Response(datas, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "查询失败"} ,status=500)

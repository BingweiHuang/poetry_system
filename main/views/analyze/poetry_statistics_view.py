import traceback

from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models.poetry_models import Shi
from main.permissions import IsAuthorOrReadOnly


class PoetryStatisticsView(APIView):
    permission_classes = ([IsAuthorOrReadOnly])

    # /analyze/poetry_statistics?author=苏轼&dynasty=宋代&num=10&mode=0
    # /analyze/poetry_statistics?author=苏轼&dynasty=宋代&num=10&mode=1
    # /analyze/poetry_statistics?author=苏轼&dynasty=宋代&num=10&mode=2
    # /analyze/poetry_statistics?dynasty=宋代&num=10&mode=0
    # /analyze/poetry_statistics?dynasty=唐代&num=10&mode=0
    # /analyze/poetry_statistics?dynasty=近现代&num=10&mode=0

    def get(self, request):
        arg = request.GET
        try:
            author = arg.get("author")
            dynasty = arg.get("dynasty")
            rhyme_num = int(arg.get("rhyme_num", 10))

            if rhyme_num > 20 or rhyme_num < 5:
                return Response({"result": "韵脚数必须在[5,15]！"}, status=400)

            kwargs = {}

            if author and author != '':
                kwargs["author"] = author
            if dynasty and dynasty != '不限朝代':
                kwargs["dynasty"] = dynasty

            qs = Shi.objects.filter(**kwargs) # 按条件筛

            res_list = []

            # 统计古近体诗
            gu = qs.filter(metric=0).count()
            jin = qs.filter(metric=1).count()
            res_list.append([{'name': '古体诗', 'value': gu}, {'name': '近体诗', 'value': jin}])

            # 统计诗的韵脚
            qs2 = qs.values('rhyme').filter(~Q(rhyme='')).annotate(num=Count('id')).order_by('-num', 'rhyme')
            count_pairs = [{'name': poem['rhyme'], 'value': poem['num']} for poem in qs2]
            if rhyme_num:
                count_pairs = count_pairs[:int(rhyme_num)]
            res_list.append(count_pairs)

            # 统计诗的言绝
            qs2 = qs.values('yan', 'jue').filter(metric=1).annotate(num=Count('id')).order_by('-num')
            count_pairs = [[(poem['yan'], poem['jue']), poem['num']] for poem in qs2]
            the_list = [{'name': '古体诗', 'value': gu}]
            for pair in count_pairs:
                yan = '七言' if pair[0][0] == 7 else '五言'
                jue = '绝句' if pair[0][1] == 0 else ('律诗' if pair[0][1] == 1 else '排律')
                the_list.append({'name': yan + jue, 'value': pair[1]})

            res_list.append(the_list)


            datas = {
                "res_list": res_list,
            }

            return Response(datas, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "查询失败"} ,status=500)

    def post(self, request):
        arg = request.POST
        try:
            author = arg.get("author")
            dynasty = arg.get("dynasty")
            rhyme_num = int(arg.get("rhyme_num", 10))

            if rhyme_num > 20 or rhyme_num < 5:
                return Response({"result": "韵脚数必须在[5,15]！"}, 400)

            kwargs = {}

            if author and author != '':
                kwargs["author"] = author
            if dynasty and dynasty != '不限朝代':
                kwargs["dynasty"] = dynasty

            qs = Shi.objects.filter(**kwargs) # 按条件筛

            res_list = []

            # 统计古近体诗
            gu = qs.filter(metric=0).count()
            jin = qs.filter(metric=1).count()
            res_list.append([{'name': '古体诗', 'value': gu}, {'name': '近体诗', 'value': jin}])

            # 统计诗的韵脚
            qs2 = qs.values('rhyme').filter(~Q(rhyme='')).annotate(num=Count('id')).order_by('-num', 'rhyme')
            count_pairs = [{'name': poem['rhyme'], 'value': poem['num']} for poem in qs2]
            if rhyme_num:
                count_pairs = count_pairs[:int(rhyme_num)]
            res_list.append(count_pairs)

            # 统计诗的言绝
            qs2 = qs.values('yan', 'jue').filter(metric=1).annotate(num=Count('id')).order_by('-num')
            count_pairs = [[(poem['yan'], poem['jue']), poem['num']] for poem in qs2]
            the_list = [{'name': '古体诗', 'value': gu}]
            for pair in count_pairs:
                yan = '七言' if pair[0][0] == 7 else '五言'
                jue = '绝句' if pair[0][1] == 0 else ('律诗' if pair[0][1] == 1 else '排律')
                the_list.append({'name': yan + jue, 'value': pair[1]})

            res_list.append(the_list)


            datas = {
                "res_list": res_list,
            }

            return Response(datas, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'result': "查询失败"} ,status=500)

import traceback

from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models.poetry_models import Shi

class PoetryStyleStatisticsView(APIView):
    permission_classes = ([IsAuthenticated])

    @method_decorator(cache_page(60 * 60 * 24 * 2))  # 14天
    def get(self, request):
        arg = request.GET
        try:
            author = arg.get("author")
            dynasty = arg.get("dynasty")

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

            # 统计诗的言绝
            qs2 = qs.values('yan', 'jue').filter(metric=1).annotate(num=Count('id')).order_by('-num')
            count_pairs = [[(poem['yan'], poem['jue']), poem['num']] for poem in qs2]
            the_list = [{'name': '古体诗', 'value': gu}]
            for pair in count_pairs:
                yan = '七言' if pair[0][0] == 7 else '五言'
                jue = '绝句' if pair[0][1] == 0 else ('律诗' if pair[0][1] == 1 else '排律')
                the_list.append({'name': yan + jue, 'value': pair[1]})

            res_list.append(the_list)

            '''
            print(res_list[0])
            print(res_list[1])
            '''


            datas = {
                "res_list": res_list,
            }

            return Response(datas, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "查询失败"} ,status=500)

class PoetryRhymeStatisticsView(APIView):
    permission_classes = ([IsAuthenticated])

    @method_decorator(cache_page(60 * 60 * 24 * 3))  # 14天
    def get(self, request):
        arg = request.GET
        try:
            author = arg.get("author")
            dynasty = arg.get("dynasty")
            rhyme_num = int(arg.get("rhyme_num", 8))

            print(rhyme_num)

            if rhyme_num > 15 or rhyme_num < 5:
                return Response({"result": "韵脚数必须在[5,15]！"}, status=400)

            kwargs = {}

            if author and author != '':
                kwargs["author"] = author
            if dynasty and dynasty != '不限朝代':
                kwargs["dynasty"] = dynasty

            qs = Shi.objects.exclude(rhyme__isnull=True).filter(**kwargs) # 按条件筛
            # 统计诗的韵脚
            qs2 = qs.values('rhyme').annotate(num=Count('id')).order_by('-num', 'rhyme')
            count_pairs = [{'name': poem['rhyme'], 'value': poem['num']} for poem in qs2]
            count_pairs = count_pairs[:rhyme_num]

            '''
            print(count_pairs)
            '''


            datas = {
                "count_pairs": count_pairs,
            }

            return Response(datas, 200)
        except Exception as e:
            traceback.print_exc()
            return Response({'msg': "查询失败"} ,status=500)
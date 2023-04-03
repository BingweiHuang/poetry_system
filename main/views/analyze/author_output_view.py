import traceback

from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models.poetry_models import Shi
from main.models.poetry_models import Ci
from main.permissions import IsAuthorOrReadOnly


class AuthorOutputView(APIView):
    permission_classes = ([IsAuthorOrReadOnly])

    # /analyze/author_output?dynasty=唐代&num=10&shici=shi

    def get(self, request):
        arg = request.GET
        try:
            num = int(arg.get("num", 10))
            dynasty = arg.get("dynasty")
            metric = arg.get("metric")
            yan = arg.get("yan")
            jue = arg.get("jue")
            three_hundred = arg.get("three_hundred")

            if num > 20 or num < 5:
                return Response({"result": "人数必须在[5,20]！"}, status=400)

            kwargs = {}

            if metric is not None:
                metric = int(metric)
                if metric != -1:
                    kwargs["metric"] = metric
            if yan is not None:
                yan = int(yan)
                if yan != -1:
                    kwargs["yan"] = yan
            if jue is not None:
                jue = int(jue)
                if jue != -1:
                    kwargs["jue"] = jue
            if three_hundred is not None:
                three_hundred = int(three_hundred)
                if three_hundred == 1:
                    kwargs["three_hundred"] = three_hundred


            if dynasty == '宋词':
                kwargs["dynasty"] = '宋代'
                the_model = Ci
            elif dynasty== '唐诗':
                kwargs["dynasty"] = '唐代'
                the_model = Shi
            elif dynasty== '宋诗':
                kwargs["dynasty"] = '宋代'
                the_model = Shi

            qs = the_model.objects.values('author').filter(~Q(author__in=['无名氏', '不详', '郊庙朝会歌辞']), **kwargs).annotate(num=Count('id')).order_by('-num') # 按条件筛
            # qs = the_model.objects.values('author').filter(**kwargs).annotate(num=Count('id')).order_by('-num') # 按条件筛
            the_list = [[poem['author'], poem['num']] for poem in qs[:int(num)]]
            the_list.sort(key=lambda x: x[1], reverse=False)

            res_list = []
            author_list = [i[0] for i in the_list]


            if the_model == Ci:
                qs2 = the_model.objects.values('author', 'complete').filter(author__in=author_list, **kwargs).annotate(num=Count('id')).order_by('-num')

                the_list1 = []
                the_list2 = []
                author2complete1 = {}
                author2complete0 = {}
                for author in author_list:  # 初始化 author2num
                    author2complete1[author] = 0
                    author2complete0[author] = 0

                for item in qs2:
                    if item['complete'] == 1:
                        author2complete1[item['author']] = item['num']
                    elif item['complete'] == 0:
                        author2complete0[item['author']] = item['num']

                for author in author_list:
                    the_list1.append([author, author2complete1[author]])
                    the_list2.append([author, author2complete0[author]])

                res_list.append(the_list1)  # 完整
                res_list.append(the_list2)  # 缺字
                pass
            else:
                if metric == -1 and yan == -1 and jue == -1: # 格律 几言 诗体 全不限
                    # print('走的全不限')
                    qs2 = the_model.objects.values('author', 'metric').filter(author__in=author_list,
                                                                    **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []
                    author2metric1 = {}
                    author2metric0 = {}
                    for author in author_list:  # 初始化 author2num
                        author2metric1[author] = 0
                        author2metric0[author] = 0

                    for item in qs2:
                        if item['metric'] == 1:
                            author2metric1[item['author']] = item['num']
                        elif item['metric'] == 0:
                            author2metric0[item['author']] = item['num']

                    for author in author_list:
                        the_list1.append([author, author2metric1[author]])
                        the_list2.append([author, author2metric0[author]])

                    res_list.append(the_list1)  # 近体
                    res_list.append(the_list2)  # 古体

                elif yan == -1 and jue == -1: # 只选格律
                    # print('走的只选格律')
                    qs2 = the_model.objects.values('author', 'yan', 'jue').filter(author__in=author_list,
                                                                                  **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []
                    the_list3 = []
                    the_list4 = []
                    the_list5 = []
                    the_list6 = []
                    author2yan7_jue0 = {}
                    author2yan7_jue1 = {}
                    author2yan7_jue2 = {}
                    author2yan5_jue0 = {}
                    author2yan5_jue1 = {}
                    author2yan5_jue2 = {}

                    author2yan_jue3 = {}

                    for author in author_list:  # 初始化 author2num
                        author2yan7_jue0[author] = 0
                        author2yan7_jue1[author] = 0
                        author2yan7_jue2[author] = 0
                        author2yan5_jue0[author] = 0
                        author2yan5_jue1[author] = 0
                        author2yan5_jue2[author] = 0

                        author2yan_jue3[author] = 0


                    if int(metric) == 1: # 选了近体诗
                        for item in qs2:
                            if item['yan'] == 7 and item['jue'] == 0:
                                author2yan7_jue0[item['author']] = item['num']
                            elif item['yan'] == 7 and item['jue'] == 1:
                                author2yan7_jue1[item['author']] = item['num']
                            elif item['yan'] == 7 and item['jue'] == 2:
                                author2yan7_jue2[item['author']] = item['num']
                            elif item['yan'] == 5 and item['jue'] == 0:
                                author2yan5_jue0[item['author']] = item['num']
                            elif item['yan'] == 5 and item['jue'] == 1:
                                author2yan5_jue1[item['author']] = item['num']
                            elif item['yan'] == 5 and item['jue'] == 2:
                                author2yan5_jue2[item['author']] = item['num']

                        for author in author_list:
                            the_list1.append([author, author2yan7_jue0[author]])
                            the_list2.append([author, author2yan7_jue1[author]])
                            the_list3.append([author, author2yan7_jue2[author]])
                            the_list4.append([author, author2yan5_jue0[author]])
                            the_list5.append([author, author2yan5_jue1[author]])
                            the_list6.append([author, author2yan5_jue2[author]])

                        res_list.append(the_list1)  # 七绝
                        res_list.append(the_list2)  # 七律
                        res_list.append(the_list3)  # 七排
                        res_list.append(the_list4)  # 五绝
                        res_list.append(the_list5)  # 五律
                        res_list.append(the_list6)  # 五排

                    elif int(metric) == 0: # 选了古体诗
                        for item in qs2:
                            if item['yan'] == 7 and item['jue'] == 0:
                                author2yan7_jue0[item['author']] = item['num']
                            elif item['yan'] == 7 and item['jue'] == 1:
                                author2yan7_jue1[item['author']] = item['num']
                            elif item['yan'] == 5 and item['jue'] == 0:
                                author2yan5_jue0[item['author']] = item['num']
                            elif item['yan'] == 5 and item['jue'] == 1:
                                author2yan5_jue1[item['author']] = item['num']
                            else:
                                author2yan_jue3[item['author']] += item['num']

                        for author in author_list:
                            the_list1.append([author, author2yan7_jue0[author]])
                            the_list2.append([author, author2yan7_jue1[author]])
                            the_list3.append([author, author2yan5_jue0[author]])
                            the_list4.append([author, author2yan5_jue1[author]])
                            the_list5.append([author, author2yan_jue3[author]])

                            the_list6.append([author, 0]) # 滥竽充数的 为了保持res_list长度一致

                        res_list.append(the_list1)  # 七绝
                        res_list.append(the_list2)  # 七律
                        res_list.append(the_list3)  # 五绝
                        res_list.append(the_list4)  # 五律
                        res_list.append(the_list5)  # 其他

                        res_list.append(the_list6)  # 滥竽充数

                elif metric == -1 and jue == -1: # 只选几言
                    # print('走的只选几言')
                    qs2 = the_model.objects.values('author', 'metric', 'jue').filter(author__in=author_list,
                                                                                  **kwargs).annotate(num=Count('id')).order_by('-num')

                    the_list1 = []
                    the_list2 = []
                    the_list3 = []
                    the_list4 = []
                    the_list5 = []
                    the_list6 = []

                    author2metric1_jue0 = {}
                    author2metric1_jue1 = {}
                    author2metric1_jue2 = {}
                    author2metric0_jue0 = {}
                    author2metric0_jue1 = {}
                    author2metric0_jue3 = {}

                    for author in author_list:  # 初始化 author2num
                        author2metric1_jue0[author] = 0
                        author2metric1_jue1[author] = 0
                        author2metric1_jue2[author] = 0
                        author2metric0_jue0[author] = 0
                        author2metric0_jue1[author] = 0
                        author2metric0_jue3[author] = 0

                    for item in qs2:
                        if item['metric'] == 1 and item['jue'] == 0:
                            author2metric1_jue0[item['author']] = item['num']
                        elif item['metric'] == 1 and item['jue'] == 1:
                            author2metric1_jue1[item['author']] = item['num']
                        elif item['metric'] == 1 and item['jue'] == 2:
                            author2metric1_jue2[item['author']] = item['num']
                        elif item['metric'] == 0 and item['jue'] == 0:
                            author2metric0_jue0[item['author']] = item['num']
                        elif item['metric'] == 0 and item['jue'] == 1:
                            author2metric0_jue1[item['author']] = item['num']
                        else:
                            author2metric0_jue3[item['author']] += item['num']

                    for author in author_list:
                        the_list1.append([author, author2metric1_jue0[author]])
                        the_list2.append([author, author2metric1_jue1[author]])
                        the_list3.append([author, author2metric1_jue2[author]])
                        the_list4.append([author, author2metric0_jue0[author]])
                        the_list5.append([author, author2metric0_jue1[author]])
                        the_list6.append([author, author2metric0_jue3[author]])

                    res_list.append(the_list1)  # 绝句
                    res_list.append(the_list2)  # 律诗
                    res_list.append(the_list3)  # 排律
                    res_list.append(the_list4)  # 古绝
                    res_list.append(the_list5)  # 古律
                    res_list.append(the_list6)  # 古体其他

                elif metric == -1 and yan == -1: # 只选诗体
                    # print('走的只选诗体')
                    qs2 = the_model.objects.values('author', 'metric', 'yan').filter(author__in=author_list,
                                                                                     **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []
                    the_list3 = []
                    the_list4 = []

                    author2metric1_yan7 = {}
                    author2metric1_yan5 = {}
                    author2metric0_yan7 = {}
                    author2metric0_yan5 = {}

                    author2metric0_yan6 = {}
                    author2metric0_yan4 = {}
                    author2metric0_yan0 = {}

                    for author in author_list:  # 初始化 author2num
                        author2metric1_yan7[author] = 0
                        author2metric1_yan5[author] = 0
                        author2metric0_yan7[author] = 0
                        author2metric0_yan5[author] = 0

                        author2metric0_yan6[author] = 0
                        author2metric0_yan4[author] = 0
                        author2metric0_yan0[author] = 0

                    if int(jue) == 2: # 排律
                        for item in qs2:
                            if item['metric'] == 1 and item['yan'] == 7:
                                author2metric1_yan7[item['author']] = item['num']
                            elif item['metric'] == 1 and item['yan'] == 5:
                                author2metric1_yan5[item['author']] = item['num']

                        for author in author_list:
                            the_list1.append([author, author2metric1_yan7[author]])
                            the_list2.append([author, author2metric1_yan5[author]])

                            # 滥竽充数
                            the_list3.append([author, 0])
                            the_list4.append([author, 0])

                        res_list.append(the_list1)  # 近体七言
                        res_list.append(the_list2)  # 近体五言

                        # 滥竽充数
                        res_list.append(the_list3)
                        res_list.append(the_list4)

                    elif int(jue) == 3: # 其他
                        for item in qs2:
                            if item['metric'] == 0 and item['yan'] == 6:
                                author2metric0_yan6[item['author']] = item['num']
                            elif item['metric'] == 0 and item['yan'] == 4:
                                author2metric0_yan4[item['author']] = item['num']
                            elif item['metric'] == 0 and item['yan'] == 0:
                                author2metric0_yan0[item['author']] = item['num']

                        for author in author_list:
                            the_list1.append([author, author2metric0_yan6[author]])
                            the_list2.append([author, author2metric0_yan4[author]])
                            the_list3.append([author, author2metric0_yan0[author]])

                            the_list4.append([author, 0]) # 滥竽充数

                        res_list.append(the_list1)  # 古体六言
                        res_list.append(the_list2)  # 古体四言
                        res_list.append(the_list3)  # 古体杂言

                        res_list.append(the_list3)  # 滥竽充数

                    else: # 绝句或律诗
                        for item in qs2:
                            if item['metric'] == 1 and item['yan'] == 7:
                                author2metric1_yan7[item['author']] = item['num']
                            elif item['metric'] == 1 and item['yan'] == 5:
                                author2metric1_yan5[item['author']] = item['num']
                            elif item['metric'] == 0 and item['yan'] == 7:
                                author2metric0_yan7[item['author']] = item['num']
                            elif item['metric'] == 0 and item['yan'] == 5:
                                author2metric0_yan5[item['author']] = item['num']

                        for author in author_list:
                            the_list1.append([author, author2metric1_yan7[author]])
                            the_list2.append([author, author2metric1_yan5[author]])
                            the_list3.append([author, author2metric0_yan7[author]])
                            the_list4.append([author, author2metric0_yan5[author]])

                        res_list.append(the_list1)  # 近体七言
                        res_list.append(the_list2)  # 近体五言
                        res_list.append(the_list3)  # 古体七言
                        res_list.append(the_list4)  # 古体五言

                elif metric == -1: # 只没选格律
                    # print('走的只没选格律')
                    qs2 = the_model.objects.values('author', 'metric').filter(author__in=author_list,
                                                                                     **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []

                    author2metric1 = {}
                    author2metric0 = {}

                    for author in author_list:  # 初始化 author2num
                        author2metric1[author] = 0
                        author2metric0[author] = 0

                    for item in qs2:
                        if item['metric'] == 1:
                            author2metric1[item['author']] = item['num']
                        elif item['metric'] == 0:
                            author2metric0[item['author']] = item['num']

                    for author in author_list:
                        the_list1.append([author, author2metric1[author]])
                        the_list2.append([author, author2metric0[author]])

                    res_list.append(the_list1)  # 近体
                    res_list.append(the_list2)  # 古体

                elif yan == -1: # 只没选几言
                    # print('走的只没选几言')
                    qs2 = the_model.objects.values('author', 'yan').filter(author__in=author_list,
                                                                                     **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []
                    the_list3 = []
                    the_list4 = []
                    the_list5 = []

                    author2yan7 = {}
                    author2yan5 = {}
                    author2yan6 = {}
                    author2yan4 = {}
                    author2yan0 = {}

                    for author in author_list:  # 初始化 author2num
                        author2yan7[author] = 0
                        author2yan5[author] = 0
                        author2yan6[author] = 0
                        author2yan4[author] = 0
                        author2yan0[author] = 0

                    for item in qs2:
                        if item['yan'] == 7:
                            author2yan7[item['author']] = item['num']
                        elif item['yan'] == 5:
                            author2yan5[item['author']] = item['num']
                        elif item['yan'] == 6:
                            author2yan6[item['author']] = item['num']
                        elif item['yan'] == 4:
                            author2yan4[item['author']] = item['num']
                        elif item['yan'] == 0:
                            author2yan0[item['author']] = item['num']

                    for author in author_list:
                        the_list1.append([author, author2yan7[author]])
                        the_list2.append([author, author2yan5[author]])
                        the_list3.append([author, author2yan6[author]])
                        the_list4.append([author, author2yan4[author]])
                        the_list5.append([author, author2yan0[author]])

                    res_list.append(the_list1)  # 七言
                    res_list.append(the_list2)  # 五言
                    res_list.append(the_list3)  # 六言
                    res_list.append(the_list4)  # 四言
                    res_list.append(the_list5)  # 杂言

                elif jue == -1:  # 只没选诗体
                    # print('走的只没选诗体')
                    qs2 = the_model.objects.values('author', 'jue').filter(author__in=author_list,
                                                                           **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []
                    the_list3 = []
                    the_list4 = []

                    author2jue0 = {}
                    author2jue1 = {}
                    author2jue2 = {}
                    author2jue3 = {}

                    for author in author_list:  # 初始化 author2num
                        author2jue0[author] = 0
                        author2jue1[author] = 0
                        author2jue2[author] = 0
                        author2jue3[author] = 0

                    for item in qs2:
                        if item['jue'] == 0:
                            author2jue0[item['author']] = item['num']
                        elif item['jue'] == 1:
                            author2jue1[item['author']] = item['num']
                        elif item['jue'] == 2:
                            author2jue2[item['author']] = item['num']
                        elif item['jue'] == 3:
                            author2jue3[item['author']] = item['num']

                    for author in author_list:
                        the_list1.append([author, author2jue0[author]])
                        the_list2.append([author, author2jue1[author]])
                        the_list3.append([author, author2jue2[author]])
                        the_list4.append([author, author2jue3[author]])

                    res_list.append(the_list1)  # 绝句
                    res_list.append(the_list2)  # 律诗
                    res_list.append(the_list3)  # 排律
                    res_list.append(the_list4)  # 其他

                else: # 全选了
                    # print('走的全选了')
                    res_list.append(the_list)

            datas = {
                # "word_dict": word_dict.sort(key=lambda x: x[1]),
                "res_list": res_list,
            }
            return Response(datas, status=200)
        except Exception as e:
            traceback.print_exc()
            return Response({'result': "查询失败"} ,status=500)


    def post(self, request):
        arg = request.POST
        try:
            num = int(arg.get("num", 10))
            dynasty = arg.get("dynasty")
            metric = arg.get("metric")
            yan = arg.get("yan")
            jue = arg.get("jue")
            three_hundred = arg.get("three_hundred")

            if num > 20 or num < 5:
                return Response({"result": "人数必须在[5,20]！"}, status=400)

            kwargs = {}

            if metric is not None:
                metric = int(metric)
                if metric != -1:
                    kwargs["metric"] = metric
            if yan is not None:
                yan = int(yan)
                if yan != -1:
                    kwargs["yan"] = yan
            if jue is not None:
                jue = int(jue)
                if jue != -1:
                    kwargs["jue"] = jue
            if three_hundred is not None:
                three_hundred = int(three_hundred)
                if three_hundred == 1:
                    kwargs["three_hundred"] = three_hundred


            if dynasty == '宋词':
                kwargs["dynasty"] = '宋代'
                the_model = Ci
            elif dynasty== '唐诗':
                kwargs["dynasty"] = '唐代'
                the_model = Shi
            elif dynasty== '宋诗':
                kwargs["dynasty"] = '宋代'
                the_model = Shi

            qs = the_model.objects.values('author').filter(~Q(author__in=['无名氏', '不详', '郊庙朝会歌辞']), **kwargs).annotate(num=Count('id')).order_by('-num') # 按条件筛
            # qs = the_model.objects.values('author').filter(**kwargs).annotate(num=Count('id')).order_by('-num') # 按条件筛
            the_list = [[poem['author'], poem['num']] for poem in qs[:int(num)]]
            the_list.sort(key=lambda x: x[1], reverse=False)

            res_list = []
            author_list = [i[0] for i in the_list]


            if the_model == Ci:
                qs2 = the_model.objects.values('author', 'complete').filter(author__in=author_list, **kwargs).annotate(num=Count('id')).order_by('-num')

                the_list1 = []
                the_list2 = []
                author2complete1 = {}
                author2complete0 = {}
                for author in author_list:  # 初始化 author2num
                    author2complete1[author] = 0
                    author2complete0[author] = 0

                for item in qs2:
                    if item['complete'] == 1:
                        author2complete1[item['author']] = item['num']
                    elif item['complete'] == 0:
                        author2complete0[item['author']] = item['num']

                for author in author_list:
                    the_list1.append([author, author2complete1[author]])
                    the_list2.append([author, author2complete0[author]])

                res_list.append(the_list1)  # 完整
                res_list.append(the_list2)  # 缺字
                pass
            else:
                if metric == -1 and yan == -1 and jue == -1: # 格律 几言 诗体 全不限
                    # print('走的全不限')
                    qs2 = the_model.objects.values('author', 'metric').filter(author__in=author_list,
                                                                    **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []
                    author2metric1 = {}
                    author2metric0 = {}
                    for author in author_list:  # 初始化 author2num
                        author2metric1[author] = 0
                        author2metric0[author] = 0

                    for item in qs2:
                        if item['metric'] == 1:
                            author2metric1[item['author']] = item['num']
                        elif item['metric'] == 0:
                            author2metric0[item['author']] = item['num']

                    for author in author_list:
                        the_list1.append([author, author2metric1[author]])
                        the_list2.append([author, author2metric0[author]])

                    res_list.append(the_list1)  # 近体
                    res_list.append(the_list2)  # 古体

                elif yan == -1 and jue == -1: # 只选格律
                    # print('走的只选格律')
                    qs2 = the_model.objects.values('author', 'yan', 'jue').filter(author__in=author_list,
                                                                                  **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []
                    the_list3 = []
                    the_list4 = []
                    the_list5 = []
                    the_list6 = []
                    author2yan7_jue0 = {}
                    author2yan7_jue1 = {}
                    author2yan7_jue2 = {}
                    author2yan5_jue0 = {}
                    author2yan5_jue1 = {}
                    author2yan5_jue2 = {}

                    author2yan_jue3 = {}

                    for author in author_list:  # 初始化 author2num
                        author2yan7_jue0[author] = 0
                        author2yan7_jue1[author] = 0
                        author2yan7_jue2[author] = 0
                        author2yan5_jue0[author] = 0
                        author2yan5_jue1[author] = 0
                        author2yan5_jue2[author] = 0

                        author2yan_jue3[author] = 0


                    if int(metric) == 1: # 选了近体诗
                        for item in qs2:
                            if item['yan'] == 7 and item['jue'] == 0:
                                author2yan7_jue0[item['author']] = item['num']
                            elif item['yan'] == 7 and item['jue'] == 1:
                                author2yan7_jue1[item['author']] = item['num']
                            elif item['yan'] == 7 and item['jue'] == 2:
                                author2yan7_jue2[item['author']] = item['num']
                            elif item['yan'] == 5 and item['jue'] == 0:
                                author2yan5_jue0[item['author']] = item['num']
                            elif item['yan'] == 5 and item['jue'] == 1:
                                author2yan5_jue1[item['author']] = item['num']
                            elif item['yan'] == 5 and item['jue'] == 2:
                                author2yan5_jue2[item['author']] = item['num']

                        for author in author_list:
                            the_list1.append([author, author2yan7_jue0[author]])
                            the_list2.append([author, author2yan7_jue1[author]])
                            the_list3.append([author, author2yan7_jue2[author]])
                            the_list4.append([author, author2yan5_jue0[author]])
                            the_list5.append([author, author2yan5_jue1[author]])
                            the_list6.append([author, author2yan5_jue2[author]])

                        res_list.append(the_list1)  # 七绝
                        res_list.append(the_list2)  # 七律
                        res_list.append(the_list3)  # 七排
                        res_list.append(the_list4)  # 五绝
                        res_list.append(the_list5)  # 五律
                        res_list.append(the_list6)  # 五排

                    elif int(metric) == 0: # 选了古体诗
                        for item in qs2:
                            if item['yan'] == 7 and item['jue'] == 0:
                                author2yan7_jue0[item['author']] = item['num']
                            elif item['yan'] == 7 and item['jue'] == 1:
                                author2yan7_jue1[item['author']] = item['num']
                            elif item['yan'] == 5 and item['jue'] == 0:
                                author2yan5_jue0[item['author']] = item['num']
                            elif item['yan'] == 5 and item['jue'] == 1:
                                author2yan5_jue1[item['author']] = item['num']
                            else:
                                author2yan_jue3[item['author']] += item['num']

                        for author in author_list:
                            the_list1.append([author, author2yan7_jue0[author]])
                            the_list2.append([author, author2yan7_jue1[author]])
                            the_list3.append([author, author2yan5_jue0[author]])
                            the_list4.append([author, author2yan5_jue1[author]])
                            the_list5.append([author, author2yan_jue3[author]])

                            the_list6.append([author, 0]) # 滥竽充数的 为了保持res_list长度一致

                        res_list.append(the_list1)  # 七绝
                        res_list.append(the_list2)  # 七律
                        res_list.append(the_list3)  # 五绝
                        res_list.append(the_list4)  # 五律
                        res_list.append(the_list5)  # 其他

                        res_list.append(the_list6)  # 滥竽充数

                elif metric == -1 and jue == -1: # 只选几言
                    # print('走的只选几言')
                    qs2 = the_model.objects.values('author', 'metric', 'jue').filter(author__in=author_list,
                                                                                  **kwargs).annotate(num=Count('id')).order_by('-num')

                    the_list1 = []
                    the_list2 = []
                    the_list3 = []
                    the_list4 = []
                    the_list5 = []
                    the_list6 = []

                    author2metric1_jue0 = {}
                    author2metric1_jue1 = {}
                    author2metric1_jue2 = {}
                    author2metric0_jue0 = {}
                    author2metric0_jue1 = {}
                    author2metric0_jue3 = {}

                    for author in author_list:  # 初始化 author2num
                        author2metric1_jue0[author] = 0
                        author2metric1_jue1[author] = 0
                        author2metric1_jue2[author] = 0
                        author2metric0_jue0[author] = 0
                        author2metric0_jue1[author] = 0
                        author2metric0_jue3[author] = 0

                    for item in qs2:
                        if item['metric'] == 1 and item['jue'] == 0:
                            author2metric1_jue0[item['author']] = item['num']
                        elif item['metric'] == 1 and item['jue'] == 1:
                            author2metric1_jue1[item['author']] = item['num']
                        elif item['metric'] == 1 and item['jue'] == 2:
                            author2metric1_jue2[item['author']] = item['num']
                        elif item['metric'] == 0 and item['jue'] == 0:
                            author2metric0_jue0[item['author']] = item['num']
                        elif item['metric'] == 0 and item['jue'] == 1:
                            author2metric0_jue1[item['author']] = item['num']
                        else:
                            author2metric0_jue3[item['author']] += item['num']

                    for author in author_list:
                        the_list1.append([author, author2metric1_jue0[author]])
                        the_list2.append([author, author2metric1_jue1[author]])
                        the_list3.append([author, author2metric1_jue2[author]])
                        the_list4.append([author, author2metric0_jue0[author]])
                        the_list5.append([author, author2metric0_jue1[author]])
                        the_list6.append([author, author2metric0_jue3[author]])

                    res_list.append(the_list1)  # 绝句
                    res_list.append(the_list2)  # 律诗
                    res_list.append(the_list3)  # 排律
                    res_list.append(the_list4)  # 古绝
                    res_list.append(the_list5)  # 古律
                    res_list.append(the_list6)  # 古体其他

                elif metric == -1 and yan == -1: # 只选诗体
                    # print('走的只选诗体')
                    qs2 = the_model.objects.values('author', 'metric', 'yan').filter(author__in=author_list,
                                                                                     **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []
                    the_list3 = []
                    the_list4 = []

                    author2metric1_yan7 = {}
                    author2metric1_yan5 = {}
                    author2metric0_yan7 = {}
                    author2metric0_yan5 = {}

                    author2metric0_yan6 = {}
                    author2metric0_yan4 = {}
                    author2metric0_yan0 = {}

                    for author in author_list:  # 初始化 author2num
                        author2metric1_yan7[author] = 0
                        author2metric1_yan5[author] = 0
                        author2metric0_yan7[author] = 0
                        author2metric0_yan5[author] = 0

                        author2metric0_yan6[author] = 0
                        author2metric0_yan4[author] = 0
                        author2metric0_yan0[author] = 0

                    if int(jue) == 2: # 排律
                        for item in qs2:
                            if item['metric'] == 1 and item['yan'] == 7:
                                author2metric1_yan7[item['author']] = item['num']
                            elif item['metric'] == 1 and item['yan'] == 5:
                                author2metric1_yan5[item['author']] = item['num']

                        for author in author_list:
                            the_list1.append([author, author2metric1_yan7[author]])
                            the_list2.append([author, author2metric1_yan5[author]])

                            # 滥竽充数
                            the_list3.append([author, 0])
                            the_list4.append([author, 0])

                        res_list.append(the_list1)  # 近体七言
                        res_list.append(the_list2)  # 近体五言

                        # 滥竽充数
                        res_list.append(the_list3)
                        res_list.append(the_list4)

                    elif int(jue) == 3: # 其他
                        for item in qs2:
                            if item['metric'] == 0 and item['yan'] == 6:
                                author2metric0_yan6[item['author']] = item['num']
                            elif item['metric'] == 0 and item['yan'] == 4:
                                author2metric0_yan4[item['author']] = item['num']
                            elif item['metric'] == 0 and item['yan'] == 0:
                                author2metric0_yan0[item['author']] = item['num']

                        for author in author_list:
                            the_list1.append([author, author2metric0_yan6[author]])
                            the_list2.append([author, author2metric0_yan4[author]])
                            the_list3.append([author, author2metric0_yan0[author]])

                            the_list4.append([author, 0]) # 滥竽充数

                        res_list.append(the_list1)  # 古体六言
                        res_list.append(the_list2)  # 古体四言
                        res_list.append(the_list3)  # 古体杂言

                        res_list.append(the_list3)  # 滥竽充数

                    else: # 绝句或律诗
                        for item in qs2:
                            if item['metric'] == 1 and item['yan'] == 7:
                                author2metric1_yan7[item['author']] = item['num']
                            elif item['metric'] == 1 and item['yan'] == 5:
                                author2metric1_yan5[item['author']] = item['num']
                            elif item['metric'] == 0 and item['yan'] == 7:
                                author2metric0_yan7[item['author']] = item['num']
                            elif item['metric'] == 0 and item['yan'] == 5:
                                author2metric0_yan5[item['author']] = item['num']

                        for author in author_list:
                            the_list1.append([author, author2metric1_yan7[author]])
                            the_list2.append([author, author2metric1_yan5[author]])
                            the_list3.append([author, author2metric0_yan7[author]])
                            the_list4.append([author, author2metric0_yan5[author]])

                        res_list.append(the_list1)  # 近体七言
                        res_list.append(the_list2)  # 近体五言
                        res_list.append(the_list3)  # 古体七言
                        res_list.append(the_list4)  # 古体五言

                elif metric == -1: # 只没选格律
                    # print('走的只没选格律')
                    qs2 = the_model.objects.values('author', 'metric').filter(author__in=author_list,
                                                                                     **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []

                    author2metric1 = {}
                    author2metric0 = {}

                    for author in author_list:  # 初始化 author2num
                        author2metric1[author] = 0
                        author2metric0[author] = 0

                    for item in qs2:
                        if item['metric'] == 1:
                            author2metric1[item['author']] = item['num']
                        elif item['metric'] == 0:
                            author2metric0[item['author']] = item['num']

                    for author in author_list:
                        the_list1.append([author, author2metric1[author]])
                        the_list2.append([author, author2metric0[author]])

                    res_list.append(the_list1)  # 近体
                    res_list.append(the_list2)  # 古体

                elif yan == -1: # 只没选几言
                    # print('走的只没选几言')
                    qs2 = the_model.objects.values('author', 'yan').filter(author__in=author_list,
                                                                                     **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []
                    the_list3 = []
                    the_list4 = []
                    the_list5 = []

                    author2yan7 = {}
                    author2yan5 = {}
                    author2yan6 = {}
                    author2yan4 = {}
                    author2yan0 = {}

                    for author in author_list:  # 初始化 author2num
                        author2yan7[author] = 0
                        author2yan5[author] = 0
                        author2yan6[author] = 0
                        author2yan4[author] = 0
                        author2yan0[author] = 0

                    for item in qs2:
                        if item['yan'] == 7:
                            author2yan7[item['author']] = item['num']
                        elif item['yan'] == 5:
                            author2yan5[item['author']] = item['num']
                        elif item['yan'] == 6:
                            author2yan6[item['author']] = item['num']
                        elif item['yan'] == 4:
                            author2yan4[item['author']] = item['num']
                        elif item['yan'] == 0:
                            author2yan0[item['author']] = item['num']

                    for author in author_list:
                        the_list1.append([author, author2yan7[author]])
                        the_list2.append([author, author2yan5[author]])
                        the_list3.append([author, author2yan6[author]])
                        the_list4.append([author, author2yan4[author]])
                        the_list5.append([author, author2yan0[author]])

                    res_list.append(the_list1)  # 七言
                    res_list.append(the_list2)  # 五言
                    res_list.append(the_list3)  # 六言
                    res_list.append(the_list4)  # 四言
                    res_list.append(the_list5)  # 杂言

                elif jue == -1:  # 只没选诗体
                    # print('走的只没选诗体')
                    qs2 = the_model.objects.values('author', 'jue').filter(author__in=author_list,
                                                                           **kwargs).annotate(num=Count('id')).order_by('-num')
                    the_list1 = []
                    the_list2 = []
                    the_list3 = []
                    the_list4 = []

                    author2jue0 = {}
                    author2jue1 = {}
                    author2jue2 = {}
                    author2jue3 = {}

                    for author in author_list:  # 初始化 author2num
                        author2jue0[author] = 0
                        author2jue1[author] = 0
                        author2jue2[author] = 0
                        author2jue3[author] = 0

                    for item in qs2:
                        if item['jue'] == 0:
                            author2jue0[item['author']] = item['num']
                        elif item['jue'] == 1:
                            author2jue1[item['author']] = item['num']
                        elif item['jue'] == 2:
                            author2jue2[item['author']] = item['num']
                        elif item['jue'] == 3:
                            author2jue3[item['author']] = item['num']

                    for author in author_list:
                        the_list1.append([author, author2jue0[author]])
                        the_list2.append([author, author2jue1[author]])
                        the_list3.append([author, author2jue2[author]])
                        the_list4.append([author, author2jue3[author]])

                    res_list.append(the_list1)  # 绝句
                    res_list.append(the_list2)  # 律诗
                    res_list.append(the_list3)  # 排律
                    res_list.append(the_list4)  # 其他

                else: # 全选了
                    # print('走的全选了')
                    res_list.append(the_list)

            datas = {
                # "word_dict": word_dict.sort(key=lambda x: x[1]),
                "res_list": res_list,
            }
            return Response(datas, status=200)
        except Exception as e:
            traceback.print_exc()
            return Response({'result': "查询失败"} ,status=500)

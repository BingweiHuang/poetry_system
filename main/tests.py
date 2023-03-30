from django.test import TestCase

# from main.utils.tools import md5_encryption
# Create your tests here.
from poetry_system.settings import BASE_DIR

print(BASE_DIR)

from django.db.models.functions import Substr, Lower
from django.forms import model_to_dict
from django.test import TestCase



class TestCase1(TestCase):
    pass
    # qs = Literature.objects.filter(Q(lit_en_title__istartswith='S') | Q(lit_en_title__endswith='E'))
    # qs = Literature.objects.filter(lit_en_title__istartswith='S', lit_category='西方哲学')
    # qs = Literature.objects.filter(lit_id__lt=10)
    # qs = Literature.objects.filter(lit_id__lt=10).values('lit_en_title', 'lit_ch_title') # values之后直接就是json格式
    # qs = Literature.objects.filter(lit_id__lt=10) # values之后直接就是json格式

    # 找到每个作者的最早出版的一本书籍
    # qs_book = Literature.objects.filter(fig_id=OuterRef("pk")).order_by("lit_published_date")
    # qs = Figure.objects.all().annotate(
    #     earlyst = Subquery(
    #         qs_book.values('lit_id')[:1]
    #     )
    # )
    # print(qs)

    # 基于字段值比较标准来筛选
    # qs = Literature.objects.annotate(lit_name=Substr("lit_ch_title", 1, 1), lit_cate=Substr("lit_category", 1, 1)).filter(lit_name=F("lit_cate"))

    # 筛选没有任何值的字段
    # qs = Literature.objects.filter(
    #     Q(lit_img_address='') | Q(lit_img_address=None)
    # )

    # 筛选指定第几个数据
    # qs = Literature.objects.values('lit_id').order_by('lit_id')[:2]
    # qs = Literature.objects.values('lit_id').order_by('lit_id')[2]

    # 筛选独一无二的字段值
    # distinct = Literature.objects.values(
    #     'lit_category'
    # ).annotate(
    #     lit_category_count=Count('lit_category')
    # ).filter(lit_category_count=1)
    # qs = Literature.objects.filter(lit_category__in=[item['lit_category'] for item in distinct])

    # 找到所有 lit_en_title 以C开始且 lit_en_title 不是以t结尾的书籍。
    # qs = Literature.objects.filter(
    #     Q(lit_en_title__startswith='C') & ~Q(lit_en_title__endswith='t')
    # )

    # 聚合查询
    # qs = Literature.objects.all().aggregate(Max('lit_read_times'))
    # print(qs)

    # 字符串转化为datetime
    # date_str = "2018-03-11"
    # from datetime import datetime
    # temp_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # 排序
    # qs = Literature.objects.all().order_by('fig_id', '-lit_published_date')

    # qs = Literature.objects.all().order_by(
    #     '-lit_category', 'fig__fig_id'
    # ).values('lit_id', 'lit_category', 'lit_ch_title', 'fig__fig_id', 'fig__fig_ch_name')

    # 忽略大小写排序
    # qs = Literature.objects.filter(~Q(lit_en_title=None)).annotate(
    #     uname=Lower('lit_en_title')
    # ).order_by('uname').values_list('lit_en_title', flat=True) # values_list直接输出string对象 不是json格式

    # qs = Literature.objects.filter(~Q(lit_en_title=None)).annotate(
    #     uname=Lower('lit_en_title')
    # ).order_by('uname').values('lit_en_title')

    # qs = FigureCategory.objects.all();


    # for lit in qs:
    #     print(model_to_dict(lit)) # model_to_dict 从model转成json格式
        # print(lit)

    # res = model_to_dict(Literature.objects.get(lit_id=1))
    # print(res)





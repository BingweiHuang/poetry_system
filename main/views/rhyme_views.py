import traceback
import re

from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.utils.rhyme_table.get_rhyme import pingshui2word, word2pingshui, xinyun2word, word2xinyun
from main.utils.rhyme_table.get_rhyme import first_sentence_tone_table, get_word_rhyme
from main.utils.algorihtm.metric_poetry_detection import metric_poetry_detection

# class AllRhymeView(APIView):
#     # permission_classes = ([IsAuthenticated])
#
#     # /rhyme/all_rhyme
#
#     def get(self, request):
#         arg = request.GET
#         try:
#             datas = {
#                 "pingshui2word": pingshui2word,
#                 "xinyun2word": xinyun2word,
#             }
#
#             return Response(datas, status=200)
#         except Exception as e:
#             traceback.print_exc()
#             return Response({'result': "获取韵表失败"},status=500)

class GetRhymeView(APIView):
    # permission_classes = ([IsAuthenticated])

    def get(self, request):
        arg = request.GET
        try:
            kind = int(arg.get('kind', 1))
            sheng_tag = arg.get('sheng_tag', '平声')
            yun_tag = arg.get('yun_tag', '')

            list = {}
            if kind == 1:
                list = {
                    'list': pingshui2word[sheng_tag][yun_tag]
                }
            elif kind == 2:
                list = {
                    'list': xinyun2word[sheng_tag][yun_tag]
                }

            return Response(list, status=200)
        except Exception as e:
            traceback.print_exc()
            return Response({'result': "获取韵表失败"},status=500)



'''如果print显示是gbk编码 而报错'''
# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors='replace', line_buffering=True)

def reserved_chinese_word(text):
    return re.sub('[^\u4e00-\u9fa5]+', '', text)

class SearchRhymeView(APIView):
    # permission_classes = ([IsAuthenticated])

    # /rhyme/search_rhyme?word=白
    def get(self, request):
        arg = request.GET
        try:
            word = arg.get('word')

            if not word:
                return Response({"result": "请输入一个汉字！"}, status=400)

            word = reserved_chinese_word(word)

            # pingshui
            ps_word2rhyme = []
            if word in word2pingshui:
                yin_list = word2pingshui[word]
                for yun in yin_list:
                    sheng_tag = yun[0]
                    yin_tag = yun[1]
                    ps_word2rhyme.append((sheng_tag, yin_tag, pingshui2word[sheng_tag][yin_tag]))

            # xinyun
            xin_word2rhyme = []
            if word in word2xinyun:
                yin_list = word2xinyun[word]
                for yun in yin_list:
                    sheng_tag = yun[0]
                    yin_tag = yun[1]
                    xin_word2rhyme.append((sheng_tag, yin_tag, xinyun2word[sheng_tag][yin_tag]))

            datas = {
                "ps_word2rhyme": ps_word2rhyme,
                "xin_word2rhyme": xin_word2rhyme,
            }
            return Response(datas, status=200)
        except Exception as e:
            traceback.print_exc()
            return Response({'result': "查韵失败"}, status=500)

class FirstSentenceView(APIView):
    # /detection/first_sentence?text=戌时皓月照空明&yan=7&use_rhyme=1&ru=0&qi=1
    def get(self, request):
        arg = request.GET
        try:
            text = arg.get("text") # 首句
            yan = int(arg.get("yan")) # 7:七言 5:五言
            ru = int(arg.get("ru")) # 0:首句入韵 1:首句不入
            qi = int(arg.get("qi")) # 0:仄起 1:平起
            use_rhyme = int(arg.get("use_rhyme", 1)) # 测哪个韵 1:平水 2:新韵

            text = re.sub('[^\u4e00-\u9fa5]+', '', text)  # 只留汉字
            tune = first_sentence_tone_table[0 if yan == 5 else 1][qi][1 - ru]

            word2rhyme = word2pingshui
            if use_rhyme == 1: # 平水韵
                word2rhyme = word2pingshui
            elif use_rhyme == 2: # 中华新韵
                word2rhyme = word2xinyun

            flag = 1 # 1:押韵 0:不押韵
            for idx, word in enumerate(text): # 测一句的平仄
                ping, ze = get_word_rhyme(word, word2rhyme)
                if tune[idx] == 'x':
                    continue
                elif tune[idx] == '0' and len(ping) > 0:
                    continue
                elif tune[idx] == '1' and len(ze) > 0:
                    continue
                else:
                    flag = 0
                    break

            return Response({"is_rhyme": flag}, status=200)

        except Exception as e:
            traceback.print_exc()
            return Response({'result': "判断失败"}, status=500)

class MetricPoetryView(APIView):

    def get(self, request):
        arg = request.GET
        try:
            text = arg.get("text")  # 整首诗
            yan = int(arg.get("yan"))  # 7:七言 5:五言
            jue = int(arg.get("jue"))  # 0:绝句 1:律
            ru = int(arg.get("ru"))  # 0:首句入韵 1:首句不入
            qi = int(arg.get("qi"))  # 0:仄起 1:平起
            use_rhyme = int(arg.get("use_rhyme", 1))  # 测哪个韵 1:平水 2:新韵

            text = re.sub('[^\u4e00-\u9fa5]+', '', text) # 只留汉字

            yun_pos_dict, pz_err_dict, duo_yin_pos, rhyme_foot = metric_poetry_detection(yan, jue, ru, qi, text, use_rhyme)

            datas = {
                'text': text,
                'yun_pos_dict': yun_pos_dict,
                'pz_err_dict': pz_err_dict,
                'duo_yin_pos': duo_yin_pos,
                'rhyme_foot': rhyme_foot,
                'yan_list': list(range(yan)),
                'jue_list': list(range(4 * (jue + 1))),
            }

            # print('存韵脚位置的字的所有平韵:', end=' ')
            # for pos in yun_pos_dict:
            #     print(f'{text[pos]}:{yun_pos_dict[pos]}', end=' ')
            # print()
            #
            # if len(pz_err_dict) == 0:
            #     print('没有平仄错误')
            # else:
            #     for idx in pz_err_dict:
            #         print(f'{text[idx]}应该为{"平" if pz_err_dict[idx] == 0 else "仄"}', end=' ')
            # print()
            #
            # print('注意多音字:', end=' ')
            # for idx in duo_yin_pos:
            #     print(text[idx], end=' ')
            # print()
            #
            # if rhyme_foot != '':
            #     print(f'韵脚:{rhyme_foot}', )
            # else:
            #     print('不押韵')

            return Response(datas, status=200)

        except Exception as e:
            traceback.print_exc()
            return Response({'result': "格律诗检测失败"}, status=500)
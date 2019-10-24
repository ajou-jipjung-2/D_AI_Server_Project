from gensim.models import fasttext as fText
import pymysql
import secrets
import os
import random
from D_AI_Project.D_AI import keyvalue
import re

def load_label():
    conn = pymysql.connect(host=keyvalue.get_hostname(), user=keyvalue.get_username(),
                           password=keyvalue.get_pw(),
                           db=keyvalue.get_dbname(), charset='utf8')
    curs = conn.cursor()
    sql = "select * from noun_label"
    curs.execute(sql)
    row = [item[1] for item in curs.fetchall()]
    return row

def load_adj():
    conn = pymysql.connect(host=keyvalue.get_hostname(), user=keyvalue.get_username(),
                           password=keyvalue.get_pw(),
                           db=keyvalue.get_dbname(), charset='utf8')
    curs = conn.cursor()
    sql = "select * from adj_label"
    curs.execute(sql)
    row = [item[1] for item in curs.fetchall()]
    return row

# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    # 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                     'ㅣ']
    # 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                     'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

class singleton_fasttext:
    _instance = None
    model = None
    vocab_list = None
    adj_list = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance



    def __init__(self):
        global model, vocab_list, adj_list
        model = fText.load_facebook_model(os.path.join(os.getcwd(),'server_singletonML','fasttext','model_ft_sk.bin'))
        vocab_list = load_label()
        adj_list = load_adj()

    def convert(self,test_keyword):
        split_keyword_list = list(test_keyword)
        # print(split_keyword_list)

        result = list()
        for keyword in split_keyword_list:
            # 한글 여부 check 후 분리
            if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', keyword) is not None:
                char_code = ord(keyword) - BASE_CODE
                char1 = int(char_code / CHOSUNG)
                result.append(CHOSUNG_LIST[char1])
                # print('초성 : {}'.format(CHOSUNG_LIST[char1]))
                char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
                result.append(JUNGSUNG_LIST[char2])
                # print('중성 : {}'.format(JUNGSUNG_LIST[char2]))
                char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
                if char3 == 0:
                    result.append('-')
                else:
                    result.append(JONGSUNG_LIST[char3])
                # print('종성 : {}'.format(JONGSUNG_LIST[char3]))
            else:
                result.append(keyword)
        # result
        return ''.join(result)

    def end_check(self,w):
        ## 588개 마다 초성이 바뀜.
        ch1 = (ord(w) - ord('가')) // 588
        ## 중성은 총 28가지 종류
        ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
        ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
        return JONGSUNG_LIST[ch3]

    def get_vocab_list(self):
        return vocab_list

    def get_adj_list(self):
        return adj_list

    def makevocab(self, k1, association):
        global model, vocab_list, adj_list
        sm_A_list = []
        k1_convert = self.convert(k1)
        for vocab_item in vocab_list:
            vocab_item_convert = self.convert(vocab_item)
            vocab = model.similarity(vocab_item_convert, k1_convert)
            # if vocab > min and vocab < max:
            sm_A_list.append([vocab_item, vocab])
        sm_A_list = sorted(sm_A_list, key=lambda acc: acc[1], reverse=True)
        out = random.sample(sm_A_list[:30], 10)
        out_index = [i[0] for i in out]
        return out_index

    def makevocab1(self, k1, association):
        global model, vocab_list, adj_list
        sm_A_list = []
        k1_convert = self.convert(k1)
        for vocab_item in vocab_list:
            vocab_item_convert = self.convert(vocab_item)
            vocab = model.similarity(vocab_item_convert, k1_convert)
            # if vocab > min and vocab < max:
            sm_A_list.append([vocab_item, vocab])
        sm_A_list = sorted(sm_A_list, key=lambda acc: acc[1], reverse=True)
        # sm_A_list_index = [i[0] for i in sm_A_list[:30]]
        s = int(len(sm_A_list) * association)
        e = int(len(sm_A_list) * (association+0.2))
        out = random.sample(sm_A_list[s:e], 30)
        out_index = [i[0] for i in out]
        return out_index

    def makevocab2(self,k1, k2, association):
        global model, vocab_list, adj_list
        sm_A_list = []
        k1_convert = self.convert(k1)
        k2_convert = self.convert(k2)
        for vocab_item in vocab_list:
            vocab_item_convert = self.convert(vocab_item)
            vocab1 = model.similarity(vocab_item_convert, k1_convert)
            vocab2 = model.similarity(vocab_item_convert, k2_convert)
            #         if vocab1>min and vocab1<max and vocab2>min and vocab2<max:
            sm_A_list.append([vocab_item, vocab1 * (1 - vocab2)])
        sm_A_list = sorted(sm_A_list, key=lambda acc: acc[1], reverse=True)
        s = int(len(sm_A_list) * association)
        e = int(len(sm_A_list) * (association + 0.2))
        out = random.sample(sm_A_list[s:e], 30)
        out_index = [i[0] for i in out]
        return out_index

    def makeSentence(self,k1,sel_N):

        select_label = sel_N
        # print("select_label : ", select_label[:][0])

        adj_A_list = []
        check_point1 = self.end_check(k1[-1])
        if check_point1 == ' ':
            sen1 = k1 + "가"
            sen2 = k1 + "를"
        else:
            sen1 = k1 + "이"
            sen2 = k1 + "을"
        sel_N_convert = self.convert(sel_N)
        sen1_convert = self.convert(sen1)
        sen2_convert = self.convert(sen2)
        for adj_item in adj_list:
            adj_item_convert = self.convert(adj_item)
            a = model.similarity(adj_item_convert, sen1_convert)
            en = model.similarity(adj_item_convert, sel_N_convert)
            b = model.similarity(adj_item_convert, sen1_convert)
            ab = [[sen1, a], [sen2, b]]
            ab = sorted(ab, key=lambda acc: acc[1], reverse=True)
            adj_A_list.append([ab[0][0] + " " + adj_item + " " + sel_N, ab[0][1] * en])
        adj_A_list = sorted(adj_A_list, key=lambda acc: acc[1], reverse=True)
        adj_A_list_index = [i[0] for i in adj_A_list[:30]]
        print("adj_A_list_index",adj_A_list_index)
        return adj_A_list_index

    def makeSentence2(self,k1,k2,sel_N_list,num):
        global model, vocab_list, adj_list
        adj_A_list = []
        adj_B_list = []
        check_point1 = self.end_check(k1[-1])
        check_point2 = self.end_check(k2[-1])
        if check_point2 == ' ':
            sen1 = k1 + " 대신 " + k2 + "가"
            sen2 = k1 + " 대신 " + k2 + "를"
        else:
            sen1 = k1 + " 대신 " + k2 + "이"
            sen2 = k1 + " 대신 " + k2 + "을"

        sel_N_convert = self.convert(sel_N_list[0])
        sen1_convert = self.convert(sen1)
        sen2_convert = self.convert(sen2)

        for adj_item in adj_list:
            adj_item_convert = self.convert(adj_item)
            a = model.similarity(adj_item_convert, sen1_convert)
            en = model.similarity(adj_item_convert, sel_N_convert)
            b = model.similarity(adj_item_convert, sen2_convert)
            ab = [[sen1, a], [sen2, b]]
            ab = sorted(ab, key=lambda acc: acc[1], reverse=True)
            adj_A_list.append([ab[0][0] + " " + adj_item + " " + sel_N_list[0], ab[0][1] * en])
        #         if a*b > b*c:
        #             adj_A_list.append([sen1+" "+adj_item+" "+sel_N_list[0], a * en])
        #         else:
        #             adj_A_list.append([sen1+" "+adj_item+" "+sel_N_list[0], b * en])

        adj_A_list = sorted(adj_A_list, key=lambda acc: acc[1], reverse=True)
        #     return adj_A_list[:num]

        if check_point1 == ' ':
            sen1 = k1 + "에 "
            sen2 = k1 + "가 "
            sen3 = k1 + "와 "
            sen4 = k1 + "와 "
            sen5 = k1 + "를 "
        else:
            sen1 = k1 + "에 "
            sen2 = k1 + "이 "
            sen3 = k1 + "과 "
            sen4 = k1 + "과 "
            sen5 = k1 + "을 "
        if check_point2 == ' ':
            sen1 += k2 + "를"
            sen2 += k2 + "로"
            sen3 += k2 + "가"
            sen4 += k2 + "를"
            sen5 += k2 + "로"
        else:
            sen1 += k2 + "을"
            sen2 += k2 + "으로"
            sen3 += k2 + "이"
            sen4 += k2 + "을"
            sen5 += k2 + "으로"

        sel_N_convert = self.convert(sel_N_list[1])
        sen1_convert = self.convert(sen1)
        sen2_convert = self.convert(sen2)
        sen3_convert = self.convert(sen3)
        sen4_convert = self.convert(sen4)
        sen5_convert = self.convert(sen5)

        for adj_item in adj_list:
            adj_item_convert = self.convert(adj_item)
            a = model.similarity(adj_item_convert, sen1_convert)
            en = model.similarity(adj_item_convert, sel_N_convert)
            b = model.similarity(adj_item_convert, sen2_convert)
            c = model.similarity(adj_item_convert, sen3_convert)
            d = model.similarity(adj_item_convert, sen4_convert)
            e = model.similarity(adj_item_convert, sen5_convert)
            ab = [[sen1, a], [sen2, b], [sen3, c], [sen4, d], [sen5, e]]
            ab = sorted(ab, key=lambda acc: acc[1], reverse=True)
            adj_B_list.append([ab[0][0] + " " + adj_item + " " + sel_N_list[1], ab[0][1] * en])
        #         if a*b > b*c:
        #             adj_A_list.append([sen1+" "+adj_item+" "+sel_N_list[0], a * b])
        #         else:
        #             adj_A_list.append([sen1+" "+adj_item+" "+sel_N_list[0], b * c])

        adj_B_list = sorted(adj_B_list, key=lambda acc: acc[1], reverse=True)
        adj_AB_list = [[], []]
        adj_AB_list[0] = [i[0] for i in adj_A_list[:num-15]]
        adj_AB_list[1] = [i[0] for i in adj_B_list[:num]]
        print("adj_AB",adj_AB_list)
        return adj_AB_list

    def makeSentence2_new(self,k1,k2,sel_N_list):
        sentence_list=[[],[]]
        sentence_list[0] = self.makeSentence2(k1, k2, sel_N_list[0], " 대신", "가")

from gensim.models import fasttext as fText
import pymysql
import secrets
import os
import random
from D_AI_Project.D_AI import keyvalue


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
        print ("print Ldsfasdfasdfasdfasdfasdfsaf",os.getcwd()) #현재 디렉토리의
        # model = fText.load_facebook_model('Z:\\study\\git\\D_AI_Server_Project\\D_AI_Project\\server_singletonML\\fasttext\\fasttext.bin')
        model = fText.load_facebook_model(os.getcwd()+'/server_singletonML/fasttext/fasttext.bin')
        print("load_model_success!!")
        # vocab_list = open(os.getcwd()+"/server_singletonML/label_list.txt", 'r', encoding="utf-8").read().split()
        vocab_list = load_label()
        # adj_list = open(os.getcwd()+"/server_singletonML/adj_list.txt", 'r', encoding="utf-8").read().split()
        adj_list = load_adj()

    def get_vocab_list(self):
        return vocab_list

    def get_adj_list(self):
        return adj_list

    def makevocab1(slef, k1, association):
        global model, vocab_list, adj_list
        sm_A_list = []
        for vocab_item in vocab_list:
            vocab = model.similarity(vocab_item, k1)
            # if vocab > min and vocab < max:
            sm_A_list.append([vocab_item, vocab])
        sm_A_list = sorted(sm_A_list, key=lambda acc: acc[1], reverse=True)
        # sm_A_list_index = [i[0] for i in sm_A_list[:30]]
        s = int(len(sm_A_list) * association)
        e = int(len(sm_A_list) * (association+0.1))
        out = random.sample(sm_A_list[s:e], 30)
        out_index = [i[0] for i in out]
        return out_index

    def makevocab2(self,k1, k2, association):
        global model, vocab_list, adj_list
        sm_A_list = []
        for vocab_item in vocab_list:
            vocab1 = model.similarity(vocab_item, k1)
            vocab2 = model.similarity(vocab_item, k2)
            #         if vocab1>min and vocab1<max and vocab2>min and vocab2<max:
            sm_A_list.append([vocab_item, vocab1 * (1 - vocab2)])
        sm_A_list = sorted(sm_A_list, key=lambda acc: acc[1], reverse=True)
        s = int(len(sm_A_list) * association)
        e = int(len(sm_A_list) * (association + 0.1))
        out = random.sample(sm_A_list[s:e], 30)
        out_index = [i[0] for i in out]
        return out_index

    def makeSentence(slef,k1,sel_N):

        select_label = sel_N
        # print("select_label : ", select_label[:][0])

        adj_A_list = []
        adj_B_list = []
        for adj_item in adj_list:
            adj_A = model.similarity(adj_item, k1)
            adj_B = model.similarity(adj_item, select_label)
            adj_A_list.append([k1+" "+adj_item+" "+select_label, adj_A * adj_B])
        adj_A_list = sorted(adj_A_list, key=lambda acc: acc[1], reverse=True)
        adj_A_list_index = [i[0] for i in adj_A_list[:30]]
        print("adj_A_list_index",adj_A_list_index)
        return adj_A_list_index

    def makeSentence2(self,k1, k2,sel_N):
        global model, vocab_list, adj_list
        select_label = sel_N
        #     for item in sm_A_list:
        #         if item[0]=='신호등':
        #             select_label = item

        k3 = k1 + "대신 " + k2 +"이"
        adj_A_list = []
        adj_B_list = []
        for adj_item in adj_list:
            adj_A = model.similarity(adj_item, k3)
            adj_B = model.similarity(adj_item, select_label)
            adj_A_list.append([k3+" "+adj_item+" "+select_label, adj_A * adj_B])
        adj_A_list = sorted(adj_A_list, key=lambda acc: acc[1], reverse=True)
        adj_A_list_index = [i[0] for i in adj_A_list[:30]]
        print("adj_A_list_index", adj_A_list_index)
        return adj_A_list_index


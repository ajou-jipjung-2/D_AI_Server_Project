from django.shortcuts import render
import os
import pymysql
import datetime, time
from D_AI_Project.D_AI import keyvalue
import sys
import random
import csv
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from D_AI_Project.server_singletonML import singleton_fasttext
def home(request):
    if request.method == "POST":
        conn = pymysql.connect(host=keyvalue.get_hostname(), user=keyvalue.get_username(),
                               password=keyvalue.get_pw(),
                               db=keyvalue.get_dbname(), charset='utf8')
        curs = conn.cursor()
        new_keyword = request.POST["new_keyword"]
        now = datetime.datetime.utcnow()
        # sql = "insert into noun_label"++" from noun_label"
        sql = "insert into noun_label (noun, count, created_at) values ('" + new_keyword + "', '" + str(0) + "', '" + str(
            now.strftime('%Y-%m-%d %H:%M:%S')) + "');"
        # print(new_keyword)
        curs.execute(sql)
        conn.commit()
        conn.close()

    return render(request, 'home.html')

def idea(request):
    FT = singleton_fasttext.singleton_fasttext.instance()
    if request.method == "POST":
        FT.end_check("동")
        print("check")
        keyword1 = request.POST["keyword1"]
        keyword2 = request.POST["keyword2"]
        association = request.POST["association"]
        key_num = request.POST["key_num"]
        # N_list 만드는 코드 작성
        key_list=[keyword1,keyword2]
        print("request :",request.POST)
        if key_num=='1':
            N_list = FT.makevocab1(keyword1,float(association))
        elif key_num=='2':
            N_list = FT.makevocab2(keyword1,keyword2,float(association))
        print(N_list)
        # N_list = ['당근', '사과', '포도', '딸기', '아주대', '소웨', '혁중', '지석', '도연', '2조','당근', '사과', '포도', '딸기', '아주대', '소웨', '혁중', '지석', '도연', '2조','당근', '사과', '포도', '딸기', '아주대', '소웨', '혁중', '지석', '도연', '2조']
        return render(request, 'idea.html', {'N_list': N_list,'key_list':key_list,'key_num':key_num})
    else:
        # 랜덤 키워드 10개 뽑아오는 코드 작성
        voc_list = FT.get_vocab_list()
        keyword = random.sample(voc_list, 10)
        return render(request, 'idea.html', {'keyword': keyword})

def ideaResult(request):
    if request.method == "POST":
        FT = singleton_fasttext.singleton_fasttext.instance()
        keyword1 = request.POST["keyword1"]
        keyword2 = request.POST["keyword2"]
        key_num = request.POST["key_num"]
        sel_N = request.POST["select_N"]
        print("request :",request.POST)
        if key_num=='1':
            S_list = FT.makeSentence(keyword1,sel_N)
        elif key_num=='2':
            sel_N_list=[sel_N,sel_N]
            S_list = FT.makeSentence2(keyword1,keyword2,sel_N_list,20)
        print(S_list)
        return render(request, 'ideaResult.html', {'S_list': S_list, 'key_num': key_num})

    else:
        return render(request, 'idea.html')
def mindmap(request):
    return render(request, 'mindmap.html')

def ideaInfo(request):
    ideaList = []
    with open(os.path.dirname(os.path.realpath(__file__)) + '/data/idea48.csv', "r", encoding='UTF8') as f:
        reader = csv.reader(f)
        for row in reader:
            idea = []
            idea.append(row[0])
            idea.append(row[1])
            ideaList.append(idea)
    return render(request, 'ideaInfo.html', {'ideaList': ideaList})

def competition(request):
    return render(request, 'competition.html')
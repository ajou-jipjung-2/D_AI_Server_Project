from django.shortcuts import render
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from D_AI_Project.server_singletonML import singleton_fasttext
def home(request):
    return render(request, 'home.html')

def idea(request):
    if request.method == "POST":
        print("check")
        FT = singleton_fasttext.singleton_fasttext.instance()
        keyword1 = request.POST["keyword1"]
        keyword2 = request.POST["keyword2"]
        association = request.POST["association"]
        key_num = request.POST["key_num"]
        # N_list 만드는 코드 작성
        key_list=[keyword1,keyword2]
        print("request :",request.POST)
        if key_num=='1':
            N_list = FT.makevocab1(keyword1,0.3,0.7)
        elif key_num=='2':
            N_list = FT.makevocab2(keyword1,keyword2,0.3,0.7)
        print(N_list)
        # N_list = ['당근', '사과', '포도', '딸기', '아주대', '소웨', '혁중', '지석', '도연', '2조','당근', '사과', '포도', '딸기', '아주대', '소웨', '혁중', '지석', '도연', '2조','당근', '사과', '포도', '딸기', '아주대', '소웨', '혁중', '지석', '도연', '2조']
        return render(request, 'idea.html', {'N_list': N_list,'key_list':key_list,'key_num':key_num})
    else:
        # 랜덤 키워드 10개 뽑아오는 코드 작성
        keyword = ['당근', '사과', '포도', '딸기', '아주대', '소웨', '혁중', '지석', '도연', '2조']
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
            N_list = FT.makeSentence(keyword1,sel_N,0.3,0.7)
        elif key_num=='2':
            N_list = FT.makeSentence2(keyword1,keyword2,sel_N,0.3,0.7)
        print(N_list)
        return render(request, 'ideaResult.html', {'N_list': N_list})
    else:
        return render(request, 'idea.html')
def mindmap(request):
    return render(request, 'mindmap.html')

def ideaInfo(request):
    return render(request, 'ideaInfo.html')

def competition(request):
    return render(request, 'competition.html')
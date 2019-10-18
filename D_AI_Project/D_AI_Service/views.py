from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def idea(request):
    if request.method == "POST":
        keyword1 = request.POST["keyword1"]
        keyword2 = request.POST["keyword2"]
        association = request.POST["association"]
        key_num = request.POST["key_num"]
        # N_list 만드는 코드 작성
        N_list = ['당근', '사과', '포도', '딸기', '아주대', '소웨', '혁중', '지석', '도연', '2조','당근', '사과', '포도', '딸기', '아주대', '소웨', '혁중', '지석', '도연', '2조','당근', '사과', '포도', '딸기', '아주대', '소웨', '혁중', '지석', '도연', '2조']
        return render(request, 'idea.html', {'N_list': N_list})
    else:
        # 랜덤 키워드 10개 뽑아오는 코드 작성
        keyword = ['당근', '사과', '포도', '딸기', '아주대', '소웨', '혁중', '지석', '도연', '2조']
        return render(request, 'idea.html', {'keyword': keyword})

def ideaResult(request):
    if request.method == "POST":
        sel_N = request.POST["select_N"]
        # print(sel_N)
        return render(request, 'ideaResult.html', {'N': sel_N})
    else:
        return render(request, 'idea.html')
def mindmap(request):
    return render(request, 'mindmap.html')

def ideaInfo(request):
    return render(request, 'ideaInfo.html')

def competition(request):
    return render(request, 'competition.html')
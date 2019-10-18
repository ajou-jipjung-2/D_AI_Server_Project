from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def idea(request):
    return render(request, 'idea.html')

def idea_create(request):
    if request.method == "POST":
        keyword1 = request.POST["keyword1"]
        keyword2 = request.POST["keyword2"]
        association = request.POST["association"]
        key_num = request.POST["key_num"]
        # if key_num is not None:
        #     auth.login(request, user)
        #     return render(request, 'idea.html')
        # else:
        return render(request, 'idea.html')
    else:
        return render(request, 'idea.html')
    return render(request, 'idea.html')

def mindmap(request):
    return render(request, 'mindmap.html')

def ideaInfo(request):
    return render(request, 'ideaInfo.html')

def competition(request):
    return render(request, 'competition.html')
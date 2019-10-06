from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def idea(request):
    return render(request, 'idea.html')

def mindmap(request):
    return render(request, 'mindmap.html')

def ideaInfo(request):
    return render(request, 'ideaInfo.html')

def competition(request):
    return render(request, 'competition.html')
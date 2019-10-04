from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def idea(request):
    return render(request, 'idea.html')

def mindmap(request):
    return render(request, 'mindmap.html')

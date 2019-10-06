from django.contrib import admin
from django.urls import path

import D_AI_Service.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',D_AI_Service.views.home, name="home"),
    path('idea/',D_AI_Service.views.idea, name="idea"),
    path('mindmap/',D_AI_Service.views.mindmap,name="mindmap"),
    path('ideaInfo/',D_AI_Service.views.ideaInfo, name="ideaInfo"),
    path('competition/',D_AI_Service.views.competition, name="competition"),
]

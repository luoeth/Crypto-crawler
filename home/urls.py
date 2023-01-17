
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Ptt, name='Ptt'),
    path('blocktempo', views.Blocktempo, name='Blocktempo')
]

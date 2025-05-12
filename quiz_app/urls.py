from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('quiz/', views.quiz, name='quiz'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('results/', views.results, name='results'),
]
from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("quiz/", views.quiz, name="quiz"),
    path("quiz-step/", views.quiz_step, name="quiz-step"),
    path("quiz-result/", views.quiz_result, name="quiz-result")
]

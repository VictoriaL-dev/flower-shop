from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("quiz/", views.quiz_step, kwargs={"step": 1}, name="quiz_start"),
    path("quiz/<int:step>/", views.quiz_step, name="quiz_step"),
    path("quiz/result/", views.quiz_result, name="quiz_result"),
]

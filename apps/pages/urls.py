from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("card/", views.card, name="card"),
    path("catalog/", views.catalog, name="catalog"),
    path("consultation/", views.consultation, name="consultation"),
    path("order/", views.order, name="order"),
    path("order-step/", views.order_step, name="order-step"),
    path("quiz/", views.quiz, name="quiz"),
    path("quiz-step/", views.quiz_step, name="quiz-step"),
    path("quiz-result/", views.quiz_result, name="quiz-result")
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.teacher_home_view, name="teacher_home"),
    path("mystudents/", views.my_students_view, name="my_students"),
]

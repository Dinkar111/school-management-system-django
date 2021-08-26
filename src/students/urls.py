from django.urls import path

from . import views

urlpatterns = [
    path("", views.student_home_view, name="student_home"),
    path("teachers/", views.view_subject_teachers, name="my_subject_teachers"),
    path("classmates/", views.view_students_of_same_class, name="my_classmates"),
]

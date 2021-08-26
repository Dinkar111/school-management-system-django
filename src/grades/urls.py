from django.urls import path

from . import views

urlpatterns = [
    path("teacher/choose/", views.add_teacher_grade_view, name="choose_teacher_grade"),
    path("teacher/remove/", views.remove_teacher_grade, name="remove_teacher_grade"),
    path("add/", views.add_grade, name="add_grade"),
    path("view/", views.view_grades, name="view_grades"),
    path("select/", views.select_grades, name="select_grade"),
    path("delete/<int:grade_id>", views.delete_grade, name="delete_grade"),
]

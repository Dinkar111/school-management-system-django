from django.urls import path

from . import views

urlpatterns = [
    path("teacher/choose/", views.add_teacher_subject_view, name="choose_teacher_subject"),
    path("teacher/remove/", views.remove_teacher_subjects, name="remove_teacher_subject"),
    path("add_subjects/", views.add_subject_view, name="add_subject"),
    path("update/<int:subject_id>", views.update_subject_view, name="update_subject"),
    path("delete_subject/<int:subject_id>", views.delete_subject, name="delete_subject"),
]

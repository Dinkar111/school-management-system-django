from django.urls import path
from . import views

urlpatterns = [
    path('choose_subject/', views.choose_subjects_view, name='choose_subject'),
    path('add_subjects/', views.add_subject_view, name='add_subjects'),
    path('delete_subject/<int:subject_id>', views.delete_subject, name='delete_subject'),
]

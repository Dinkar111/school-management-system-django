from django.urls import path
from . import views


urlpatterns = [
    path('add_class/', views.add_grade, name='add_grade'),
    path('view_class/', views.view_grades, name='view_grades'),
]
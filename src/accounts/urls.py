from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.redirect_user, name='user_home'),
    path('admin_url/register', views.register_admin_view, name='register_admin'),
    path('admin_url/', views.admin_home_view, name='admin'),

    path('admin_url/register_student', views.register_student_view, name='admin_register_students'),
    path('admin_url/register_teacher', views.register_teacher_view, name='admin_register_teachers'),

    path('admin_url/all_students', views.all_students_view, name='admin_all_students'),
    path('admin_url/all_teachers', views.all_teachers_view, name='admin_all_teachers'),
    path('admin_url/all_subjects', views.all_subjects_view, name='admin_all_subjects'),

    path('update/', views.update_user, name='update_user'),
    path('update/change_password/', views.change_password_view, name='change_password'),
    path('admin_url/delete/<int:user_id>', views.delete_user_view, name='delete_user'),
    path('logout_admin/', views.logout_user, name='logout'),
]

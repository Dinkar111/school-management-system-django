from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("home/", views.redirect_user, name="user_home"),
    path("adminpanel/", views.admin_home_view, name="admin"),
    path("manage/student/register/", views.register_student_view, name="register_students"),
    path("manage/teacher/register/", views.register_teacher_view, name="register_teachers"),
    path("manage/student/", views.all_students_view, name="manage_students"),
    path("manage/teacher/", views.all_teachers_view, name="manage_teachers"),
    path("manage/subject/", views.all_subjects_view, name="manage_subjects"),
    path("manage/grade/", views.all_grades_view, name="manage_grades"),
    path("manage/update/student/<int:user_id>/", views.update_student, name="update_student"),
    path("manage/update/teacher/<int:user_id>/", views.update_teacher, name="update_teacher"),
    path("user/upload/img/", views.upload_profile, name="upload_photo"),
    path("update/profile/", views.update_profile, name="update_profile"),
    path("update/change_password/", views.change_password_view, name="change_password"),
    path("manage/delete/<int:user_id>/", views.delete_user_view, name="delete_user"),
    path("logout/", views.logout_user, name="logout"),
]

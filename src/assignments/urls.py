from django.urls import path

from . import views

urlpatterns = [
    path("create/<int:grade_id>/", views.create_assignments, name="create_assignments"),
    path("", views.assignments_lists, name="assignments_lists"),
    path("submit/<int:assignment_id>/", views.assignment_submission, name="assignment_submission"),
    path("check/<int:grade_id>/", views.check_assignments_lists, name="check_assignments_lists"),
    path(
        "students/<int:assignment_id>/", views.check_assignment_student_lists, name="check_assignments_students_lists"
    ),
]

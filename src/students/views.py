from django.shortcuts import render

from helper.authentication import login_required
from teachers.models import Teacher

from .models import Student

"""
    Render student context to Student home
"""


@login_required
def student_home_view(request):
    student = Student.objects.get(user=request.user.id)
    subjects = student.grade.subject_set.all()
    context = {"student": student, "subjects": subjects}
    return render(request, template_name="users/students/student_home.html", context=context)


"""
    View Teachers related with chosen subjects
"""


@login_required
def view_subject_teachers(request):
    grade = Student.objects.get(user=request.user).grade
    teachers = Teacher.objects.filter(grade=grade)
    context = {"teachers": teachers, "grade": grade}
    return render(request, template_name="users/students/my_subject_teachers.html", context=context)


"""
    View other students of same class
"""


@login_required
def view_students_of_same_class(request):
    students = Student.objects.get(user=request.user.id).grade.student_set.all()

    context = {"students": students}
    return render(request, template_name="users/students/my_classmates.html", context=context)

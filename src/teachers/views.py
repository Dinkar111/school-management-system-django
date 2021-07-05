from django.shortcuts import render
from helper.authentication import login_required
from .models import Teacher
from students.models import Student

'''
    Render student context to Student home 
'''


@login_required
def teacher_home_view(request):
    teacher = Teacher.objects.get(user=request.user.id)
    subjects = teacher.subject.filter(teacher=teacher.id)
    grades = teacher.grade.filter(teacher=teacher.id)

    context = {
        'teacher': teacher,
        'subjects': subjects,
        'grades': grades
    }
    return render(request, template_name='users/teachers/teacher_home.html', context=context)


'''
    View students teacher has to teach
'''


@login_required
def my_students_view(request):

    grades = Teacher.objects.get(user=request.user.id).grade.all()
    students = [student for grade in grades for student in grade.student_set.all()]
    context = {
        'students': students,
        'grades': grades
    }
    return render(request, template_name='users/teachers/my_students.html', context=context)

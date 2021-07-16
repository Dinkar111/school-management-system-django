from django.shortcuts import render, redirect
from helper.authentication import login_required
from django.contrib import messages
from .models import Student
from subjects.models import Subject

'''
    Render student context to Student home 
'''


@login_required
def student_home_view(request):
    student = Student.objects.get(user=request.user.id)
    subjects = student.grade.subject_set.all()
    context = {
        'student': student,
        'subjects': subjects
    }
    return render(request, template_name='users/students/student_home.html', context=context)


'''
    View Teachers related with chosen subjects
'''


@login_required
def view_subject_teachers(request):
    subjects = Student.objects.get(user=request.user.id).grade.subject_set.all()

    teachers = [{'teacher': teacher,
                 'subject': teacher.subject.all()
                 }
                for subject in subjects for teacher in subject.teacher_set.all()]
    context = {
        'teachers': teachers,
        'subjects': subjects
    }
    return render(request, template_name='users/students/my_subject_teachers.html', context=context)


'''
    View other students of same class
'''


@login_required
def view_students_of_same_class(request):
    students = Student.objects.get(user=request.user.id).grade.student_set.all()

    context = {
        'students': students
    }
    return render(request, template_name='users/students/my_classmates.html', context=context)

from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from helper.authentication import login_required
from django.db import IntegrityError

from .models import Subject
from teachers.models import Teacher
from grades.models import Grade

'''
    Choose subject by students and teachers
'''


@login_required
def choose_subjects_view(request):
    grades = Teacher.objects.get(user=request.user.id).grade.all()
    subjects = [subject for grade in grades for subject in grade.subject_set.all()]

    if request.method == "POST":
        subject_id = request.POST.get('subject_name')
        subject = Subject.objects.get(id=subject_id)
        if request.user.is_teacher:
            Teacher.objects.get(user_id=request.user.id).subject.add(subject)
            messages.success(request, "You have chose {}".format(subject.subject_name))
            return redirect('choose_subject')
    else:
        context = {
            'subjects': subjects
        }
        return render(request, template_name='subjects/choose_subjects.html', context=context)


'''
    Add Subjects and has to be logged in using admin 
'''


@staff_member_required
def add_subject_view(request):
    grades = Grade.objects.all()
    if request.method == "POST":
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        grade_name = request.POST.get('class_name')
        try:
            grade = Grade.objects.get(grade_name=grade_name)
            subject = Subject.objects.create(subject_code=subject_code, subject_name=subject_name, grade=grade)
            subject.save()
            messages.success(request, "Subject Added")
            return redirect('add_subjects')
        except IntegrityError:
            messages.error(request, "something wrong")
            return redirect('add_subjects')
    else:
        context = {
            'grades': grades
        }
        return render(request, template_name='subjects/add_subject.html', context=context)


'''
    Delete subject
'''


@staff_member_required
def delete_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    if request.method == "POST":
        subject.delete()
        return redirect('admin_all_subjects')
    else:
        return render(request, template_name='subjects/delete_subjects.html', context={'subject': subject})

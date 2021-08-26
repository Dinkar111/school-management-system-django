from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from grades.models import Grade

# from helper.authentication import login_required
from teachers.models import Teacher

from .models import Subject

"""
    Choose subject by students and teachers
"""


@staff_member_required
def add_teacher_subject_view(request):

    if request.is_ajax():
        user_id = request.GET.get("user_id")
        subject_id = request.GET.get("subject_id")
        subject_obj = Subject.objects.get(id=subject_id)
        Teacher.objects.get(user_id=user_id).subject.add(subject_obj)
        return HttpResponse("Subject Added ")


@staff_member_required
def remove_teacher_subjects(request):

    if request.is_ajax():
        user_id = request.GET.get("user_id")
        subject_id = request.GET.get("subject_id")
        teacher = Teacher.objects.get(user_id=user_id)
        subject_obj = Subject.objects.get(id=subject_id)
        teacher.subject.remove(subject_obj)
        return HttpResponse("Subject Removed")


"""
    Add Subjects and has to be logged in using admin
"""


@staff_member_required
def add_subject_view(request):
    grades = Grade.objects.all()
    if request.method == "POST":
        subject_code = request.POST.get("subject_code")
        subject_name = request.POST.get("subject_name")
        grade = request.POST.get("grade_name")
        try:
            grade = Grade.objects.get(id=grade)
            subject = Subject.objects.create(subject_code=subject_code, subject_name=subject_name, grade=grade)
            subject.save()
            messages.success(request, "Subject Added")
            return redirect("manage_subjects")
        except IntegrityError:
            messages.error(request, "Subject Code already exist or something wrong")
            return redirect("add_subject")
    else:
        context = {"grades": grades}
        return render(request, template_name="subjects/add_subject.html", context=context)


@staff_member_required
def update_subject_view(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    print(subject.grade)
    if request.method == "POST":
        subject_code = request.POST.get("subject_code")
        subject_name = request.POST.get("subject_name")
        try:
            subject.subject_code = subject_code
            subject.subject_name = subject_name
            subject.save()
            messages.success(request, "Subject Updated")
            return redirect("update_subject", subject_id=subject_id)
        except IntegrityError:
            messages.error(request, "Subject Code already exist or something wrong")
            return redirect("update_subject", subject_id=subject_id)
    else:
        context = {"subject": subject}
        return render(request, template_name="subjects/update_subject.html", context=context)


"""
    Delete subject
"""


@staff_member_required
def delete_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    subject.delete()
    messages.success(request, "SUBJECT HAS BEEN DELETED")
    return redirect("manage_subjects")

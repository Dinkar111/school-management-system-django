from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from helper.authentication import login_required
from teachers.models import Teacher

from .models import Grade

"""
    Add grades and should be admin
"""


@staff_member_required
def add_grade(request):
    if request.method == "POST":
        try:
            grade_name = request.POST.get("grade_name")
            grade = Grade.objects.create(grade_name=grade_name)
            if grade:
                messages.success(request, "{} has been added".format(grade_name))
                return redirect("add_grade")
        except IntegrityError:
            messages.warning(request, "Class name already exist")
            return redirect("add_grade")
    else:
        context = {}
        return render(request, template_name="grades/add_grade.html", context=context)


"""
    View all grades and should be admin
"""


@staff_member_required
def view_grades(request):
    grades = Grade.objects.all()
    context = {"grades": grades}
    return render(request, template_name="grades/view_grades.html", context=context)


@staff_member_required
def delete_grade(request, grade_id):
    grade = Grade.objects.get(id=grade_id)
    grade.delete()
    return redirect("manage_grades")


@login_required
def select_grades(request):
    grades = Grade.objects.filter(teacher__user_id=request.user.id)
    context = {"grades": grades}
    return render(request, template_name="users/teachers/select_grade.html", context=context)


@staff_member_required
def add_teacher_grade_view(request):

    if request.is_ajax():
        user_id = request.GET.get("user_id")
        grade_id = request.GET.get("grade_id")
        grade_obj = Grade.objects.get(id=grade_id)
        Teacher.objects.get(user_id=user_id).grade.add(grade_obj)
        return HttpResponse("Grade Added ")


@staff_member_required
def remove_teacher_grade(request):

    if request.is_ajax():
        user_id = request.GET.get("user_id")
        grade_id = request.GET.get("grade_id")
        teacher = Teacher.objects.get(user_id=user_id)
        grade_obj = Grade.objects.get(id=grade_id)
        teacher.grade.remove(grade_obj)
        return HttpResponse("Grade Removed")

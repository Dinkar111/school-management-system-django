from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import IntegrityError

from .models import Grade

'''
    Add grades and should be admin
'''
@staff_member_required
def add_grade(request):
    if request.method == "POST":
        try:
            grade_name = request.POST.get('class_name')
            grade = Grade.objects.create(grade_name=grade_name)
            if grade:
                messages.success(request, '{} has been added'.format(grade_name))
                return redirect('add_grade')
        except IntegrityError:
            messages.error(request, 'Class name already exist')
            return redirect('add_grade')
    else:
        context = {}
        return render(request, template_name='grades/add_grade.html', context=context)


'''
    View all grades and should be admin
'''
@staff_member_required
def view_grades(request):
    grades = Grade.objects.all()
    context = {
        'grades': grades
    }
    return render(request, template_name='grades/view_grades.html', context=context)

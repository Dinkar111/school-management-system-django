from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db import IntegrityError
from django.db.models import F
from helper.authentication import login_required, unauthenticated_user

from students.models import Student
from teachers.models import Teacher
from subjects.models import Subject
from grades.models import Grade
from .models import User

'''
    If already logged in redirects to user_home else login user
'''


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            user = User.objects.get(id=request.user.id)
            if user:
                return redirect('user_home')
            else:
                messages.info(request, 'User not found')
                return redirect('login')
        else:
            messages.info(request, 'Email or password is incorrect. Try again')
            return redirect('login')
    else:
        return render(request, template_name='main/login.html')


'''
    redirects users to homepage according to their roles.
'''


def redirect_user(request):
    if request.user.is_student:
        return redirect('student_home')
    elif request.user.is_teacher:
        return redirect('teacher_home')
    else:
        return redirect('admin')


'''
    Has to be logged in using admin and redirects to admin home page.
'''


@staff_member_required
def admin_home_view(request):
    admin = User.objects.get(id=request.user.id)
    if admin:
        context = {
            'admin': admin
        }
        messages.info(request, "Welcome Admin")
        return render(request, template_name='users/admin/admin_home.html', context=context)
    else:
        messages.error(request, 'No Admin found')
        return redirect('login')


'''
    Has to be logged in using admin and registers new admin
'''


@staff_member_required
def register_admin_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = User.objects.create_superuser(email=email, password=password)
        if not admin:
            messages.error(request, 'Admin could not be registered')
            return redirect('register_admin')
        else:
            messages.success(request, 'Admin has been registered')
            return redirect('register_admin')
    else:
        return render(request, template_name='users/admin/add_admin.html')


'''
    Has to be logged in using admin and registers new students
'''


@staff_member_required
def register_student_view(request):
    grades = Grade.objects.all()
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        grade_id = request.POST.get('grade_name')
        is_student = True
        try:
            grade = Grade.objects.get(id=grade_id)
            grade.no_of_students += 1
            grade.save()
            user = User.objects.create_user(email=email, password=password, full_name=full_name,
                                            address=address, phone=phone, is_student=is_student)
            student = Student.objects.create(user=user, roll_no=grade.no_of_students, grade=grade)
            student.save()
            messages.success(request, 'Student Successfully Registered')
            return redirect('admin_register_students')
        except IntegrityError:
            messages.warning(request, 'Email Already exist and Student not Registered')
            return redirect('admin_register_students')
    else:
        context = {
            'grades': grades
        }
        return render(request, template_name='users/students/add_student.html', context=context)


'''
    Has to be logged in using admin and view all students
'''


@staff_member_required
def all_students_view(request):
    grades = Grade.objects.all()
    if request.method == "POST":
        grade = request.POST.get('grade_name')
        students = Student.objects.filter(grade=grade).order_by('roll_no')
        context = {
            'students': students,
            'grades': grades
        }
    else:
        context = {
            'grades': grades
        }
    return render(request, template_name='users/admin/view_students.html', context=context)


'''
    Has to be logged in using admin and registers new teachers
'''


@staff_member_required
def register_teacher_view(request):
    grades = Grade.objects.all()
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        grade_id = request.POST.get('grade_name')
        is_teacher = True
        try:
            user = User.objects.create_user(email=email, password=password, full_name=full_name,
                                            address=address, phone=phone, is_teacher=is_teacher)
            teacher = Teacher.objects.create(user=user)
            Grade.objects.get(id=grade_id).teacher_set.add(teacher)
            teacher.save()
            messages.success(request, 'Teacher Successfully Registered')
            return redirect('admin_register_teachers')
        except IntegrityError:
            messages.warning(request, 'Email Already exist and teacher not Registered')
            return redirect('admin_register_teachers')
    else:
        context = {
            'grades': grades
        }
        return render(request, template_name='users/teachers/add_teacher.html', context=context)


'''
    View all teachers and has to be logged in using admin 
'''


@staff_member_required
def all_teachers_view(request):
    all_grades = Grade.objects.all()
    if request.method == "POST":
        grade = request.POST.get('grade_name')
        teachers = Grade.objects.get(id=grade).teacher_set.all()
        results = [{
            'teacher': teacher,
            'subject': ', '.join(list(teacher.subject.values_list('subject_name', flat=True))),
            'grade': ', '.join(list(teacher.grade.values_list('grade_name', flat=True)))
        } for teacher in teachers]
        context = {
            'results': results,
            'grades': all_grades
        }
    else:
        context = {
            'grades': all_grades
        }
    return render(request, template_name='users/admin/view_teachers.html', context=context)


'''
    view all subjects and has to be logged in using admin 
'''


@staff_member_required
def all_subjects_view(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects
    }
    return render(request, template_name='users/admin/view_subjects.html', context=context)


'''
    logout user
'''


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


'''
    Delete User
'''


@login_required
def delete_user_view(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        if user.is_student:
            student = Student.objects.get(user=user)
            student.grade.no_of_students -= 1
            student.grade.save()
            user.delete()
            return redirect('user_home')
        else:
            user.delete()
            return redirect('user_home')
    else:
        context = {
            'user': user
        }
        return render(request, 'users/delete_user.html', context=context)


'''
    Update user 
'''


@login_required
def update_user(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        data = {
            'full_name': request.POST.get('full_name'),
            'address': request.POST.get('address'),
            'phone': request.POST.get('phone')
        }

        for (key, value) in data.items():
            setattr(user, key, value)

        user.save()
        messages.success(request, 'Your Profile has been updated')
        return redirect('update_user')
    else:
        context = {
            'user': user
        }
        if not user:
            messages.error(request, "No user found")
            return redirect('update_user')
        else:
            return render(request, template_name='users/update_user.html', context=context)


'''
    Change Password 
'''


@login_required
def change_password_view(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        password = request.POST.get('password')
        hashed_password = make_password(password)
        data = {
            'password': hashed_password
        }

        for key, value in data.items():
            setattr(user, key, value)

        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Your Password has been changed')
        return redirect('change_password')
    else:
        context = {}
        return render(request, 'users/change_password.html', context=context)

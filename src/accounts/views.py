from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password, make_password

# from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError

# from django.http import JsonResponse
from django.shortcuts import redirect, render

from grades.models import Grade
from helper.authentication import login_required, unauthenticated_user
from helper.validators import email_validation, password_validation
from students.models import Student
from subjects.models import Subject
from teachers.models import Teacher

from .models import User

"""
    If already logged in redirects to user_home else login user
"""


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            user = User.objects.get(id=request.user.id)
            if user:
                return redirect("user_home")
            else:
                messages.info(request, "User not found")
                return redirect("login")
        else:
            messages.info(request, "Email or password is incorrect. Try again")
            return redirect("login")
    else:
        return render(request, template_name="main/login.html")


"""
    redirects users to homepage according to their roles.
"""


def redirect_user(request):
    if request.user.is_student:
        return redirect("student_home")
    elif request.user.is_teacher:
        return redirect("teacher_home")
    else:
        return redirect("admin")


"""
    Has to be logged in using admin and redirects to admin home page.
"""


@staff_member_required
def admin_home_view(request):
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    grades = Grade.objects.all()
    context = {"students": students, "teachers": teachers, "subjects": subjects, "grades": grades}
    messages.info(request, "Welcome Admin")
    return render(request, template_name="users/admin/admin_home.html", context=context)


"""
    Has to be logged in using admin and registers new admin
"""


@staff_member_required
def register_admin_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        admin = User.objects.create_superuser(email=email, password=password)
        if not admin:
            messages.error(request, "Admin could not be registered")
            return redirect("register_admin")
        else:
            messages.success(request, "Admin has been registered")
            return redirect("register_admin")
    else:
        return render(request, template_name="users/admin/add_admin.html")


"""
    Has to be logged in using admin and registers new students
"""


@staff_member_required
def register_student_view(request):
    grades = Grade.objects.all()
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        roll_no = request.POST.get("roll_no")
        grade_id = request.POST.get("grade_name")
        grade = Grade.objects.get(id=grade_id)
        students = Student.objects.filter(grade=grade)
        roll_exist = False

        for student in students:
            if student.roll_no == int(roll_no):
                roll_exist = True
                break

        if roll_exist:
            messages.error(request, "Roll no already exist")
            return redirect("register_students")
        else:
            is_student = True
            try:
                email_validation(email)
                grade = Grade.objects.get(id=grade_id)
                grade.no_of_students += 1
                grade.save()
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    full_name=full_name,
                    address=address,
                    phone=phone,
                    is_student=is_student,
                )
                Student.objects.create(user=user, roll_no=roll_no, grade=grade)
                messages.success(request, "Student Successfully Registered")
                return redirect("manage_students")
            except IntegrityError:
                messages.warning(request, "Email Already exist and Student not Registered")
                return redirect("register_students")
            except ValidationError as err:
                for e in err:
                    messages.warning(request, str(e))
                return redirect("register_students")
    else:
        context = {"grades": grades}
        return render(request, template_name="users/students/add_student.html", context=context)


"""
    Has to be logged in using admin and view all students
"""


@staff_member_required
def all_students_view(request):
    grades = Grade.objects.all()
    name = request.GET.get("name")

    # if request.is_ajax():
    #     grade = request.GET.get("grade")
    #     sort_by = request.GET.get("sort_by")
    #     students = Student.objects.filter(grade=grade).order_by(sort_by)
    #     paginator = Paginator(students, 5)
    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)
    #     student = serializers.serialize("python", page_obj, use_natural_foreign_keys=True)
    #     return JsonResponse(student, safe=False)
    # else:
    if name:
        students = Student.objects.filter(user__full_name__icontains=name)
    else:
        students = Student.objects.all().order_by("user_id")

    # paginator = Paginator(students, 5)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    context = {"grades": grades, "students": students}

    return render(request, template_name="users/admin/student.html", context=context)


"""
    Has to be logged in using admin and registers new teachers
"""


@staff_member_required
def register_teacher_view(request):
    grades = Grade.objects.all()
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        grade_id = request.POST.get("grade_name")
        is_teacher = True
        try:
            email_validation(email)
            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                address=address,
                phone=phone,
                is_teacher=is_teacher,
            )
            teacher = Teacher.objects.create(user=user)
            Grade.objects.get(id=grade_id).teacher_set.add(teacher)
            messages.success(request, "Teacher Successfully Registered")
            return redirect("manage_teachers")
        except IntegrityError:
            messages.warning(request, "Email Already exist and teacher not Registered")
            return redirect("register_teachers")
        except ValidationError as err:
            for e in err:
                messages.warning(request, str(e))
            return redirect("register_teachers")
    else:
        context = {"grades": grades}
        return render(request, template_name="users/teachers/add_teacher.html", context=context)


"""
    View all teachers and has to be logged in using admin
"""


@staff_member_required
def all_teachers_view(request):
    all_grades = Grade.objects.all()
    name = request.GET.get("name")
    grade = request.GET.get("grade")
    sort_by = request.GET.get("sort_by")
    if name:
        teachers = Teacher.objects.filter(user__full_name__icontains=name)
    elif grade and sort_by:
        teachers = Grade.objects.get(id=grade).teacher_set.all().order_by(sort_by)
    else:
        teachers = Teacher.objects.all()
    context = {"teachers": teachers, "grades": all_grades}
    return render(request, template_name="users/admin/teacher.html", context=context)


"""
    view all subjects and has to be logged in using admin
"""


@staff_member_required
def all_subjects_view(request):
    all_grades = Grade.objects.all()
    grade = request.GET.get("grade")
    subject_name = request.GET.get("subject_name")

    if grade:
        subjects = Subject.objects.filter(grade=grade)
    elif subject_name:
        subjects = Subject.objects.filter(subject_name__icontains=subject_name)
    else:
        subjects = Subject.objects.all()

    paginator = Paginator(subjects, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "grades": all_grades}
    return render(request, template_name="users/admin/subject.html", context=context)


@staff_member_required
def all_grades_view(request):
    all_grades = Grade.objects.all()
    context = {"grades": all_grades}
    return render(request, template_name="users/admin/grade.html", context=context)


"""
    logout user
"""


@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


"""
    Delete User
"""


@staff_member_required
def delete_user_view(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_student:
        student = Student.objects.get(user=user)
        student.grade.no_of_students -= 1
        student.grade.save()
        user.delete()
        messages.success(request, "Student HAS BEEN DELETED")
        return redirect("user_home")
    else:
        user.delete()
        messages.success(request, "Teacher HAS BEEN DELETED")
        return redirect("user_home")


"""
    Update user
"""


@staff_member_required
def update_student(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        data = {
            "full_name": request.POST.get("full_name"),
            "address": request.POST.get("address"),
            "phone": request.POST.get("phone"),
        }

        for (key, value) in data.items():
            setattr(user, key, value)

        user.save()
        messages.success(request, "Your Profile has been updated")
        return redirect("update_student", user_id=user_id)
    else:
        context = {"student": user}
        if not user:
            messages.error(request, "No user found")
            return redirect("update_student")
        else:
            return render(request, template_name="users/admin/update_student.html", context=context)


@staff_member_required
def update_teacher(request, user_id):
    teacher = Teacher.objects.get(user_id=user_id)
    grades = teacher.grade.filter(teacher=teacher.id)
    all_subjects = [subject for grade in grades for subject in grade.subject_set.all()]
    all_grades = Grade.objects.all()

    if request.method == "POST":
        teacher.user.full_name = request.POST.get("full_name")
        teacher.user.address = request.POST.get("address")
        teacher.user.phone = request.POST.get("phone")

        teacher.user.save()
        messages.success(request, "Your Profile has been updated")
        return redirect("update_teacher", user_id=user_id)
    else:
        context = {"teacher": teacher, "all_subjects": all_subjects, "all_grades": all_grades}
        if not teacher:
            messages.error(request, "No user found")
            return redirect("update_teacher")
        else:
            return render(request, template_name="users/admin/update_teacher.html", context=context)


@login_required
def upload_profile(request):
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        user.profile_pic = request.FILES["profile_image"]
        user.save()
        messages.success(request, "Your Photo has been changed")
        return redirect("upload_photo")
    else:
        return render(request, template_name="users/upload_photo.html")


"""
    Change Password
"""


@login_required
def change_password_view(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if not check_password(old_password, user.password):
            messages.error(request, "Your old password does not match")
        else:
            try:
                password_validation(new_password)
                if new_password != confirm_password:
                    messages.error(request, "Your confirmation password doesnt match")
                else:
                    hashed_password = make_password(new_password)
                    user.password = hashed_password
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Your password has been updated")
            except ValidationError as err:
                for e in err:
                    messages.error(request, str(e))
        return redirect("change_password")
    else:
        context = {}
        return render(request, "users/change_password.html", context=context)


@login_required
def update_profile(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        user.full_name = full_name
        user.address = address
        user.email = email
        user.phone = phone
        user.save()
        messages.success(request, "Your Profile has been updated")
        return redirect("update_profile")
    else:
        context = {"user": user}
        return render(request, template_name="users/update_user.html", context=context)

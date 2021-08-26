import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

from grades.models import Grade
from helper.authentication import login_required
from students.models import Student
from subjects.models import Subject
from teachers.models import Teacher

from .models import Assignment, AssignmentSubmission


@login_required
def create_assignments(request, grade_id):
    if request.method == "POST":
        question = request.POST.get("question")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")
        subject_id = request.POST.get("subject_name")
        teacher = Teacher.objects.get(user_id=request.user.id)
        subject = Subject.objects.get(id=subject_id)
        grade = Grade.objects.get(id=grade_id)

        assignment = Assignment.objects.create(
            question=question,
            description=description,
            deadline=deadline,
            subject=subject,
            teacher=teacher,
            grade=grade,
        )
        students = Student.objects.filter(grade=grade)
        for student in students:
            AssignmentSubmission.objects.create(
                assignment=assignment,
                student=student,
            )
        messages.success(request, "Assignment Added")
        return redirect("create_assignments", grade_id=grade_id)
    else:
        grade = grade_id
        teacher = Teacher.objects.get(user_id=request.user.id)
        subjects = Subject.objects.filter(grade=grade, teacher=teacher)
        context = {"subjects": subjects, "grade": grade}
        return render(request, template_name="users/teachers/create_assignments.html", context=context)


@login_required
def assignments_lists(request):
    submissions = AssignmentSubmission.objects.filter(student=request.user.student).order_by("-assignment__deadline")
    context = {"submissions": submissions}
    return render(request, template_name="users/students/assignments.html", context=context)


@login_required
def assignment_submission(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)

    if request.method == "POST":
        assignment_file = request.FILES["assignment_file"]
        student = Student.objects.get(user_id=request.user.id)
        submit_date = datetime.date.today()
        assignment_submit = AssignmentSubmission.objects.get(assignment=assignment, student=student)
        assignment_submit.assignment_file = assignment_file
        assignment_submit.submitted_on = submit_date
        assignment_submit.submitted = "Submitted"
        assignment_submit.save()
        messages.success(request, "Assignment Submitted")
        return redirect("assignments_lists")
    else:
        submission = AssignmentSubmission.objects.get(assignment=assignment, student__user_id=request.user.id)
        today = datetime.date.today()
        deadline = submission.assignment.deadline
        delta = deadline - today
        days = delta.days
        context = {"assignment": assignment, "submission": submission, "days": days}
        return render(request, template_name="users/students/submit_assignment.html", context=context)


@login_required
def check_assignments_lists(request, grade_id):
    grade = Grade.objects.get(id=grade_id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    if from_date and to_date:
        assignments = Assignment.objects.filter(grade=grade, teacher=teacher, date__range=[from_date, to_date])
    elif from_date:
        today = datetime.date.today()
        assignments = Assignment.objects.filter(grade=grade, teacher=teacher, date__range=[from_date, today])
    else:
        assignments = Assignment.objects.filter(grade=grade, teacher=teacher).order_by("-deadline")
    context = {"assignments": assignments, "grade": grade_id}
    return render(request, template_name="users/teachers/assignments.html", context=context)


@login_required
def check_assignment_student_lists(request, assignment_id):
    submissions = AssignmentSubmission.objects.filter(assignment=assignment_id)
    context = {"submissions": submissions}
    return render(request, template_name="users/teachers/check_assignment_students.html", context=context)

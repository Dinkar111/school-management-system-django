from django.db import models

from grades.models import Grade
from students.models import Student
from subjects.models import Subject
from teachers.models import Teacher


class Assignment(models.Model):
    question = models.TextField()
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    deadline = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.subject} assignment by {self.teacher}"

    class Meta:
        db_table = "assignments"


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey("Assignment", on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment_file = models.FileField(upload_to="submitted_assignments", blank=True, null=True)
    submitted_on = models.DateField(null=True)
    submitted = models.CharField(max_length=50, default="Not Submitted")

    class Meta:
        db_table = "assignment_submissions"

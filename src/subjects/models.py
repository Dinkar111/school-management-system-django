from django.db import models
from grades.models import Grade


class Subject(models.Model):
    subject_code = models.CharField(max_length=10, unique=True)
    subject_name = models.CharField(max_length=20)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.subject_name

    class Meta:
        db_table = 'subjects'
        ordering = ['grade']

from django.db import models
from django.conf import settings
from subjects.models import Subject
from grades.models import Grade


User = settings.AUTH_USER_MODEL


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject, db_table='teachers_and_subjects')
    grade = models.ManyToManyField(Grade, db_table='grades_and_teachers')

    objects = models.Manager()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        db_table = 'teachers'
        ordering = ['user']

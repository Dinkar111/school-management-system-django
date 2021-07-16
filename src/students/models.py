from django.db import models
from django.conf import settings
from grades.models import Grade


User = settings.AUTH_USER_MODEL


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.PositiveIntegerField(default=0)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        db_table = 'students'
        ordering = ['user']

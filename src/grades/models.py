from django.db import models


class Grade(models.Model):
    grade_name = models.CharField(max_length=10, unique=True)
    no_of_students = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.grade_name

    class Meta:
        db_table = 'grades'
        ordering = ['grade_name']
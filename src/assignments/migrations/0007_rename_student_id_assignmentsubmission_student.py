# Generated by Django 3.2.5 on 2021-08-30 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0006_assignment_assignmentsubmission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignmentsubmission',
            old_name='student_id',
            new_name='student',
        ),
    ]
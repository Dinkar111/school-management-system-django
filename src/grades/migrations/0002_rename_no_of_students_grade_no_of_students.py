# Generated by Django 3.2.5 on 2021-07-15 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grade',
            old_name='No_of_students',
            new_name='no_of_students',
        ),
    ]

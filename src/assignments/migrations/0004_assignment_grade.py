# Generated by Django 3.2.5 on 2021-08-30 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0003_alter_grade_options'),
        ('assignments', '0003_auto_20210830_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='grades.grade'),
        ),
    ]

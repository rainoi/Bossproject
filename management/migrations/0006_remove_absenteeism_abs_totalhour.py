# Generated by Django 4.1.7 on 2023-05-15 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0005_absenteeism_abs_totalhour_absenteeism_abs_totalwage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="absenteeism",
            name="abs_totalhour",
        ),
    ]

# Generated by Django 4.1.7 on 2023-05-15 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="absenteeism",
            name="abs_finish",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="absenteeism",
            name="abs_start",
            field=models.DateTimeField(),
        ),
    ]

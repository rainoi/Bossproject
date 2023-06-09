# Generated by Django 4.1.7 on 2023-05-29 15:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0009_rename_user_id_user_user_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="Timeinfo",
            fields=[
                ("tim_id", models.AutoField(primary_key=True, serialize=False)),
                ("tim_time", models.TimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name="schedule_exchange",
            name="employee",
        ),
        migrations.RemoveField(
            model_name="schedule_exchange",
            name="schedule",
        ),
        migrations.RemoveField(
            model_name="schedulefix",
            name="sch_finish",
        ),
        migrations.RemoveField(
            model_name="schedulefix",
            name="sch_start",
        ),
        migrations.RemoveField(
            model_name="user",
            name="employee",
        ),
        migrations.AddField(
            model_name="employee",
            name="user",
            field=models.ForeignKey(
                db_column="user_email",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="management.user",
            ),
        ),
        migrations.AddField(
            model_name="schedule_exchange",
            name="employee1",
            field=models.ForeignKey(
                db_column="emp_id1",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exchange_employee1",
                to="management.employee",
            ),
        ),
        migrations.AddField(
            model_name="schedule_exchange",
            name="employee2",
            field=models.ForeignKey(
                db_column="emp_id2",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exchange_employee2",
                to="management.employee",
            ),
        ),
        migrations.AddField(
            model_name="schedule_exchange",
            name="schedule1",
            field=models.ForeignKey(
                db_column="sch_id1",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exchange_schedule1",
                to="management.schedulefix",
            ),
        ),
        migrations.AddField(
            model_name="schedule_exchange",
            name="schedule2",
            field=models.ForeignKey(
                db_column="sch_id2",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exchange_schedule2",
                to="management.schedulefix",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_level",
            field=models.CharField(default=1, max_length=1),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_pw",
            field=models.CharField(
                max_length=11, validators=[django.core.validators.MinLengthValidator(8)]
            ),
        ),
        migrations.AddField(
            model_name="schedulefix",
            name="time_end",
            field=models.ForeignKey(
                db_column="time_end",
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="schedule_timeend",
                to="management.timeinfo",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="schedulefix",
            name="time_start",
            field=models.ForeignKey(
                db_column="time_start",
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="schedule_timestart",
                to="management.timeinfo",
            ),
            preserve_default=False,
        ),
    ]

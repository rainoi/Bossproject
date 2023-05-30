from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.utils.functional import cached_property

class Employee(models.Model):
    # here
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=10)
    emp_birth = models.DateField()
    emp_gender = models.CharField(max_length=1)
    emp_address = models.CharField(max_length=45)
    emp_phone = models.CharField(max_length=45)
    emp_account = models.CharField(max_length=45)
    emp_email = models.EmailField()  # email
    emp_level = models.CharField(max_length=1, default=1)
    emp_plus = models.IntegerField(default=0)

class Timeinfo(models.Model):
    tim_id = models.AutoField(primary_key=True)
    tim_time = models.TimeField()

class Schedulefix(models.Model):
    # here
    sch_id = models.AutoField(primary_key=True)
    sch_date = models.DateField()
    time_start = models.ForeignKey(Timeinfo, related_name="schedule_timestart", on_delete=models.CASCADE, db_column="time_start")  #Starttime
    time_end = models.ForeignKey(Timeinfo, related_name="schedule_timeend", on_delete=models.CASCADE, db_column="time_end")  #Endtime
    #sch_start = models.DateTimeField()
    #sch_finish = models.DateTimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="emp_id")

class Schedule_exchange(models.Model):
    # write here
    employee1 = models.ForeignKey(Employee, related_name="exchange_employee1", on_delete=models.CASCADE, db_column="emp_id1")
    employee2 = models.ForeignKey(Employee, related_name="exchange_employee2", on_delete=models.CASCADE, db_column="emp_id2")
    schedule1 = models.ForeignKey(Schedulefix, related_name="exchange_schedule1", on_delete=models.CASCADE, db_column="sch_id1")
    schedule2 = models.ForeignKey(Schedulefix, related_name="exchange_schedule2", on_delete=models.CASCADE, db_column="sch_id2")

class Wage_hourly(models.Model):
    # write here
    wag_id = models.AutoField(primary_key=True)
    wag_info = models.CharField(max_length=10)
    wag_price = models.IntegerField(default=0)


class Absenteeism(models.Model):
    # wrtie here
    abs_id = models.AutoField(primary_key=True)
    abs_start = models.DateTimeField()
    abs_finish = models.DateTimeField()
    abs_totalmin = models.IntegerField(default=0)
    abs_totalwage = models.IntegerField(default=0)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="emp_id")
    wageinfo = models.ForeignKey(Wage_hourly, on_delete=models.CASCADE, db_column="wag_id")

    def calculate_totalhour(self):
        time_difference = self.abs_finish - self.abs_start
        self.abs_totalmin = int(time_difference.total_seconds() / 60)

    def calculate_totalwage(self):
        wage_price = self.wageinfo.wag_price +self.employee.emp_plus
        self.abs_totalwage = int(self.abs_totalmin * (wage_price/60))

    def save(self, *args, **kwargs):
        self.calculate_totalhour()
        self.calculate_totalwage()
        super().save(*args, **kwargs)

class Notice(models.Model):
    not_id = models.AutoField(primary_key=True)
    not_title = models.CharField(max_length=50)
    not_contents = models.CharField(max_length=200)
    employee_notice = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="emp_id")

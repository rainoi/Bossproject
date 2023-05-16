from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.utils.functional import cached_property
# question = models.ForeignKey(Question, on_delete=models.CASCADE)
# FK 연결

class Employee(models.Model):
    # here
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=10)
    emp_birth = models.DateField()
    emp_gender = models.CharField(max_length=1)
    emp_address = models.CharField(max_length=45)
    emp_phone = models.CharField(max_length=45)
    emp_account = models.CharField(max_length=45)
    emp_plus = models.IntegerField(default=0)


class Schedulefix(models.Model):
    # here
    sch_id = models.AutoField(primary_key=True)
    sch_date = models.DateField()
    sch_start = models.DateTimeField()
    sch_finish = models.DateTimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="emp_id")


class Schedule_exchange(models.Model):
    # write here
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="employee_id")
    schedule = models.ForeignKey(Schedulefix, on_delete=models.CASCADE, db_column="sch_id")


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

class User(models.Model):
    # wrtie here
    user_id = models.EmailField(primary_key=True)  # email
    user_pw = models.CharField(validators=[MinLengthValidator(8)], max_length=10)  # min length
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="emp_id")  # foreignkey


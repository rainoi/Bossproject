from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.utils.functional import cached_property

#question = models.ForeignKey(Question, on_delete=models.CASCADE)
#FK 연결

class Employee(models.Model):
    #here
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=10)
    emp_birth = models.DateField()
    emp_gender = models.CharField(max_length=1)
    emp_address = models.CharField(max_length=45)
    emp_phone = models.CharField(max_length=45)
    emp_account = models.CharField(max_length=45)
    emp_plus = models.IntegerField(default=0)

class Schedulefix(models.Model):
    #here
    sch_id = models.AutoField(primary_key=True)
    sch_date = models.DateField()
    sch_start = models.DateTimeField()
    sch_finish = models.DateTimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,db_column="emp_id")

class Schedule_exchange(models.Model):
    #write here
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,db_column="employee_id")
    schedule = models.ForeignKey(Schedulefix, on_delete=models.CASCADE, db_column="sch_id")

class Wage_hourly(models.Model):
    #write here
    wag_id = models.AutoField(primary_key=True)
    wag_info = models.CharField(max_length=10)
    wag_price = models.IntegerField(default=0)

class Absenteeism(models.Model):
    #wrtie here
    abs_id = models.AutoField(primary_key=True)
    abs_start = models.DateTimeField()
    abs_finish = models.DateTimeField()
    abs_totalhour = models.IntegerField(default=0)
    abs_totalwage = models.IntegerField(default=0)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="emp_id")
    wageinfo = models.ForeignKey(Wage_hourly, on_delete=models.CASCADE, db_column="wag_id")

    @cached_property
    def totalhour(self,*args, **kwargs):
        time_difference = self.abs_finish - self.abs_start
        self.abs_totalhour = time_difference.total_seconds() / 60
        wage_price = self.wageinfo.wag_price
        emp_add_price = self.employee.emp_plus / 60
        self.abs_totalwage = int(self.abs_totalhour * (wage_price+emp_add_price))
        super().totalhour(*args, **kwargs)

    @cached_property
    def abs_totalhour(self):
        return self.abs_totalhour

    @cached_property
    def abs_totalwage(self):
        return self.abs_totalwage

    
class User(models.Model):
    #wrtie here
    user_id = models.EmailField(primary_key=True)  #email
    user_pw = models.CharField(validators=[MinLengthValidator(8)],max_length=10)  #min length
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column="emp_id")  #foreignkey



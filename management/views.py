from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect

def login(request):
    return render(request, 'login.html')

# Create your views here.
from management.models import Employee
# Create your views here.

# def list_employees(request):
#         employees = Employee.objects.all()
#         return render(request, 'management/list_employees', {'employees' : employees})
#
# def register_worktime(request):
#     form = UserForm(request.POST or None)
#
#     if form.is_valid():
#         form.save()
#         return redirect('Absenteeism')
#
#     return render(request, 'management/login.html', {'form': form})
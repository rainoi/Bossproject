from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Wage_hourly, Employee
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import EmployeeForm
from management.models import Absenteeism
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.models import User


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('list_employees')  # 로그인 성공 시 list_employees 페이지로 리디렉션
        else:
            # 인증 실패 처리
            return render(request, 'management/login.html', {'error': '잘못된 자격 증명입니다.'})
    return render(request, 'management/login.html')


def list_wages(request):
    wages = Wage_hourly.objects.all()
    return render(request, 'management/list_wages.html', {'wages': wages})


@login_required
def list_employees(request):
    user = request.user
    if user.username == 'boss':
        employees = Employee.objects.all()  # Get all employees' information
    else:
        email = user.email
        employees = Employee.objects.filter(emp_email=email)

    return render(request, 'management/employee_list.html', {'employees': employees})


def create_employee(request):
    form = EmployeeForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('list_employees')

    return render(request, 'management/employee_form.html', {'form': form})


def update_employee(request, emp_id):
    employee = Employee.objects.get(emp_id=emp_id)
    form = EmployeeForm(request.POST or None, instance=employee)

    if form.is_valid():
        form.save()
        return redirect('list_employees')

    return render(request, 'management/employee_form.html', {'emp': employee, 'form': form})


def delete_employee(request, emp_id):
    employee = Employee.objects.get(emp_id=emp_id)
    employee.delete()
    return redirect('list_employees')  # 'home'은 홈 페이지의 URL 이름으로 변경해야 합니다.


# logout using self-defined function
def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


# 필터링 해보다가 안되는거
def list_statement(request):
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')
    selected_employee_name = request.GET.get('employee')

    if not selected_year:
        selected_year = datetime.now().year

    if selected_month and selected_year and selected_employee_name:
        selected_employee_id = Employee.objects.get(emp_name=selected_employee_name).emp_id
        message = f'{selected_year}년 {selected_month}월 {selected_employee_name}의 명세서'
        lists = Absenteeism.objects.filter(
            abs_start__year=selected_year,
            abs_start__month=selected_month,
            employee=selected_employee_id
        )
    elif selected_month and selected_year:
        message = f'{selected_year}년 {selected_month}월의 명세서'
        lists = Absenteeism.objects.filter(
            abs_start__year=selected_year,
            abs_start__month=selected_month
        )
    elif selected_year and selected_employee_name:
        selected_employee_id = Employee.objects.get(emp_name=selected_employee_name).emp_id
        message = f'{selected_year}년 {selected_employee_name}의 명세서'
        lists = Absenteeism.objects.filter(
            abs_start__year=selected_year,
            employee=selected_employee_id
        )
    elif selected_year:
        message = f'{selected_year}년의 명세서'
        lists = Absenteeism.objects.filter(
            abs_start__year=selected_year
        )
    else:
        message = '검색어를 입력하세요.'
        lists = Absenteeism.objects.order_by('employee')

    total_sum = lists.aggregate(total_sum=Sum('abs_totalmin'))['total_sum'] or 0
    total_wage = lists.aggregate(total_wage=Sum('abs_totalwage'))['total_wage'] or 0

    return render(request, 'management/list_statement.html', {
        'message': message,
        'lists': lists,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'selected_employee_name': selected_employee_name,
        'total_sum': total_sum,
        'total_wage': total_wage,
        'years': range(2021, datetime.now().year + 1),
        'months': [
            (1, '1월'), (2, '2월'), (3, '3월'), (4, '4월'), (5, '5월'), (6, '6월'),
            (7, '7월'), (8, '8월'), (9, '9월'), (10, '10월'), (11, '11월'), (12, '12월')
        ],
        'employees': Employee.objects.all()
    })


from django.http import JsonResponse


def save_absenteeism(request):
    if request.method == 'POST':
        time = request.POST['time']
        absenteeism = Absenteeism(abs_start=time)
        absenteeism.save()
        response_data = {
            'message': '시간이 성공적으로 저장되었습니다.'
        }
        return JsonResponse(response_data)
        # return HttpResponse(status=204)

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
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

    return render(request, 'management/list_employees.html', {'employees': employees})


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


def list_statement(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    employee = request.GET.get('employee')

    if not year:
        year = datetime.now().year
    if month and year and employee:
        message = f'{year}년 {month}월 {employee}의 명세서'
        lists = Absenteeism.objects.filter(abs_start__year=year, abs_start__month=month, employee=employee)
    else:
        message = '검색어를 입력하세요.'
        lists = Absenteeism.objects.order_by('employee')
    total = lists.aggregate(total_sum=Sum('abs_totalmin'), total_wage=Sum('abs_totalwage'))

    return render(request, 'management/list_statement.html', {'message': message, 'lists': lists, 'total': total})

    def convert_to_hours_minutes(total_minutes):
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f'{hours}시간 {minutes}분'

    context = {
        'message': message,
        'lists': lists,
        'total_sum': convert_to_hours_minutes(total['total_sum']),
        'total_wage': total['total_wage']
    }
    return render(request, "management/list_statement.html", context)


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

# def social_login(request):
#     # 현재 로그인한 사용자의 소셜 계정 정보 가져오기
#     social_account = SocialAccount.objects.get(user=request.user)
#     social_email = social_account.extra_data.get('email', '')  # 이메일 정보 가져오기
#
#     if social_email:
#         # 이메일로 사용자 확인
#         User = get_user_model()
#         user = User.objects.filter(emp_email=social_email).first()
#
#         if user:
#             # 사용자가 존재하는 경우
#             user_id = user.id
#             # 사용자 고유의 페이지로 리다이렉트
#             return redirect(f'/page/{user_id}/')
#
#     # 사용자가 존재하지 않거나 이메일 정보가 없는 경우 등에 대한 처리
#     return redirect('/')


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

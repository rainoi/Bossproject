from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Wage_hourly, Employee
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout



def login(request):
    if 'id' in request.POST and 'password' in request.POST:
        id = request.POST['id']
        password = request.POST['password']
        # hashed_password = make_password(password)
        user = authenticate(request, username=id, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('list_employees') # 로그인 성공 시 list_employees 페이지로 리디렉션
        else:
            # 인증 실패 처리
            return render(request, 'management/login.html', {'error': '잘못된 자격 증명입니다.'})
    return render(request, 'management/login.html')

def list_wages(request):
     wages = Wage_hourly.objects.all()
     return render(request, 'management/list_wages.html', {'wages':wages})

@login_required
def list_employees(request):
    user = request.user
    # if user.username == 'boss':
    #     employees = Employee.objects.all()  # 모든 직원 정보를 가져옴
    # else:
    #     email = EmailAddress.objects.get(user=user).email
    #     employees = Employee.objects.filter(emp_email=email)
    if user.username == 'boss' or (user.email and Employee.objects.filter(emp_email=user.email).exists()):
        employees = Employee.objects.all()
    else:
        employees = []

    return render(request, 'management/list_employees.html', {'employees': employees})

# logout using self-defined function
# def logout(request):
#     """Logs out user"""
#     auth_logout(request)
#     return redirect('/')


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
from django.urls import path

import management.views
from management import views
from .views import list_employees, login


urlpatterns = [
    path('', views.list_wages, name = 'list_wages'),
    #path('page/<int:id>/', list_employees, name='employee_page'),
    path('list_employees/', views.list_employees, name='list_employees'),
    path('login/', views.login, name='login')
    #path('social-login/', social_login, name='social_login'),
]
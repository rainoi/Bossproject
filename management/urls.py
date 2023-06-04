from django.urls import path
import management.views
from management import views
from .views import list_employees, login


urlpatterns = [
    path('', views.list_wages, name='list_wages'),
    # path('page/<int:id>/', list_employees, name='employee_page'),
    path('list_employees/', views.list_employees, name='list_employees'),
    path('login/', views.login, name='login'),
    path('empupdate/<int:emp_id>/', views.update_employee, name='update_employee'),
    path('empdelete/<int:emp_id>/', views.delete_employee, name='delete_employee'),
    path('empcreate/', views.create_employee, name='create_employee'),
    path('sta/', views.list_statement, name="list_statement"),
    #path('save_time_to_db/', views.save_absenteeism, name='save_time_to_db'),


]

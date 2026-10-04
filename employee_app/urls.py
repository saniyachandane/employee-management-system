from django.urls import path,include
from . import views

urlpatterns = [
    path('add-employee/',views.add_employees,name='add_employee'),
    
    path('show-employee/',views.show_employees,name='show_employees'),
    
    path('update-employee/<str:emp_id>',views.update_employee,name='update_employee'),
    
    path('delete-employee/<str:emp_id>/', views.delete_employee, name='delete_employee'),
    
    path('login/', views.user_login, name='user_login'),
    
    path('logout/', views.user_logout, name='user_logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('employee-details/<str:emp_id>/',views.employee_details,name='employee_details'),
    
    path('export-employees/',views.export_employees,name='export_employees'),
    
    path('export-employees-pdf/',views.export_employees_pdf,name='export_employees_pdf'),
    
    path('profile/', views.profile, name='profile'),

    path('change-password/',views.change_password,name='change_password'),
    
]
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Employees
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse
from django.db.models import Count, Sum, Avg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.contrib.auth import update_session_auth_hash

# Create your views here.
@login_required
def add_employees(request):

    if request.method == 'POST':

        emp_id = request.POST.get('emp_id', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        department = request.POST.get('department', '').strip()
        salary = request.POST.get('salary', '').strip()
        photo = request.FILES.get('photo')

        # Empty field validation
        if not emp_id or not name or not email or not phone or not department or not salary:
            messages.error(request, "All fields are required.")
            return redirect('add_employee')

        # Phone validation
        if not phone.isdigit():
            messages.error(request, "Phone number must contain only digits.")
            return redirect('add_employee')

        if len(phone) != 10:
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect('add_employee')

        # Employee ID validation
        if Employees.objects.filter(emp_id=emp_id).exists():
            messages.error(request, "Employee ID already exists.")
            return redirect('add_employee')

        # Email validation
        if '@' not in email or '.' not in email:
            messages.error(request, "Please enter a valid email address.")
            return redirect('add_employee')

        # Duplicate email
        if Employees.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('add_employee')

        # Salary validation
        try:
            salary = float(salary)

            if salary <= 0:
                messages.error(request, "Salary must be greater than 0.")
                return redirect('add_employee')

        except ValueError:
            messages.error(request, "Please enter a valid salary.")
            return redirect('add_employee')

        # Create employee
        Employees.objects.create(
            emp_id=emp_id,
            name=name,
            email=email,
            phone=phone,
            department=department,
            salary=salary,
            photo=photo
        )

        messages.success(
            request,
            'Employee Added Successfully...!!'
        )

        return redirect('show_employees')

    return render(request, 'add_employee.html')

@login_required
def show_employees(request):

    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '')
    department = request.GET.get('department', '')

    employees = Employees.objects.all()

    # Search
    if search:
        employees = employees.filter(
            name__icontains=search
        ) | employees.filter(
            emp_id__icontains=search
        )

    # Department Filter
    if department:
        employees = employees.filter(
            department=department
        )

    # Sorting
    if sort == 'name_asc':
        employees = employees.order_by('name')

    elif sort == 'name_desc':
        employees = employees.order_by('-name')

    elif sort == 'salary_asc':
        employees = employees.order_by('salary')

    elif sort == 'salary_desc':
        employees = employees.order_by('-salary')

    # Pagination
    paginator = Paginator(employees, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    # Departments for dropdown
    departments = Employees.objects.values_list(
        'department',
        flat=True
    ).distinct()

    return render(
        request,
        'show_employees.html',
        {
            'employees': page_obj,
            'search': search,
            'sort': sort,
            'department': department,
            'departments': departments,
        }
    )
    
    
@login_required
def update_employee(request, emp_id):

    employee = Employees.objects.get(emp_id=emp_id)

    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        department = request.POST['department']
        salary = request.POST['salary']

        # Phone validation
        if not phone.isdigit():
            messages.error(request, "Phone number must contain only digits.")
            return redirect('update_employee', emp_id=emp_id)

        if len(phone) != 10:
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect('update_employee', emp_id=emp_id)

        # Email duplicate validation
        if Employees.objects.filter(email=email).exclude(emp_id=emp_id).exists():
            messages.error(request, "Email already exists.")
            return redirect('update_employee', emp_id=emp_id)

        # Update employee
        employee.name = name
        employee.email = email
        employee.phone = phone
        employee.department = department
        employee.salary = salary

        # New photo
        photo = request.FILES.get('photo')

        if photo:
            employee.photo = photo

        employee.save()

        messages.success(request, "Employee updated successfully!")

        return redirect('show_employees')

    return render(request, 'update_employee.html', {
        'employee': employee
    })

@login_required
def delete_employee(request, emp_id):

    if request.method == "POST":

        employee = Employees.objects.get(emp_id=emp_id)

        employee.delete()

        messages.success(
            request,
            "Employee deleted successfully!"
        )

        return redirect("show_employees")

    return redirect("show_employees")


def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            messages.error(
                request,
                'Invalid username or password...!'
            )

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def employee_details(request, emp_id):

    employee = Employees.objects.get(emp_id=emp_id)

    return render(
        request,
        'employee_details.html',
        {'employee': employee}
    )

@login_required
def export_employees(request):

    search = request.GET.get('search', '')
    department = request.GET.get('department', '')

    employees = Employees.objects.all()

    if search:
        employees = employees.filter(
            name__icontains=search
        ) | employees.filter(
            emp_id__icontains=search
        )

    if department:
        employees = employees.filter(
            department=department
        )

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="employees.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Employee ID',
        'Name',
        'Email',
        'Phone',
        'Department',
        'Salary'
    ])

    for employee in employees:

        writer.writerow([
            employee.emp_id,
            employee.name,
            employee.email,
            employee.phone,
            employee.department,
            employee.salary
        ])

    return response

@login_required
def dashboard(request):

    total_employees = Employees.objects.count()

    total_departments = Employees.objects.values(
        'department'
    ).distinct().count()

    total_salary = Employees.objects.aggregate(
        total=Sum('salary')
    )['total'] or 0

    average_salary = Employees.objects.aggregate(
        average=Avg('salary')
    )['average'] or 0

    department_data = Employees.objects.values(
        'department'
    ).annotate(
        total=Count('emp_id')
    ).order_by('department')
    
    salary_data = Employees.objects.values(
    'department'
    ).annotate(
        average_salary=Avg('salary')
    ).order_by('department')

    recent_employees = Employees.objects.all().order_by('-emp_id')[:5]

    return render(request, 'dashboard.html', {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_salary': total_salary,
        'average_salary': average_salary,
        'department_data': department_data,
        'recent_employees': recent_employees,
        'salary_data': salary_data,
    })
    
@login_required
def export_employees_pdf(request):

    search = request.GET.get('search', '')
    department = request.GET.get('department', '')
    sort = request.GET.get('sort', '')

    employees = Employees.objects.all()

    # Search
    if search:
        employees = employees.filter(
            name__icontains=search
        ) | employees.filter(
            emp_id__icontains=search
        )

    # Department Filter
    if department:
        employees = employees.filter(
            department=department
        )

    # Sorting
    if sort == 'name_asc':
        employees = employees.order_by('name')

    elif sort == 'name_desc':
        employees = employees.order_by('-name')

    elif sort == 'salary_asc':
        employees = employees.order_by('salary')

    elif sort == 'salary_desc':
        employees = employees.order_by('-salary')


    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        'attachment; filename="employees.pdf"'
    )

    pdf = canvas.Canvas(response, pagesize=A4)

    width, height = A4

    # Title
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(200, height - 50, "Employee Report")

    y = height - 100

    # Table Header
    pdf.setFont("Helvetica-Bold", 9)

    pdf.drawString(30, y, "ID")
    pdf.drawString(70, y, "Name")
    pdf.drawString(180, y, "Email")
    pdf.drawString(330, y, "Phone")
    pdf.drawString(400, y, "Department")
    pdf.drawString(490, y, "Salary")

    y -= 20

    pdf.setFont("Helvetica", 8)

    for employee in employees:

        pdf.drawString(30, y, str(employee.emp_id))
        pdf.drawString(70, y, str(employee.name)[:18])
        pdf.drawString(180, y, str(employee.email)[:25])
        pdf.drawString(330, y, str(employee.phone))
        pdf.drawString(400, y, str(employee.department)[:12])
        pdf.drawString(490, y, str(employee.salary))

        y -= 20

        if y < 40:

            pdf.showPage()

            pdf.setFont("Helvetica", 8)

            y = height - 50


    pdf.save()

    return response

@login_required
def profile(request):

    return render(request, 'profile.html')

@login_required
def change_password(request):

    if request.method == 'POST':

        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not current_password or not new_password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect('change_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('change_password')

        if len(new_password) < 8:
            messages.error(
                request,
                "New password must contain at least 8 characters."
            )
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(
            request,
            "Password changed successfully!"
        )

        return redirect('profile')

    return render(request, 'change_password.html')
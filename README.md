# Employee Management System

A web-based Employee Management System developed using **Python, Django, MySQL, HTML, CSS, JavaScript and Bootstrap**.

The system helps manage employee records through a secure and user-friendly dashboard.

## 🚀 Features

* 🔐 User Login and Logout
* 👤 User Profile
* 🔑 Change Password
* ➕ Add Employee
* 📋 View Employee List
* ✏️ Update Employee
* 🗑️ Delete Employee
* 🔎 Search Employees
* 🏢 Department Filter
* ↕️ Sort Employees by Name and Salary
* 📄 Pagination
* 🖼️ Employee Profile Photo Upload
* 👨‍💼 Employee Details Page
* 📊 Dashboard Statistics
* 📈 Department-wise Employee Charts
* 💰 Salary Statistics
* 📥 Export Employee Data to CSV
* 📄 Export Employee Data to PDF
* ✅ Form Validation
* 🔒 Login-protected Employee Management

## 🛠️ Technologies Used

### Backend

* Python
* Django
* Django ORM

### Frontend

* HTML
* CSS
* JavaScript
* Bootstrap 5

### Database

* MySQL

### Other Tools

* Chart.js
* Pillow
* CSV
* ReportLab

## 📂 Main Modules


Employee Management System
│
├── Login
├── Dashboard
│
├── Employee Management
│   ├── Add Employee
│   ├── View Employees
│   ├── Update Employee
│   ├── Delete Employee
│   └── Employee Details
│
├── Search & Filter
│
├── Sorting & Pagination
│
├── Reports
│   ├── CSV Export
│   └── PDF Export
│
├── Profile
│
└── Change Password


## 📊 Dashboard

The dashboard provides:

* Total number of employees
* Total departments
* Total salary
* Average salary
* Department-wise employee statistics
* Department-wise average salary
* Recent employees
* Visual charts

## 🔐 Security

The project uses Django authentication and login protection.

Employee management pages are accessible only to authenticated users.

Additional security features include:

* CSRF protection
* Login-required views
* Password validation
* POST-based employee deletion
* Input validation

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project

```bash
cd employee_project
```

### 3. Install dependencies

```bash
pip install django mysqlclient pillow reportlab
```

### 4. Configure MySQL

Create a MySQL database and update the database configuration in:

```text
settings.py
```

### 5. Run migrations

```bash
py manage.py makemigrations
py manage.py migrate
```

### 6. Create admin user

```bash
py manage.py createsuperuser
```

### 7. Start the server

```bash
py manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## 👩‍💻 Project Purpose

This project was developed to gain practical experience in:

* Django web development
* Python backend development
* MySQL database management
* CRUD operations
* Authentication
* Django ORM
* File upload
* Search and filtering
* Data export
* Dashboard development
* REST-style backend concepts

## 🔮 Future Improvements

* Employee attendance management
* Leave management
* Role-based access control
* Email notifications
* REST API integration
* Employee salary reports
* Advanced analytics

## 👩‍💻 Developer

**Saniya Vishwas Chandane**

B.Tech Computer Science Engineering

Skills: Python | Django | SQL | MySQL | HTML | CSS | JavaScript

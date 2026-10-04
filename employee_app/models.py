from django.db import models

# Create your models here.
class Employees(models.Model):
    emp_id=models.CharField(max_length=10,unique=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15)
    department=models.CharField(max_length=50)
    salary=models.DecimalField(max_digits=10,decimal_places=2)
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)
    
    def __str__(self):
        return self.name
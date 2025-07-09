from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # <-- set role here

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (('user', 'User'), ('staff', 'Staff'), ('admin', 'Admin'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    aadhar_number = models.CharField(max_length=12, unique=True)

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True) 
    block_number = models.CharField(max_length=50)
    building_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.title} ({self.status})"



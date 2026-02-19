from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('alumni', 'Alumni'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    enrollment_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        default='',
    )

    USERNAME_FIELD = "enrollment_number"
    REQUIRED_FIELDS = ["username"]


    def __str__(self):
        return f"{self.enrollment_number} ({self.role})"
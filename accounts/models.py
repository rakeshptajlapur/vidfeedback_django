from django.contrib.auth.models import AbstractUser
from django.db import models

class BusinessOwner(AbstractUser):
    PLAN_CHOICES = [
        ('FREE', 'Free - 1 form, 10 submissions'),
        ('BASIC', 'Basic - 5 forms, 100 submissions'),
        ('PRO', 'Pro - Unlimited'),
    ]
    
    business_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    plan_type = models.CharField(max_length=10, choices=PLAN_CHOICES, default='FREE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} ({self.email})"

from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

# Create your models here.
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), null=True)

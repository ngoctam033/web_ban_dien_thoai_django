from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import check_password as django_check_password
from django.contrib.auth.models import AbstractUser, Group, Permission

class Customer(AbstractUser):
    customers_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    tel = models.CharField(max_length=10)
    address = models.CharField(max_length=255, default='No address provided')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)
    class Meta:
        db_table = "customers"

    REQUIRED_FIELDS = ['email','tel']
    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)
    def __str__(self):
        return str(self.customers_id)

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """Represents role class model"""
    name = models.CharField(
        max_length=200,
        blank=True,
        null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Represents user class model"""
    id = models.CharField(
        max_length=100,
        unique=True,
        default=uuid.uuid4,
        primary_key=True)
    roles = models.ManyToManyField(Role, blank=True)
    org_id = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    identification_no = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Employee(models.Model):
    """Represents employee class model"""
    employee_no = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Restaurant(models.Model):
    """Represents restaurant class model"""
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    contact_no = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Menu(models.Model):
    """Represents menu class model"""
    restaurant = models.ForeignKey(
        Restaurant,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    file = models.FileField(upload_to='menus/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.CharField(max_length=50, null=True, blank=True)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.restaurant.name


class Vote(models.Model):
    """Represents vote class model"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee}'

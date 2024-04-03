import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    lang_id = models.IntegerField(null=True, blank=True)
    chat_id = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Adjust this line

    class Meta:
        verbose_name = 'Клиенты'
        verbose_name_plural = 'Клиенты'




class Order(models.Model):
    order_id = models.IntegerField( unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField()
    amount = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user



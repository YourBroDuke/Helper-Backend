# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# User table
class User(models.Model):
    name = models.CharField(max_length=20)
    hashed_password = models.CharField(max_length=32)
    email_address = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    balance = models.DecimalField(max_digits=5, decimal_places=4)


# Order table
class Order(models.Model):
    type = models.IntegerField()
    campus = models.IntegerField()
    title = models.CharField(max_length=32)
    detail = models.TextField()
    current_num = models.IntegerField()
    max_num = models.IntegerField()
    reward = models.DecimalField(max_digits=5, decimal_places=4)
    state = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()


# Order to User
class OrderToUser(models.Model):
    role = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

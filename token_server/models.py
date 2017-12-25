# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Market(models.Model):
    market_name = models.CharField(max_length=120)
    create_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    active_flag = models.BooleanField(default=True)

    def __str__(self):
        return self.market_name


class AdminAccount(models.Model):
    user = models.OneToOneField(User)
    create_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    active_flag = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class TokenType(models.Model):
    token_name = models.CharField(max_length=200, blank=False, null=False)
    market_limit = models.IntegerField(blank=False, null=False)
    active_flag = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.token_name


class TokenKey(models.Model):
    token_hash = models.CharField(max_length=200, blank=False, null=False)
    token_type = models.ForeignKey(TokenType, on_delete=models.CASCADE)

    expire_date = models.DateTimeField(blank=True, null=True)
    customer_email = models.CharField(max_length=200, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    active_flag = models.BooleanField(default=True)

    def __str__(self):
        return self.token_hash


class CustomerTokenBinding(models.Model):
    token_key = models.ForeignKey(TokenKey, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=200, blank=False, null=False)
    market = models.ForeignKey(Market)
    active_flag = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_time = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.token_key.token_type.token_name

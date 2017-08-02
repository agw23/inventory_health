# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.utils.encoding import python_2_unicode_compatible

from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django import forms

# Create your models here.

@python_2_unicode_compatible
class IP(models.Model):
    IP_address = models.CharField(max_length=20,
                                  error_messages={'unique': 'Please enter a different IP address.'})

    IP_serial = models.CharField(max_length=200, default="00000")

    version = models.CharField(max_length=200, default="00000")

    uptime = models.CharField(max_length=100, default="00000")

    IP_address_auto = models.CharField(max_length=100, default="0000")

    model = models.CharField(max_length=100, default="00000")

    username = models.CharField(max_length=100, default="00000")

    password = models.CharField(max_length=100, default="00000")

    def __str__(self):
        return self.IP_address


@python_2_unicode_compatible
class Graph(models.Model):
    IP_address = models.CharField(max_length=200, default="0000")

    def __str__(self):
        return self.IP_address


@python_2_unicode_compatible
class Autodiscover(models.Model):
    subnet = models.CharField(max_length=200, default="0000")
    host = models.CharField(max_length=200, default="0000")
    port_status = models.CharField(max_length=200, default="0000")
    ports = models.CharField(max_length=200, default="0000")
    protocol = models.CharField(max_length=200, default="0000")


    def __str__(self):
        return self.host
# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 15:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0038_ip_password'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 16:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0027_singledevicemodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SingleDeviceModel',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 15:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0025_auto_20170707_1019'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SingleDeviceModel',
        ),
    ]

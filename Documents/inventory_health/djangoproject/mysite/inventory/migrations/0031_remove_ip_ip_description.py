# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 19:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0030_ip_ip_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ip',
            name='IP_description',
        ),
    ]

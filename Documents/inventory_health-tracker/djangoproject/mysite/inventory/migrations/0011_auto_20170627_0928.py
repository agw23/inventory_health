# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_ip_ip_serial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip',
            name='IP_address',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
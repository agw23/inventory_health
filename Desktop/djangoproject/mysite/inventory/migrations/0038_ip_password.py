# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-24 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0037_remove_ip_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip',
            name='password',
            field=models.CharField(default='00000', max_length=100),
        ),
    ]

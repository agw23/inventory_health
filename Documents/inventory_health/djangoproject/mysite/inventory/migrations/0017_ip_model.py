# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_ip_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip',
            name='model',
            field=models.CharField(default='00000', max_length=100),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-24 17:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0034_auto_20170724_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ip',
            name='user',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 14:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20170620_0926'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='IP_Info',
            new_name='IP',
        ),
    ]

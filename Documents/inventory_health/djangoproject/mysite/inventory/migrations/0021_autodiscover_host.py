# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_auto_20170629_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='autodiscover',
            name='host',
            field=models.CharField(default='0000', max_length=200),
        ),
    ]

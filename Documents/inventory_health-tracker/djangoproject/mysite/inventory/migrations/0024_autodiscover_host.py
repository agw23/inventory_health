# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_remove_autodiscover_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='autodiscover',
            name='host',
            field=models.CharField(default='0000', max_length=200),
        ),
    ]

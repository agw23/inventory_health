# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 17:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_autodiscover_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autodiscover',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.IP'),
        ),
    ]
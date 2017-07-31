# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_ip_uptime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Autodiscover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hosts', models.CharField(default='0000', max_length=200)),
                ('port_status', models.CharField(default='0000', max_length=200)),
                ('ports', models.CharField(default='0000', max_length=200)),
                ('protocol', models.CharField(default='0000', max_length=200)),
            ],
        ),
    ]
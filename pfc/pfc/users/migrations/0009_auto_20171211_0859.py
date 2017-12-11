# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-11 08:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_company_main_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='permissions',
            field=models.ManyToManyField(blank=True, related_name='users', to='applications.Permission'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-09 18:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0006_auto_20171209_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='users',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-11 19:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20171211_1905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrule',
            name='argument',
        ),
    ]

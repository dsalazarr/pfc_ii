# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-18 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20171118_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text=b"Account's holder password", max_length=256),
        ),
    ]
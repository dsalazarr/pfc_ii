# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-09 10:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0004_message_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='sent_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 9, 10, 49, 13, 170736)),
        ),
    ]
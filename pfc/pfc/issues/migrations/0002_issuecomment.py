# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-03 15:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name="Comment's primary key")),
                ('body', models.TextField(verbose_name="Comment's body")),
                ('issue_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='issues.Issue')),
            ],
        ),
    ]

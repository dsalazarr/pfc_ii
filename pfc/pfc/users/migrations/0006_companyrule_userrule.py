# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-03 15:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20171118_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyRule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('operator', models.CharField(max_length=255)),
                ('argument', models.CharField(blank=True, max_length=255)),
                ('companies', models.ManyToManyField(related_name='rules', to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='UserRule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('operator', models.CharField(max_length=255)),
                ('argument', models.CharField(blank=True, max_length=255)),
                ('users', models.ManyToManyField(related_name='rules', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

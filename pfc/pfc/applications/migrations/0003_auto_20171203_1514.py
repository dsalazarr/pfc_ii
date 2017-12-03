# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-03 15:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0002_auto_20171121_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserApplicationLicense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='companyapplicationlicense',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='users.Company'),
        ),
        migrations.AddField(
            model_name='userapplicationlicense',
            name='company_license',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applications.CompanyApplicationLicense'),
        ),
        migrations.AddField(
            model_name='userapplicationlicense',
            name='user',
            field=models.ForeignKey(on_delete=b'id', to=settings.AUTH_USER_MODEL, to_field='licenses'),
        ),
        migrations.AlterUniqueTogether(
            name='userapplicationlicense',
            unique_together=set([('user', 'company_license')]),
        ),
    ]
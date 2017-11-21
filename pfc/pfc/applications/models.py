from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from pfc.users.models import Company


class ApplicationConfig(models.Model):
    id = models.AutoField(primary_key=True)
    application = models.ForeignKey(settings.OAUTH2_PROVIDER_APPLICATION_MODEL)
    key = models.CharField(max_length=255, null=False)
    value = models.CharField(max_length=255, null=False)

    class Meta:
        unique_together = ('application', 'key')


class License(models.Model):
    LICENSE_TYPES = (
        ('DAY', 'DAY'),
        ('MONTH', 'MONTH'),
        ('YEAR', 'YEAR'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=15, choices=LICENSE_TYPES)
    max_users = models.IntegerField("Maximum number of users")
    duration_days = models.IntegerField("Duration days of the license")


class CompanyApplicationLicense(models.Model):
    company = models.ForeignKey(Company)
    license = models.ForeignKey(License)
    application = models.ForeignKey(settings.OAUTH2_PROVIDER_APPLICATION_MODEL)
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)

    class Meta:
        unique_together = (
            ('company', 'application', 'active')
        )

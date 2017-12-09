from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from oauth2_provider.models import Application

from pfc.users.models import Company, User


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

    def __str__(self):
        return self.name


class CompanyApplicationLicense(models.Model):
    company = models.ForeignKey(Company, related_name='licenses')
    license = models.ForeignKey(License)
    application = models.ForeignKey(settings.OAUTH2_PROVIDER_APPLICATION_MODEL)
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return "%s %s" % (self.application, self.license)


class UserApplicationLicense(models.Model):
    user = models.ForeignKey(User, related_name='licenses')
    company_license = models.ForeignKey(CompanyApplicationLicense)

    class Meta:
        unique_together = (
            ('user', 'company_license')
        )


class Permission(models.Model):
    application = models.ForeignKey(Application)

    id = models.AutoField(primary_key=True)
    codename = models.CharField(max_length=50)
    name = models.CharField(max_length=256)

    users = models.ManyToManyField(User)

    class Meta:
        unique_together = (
            ('application', 'codename')
        )

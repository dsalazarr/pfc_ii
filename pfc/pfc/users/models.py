"""
PFC main app models
"""
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException


class AccessDeniedApplication(APIException):
    status_code = 403
    default_detail = 'You or your company do not have access to this application'


class MaxUsersReached(APIException):
    status_code = 400
    default_detail = 'You reached the maximum number of users for this license'


class Company(models.Model):
    """
    Client company that has access to the owner's products
    """
    id = models.AutoField(_('Company\'s database id'), primary_key=True)
    name = models.CharField(_('Name of Company'), blank=False, max_length=255)
    slug = models.CharField(_('Company slug'), blank=True, unique=True, max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('companies:detail', kwargs={'slug': self.slug})

    def assign_license(self, license, application):
        try:
            company_license = self.licenses.get(active=1, application=application)
        except ObjectDoesNotExist:
            pass
        else:
            company_license.active = False
            company_license.end_date = datetime.utcnow()
            company_license.save()
        return self.licenses.create(
            license=license,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=license.duration_days),
            application=application,
        )


@python_2_unicode_compatible
class User(AbstractUser):
    """
    Company's user that has access to some of the owner's products
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.
    id = models.AutoField(_('User\'s database id'), primary_key=True)
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    email = models.EmailField(
        max_length=255,
        help_text='Account email',
    )
    password = models.CharField(
        max_length=256,
        help_text='Account\'s holder password',
    )
    company = models.ForeignKey(
        'Company',
        related_name='users',
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={
            'company': self.company.slug,
            'username': self.username
        })

    def has_access_to_application(self, application):
        try:
            self.user.licenses.get(
                company_license__active=1,
                company_license__application=application,
            )
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def give_access_to_application(self, application):
        try:
            company_license = self.company.licenses.get(active=1, application=application)
        except ObjectDoesNotExist:
            raise AccessDeniedApplication()
        if company_license.users.count() >= company_license.license.max_users:
            raise MaxUsersReached()
        return self.licenses.create(
            company_license=company_license,
        )


class UserRule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    operator = models.CharField(max_length=255, blank=False)
    argument = models.CharField(max_length=255, blank=True)

    users = models.ManyToManyField(User, related_name='rules')


class CompanyRule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    operator = models.CharField(max_length=255, blank=False)
    argument = models.CharField(max_length=255, blank=True)

    companies = models.ManyToManyField(Company, related_name='rules')


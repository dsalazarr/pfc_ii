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
    main_company = models.BooleanField(default=False)

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
    permissions = models.ManyToManyField(
        'applications.Permission',
        related_name='users',
        blank=True,
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
            self.licenses.get(
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
        if company_license.userapplicationlicense_set.count() >= company_license.license.max_users:
            raise MaxUsersReached()
        return self.licenses.create(
            company_license=company_license,
        )

    @property
    def is_from_main_company(self):
        return self.is_superuser

    def apply_rules(self, request):
        for user_rule in self.user_rules.all():
            if not user_rule.apply_rule(request):
                return False
        return True


class UserRule(models.Model):
    OPERATOR_CHOICES = [
        ('only_from_ip', 'Only from ip'),
        ('only_from_useragent', 'Only from useragent'),
        ('only_after_hour', 'Only after hour'),
        ('only_before_hour', 'Only before hour'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    operator = models.CharField(max_length=255, blank=False)

    users = models.ManyToManyField(
        User,
        through='UserRuleUser',
        related_name='rules'
    )

    def apply_rule(self, request, argument):
        return getattr(self, self.operator)(request, argument)

    def only_from_ip(self, request, ip):
        headers = getattr(request, 'META', None) or getattr(request, 'headers', {})
        x_forwarded_for = headers.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request_ip = x_forwarded_for.split(',')[0]
        else:
            return True
        return ip == request_ip

    def only_from_useragent(self, request, value):
        headers = getattr(request, 'META', None) or getattr(request, 'headers', {})
        user_agent = headers.get('HTTP_USER_AGENT')
        if user_agent:
            return user_agent.startswith(value) or user_agent == 'configuration'
        return False

    def only_after_hour(self, request, value):
        hour = datetime.utcnow().strftime("%H")
        return int(hour) >= int(value)

    def only_before_hour(self, request, value):
        hour = datetime.utcnow().strftime("%H")
        return int(hour) < int(value)

    def __str__(self):
        return self.name


class UserRuleUser(models.Model):
    user = models.ForeignKey(User, related_name='user_rules')
    rule = models.ForeignKey(UserRule)
    argument = models.CharField(max_length=255, blank=True)

    def apply_rule(self, request):
        return self.rule.apply_rule(request, self.argument)


class CompanyRule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    operator = models.CharField(max_length=255, blank=False)
    argument = models.CharField(max_length=255, blank=True)

    companies = models.ManyToManyField(Company, related_name='rules')


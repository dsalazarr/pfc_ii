"""
PFC main app models
"""

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    """
    Client company that has access to the owner's products
    """
    id = models.IntegerField(_('Company\'s database id'), primary_key=True)
    name = models.CharField(_('Name of Company'), blank=False, max_length=255)
    slug = models.CharField(_('Company slug'), blank=True, unique=True, max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('companies:detail', kwargs={'slug': self.slug})


@python_2_unicode_compatible
class User(AbstractUser):
    """
    Company's user that has access to some of the owner's products
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    email = models.EmailField(
        max_length=255,
        help_text='Account email',
    )
    password = models.CharField(
        max_length=56,
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

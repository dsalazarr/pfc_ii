from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class ApplicationConfig(models.Model):
    id = models.AutoField(primary_key=True)
    application = models.ForeignKey(settings.OAUTH2_PROVIDER_APPLICATION_MODEL)
    key = models.CharField(max_length=255, null=False)
    value = models.CharField(max_length=255, null=False)

    class Meta:
        unique_together = ('application', 'key')

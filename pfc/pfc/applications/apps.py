from __future__ import unicode_literals

from django.apps import AppConfig


class ApplicationsConfig(AppConfig):
    name = 'pfc.applications'
    verbose_name = 'Applications'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass

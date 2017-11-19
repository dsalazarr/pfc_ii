from __future__ import unicode_literals

from django.apps import AppConfig


class IssuesConfig(AppConfig):
    name = 'pfc.issues'
    verbose_name = 'Issues'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass

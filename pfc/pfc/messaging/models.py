from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from pfc.users.models import User


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(_('Message\'s subject'), blank=False, max_length=255)
    body = models.TextField(_("Message's body"), blank=False)

    author_id = models.ForeignKey(User, related_name='sent_messages')
    destination_id = models.ForeignKey(User, related_name='received_messages')

    def __str__(self):
        return self.subject

from __future__ import unicode_literals

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from pfc.users.models import User


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(_('Message\'s subject'), blank=False, max_length=255)
    body = RichTextField(_("Message's body"), blank=False)
    read = models.BooleanField(default=False)

    author = models.ForeignKey(User, related_name='sent_messages')
    destination = models.ForeignKey(User, related_name='received_messages')

    def __str__(self):
        return self.subject

    def get_admin_url(self):
        return "/admin/messaging/message/{}/change/".format(self.id)

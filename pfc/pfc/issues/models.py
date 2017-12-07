from __future__ import unicode_literals

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from pfc.users.models import User


class Issue(models.Model):
    ISSUE_OPEN = "open"
    ISSUE_CLOSED = "closed"
    ISSUE_IN_PROGRESS = "in_progress"
    ISSUE_TO_VERIFY = "to_verify"
    ISSUE_STATUSES = (
        (ISSUE_OPEN, "Open"),
        (ISSUE_CLOSED, "Closed")
    )

    id = models.AutoField(_("Issue's database id"), primary_key=True)
    ref = models.CharField(_("Issue's reference"), max_length=255, null=True)
    status = models.CharField(
        _("Issue's status"),
        max_length=20,
        null=False,
        default="open",
        choices=ISSUE_STATUSES
    )
    title = models.CharField(_("Issue's title"), max_length=255, null=False)
    description = RichTextField(_("Issue's description"), null=False)
    solution = models.TextField(_("Issue's solution"), null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, related_name='created_issues')
    assigned_to = models.ForeignKey(User, null=True, related_name='assigned_issues')
    closed_by = models.ForeignKey(User, null=True, related_name='closed_issues')


class IssueComment(models.Model):
    id = models.AutoField(_("Comment's primary key"), primary_key=True)
    body = RichTextField(_("Comment's body"), blank=False)

    issue_id = models.ForeignKey(Issue, related_name='comments')


from jet.dashboard.modules import DashboardModule

from pfc.issues.models import Issue


class MessageInbox(DashboardModule):
    title = 'Recent messages'
    limit = 10
    template = 'dashboard/inbox.html'

    def init_with_context(self, context):
        self.children = context['user'].received_messages.filter(read=False)


class IssueInbox(DashboardModule):
    title = 'Open issues'
    limit = 10
    template = 'dashboard/open_issues.html'

    def init_with_context(self, context):
        if context['user'].is_from_main_company:
            self.children = Issue.objects.filter(status=Issue.ISSUE_OPEN)
        else:
            self.children = context['user'].created_issues.filter(status=Issue.ISSUE_OPEN)


class AssignedIssueInbox(DashboardModule):
    title = 'Assigned issues'
    limit = 10
    template = 'dashboard/open_issues.html'

    def init_with_context(self, context):
        self.children = context['user'].assigned_issues.filter(status=Issue.ISSUE_OPEN)

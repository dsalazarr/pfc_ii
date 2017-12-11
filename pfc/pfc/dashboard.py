from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard

from django.utils.translation import ugettext as _

from pfc import dashboard_modules


class CustomDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.available_children.append(dashboard_modules.MessageInbox)
        self.children.append(dashboard_modules.IssueInbox())
        self.children.append(dashboard_modules.AssignedIssueInbox())

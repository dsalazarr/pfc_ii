
from jet.dashboard.modules import DashboardModule
from pfc.messaging.models import Message


class MessageInbox(DashboardModule):
    title = 'Recent messages'
    limit = 10
    template = 'dashboard/inbox.html'

    def init_with_context(self, context):
        self.children = context['user'].received_messages.filter(read=False)

from django.contrib.admin.forms import AdminAuthenticationForm
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard

from django.contrib import admin
from django import forms

from pfc import dashboard_modules


class CustomDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.available_children.append(dashboard_modules.MessageInbox)
        self.children.append(dashboard_modules.IssueInbox())
        self.children.append(dashboard_modules.AssignedIssueInbox())


class MyLoginForm(AdminAuthenticationForm):
    error_message = AdminAuthenticationForm.error_messages.update({
        'rules_error': 'Forbidden access by rules'
    })

    def clean(self):
        data = super(MyLoginForm, self).clean()
        if not self.user_cache.apply_rules(self.request):
            raise forms.ValidationError(
                self.error_messages['rules_error'],
                code='rules_error',
                params={'username': self.username_field.verbose_name},
            )
        return data

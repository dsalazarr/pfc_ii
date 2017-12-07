import logging
from django import forms
from django.contrib import admin

# Register your models here.
from pfc.issues.models import Issue


logger = logging.getLogger('issue')


class IssueCreationForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = (
            'title',
            'status',
            'assigned_to',
            'ref',
            'description',
        )


@admin.register(Issue)
class MyIssueForm(admin.ModelAdmin):
    change_form = IssueCreationForm
    fields = ('title', 'ref', 'description')
    list_display = ('title', 'status', 'author', 'assigned_to', 'created_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        return super(MyIssueForm, self).save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is not None:
            print('Creating')
            defaults['form'] = self.change_form
        defaults.update(**kwargs)
        return super(MyIssueForm, self).get_form(request, obj, **defaults)

    def get_fields(self, request, obj=None):
        if obj is not None:
            return self.change_form.Meta.fields
        return super(MyIssueForm, self).get_fields(request, obj)

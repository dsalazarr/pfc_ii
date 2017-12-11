import logging
from django import forms
from django.contrib import admin

# Register your models here.
from oauth2_provider.models import Application

from pfc.issues.models import Issue, IssueComment


logger = logging.getLogger('issue')


class IssueCreationForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = (
            'title',
            'status',
            'assigned_to',
            'application',
            'ref',
            'description',
        )


class CommentInline(admin.TabularInline):
    model = IssueComment
    fields = ('body',)
    extra = 1


@admin.register(Issue)
class MyIssueForm(admin.ModelAdmin):
    change_form = IssueCreationForm
    fields = ('title', 'ref', 'description',)
    list_display = ('title', 'status', 'author', 'assigned_to', 'created_at')
    inlines = [CommentInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "application":
            kwargs['queryset'] = Application.objects.filter(
                companyapplicationlicense__userapplicationlicense__user=request.user,
                companyapplicationlicense__active=True,
            )
        return super(MyIssueForm, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        return super(MyIssueForm, self).save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is not None:
            defaults['form'] = self.change_form
        defaults.update(**kwargs)
        return super(MyIssueForm, self).get_form(request, obj, **defaults)

    def get_readonly_fields(self, request, obj=None):
        fields = super(MyIssueForm, self).get_readonly_fields(request, obj)
        if obj is not None:
            if not request.user.is_from_main_company:
                return fields + ('assigned_to',)
        return fields

    def get_fields(self, request, obj=None):
        if obj is not None:
            return self.change_form.Meta.fields
        return super(MyIssueForm, self).get_fields(request, obj)

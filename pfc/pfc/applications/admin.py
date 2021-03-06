from allauth.account.models import EmailAddress
from allauth.socialaccount.admin import SocialTokenAdmin
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from django import forms
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from oauth2_provider.admin import ApplicationAdmin, AccessTokenAdmin
from oauth2_provider.models import (
    Application as ApplicationModel,
    AccessToken as AccessTokenModel,
    Grant,
    RefreshToken,
)

from pfc.applications.models import License, CompanyApplicationLicense, UserApplicationLicense, \
    ApplicationConfig, Permission, Application, AccessToken


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'type',
        'max_users',
        'duration_days',
    )
    list_display = (
        'name',
        'type',
        'max_users',
        'duration_days',
    )


class CompanyApplicationLicenseForm(forms.ModelForm):
    class Meta:
        model = CompanyApplicationLicense
        fields = tuple()

    def save(self, commit=True):
        self.instance = self.instance.company.assign_license(
            self.instance.license,
            self.instance.application
        )
        return self.instance


class CompanyLicenseInline(admin.StackedInline):
    model = CompanyApplicationLicense
    extra = 1
    show_change_link = False
    fields = ('application', 'license', 'active')
    readonly_fields = ('active',)
    form = CompanyApplicationLicenseForm
    ordering = ('-active', 'application')


class UserApplicationLicenseForm(forms.ModelForm):
    company_license = forms.ModelChoiceField(
        queryset=CompanyApplicationLicense.objects.none(),
    )

    class Meta:
        model = UserApplicationLicense
        fields = tuple()

    def save(self, commit=True):
        self.instance = self.instance.user.give_access_to_application(
            self.instance.company_license.application
        )
        return self.instance


class UserApplicationInline(admin.TabularInline):
    model = UserApplicationLicense
    extra = 1
    form = UserApplicationLicenseForm
    show_change_link = False
    fields = ('company_license',)

    def __init__(self, parent_model, admin_site):
        super(UserApplicationInline, self).__init__(parent_model, admin_site)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(UserApplicationInline, self).get_formset(request, obj, **kwargs)
        if obj:
            formset.form.declared_fields['company_license'].queryset = (
                CompanyApplicationLicense.objects.annotate(
                    num_users=Count('userapplicationlicense')
                ).filter(
                    active=True,
                    company=obj.company
                ).exclude(
                    ~Q(userapplicationlicense__user=obj),
                    license__max_users__lte=F('num_users'),
                )
            )

        return formset


admin.site.unregister(ApplicationModel)
admin.site.unregister(AccessTokenModel)
admin.site.unregister(Grant)
admin.site.unregister(RefreshToken)
admin.site.unregister(Site)
admin.site.unregister(EmailAddress)
admin.site.unregister(Group)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)


class ApplicationConfigInline(admin.StackedInline):
    model = ApplicationConfig
    verbose_name = "Application configuration value"
    verbose_name_plural = "Application configuration set"
    extra = 1


class ApplicationPermissionsInline(admin.StackedInline):
    model = Permission
    verbose_name = "Application permission"
    verbose_name_plural = "Application permissions"
    extra = 1
    fields = ('codename', 'name')


@admin.register(Application)
class CustomApplicationAdmin(ApplicationAdmin):
    inlines = [ApplicationConfigInline, ApplicationPermissionsInline]


admin.site.register(AccessToken, AccessTokenAdmin)

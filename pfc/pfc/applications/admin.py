
from django import forms
from django.contrib import admin

# Register your models here.
from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.db.models.query_utils import Q

from pfc.applications.models import License, CompanyApplicationLicense, UserApplicationLicense


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

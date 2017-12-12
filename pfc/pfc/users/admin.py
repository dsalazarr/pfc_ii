from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from slugify import slugify

from pfc.applications.admin import CompanyLicenseInline, UserApplicationInline
from pfc.applications.models import Permission
from pfc.users.models import UserRule, CompanyRule, Company
from .models import User


class UserRuleInline(admin.TabularInline):
    model = User.rules.through
    extra = 1


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'company')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_company(self):
        return self.cleaned_data['company']


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
            ('User Profile', {'fields': ('name',)}),
            ('Application Permissions', {'fields': ('permissions',)}),
    ) + AuthUserAdmin.fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'company', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'name',)
    search_fields = ['name']
    inlines = [UserApplicationInline, UserRuleInline]

    def get_readonly_fields(self, request, obj=None):
        fields = super(MyUserAdmin, self).get_readonly_fields(request, obj)
        if not request.user.is_from_main_company:
            return fields + ('company',)
        return fields

    def get_queryset(self, request):
        queryset = super(MyUserAdmin, self).get_queryset(request)
        return queryset.filter(company=request.user.company)

    def save_model(self, request, obj, form, change):
        if not change:
            if not request.user.is_from_main_company:
                obj.company = request.user.company
            obj.is_staff = True
        return super(MyUserAdmin, self).save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "permissions":
            kwargs["queryset"] = Permission.objects.filter(
                application__companyapplicationlicense__userapplicationlicense__user=request.user,
                application__companyapplicationlicense__active=True,
            )
        return super(MyUserAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company":
            if request.user.is_from_main_company:
                kwargs["required"] = True
        return super(MyUserAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            fieldsets = self.add_fieldsets
            fields = ('username', 'password1', 'password2')
            if request.user.is_from_main_company:
                fieldsets[0][1]['fields'] = fields + ('company',)
            else:
                fieldsets[0][1]['fields'] = fields
        return super(MyUserAdmin, self).get_fieldsets(request, obj)


class UserRuleCreationForm(forms.ModelForm):
    operator = forms.CharField(
        label=_("Operator"),
        widget=forms.Select(choices=UserRule.OPERATOR_CHOICES)
    )

    class Meta:
        model = UserRule
        fields = ('name', 'operator')


@admin.register(UserRule)
class MyUserRule(admin.ModelAdmin):
    form = UserRuleCreationForm
    add_form = UserRuleCreationForm
    list_display = ('name', 'operator')
    search_fields = ('name',)


class CompanyRuleCreationForm(forms.ModelForm):
    operator = forms.CharField(
        label=_("Operator"),
        widget=forms.Select(choices=UserRule.OPERATOR_CHOICES)
    )

    class Meta:
        model = CompanyRule
        fields = ('name', 'operator', 'argument')


@admin.register(CompanyRule)
class MyCompanyRule(admin.ModelAdmin):
    form = CompanyRuleCreationForm
    add_form = CompanyRuleCreationForm
    list_display = ('name', 'operator', 'argument')
    search_fields = ('name',)


class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)

    def save(self, commit=True):
        return super(CompanyCreationForm, self).save(commit=commit)


@admin.register(Company)
class MyCompanyForm(admin.ModelAdmin):

    form = CompanyCreationForm
    add_form = CompanyCreationForm
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    inlines = (CompanyLicenseInline,)

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.name).lower()
        return super(MyCompanyForm, self).save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        return super(MyCompanyForm, self).save_related(request, form, formsets, change)

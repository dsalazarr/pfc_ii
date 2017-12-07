from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from slugify import slugify

from pfc.applications.admin import CompanyLicenseInline, UserApplicationInline
from pfc.users.models import UserRule, CompanyRule, Company
from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
            ('User Profile', {'fields': ('name',)}),
    ) + AuthUserAdmin.fieldsets
    list_display = ('username', 'name', 'is_superuser')
    search_fields = ['name']
    inlines = [UserApplicationInline]


class UserRuleCreationForm(forms.ModelForm):
    operator = forms.CharField(
        label=_("Operator"),
        widget=forms.Select(choices=UserRule.OPERATOR_CHOICES)
    )

    class Meta:
        model = UserRule
        fields = ('name', 'operator', 'argument')


@admin.register(UserRule)
class MyUserRule(admin.ModelAdmin):
    form = UserRuleCreationForm
    add_form = UserRuleCreationForm
    list_display = ('name', 'operator', 'argument')
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

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        import ipdb; ipdb.set_trace()
        return super(MyCompanyForm, self).formfield_for_choice_field(db_field, request, **kwargs)

    def save_related(self, request, form, formsets, change):
        return super(MyCompanyForm, self).save_related(request, form, formsets, change)

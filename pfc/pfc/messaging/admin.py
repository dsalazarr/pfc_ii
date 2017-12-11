from datetime import datetime

from django.contrib import admin
from django.db.models.query_utils import Q

from pfc.messaging.models import Message


@admin.register(Message)
class MyMessageForm(admin.ModelAdmin):
    list_display = ('subject', 'author', 'destination')
    fields = ('subject', 'body', 'destination')
    search_fields = ('subject',)

    def get_queryset(self, request):
        queryset = super(MyMessageForm, self).get_queryset(request)
        return queryset.filter(
            Q(author=request.user) | Q(destination=request.user)
        )

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.id and obj.destination == request.user and not obj.read:
            obj.read = True
            obj.read_at = datetime.utcnow()
            obj.save(update_fields=['read', 'read_at'])
        return super(MyMessageForm, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(MyMessageForm, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "destination":
            kwargs['queryset'] = request.user.company.users.all()
        return super(MyMessageForm, self).formfield_for_foreignkey(db_field, request, **kwargs)


class InboxAdmin(admin.ModelAdmin):
    list_display = ('subject', 'author',)

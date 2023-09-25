from django.contrib import admin
from mailing.models import Client, Message, Mailing, MailingLogs, Category


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'comment', 'is_active', 'creator')
    list_filter = ('is_active',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'message', 'creator', 'category')
    list_filter = ('topic',)
    ordering = ('id',)


@admin.register(Mailing)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('create_date', 'sending_time', 'frequency', 'status',
                    'message', 'finish_date', 'finish_time')


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    list_display = ('last_try', 'status', 'mail_settings', 'client',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


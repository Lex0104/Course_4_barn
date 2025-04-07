from django.contrib import admin

from mailings.models import Mailing, MailingAttempts, MailingRecipient, Message


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "full_name",
    )
    list_filter = ("email",)
    search_field = (
        "comment",
        "email",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
    )
    search_field = ("subject", "message")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "message",
    )
    list_filter = ("date_of_first_sending",)
    search_field = ("status", "message", "recipients")


@admin.register(MailingAttempts)
class MailingAttemptsAdmin(admin.ModelAdmin):
    list_display = ("mailing", "status", "date_first_attempt")
    list_filter = ("date_first_attempt",)
from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import (HomeView, MailingAttemptsListView, MailingCreateView, MailingDeleteView, MailingDetailView,
                            MailingRecipientCreateView, MailingRecipientDeleteView, MailingRecipientDetailView,
                            MailingRecipientsListView, MailingRecipientUpdateView, MailingsListView, MailingUpdateView,
                            MessageCreateView, MessageDeleteView, MessageDetailView, MessageListView,
                            MessageUpdateView, SendMailingView)

app_name = MailingsConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("mailing_recipient/", MailingRecipientsListView.as_view(), name="mailing_recipients_list"),
    path("mailing_recipient/create/", MailingRecipientCreateView.as_view(), name="mailing_recipient_create"),
    path("mailing_recipient/<int:pk>/", MailingRecipientDetailView.as_view(), name="mailing_recipient_detail"),
    path(
        "mailing_recipient/<int:pk>/update/",
        MailingRecipientUpdateView.as_view(),
        name="mailing_recipient_detail_update",
    ),
    path(
        "mailing_recipient/<int:pk>/delete/",
        MailingRecipientDeleteView.as_view(),
        name="mailing_recipient_detail_delete",
    ),
    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("mailing/", MailingsListView.as_view(), name="mailings_list"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/<int:pk>/delete", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailing/<int:pk>/attempts/", MailingAttemptsListView.as_view(), name="mailing_attempts_list"),
    path("mailing/<int:pk>/send/", SendMailingView.as_view(), name="send_mailing"),
]
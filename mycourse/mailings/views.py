import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from mailings.forms import MailingForm, MailingRecipientForm, ManagerMailingForm, MessageForm
from mailings.models import Mailing, MailingAttempts, MailingRecipient, Message
from mailings.services import send_mailing

logger = logging.getLogger(__name__)


class HomeView(View):
    template_name = "mailings/home.html"

    def get(self, request):
        mailings = Mailing.objects.count()
        mailings_active = Mailing.objects.filter(status=Mailing.LAUNCHED).count()
        unique_recipients = MailingRecipient.objects.count()
        context = {
            "total_mailings": mailings,
            "unique_recipients": unique_recipients,
            "mailings_active": mailings_active,
        }

        return render(request, self.template_name, context)


class MailingRecipientsListView(LoginRequiredMixin, ListView):
    model = MailingRecipient

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Managers").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingRecipientCreateView(LoginRequiredMixin, CreateView):
    template_name = "mailings/mailing_recipient_form.html"
    form_class = MailingRecipientForm
    success_url = reverse_lazy("mailings:mailing_recipients_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        try:
            return super().form_valid(form)
        except Exception as ex:
            logger.error(f"Ошибка при создании клиента: {str(ex)}")


@method_decorator(cache_page(60 * 5), name="dispatch")
class MailingRecipientDetailView(LoginRequiredMixin, DetailView):
    model = MailingRecipient

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Managers").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingRecipientUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "mailings/mailing_recipient_form.html"
    model = MailingRecipient
    form_class = MailingRecipientForm
    success_url = reverse_lazy("mailings:mailing_recipients_list")

    def get_success_url(self):
        return reverse("mailings:mailing_recipient_detail", args=[self.kwargs.get("pk")])

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class MailingRecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    template_name = "mailings/confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_recipients_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Managers").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    template_name = "mailings/message_form.html"
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        try:
            return super().form_valid(form)
        except Exception as ex:
            logger.error(f"Ошибка при создании сообщения: {str(ex)}")


@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Managers").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "mailings/message_form.html"
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")

    def get_success_url(self):
        return reverse("mailings:message_detail", args=[self.kwargs.get("pk")])

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "mailings/confirm_delete.html"
    model = Message
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class MailingsListView(LoginRequiredMixin, ListView):
    model = Mailing
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Managers").exists():
            return queryset
        return queryset.filter(owner=self.request.user, mailing_is_working=True)


class MailingCreateView(LoginRequiredMixin, CreateView):
    template_name = "mailings/mailing_form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailings_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        try:
            return super().form_valid(form)
        except Exception as ex:
            logger.error(f"Ошибка при создании рассылки: {str(ex)}")

    def get_form(self, form_class=MailingForm):
        form = super().get_form()
        form.fields["recipients"].queryset = form.fields["recipients"].queryset.filter(owner=self.request.user)
        form.fields["message"].queryset = form.fields["message"].queryset.filter(owner=self.request.user)
        return form


@method_decorator(cache_page(60), name="dispatch")
class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attempts"] = self.object.mailing_attempts.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Managers").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    template_name = "mailings/mailing_form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailings_list")

    def get_success_url(self):
        return reverse("mailings:mailing_detail", args=[self.kwargs.get("pk")])

    def get_form(self, form_class=MailingForm):
        form = super().get_form()
        is_own_instance = self.request.user == self.get_object().owner
        if is_own_instance:
            form.fields["recipients"].queryset = form.fields["recipients"].queryset.filter(owner=self.request.user)
            form.fields["message"].queryset = form.fields["message"].queryset.filter(owner=self.request.user)
        elif self.request.user.groups.filter(name="Managers").exists():
            pass
        return form

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Managers").exists():
            return queryset
        return queryset.filter(owner=self.request.user)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if user.groups.filter(name="Managers").exists():
            return ManagerMailingForm
        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/confirm_delete.html"
    success_url = reverse_lazy("mailings:mailings_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class MailingAttemptsListView(LoginRequiredMixin, ListView):
    model = MailingAttempts

    def get_queryset(self):
        mailing_id = self.kwargs["pk"]
        return MailingAttempts.objects.filter(mailing_id=mailing_id).order_by("-date_first_attempt")


class SendMailingView(View):

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        try:
            send_mailing(mailing)
        except Exception as ex:
            logger.error(f"Ошибка при отправке рассылки: {str(ex)} от пользователя {request.user}")
        return redirect("/")
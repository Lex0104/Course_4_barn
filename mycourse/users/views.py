import logging
import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from config import settings
from mailings.models import MailingAttempts
from users.forms import ManagerForm, UserForm, UserRegisterForm
from users.models import User


logger = logging.getLogger(__name__)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return render ( request, 'users/register.html' )


class UserCreateView(CreateView):
    model = User
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("mailings:home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/email-confirm/{token}/"
        try:
            send_mail(
                "Подтверждение почты",
                f"Добро пожаловать на сервис для рассылок! Для подтверждения регистрации перейдите по ссылке: {url}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            return super().form_valid(form)
        except Exception as ex:
            logging.error(f"Ошибка отправки подтверждения почты {str(ex)}")


class PasswordResetUserView(PasswordResetView):
    template_name = "reset_password.html"
    email_template_name = "password_reset_email.html"
    subject_template_name = "password_reset_subject.txt"
    from_email = settings.DEFAULT_FROM_EMAIL
    success_url = reverse_lazy("users:password_reset_done")


@method_decorator(cache_page(60 * 5), name="dispatch")
class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = "user_detail.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        successful_attempts = MailingAttempts.objects.filter(mailing__owner=user, status="Успешно").count()

        unsuccessful_attempts = MailingAttempts.objects.filter(mailing__owner=user, status="Не успешно").count()

        context["successful_attempts"] = successful_attempts
        context["unsuccessful_attempts"] = unsuccessful_attempts
        return context

    def get_object(self, queryset=None):
        if self.request.user.pk == self.kwargs.get("pk"):
            return get_object_or_404(User, pk=self.kwargs.get("pk"))
        else:
            raise PermissionDenied


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "user_form.html"
    model = User
    form_class = UserForm
    success_url = reverse_lazy("mailings:home")

    def get_success_url(self):
        return reverse("users:user_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        if user == self.object:
            return UserForm
        if user.groups.filter(name="Managers").exists():
            return ManagerForm
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["is_self"] = user == self.object
        context["is_manager"] = user.groups.filter(name="Managers").exists()
        return context


@method_decorator(cache_page(60 * 5), name="dispatch")
class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "user_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Managers").exists():
            return queryset
        raise PermissionDenied
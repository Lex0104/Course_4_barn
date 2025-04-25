from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetCompleteView, PasswordResetConfirmView,
                                       PasswordResetDoneView)
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from .views import (PasswordResetUserView, UserCreateView, UserDetailView, UsersListView, UserUpdateView,
                         email_verification)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),
    path("logout/", LogoutView.as_view(next_page="mailings:home"), name="logout"),
    path("reset_password/", PasswordResetUserView.as_view(template_name="users/reset_password.html"), name="reset_password"),
    path(
        "reset_password/done/",
        PasswordResetDoneView.as_view(template_name="users/reset_password_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html", success_url=reverse_lazy("users:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("user/", UsersListView.as_view(), name="users_list"),
]
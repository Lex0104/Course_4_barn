from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    avatar = models.ImageField(upload_to="users/images", verbose_name="Аватар", blank=True, null=True)
    phone_number = PhoneNumberField(verbose_name="Номер телефона", blank=True, null=True)
    country = models.CharField(max_length=60, verbose_name="Страна", blank=True, null=True)
    count_sent_messages = models.IntegerField(
        default=0, blank=True, null=True, verbose_name="Количество отправленных сообщений"
    )

    token = models.CharField(max_length=100, verbose_name="Токен", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [("can_view_all_users", "Can view all users"), ("can_block_users", "Can block users")]
from django.db import models

from users.models import User


class MailingRecipient(models.Model):
    email = models.CharField(max_length=100, unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Владелец", related_name="mailing_recipient", null=True
    )

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["email"]
        permissions = [("can_view_all_mailing_recipients", "Can view all mailing recipients")]


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name="Тема письма")
    message = models.TextField(verbose_name="Текст сообщения")
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Владелец", related_name="message", null=True
    )

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]
        permissions = [("can_view_all_messages", "Can view all mailing messages")]


class Mailing(models.Model):
    CREATED = "Создана"
    LAUNCHED = "Запущена"
    COMPLETED = "Завершена"
    STATUS_MAILING = [
        (CREATED, "Создана"),
        (LAUNCHED, "Запущена"),
        (COMPLETED, "Завершена"),
    ]

    date_of_first_sending = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время первой отправки")
    date_of_sending_end = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=10, choices=STATUS_MAILING, default=CREATED, verbose_name="Статус рассылки")
    message = models.ForeignKey(
        "Message", on_delete=models.SET_NULL, related_name="mailing", null=True, blank=True, verbose_name="Сообщение"
    )
    recipients = models.ManyToManyField("MailingRecipient", related_name="mailing", verbose_name="Получатели")
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Владелец", related_name="mailing", null=True
    )
    mailing_is_working = models.BooleanField(blank=True, null=True, default=True, verbose_name="Рассылка работает")

    def __str__(self):
        return f"{self.message}: {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status"]
        permissions = [
            ("can_view_all_mailings", "Can view all mailings"),
            ("can_disabling_mailings", "Can disabling mailings"),
        ]


class MailingAttempts(models.Model):
    successfully = "Успешно"
    not_successfully = "Не успешно"
    STATUS_ATTEMPT = [
        (successfully, "Успешно"),
        (not_successfully, "Не успешно"),
    ]

    date_first_attempt = models.DateTimeField(auto_now=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=20, choices=STATUS_ATTEMPT, verbose_name="Статус попытки рассылки")
    mail_server_response = models.TextField(null=True, blank=True, verbose_name="Ответ почтового сервиса")
    mailing = models.ForeignKey(
        "Mailing", on_delete=models.CASCADE, related_name="mailing_attempts", verbose_name="Рассылка"
    )

    def __str__(self):
        return f"{self.status}: {self.mail_server_response}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["status"]
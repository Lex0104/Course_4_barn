import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.utils import timezone

from mailings.models import MailingAttempts, MailingAttempts
from users.models import User


def send_mailing(mailing):
    mailing.status = MailingAttempts.LAUNCHED
    if mailing.date_of_first_sending is None:
        mailing.date_of_first_sending = timezone.now()
        mailing.save()

    attempt = MailingAttempts.objects.create(status=MailingAttempts.not_successfully, mailing=mailing)

    try:
        message = mailing.message
        subject = message.subject
        body = message.message

        recipients_count = mailing.recipients.count()

        for recipient in mailing.recipients.all():
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [recipient.email],
                fail_silently=False,
            )

        User.objects.filter(pk=mailing.owner.pk).update(
            count_sent_messages=F("count_sent_messages") + recipients_count
        )

        attempt.status = MailingAttempts.successfully
        mailing.status = MailingAttempts.COMPLETED

    except smtplib.SMTPException as e:
        attempt.mail_server_response = f"Ошибка SMTP: {str(e)}"

    except Exception as e:
        attempt.mail_server_response = f"Системная ошибка: {str(e)}"

    finally:
        attempt.save()
        mailing.date_of_sending_end = timezone.now()
        mailing.save()
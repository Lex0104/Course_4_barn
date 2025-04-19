from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from mailings.models import Mailing


class Command(BaseCommand):
    help = "Отправка рассылки"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки")

    def handle(self, *args, **kwargs):
        mailing_id = kwargs["mailing_id"]

        try:
            mailing = Mailing.objects.get(id=mailing_id)

            mailing.status = Mailing.LAUNCHED
            mailing.date_of_first_sending = timezone.now()
            mailing.save()

            recipients = mailing.recipients.all()
            message = mailing.message

            subject = message.subject
            body = message.message

            for recipient in recipients:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient.email],
                    fail_silently=False,
                )

            mailing.date_of_sending_end = timezone.now()
            mailing.status = Mailing.COMPLETED
            mailing.save()

            self.stdout.write(self.style.SUCCESS(f"Рассылка успешно отправлена на {recipients.count()} email(ов)."))

        except Mailing.DoesNotExist:
            self.stderr.write(self.style.ERROR("Рассылка не найдена."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ошибка: {str(e)}"))
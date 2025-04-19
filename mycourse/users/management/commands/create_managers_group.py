from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        group_name = "Managers"
        can_view_all_users = Permission.objects.get(codename="can_view_all_users")
        can_view_all_mailings = Permission.objects.get(codename="can_view_all_mailings")
        can_disabling_mailings = Permission.objects.get(codename="can_disabling_mailings")
        can_view_all_messages = Permission.objects.get(codename="can_view_all_messages")
        can_view_all_mailing_recipients = Permission.objects.get(codename="can_view_all_mailing_recipients")
        can_block_users = Permission.objects.get(codename="can_block_users")

        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана.'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа "{group_name}" уже существует.'))

        group.permissions.add(
            can_view_all_users,
            can_block_users,
            can_view_all_mailings,
            can_disabling_mailings,
            can_view_all_messages,
            can_view_all_mailing_recipients,
        )

        group.save()
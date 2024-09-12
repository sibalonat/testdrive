from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Delete all entries in the users table'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all users'))
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.contrib.auth.models import User
from decouple import config

SUPER_USERNAME = config("SUPER_USERNAME", cast=str)
SUPER_EMAIL = config("SUPER_EMAIL", cast=str)
SUPER_PASSWORD = config("SUPER_PASSWORD", cast=str)


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            superuser = User.objects.create_superuser(
                username=SUPER_USERNAME,
                email=SUPER_EMAIL,
                password=SUPER_PASSWORD)
            superuser.save()
        except IntegrityError:
            print(f"Super User with username {SUPER_USERNAME} already exit!")
        except Exception as e:
            print(e)



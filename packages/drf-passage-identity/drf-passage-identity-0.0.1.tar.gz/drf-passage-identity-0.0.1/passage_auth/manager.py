from django.contrib.auth.base_user import BaseUserManager
from django.core.management.base import CommandError
from django.conf import settings

from passageidentity.errors import PassageError
from passageidentity import Passage

PASSAGE_APP_ID = settings.PASSAGE_APP_ID
PASSAGE_API_KEY = settings.PASSAGE_API_KEY
PASSAGE_AUTH_STRATEGY = settings.PASSAGE_AUTH_STRATEGY
psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY, auth_strategy=PASSAGE_AUTH_STRATEGY)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, id, password=None, email=None, **extra_fields):
        if not id:
            raise ValueError("Passage ID is required")

        user = self.model(id=id, email=email, **extra_fields)

        if extra_fields.get('is_superuser'):
            user.set_password(password)

        user.save()
        return user

    def create_superuser(self, id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        try:
            psg.getUser(id)
        except PassageError as e:
            raise CommandError(f"Invalid Passage ID: {e}")

        return self.create_user(id, password, **extra_fields)

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .manager import UserManager

class PassageUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(("Passage User Id"), max_length=255, primary_key=True)
    email = models.EmailField(null=True)


    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []
    objects = UserManager()

    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def email_validator(email):
    try:
        validate_email(email)
    except ValidationError:
        raise ValueError(_('You must provide a valid email address'))


class CustomUserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, password=None):
        if not first_name:
            raise ValueError(_("Users must provide a first name"))
        if not last_name:
            raise ValueError(_("Users must provide a last name"))

        if email:
            email = self.normalize_email(email)
            email_validator(email)
        else:
            raise ValueError(_("An email address is required"))

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, first_name, last_name, email, password):

        user = self.create_user(first_name, last_name, email, password)

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user

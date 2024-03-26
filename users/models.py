from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(_("Email Address"), max_length=254, unique=True)
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> email:
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    username = models.CharField(_("Username"), max_length=50, null=True, blank=True)
    email = models.EmailField(_("Email"), max_length=254, null=True, blank=True)
    profile_picture = models.ImageField(
        _("Profile Picture"),
        upload_to="Profile_Pics",
        blank=True,
        null=True,
    )
    designation = models.CharField(
        _("Designation"),
        max_length=50,
        null=True,
        blank=True,
        help_text="e.g: Software Engineer",
    )
    bio = models.TextField(_("Bio"), blank=True)
    website = models.URLField(_("Website"), blank=True)
    github_link = models.URLField(
        _("Github Link"), max_length=200, null=True, blank=True
    )
    facebook_link = models.URLField(
        _("Facebook Link"), max_length=200, null=True, blank=True
    )
    linkedin_link = models.URLField(
        _("Linkedin Link"), max_length=200, null=True, blank=True
    )
    tweeter_link = models.URLField(
        _("Tweeter Link"), max_length=200, null=True, blank=True
    )
    phone = models.CharField(_("Phone Number"), max_length=16, blank=True)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self) -> email:
        return self.user.email

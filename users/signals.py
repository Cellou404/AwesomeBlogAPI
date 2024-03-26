from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    print("Profile Signal Trigged")
    """_summary_
        Create a Profile  when a User is Created.
    """
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.last_name,
            username=user.email.split("@")[0],
        )


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    """_summary_
        Deletes the associated User when a profile is deleted.
    Parameters
    ----------
    sender : TYPE
        DESCRIPTION.
    instance : TYPE
        The instance of the model being deleted.
    """ """
    # Delete the associated User object as well
    """
    user = instance.user
    user.delete()


# post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
# post_delete.connect(delete_user, sender=Profile)

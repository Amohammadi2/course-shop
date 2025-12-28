from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from wallet.models import Wallet

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    """
    Signal handler to create a Wallet instance for each new User.
    This function is triggered whenever a User object is saved. If the user
    was just created (as indicated by the `created` flag), a new Wallet is
    created and associated with that user.
    """
    if created:
        Wallet.objects.create(user=instance)

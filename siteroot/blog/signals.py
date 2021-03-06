from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=get_user_model())
def create_user_profile(instance, created, **kwargs):
    ''' For every new registered user (created User) create a Profile '''
    if created:
        Profile.objects.create(user=instance).save()

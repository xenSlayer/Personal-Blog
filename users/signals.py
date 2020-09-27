from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Friend


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Friend.objects.create(current_user=instance)
        name = str(instance.oser)
        name = name.split("(")
        name = name[0]
        print('Profile created for username:', name)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.oser.save()
    print('saved')

from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUsers, Profile


@receiver(post_save, sender=CustomUsers)
def post(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

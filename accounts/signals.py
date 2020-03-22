from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Team, Membership
from budgeting.models import Expense


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Expense)
def change_balance(sender, instance, created, **kwargs):
    if created:
        profile = instance.user
        membership = Membership.objects.filter(profile=profile).first()
        if membership:
            team = membership.team
            team.balance += instance.amount
            team.save()
        
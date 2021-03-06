from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile, Team, Membership
from budgeting.models import Expense

from expense_tracker.utils import color_picker


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, color=color_picker())

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Expense)
def change_balance(sender, instance, created, **kwargs):
    if created:
        team = instance.team
        if team:
            team.balance += instance.amount
            team.save()

@receiver(pre_delete, sender=Expense)
def deleted_expense(sender, instance, **kwargs):
    team = instance.team
    if team:
        team.balance -= instance.amount
        team.save()

        
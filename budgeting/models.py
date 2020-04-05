from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import Profile, Team

from expense_tracker.utils import color_picker


class Category(models.Model):
    title = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='red')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Expense(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='for_team', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Category)
def category_pre_save_signal(sender, instance, **kwargs):
    if instance.color=='red':
        instance.color = color_picker()
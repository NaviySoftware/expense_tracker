from django.db import models

from accounts.models import Profile, Team


class Category(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Expense(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    categor = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='for_team', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
from django.db import models

from accounts.models import Profile

class Expense(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
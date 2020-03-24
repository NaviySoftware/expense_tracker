from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg')

    def __str__(self):
        return self.user.username


class Team(models.Model):
    title = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)
    members = models.ManyToManyField(Profile, through='Membership')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Membership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)


class MemberRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'from {self.from_user.username} to {self.to_user.username}'
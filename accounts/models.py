from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

from expense_tracker.utils import color_picker

today = timezone.now()


class ProfileManager(models.Manager):
    def expenses_per_year(self, user):
        return self.filter(user=user).annotate(year=TruncYear('expense__created'), sum=Sum('expense__amount')).order_by('year')

    def expenses_per_month(self, user):
        return self.filter(user=user).annotate(month=TruncMonth('expense__created'), sum=Sum('expense__amount')).order_by('month')

    def expenses_per_day(self, user):
        return self.filter(user=user).annotate(day=TruncDay('expense__created'), sum=Sum('expense__amount')).order_by('day')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=20, default='green')
    image = models.ImageField(default='default.jpg')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    @property
    def all_teams(self):
        if self.team_set.all():
            return self.team_set.all()[0]
        return False

        
class Team(models.Model):
    title = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)
    members = models.ManyToManyField(Profile, through='Membership')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def all_expenses(self):
        return self.for_team.all().order_by('-created')

    @property
    def percentage(self):
        members = []
        t_exps = self.all_expenses.aggregate(summary=Sum('amount'))
        team_members = self.members.all()
        for member in team_members:
            m_exps = member.expense_set.aggregate(summary=Sum('amount'))
            if m_exps['summary'] != 0 and m_exps['summary'] is not None:
                perc = round(m_exps['summary']/t_exps['summary']*100)
            else:
                perc = 0
            members.append(
                {'name': member.user.username, 
                'perc': perc, 
                'color': color_picker()})
        return members



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
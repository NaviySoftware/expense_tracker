from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Sum, Case, When, IntegerField
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

today = timezone.now()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=20, default='green')
    image = models.ImageField(default='default.jpg')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})

    @property
    def team(self):
        if self.team_set.all():
            return self.team_set.all()[0]
        return False

    @property
    def all_expenses(self):
        return self.expense_set.all()

    @property
    def current_year_exps(self):
        return self.expense_set.filter(
                created__year=today.year).aggregate(
                    summary=Sum('amount'))

    @property
    def current_month_exps(self):
        return self.expense_set.filter(
            created__month=today.month).aggregate(
                summary=Sum('amount'))

    @property
    def today_exps(self):
        return self.expense_set.filter(
            created__day=today.day).aggregate(summary=Sum('amount'))

    @property
    def expenses_per_day(self):
        return self.expense_set.annotate(
            day=TruncDay('created'), sum=Sum('amount')).order_by('day')

        
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
    def sum_of_current_year(self):
        return self.for_team.filter(created__year=today.year).aggregate(summary=Sum('amount'))

    @property
    def team_category_exps_monthly(self):
        return self.for_team.values(
            'category__title', 'category__color').annotate(
                month=TruncMonth('created'), summary=Sum('amount'))
    
    @property
    def team_members_exps(self):
        return self.members.annotate(year = Case(
                    When(expense__created__year=today.year, then=today.year), 
                    default=0, 
                    output_field=IntegerField())
                    ).filter(year=today.year).annotate(sum=Sum('expense__amount'))

    @property
    def team_month_exp(self):
        return self.members.annotate(
                    month=TruncMonth('expense__created'), 
                    summary=Sum('expense__amount'))


class Membership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)


class MemberRequest(models.Model):
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_user')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'from {self.from_user.user.username} to {self.to_user.user.username}'
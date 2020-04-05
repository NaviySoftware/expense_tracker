from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum, Count, Max, When, Case, Value, IntegerField
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
import datetime

from .models import Profile, Team
from expense_tracker.utils import color_picker

def maximum(exps):
    e_max = 0
    for exp in exps:
        if exp['summary'] > e_max:
            e_max = exp['summary']
    return e_max

@login_required
def dashboard(request):
    today = timezone.now()
    profile = get_object_or_404(Profile, user=request.user)
    team = profile.all_teams
    team_expenses = team.all_expenses

    team_members_exps = team.members.annotate(year = Case(
        When(expense__created__year=today.year, then=today.year), 
        default=0, 
        output_field=IntegerField())).filter(year=today.year).annotate(sum=Sum('expense__amount'))

    lebel_months = []
    members_monthly_exps = []


    for member in team.members.all():
        qs = Profile.objects.expenses_per_month(member.user)
        clr = member.color
        member_qs = []
        for exp in qs:
            user = get_object_or_404(User, id=exp.user_id)
            month = exp.month
            summary = exp.sum
            if month not in lebel_months and month is not None:
                lebel_months.append(month)
            if month is not None and summary is not None:                
                member_qs.append({
                    'user': user.username, 
                    'clr': clr, 
                    'month': month, 
                    'summary': summary})
        if member_qs:
            members_monthly_exps.append(member_qs)

    user_category_exps_year = profile.expense_set.values('category__title', 'category__color').filter(created__year=today.year).annotate(summary=Sum('amount'))

    user_category_exps_monthly = profile.expense_set.values('category__title', 'category__color').annotate(month=TruncMonth('created'), summary=Sum('amount'))

    team_category_exps_monthly = team.for_team.values('category__title', 'category__color').annotate(month=TruncMonth('created'), summary=Sum('amount'))
    
    context={
        'team': team,
        'team_members_exps': team_members_exps,
        'profile': profile,
        'expenses': team_expenses,
        'exps_year': Profile.objects.expenses_per_year(request.user),
        'exps_month': Profile.objects.expenses_per_month(request.user),
        'exps_day': Profile.objects.expenses_per_day(request.user),
        'members_exps': members_monthly_exps,
        'm_lebel': lebel_months,
        'user_category_exps_year': user_category_exps_year,
        'user_category_exps_monthly': user_category_exps_monthly,
        'team_category_exps_monthly': team_category_exps_monthly,

    }

    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    today = timezone.now()
    user_profile = Profile.objects.filter(user=request.user).first()

    expenses = user_profile.expense_set.annotate(
        field = Case(
            When(created__year=today.year, then=1),
            When(created__month=today.month, then=2),
            When(created__day=today.day, then=3),
            default=0,
            output_field=IntegerField()
        )
    )

    curent_month_expenses = expenses.filter(created__month=today.month)

    expenses_per_day = expenses.values(
        day=TruncDay('created')).annotate(
            expenses=Count('id'), summary=Sum('amount')
        ).order_by('day')

    expenses_per_month = expenses.values(
        month=TruncMonth('created')).annotate(
            expenses=Count('id'), summary=Sum('amount')
        ).order_by('month')

    expenses_per_year = expenses.values(
        year=TruncYear('created')).annotate(
            expenses=Count('id'), summary=Sum('amount')
        ).order_by('year')

    context = {
        'profile': user_profile,
        'curent_month_expenses': curent_month_expenses,
        'yearly_expenses': expenses_per_year,
        'dayly_expenses': expenses_per_day,
        'monthly_expenses': expenses_per_month,
        'month_max': maximum(expenses_per_month),
        'day_max': maximum(expenses_per_day),
    }

    return render(request, 'accounts/profile.html', context)


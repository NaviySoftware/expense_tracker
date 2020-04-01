from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Max, When, Case, Value, IntegerField
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
import datetime

from .models import Profile, Team

def maximum(exps):
    e_max = 0
    for exp in exps:
        if exp['summary'] > e_max:
            e_max = exp['summary']
    return e_max


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
            order_by=('created'),
            output_field=IntegerField()
        )
    )

    curent_month_expenses = expenses.filter(created__month=today.month)

    expenses_per_day = expenses.annotate(
        day=TruncDay('created')).values('day').annotate(
            expenses=Count('id'), summary=Sum('amount')
        ).order_by('day').values('day', 'expenses', 'summary')

    expenses_per_month = expenses.annotate(
        month=TruncMonth('created')).values('month').annotate(
            expenses=Count('id'), summary=Sum('amount')
        ).order_by('month').values('month', 'expenses', 'summary')

    expenses_per_year = expenses.annotate(
        year=TruncYear('created')).values('year').annotate(
            expenses=Count('id'), summary=Sum('amount')
        ).order_by('year').values('year', 'expenses', 'summary')

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

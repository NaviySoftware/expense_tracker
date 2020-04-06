from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum, When, Case, IntegerField
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

from .models import Profile, Team

@login_required
def dashboard(request):
    today = timezone.now()
    label_months = []
    profile = get_object_or_404(Profile, user=request.user)
    team = profile.team
    
    user_category_exps_year = profile.expense_set.values(
        'category__title', 'category__color').filter(
            created__year=today.year).annotate(
                summary=Sum('amount'))

    user_category_exps_monthly = profile.expense_set.values(
        'category__title', 'category__color').annotate(
            month=TruncMonth('created'), summary=Sum('amount'))

    # for take  expenses created months for chartjs
    for exp in user_category_exps_monthly:
        month = exp['month']
        if month not in label_months:
            label_months.append(month)

    context={
        'team': team,
        'profile': profile,
        'm_lebel': label_months,
        'user_category_exps_year': user_category_exps_year,
        'user_category_exps_monthly': user_category_exps_monthly,
    }

    return render(request, 'accounts/dashboard.html', context)

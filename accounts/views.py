from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum, When, Count, Case, IntegerField, Q
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

from .models import Profile, Team, Membership, MemberRequest
from .forms import CreateTeamForm, UserSearchForm
from budgeting.forms import AddExpenseForm

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
        'form': AddExpenseForm(user=request.user)
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required
def team_members(request):
    profile = request.user.profile
    members = profile.team.members.annotate(summary=Sum('expense__amount'), exps=Count('expense__id'))

    context = {
        'members': members,
    }
    return render(request, 'accounts/team.html', context)

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    membership_from = MemberRequest.objects.filter(from_user=profile)
    membership_to = MemberRequest.objects.filter(to_user=request.user.profile)
    form = CreateTeamForm()
    context = {
        'profile': profile,
        'form': form,
        'membership_from': membership_from,
        'membership_to': membership_to,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def create_team(request):
    form = CreateTeamForm(request.POST)
    profile = request.user.profile

    if form.is_valid() and not profile.team:
        team = form.save()
        team.members.add(profile)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return redirect(profile)

@login_required
def leave_team(request):
    team_id = request.POST.get('team_id')

    if team_id is not None:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return redirect('dashboard') 
        
        if team.members.count() == 1:
            team.delete()
        else:
            team.members.remove(request.user.profile)

    return redirect(request.user.profile)
        
@login_required
def membership_request(request):
    user_id = request.POST.get('user_id')

    if user_id is not None:
        user = get_object_or_404(User, id=user_id)
        obj, created = MemberRequest.objects.get_or_create(
                        from_user=request.user.profile, 
                        to_user=user.profile)
        if created:
            obj.save()

    return redirect(request.user.profile)

@login_required
def cancel_request(request):
    user_id = request.POST.get('user_to_id')

    if user_id is not None:
        user_to = get_object_or_404(User, id=user_id)
        mr = MemberRequest.objects.filter(to_user=user_to.profile, from_user=request.user.profile).first()
        mr.delete()
    return redirect(request.user.profile)

@login_required
def accept_request(request):
    user_id = request.POST.get('user_from_id')

    if user_id is not None:
        user_from = get_object_or_404(User, id=user_id)
        mr = MemberRequest.objects.filter(to_user=request.user.profile, from_user=user_from.profile).first()
        if mr and user_from.profile.team:
            team = user_from.profile.team
            team.members.add(request.user.profile)
            mr.delete()
    return redirect(request.user.profile)

@login_required
def remove_request(request):
    user_id = request.POST.get('f_user_id')

    if user_id is not None:
        user_from = get_object_or_404(User, id=user_id)
        mr = MemberRequest.objects.filter(to_user=request.user.profile, from_user=user_from.profile).first()
        mr.delete()
    return redirect(request.user.profile)

@login_required
def search_users(request):
    qs = Profile.objects.none()    
    if request.method == 'GET':
        form = UserSearchForm(request.GET)
        if form.is_valid():
            username = form.cleaned_data['username']
            qs = Profile.objects.filter(
                Q(user__username__icontains = username), 
                user__is_active=True).exclude(user=request.user)

    form = UserSearchForm()
    context = {
        'form': form,
        'qs': qs,
    }
    return render(request, 'accounts/users_search.html', context)
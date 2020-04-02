from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import AddExpenseForm


@login_required
def add_expense(request):
    form = AddExpenseForm()
    context = {
        'form': form,
    }
    return render(request, 'budgeting/add-expense.html', context)

def save_expense(request):
    form = AddExpenseForm(request.POST)

    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user.profile
        if request.user.profile.all_teams:
            expense.team = request.user.profile.all_teams
        expense.save()
    
    return redirect('profile')


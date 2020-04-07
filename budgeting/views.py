from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Sum, Count

from .models import Expense, Category
from .forms import AddExpenseForm, CreateCategoryForm
from accounts.models import Profile


@login_required
def add_expense(request):
    form = AddExpenseForm(user=request.user)
    context = {
        'form': form,
    }
    return render(request, 'budgeting/add-expense.html', context)

@login_required
def save_expense(request):
    form = AddExpenseForm(request.POST)

    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user.profile
        if request.user.profile.team:
            expense.team = request.user.profile.team
        expense.save()
    
    return redirect('dashboard')

@login_required
def category_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    form = CreateCategoryForm()

    categories = profile.expense_set.values(
        'category__id', 'category__title', 'category__color').annotate(
                summary=Sum('amount'), items=Count('id')).order_by('-summary')

    empy_categories = profile.category_set.filter(expense=None)

    context = {
        'categories': categories,
        'empty': empy_categories,
        'form': form,
    }

    return render(request, 'budgeting/category_list.html', context)

@login_required
def add_category(request):
    form = CreateCategoryForm(request.POST)
    
    if form.is_valid():
        category = form.save()
        team = request.user.profile.team
        if team:
            category.users.add(*[member for member in team.members.all()])
        else:
            category.users.add(request.user.profile)

    return redirect('categories')

@login_required
def change_category(request):
    category_id = request.POST.get('category_id')
    category_title = request.POST.get('category_title')

    if category_id is not None:
        try:
            category = Category.objects.get(id=category_id)
            category.title=category_title
            category.save()
        except Category.DoesNotExist:
            return redirect('categories')
        
        return redirect('categories')

@login_required
def delete_category(request):
    category_id = request.POST.get('category_id')

    if category_id is not None:
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
        except Category.DoesNotExist:
            return redirect('categories')      

        return redirect('categories')


class ExpensesListView(ListView):
    model = Expense
    template_name = 'budgeting/all-expenses.html'
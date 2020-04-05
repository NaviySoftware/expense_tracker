from django.urls import path
from .views import add_expense, save_expense, ExpensesListView

urlpatterns = [
    path('add/', add_expense, name='add-expense'),
    path('save/', save_expense, name='save-expense'),
    path('all/', ExpensesListView.as_view(), name='all-expenses'),
]
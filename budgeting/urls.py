from django.urls import path
from .views import add_expense, save_expense

urlpatterns = [
    path('add/', add_expense, name='add-expense'),
    path('save/', save_expense, name='save-expense'),
]
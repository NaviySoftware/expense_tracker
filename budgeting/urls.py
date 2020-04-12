from django.urls import path
from .views import (save_expense, 
                    delete_expense,
                    category_list, 
                    add_category, 
                    delete_category, 
                    change_category,
                    ExpensesListView)

urlpatterns = [
    path('save/', save_expense, name='save-expense'),
    path('expenses/user/<str:username>', ExpensesListView.as_view(), name='all-expenses'),
    path('expenses/delete-expense', delete_expense, name='delete-expense'),
    path('categories/', category_list, name='categories'),
    path('categories/add-category', add_category, name='add-category'),
    path('categories/delete-category', delete_category, name='delete-category'),
    path('categories/change-category', change_category, name='change-category'),
]
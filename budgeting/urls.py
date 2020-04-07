from django.urls import path
from .views import (add_expense, 
                    save_expense, 
                    category_list, 
                    add_category, 
                    delete_category, 
                    change_category,
                    ExpensesListView)

urlpatterns = [
    path('add/', add_expense, name='add-expense'),
    path('save/', save_expense, name='save-expense'),
    path('all/', ExpensesListView.as_view(), name='all-expenses'),
    path('categories/', category_list, name='categories'),
    path('categories/add-category', add_category, name='add-category'),
    path('categories/delete-category', delete_category, name='delete-category'),
    path('categories/change-category', change_category, name='change-category'),
]
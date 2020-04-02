from django.forms import ModelForm
from .models import Expense

class AddExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'description', 'categor', 'amount']
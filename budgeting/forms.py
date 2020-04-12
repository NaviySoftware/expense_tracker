from django import forms
from .models import Expense, Category

class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'description', 'category', 'amount']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddExpenseForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'] = forms.ModelChoiceField(Category.objects.filter(users=user.profile), empty_label='Without category', required=False)


class CreateCategoryForm(forms.ModelForm):
    title = forms.CharField(label='',
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Category title', 
            'aria-label': 'Category title',
            'aria-describedby': 'button-addon2',
    }))
    
    class Meta:
        model = Category
        fields = ['title',]
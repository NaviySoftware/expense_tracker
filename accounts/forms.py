from django import forms

from .models import Team


class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['title',]

class UserSearchForm(forms.Form):
    username = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Search users',
            'aria-label': 'Search users',
            'aria-describedby': 'button-addon2'
        }))
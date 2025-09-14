from django import forms
from .models import CustomUser

# Example: a registration form
class ExampleForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'date_of_birth']


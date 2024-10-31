# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=[('taker', 'Survey Taker'), ('creator', 'Survey Creator')],
        widget=forms.RadioSelect,
        required=True,
        label='User Type'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterBasicInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']


class RegisterLoginInfoForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
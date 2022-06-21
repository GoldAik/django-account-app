from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    login = forms.CharField(
        max_length=30, 
        label=_("Username or email")
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                'id': 'password_input'
            }
        )
    )

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if '@' in login:
            email = login
            qs = User.objects.filter(email__iexact=email)
            if not qs.exists():
                raise forms.ValidationError("This is an invalid email")

        else:
            username = login
            qs = User.objects.filter(username__iexact=username)
            if not qs.exists():
                raise forms.ValidationError("This is an invalid username")
        
        return login


class RegisterBasicInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 3 and first_name:
            raise forms.ValidationError("To short first name")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 3 and last_name:
            raise forms.ValidationError("To short last name")
        return last_name


not_allowed_usernames = []

class RegisterLoginInfoForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 3:
            raise forms.ValidationError("To short username")

        if username in not_allowed_usernames:
            raise forms.ValidationError("This is an invalid username")

        return username